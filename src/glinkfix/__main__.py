#!/usr/bin/env python3

"""Main module."""

import argparse

from glinkfix.tools import fix_link


def main() -> None:
    """Initiate link fixing.

    1. Generate an argument parser to collect command line input.
    2. Call `fix_link` to perform link correction.
    """
    msg = """This program takes a Google Drive sharing link for a
    file and repackages it into a link that can be downloaded directly
    (e.g. using curl) or embedded in a document to be viewed (e.g. an
    image in a markdown document). Note: there is a size limit of 40MB
    for a single file when using Google Drive links in this manner."""

    epi = "Version: 1.2.1"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    group = parser.add_mutually_exclusive_group(required=True)

    msg = """repackage the link for viewing (e.g. as an embedded
    link in a markdown document)."""
    group.add_argument("-v", "--view", action="store_true", help=msg)

    msg = """repackage the link for downloading (e.g. downloading
    using curl)."""
    group.add_argument("-d", "--download", action="store_true", help=msg)

    args = parser.parse_args()
    fix_link(args)
    return


if __name__ == "__main__":
    main()
