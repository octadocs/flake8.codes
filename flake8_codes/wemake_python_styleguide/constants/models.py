from typing import Union, Any

from documented import DocumentedError
from libcst import SimpleStatementLine, BaseCompoundStatement
from pydantic import BaseModel

BodyStatement = Union[SimpleStatementLine, BaseCompoundStatement]


class WPSConstant(BaseModel):
    """WPS constant description."""

    name: str
    description: str
    value: Any


class GenerationFailed(DocumentedError):
    """Generation of a WPSConstant has failed."""


class NotAnAssignment(GenerationFailed):
    """This is not an assignment."""


class NotPublicConstant(GenerationFailed):
    """This constant is not public."""
