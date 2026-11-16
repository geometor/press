"""Tests for the GEOMETOR Press compass-and-straightedge portrait system."""

from __future__ import annotations

import re
from pathlib import Path

from geometor.press import (
    MEDALLION_SPEC,
    build_durer_elements,
    load_portraits,
    render_medallion_svg,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_portraits_manifest_loads_with_durer_and_next_five() -> None:
    """Verify resources/portraits.json loads Dürer and the Next-5 reference queue."""
    records = load_portraits()
    ids = [rec.id for rec in records]
    assert ids[:6] == ["durer", "euclid", "plato", "aristotle", "pacioli", "kepler"]
    assert "euler" in ids
    durer = next(rec for rec in records if rec.id == "durer")
    assert durer.status == "complete"
    assert MEDALLION_SPEC["medallion_radius"] == 92.0


def test_durer_medallion_strictly_lines_and_circles() -> None:
    """Verify Dürer 1500 medallion uses only lines, circles, and circular arcs (zero Beziers)."""
    layers = build_durer_elements()
    assert set(layers.keys()) == {"scaffold", "golden", "primary", "detail"}
    total = sum(len(items) for items in layers.values())
    assert total >= 150

    for theme in ("dark", "light"):
        svg = render_medallion_svg(layers, theme)
        assert 'viewBox="-102 -106 204 196"' in svg
        for path_d in re.findall(r'<path d="([^"]+)"', svg):
            assert not any(cmd in path_d for cmd in "CQSTcqst")
            assert " A " in path_d


def test_exported_portrait_assets_present() -> None:
    """Verify exported Dürer SVGs and interactive HTML studio exist in repo."""
    assert (REPO_ROOT / "docsrc" / "_static" / "portraits" / "durer_dark.svg").is_file()
    assert (REPO_ROOT / "docsrc" / "_static" / "portraits" / "durer_light.svg").is_file()
    assert (REPO_ROOT / "demos" / "durer_portrait_studio.html").is_file()
