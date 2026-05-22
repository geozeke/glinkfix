# glinkfix

`glinkfix` is a Python CLI package that converts Google Drive sharing
links into links suitable for embedding or direct download.

## Project Layout

- `src/glinkfix/app.py`: CLI entry point and argument parsing for the
  `glinkfix` console script.
- `src/glinkfix/tools.py`: core Google Drive link rewriting logic.
- `tests/`: pytest coverage and test data for link rewriting behavior.
- `pyproject.toml`: package metadata, build backend, dependencies, and
  Ruff/Coverage settings.
- `justfile`: common setup, test, build, release, and maintenance tasks.

## Working Constraints

- Do not traverse, modify, or rely on `.venv/`.
- Do not traverse cache or generated-state directories such as
  `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `__pycache__/`, or
  `.cache/` unless the task explicitly requires it.
- Use `rg` for searches and `just` or `uv` for common project tasks.
- Prefer `pathlib.Path` objects over raw path strings where practical.
- Prefer truthiness checks like `if value:` and `if not value:` over
  explicit empty or `None` comparisons when they are equivalent.
- Use strict NumPy-style docstrings for all function, class, and module
  docstrings.
- Use snake case for variable names.
- Run Ruff on any Python code changes or additions.
- When reviewing or modifying `.gitignore`, also check whether Git
  global excludes are configured, for example with
  `git config --global core.excludesfile`.
- Wrap Markdown prose to 72 characters when practical, without breaking
  links, code spans, tables, or other formatting.
- Keep documentation and metadata consistent with code changes,
  including README content, AGENTS.md, argparse messages, docstrings, and
  code comments.

## Verification

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src`
