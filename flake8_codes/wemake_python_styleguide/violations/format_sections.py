import re
from typing import List

from pydantic import BaseModel, Field

from flake8_codes.models import Violation


class FormatSections(BaseModel):
    """Format sections."""

    violation: Violation
    section_headers = (
        'Reasoning',
        'Solution',
        'Configuration',
        'See also',
    )

    def _format_content(self, content: str) -> str:
        """Format section contents."""
        return content.replace('    ', '')

    def _match_section(self, match: re.Match):
        """Format an individual section."""
        name, content, *etc = match.groups()

        content = self._format_content(content)

        return f'## {name}\n{content}'

    def _format_section_headers(self):
        return '|'.join(self.section_headers)

    def _format_sections(self, description: str) -> str:
        """Reformat sections."""
        return re.sub(
            ' *- (' + self._format_section_headers() + '): *\n(( {4}.+\n)+)',
            self._match_section,
            description,
            flags=re.MULTILINE,
        )

        # return description.replace('  - Reasoning:', '## Reasoning')

    def process(self) -> Violation:
        """Process the violation description for sections."""
        description = self._format_sections(self.violation.description)

        return Violation(
            description=description,
            **self.violation.dict(exclude={
                'description',
            })
        )
