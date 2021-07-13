import html
import io
from base64 import b64encode
from functools import partial
from unittest.mock import patch

import pydotplus
from mkdocs.structure.pages import Page
from mkdocs_macros.plugin import MacrosPlugin
from more_itertools import first
from octadocs.octiron import Octiron
from rdflib import Literal, URIRef, Graph, ConjunctiveGraph
from rdflib.tools.rdf2dot import rdf2dot


def wps_violation(
    internal_name: str,
    current_page: Page,
    octiron: Octiron,
) -> str:
    """Render a link to a WPS Violation page."""
    violation = first(octiron.query(
        '''SELECT * WHERE {
            ?current_page_iri :version ?version .
        
            ?violation
                :internalName ?name ;
                :code ?code ;
                octa:title ?title ;
                octa:url ?url ;
                :version ?version .
        }''',
        name=Literal(internal_name),
        current_page_iri=current_page.iri,
    ))

    return (
        f"[**{violation['code']}** {violation['title']}]({violation['url']})"
    )


def wps_constant(
    url: str,
    current_page: Page,
    octiron: Octiron,
):
    """Render a link to a WPS constant page."""
    constant = first(octiron.query(
        '''SELECT * WHERE {
            ?current_page_iri :version ?version .
            
            ?constant_iri
                :about ?python_iri ;
                :name ?name ;
                octa:url ?url ;
                :version ?version .
        }''',
        current_page_iri=current_page.iri,
        python_iri=URIRef(url + '/'),
    ))

    return f"[{constant['name']}]({constant['url'] })"


def foundational_classes(octiron: Octiron) -> Graph:
    """Select the foundational classes of the website."""
    return octiron.query('''
        CONSTRUCT {
            ?s ?p ?o .
            
            ?s rdfs:label ?s_label .
            ?o rdfs:label ?o_label .
        } WHERE {
            ?p
                rdfs:domain ?s ;
                rdfs:range ?o .
            
            OPTIONAL {
                ?s rdfs:label ?s_label .
            }
            
            OPTIONAL {
                ?o rdfs:label ?o_label .
            }

            FILTER(?s IN (<local:Violation>, <local:ViolationPage>, <local:Flake8Plugin>, <local:Flake8PluginVersion>))
            FILTER(?o IN (<local:Violation>, <local:ViolationPage>, <local:Flake8Plugin>, <local:Flake8PluginVersion>))
        }
    ''')


def graph(instance: ConjunctiveGraph) -> str:
    """
    Render RDF graph visually as PNG image.

    Idea: https://stackoverflow.com/a/61483971/1245471
    """
    dot_description = io.StringIO()

    with patch('rdflib.tools.rdf2dot.cgi', html):
        # FIXME hack, fixes this: https://github.com/RDFLib/rdflib/issues/1110
        rdf2dot(instance, dot_description)

    dg = pydotplus.graph_from_dot_data(dot_description.getvalue())
    png = dg.create_png()

    encoded_png = b64encode(png).decode('utf-8')

    return f'<img src="data:image/png;base64,{encoded_png}" />'



def define_env(env: MacrosPlugin) -> MacrosPlugin:
    """
    Define a few Jinja2 macros useful for flake8-codes project.

    These macros are only valid if used **inside .md files.**
    See [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/) for
    more information.
    """
    octiron = env.variables.octiron

    env.macro(
        partial(foundational_classes, octiron=octiron),
        name='foundational_classes',
    )

    env.filter(graph)

    env.variables['wps'] = {
        'violation': partial(
            wps_violation,
            octiron=octiron,
        ),
        'constant': partial(
            wps_constant,
            octiron=octiron,
        )
    }

    return env
