from re import Pattern
from typing import Any, List, Set
from classes import typeclass
from pydantic import BaseModel, Field


def identity(instance):
    """Return argument."""
    return instance


@typeclass
def semanticize(instance: Any) -> Any:
    """Convert a Python object into a semantic description."""


semanticize.instance(int)(identity)
semanticize.instance(float)(identity)
semanticize.instance(str)(identity)
semanticize.instance(bool)(identity)
semanticize.instance(type(None))(identity)
semanticize.instance(complex)(str)


class OctagenRePattern(BaseModel):
    """Regex pattern."""

    pattern: str
    value_type: str = 'python://re.Pattern'


@semanticize.instance(frozenset)
def _semanticize_frozenset(instance: frozenset) -> list:
    return list(map(semanticize, instance))


@semanticize.instance(Pattern)
def _semanticize_pattern(instance: Pattern):
    return OctagenRePattern(pattern=instance.pattern)
