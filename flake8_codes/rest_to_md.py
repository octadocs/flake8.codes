import pypandoc
from pydantic import BaseModel

from flake8_codes.models import Violation


class Pypandoc(BaseModel):
    """Convert ReST text to Markdown."""

    violation: Violation

    source_format: str = 'rst'
    destination_format: str = 'commonmark'

    def process(self) -> Violation:
        """Replace with pypandoc."""
        description = pypandoc.convert_text(
            source=self.violation.description,
            format=self.source_format,
            to=self.destination_format,
        )

        return Violation(
            description=description,
            **self.violation.dict(exclude={
                'description',
            }),
        )
