"""Tests for command-line entry points."""

from __future__ import annotations

import runpy

import pytest

from glinkfix import app

FILE_ID = "1BJ5cR04cSzHa4xMIPApjLXv0IHPDu9U2"
DRIVE_LINK = f"https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing"
VIEW_LINK = f"https://lh3.googleusercontent.com/d/{FILE_ID}"
DOWNLOAD_LINK = f"https://drive.google.com/uc?export=download&id={FILE_ID}"


def test_main_converts_positional_url_and_copies(monkeypatch, capsys) -> None:
    """Test that positional URL input converts and copies."""
    copied_link = ""

    def fake_copy(value: str) -> None:
        nonlocal copied_link
        copied_link = value

    monkeypatch.setattr(app.pc, "copy", fake_copy)
    monkeypatch.setattr("sys.argv", ["glinkfix", DRIVE_LINK])

    assert app.main() == 0
    output = capsys.readouterr()
    assert output.err == ""
    assert copied_link == VIEW_LINK
    assert output.out == f"Mode: embed\nCopied: yes\nLink: {VIEW_LINK}\n"


def test_main_prompts_when_url_is_omitted(monkeypatch, capsys) -> None:
    """Test that omitted URL input uses the interactive prompt."""
    prompt = ""

    def fake_input(value: str) -> str:
        nonlocal prompt
        prompt = value
        return DRIVE_LINK

    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr(app.pc, "copy", lambda _: None)
    monkeypatch.setattr("sys.argv", ["glinkfix"])

    assert app.main() == 0
    output = capsys.readouterr()
    assert prompt == "Google Drive file link: "
    assert output.err == ""
    assert f"Link: {VIEW_LINK}\n" in output.out


def test_main_converts_download_link(monkeypatch, capsys) -> None:
    """Test that download mode creates a direct-download link."""
    monkeypatch.setattr(app.pc, "copy", lambda _: None)
    monkeypatch.setattr("sys.argv", ["glinkfix", "--download", DRIVE_LINK])

    assert app.main() == 0
    output = capsys.readouterr()
    assert output.err == ""
    assert output.out == f"Mode: download\nCopied: yes\nLink: {DOWNLOAD_LINK}\n"


def test_main_can_skip_clipboard_copy(monkeypatch, capsys) -> None:
    """Test that ``--no-copy`` disables clipboard writes."""

    def fail_copy(value: str) -> None:
        raise AssertionError("copy should not be called")

    monkeypatch.setattr(app.pc, "copy", fail_copy)
    monkeypatch.setattr("sys.argv", ["glinkfix", "--no-copy", DRIVE_LINK])

    assert app.main() == 0
    output = capsys.readouterr()
    assert output.err == ""
    assert output.out == f"Mode: embed\nCopied: no\nLink: {VIEW_LINK}\n"


def test_main_quiet_prints_only_link_and_skips_copy(monkeypatch, capsys) -> None:
    """Test that ``--quiet`` prints only the converted link."""

    def fail_copy(value: str) -> None:
        raise AssertionError("copy should not be called")

    monkeypatch.setattr(app.pc, "copy", fail_copy)
    monkeypatch.setattr("sys.argv", ["glinkfix", "--quiet", DRIVE_LINK])

    assert app.main() == 0
    output = capsys.readouterr()
    assert output.err == ""
    assert output.out == f"{VIEW_LINK}\n"


def test_main_reports_clipboard_failure(monkeypatch, capsys) -> None:
    """Test that clipboard failure is reported without failing conversion."""

    def fake_copy(value: str) -> None:
        raise app.pc.PyperclipException("clipboard unavailable")

    monkeypatch.setattr(app.pc, "copy", fake_copy)
    monkeypatch.setattr("sys.argv", ["glinkfix", DRIVE_LINK])

    assert app.main() == 0
    output = capsys.readouterr()
    assert output.err == ""
    assert output.out == (
        f"Mode: embed\nCopied: no (clipboard unavailable)\nLink: {VIEW_LINK}\n"
    )


def test_main_returns_error_for_invalid_url(monkeypatch, capsys) -> None:
    """Test that unsupported input returns an error status."""

    def fail_copy(value: str) -> None:
        raise AssertionError("copy should not be called")

    monkeypatch.setattr(app.pc, "copy", fail_copy)
    monkeypatch.setattr("sys.argv", ["glinkfix", "https://ubuntu.com"])

    assert app.main() == 1
    output = capsys.readouterr()
    assert output.out == ""
    assert output.err == "Error: unsupported Google Drive file link.\n"


def test_main_handles_keyboard_interrupt(monkeypatch, capsys) -> None:
    """Test that Ctrl-C during the prompt exits cleanly."""

    def fake_input(value: str) -> str:
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr("sys.argv", ["glinkfix"])

    assert app.main() == 130
    output = capsys.readouterr()
    assert output.out == ""
    assert output.err == "\nCanceled.\n"


def test_help_uses_console_command_name(monkeypatch, capsys) -> None:
    """Test that help output uses the console command name."""
    monkeypatch.setattr(app, "__version__", "test-version")
    monkeypatch.setattr("sys.argv", ["__main__.py", "-h"])

    with pytest.raises(SystemExit) as exc_info:
        app.main()

    assert exc_info.value.code == 0
    output = capsys.readouterr().out
    assert "usage: glinkfix" in output
    assert "[url]" in output
    assert "--no-copy" in output
    assert "--quiet" in output
    assert "usp=drive_link" in output
    assert "standard-library URL parser" in output


def test_module_entry_point_delegates_to_app_main(monkeypatch) -> None:
    """Test that ``python -m glinkfix`` delegates to ``app.main``."""
    monkeypatch.setattr(app, "main", lambda: 7)

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("glinkfix.__main__", run_name="__main__")

    assert exc_info.value.code == 7
