import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def get_version() -> str:
    """Return the version number of the project.

    Starting at the current directory, search for pyproject.toml,
    working your way up the parents in the directory tree. This allows
    the version number to be maintained on one place.

    IMPORTANT: For this to work properly when you distribute your
    package, you must include the following in your `pyproject.toml`
    file:

    ```
    [tool.hatch.build.targets.wheel.force-include]
    "./pyproject.toml" = "<package name>/pyproject.toml"
    ```

    Returns
    -------
    str
        Version number of the project.
    """
    start = Path(__file__).absolute().parents

    for path in start:
        for file in path.glob("*.toml"):
            if file.name == "pyproject.toml":
                try:
                    with open(file, "rb") as f:
                        tom = tomllib.load(f)
                    return tom["project"]["version"]
                except Exception:
                    return "unknown"

    return "unknown"


# ======================================================================
