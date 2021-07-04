import cProfile
from mkdocs.__main__ import build_command, gh_deploy_command


def main():
    # cProfile.run('build_command()', 'profile_dump')
    cProfile.run('gh_deploy_command()', 'profile_dump')


if __name__ == '__main__':
    main()
