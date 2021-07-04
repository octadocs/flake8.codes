import re
from typing import List

from pydantic import BaseModel, Field

from flake8_codes.models import Violation


class WPSConfig(BaseModel):
    """Insert a link to a WPS configuration parameter page."""

    violation: Violation
    related_configuration_parameters: List[str] = Field(default_factory=list)

    def _replace_wps_config(self, match: re.Match) -> str:
        """Process an occurrence."""
        url = f'python://{match.group(1)}'
        self.related_configuration_parameters.append(url)
        *_etc, name = url.rsplit('.', maxsplit=1)
        return f'`{name}`'

    def process(self) -> Violation:
        """Insert links."""
        description = self.violation.description

        description = re.sub(
            r'`(wemake_python_styleguide\.options\.defaults\.[^`]+)`',
            self._replace_wps_config,
            description,
        )

        return Violation(
            description=description,
            related_configuration_parameters=(
                self.related_configuration_parameters or None
            ),
            **self.violation.dict(exclude={
                'description',
                'related_configuration_parameters',
            }),
        )
