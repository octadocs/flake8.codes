import textwrap
from importlib import import_module
from pathlib import Path

import frontmatter
from pydantic import Field, BaseModel, validator
from wemake_python_styleguide import violations
from wemake_python_styleguide.version import pkg_version


class Violation(BaseModel):
    """Violation description."""

    code: int = Field(title='Error Code.')
    title: str
    description: str = ''

    @validator('description')
    def validate_description(cls, description: str) -> str:
        """Format the description."""
        return textwrap.dedent(description)


def generate_wps():
    version_directory = Path(__file__).parent / 'docs/wemake-python-styleguide' / pkg_version
    version_directory.mkdir(parents=True, exist_ok=True)

    # This code is from flakehell
    codes = dict()
    for path in Path(violations.__path__[0]).iterdir():
        module = import_module('wemake_python_styleguide.violations.' + path.stem)
        for checker_name in dir(module):
            if not checker_name.endswith('Violation'):
                continue
            checker = getattr(module, checker_name)
            if not hasattr(checker, 'code'):
                continue
            code = 'WPS' + str(checker.code).zfill(3)
            codes[code] = checker.error_template

            violation = Violation(
                code=checker.code,
                title=checker.error_template,
                description=checker.__doc__,
            )

            md = frontmatter.Post(
                content=violation.description,
                handler=frontmatter.YAMLHandler(),
                **violation.dict(include={'title', 'code'}),
            )

            with open(version_directory / f'{code}.md', 'wb+') as code_file:
                frontmatter.dump(md, code_file)

    return codes


def main():
    generate_wps()


if __name__ == '__main__':
    main()
