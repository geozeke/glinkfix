#!/usr/bin/env python3
"""Test glinkfix."""

import csv
from argparse import Namespace
from pathlib import Path

from glinkfix import tools

# # Adjust path before local imports
# sys.path.append(str(Path(__file__).resolve().parent.parent))

# try:
#     from tools import glinkfix  # noqa
# except Exception as e:
#     print(e)
#     sys.exit(1)

TESTDATA = Path(__file__).resolve().parent/'testdata.dat'


def pytest_generate_tests(metafunc):
    """Use the pytest_generate_tests hook to create test cases.

    Parameters
    ----------
    metafunc : obj
        The python object that facilitates parametrization.
    """
    with open(TESTDATA, 'r') as f:
        reader = csv.reader(filter(lambda row: row.strip(), f))
        testcases = [row for row in reader if row[0][0] != '#']
    metafunc.parametrize('testcase', testcases)


def test_glinkfix(capsys, monkeypatch, testcase):
    """Test the glinkfix code.

    Parameters
    ----------
    node : dict
        A dictionary object containing a test string and expected
        results for various tests.
    """
    mode, userin, userout = testcase[0], testcase[1], testcase[2]
    args = Namespace()
    args.view = True if mode == 'view' else False
    args.download = True if mode == 'download' else False
    monkeypatch.setattr('builtins.input', lambda: userin)
    tools.fixlink(args)

    monkeypatch.delattr('builtins.input')

    # Capture the interactive menu that the student code generates

    useroutput, codeerrors = capsys.readouterr()

    # If the assertion is successful, the print statement below will be
    # suppressed.

    print(f'Simulated user input: {userin}')
    assert userout in useroutput
