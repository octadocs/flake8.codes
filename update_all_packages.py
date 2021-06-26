import subprocess
from pathlib import Path

from pip_versions.core import find_versions


def generate_every_version(package_name: str):
    directory = Path(__file__).parent / 'docs' / package_name

    candidates = find_versions(package_name=package_name)
    versions = {c.version.base_version for c in candidates}

    for version in sorted(versions):
        version_directory = directory / version

        if version_directory.is_dir():
            print(f'Version {version} is already generated.')
            continue

        print(f'Going to install version {version}...')
        try:
            subprocess.run([
                'sh',
                '-c',
                f'poetry add {package_name}=={version}',
            ], check=True)
        except subprocess.CalledProcessError:
            print('Installation failed. Skipping :(')

        try:
            subprocess.run([
                'python',
                'run.py',
            ], check=True)
        except subprocess.CalledProcessError:
            print('Generation failed. Skipping :(')

        print('Installed.')


generate_every_version('wemake-python-styleguide')
generate_every_version('flake8-bugbear')
