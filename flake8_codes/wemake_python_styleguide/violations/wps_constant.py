import re
from typing import List

from pydantic import BaseModel, Field

from flake8_codes.models import Violation


class WPSConstants(BaseModel):
    """Insert a link to a WPS configuration parameter page."""

    violation: Violation
    related_constants: List[str] = Field(default_factory=list)

    def _replace_wps_constant(self, match: re.Match) -> str:
        """Process an occurrence."""
        url = f'python://{match.group(1)}'
        self.related_constants.append(url)
        return f"{{{{ wps.constant('{url}') }}}}"

    def process(self) -> Violation:
        """Insert links."""
        description = self.violation.description

        description = re.sub(
            r':py`~(wemake_python_styleguide\.constants\.[^`]+)`',
            self._replace_wps_constant,
            description,
        )

        description = re.sub(
            r'`(wemake_python_styleguide\.constants\.[^`]+)`',
            self._replace_wps_constant,
            description,
        )

        return Violation(
            description=description,
            related_constants=(
                self.related_constants or None
            ),
            **self.violation.dict(exclude={
                'description',
                'related_constants',
            }),
        )
