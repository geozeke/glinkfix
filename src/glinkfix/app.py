#!/usr/bin/env python3

"""Command-line interface for glinkfix."""

import argparse
from importlib.metadata import version

from glinkfix.tools import fix_link

__version__ = version("glinkfix")


def main() -> int:
    """Run the glinkfix command-line interface."""
    msg = """
    Convert a Google Drive sharing link into a link suitable for direct
    download, such as with curl, or for embedding in a document, such as
    an image in Markdown or HTML. Google Drive links used this way have
    a single-file size limit of 40 MB.
    """

    epi = f"Version: {__version__}"

    parser = argparse.ArgumentParser(prog="glinkfix", description=msg, epilog=epi)

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Create a direct-download link instead of an embeddable link.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"glinkfix {__version__}",
    )

    args = parser.parse_args()
    fix_link(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
