"""Tests for release tag generation."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


def release_script(tmp_path: Path, version: str) -> Path:
    scripts_path = tmp_path / "scripts"
    scripts_path.mkdir()
    script_path = scripts_path / "release_tags.sh"
    shutil.copy(Path("scripts/release_tags.sh"), script_path)
    (tmp_path / "pyproject.toml").write_text(
        f'[project]\nname = "glinkfix"\nversion = "{version}"\n',
        encoding="utf-8",
    )
    return script_path


def run_release_script(
    script_path: Path, *args: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(script_path), *args],
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("version", ["2.3.0-beta.1", "2.3.0-rc.1"])
def test_latest_refuses_beta_and_release_candidate_before_git(
    tmp_path: Path, version: str
) -> None:
    result = run_release_script(release_script(tmp_path, version), "--latest")

    assert result.returncode == 1
    assert (
        f"Error: Refusing to move 'latest' for prerelease version '{version}'."
        in result.stdout
    )
    assert (
        "Use 'just tag-release' for beta and release candidate versions."
        in result.stdout
    )
    assert "not a git repository" not in result.stderr


def test_tag_release_allows_prerelease_versions(tmp_path: Path) -> None:
    result = run_release_script(release_script(tmp_path, "2.3.0-rc.1"))

    assert result.returncode != 1
    assert "Refusing to move 'latest'" not in result.stdout
    assert "not a git repository" in result.stderr


def test_latest_stable_version_reaches_git_checks(tmp_path: Path) -> None:
    result = run_release_script(release_script(tmp_path, "2.3.0"), "--latest")

    assert result.returncode != 1
    assert "Refusing to move 'latest'" not in result.stdout
    assert "not a git repository" in result.stderr
