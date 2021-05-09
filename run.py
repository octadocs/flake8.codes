from flake8_codes.wemake_python_styleguide.violations.main import (
    generate_wps_violations,
)

from flake8_codes.wemake_python_styleguide.options import (
    generate_wps_options,
)


def main():
    generate_wps_violations()
    generate_wps_options()


if __name__ == '__main__':
    main()
