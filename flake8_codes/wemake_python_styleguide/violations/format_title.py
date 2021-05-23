import re

from pydantic import BaseModel

from flake8_codes.models import Violation


class FormatTitle(BaseModel):
    """Remove special characters in page title."""

    violation: Violation

    def format_title(self) -> str:
        return self.violation.title.replace('{0}', '_').replace('`', '')

    def process(self) -> Violation:
        """Remove special characters in page title."""
        return Violation(
            title=self.format_title(),
            **self.violation.dict(exclude={
                'title',
            }),
        )
