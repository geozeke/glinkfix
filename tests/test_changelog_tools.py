"""Tests for changelog and release-maintenance helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.changelog_tools import Section
from scripts.changelog_tools import archive_changelog
from scripts.changelog_tools import extract_release_notes
from scripts.changelog_tools import merge_unreleased
from scripts.changelog_tools import parse_version
from scripts.changelog_tools import validate_changelog_collection
from scripts.changelog_tools import validate_commit_title
from scripts.validate_release import write_github_outputs

PREAMBLE = "# Changelog\n\nRelease history."


def release(version: str, note: str = "Changed") -> str:
    """Return a minimal generated-format release section."""
    return f"## [{version}] - 2026-08-02\n\n### Changed\n\n- {note}"


@pytest.mark.parametrize("version", ("0.1.0", "1.2.3b1", "2.0.0rc2"))
def test_parse_version_accepts_canonical_versions(version: str) -> None:
    """Canonical stable and prerelease versions parse."""
    assert parse_version(version).text == version


@pytest.mark.parametrize("version", ("v1.2.3", "1.2", "01.2.3", "1.2.3-rc.1"))
def test_parse_version_rejects_noncanonical_versions(version: str) -> None:
    """Noncanonical release versions fail validation."""
    with pytest.raises(ValueError, match="canonical"):
        parse_version(version)


@pytest.mark.parametrize(
    "title",
    ("feat: add command", "fix(cli): reject empty URLs", "build(deps): update ruff"),
)
def test_validate_commit_title_accepts_documented_types(title: str) -> None:
    """Documented Conventional Commit titles are accepted."""
    validate_commit_title(title)


@pytest.mark.parametrize(
    "title", ("Add command", "deps: update ruff", "fix(): empty scope")
)
def test_validate_commit_title_rejects_legacy_or_malformed_types(title: str) -> None:
    """Legacy and malformed titles are rejected for new work."""
    with pytest.raises(ValueError, match="Conventional Commit"):
        validate_commit_title(title)


def test_merge_unreleased_combines_matching_groups() -> None:
    """Curated unreleased entries merge with generated entries."""
    generated = Section("2.2.3", release("2.2.3", "Generated entry"))
    curated = Section("Unreleased", "## [Unreleased]\n\n### Changed\n\n- Curated entry")

    merged = merge_unreleased(generated, curated)

    assert "- Curated entry\n- Generated entry" in merged.text


def test_archive_and_extract_release_notes(tmp_path: Path) -> None:
    """Inactive release lines archive and notes remain discoverable."""
    changelog = tmp_path / "CHANGELOG.md"
    archives = tmp_path / "changelogs"
    changelog.write_text(
        f"{PREAMBLE}\n\n{release('2.2.3')}\n\n{release('2.1.0', 'Archived')}\n",
        encoding="utf-8",
    )

    assert archive_changelog("2.2.3", changelog, archives) == [archives / "v2.1.x.md"]
    assert "- Archived" in extract_release_notes("v2.1.0", changelog, archives)


def test_repository_changelogs_use_current_format() -> None:
    """Every checked-in changelog passes the current collection validator."""
    validate_changelog_collection(
        PROJECT_ROOT / "CHANGELOG.md", PROJECT_ROOT / "changelogs", "2.2.2"
    )


@pytest.mark.parametrize(
    ("version", "prerelease"), (("2.2.3", "false"), ("2.2.3rc1", "true"))
)
def test_github_outputs_classify_prereleases(
    version: str, prerelease: str, tmp_path: Path
) -> None:
    """Release metadata selects the appropriate publication path."""
    output = tmp_path / "github-output"

    write_github_outputs(output, parse_version(version))

    assert output.read_text(encoding="utf-8").splitlines() == [
        f"version={version}",
        f"prerelease={prerelease}",
    ]
