from typing import Iterable, Union

from dominate.tags import ul, li, strong, code, a, html_tag
from octadocs.octiron import Octiron
from rdflib.term import Node

from prodict import Prodict


def directory_list(octiron: Octiron, iri: Node) -> Union[html_tag, str]:
    """Render a list of subdirectories in given directory."""
    links = map(Prodict, octiron.query(
        '''
        SELECT * WHERE {
            ?index_page octa:isChildOf ?directory .
            
            ?directory
                octa:isParentOf /
                octa:isParentOf /
                octa:isParentOf ?link .
        
            ?link
                a octa:IndexPage ;
                octa:title ?title ;
                octa:url ?url .
        } ORDER BY ?title
        ''',
        index_page=iri,
    ))

    lis = [
        li(a(link.title, href=link.url))
        for link in links
    ]

    return ul(*lis)
