"""Google Drive link conversion utilities."""

import argparse
import re

import pyperclip as pc  # type: ignore

DRIVE_LINK_PATTERN = re.compile(
    r"https:\/\/drive\.google\.com\/file\/d\/"
    r"(?P<file_id>[a-zA-Z0-9_-]+)"
    r"(\/view)?"
    r"(\?usp=(share_link|sharing))?"
    r"(&resourcekey=(?P<resourcekey>[a-zA-Z0-9_-]+))?"
)

VIEW_LINK_TEMPLATE = "https://lh3.googleusercontent.com/d/{file_id}"
DOWNLOAD_LINK_TEMPLATE = "https://drive.google.com/uc?export=download&id={file_id}"


def convert_link(link: str, *, download: bool = False) -> str | None:
    """Convert a Google Drive sharing link.

    Parameters
    ----------
    link : str
        Google Drive sharing link to convert.
    download : bool, optional
        Whether to create a direct-download link. By default, create an
        embeddable link.

    Returns
    -------
    str or None
        Converted link when `link` is valid, otherwise ``None``.
    """
    match = DRIVE_LINK_PATTERN.fullmatch(link)
    if not match:
        return None

    file_id = match.group("file_id")
    if download:
        new_link = DOWNLOAD_LINK_TEMPLATE.format(file_id=file_id)
    else:
        new_link = VIEW_LINK_TEMPLATE.format(file_id=file_id)

    resourcekey = match.group("resourcekey")
    if resourcekey:
        new_link = f"{new_link}&resourcekey={resourcekey}"

    return new_link


def fix_link(args: argparse.Namespace) -> None:
    """Convert a Google Drive sharing link.

    Prompt for a Google Drive link to fix (usually entered by pasting
    into the terminal) and generate an embeddable or downloadable URL.

    Parameters
    ----------
    args : argparse.Namespace
        Command-line arguments that determine how to prepare the fixed
        link. By default, prepare the link for embedding in a webpage. If
        `-d` was selected (`args.download`), prepare the link for use
        with a download tool such as `curl`.
    """
    oldlink = input("\nGoogle Drive link to fix: ")
    new_link = convert_link(oldlink, download=args.download)
    if new_link:
        if args.download:
            url_type = "for downloading"
        else:
            url_type = "for embedding"

        try:
            pc.copy(new_link)
            msg = f"\nFixed link ({url_type}) copied to the clipboard:"
        except pc.PyperclipException:
            msg = f"\nManually copy and paste this fixed link ({url_type}):"

        print(msg)
        print(f"{new_link}\n")

    else:
        print("\nInput URL is not a valid Google Drive sharing link.")


if __name__ == "__main__":
    pass
