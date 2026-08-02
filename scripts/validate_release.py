"""Validate a release tag against metadata and committed release notes."""

from __future__ import annotations

import argparse
from pathlib import Path

from .changelog_tools import Version
from .changelog_tools import extract_release_notes
from .changelog_tools import parse_version
from .changelog_tools import validate_changelog_collection
from .changelog_tools import validate_project_version

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def validate_release(tag: str, project_root: Path = PROJECT_ROOT) -> Version:
    """Validate a release tag and return its parsed version."""
    if not tag.startswith("v"):
        raise ValueError("Release tag must start with v")
    version = parse_version(tag.removeprefix("v"))
    validate_project_version(project_root, version.text)
    validate_changelog_collection(
        project_root / "CHANGELOG.md", project_root / "changelogs", version.text
    )
    extract_release_notes(
        tag, project_root / "CHANGELOG.md", project_root / "changelogs"
    )
    return version


def write_github_outputs(path: Path, version: Version) -> None:
    """Append release metadata to a GitHub Actions output file."""
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"version={version.text}\n")
        handle.write(f"prerelease={str(bool(version.prerelease)).lower()}\n")


def main() -> None:
    """Validate the requested release tag."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", help="Release tag in vX.Y.Z form.")
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        version = validate_release(args.tag)
        if args.github_output:
            write_github_outputs(args.github_output, version)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
