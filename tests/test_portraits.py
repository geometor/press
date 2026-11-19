"""Tests for the GEOMETOR Press compass-and-straightedge portrait system."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

import pytest

from geometor.press import (
    MEDALLION_SPEC,
    build_aristotle_elements,
    build_durer_elements,
    build_euclid_elements,
    build_euler_elements,
    build_kepler_elements,
    build_pacioli_elements,
    build_plato_elements,
    load_portraits,
    render_medallion_svg,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

PORTRAIT_BUILDERS: dict[str, Callable[[], dict[str, list[dict[str, object]]]]] = {
    "durer": build_durer_elements,
    "euclid": build_euclid_elements,
    "plato": build_plato_elements,
    "aristotle": build_aristotle_elements,
    "pacioli": build_pacioli_elements,
    "kepler": build_kepler_elements,
    "euler": build_euler_elements,
}


def test_portraits_manifest_loads_all_seven_complete() -> None:
    """Verify resources/portraits.json loads all seven completed portrait studies."""
    records = load_portraits()
    ids = [rec.id for rec in records]
    assert ids[:7] == ["durer", "euclid", "plato", "aristotle", "pacioli", "kepler", "euler"]
    for rec in records:
        assert rec.status == "complete"
        assert "dark_svg" in rec.outputs
        assert "light_svg" in rec.outputs
    assert MEDALLION_SPEC["medallion_radius"] == 92.0


@pytest.mark.parametrize(("portrait_id", "builder"), sorted(PORTRAIT_BUILDERS.items()))
def test_portrait_medallion_strictly_lines_and_circles(
    portrait_id: str,
    builder: Callable[[], dict[str, list[dict[str, object]]]],
) -> None:
    """Verify each portrait medallion uses only lines, circles, and circular arcs (zero Beziers)."""
    layers = builder()
    assert set(layers.keys()) == {"scaffold", "golden", "primary", "detail"}
    total = sum(len(items) for items in layers.values())
    assert total >= 80, f"{portrait_id} has unexpectedly few elements ({total})"

    for theme in ("dark", "light"):
        svg = render_medallion_svg(layers, theme)
        assert 'viewBox="-102 -106 204 196"' in svg
        for path_d in re.findall(r'<path d="([^"]+)"', svg):
            assert not any(cmd in path_d for cmd in "CQSTcqst")
            assert " A " in path_d


@pytest.mark.parametrize("portrait_id", sorted(PORTRAIT_BUILDERS.keys()))
def test_exported_portrait_assets_present_and_bezier_free(portrait_id: str) -> None:
    """Verify exported dark and light SVGs exist and contain zero Bezier commands."""
    for theme in ("dark", "light"):
        svg_path = REPO_ROOT / "docsrc" / "_static" / "portraits" / f"{portrait_id}_{theme}.svg"
        assert svg_path.is_file()
        svg = svg_path.read_text(encoding="utf-8")
        assert 'viewBox="-102 -106 204 196"' in svg
        for path_d in re.findall(r'<path d="([^"]+)"', svg):
            assert not any(cmd in path_d for cmd in "CQSTcqst")
            assert " A " in path_d


def test_durer_interactive_studio_present() -> None:
    """Verify the interactive Dürer HTML studio demo exists in repo."""
    assert (REPO_ROOT / "demos" / "durer_portrait_studio.html").is_file()
