from pathlib import Path


def create_empty_index_md_in_directory(directory: Path) -> None:
    try:
        (directory / 'index.md').write_text('')
    except FileNotFoundError:
        directory.mkdir(parents=True, exist_ok=True)
        create_empty_index_md_in_directory(directory=directory)
