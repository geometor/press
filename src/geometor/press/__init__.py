"""Public interface for the :mod:`geometor.press` catalog, census, and CLI."""

from __future__ import annotations

from .census import (
    RepoCensus,
    load_census_snapshot,
    scan_repo,
    scan_workspace,
    write_census_json,
)
from .cli import run_cli
from .shelf import (
    CatalogEntry,
    DerivedProduct,
    ImprintProfile,
    RepoMetrics,
    SeriesSpec,
    ShelfCatalog,
    WorkSpec,
    load_shelf,
)

__version__ = "0.1.0"

__all__ = [
    "CatalogEntry",
    "DerivedProduct",
    "ImprintProfile",
    "RepoCensus",
    "RepoMetrics",
    "SeriesSpec",
    "ShelfCatalog",
    "WorkSpec",
    "__version__",
    "load_census_snapshot",
    "load_shelf",
    "run_cli",
    "scan_repo",
    "scan_workspace",
    "write_census_json",
]
