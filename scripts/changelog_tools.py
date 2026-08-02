"""Provide changelog, release-note, and Conventional Commit helpers."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

PROJECT_NAME = "glinkfix"
REPOSITORY_URL = "https://github.com/geozeke/glinkfix"
VERSION_CORE = r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
PRERELEASE = r"(?:(?:a|b|rc)(?:0|[1-9]\d*))?"
VERSION_RE = re.compile(rf"^(?P<version>{VERSION_CORE}{PRERELEASE})$")
HEADING_RE = re.compile(
    rf"^## \[(?P<label>Unreleased|{VERSION_CORE}{PRERELEASE})\]"
    r"(?: - (?P<date>\d{4}-\d{2}-\d{2}))?$"
)
GROUP_RE = re.compile(r"^### (?P<group>.+)$")
COMMIT_TITLE_RE = re.compile(
    r"^(?P<type>feat|change|deprecate|remove|fix|security|perf|deploy|docs|"
    r"build|chore|ci|refactor|style|test|revert)"
    r"(?:\([a-z0-9][a-z0-9._/-]*\))?(?:!)?: [^\s].*$"
)
CHANGELOG_GROUPS = {
    "Added",
    "Breaking Changes",
    "Changed",
    "Dependencies",
    "Deprecated",
    "Deployment & Operations",
    "Documentation",
    "Fixed",
    "Performance",
    "Removed",
    "Reverted",
    "Security",
}
CHANGELOG_GROUP_ORDER = (
    "Breaking Changes",
    "Security",
    "Added",
    "Changed",
    "Deprecated",
    "Removed",
    "Fixed",
    "Performance",
    "Deployment & Operations",
    "Documentation",
    "Dependencies",
    "Reverted",
)
PrereleaseKey = tuple[tuple[int, int | str], ...]


@dataclass(frozen=True)
class Version:
    """Represent a canonical project release version.

    Parameters
    ----------
    text
        Normalized version text without a leading ``v``.
    major
        Major version component.
    minor
        Minor version component.
    patch
        Patch version component.
    prerelease
        Parsed prerelease identifiers.
    """

    text: str
    major: int
    minor: int
    patch: int
    prerelease: PrereleaseKey

    @property
    def major_minor(self) -> tuple[int, int]:
        """Return the major and minor release line."""
        return self.major, self.minor

    def sort_key(self) -> tuple[int, int, int, bool, PrereleaseKey]:
        """Return a key that sorts stable versions after prereleases."""
        return self.major, self.minor, self.patch, not self.prerelease, self.prerelease


@dataclass(frozen=True)
class Section:
    """Represent a second-level changelog section.

    Parameters
    ----------
    label
        ``Unreleased`` or a canonical release version.
    text
        Complete Markdown for the section, including its heading.
    """

    label: str
    text: str

    @property
    def version(self) -> Version | None:
        """Return the parsed version, or ``None`` for Unreleased."""
        if self.label == "Unreleased":
            return None
        return parse_version(self.label)


def _prerelease_key(text: str) -> PrereleaseKey:
    """Return a sortable prerelease key."""
    match = re.fullmatch(r"\d+\.\d+\.\d+(?P<label>a|b|rc)(?P<number>\d+)", text)
    if not match:
        return ()
    return (
        (0, {"a": 0, "b": 1, "rc": 2}[match.group("label")]),
        (0, int(match.group("number"))),
    )


def parse_version(text: str) -> Version:
    """Parse a canonical project release version.

    Parameters
    ----------
    text
        Bare release version without a leading ``v``.

    Returns
    -------
    Version
        Parsed version components.

    Raises
    ------
    ValueError
        If the value is not a supported canonical release version.
    """
    match = VERSION_RE.fullmatch(text)
    if not match:
        raise ValueError(
            f"Expected a canonical version such as 2.2.3 or 2.2.3rc1, got: {text}"
        )
    normalized = match.group("version")
    core_match = re.match(VERSION_CORE, normalized)
    if not core_match:
        raise ValueError(f"Missing release segment in version: {text}")
    major, minor, patch = (int(part) for part in core_match.group().split("."))
    return Version(normalized, major, minor, patch, _prerelease_key(normalized))


def split_changelog(text: str) -> tuple[str, list[Section]]:
    """Split changelog Markdown into a preamble and release sections."""
    lines = text.splitlines()
    headings = [index for index, line in enumerate(lines) if HEADING_RE.fullmatch(line)]
    if not headings:
        return text.strip(), []
    preamble = "\n".join(lines[: headings[0]]).strip()
    sections: list[Section] = []
    for position, start in enumerate(headings):
        end = headings[position + 1] if position + 1 < len(headings) else len(lines)
        match = HEADING_RE.fullmatch(lines[start])
        if not match:
            raise ValueError(f"Invalid changelog heading: {lines[start]}")
        sections.append(
            Section(match.group("label"), "\n".join(lines[start:end]).strip())
        )
    return preamble, sections


def format_changelog(preamble: str, sections: list[Section]) -> str:
    """Format a preamble and release sections as normalized Markdown."""
    parts = [preamble.strip(), *(section.text.strip() for section in sections)]
    return "\n\n".join(part for part in parts if part).strip() + "\n"


def _group_content(section: Section) -> tuple[str, list[str], dict[str, list[str]]]:
    """Return a section heading, introduction, and grouped content."""
    lines = section.text.splitlines()
    heading = lines[0]
    introduction: list[str] = []
    groups: dict[str, list[str]] = {}
    current = ""
    for line in lines[1:]:
        match = GROUP_RE.fullmatch(line)
        if match:
            current = match.group("group")
            groups.setdefault(current, [])
        elif current and line.strip():
            groups[current].append(line)
        elif line.strip():
            introduction.append(line)
    return heading, introduction, groups


def merge_unreleased(generated: Section, curated: Section) -> Section:
    """Merge generated release notes with a curated matching baseline."""
    heading, generated_intro, generated_groups = _group_content(generated)
    _curated_heading, curated_intro, curated_groups = _group_content(curated)
    merged = {group: list(lines) for group, lines in curated_groups.items()}
    for group, lines in generated_groups.items():
        merged.setdefault(group, []).extend(
            line for line in lines if line not in merged[group]
        )
    introduction = [*generated_intro]
    introduction.extend(line for line in curated_intro if line not in introduction)
    parts = [heading, *introduction]
    parts.extend(
        f"### {group}\n\n" + "\n".join(lines) for group, lines in merged.items()
    )
    return Section(generated.label, "\n\n".join(parts))


def has_release_entries(section: Section) -> bool:
    """Return whether a release section contains at least one list entry."""
    return any(line.startswith("- ") for line in section.text.splitlines())


def _required_version(section: Section) -> Version:
    """Return a section version or fail for an Unreleased section."""
    version = section.version
    if not version:
        raise ValueError("Archive contains an Unreleased section")
    return version


def archive_changelog(
    version: str, changelog_path: Path, archive_dir: Path
) -> list[Path]:
    """Move releases outside the target minor line into archive files."""
    target = parse_version(version)
    preamble, sections = split_changelog(changelog_path.read_text(encoding="utf-8"))
    inactive: dict[tuple[int, int], list[Section]] = {}
    active: list[Section] = []
    for section in sections:
        parsed = section.version
        if not parsed or parsed.major_minor == target.major_minor:
            active.append(section)
        else:
            inactive.setdefault(parsed.major_minor, []).append(section)
    if not inactive:
        return []
    archive_dir.mkdir(parents=True, exist_ok=True)
    updated: list[Path] = []
    for major_minor, moved in inactive.items():
        archive_path = archive_dir / f"v{major_minor[0]}.{major_minor[1]}.x.md"
        existing: list[Section] = []
        if archive_path.exists():
            _preamble, existing = split_changelog(
                archive_path.read_text(encoding="utf-8")
            )
        merged = {section.label: section for section in existing if section.version}
        merged.update({section.label: section for section in moved})
        ordered = sorted(
            merged.values(),
            key=lambda section: _required_version(section).sort_key(),
            reverse=True,
        )
        archive_preamble = (
            f"# Changelog archive: {major_minor[0]}.{major_minor[1]}.x\n\n"
            f"Archived {PROJECT_NAME} releases for the {major_minor[0]}.{major_minor[1]}.x minor version line."
        )
        archive_path.write_text(
            format_changelog(archive_preamble, ordered), encoding="utf-8"
        )
        updated.append(archive_path)
    changelog_path.write_text(format_changelog(preamble, active), encoding="utf-8")
    return updated


def extract_release_notes(tag: str, changelog_path: Path, archive_dir: Path) -> str:
    """Return release notes for a tag without its release heading."""
    if not tag.startswith("v"):
        raise ValueError("Release tag must start with v")
    version = parse_version(tag.removeprefix("v"))
    candidates = [
        changelog_path,
        archive_dir / f"v{version.major}.{version.minor}.x.md",
    ]
    matches: list[Section] = []
    for candidate in candidates:
        if candidate.exists():
            _preamble, sections = split_changelog(candidate.read_text(encoding="utf-8"))
            matches.extend(
                section for section in sections if section.label == version.text
            )
    if not matches:
        raise ValueError(f"Release notes for {version.text} were not found")
    if len(matches) > 1:
        raise ValueError(f"Duplicate changelog sections for {version.text}")
    body = "\n".join(matches[0].text.splitlines()[1:]).strip()
    if not body:
        raise ValueError(f"Release notes for {version.text} are empty")
    return body + "\n"


def validate_commit_title(title: str) -> None:
    """Validate a project Conventional Commit title."""
    if not COMMIT_TITLE_RE.fullmatch(title):
        raise ValueError(
            "Expected '<type>(optional-scope): description' using a documented Conventional Commit type"
        )


def project_versions(project_root: Path) -> dict[str, str]:
    """Read every tracked application version."""
    with (project_root / "pyproject.toml").open("rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)
    with (project_root / "uv.lock").open("rb") as uv_lock_file:
        uv_lock = tomllib.load(uv_lock_file)
    locked_project = next(
        (package for package in uv_lock["package"] if package["name"] == PROJECT_NAME),
        None,
    )
    if not locked_project:
        raise ValueError(f"{PROJECT_NAME} is missing from uv.lock")
    return {
        "pyproject.toml": str(pyproject["project"]["version"]),
        "uv.lock": str(locked_project["version"]),
    }


def validate_project_version(project_root: Path, expected: str | None = None) -> str:
    """Require synchronized project versions and optionally an expected value."""
    versions = project_versions(project_root)
    unique = set(versions.values())
    if len(unique) != 1:
        details = ", ".join(
            f"{source}={version}" for source, version in versions.items()
        )
        raise ValueError(f"Project versions are not synchronized: {details}")
    version = unique.pop()
    parse_version(version)
    if expected and version != parse_version(expected).text:
        raise ValueError(
            f"Project version {version} does not match expected {expected}"
        )
    return version


def validate_changelog_collection(
    changelog_path: Path, archive_dir: Path, expected_version: str | None = None
) -> None:
    """Validate active and archived changelogs against the current format."""
    paths = [changelog_path, *sorted(archive_dir.glob("v*.x.md"))]
    seen: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        preamble, sections = split_changelog(text)
        if not preamble.startswith("# Changelog"):
            raise ValueError(f"{path} is missing a changelog preamble")
        if not sections:
            raise ValueError(f"{path} contains no release sections")
        headings = [line for line in text.splitlines() if line.startswith("## ")]
        if len(headings) != len(sections):
            raise ValueError(f"{path} contains a legacy release heading")
        versions = [_required_version(section) for section in sections]
        if versions != sorted(versions, key=Version.sort_key, reverse=True):
            raise ValueError(f"{path} release sections are not newest first")
        for section, version in zip(sections, versions, strict=True):
            heading = HEADING_RE.fullmatch(section.text.splitlines()[0])
            if not heading or not heading.group("date"):
                raise ValueError(f"{section.label} is missing its release date")
            if section.label in seen:
                raise ValueError(f"Duplicate changelog section for {section.label}")
            seen.add(section.label)
            if (
                path != changelog_path
                and path.name != f"v{version.major}.{version.minor}.x.md"
            ):
                raise ValueError(
                    f"{section.label} belongs in v{version.major}.{version.minor}.x.md, not {path.name}"
                )
            groups = [
                group.group("group")
                for line in section.text.splitlines()
                if (group := GROUP_RE.fullmatch(line))
            ]
            if any(group not in CHANGELOG_GROUPS for group in groups):
                unsupported = next(
                    group for group in groups if group not in CHANGELOG_GROUPS
                )
                raise ValueError(f"Unsupported changelog heading: ### {unsupported}")
            if len(groups) != len(set(groups)):
                raise ValueError(f"{section.label} repeats a changelog heading")
            if groups != sorted(groups, key=CHANGELOG_GROUP_ORDER.index):
                raise ValueError(f"{section.label} changelog headings are out of order")
    if expected_version and expected_version not in seen:
        raise ValueError(f"Changelog section for {expected_version} was not found")
