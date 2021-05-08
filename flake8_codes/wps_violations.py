import re
from typing import List


class RelatedViolations(List[str]):
    """Process the description for of related violations."""

    def replace_related_to(self, match_object: re.Match):
        """Replace the occurrence and log it."""
        name = match_object.group(1)
        self.append(name)
        return "{{ macros.wps_violation('" + name + "') }}"

    def process_description(self, description: str) -> str:
        """Process the violation description for links to related violations."""
        return re.sub(
            r':class:`~\.*([^`]+)`',
            self.replace_related_to,
            description,
        )
