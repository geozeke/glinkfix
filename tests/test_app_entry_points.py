"""Tests for command-line entry points."""

from __future__ import annotations

import runpy

import pytest

from glinkfix import app


def test_main_returns_success(monkeypatch) -> None:
    """Test that the console entry point returns success after fixing."""
    called = False

    def fake_fix_link(args) -> None:
        nonlocal called
        called = True
        assert args.download is False

    monkeypatch.setattr(app, "fix_link", fake_fix_link)
    monkeypatch.setattr("sys.argv", ["glinkfix"])

    assert app.main() == 0
    assert called


def test_help_uses_console_command_name(monkeypatch, capsys) -> None:
    """Test that help output uses the console command name."""
    monkeypatch.setattr(app, "__version__", "test-version")
    monkeypatch.setattr("sys.argv", ["__main__.py", "-h"])

    with pytest.raises(SystemExit) as exc_info:
        app.main()

    assert exc_info.value.code == 0
    assert "usage: glinkfix" in capsys.readouterr().out


def test_module_entry_point_delegates_to_app_main(monkeypatch) -> None:
    """Test that ``python -m glinkfix`` delegates to ``app.main``."""
    monkeypatch.setattr(app, "main", lambda: 7)

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("glinkfix.__main__", run_name="__main__")

    assert exc_info.value.code == 7
