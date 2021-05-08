from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


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
    internal_name: str = Field(alias='internalName')
    title: str
    description: str
    output_file: Path

    class Config:
        allow_population_by_field_name = True
