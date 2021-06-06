import re
from typing import Any, Tuple, Dict, Optional

from boltons.iterutils import remap
from pydantic import BaseModel, Extra, Field, validator


class BugbearViolation(BaseModel):
    """Violation defined by flake8-bugbear."""

    type: Any
    vars: Optional[tuple] = None

    code: str
    message: str

    extra: Optional[Dict[str, Any]] = None

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
                lambda path, key, value: (
                    key,
                    list(sorted(value)) if isinstance(value, set) else value,
                ),
            )

        return extra

    class Config:
        """Forbid extra arguments, - mostly for debugging sake."""

        extra = Extra.forbid
