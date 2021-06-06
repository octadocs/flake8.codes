from typing import Any, Tuple, Dict, Optional

from pydantic import BaseModel, Extra, Field


class BugbearViolation(BaseModel):
    """Violation defined by flake8-bugbear."""

    type: Any
    vars: tuple

    code: str
    message: str

    extra: Optional[Dict[str, Any]] = None

    class Config:
        extra = Extra.forbid
