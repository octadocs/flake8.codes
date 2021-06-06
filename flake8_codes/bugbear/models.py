import re
from typing import Any, Tuple, Dict, Optional

from boltons.iterutils import remap
from pydantic import BaseModel, Extra, Field, validator, root_validator


def validate_extra_item(path, key, value) -> Tuple[str, Any]:
    """Validate an item of `extra` dictionary."""
    if isinstance(value, set):
        return key, list(sorted(value))

    if isinstance(value, type):
        return key, value.__name__

    return key, value


class BugbearViolation(BaseModel):
    """Violation defined by flake8-bugbear."""

    type: Any
    vars: Optional[tuple] = None

    code: str
    message: str

    extra: Optional[Dict[str, Any]] = None
    title: Optional[str] = None

    @validator('message')
    def validate(cls, message: str) -> str:
        """Remove the code name from the message."""
        return re.sub(
            r'^(B\d+ )',
            '',
            message,
        )

    @validator('extra')
    def validate_extra(cls, extra):
        """
        Replace all `set` occurrences with `list`.

        This alleviates the !!set tag in YAML output which breaks JSON-LD
        processing and generally looks dirty. We do not need it.
        """
        if isinstance(extra, dict):
            return remap(
                extra,
                validate_extra_item,
            )

        return extra

    @validator('title', always=True)
    def fill_title(cls, title, values):
        message: str = values['message']

        title = re.split(
            r'\. ', message,
            maxsplit=1,
        )[0].replace('`', '').replace('{}', '_')

        return title

    class Config:
        """Forbid extra arguments, - mostly for debugging sake."""

        extra = Extra.forbid
