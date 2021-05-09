from pathlib import Path
from typing import Optional

import frontmatter
import libcst
from wemake_python_styleguide.options import defaults

from flake8_codes.models import WPSConfigurationParameter


def format_reasoning(comment: Optional[libcst.Comment]) -> Optional[str]:
    """Format the reasoning for the config parameter value."""
    if comment is None:
        return None

    return comment.value.lstrip('# ')


def generate_wps_options() -> None:
    """Generate configuration defaults for current version of WPS."""
    with open(defaults.__file__, 'r') as f:
        module = libcst.parse_module(f.read())

    for statement in module.body:
        assignment = statement.body[0]

        if not isinstance(assignment, libcst.AnnAssign):
            continue

        name = assignment.target.value

        value = getattr(defaults, name)
        last_leading_line = statement.leading_lines[-1]
        description = last_leading_line.comment.value.lstrip(
            '#: ',
        ).replace('``', '`')

        reasoning = format_reasoning(statement.trailing_whitespace.comment)

        cli_name = '--' + name.lower().replace('_', '-')

        parameter = WPSConfigurationParameter(
            about=f'python://wemake_python_styleguide.options.defaults.{name}',
            name=name,
            cli_name=cli_name,
            value=str(value),
            description=description,
            reasoning=reasoning,
        )

        document = frontmatter.Post(
            content=parameter.description,
            handler=frontmatter.YAMLHandler(),
            **parameter.dict(
                exclude={'description'},
                exclude_defaults=True,
            ),
        )

        output_path = (
            Path(__file__).parent.parent /
            'docs/wemake-python-styleguide/0.15.2/configuration' /
            f'{parameter.name}.md'
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open('wb+') as output_file:
            frontmatter.dump(
                document,
                output_file,
            )
