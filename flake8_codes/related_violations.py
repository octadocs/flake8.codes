import re
from typing import List

from pydantic import BaseModel, Field

from flake8_codes.models import Violation


class RelatedViolations(BaseModel):
    """Violations related to this one."""

    violation: Violation
    related_violations: List[str] = Field(default_factory=list)

    def _replace_wps_violation(self, match_object: re.Match):
        """Replace the occurrence and log it."""
        name = match_object.group(1)
        self.related_violations.append(name)
        return "{{ macros.wps_violation('%s') }}" % name

    def process(self) -> Violation:
        """Process the violation description for links to related violations."""
        self.related_violations = []

        description = re.sub(
            r'`~\.*([^`]+Violation)`',
            self._replace_wps_violation,
            self.violation.description,
        )

        return Violation(
            description=description,
            related_violations=self.related_violations or None,
            **self.violation.dict(exclude={
                'description',
                'related_violations',
            })
        )
