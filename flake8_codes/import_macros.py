from pydantic import BaseModel

from flake8_codes.models import Violation


IMPORT_STATEMENT = '{% import "macros.html" as macros with context %}\n\n'


class ImportMacros(BaseModel):
    """Add Jinja2 common macros import."""

    violation: Violation

    def process(self) -> Violation:
        """Prepend the import statement."""
        description = IMPORT_STATEMENT + self.violation.description

        return Violation(
            description=description,
            **self.violation.dict(exclude={'description'}),
        )
