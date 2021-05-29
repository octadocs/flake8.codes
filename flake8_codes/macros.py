from functools import partial

from mkdocs_macros.plugin import MacrosPlugin
from more_itertools import first
from octadocs.octiron import Octiron
from rdflib import URIRef, Literal


def wps_config(
    url: str,
    octiron: Octiron,
) -> str:
    """Render a link to a WPS configuration parameter page."""
    config = first(octiron.query(
        '''
        SELECT * WHERE {
            ?page
                :about ?parameter ;
                :name ?name ;
                :value ?value ;
                octa:url ?url .
        }
        ''',
        parameter=URIRef(url + '/'),   # FIXME THIS!!!
    ))

    return f"[{config['name']}]({config['url']}) = `{config['value']}`"


def wps_violation(
    internal_name: str,
    octiron: Octiron,
) -> str:
    """Render a link to a WPS Violation page."""
    violation = first(octiron.query(
        '''SELECT * WHERE {
            ?violation
                :internalName ?name ;
                :code ?code ;
                octa:title ?title ;
                octa:url ?url .
        }''',
        name=Literal(internal_name),
    ))

    return (
        f"[**WPS{violation['code']}** {violation['title']}]({violation['url']})"
    )


def define_env(env: MacrosPlugin) -> MacrosPlugin:
    """
    Define a few Jinja2 macros useful for flake8-codes project.

    These macros are only valid if used **inside .md files.**
    See [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/) for
    more information.
    """
    env.variables['wps'] = {
        'config': partial(
            wps_config,
            octiron=env.variables.octiron,
        ),
        'violation': partial(
            wps_violation,
            octiron=env.variables.octiron,
        )
    }

    return env
