from pathlib import Path

from flake8_codes.bandit.main import document_flake8_bandit
from flake8_codes.bugbear.main import document_bugbear
from flake8_codes.wemake_python_styleguide.main import (
    document_wemake_python_styleguide
)


def main() -> None:
    root = Path(__file__).parent
    docs_dir = root / 'docs'

    document_flake8_bandit(docs_dir=docs_dir)
    # document_bugbear()
    # document_wemake_python_styleguide()


if __name__ == '__main__':
    main()
