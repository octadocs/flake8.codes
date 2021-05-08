from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class WPSConfigurationParameter(BaseModel):
    """WPS configuration parameter with its default value and meta data."""

    about: str
    name: str
    cli_name: str
    value: str
    description: str
    reasoning: Optional[str] = None


class Violation(BaseModel):
    """Violation description."""

    code: int
    name: str
    title: str
    description: str
    output_file: Path
