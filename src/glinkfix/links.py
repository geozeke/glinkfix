"""Google Drive link conversion utilities."""

import re
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse

DRIVE_HOSTS = {"drive.google.com", "www.drive.google.com"}
FILE_ID_PATTERN = re.compile(r"[a-zA-Z0-9_-]+")
VIEW_LINK_TEMPLATE = "https://lh3.googleusercontent.com/d/{file_id}"
DOWNLOAD_LINK_TEMPLATE = "https://drive.google.com/uc?export=download&id={file_id}"
SUPPORTED_FILE_ACTIONS = {"view", "preview"}


def _file_id_from_path(path: str) -> str | None:
    """Extract a Google Drive file ID from a URL path.

    Parameters
    ----------
    path : str
        Parsed URL path.

    Returns
    -------
    str or None
        Google Drive file ID when the path is supported, otherwise
        ``None``.
    """
    parts = path.strip("/").split("/")
    if len(parts) not in {3, 4} or parts[:2] != ["file", "d"]:
        return None

    file_id = parts[2]
    if not FILE_ID_PATTERN.fullmatch(file_id):
        return None

    if len(parts) == 4 and parts[3] not in SUPPORTED_FILE_ACTIONS:
        return None

    return file_id


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
    parsed = urlparse(link)
    if parsed.scheme != "https" or parsed.hostname not in DRIVE_HOSTS:
        return None

    file_id = _file_id_from_path(parsed.path)
    if not file_id:
        return None

    if download:
        new_link = DOWNLOAD_LINK_TEMPLATE.format(file_id=file_id)
    else:
        new_link = VIEW_LINK_TEMPLATE.format(file_id=file_id)

    params = parse_qs(parsed.query)
    resourcekey = params.get("resourcekey", [""])[0]
    if resourcekey:
        separator = "&" if "?" in new_link else "?"
        new_link = f"{new_link}{separator}{urlencode({'resourcekey': resourcekey})}"

    return new_link
