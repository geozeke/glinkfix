#!/usr/bin/env python3
"""Test fix_link."""

import csv
from argparse import Namespace
from pathlib import Path

import pytest
from glinkfix.tools import InvalidLinkError, fix_link

# Adjust path for local imports and data file opening. moduleLocation
# represents the location of the module we want to import for testing. Use
# import_module so we can perform the import after adjusting the path.
TESTDATA = Path(__file__).resolve().parent / "testdata.dat"


def pytest_generate_tests(metafunc):
    """Use the pytest_generate_tests hook to create test cases.

    Parameters
    ----------
    metafunc : obj
        The python object that facilitates parametrization.
    """
    with open(TESTDATA, "r") as f:
        reader = csv.reader(filter(lambda row: row.strip(), f))
        testcases = [row for row in reader if row[0][0] != "#"]
    metafunc.parametrize("case", testcases)


def test_fix_link(capsys, monkeypatch, case):
    """Test the fix_link function.

    Parameters
    ----------
    capsys : class CaptureFixture
        A pytest object. It captures stdout and stderr each time the
        test is run.
    monkeypatch : class MonkeyPatch
        A pytest object. It allows us to mock the input() function.
    case : [str, str, str, str]
        A list of four strings that have been parameterized to be used
        for testing. The four strings represent (in order):
        mode (view | download), status (raise | noraise) input link,
        output link.
    """
    mode, status, linkin, linkout = tuple(case)
    args = Namespace()
    args.view = True if mode == "view" else None
    args.download = True if mode == "download" else None
    monkeypatch.setattr("builtins.input", lambda: linkin)
    if status == "noraise":
        fix_link(args)
        useroutput, codeerrors = capsys.readouterr()
        # If the assertion is successful, the print statement below will be
        # suppressed.
        print(f"Simulated user input: {linkin}")
        assert linkout in useroutput
    else:
        with pytest.raises(InvalidLinkError):
            fix_link(args)

    monkeypatch.delattr("builtins.input")
