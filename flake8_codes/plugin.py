import json
import operator
from pathlib import Path
from typing import Iterable, cast, List

import rdflib
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Navigation
from octadocs.octiron import Octiron


class Flake8Codes(BasePlugin):
    # def on_files(
    #     self,
    #     files: Files,
    #     config,
    # ):
    def on_nav(
        self,
        nav: Navigation,
        config,
        files: Files,
    ):
        """Publish the violation pages of every flake8 plugin in the root."""
        octiron: Octiron = config['extra']['octiron']
        site_dir = Path(config['site_dir'])

        pages_and_urls = octiron.query(
            'SELECT ?page ?url WHERE { ?page octa:url ?url }',
        )

        url_by_page = {
            row['page'].toPython().replace(
                'local:',
                '',
            ): row['url'].toPython().lstrip('/')
            for row in pages_and_urls
        }

        mkdocs_file: File
        for mkdocs_file in files:
            url_from_graph = url_by_page.get(mkdocs_file.src_path)

            if not url_from_graph:
                continue

            if url_from_graph == mkdocs_file.url:
                continue

            mkdocs_file.dest_path = url_from_graph + 'index.html'
            mkdocs_file.abs_dest_path = str(site_dir / mkdocs_file.dest_path)
            mkdocs_file.url = url_from_graph
