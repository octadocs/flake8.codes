from pathlib import Path

from wemake_python_styleguide import constants

from flake8_codes.wemake_python_styleguide.constants.main import \
    generate_constants
from flake8_codes.wemake_python_styleguide.versions import document_wps_version
from flake8_codes.wemake_python_styleguide.violations.main import (
    document_wps_violations,
)

from flake8_codes.wemake_python_styleguide.options import (
    generate_wps_options,
)

from wemake_python_styleguide.version import pkg_version


def main():
    docs = Path(__file__).parent / 'docs/wemake-python-styleguide' / pkg_version

    document_wps_version(docs)
    generate_constants(
        constants=constants,
        destination=docs / 'constants',
    )
    document_wps_violations(docs / 'violations')
    generate_wps_options(docs / 'configuration')


if __name__ == '__main__':
    main()
