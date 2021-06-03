import textwrap
from importlib import import_module
from pathlib import Path
from typing import Iterator

import frontmatter
from wemake_python_styleguide import violations

from flake8_codes.models import Violation
from flake8_codes.wemake_python_styleguide.violations.format_example_section import \
    FormatExampleSection
from flake8_codes.wemake_python_styleguide.violations.format_sections import \
    FormatSections
from flake8_codes.wemake_python_styleguide.violations.format_title import \
    FormatTitle
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


def format_violation_document(violation: Violation) -> Violation:
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

    violation = FormatTitle(violation=violation).process()
    violation = FormatSections(violation=violation).process()
    violation = FormatExampleSection(violation=violation).process()

    return violation


def document_violations_module_index(module, path: Path) -> None:
    """Write index.md file for a module from its docstring."""
    description = module.__doc__

    if not description:
        return

    try:
        path.write_text(description)
    except FileNotFoundError:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(description)


def write_violations_to_disk(
    violations: Iterator[Violation],
    directory: Path,
) -> None:
    for violation in violations:
        violation_path = directory / f'{violation.readable_code}.md'
        document = frontmatter.Post(
            content=violation.description,
            handler=frontmatter.YAMLHandler(),
            **violation.dict(
                exclude={'description', 'output_file'},
                by_alias=True,
                exclude_none=True,
            ),
        )

        with open(violation_path, 'wb+') as code_file:
            frontmatter.dump(document, code_file)


def document_violations_module(
    target_directory: Path,
    module_name: str,
) -> None:
    """Document a submodule of wemake_python_styleguide.violations."""
    if module_name == 'base':
        return

    module_path = f'wemake_python_styleguide.violations.{module_name}'
    module = import_module(module_path)

    module_directory = target_directory / module_name
    document_violations_module_index(
        module=module,
        path=module_directory / 'index.md',
    )

    violation_instances = extract_violations_from_module(module)
    violations = map(
        format_violation_document,
        violation_instances,
    )

    write_violations_to_disk(
        violations=violations,
        directory=module_directory,
    )


def extract_violations_from_module(module) -> Iterator[Violation]:
    """
    Retrieve Violation objects from given module.

    Idea was sourced from `flakehell`:
        https://github.com/life4/flakehell/blob/master/flakehell/
        _logic/_extractors.py#L389
    """
    for violation_class_name in dir(module):
        if not violation_class_name.endswith('Violation'):
            continue

        violation_class = getattr(module, violation_class_name)
        if not hasattr(violation_class, 'code'):
            continue

        code = violation_class.code
        yield Violation(
            code=code,
            internal_name=violation_class_name,
            title=violation_class.error_template,
            description=violation_class.__doc__,
        )


def document_wps_violations(directory: Path):
    """Generate docs for installed version of wemake-python-styleguide."""
    violations_module_files = Path(violations.__file__).parent

    for module_path in violations_module_files.iterdir():
        document_violations_module(
            target_directory=directory,
            module_name=module_path.stem,
        )
