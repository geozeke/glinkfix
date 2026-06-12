"""Tests for dependency upgrade helper logic."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "dependency_upgrade_commit.py"
)
SPEC = importlib.util.spec_from_file_location("dependency_upgrade_commit", SCRIPT_PATH)
assert SPEC is not None
dependency_upgrade_commit = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = dependency_upgrade_commit
SPEC.loader.exec_module(dependency_upgrade_commit)


def test_first_order_dependencies_include_runtime_and_groups(tmp_path: Path) -> None:
    """Test direct dependency discovery from project metadata."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """[project]
dependencies = [
    "pyperclip>=1.9.0",
    "tomli>=1.1.0 ; python_full_version < '3.11'",
]

[dependency-groups]
dev = [
    "pytest>=8.3.3",
    "coverage[toml]>=7.6.1",
]
""",
        encoding="utf-8",
    )

    dependencies = dependency_upgrade_commit.first_order_dependencies(pyproject)

    assert dependencies == {
        "pyperclip": "pyperclip",
        "tomli": "tomli",
        "pytest": "pytest",
        "coverage": "coverage",
    }


def test_locked_versions_ignores_editable_project(tmp_path: Path) -> None:
    """Test that lock snapshots ignore the editable root project."""
    lockfile = tmp_path / "uv.lock"
    lockfile.write_text(
        """[[package]]
name = "glinkfix"
version = "2.1.0"
source = { editable = "." }

[[package]]
name = "pyperclip"
version = "1.11.0"
source = { registry = "https://pypi.org/simple" }
""",
        encoding="utf-8",
    )

    assert dependency_upgrade_commit.locked_versions(lockfile) == {
        "pyperclip": "1.11.0"
    }


def test_dependency_updates_ignores_transitive_only_changes() -> None:
    """Test that transitive-only lockfile churn is not reported."""
    dependencies = {"pytest": "pytest"}
    before_versions = {"pytest": "9.0.3", "pluggy": "1.6.0"}
    after_versions = {"pytest": "9.0.3", "pluggy": "1.7.0"}

    updates = dependency_upgrade_commit.dependency_updates(
        dependencies,
        before_versions,
        after_versions,
    )

    assert updates == []


def test_outdated_first_order_packages_ignores_transitive_packages() -> None:
    """Test parsing outdated first-order packages from ``uv tree`` output."""
    dependencies = {
        "coverage": "coverage",
        "pyperclip": "pyperclip",
        "pytest": "pytest",
    }
    tree_output = """Resolved 12 packages in 3ms
coverage[toml] v7.14.0 (group: dev) (latest: v7.14.1)
glinkfix v2.1.0
├── pyperclip v1.9.0 (latest: v1.11.0)
├── pytest v8.3.3 (latest: v9.0.3) (group: dev)
│   └── pluggy v1.6.0 (latest: v1.7.0)
└── ruff v0.15.13
"""

    packages = dependency_upgrade_commit.outdated_first_order_packages(
        dependencies,
        tree_output,
    )

    assert packages == ["coverage", "pyperclip", "pytest"]


def test_render_commit_message_lists_changed_direct_dependencies() -> None:
    """Test rendering the local dependency upgrade commit message."""
    updates = [
        dependency_upgrade_commit.DependencyUpdate(
            name="pyperclip",
            old_version="1.9.0",
            new_version="1.11.0",
        ),
        dependency_upgrade_commit.DependencyUpdate(
            name="pytest",
            old_version="8.3.3",
            new_version="9.0.3",
        ),
    ]

    message = dependency_upgrade_commit.render_commit_message(updates)

    assert message == (
        "deps: DEPS-See commit msg for list\n"
        "\n"
        "- pyperclip: 1.9.0 -> 1.11.0\n"
        "- pytest: 8.3.3 -> 9.0.3\n"
    )
