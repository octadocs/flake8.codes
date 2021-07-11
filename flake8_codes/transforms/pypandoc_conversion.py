import pypandoc
from pydantic import BaseModel

from flake8_codes.models import Violation


class Pypandoc(BaseModel):
    """Convert ReST text in a Violation to Markdown."""

    source_format: str = 'rst'
    destination_format: str = 'commonmark'

    def __call__(self, violation: Violation) -> Violation:
        """Replace with pypandoc."""
        description = pypandoc_convert(
            text=violation.description,
            source_format=self.source_format,
            destination_format=self.destination_format,
        )

        return Violation(
            description=description,
            **violation.dict(exclude={
                'description',
            }),
        )


def pypandoc_convert(
    text: str,
    source_format: str = 'rst',
    destination_format: str = 'commonmark',
) -> str:
    return pypandoc.convert_text(
        source=text,
        format=source_format,
        to=destination_format,
    )
