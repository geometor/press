"""Typed loader and query engine for the GEOMETOR Press shelf manifest."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

DEFAULT_RESOURCES_DIR = Path(__file__).resolve().parents[3] / "resources"


@dataclass(frozen=True)
class ImprintProfile:
    """Core brand metadata for the GEOMETOR Press imprint."""

    name: str
    tagline: str
    engine: str
    portal: str
    colophon_motif: str


@dataclass(frozen=True)
class SeriesSpec:
    """Color-coded spine series definition."""

    key: str
    title: str
    subtitle: str
    accent: str


@dataclass(frozen=True)
class RepoMetrics:
    """Repository content and asset metrics recorded in the shelf manifest."""

    docsrc_rst: int = 0
    folios: int = 0
    svgs: int = 0
    py_modules: int = 0


@dataclass(frozen=True)
class WorkSpec:
    """Individual book, treatise, or monograph work entry."""

    slug: str
    title: str
    author: str
    year: str
    languages: tuple[str, ...]
    subtitle: str = ""
    notes: str = ""


@dataclass(frozen=True)
class DerivedProduct:
    """Non-book tactile or interactive product derived from a repository."""

    kind: str
    title: str


@dataclass(frozen=True)
class CatalogEntry:
    """Shelf catalog record for a single repository and its published works."""

    repo: str
    series: str
    stage: str
    version: str
    metrics: RepoMetrics
    works: tuple[WorkSpec, ...]
    formats: tuple[str, ...]
    derived_products: tuple[DerivedProduct, ...]


@dataclass(frozen=True)
class ShelfCatalog:
    """Immutable master catalog across all GEOMETOR Press series and stages."""

    imprint: ImprintProfile
    series: dict[str, SeriesSpec]
    entries: tuple[CatalogEntry, ...]

    def by_stage(self, stage: str) -> list[CatalogEntry]:
        """Return catalog entries matching a specific readiness stage."""
        return [entry for entry in self.entries if entry.stage == stage]

    def by_series(self, series_key: str) -> list[CatalogEntry]:
        """Return catalog entries assigned to a specific spine series."""
        return [entry for entry in self.entries if entry.series == series_key]

    def by_repo(self, repo_name: str) -> CatalogEntry | None:
        """Look up a catalog entry by repository slug."""
        for entry in self.entries:
            if entry.repo == repo_name:
                return entry
        return None

    def all_works(self) -> list[tuple[CatalogEntry, WorkSpec]]:
        """Return every ``(entry, work)`` pair across the shelf."""
        pairs: list[tuple[CatalogEntry, WorkSpec]] = []
        for entry in self.entries:
            for work in entry.works:
                pairs.append((entry, work))
        return pairs

    def all_derived_products(
        self, kind: str | None = None
    ) -> list[tuple[CatalogEntry, DerivedProduct]]:
        """Return derived non-book products, optionally filtered by kind.

        Args:
            kind: Optional product kind filter (e.g., ``"cards_collector"``,
                ``"cards_greeting"``, ``"poster"``, or ``"app"``).

        Returns:
            Matching ``(entry, product)`` pairs in catalog order.
        """
        results: list[tuple[CatalogEntry, DerivedProduct]] = []
        for entry in self.entries:
            for prod in entry.derived_products:
                if kind is None or prod.kind == kind:
                    results.append((entry, prod))
        return results

    def summary_counts(self) -> dict[str, Any]:
        """Compute aggregate counts across stages, series, works, and assets."""
        stage_counts: dict[str, int] = {}
        series_counts: dict[str, int] = {}
        product_counts: dict[str, int] = {}
        total_rst = 0
        total_folios = 0
        total_svgs = 0
        total_works = 0

        for entry in self.entries:
            stage_counts[entry.stage] = stage_counts.get(entry.stage, 0) + 1
            series_counts[entry.series] = series_counts.get(entry.series, 0) + 1
            total_rst += entry.metrics.docsrc_rst
            total_folios += entry.metrics.folios
            total_svgs += entry.metrics.svgs
            total_works += len(entry.works)
            for prod in entry.derived_products:
                product_counts[prod.kind] = product_counts.get(prod.kind, 0) + 1

        return {
            "repositories": len(self.entries),
            "works": total_works,
            "docsrc_rst": total_rst,
            "folios": total_folios,
            "svgs": total_svgs,
            "stages": stage_counts,
            "series": series_counts,
            "derived_products": product_counts,
        }


def _read_raw_shelf(path: Path | None = None) -> dict[str, Any]:
    """Read raw shelf dictionary from YAML (preferred) or JSON mirror.

    Args:
        path: Optional explicit path to ``shelf.yaml`` or ``shelf.json``.

    Returns:
        Parsed top-level dictionary representing the shelf manifest.

    Raises:
        FileNotFoundError: If neither the requested file nor default resources exist.
    """
    if path is not None:
        if not path.is_file():
            msg = f"Shelf manifest not found: {path}"
            raise FileNotFoundError(msg)
        if path.suffix.lower() == ".json":
            return dict(json.loads(path.read_text(encoding="utf-8")))
        try:
            import yaml  # type: ignore[import-untyped]

            return dict(yaml.safe_load(path.read_text(encoding="utf-8")))
        except ModuleNotFoundError:
            json_fallback = path.with_suffix(".json")
            if json_fallback.is_file():
                return dict(json.loads(json_fallback.read_text(encoding="utf-8")))
            raise

    yaml_path = DEFAULT_RESOURCES_DIR / "shelf.yaml"
    json_path = DEFAULT_RESOURCES_DIR / "shelf.json"
    if yaml_path.is_file():
        try:
            import yaml

            return dict(yaml.safe_load(yaml_path.read_text(encoding="utf-8")))
        except ModuleNotFoundError:
            if json_path.is_file():
                return dict(json.loads(json_path.read_text(encoding="utf-8")))
    if json_path.is_file():
        return dict(json.loads(json_path.read_text(encoding="utf-8")))

    msg = f"No shelf manifest found in {DEFAULT_RESOURCES_DIR}"
    raise FileNotFoundError(msg)


def load_shelf(path: Path | None = None) -> ShelfCatalog:
    """Load and validate the GEOMETOR Press master shelf catalog.

    Args:
        path: Optional explicit path to ``shelf.yaml`` or ``shelf.json``.

    Returns:
        Typed :class:`ShelfCatalog` instance.
    """
    raw = _read_raw_shelf(path)
    imp = raw["imprint"]
    imprint = ImprintProfile(
        name=str(imp["name"]),
        tagline=str(imp["tagline"]),
        engine=str(imp["engine"]),
        portal=str(imp["portal"]),
        colophon_motif=str(imp["colophon_motif"]),
    )

    series_map: dict[str, SeriesSpec] = {}
    for key, s_raw in raw.get("series", {}).items():
        series_map[str(key)] = SeriesSpec(
            key=str(key),
            title=str(s_raw["title"]),
            subtitle=str(s_raw["subtitle"]),
            accent=str(s_raw["accent"]),
        )

    entries: list[CatalogEntry] = []
    for item in raw.get("catalog", []):
        m_raw = item.get("metrics", {})
        metrics = RepoMetrics(
            docsrc_rst=int(m_raw.get("docsrc_rst", 0)),
            folios=int(m_raw.get("folios", 0)),
            svgs=int(m_raw.get("svgs", 0)),
            py_modules=int(m_raw.get("py_modules", 0)),
        )
        works = tuple(
            WorkSpec(
                slug=str(w["slug"]),
                title=str(w["title"]),
                subtitle=str(w.get("subtitle", "")),
                author=str(w.get("author", "")),
                year=str(w.get("year", "")),
                languages=tuple(str(lang) for lang in w.get("languages", [])),
                notes=str(w.get("notes", "")),
            )
            for w in item.get("works", [])
        )
        products = tuple(
            DerivedProduct(
                kind=str(p["kind"]),
                title=str(p["title"]),
            )
            for p in item.get("derived_products", [])
        )
        entries.append(
            CatalogEntry(
                repo=str(item["repo"]),
                series=str(item["series"]),
                stage=str(item["stage"]),
                version=str(item.get("version", "")),
                metrics=metrics,
                works=works,
                formats=tuple(str(fmt) for fmt in item.get("formats", [])),
                derived_products=products,
            )
        )

    return ShelfCatalog(
        imprint=imprint,
        series=series_map,
        entries=tuple(entries),
    )
