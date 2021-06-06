from pathlib import Path


def document_wps_version(directory: Path) -> None:
    """Create index.md file at every WPS version directory."""
    (directory / 'index.md').write_text('')
