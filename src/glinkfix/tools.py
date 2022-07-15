"""Tools to perform link fixing."""

import os


class InvalidLinkError(Exception):
    """Custom exception for handling invalid sharing links.

    Parameters
    ----------
    Exception : Exception
        InvalidLinkError is a sub-class of Python's Exception class.
    """

    def __init__(self):
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


def clear():
    """Clear the screen.

    OS-agnostic version, which will work with both Windows and Linux.
    """
    os.system('clear' if os.name == 'posix' else 'cls')


def fixlink(args):
    """Fix malformed Google link.

    Prompt for a Google link to fix (usually entered by pasting into the
    terminal) and generate a corrected version.

    Parameters
    ----------
    args : argparse
        Command line arguments to determine how to prep the fixed link.
        If `-v` was selected (`args.view`) then prep the link for
        embedding into a file. If `-d` was selected (`args.download`)
        then prep the link for use with a download tool like `curl`.
    """
    clear()

    print('Enter a Google Drive sharing URL to be repackaged:\n')
    oldlink = input()
    resourcekey = None

    template = "https://drive.google.com/uc?export=ACTION&id=IDNUM"
    required1 = "https://drive.google.com/file/d/"
    required2 = "view?usp=sharing"
    if required1 not in oldlink and required2 not in oldlink:
        raise(InvalidLinkError)

    try:
        parts = oldlink.split('/')
        id = parts[-2]
        if 'resourcekey' in oldlink:
            resourcekey = oldlink.split('=')[-1]
    except IndexError:
        raise(InvalidLinkError)

    if args.view:
        action = template.replace('ACTION', 'view')
        linkType = 'viewing'
    else:
        action = template.replace('ACTION', 'download')
        linkType = 'downloading'

    print(f'\nClean {linkType} URL is:\n')
    newlink = action.replace("IDNUM", id)
    if resourcekey:
        newlink = f'{newlink}&resourcekey={resourcekey}'
    print(f'{newlink}\n')

    return


if __name__ == '__main__':
    pass
