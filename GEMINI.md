# GEOMETOR Press (`geometor/press`)

Editorial, brand, typographic, and multi-format product headquarters for **GEOMETOR Press**, powered by `photon-platform/publish`.

## Purpose

`geometor/press` maintains the master catalog ("the Shelf"), brand architecture, parametric cover/spine design standards, lookbook concept plates, and interactive object studios across all 47+ repositories in `/home/phi/PROJECTS/geometor` (and sibling imprints such as `phiarchitect/GOR-9`).

## Key Paths

- `resources/shelf.yaml` & `resources/shelf.json`: Canonical machine-readable catalog of series, readiness stages (`stage_1_seed` through `stage_4_codex_live`), book works, print/ebook formats, and derived tactile/digital products (`cards_collector`, `cards_greeting`, `poster`, `app`). Keep `shelf.json` synchronized whenever `shelf.yaml` is edited.
- `resources/census.json`: Empirical file, folio, RST, and SVG census across the workspace.
- `demos/cover_studio.html` & `demos/cards_posters_studio.html`: Zero-CDN standalone HTML/SVG studios (automatically synced into `docsrc/_static/studios/` during `publish build`).
- `docsrc/_static/lookbook/`: 12 concept design plates covering the 5-series spine lineup, Round 1 & Round 2 cover systems, collector card decks, greeting cards, and museum broadsides.
- `src/geometor/press/`:
  - `shelf.py`: Frozen dataclasses (`ShelfCatalog`, `CatalogEntry`, `WorkSpec`, `DerivedProduct`, `SeriesSpec`) and `load_shelf()`.
  - `census.py`: Read-only workspace scanner (`scan_repo`, `scan_workspace`, `load_census_snapshot`).
  - `cli.py`: `press` CLI (`summary`, `shelf`, `products`, `census`).

## Verification Gates (Python 3.13 / Offline Sandbox)

```bash
pytest
ruff check src tests
publish build
```
