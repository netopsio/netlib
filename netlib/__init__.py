"""NetLib - Network device connection library."""

import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

__name__ = "netlib"

# Try to get version from installed package metadata
try:
    __version__ = version("netlib")
except PackageNotFoundError:
    # Fallback: read from pyproject.toml during development
    try:
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            try:
                import tomli as tomllib  # type: ignore[import-not-found]
            except ImportError:
                # If tomli not available, use fallback version
                __version__ = "0.2.0-dev"
                tomllib = None  # type: ignore[assignment,unused-ignore]

        if tomllib is not None:
            pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
            if pyproject_path.exists():
                with pyproject_path.open("rb") as f:
                    pyproject_data = tomllib.load(f)
                __version__ = pyproject_data["tool"]["poetry"]["version"]
            else:
                __version__ = "0.2.0-dev"
    except Exception:
        __version__ = "0.2.0-dev"

from netlib.conn_type import SSH, Telnet
from netlib.user_keyring import KeyRing

__all__ = ["SSH", "KeyRing", "Telnet"]
