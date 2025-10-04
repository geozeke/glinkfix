#!/usr/bin/env python3

"""Main module."""

import argparse
from importlib.metadata import version

from glinkfix.tools import fix_link

__version__ = version("glinkfix")


def main() -> None:
    """Initiate link fixing.

    1. Generate an argument parser to collect command line input.
    2. Call `fix_link` to perform link correction.
    """
    msg = """
    This program takes a Google Drive sharing link for a file and
    repackages it into a link that can be downloaded directly (e.g.
    using curl) or embedded in a document to be viewed (e.g. an image in
    a markdown document). Note: there is a size limit of 40MB for a
    single file when using Google Drive links in this manner.
    """

    epi = f"Version: {__version__}"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """
    The default behavior for glinkfix is to repackage a Google Drive
    link to make it suitable for embedding in a website. Use the -d
    option if you want to repackage a Google Drive link for direct
    downloading instead (e.g. downloading using curl).
    """
    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help=msg,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"glinkfix {__version__}",
    )

    args = parser.parse_args()
    fix_link(args)
    return


if __name__ == "__main__":
    main()
