import re

from pydantic import BaseModel

from flake8_codes.models import Violation


class ExtractCodeAndTitle(BaseModel):
    def __call__(self, violation: Violation) -> Violation:
        first_line, description = violation.description.split('\n', maxsplit=1)
        first_line = first_line.replace('*', '')

        try:
            code, title = re.match(r'#? *([^:]+): (.+)', first_line).groups()
        except AttributeError:
            raise Exception(violation.description)

        return Violation(
            # To avoid conflicts with flake8-bugbear
            code=code.replace('B', 'S'),

            title=title,
            description=description.lstrip('\n'),

            **violation.dict(
                exclude={'code', 'title', 'description'},
            ),
        )
