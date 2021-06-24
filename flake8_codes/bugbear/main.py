import functools
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable, Tuple

import bugbear
import frontmatter

from flake8_codes.bugbear.models import BugbearViolation
from flake8_codes.stubs import create_empty_index_md_in_directory


def bugbear_violation_objects() -> Iterable[Tuple[str, functools.partial]]:
    return (
        (name, partial_object)
        for name, partial_object
        in vars(bugbear).items()
        if (
            isinstance(partial_object, functools.partial) and
            name.startswith('B')
        )
    )


def bugbear_violations() -> Iterable[BugbearViolation]:
    for code, partial_object in bugbear_violation_objects():
        yield BugbearViolation(
            code=code,
            extra=vars(partial_object) or None,
            **partial_object.keywords,
        )


def document_violation(
    version_directory: Path,
    violation: BugbearViolation,
) -> None:
    """Write violation description into a Markdown file."""
    document = frontmatter.Post(
        content=violation.message,
        handler=frontmatter.YAMLHandler(),
        **violation.dict(
            exclude={'message', 'type', 'vars'},
            exclude_none=True,
        )
    )

    (version_directory / f'{violation.code}.md').write_text(
        frontmatter.dumps(document),
    )


def document_bugbear():
    """Generate a bunch of documentation files for flake8-bugbear."""
    version = bugbear.__version__

    bugbear_directory = Path(__file__).parent.parent.parent / 'docs/flake8-bugbear'
    create_empty_index_md_in_directory(bugbear_directory)

    version_directory = bugbear_directory / version

    create_empty_index_md_in_directory(version_directory)

    violations = list(bugbear_violations())

    for violation in violations:
        document_violation(
            version_directory=version_directory,
            violation=violation,
        )
