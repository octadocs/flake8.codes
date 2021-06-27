from flake8_codes.bugbear.main import document_bugbear
from flake8_codes.wemake_python_styleguide.main import (
    document_wemake_python_styleguide
)


def main() -> None:
    document_bugbear()

    try:
        document_wemake_python_styleguide()
    except ModuleNotFoundError:
        print('Warning: wemake-python-styleguide is probably not installed.')


if __name__ == '__main__':
    main()
