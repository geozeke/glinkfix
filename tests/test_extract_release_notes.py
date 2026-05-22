"""Tests for release-note extraction."""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_extract_release_notes_for_current_changelog(tmp_path: Path) -> None:
    """Test extracting a known release section from the changelog."""
    output = tmp_path / "release-notes.md"

    subprocess.run(
        ["sh", "scripts/extract_release_notes.sh", "v2.1.0", str(output)],
        check=True,
    )

    notes = output.read_text(encoding="utf-8")
    assert notes.startswith("## 2.1.0")
    assert "Bump pytest from 8.4.2 to 9.0.2" in notes


def test_extract_release_notes_for_archived_changelog(tmp_path: Path) -> None:
    """Test extracting a release section from a minor-line archive."""
    output = tmp_path / "release-notes.md"

    subprocess.run(
        ["sh", "scripts/extract_release_notes.sh", "v2.0.11", str(output)],
        check=True,
    )

    notes = output.read_text(encoding="utf-8")
    assert notes.startswith("## 2.0.11")
    assert "formatted release messages" in notes
