"""Tools to perform link fixing."""

import argparse
import re

import pyperclip as pc  # type: ignore


def fix_link(args: argparse.Namespace) -> None:
    """Fix malformed Google Drive link.

    Prompt for a Google Drive link to fix (usually entered by pasting
    into the terminal) and generate a corrected version.

    Parameters
    ----------
    args : argparse.Namespace
        Command line arguments to determine how to prep the fixed link.
        By default, prep the link for embedding into a webpage. If `-d`
        was selected (`args.download`) then prep the link for use with a
        download tool like `curl`.
    """
    r1 = r"https:\/\/drive\.google\.com\/file\/d\/"
    r2 = r"([a-zA-Z0-9_-]+)"
    r3 = r"(\/view)?(\?usp=(share_link|sharing))?"
    r4 = r"(&resourcekey=[a-zA-Z0-9_-]+)?"
    regex = f"{r1}{r2}{r3}{r4}"

    v1 = "https://lh3.googleusercontent.com/d/"
    view_template = rf"{v1}IDNUM"

    d1 = "https://drive.google.com/"
    d2 = "uc?export=download&id="
    download_template = rf"{d1}{d2}IDNUM"

    oldlink = input("\nLink to fix: ")
    if re.fullmatch(regex, oldlink):
        start = oldlink.find("/d/") + 3
        end = oldlink.find("/view")
        id_num = oldlink[start:end]
        if args.download:
            new_link = download_template.replace("IDNUM", id_num)
            url_type = "for downloading"
        else:
            new_link = view_template.replace("IDNUM", id_num)
            url_type = "for embedding"
        if "resourcekey" in oldlink:
            key = oldlink.split("resourcekey=")[-1]
            new_link = f"{new_link}&resourcekey={key}"

        try:
            pc.copy(new_link)
            msg = f"\nFixed link ({url_type}) was copied to the clipboard:"
        except pc.PyperclipException:
            msg = f"\nManually copy/paste this fixed link ({url_type}):"

        print(msg)
        print(f"{new_link}\n")

    else:
        print("\nInput url is not a valid Google Drive Sharing Link.")

    return


if __name__ == "__main__":
    pass
