from pathlib import Path

import frontmatter
from packaging import version


def create_empty_index_md_in_directory(directory: Path) -> None:
    try:
        (directory / 'index.md').write_text('')
    except FileNotFoundError:
        directory.mkdir(parents=True, exist_ok=True)
        create_empty_index_md_in_directory(directory=directory)


def create_version_index_md(docs: Path, package_version: str) -> None:
    """Write version description."""
    v = version.parse(package_version)
    post = frontmatter.Post(
        content='',
        handler=frontmatter.YAMLHandler(),

        major_version=v.major,
        minor_version=v.minor,
        patch_version=v.micro,
    )

    post_content = frontmatter.dumps(post)
    text_content = f'{post_content}\n\n'

    try:
        (docs / 'index.md').write_text(text_content)
    except FileNotFoundError:
        docs.mkdir(parents=True, exist_ok=True)
        (docs / 'index.md').write_text(text_content)
