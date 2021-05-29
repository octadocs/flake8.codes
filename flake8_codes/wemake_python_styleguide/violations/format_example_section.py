import re
from typing import List

from pydantic import BaseModel, Field

from flake8_codes.models import Violation


class FormatExampleSection(BaseModel):
    """Format code blocks."""

    violation: Violation

    def process(self) -> Violation:
        """Process the violation description for sections."""
        description = self._format_example(self.violation.description)

        return Violation(
            description=description,
            **self.violation.dict(exclude={
                'description',
            })
        )

    def _format_example(self, description: str) -> str:
        return re.sub(
            'Example:',
            '## Example',
            description,
        )
