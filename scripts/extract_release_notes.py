"""Extract one release's notes from the active or archived changelog."""

from __future__ import annotations

import argparse
from pathlib import Path

from .changelog_tools import extract_release_notes

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Parse arguments and write release notes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", help="Release tag in vX.Y.Z form.")
    parser.add_argument("output", type=Path, help="Output Markdown file.")
    args = parser.parse_args()
    try:
        notes = extract_release_notes(
            args.tag, PROJECT_ROOT / "CHANGELOG.md", PROJECT_ROOT / "changelogs"
        )
    except ValueError as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(notes, encoding="utf-8")


if __name__ == "__main__":
    main()
