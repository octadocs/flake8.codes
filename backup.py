import operator
import shutil
from pathlib import Path

from more_itertools import consume

DIRECTORIES = ('flake8-bugbear', 'flake8-bandit', 'wemake-python-styleguide')


def backup(path: Path):
    backup_directory = Path(__file__).parent / 'backup'
    backup_directory.mkdir(parents=True, exist_ok=True)

    package_name = path.parent.name
    version_name = path.name
    shutil.move(
        path,
        backup_directory / package_name / version_name,
    )


def main():
    docs_dir = Path(__file__).parent / 'docs'

    for directory_name in DIRECTORIES:
        versions = filter(
            operator.methodcaller('is_dir'),
            (docs_dir / directory_name).iterdir()
        )

        versions_to_backup = list(sorted(versions))[:-1]

        consume(map(backup, versions_to_backup))


if __name__ == '__main__':
    main()
