import os


def clear():
    """Clear the screen

    This is an os-agnostic version, which will work with both Windows
    and Linux.
    """
    return os.system('clear' if os.name == 'posix' else 'cls')

# --------------------------------------------------------------------


def fixlink(args):

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
