import re

from pydantic import BaseModel

from flake8_codes.models import Violation


class UnpairedQuote(BaseModel):
    """Replace `something`` with ``something`` for ReST correctness."""

    violation: Violation

    def process(self) -> Violation:
        """It seems a solitary ` is invalid in ReST: they should go in pairs."""
        description = self.violation.description

        # TODO: file a PR for WPS461.
        description = re.sub(
            ' `([^`])',
            r' ``\g<1>',
            description,
        )

        return Violation(
            description=description,
            **self.violation.dict(exclude={
                'description',
            }),
        )
