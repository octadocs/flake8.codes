import concurrent.futures
import re
import textwrap
from importlib import import_module
from pathlib import Path

import frontmatter
import pypandoc
from pydantic import BaseModel
from wemake_python_styleguide import violations
from wemake_python_styleguide.version import pkg_version

from flake8_codes.wps_configuration_defaults import \
    generate_wps_configuration_defaults


class Violation(BaseModel):
    """Violation description."""

    code: int
    title: str
    description: str
    output_file: Path


def format_violation_description(description: str) -> str:
    """Format violation description properly."""
    # The description is originally a docstring, need to remote indentation.
    description = textwrap.dedent(description)

    # Sometimes `{{` is met in Python examples, which breaks Jinja2 templating.
    # FIXME: just wrap Python examples into {% raw %} instead.
    description = description.replace(
        '{{', "{{ '{{' }}",
    )

    # Fix misprints. It seems a solitary ` is invalid in ReST: they should go
    # in pairs.
    #   TODO: file a PR for WPS461.
    # description = re.sub(
    #     ' `{1}',
    #     ' ``',
    #     description,
    # )
    # description = description.replace(' `', ' ``')

    # Replace the added-value Sphinx plugin embeds with our Jinja2 macro calls.
    description = re.sub(
        ':str:`([^`]+)`',
        r"``python://\g<1>``",
        description,
    )

    # Convert to Markdown and be done
    return pypandoc.convert_text(
        source=description,
        to='commonmark',
        format='rst',
    )


def generate_violation_file(violation: Violation) -> None:
    """Store violation description into a Markdown file with meta."""
    # Here is the heavy I/O operation with pandoc
    description = format_violation_description(violation.description)

    md = frontmatter.Post(
        content=description,
        handler=frontmatter.YAMLHandler(),
        **violation.dict(include={'code', 'title'}),
    )

    with open(violation.output_file, 'wb+') as code_file:
        frontmatter.dump(md, code_file)


def generate_wps_violations():
    """Generate docs for installed version of wemake-python-styleguide."""
    version_directory = Path(
        __file__,
    ).parent / 'docs/wemake-python-styleguide' / pkg_version / 'violations'
    version_directory.mkdir(parents=True, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # This cycle is adapted from flakehell
        for path in Path(violations.__path__[0]).iterdir():
            module = import_module(
                'wemake_python_styleguide.violations.' + path.stem,
            )
            for checker_name in dir(module):
                if not checker_name.endswith('Violation'):
                    continue
                checker = getattr(module, checker_name)
                if not hasattr(checker, 'code'):
                    continue

                code = checker.code
                output_file = version_directory / f'WPS{code:03}.md'

                violation = Violation(
                    code=code,
                    title=checker.error_template,
                    description=checker.__doc__,
                    output_file=output_file,
                )

                executor.submit(
                    generate_violation_file,
                    violation,
                )


def main():
    generate_wps_violations()
    generate_wps_configuration_defaults()


if __name__ == '__main__':
    main()
