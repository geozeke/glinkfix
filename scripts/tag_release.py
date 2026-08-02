"""Validate, create, and push the current annotated release tag."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from .changelog_tools import extract_release_notes
from .changelog_tools import validate_changelog_collection
from .changelog_tools import validate_project_version

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def git(*args: str) -> str:
    """Run Git from the project root and return stripped stdout."""
    return subprocess.run(
        ("git", *args), cwd=PROJECT_ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def tag_release() -> str:
    """Validate release state, then create and push its annotated tag."""
    if git("branch", "--show-current") != "main":
        raise ValueError("Release tags can only be created from main")
    if git("status", "--porcelain=v1", "--untracked-files=all"):
        raise ValueError("Working tree must be clean before tagging a release")
    git("fetch", "origin", "main", "--tags")
    if git("rev-parse", "main") != git("rev-parse", "origin/main"):
        raise ValueError("Local main must exactly match origin/main")
    version = validate_project_version(PROJECT_ROOT)
    validate_changelog_collection(
        PROJECT_ROOT / "CHANGELOG.md", PROJECT_ROOT / "changelogs", version
    )
    tag = f"v{version}"
    extract_release_notes(
        tag, PROJECT_ROOT / "CHANGELOG.md", PROJECT_ROOT / "changelogs"
    )
    if git("tag", "--list", tag) or git(
        "ls-remote", "--tags", "origin", f"refs/tags/{tag}"
    ):
        raise ValueError(f"Release tag {tag} already exists")
    git("tag", "--annotate", tag, "--message", f"glinkfix {tag}")
    try:
        git("push", "origin", f"refs/tags/{tag}")
    except subprocess.CalledProcessError:
        git("tag", "--delete", tag)
        raise
    return tag


def main() -> None:
    """Create and push the validated release tag."""
    argparse.ArgumentParser(description=__doc__).parse_args()
    try:
        print(f"Pushed {tag_release()} successfully")
    except (ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
