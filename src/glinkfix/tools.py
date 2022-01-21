"""Tools to perform link fixing."""

import os


def clear():
    """Clear the screen.

    This is an os-agnostic version, which will work with both Windows
    and Linux.
    """
    os.system('clear' if os.name == 'posix' else 'cls')

# --------------------------------------------------------------------


def fixlink(args):
    """Fix broken Google links.

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

    template = "https://drive.google.com/uc?export=ACTION&id=IDNUM"
    print('Enter a Google Drive URL to be repackaged:\n')
    oldlink = input()
    resourcekey = None

    try:
        parts = oldlink.split('/')
        id = parts[-2]
        if 'resourcekey' in oldlink:
            resourcekey = oldlink.split('&')[-1]
    except Exception as e:
        print(f'\nCannot repackage link: {e}')
        return

    if parts[3] != 'file':
        print('Link to repackage must point to a file.')
        return

    if args.view:
        action = template.replace('ACTION', 'view')
        linkType = 'viewing'
    elif args.download:
        action = template.replace('ACTION', 'download')
        linkType = 'downloading'
    else:
        pass

    print(f'\nClean {linkType} URL is:\n')
    newlink = action.replace("IDNUM", id)
    if resourcekey:
        newlink += f'&{resourcekey}'
    print(f'{newlink}\n')

    return

# --------------------------------------------------------------------


if __name__ == '__main__':
    pass
