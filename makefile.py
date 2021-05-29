import re
import subprocess
from dataclasses import dataclass, make_dataclass, field
from typing import Any, Type

from dependencies import Injector


@dataclass
class Shell:
    """Shell command."""

    def __call__(self) -> None:
        """Execute the provided shell command in a subprocess."""
        subprocess.run(('sh', '-c', self.command))


def shell(command: str) -> Type[Shell]:
    match = re.search(
        '{([^}]+)}',
        command,
    )

    if match:
        arguments = match.groups()
    else:
        arguments = ()

    argument_fields = [
        (argument, Any)
        for argument in arguments
    ]

    return make_dataclass(
        cls_name='Cls',
        fields=[
            *argument_fields,
            ('command', 'str', field(default=command)),
        ],
        bases=(Shell, ),
    )


class Flake8Codes(Injector):
    """Jeeves helper for the project."""

    project_directory = 'flake8_codes'
    lint = shell(
        'git diff origin/master | flakehell lint --diff {project_directory}',
    )
    format = shell('isort {project_directory}')


def main():
    # Flake8Codes.lint()
    Flake8Codes.format()


if __name__ == '__main__':
    main()
