import re
from dataclasses import dataclass, make_dataclass, Field, field, asdict
from typing import Any

from dependencies import Injector
import subprocess


@dataclass
class Shell:
    def __call__(self):
        command = self.command.format(**asdict(self)).split(' ')
        return subprocess.run(command)


def shell(command: str):
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
    lint = shell('flakehell lint {project_directory}')


def main():
    print(Flake8Codes.lint())


if __name__ == '__main__':
    main()
