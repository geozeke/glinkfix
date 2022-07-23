#!/usr/bin/env python3
"""Test the __str__ method for the InvalidLinkError class."""

from glinkfix.tools import InvalidLinkError


def test_linkerrorstr():
    """Test the __str__ method for the InvalidLinkError class."""
    e = InvalidLinkError()
    assert str(e) == 'Input is not a valid Google sharing link.'
