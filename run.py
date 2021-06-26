from pathlib import Path

from wemake_python_styleguide import constants
from wemake_python_styleguide.version import pkg_version

from flake8_codes.bugbear.main import document_bugbear
from flake8_codes.stubs import create_empty_index_md_in_directory
from flake8_codes.wemake_python_styleguide.constants.main import (
    generate_constants
)
from flake8_codes.wemake_python_styleguide.options import (
    generate_wps_options,
)
from flake8_codes.wemake_python_styleguide.violations.main import (
    document_wps_violations,
)


def document_wps(path: Path) -> None:
    (path / 'index.md').write_text('')


def document_wemake_python_styleguide():
    wps = Path(__file__).parent / 'docs/wemake-python-styleguide'
    create_empty_index_md_in_directory(wps)

    docs = wps / pkg_version
    create_empty_index_md_in_directory(docs)

    generate_constants(
        constants=constants,
        destination=docs / 'constants',
    )
    document_wps_violations(docs / 'violations')
    generate_wps_options(docs / 'configuration')


def main() -> None:
    document_bugbear()
    document_wemake_python_styleguide()


if __name__ == '__main__':
    main()
