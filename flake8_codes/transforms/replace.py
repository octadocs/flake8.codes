import re

from pydantic import BaseModel

from flake8_codes.models import Violation


class Replace(BaseModel):
    """Replace substring in description."""

    find: str
    replace: str

    def __call__(self, violation: Violation) -> Violation:
        return Violation(
            description=re.sub(self.find, self.replace, violation.description),
            **violation.dict(
                exclude={'description'},
            ),
        )
