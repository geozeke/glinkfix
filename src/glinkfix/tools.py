"""Tools to perform link fixing."""

import argparse
import os
import re


class InvalidLinkError(Exception):
    """Custom exception for handling invalid sharing links.

    Parameters
    ----------
    Exception : Exception
        InvalidLinkError is a sub-class of Python's Exception class.
    """

    def __init__(self):
        """Link exception initializer."""
        self.message = "Input is not a valid Google sharing link."
        super().__init__()

    def __str__(self):
        """Override __str__ method.

        Return a string version of InvalidLinkError.

        Returns
        -------
        str
            The message string.
        """
        return self.message


def clear() -> None:
    """Clear the screen.

    OS-agnostic version, which will work with both Windows and Linux.
    """
    os.system("clear" if os.name == "posix" else "cls")


def fix_link(args: argparse.Namespace) -> None:
    """Fix malformed Google Drive link.

    Prompt for a Google Drive link to fix (usually entered by pasting
    into the terminal) and generate a corrected version.

    Parameters
    ----------
    args : argparse.Namespace
        Command line arguments to determine how to prep the fixed link.
        If `-v` was selected (`args.view`) then prep the link for
        embedding into a file. If `-d` was selected (`args.download`)
        then prep the link for use with a download tool like `curl`.
    """
    clear()

    print("Enter a Google Drive sharing URL to be repackaged:\n")
    old_link = input()
    resourcekey = None
    template = "https://drive.google.com/uc?export=ACTION&id=IDNUM"
    prefix = "https://drive.google.com/file/d/"
    if "share_link" in old_link:
        suffix = "/view\\?usp=share_link"
    else:
        suffix = "/view\\?usp=sharing"
    parts = re.findall(rf"{prefix}([0-9A-Za-z_-]*){suffix}", old_link)

    if len(parts) != 1:
        raise InvalidLinkError
    else:
        idstring = parts[0]

    parts = re.findall(r"resourcekey=([0-9A-Za-z_-]*)", old_link)
    if len(parts) == 1:
        resourcekey = parts[0]

    if args.view:
        action = template.replace("ACTION", "view")
        link_type = "viewing"
    else:
        action = template.replace("ACTION", "download")
        link_type = "downloading"

    print(f"\nClean {link_type} URL is:\n")  # noqa
    new_link = action.replace("IDNUM", idstring)
    if resourcekey:
        new_link = f"{new_link}&resourcekey={resourcekey}"
    print(f"{new_link}\n")
    return


if __name__ == "__main__":  # pragma no cover
    pass
