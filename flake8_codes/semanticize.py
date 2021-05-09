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


class OctagenSet(BaseModel):
    """Representation of a set."""

    elements: Set[Any] = Field(alias='$value')
    container: str = Field('$set', alias='$container')

    class Config:
        """Use Python friendly field names."""

        allow_population_by_field_name = True


class OctagenRePattern(BaseModel):
    """Regex pattern."""

    pattern: str
    value_type: str = 'python://re.Pattern'


@semanticize.instance(frozenset)
def _semanticize_frozenset(instance: frozenset) -> OctagenSet:
    return OctagenSet(elements=set(instance))


@semanticize.instance(Pattern)
def _semanticize_pattern(instance: Pattern):
    return OctagenRePattern(pattern=instance.pattern)
