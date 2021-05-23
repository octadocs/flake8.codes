import concurrent.futures
import textwrap
from importlib import import_module
from pathlib import Path

import frontmatter
from wemake_python_styleguide import violations

from flake8_codes.models import Violation
from flake8_codes.wemake_python_styleguide.violations.format_title import \
    FormatTitle
from flake8_codes.wemake_python_styleguide.violations.import_macros import \
    ImportMacros
from flake8_codes.wemake_python_styleguide.violations.pypandoc_conversion import \
    Pypandoc
from flake8_codes.wemake_python_styleguide.violations.related_violations import \
    RelatedViolations
from flake8_codes.wemake_python_styleguide.violations.unpaired_quote import \
    UnpairedQuote
from flake8_codes.wemake_python_styleguide.violations.wps_config import \
    WPSConfig
from flake8_codes.wemake_python_styleguide.violations.wps_constant import \
    WPSConstants


def format_violation_description(description: str) -> str:
    """Format violation description properly."""
    # The description is originally a docstring, need to remote indentation.
    description = textwrap.dedent(description)

    # Sometimes `{{` is met in Python examples, which breaks Jinja2 templating.
    # FIXME: just wrap Python examples into {% raw %} instead.
    description = description.replace(
        '{{', "{{ '{{' }}",
    )

    description = description.replace(
        ':py:class:',
        ':class:',
    )

    return description


def generate_violation_file(violation: Violation) -> None:
    """Store violation description into a Markdown file with meta."""
    # Ugly transformations
    description = format_violation_description(
        violation.description,
    )
    violation.description = description

    # Nice transformations
    violation = UnpairedQuote(violation=violation).process()
    violation = Pypandoc(violation=violation).process()

    # Insert macro links
    violation = WPSConfig(violation=violation).process()
    violation = WPSConstants(violation=violation).process()
    violation = RelatedViolations(violation=violation).process()

    violation = ImportMacros(violation=violation).process()
    violation = FormatTitle(violation=violation).process()

    md = frontmatter.Post(
        content=violation.description,
        handler=frontmatter.YAMLHandler(),
        **violation.dict(
            exclude={'description', 'output_file'},
            by_alias=True,
            exclude_none=True,
        ),
    )

    with open(violation.output_file, 'wb+') as code_file:
        frontmatter.dump(md, code_file)


def generate_wps_violations(directory: Path):
    """Generate docs for installed version of wemake-python-styleguide."""
    directory.mkdir(parents=True, exist_ok=True)

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # This cycle is adapted from flakehell
        for path in Path(violations.__path__[0]).iterdir():
            module = import_module(
                'wemake_python_styleguide.violations.' + path.stem,
            )
            module_directory = directory / path.stem
            module_directory.mkdir(parents=True, exist_ok=True)

            for checker_name in dir(module):
                if not checker_name.endswith('Violation'):
                    continue
                checker = getattr(module, checker_name)
                if not hasattr(checker, 'code'):
                    continue

                code = checker.code
                output_file = module_directory / f'WPS{code:03}.md'

                violation = Violation(
                    code=code,
                    internal_name=checker_name,
                    title=checker.error_template,
                    description=checker.__doc__,
                    output_file=output_file,
                    related_violations=[],
                )

                results.append(executor.submit(
                    generate_violation_file,
                    violation,
                ))

    for future in results:
        future.result()
