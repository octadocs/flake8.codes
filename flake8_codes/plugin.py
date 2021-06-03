from pathlib import Path

from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files


class Flake8Codes(BasePlugin):
    def on_files(self, files: Files, config):
        """Publish the violation pages of every flake8 plugin in the root."""
        wps_violations = [
            mkdocs_file for mkdocs_file in files
            if mkdocs_file.src_path.startswith(
                'wemake-python-styleguide/0.15.2/violations',
            )
        ]

        violation_file: File
        for violation_file in wps_violations:
            destination_path = Path(violation_file.dest_path)

            violation_file.dest_path = str(destination_path.relative_to(
                destination_path.parent.parent,
            ))
            violation_file.abs_dest_path = str(
                Path(config['site_dir']) / violation_file.dest_path,
            )
            violation_file.url = f'{violation_file.name}/'