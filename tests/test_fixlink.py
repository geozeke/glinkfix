"""Tests for Google Drive link conversion."""

from __future__ import annotations

from argparse import Namespace

import pytest

from glinkfix import tools

FILE_ID = "1BJ5cR04cSzHa4xMIPApjLXv0IHPDu9U2"
RESOURCE_FILE_ID = "0B0vgUO_i57e9hrf9456jdfgfg"
RESOURCE_KEY = "sdfdf_Psdf-UjdfhTereu"
VIEW_LINK = f"https://lh3.googleusercontent.com/d/{FILE_ID}"
DOWNLOAD_LINK = f"https://drive.google.com/uc?export=download&id={FILE_ID}"


@pytest.mark.parametrize(
    ("link", "download", "expected"),
    [
        (
            f"https://drive.google.com/file/d/{FILE_ID}/view?usp=share_link",
            False,
            VIEW_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing",
            False,
            VIEW_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}/view?usp=share_link",
            True,
            DOWNLOAD_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing",
            True,
            DOWNLOAD_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}/view?usp=drive_link",
            False,
            VIEW_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}/view?usp=drivesdk",
            True,
            DOWNLOAD_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}/preview?usp=drive_link",
            False,
            VIEW_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}",
            False,
            VIEW_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}?usp=sharing",
            True,
            DOWNLOAD_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}/view?foo=bar&usp=drive_link",
            False,
            VIEW_LINK,
        ),
        (
            f"https://drive.google.com/file/d/{FILE_ID}/view?usp=private",
            False,
            VIEW_LINK,
        ),
        (
            f"https://www.drive.google.com/file/d/{FILE_ID}/view?usp=sharing",
            False,
            VIEW_LINK,
        ),
        (
            f"https://DRIVE.GOOGLE.COM/file/d/{FILE_ID}/view?usp=sharing",
            False,
            VIEW_LINK,
        ),
        (
            "https://drive.google.com/file/d/"
            f"{RESOURCE_FILE_ID}/view?usp=sharing&resourcekey={RESOURCE_KEY}",
            False,
            f"https://lh3.googleusercontent.com/d/{RESOURCE_FILE_ID}"
            f"?resourcekey={RESOURCE_KEY}",
        ),
        (
            "https://drive.google.com/file/d/"
            f"{RESOURCE_FILE_ID}/view?usp=share_link&resourcekey={RESOURCE_KEY}",
            True,
            "https://drive.google.com/uc?export=download"
            f"&id={RESOURCE_FILE_ID}&resourcekey={RESOURCE_KEY}",
        ),
        (
            "https://drive.google.com/file/d/"
            f"{RESOURCE_FILE_ID}/view?resourcekey={RESOURCE_KEY}&usp=drive_link",
            False,
            f"https://lh3.googleusercontent.com/d/{RESOURCE_FILE_ID}"
            f"?resourcekey={RESOURCE_KEY}",
        ),
    ],
)
def test_convert_link_returns_expected_url(
    link: str,
    download: bool,
    expected: str,
) -> None:
    """Test that valid Drive links are converted exactly."""
    assert tools.convert_link(link, download=download) == expected


@pytest.mark.parametrize(
    "link",
    [
        "https://ubuntu.com",
        f"https://drive.google.com/file/d/q/{FILE_ID}/view?usp=sharing",
        "https://drive.google.com/file/d//view?usp=sharing",
        f"https://drive.google.com/file/d/{FILE_ID}/edit?usp=sharing",
        f"https://drive.google.com/file/d/{FILE_ID}/view/details?usp=sharing",
        f"https://drive.google.com/drive/folders/{FILE_ID}?usp=sharing",
        f"https://docs.google.com/document/d/{FILE_ID}/edit?usp=sharing",
        f"https://docs.google.com/file/d/{FILE_ID}/view?usp=sharing",
        f"http://drive.google.com/file/d/{FILE_ID}/view?usp=sharing",
    ],
)
def test_convert_link_rejects_invalid_urls(link: str) -> None:
    """Test that unsupported links return ``None``."""
    assert tools.convert_link(link) is None


def test_fix_link_copies_valid_link(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    """Test that valid input is copied and printed."""
    copied_link = ""
    link = f"https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing"

    def fake_copy(value: str) -> None:
        nonlocal copied_link
        copied_link = value

    monkeypatch.setattr("builtins.input", lambda _: link)
    monkeypatch.setattr(tools.pc, "copy", fake_copy)

    tools.fix_link(Namespace(download=False))

    output = capsys.readouterr().out
    assert copied_link == VIEW_LINK
    assert "Fixed link (for embedding) copied to the clipboard:" in output
    assert VIEW_LINK in output


def test_fix_link_prints_download_link_when_clipboard_fails(
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    """Test that clipboard failure still prints the fixed link."""
    link = f"https://drive.google.com/file/d/{FILE_ID}/view?usp=share_link"

    def fake_copy(value: str) -> None:
        raise tools.pc.PyperclipException("clipboard unavailable")

    monkeypatch.setattr("builtins.input", lambda _: link)
    monkeypatch.setattr(tools.pc, "copy", fake_copy)

    tools.fix_link(Namespace(download=True))

    output = capsys.readouterr().out
    assert "Manually copy and paste this fixed link (for downloading):" in output
    assert DOWNLOAD_LINK in output


def test_fix_link_does_not_copy_invalid_input(
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    """Test that invalid input does not touch the clipboard."""

    def fail_copy(value: str) -> None:
        raise AssertionError("copy should not be called")

    monkeypatch.setattr("builtins.input", lambda _: "https://ubuntu.com")
    monkeypatch.setattr(tools.pc, "copy", fail_copy)

    tools.fix_link(Namespace(download=False))

    output = capsys.readouterr().out
    assert "Input URL is not a valid Google Drive sharing link." in output
