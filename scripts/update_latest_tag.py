"""Move the mutable latest tag after a successful stable release."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from .changelog_tools import parse_version

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def update_latest_tag(candidate_tag: str, latest_release_tag: str, commit: str) -> bool:
    """Move ``latest`` only when the candidate is GitHub's latest stable release."""
    if not candidate_tag.startswith("v"):
        raise ValueError("Candidate release tag must start with v")
    candidate = parse_version(candidate_tag.removeprefix("v"))
    if candidate.prerelease or candidate_tag != latest_release_tag:
        return False
    subprocess.run(
        ("git", "tag", "--force", "latest", commit), cwd=PROJECT_ROOT, check=True
    )
    subprocess.run(
        ("git", "push", "--force", "origin", "refs/tags/latest"),
        cwd=PROJECT_ROOT,
        check=True,
    )
    return True


def main() -> None:
    """Parse release metadata and update the mutable installation tag."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_tag")
    parser.add_argument("latest_release_tag")
    parser.add_argument("commit")
    args = parser.parse_args()
    try:
        updated = update_latest_tag(
            args.candidate_tag, args.latest_release_tag, args.commit
        )
    except (ValueError, subprocess.CalledProcessError) as exc:
        parser.error(str(exc))
    print(
        f"{'Moved' if updated else 'Left'} latest {'to' if updated else 'unchanged for'} {args.candidate_tag}."
    )


if __name__ == "__main__":
    main()
