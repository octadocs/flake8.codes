from pathlib import Path

from flake8_codes.stubs import (
    create_empty_index_md_in_directory,
    create_version_index_md,
)
from flake8_codes.wemake_python_styleguide.constants.main import (
    generate_constants,
)
from flake8_codes.wemake_python_styleguide.options import generate_wps_options
from flake8_codes.wemake_python_styleguide.violations.main import (
    document_wps_violations,
)


def document_wemake_python_styleguide():
    from wemake_python_styleguide.version import pkg_version
    from wemake_python_styleguide import constants

    wps = Path(__file__).parent / 'docs/wemake-python-styleguide'
    create_empty_index_md_in_directory(wps)

    docs = wps / pkg_version
    create_version_index_md(docs=docs, package_version=pkg_version)

    generate_constants(
        constants=constants,
        destination=docs / 'constants',
    )
    document_wps_violations(docs / 'violations')
    generate_wps_options(docs / 'configuration')
