"""Unit tests for the :mod:`geometor.press` shelf catalog, census, and CLI."""

from __future__ import annotations

import json
from pathlib import Path

from geometor.press import (
    __version__,
    load_census_snapshot,
    load_shelf,
    run_cli,
    scan_repo,
)
from geometor.press.shelf import DEFAULT_RESOURCES_DIR


def test_version() -> None:
    """Package exposes expected semantic version."""
    assert __version__ == "0.1.1"


def test_load_shelf_yaml_and_json_parity() -> None:
    """Shelf catalog loads cleanly from JSON mirror and matches YAML structure."""
    json_path = DEFAULT_RESOURCES_DIR / "shelf.json"
    catalog = load_shelf(json_path)
    assert catalog.imprint.name == "GEOMETOR Press"
    assert catalog.imprint.engine == "photon-platform/publish"
    assert set(catalog.series.keys()) == {
        "fontes",
        "noetica",
        "synthesis",
        "natura",
        "architectura",
    }
    assert len(catalog.entries) >= 47

    counts = catalog.summary_counts()
    assert counts["works"] >= 44
    assert counts["svgs"] >= 71000
    assert counts["folios"] >= 2300
    assert counts["derived_products"]["cards_collector"] >= 8
    assert counts["derived_products"]["poster"] >= 18
    assert counts["derived_products"]["cards_greeting"] >= 8


def test_shelf_queries() -> None:
    """Stage, series, repo, and derived-product filters return expected entries."""
    catalog = load_shelf(DEFAULT_RESOURCES_DIR / "shelf.json")

    hoenen = catalog.by_repo("hoenen")
    assert hoenen is not None
    assert hoenen.series == "noetica"
    assert hoenen.stage == "stage_4_codex_live"
    assert hoenen.works[0].slug == "de_noetica_geometriae"

    press_entry = catalog.by_repo("press")
    assert press_entry is not None
    assert press_entry.series == "architectura"

    stage4 = catalog.by_stage("stage_4_codex_live")
    assert len(stage4) >= 12

    decks = catalog.all_derived_products(kind="cards_collector")
    deck_repos = {entry.repo for entry, _ in decks}
    assert {"divine", "etc", "pacioli"}.issubset(deck_repos)


def test_census_snapshot_and_live_scan() -> None:
    """Census snapshot deserializes cleanly and scan_repo inspects press itself."""
    records = load_census_snapshot()
    assert len(records) >= 47
    names = {rec.name for rec in records}
    assert {"euclid", "hoenen", "divine", "etc"}.issubset(names)

    press_root = Path(__file__).resolve().parents[1]
    live = scan_repo(press_root)
    assert live.name == "press"
    assert live.version in {"0.1.0", "0.1.1"}
    assert live.py_files >= 4
    assert live.has_demos is True


def test_cli_commands(capsys: object) -> None:
    """CLI subcommands execute with exit code zero."""
    assert run_cli(["summary"]) == 0
    assert run_cli(["shelf", "--stage", "stage_4_codex_live"]) == 0
    assert run_cli(["products", "--kind", "cards_collector"]) == 0
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert "GEOMETOR Press" in captured.out
    assert "The Golden Deck" in captured.out


def test_studios_and_lookbook_assets_exist() -> None:
    """All 12 lookbook images and both standalone zero-CDN studio HTML files exist."""
    press_root = Path(__file__).resolve().parents[1]
    lookbook_dir = press_root / "docsrc" / "_static" / "lookbook"
    jpgs = sorted(lookbook_dir.glob("*.jpg"))
    assert len(jpgs) == 12

    for studio_name in ("cover_studio.html", "cards_posters_studio.html"):
        demo_file = press_root / "demos" / studio_name
        assert demo_file.is_file()
        html = demo_file.read_text(encoding="utf-8")
        assert "gstatic.com" not in html
        assert "<svg" in html

    raw_json = json.loads(
        (press_root / "resources" / "shelf.json").read_text(encoding="utf-8")
    )
    assert len(raw_json["catalog"]) >= 48
