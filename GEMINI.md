# GEOMETOR Press (`geometor/press`)

Editorial, brand, typographic, and multi-format product headquarters for **GEOMETOR Press**, powered by `photon-platform/publish`.

## Purpose

`geometor/press` maintains the master catalog ("the Shelf"), brand architecture, parametric cover/spine design standards, lookbook concept plates, and interactive object studios across all 47+ repositories in `/home/phi/PROJECTS/geometor` (and sibling imprints such as `phiarchitect/GOR-9`).

## Key Paths

- `resources/shelf.yaml` & `resources/shelf.json`: Canonical machine-readable catalog of series, readiness stages (`stage_1_seed` through `stage_4_codex_live`), book works, print/ebook formats, and derived tactile/digital products (`cards_collector`, `cards_greeting`, `poster`, `app`). Keep `shelf.json` synchronized whenever `shelf.yaml` is edited.
- `resources/census.json`: Empirical file, folio, RST, and SVG census across the workspace.
- `demos/cover_studio.html` & `demos/cards_posters_studio.html`: Zero-CDN standalone HTML/SVG studios (automatically synced into `docsrc/_static/studios/` during `publish build`).
- `docsrc/_static/lookbook/`: 12 concept design plates covering the 5-series spine lineup, Round 1 & Round 2 cover systems, collector card decks, greeting cards, and museum broadsides.
- `docsrc/standards/index.rst`: Canonical Codex, SVG XML, `README.rst` storefront, multi-track Title Page, and `1280×640px` banner standards.
- `src/geometor/press/`:
  - `shelf.py`: Frozen dataclasses (`ShelfCatalog`, `CatalogEntry`, `WorkSpec`, `DerivedProduct`, `SeriesSpec`) and `load_shelf()`.
  - `census.py`: Read-only workspace scanner (`scan_repo`, `scan_workspace`, `load_census_snapshot`).
  - `cli.py`: `press` CLI (`summary`, `shelf`, `products`, `census`).

## Authoring, Scaffolding & Release Process

1. **Scaffold with `clerk init`**: Start new repositories via `photon-platform/clerk` so `pyproject.toml`, `README.rst`, `docsrc/`, and GitHub Actions follow current GEOMETOR standards.
2. **Strict XML & Theme-Safe SVGs**:
   - Escape `<`, `>`, and `&` inside XML attributes (`data-ref="&lt; A B C &gt;"`) and wrap inline `<script>` blocks in `//<![CDATA[ ... //]]>`.
   - Embed standalone `<style>` (`@media (prefers-color-scheme: dark)` + opaque `.svg-bg` canvas) on hero SVGs and validate with `xml.etree.ElementTree.fromstring`.
3. **Storefront `README.rst` & GitHub Metadata**:
   - Never wrap `` `Title <url>`_ `` in `**...**`.
   - Lead with `GEOMETOR • <repo>`, `**Visit the Online Archive:**`, clickable construction hero `.. image::`, and `•`-delimited `semantic digital archive` description (English titles, keeping accepted loan-titles like *Almagest*, *Metrica*, *Organon*, *Summa Theologiae*).
   - Validate `README.rst` with `docutils` (0 warnings).
4. **English Elevation & Multi-Track Book Title Pages**:
   - Keep primary `docsrc/<book>/index.rst` pure English (`<h1>`, `:book_title:`, `:nav_title:`, `:breadcrumb_title:`) with italicized native title in `.. rubric::`, and pair bilingual works with a dedicated `title-<lang>.rst` (`:type: book_title`, `:layout: book`) wired via `:tracks:`.
   - Keep menus year-free (`:nav_title:`, `:breadcrumb_title:`, `:caption:`) and use canonical full English track labels (`English`, `Latin`, `Greek`, `German`, `French`, `Italian`, `Summary`, `Notes`).
5. **Social & GitHub Banners (`1280×640px`)**:
   - Run `publish social-banner --force` to generate `1280×640px` `banner.png`, `<book>.png`, and `github.png` in `docsrc/_static/social/`.

## Verification Gates (Python 3.13 / Offline Sandbox)

```bash
uv run --no-sync pytest
ruff check src tests
publish build
```
