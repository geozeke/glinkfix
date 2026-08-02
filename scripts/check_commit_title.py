"""Validate a pull-request title as a project Conventional Commit."""

from __future__ import annotations

import argparse

from .changelog_tools import validate_commit_title


def main() -> None:
    """Parse and validate a pull-request title."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Pull-request title to validate.")
    args = parser.parse_args()
    try:
        validate_commit_title(args.title)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
