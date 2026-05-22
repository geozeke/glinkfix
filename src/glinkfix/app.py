#!/usr/bin/env python3

"""Command-line interface for glinkfix."""

import argparse
import sys
from importlib.metadata import version

import pyperclip as pc  # type: ignore

from glinkfix.links import convert_link

__version__ = version("glinkfix")


def copy_link(link: str) -> str:
    """Copy a link to the clipboard.

    Parameters
    ----------
    link : str
        Link to copy.

    Returns
    -------
    str
        Clipboard status for terminal output.
    """
    try:
        pc.copy(link)
    except pc.PyperclipException:
        return "no (clipboard unavailable)"

    return "yes"


def print_result(link: str, *, download: bool, copied: str) -> None:
    """Print normal conversion output.

    Parameters
    ----------
    link : str
        Converted Google Drive link.
    download : bool
        Whether the link is a direct-download link.
    copied : str
        Clipboard status for terminal output.
    """
    mode = "download" if download else "embed"
    print(f"Mode: {mode}")
    print(f"Copied: {copied}")
    print(f"Link: {link}")


def prompt_for_link() -> str | None:
    """Prompt for a Google Drive file link.

    Returns
    -------
    str or None
        User-entered link, or ``None`` when input is canceled.
    """
    try:
        return input("Google Drive file link: ")
    except KeyboardInterrupt:
        print("\nCanceled.", file=sys.stderr)
        return None


def main() -> int:
    """Run the glinkfix command-line interface."""
    msg = """
    Convert a Google Drive file sharing link into a link suitable for
    embedding in a document, such as an image in Markdown or HTML, or
    for direct download, such as with curl. glinkfix accepts current
    Drive file link formats such as usp=drive_link and uses Python's
    standard-library URL parser for lightweight, dependency-minimal
    processing. Google Drive links used this way have a single-file size
    limit of 40 MB.
    """

    epi = f"Version: {__version__}"

    parser = argparse.ArgumentParser(prog="glinkfix", description=msg, epilog=epi)

    parser.add_argument(
        "url",
        nargs="?",
        help="Google Drive file sharing link to convert. If omitted, prompt for one.",
    )
    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Create a direct-download link instead of the default embeddable link.",
    )
    parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Do not copy the converted link to the clipboard.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only the converted link and skip clipboard copying.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"glinkfix {__version__}",
    )

    args = parser.parse_args()
    old_link = args.url or prompt_for_link()
    if old_link is None:
        return 130

    new_link = convert_link(old_link, download=args.download)
    if not new_link:
        print("Error: unsupported Google Drive file link.", file=sys.stderr)
        return 1

    if args.quiet:
        print(new_link)
        return 0

    copied = "no"
    if not args.no_copy:
        copied = copy_link(new_link)

    print_result(new_link, download=args.download, copied=copied)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
