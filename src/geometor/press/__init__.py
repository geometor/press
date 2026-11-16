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
from .portrait_studies import build_durer_elements
from .portraits import (
    MEDALLION_SPEC,
    PortraitRecord,
    load_portraits,
    render_medallion_svg,
    tangent_wave_arcs,
)
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

__version__ = "0.1.1"

__all__ = [
    "CatalogEntry",
    "DerivedProduct",
    "ImprintProfile",
    "MEDALLION_SPEC",
    "PortraitRecord",
    "RepoCensus",
    "RepoMetrics",
    "SeriesSpec",
    "ShelfCatalog",
    "WorkSpec",
    "__version__",
    "build_durer_elements",
    "load_census_snapshot",
    "load_portraits",
    "load_shelf",
    "render_medallion_svg",
    "run_cli",
    "scan_repo",
    "scan_workspace",
    "tangent_wave_arcs",
    "write_census_json",
]
