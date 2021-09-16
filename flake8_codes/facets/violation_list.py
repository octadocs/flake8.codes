from typing import Iterable

from dominate.tags import h2, ul, li, strong, code, a, html_tag
from octadocs.octiron import Octiron
from rdflib.term import Node


def construct_list_items(violations) -> Iterable[li]:
    """Construct list items."""
    for violation in violations:
        yield li(
            strong(code(violation['code'])),
            a(violation['title'], href=violation['url']),
        )


def violation_list(octiron: Octiron, iri: Node) -> html_tag:
    """Render a list of violations by directory."""
    violations = octiron.query(
        '''
        SELECT * WHERE {
            ?index_page octa:isChildOf ?violations_directory .
        
            ?page
                a :ViolationPage ;
                octa:isChildOf ?violations_directory ;
                octa:title ?title ;
                octa:url ?url ;
                :code ?code .
        } # ORDER BY ?code
        ''',
        index_page=iri,
    )

    return ul(
        *construct_list_items(violations),
        style='column-count: 2',
    )
