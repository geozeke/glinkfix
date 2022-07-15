#!/usr/bin/env python3
"""Test fixlink."""

import csv
import sys
from argparse import Namespace
from importlib import import_module
from pathlib import Path

# Adjust path for local imports and data file opening. moduleLocation
# represents the location of the module we want to import for testing. Use
# import_module so we can perform the import after adjusting the path.
local = Path(__file__).resolve().parent
TESTDATA = local/'testdata.dat'
moduleLocation = local.parent/'src/glinkfix'
sys.path.append(str(moduleLocation))
fixlink = import_module('tools').fixlink


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


def test_fixlink(capsys, monkeypatch, testcase):
    """Test the fixlink function.

    Parameters
    ----------
    capsys : class CaptureFixture
        A pytest object. It captures stdout and stderr each time the
        test is run.
    monkeypatch : class MonkeyPatch
        A pytest object. It allows us to mock the input() function.
    testcase : [str, str, str]
        A list of three strings that have been parameterized to be used
        for testing. The three strings represent (in order):
        mode (view | download), input link, output link.
    """
    mode, linkin, linkout = testcase[0], testcase[1], testcase[2]
    args = Namespace()
    args.view = True if mode == 'view' else None
    args.download = True if mode == 'download' else None
    monkeypatch.setattr('builtins.input', lambda: linkin)
    fixlink(args)
    useroutput, codeerrors = capsys.readouterr()
    monkeypatch.delattr('builtins.input')

    # If the assertion is successful, the print statement below will be
    # suppressed.
    print(f'Simulated user input: {linkin}')
    assert linkout in useroutput
