import json
import logging
import operator
import os
from pathlib import Path
from typing import Iterable, cast, List

import rdflib
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Navigation
from octadocs.octiron import Octiron
from octadocs.storage import DiskCacheStorage


CI = os.getenv('CI')


class Flake8Codes(BasePlugin):
    """Customizations for flake8.codes website."""

    def octiron(self, config) -> Octiron:
        """Return Octiron instance."""
        return config['extra']['octiron']

    def assign_title_to_each_version_index_page(self, octiron: Octiron):
        """
        Assign octa:title based on version name.

        This cannot be done by OWL inference, so we do it by a custom query.
        """
        octiron.graph.update(
            '''
            INSERT {
                ?page octa:title ?version_directory_name .
            } WHERE {
                ?page
                    a :ViolationListPage ;
                    octa:isChildOf / octa:fileName ?version_directory_name ;
                    
                    # This one is to not create titles for WPS version pages.
                    :major_version ?major_version .
            }
            ''',
        )

    def moderate_files(self, files: Files, octiron: Octiron):
        """
        Exclude some files when building site locally.

        This helps reduce the site building time for the sake of local dev.
        """
        logging.warning(
            'A few files have been stripped from the site because local dev env'
            ' has been detected. Beware of 404 errors!',
        )
        directories = [
            row['version_directory'].toPython().replace('local:', '')
            for row in
            octiron.query(
                '''
                SELECT * WHERE {
                    ?version_directory a :Flake8PluginVersion .
                    
                    FILTER NOT EXISTS {
                        ?version_directory a :LatestVersion .
                    }
                }
                ''',
            )
        ]

        return Files([
            mkdocs_file for mkdocs_file in files
            if not any(
                mkdocs_file.src_path.startswith(directory)
                for directory in directories
            )
        ])

    def on_files(self, files: Files, config):
        """Automatic hooks."""
        octiron = self.octiron(config)

        self.assign_title_to_each_version_index_page(octiron)

        # Save the graph content to disk after octa:title was saved
        DiskCacheStorage(octiron=octiron).save()

        if CI is None:
            return self.moderate_files(
                files=files,
                octiron=octiron,
            )

        return files

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
