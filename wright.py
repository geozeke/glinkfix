#!/usr/bin/env python3
"""Wright is a makefile alternative written in pure Python.

wright /rīt/, noun ARCHAIC: a person who makes or builds things,
especially out of wood.
"""

import argparse
import subprocess as sp
import webbrowser
from pathlib import Path

PROJNAME = 'glinkfix'


def clean(*args):
    """Clean the project build artifacts."""
    # Whole directories to delete
    directories = []
    directories.append('__pycache__')
    directories.append('.pytest_cache')
    directories.append('.mypy_cache')
    directories.append('build')
    directories.append('dist')
    directories.append('.eggs')
    directories.append('htmlcov')
    directories.append('*.egg-info')

    # NOTE: If this command were being run on the command line, you'd need to
    # escape the semicolon (\;)
    command = 'find . -name DIR -type d -exec rm -rf {} ; -prune'
    for directory in directories:
        print(command.replace('DIR', directory))
        sp.run(command.replace('DIR', directory).split())

    # Files to delete.
    files = []
    files.append('*.egg')
    files.append('*.pyc')
    files.append('*.pyo')
    files.append('.coverage')

    command = 'find . -name FILE -type f -delete'
    for file in files:
        print(command.replace('FILE', file))
        sp.run(command.replace('FILE', file).split())

    return


def coverage(*args):
    """Generate an HTML version of a test coverage report."""
    commands = []
    commands.append('coverage run -m pytest')
    commands.append('coverage report -m')
    commands.append('coverage html')

    for command in commands:
        print(command)
        sp.run(command.split())

    p = Path(__file__).resolve().parent/'htmlcov/index.html'
    webbrowser.open(f'file://{p}', new=2)

    return


def dist(*args):
    """Build distribution products."""
    clean()
    commands = []
    commands.append('python3 -m build')
    commands.append('twine check dist/*')

    for command in commands:
        print(command)
        sp.run(command.split())

    return


def test(*args):
    """Run pytest."""
    command = 'pytest --tb=short'
    print(command)
    sp.run(command.split())

    return


def pushtest(*args):
    """Push a distribution build to test.pypi.org."""
    dist()
    command = f'twine upload dist/* --repository {PROJNAME}-test'
    print(command)
    sp.run(command.split())

    return


def bump(*args):
    """Bump the version number of the project.

    Parameters
    ----------
    *args : [Any]
        0 or more arguments. In this case, it will be one of the
        following bump categories: patch, minor, major.
    """
    dry = input('Dry run (y/n)? ')[0].lower()
    command = f'bump2version {args[0]}'
    if dry != 'n':
        command = f'{command} --verbose -n'
    print(command)
    sp.run(command.split())

    return


def release(*args):
    """Build a distribution and release it to pypi.org."""
    dist()
    command = f'twine upload dist/* --repository {PROJNAME}-release'
    print(command)
    sp.run(command.split())

    return


def performTask(args):
    """Perform the selected task on the project.

    Parameters
    ----------
    args : Namespace
        A Namespace containing all the argparse-generated values. Since
        the range of operations is mutually exclusive (only one will /
        can be run at a time), iterate over the dictionary of the
        Namespace object (`args`) until a valid operation is found. If
        none is found, then print a status message and return.
    """
    for k, v in args.__dict__.items():
        if v:
            eval(f'{k}')(f'{v}')
            return
    return


def main():  # noqa

    # Build a python argument parser

    msg = """Perform various utility operations for a pypi development
    project."""

    epi = "Latest update: 07/29/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    group = parser.add_mutually_exclusive_group(required=True)

    msg = """clean-up build products."""
    group.add_argument('-c', '--clean',
                       help=msg,
                       action='store_true')

    msg = """generate an HTML version of a code coverage report and open it in
    the default browser."""
    group.add_argument('-C', '--coverage',
                       help=msg,
                       action='store_true')

    msg = """create a distribution package ready for publication to
    pypi, but do not actually publish. Good for installing locally and
    checking the integrity of the build before release."""
    group.add_argument('-d', '--dist',
                       help=msg,
                       action='store_true')

    msg = """run pytest with the --tb=short option."""
    group.add_argument('-t', '--test',
                       help=msg,
                       action='store_true')

    msg = """create and push a distribution package to test.pypi.org."""
    group.add_argument('-p', '--pushtest',
                       help=msg,
                       action='store_true')

    msg = """bump the version number of the project based on the
    provided choice: major, minor, patch."""
    group.add_argument('-b', '--bump',
                       help=msg,
                       choices=['major', 'minor', 'patch'])

    msg = """generate a distribution package and release it to
    pypi.org."""
    group.add_argument('-r', '--release',
                       help=msg,
                       action='store_true')

    args = parser.parse_args()
    performTask(args)

    return


if __name__ == '__main__':
    main()
