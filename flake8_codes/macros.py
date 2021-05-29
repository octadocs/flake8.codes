from mkdocs_macros.plugin import MacrosPlugin


def wps_config(url: str) -> str:
    """Render a link to a WPS configuration parameter page."""
    return '**[DATA EXPUNGED]**'


def define_env(env: MacrosPlugin) -> MacrosPlugin:
    """
    Define a few Jinja2 macros useful for flake8-codes project.

    These macros are only valid if used **inside .md files.**
    See [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/) for
    more information.
    """
    env.variables['wps'] = {
        'config': wps_config,
    }

    return env
