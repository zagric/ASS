# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import importlib.metadata
from pathlib import Path
import tomllib


try:
    __version__ = importlib.metadata.version("backend")
except importlib.metadata.PackageNotFoundError:
    project_root = Path(__file__).parent.parent.parent
    pyproject_path = project_root / "pyproject.toml"

    with Path(pyproject_path).open("rb") as f:
        pyproject_data = tomllib.load(f)

    __version__ = pyproject_data["project"]["version"]
