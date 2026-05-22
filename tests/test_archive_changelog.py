"""Tests for changelog archive maintenance."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "archive_changelog.py"
SPEC = importlib.util.spec_from_file_location("archive_changelog", SCRIPT_PATH)
assert SPEC is not None
archive_changelog = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = archive_changelog
SPEC.loader.exec_module(archive_changelog)


def test_archive_changelog_moves_non_target_minor(tmp_path: Path) -> None:
    """Test archiving releases outside the target minor version."""
    changelog = tmp_path / "CHANGELOG.md"
    archive_dir = tmp_path / "changelogs"
    changelog.write_text(
        """# Changelog

## 2.1.0 (2026-03-06)

### Changes

- Current release.

## 2.0.11 (2026-01-11)

### Changes

- Previous minor release.
""",
        encoding="utf-8",
    )

    updated = archive_changelog.archive_changelog("2.1.1", changelog, archive_dir)

    assert updated is True
    assert "2.1.0" in changelog.read_text(encoding="utf-8")
    assert "2.0.11" not in changelog.read_text(encoding="utf-8")
    archive_text = (archive_dir / "v2.0.x.md").read_text(encoding="utf-8")
    assert "## 2.0.11 (2026-01-11)" in archive_text
