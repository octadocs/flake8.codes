from typing import Union, Any

from documented import DocumentedError
from libcst import SimpleStatementLine, BaseCompoundStatement
from pydantic import BaseModel, stricturl, constr
from urlpath import URL

BodyStatement = Union[SimpleStatementLine, BaseCompoundStatement]


PythonIRI = constr(regex=r'^python:[a-zA-Z0-9_\.]+')


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
