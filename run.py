from pathlib import Path

from flake8_codes.wemake_python_styleguide.violations.main import (
    generate_wps_violations,
)

from flake8_codes.wemake_python_styleguide.options import (
    generate_wps_options,
)

from wemake_python_styleguide.version import pkg_version


def main():
    docs = Path(__file__).parent / 'docs/wemake-python-styleguide' / pkg_version
    generate_wps_violations(docs / 'violations')
    generate_wps_options(docs / 'configuration')


if __name__ == '__main__':
    main()
