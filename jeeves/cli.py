import os
from dataclasses import dataclass

from dependencies import Injector
from typer import Typer

from jeeves.shell import shell


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
    flakehell = shell(
        (
            'git diff origin/master | '
            '{flakehell_command} --diff {project_directory}'
        ),
        description='Verify correctness of Python code with flake8 & friends.'
    )
    mypy = shell(
        'mypy {project_directory}',
        description='Verify type annotations',
    )

    format = shell(
        'isort {project_directory}',
        description='Isort imports in project.',
    )

    lint = flakehell


app = Typer()
app.command(name='lint')(Flake8Codes.lint)
app.command(name='format')(Flake8Codes.format)
