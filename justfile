set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
project_name := "glinkfix"

# Show available recipes
default:
    @just --list

# --------------------------------------------

# Open a generated HTML report in the default browser
_display_webpage web_path:
    #!/usr/bin/env python3
    import webbrowser
    from pathlib import Path
    p = Path(".").resolve() / "{{web_path}}"
    if not p.exists():
        raise SystemExit(f"File not found: {p}")
    url = f"file://{p}"
    print(f"Coverage report: {url}")
    webbrowser.open(url, new=2)

# --------------------------------------------

# Require initial setup to be complete
_require_setup:
    #!/usr/bin/env bash
    if [ ! -f .init/setup ]; then
        echo 'Please run "just setup" first'
        exit 1
    fi

# --------------------------------------------

# Build package for publishing
build:
    #!/usr/bin/env bash
    export UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}"
    rm -rf dist
    uv build

# --------------------------------------------

# Prepare a project version and generate its changelog
bump version:
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run python -m scripts.bump_version {{version}}

# --------------------------------------------

# Preview user-visible changes since the latest release
changelog:
    git-cliff --unreleased

# --------------------------------------------

# Clean python runtime and build artifacts
clean:
    echo "Cleaning python runtime and build artifacts"
    rm -rf build dist .*cache htmlcov
    rm -rf site cover coverage.xml .coverage .coverage.*
    rm -rf .tox .nox .hypothesis .pybuilder .pytype .pyre
    rm -rf .release-notes.md
    rm -rf develop-eggs downloads eggs parts sdist var wheels
    rm -rf share/python-wheels target
    find . -type d -name __pycache__ -exec rm -rf {} \; -prune
    find . -type d -name .ipynb_checkpoints -exec rm -rf {} \; -prune
    find . -type d -name .pytest_cache -exec rm -rf {} \; -prune
    find . -type d -name .eggs -exec rm -rf {} \; -prune
    find . -type d -name '*.egg-info' -exec rm -rf {} \; -prune
    find . -type f -name .DS_Store -delete
    find . -type f -name '._*' -delete
    find . -type f -name '*.egg' -delete
    find . -type f -name '*.pyc' -delete
    find . -type f -name '*.pyo' -delete
    find . -type f -name '*.coverage' -delete

# --------------------------------------------

# Run tests with coverage reporting
coverage:
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run coverage run -m pytest --tb=short
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run coverage report -m
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run coverage html

# --------------------------------------------

# Run coverage and open HTML report in browser
coverage-open: coverage
    just _display_webpage "htmlcov/index.html"

# --------------------------------------------

# Format Python files and apply fixable Ruff lint rules
format:
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run ruff check --fix .
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run ruff format .

# --------------------------------------------

# Run lint checks
lint:
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run ruff check .
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run ruff format --check .

# --------------------------------------------

# Show outdated top-level dependencies
outdated:
    #!/usr/bin/env bash
    export UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}"
    uv tree --outdated --depth=1 | awk '
        /latest/ {
            found = 1
            print
        }
        END {
            if (!found) {
                print "No outdated top-level dependencies found."
            }
        }
    '

# --------------------------------------------

# Reset the project state
reset: clean
    echo "Resetting project state"
    rm -rf .init .venv

# --------------------------------------------

# Initialize the project environment
setup:
    #!/usr/bin/env bash
    if [ ! -f .init/setup ]; then
        if ! command -v uv >/dev/null 2>&1; then
            echo "{{project_name}} requires uv. See README for instructions."
            exit 1
        fi
        if ! command -v git >/dev/null 2>&1; then
            echo "{{project_name}} requires git. See README for instructions."
            exit 1
        fi
        if ! command -v git-cliff >/dev/null 2>&1; then
            echo "{{project_name}} requires git-cliff. See README for instructions."
            exit 1
        fi
        mkdir -p scratch .init
        touch .init/setup
    else
        echo "Initial setup is already complete. If you are having issues, run:"
        echo
        echo "just reset"
        echo "just setup"
        echo
        exit 0
    fi
    export UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}"
    export UV_PYTHON_PREFERENCE=only-managed
    uv sync --all-groups --frozen

# --------------------------------------------

# Sync dependencies with the lockfile
sync: _require_setup
    #!/usr/bin/env bash
    export UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}"
    uv sync --all-groups

# --------------------------------------------

# Generate and push the validated release tag
tag-release:
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run python -m scripts.tag_release

# --------------------------------------------

# Run pytest with --tb=short option
test:
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run pytest --tb=short

# --------------------------------------------

# Run static type checks
typecheck:
    UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}" uv run mypy src scripts

# --------------------------------------------

# Upgrade dependencies
upgrade: _require_setup
    bash ./scripts/upgrade_dependencies.sh
