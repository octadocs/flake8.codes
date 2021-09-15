from functools import lru_cache
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template
from octadocs.octiron import Octiron
from rdflib.term import Node


@lru_cache(maxsize=None)
def create_template() -> Template:
    return Environment(
        loader=FileSystemLoader(
            searchpath=Path(__file__).parent.parent.parent / 'templates',
        ),
    ).get_template('facets/latest_version_list.html')


def latest_version_list(octiron: Octiron, iri: Node) -> str:
    """List latest version of every package as cards."""

    plugins = octiron.query(
        '''
        SELECT * WHERE {
            ?plugin
                a :Flake8Plugin ;
                :code-prefix ?prefix ;
                rdfs:label ?title .
        
            ?version
                a ?version_class ;
                rdfs:label ?version_number ;
                :plugin ?plugin .
        
            ?index_page
                a octa:IndexPage ;
                octa:isChildOf ?version ;
                octa:url ?url .
        } ORDER BY ?prefix
        ''',
        version_class=iri,
    )

    return create_template().render(
        plugins=plugins,
    )
