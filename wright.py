#!/usr/bin/env python3
"""Wright is a makefile alternative written in pure Python.

wright /rīt/, noun ARCHAIC: a person who makes or builds things,
especially out of wood.
"""

import argparse
import os
import subprocess as sp
import textwrap


def clean(*args):
    """Clean the project build artifacts."""
    # Whole directories to delete
    directories = []
    directories.append('__pycache__')
    directories.append('.pytest_cache')
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


def pushtest(*args):
    """Push a distribution build to test.pypi.org."""
    dist()

    command = 'twine upload --repository-url https://test.pypi.org/legacy/ '
    command += 'dist/*'
    print(command)
    sp.run(command.split())

    return


def test(*args):
    """Run pytest."""
    command = 'pytest --tb=short'
    print(command)
    sp.run(command.split())

    return


def release(*args):
    """Build a distribution and release it to pypi.org."""
    dist()

    command = 'twine upload dist/*'
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
    command = 'bump2version ' + args[0]
    if dry != 'n':
        command += ' --verbose -n'
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
    # This is the name of the project.
    # basename = 'glinkfix'
    for k, v in args.__dict__.items():
        if v:
            eval(f'{k}')(f'{v}')
            return

    msg = "Please provide a task to perform. Use "
    msg += f"./{os.path.basename(__file__)} -h for help."
    print('\n' + textwrap.fill(msg) + '\n')

    return


def main():  # noqa

    # Build a python argument parser

    msg = """Perform various utility operations for a pypi development
    project."""

    epi = "Latest update: 01/12/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """clean-up build products."""
    parser.add_argument('-c', '--clean',
                        help=msg,
                        action='store_true',
                        dest='clean')

    msg = """create a distribution package ready for publication to
    pypi, but do not actually publish. Good for installing locally and
    checking the integrity of the build before release."""
    parser.add_argument('-d', '--dist',
                        help=msg,
                        action='store_true',
                        dest='dist')

    msg = """create and push a distribution package to test.pypi.org."""
    parser.add_argument('-p', '--pushtest',
                        help=msg,
                        action='store_true',
                        dest='pushtest')

    msg = """run pytest with the --tb=short option."""
    parser.add_argument('-t', '--test',
                        help=msg,
                        action='store_true',
                        dest='test')

    msg = """bump the version number of the project based on the
    provided choice: major, minor, patch."""
    parser.add_argument('-b', '--bump',
                        help=msg,
                        choices=['major', 'minor', 'patch'])

    msg = """generate a distribution package and release it to
    pypi.org."""
    parser.add_argument('-r', '--release',
                        help=msg,
                        action='store_true',
                        dest='release')

    args = parser.parse_args()

    performTask(args)

    return


if __name__ == '__main__':
    main()
