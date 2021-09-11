import itertools
import json
from pathlib import Path
from typing import Iterator

import pbr.version
from bandit.blacklists.calls import gen_blacklist as gen_calls_blacklist
from bandit.blacklists.imports import gen_blacklist as gen_imports_blacklist
from flake8_codes.models import Violation
from flake8_codes.stubs import (
    create_empty_index_md_in_directory,
    create_version_index_md,
)
from flake8_codes.transforms.extract_code_and_title import ExtractCodeAndTitle
from flake8_codes.transforms.pypandoc_conversion import Pypandoc
from flake8_codes.transforms.replace import Replace
from flake8_codes.wemake_python_styleguide.violations.main import \
    write_violations_to_disk
from pytkdocs.cli import process_config
from returns.pipeline import flow


def violations_docstrings() -> Iterator[str]:
    """Document currently installed version of bandit."""
    config = {
        'objects': [{
            'path': 'bandit.plugins',
            'new_path_syntax': True,
            'inherited_members': True,
            'docstring_style': 'restructured-text',
        }],
    }

    pytkdocs_response = process_config(config)

    if pytkdocs_response['loading_errors']:
        raise ValueError(pytkdocs_response['loading_errors'])

    if pytkdocs_response['parsing_errors']:
        raise ValueError(pytkdocs_response['parsing_errors'])

    modules = list(pytkdocs_response['objects'][0]['children'].values())

    for module in modules:
        violations = module['children'].values()
        for violation in violations:
            if docstring := violation['docstring'] or module['docstring']:
                yield docstring


def blacklist_item_to_violation(blacklist) -> Violation:
    """Parse flake8-bandit blacklist object into violations stream."""
    return Violation(
        code=blacklist['id'].replace('B', 'S'),
        title=blacklist['message'],
        description='\n'.join(
            f' * `{qualname}`' for qualname in blacklist['qualnames']
        ),
    )


def docstring_to_violation(docstring: str) -> Violation:
    """Clean up and parse the docstring into Violation instance."""
    violation = Violation(
        description=docstring,
        code='',
        internal_name='',
        title='',
    )

    violation = flow(
        violation,

        # It appears the .. seealso:: block is invalid and is skipped
        Replace(find='\.\. seealso::', replace='See Also::'),

        Pypandoc(),

        # Convert .. [1] lists to Markdown lists
        Replace(find=r' +.. \[\d+\]', replace='*'),

        # Replace ``` sourceCode yaml with just ```yaml for mkdocs compatibility
        Replace(find=' sourceCode ', replace=''),

        # ```none is not a valid lang specifier.
        Replace(find='```none', replace='```'),

        ExtractCodeAndTitle(),
    )

    return violation


def bandit_version() -> str:
    return pbr.version.VersionInfo('bandit').version_string()


def document_flake8_bandit(docs_dir: Path) -> None:
    """Document currently installed version of bandit."""
    package_dir = docs_dir / 'flake8-bandit'
    create_empty_index_md_in_directory(package_dir)

    docstrings = violations_docstrings()
    violations = itertools.chain(
        map(docstring_to_violation, docstrings),
        map(blacklist_item_to_violation, gen_calls_blacklist()['Call']),
        map(blacklist_item_to_violation, gen_imports_blacklist()['Call']),
    )

    version = bandit_version()
    version_dir = package_dir / version
    create_version_index_md(
        docs=version_dir,
        package_version=version,
    )

    write_violations_to_disk(
        violations=violations,
        directory=version_dir,
    )
