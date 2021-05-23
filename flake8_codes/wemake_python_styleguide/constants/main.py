import functools
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable

import frontmatter
from libcst import (
    parse_module,
    AnnAssign,
)

from flake8_codes.semanticize import semanticize
from flake8_codes.wemake_python_styleguide.constants.models import (
    BodyStatement,
    WPSConstant, NotAnAssignment, GenerationFailed, NotPublicConstant,
)

logger = logging.getLogger(__name__)


def construct_description(statement: BodyStatement) -> str:
    """Fetch description from preceding comment."""
    last_leading_line = statement.leading_lines[-1]
    description = last_leading_line.comment.value

    if not description.startswith('#:'):
        raise NotPublicConstant()

    return description.lstrip('#: ').replace('``', '`')


def construct_constant(
    statement: BodyStatement,
    module,
) -> WPSConstant:
    """Parse WPSConstant object from a LibCST statement."""
    assignment = statement.body[0]
    if not isinstance(assignment, AnnAssign):
        raise NotAnAssignment()

    name = assignment.target.value

    description = construct_description(statement)

    about = f'python://{module.__name__}.{name}'

    return WPSConstant(
        name=name,
        about=about,
        description=description,
        value=semanticize(getattr(module, name)),
    )


def construct_constants(constants) -> Iterable[WPSConstant]:
    """Describe WPS constants."""
    python_code = Path(constants.__file__).read_text()
    module = parse_module(python_code)

    for statement in module.body:
        try:
            yield construct_constant(
                statement=statement,
                module=constants,
            )
        except GenerationFailed as err:
            logger.info(err)


def persist_constant(
    constant: WPSConstant,
    directory: Path,
):
    post = frontmatter.Post(
        content=constant.description,
        handler=frontmatter.YAMLHandler(),

        # To avoid yaml.representer.RepresenterError
        about=str(constant.about),

        **constant.dict(
            exclude={'description', 'about'},
            exclude_none=True,
            by_alias=True,
        ),
    )

    with (directory / f'{constant.name}.md').open('wb+') as output_file:
        frontmatter.dump(
            post=post,
            fd=output_file,
        )


def persist_constants(
    constants: Iterable[WPSConstant],
    directory: Path,
):
    directory.mkdir(parents=True, exist_ok=True)
    list(ThreadPoolExecutor(
        max_workers=10,
    ).map(
        functools.partial(
            persist_constant,
            directory=directory,
        ),
        constants,
    ))


def generate_constants(
    constants,
    destination: Path,
):
    generated_constants = construct_constants(constants)
    persist_constants(
        generated_constants,
        directory=destination,
    )
