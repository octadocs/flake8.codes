import os
import re
import subprocess
import uuid
from dataclasses import dataclass, make_dataclass, field, asdict, fields
from typing import Any, Type, Dict, Optional

from dependencies import Injector
from typer import Typer


def shallow_dict(data_cls) -> Dict[str, Any]:
    """Equivalent to dataclasses.asdict but with no recursion."""
    return {
        dataclass_field.name: getattr(data_cls, dataclass_field.name)
        for dataclass_field in fields(data_cls)
    }


@dataclass
class Shell:
    """Shell command."""

    def __call__(self) -> None:
        """Execute the provided shell command in a subprocess."""
        command = self.command.format(**shallow_dict(self))
        subprocess.run(('sh', '-c', command))


def shell(command: str, description: Optional[str] = None) -> Type[Shell]:
    arguments = re.findall(
        '{([^}]+)}',
        command,
    )

    argument_fields = [
        (argument, Any)
        for argument in arguments
    ]

    uid = uuid.uuid4().hex[:5]
    return make_dataclass(
        cls_name=f'_ShellCommand_{uid}',
        namespace={
            '__doc__': description,
        },
        fields=[
            *argument_fields,
            ('command', 'str', field(default=command)),
        ],
        bases=(Shell, ),
    )


@dataclass(repr=False)
class FlakehellCommand:
    in_pycharm: bool

    def __str__(self):
        if self.in_pycharm:
            return 'flake8helled'
        else:
            return 'flakehell lint'


def is_pycharm() -> bool:
    """Determine if the script is being called from PyCharm."""
    return os.getenv('PYCHARM_HOSTED') is not None


class Flake8Codes(Injector):
    """Jeeves helper for the project."""

    project_directory = 'flake8_codes'
    in_pycharm = is_pycharm()

    flakehell_command = FlakehellCommand
    lint = shell(
        'git diff origin/master | {flakehell_command} --diff {project_directory}',
        description='Verify correctness of Python code with flake8 & friends.'
    )

    format = shell(
        'isort {project_directory}',
        description='Isort imports in project.'
    )


cli = Typer()
cli.command(name='lint', short_help=Flake8Codes.lint.__doc__)(Flake8Codes.lint)
cli.command(name='format', short_help=Flake8Codes.format.__doc__)(Flake8Codes.format)


if __name__ == '__main__':
    cli()
