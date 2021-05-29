from typing import Any, Union

from documented import DocumentedError
from libcst import BaseCompoundStatement, SimpleStatementLine
from pydantic import BaseModel, stricturl

BodyStatement = Union[SimpleStatementLine, BaseCompoundStatement]


PythonIRI = stricturl(allowed_schemes={'python'}, tld_required=False)


class WPSConstant(BaseModel):
    """WPS constant description."""

    name: str
    about: PythonIRI
    description: str
    value: Any


class GenerationFailed(DocumentedError):
    """Generation of a WPSConstant has failed."""


class NotAnAssignment(GenerationFailed):
    """This is not an assignment."""


class NotPublicConstant(GenerationFailed):
    """This constant is not public."""
