import re
import subprocess
import uuid
from dataclasses import dataclass, field, fields, make_dataclass
from typing import Any, Dict, Optional, Type

import typer


def shallow_dict(data_cls) -> Dict[str, Any]:
    """Equivalent to dataclasses.asdict but with no recursion."""
    return {
        dataclass_field.name: getattr(data_cls, dataclass_field.name)
        for dataclass_field in fields(data_cls)
    }


@dataclass
class Shell:
    """Shell command."""

    def format_command(self):
        return self.command.format(**shallow_dict(self))

    def __call__(self) -> None:
        """Execute the provided shell command in a subprocess."""
        try:
            subprocess.run(('sh', '-c', self.format_command()), check=True)
        except subprocess.CalledProcessError as err:
            raise typer.Exit(err.returncode)


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
