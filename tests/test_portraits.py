"""Tests for the GEOMETOR Press compass-and-straightedge portrait system."""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Callable

import pytest

from geometor.press import (
    MEDALLION_SPEC,
    build_apollonius_elements,
    build_aquinas_elements,
    build_archimedes_elements,
    build_aristotle_elements,
    build_bertrand_russell_elements,
    build_byrne_elements,
    build_casey_elements,
    build_cusa_elements,
    build_durer_elements,
    build_empty_medallion_svg,
    build_ernst_haeckel_elements,
    build_euclid_elements,
    build_euler_elements,
    build_feuerbach_elements,
    build_fibonacci_elements,
    build_heath_elements,
    build_heron_elements,
    build_hilbert_elements,
    build_hoenen_elements,
    build_kepler_elements,
    build_klein_elements,
    build_lemoine_elements,
    build_leonardo_elements,
    build_livio_elements,
    build_mascheroni_elements,
    build_nicomachus_elements,
    build_pacioli_elements,
    build_pascal_elements,
    build_pasch_elements,
    build_petersen_elements,
    build_piero_elements,
    build_plato_elements,
    build_poincare_elements,
    build_ptolemy_elements,
    build_staudt_elements,
    build_steiner_elements,
    build_thompson_elements,
    build_walter_russell_elements,
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
    "archimedes": build_archimedes_elements,
    "aquinas": build_aquinas_elements,
    "pascal": build_pascal_elements,
    "steiner": build_steiner_elements,
    "byrne": build_byrne_elements,
    "hilbert": build_hilbert_elements,
    "bertrand_russell": build_bertrand_russell_elements,
    "heath": build_heath_elements,
    "leonardo": build_leonardo_elements,
    "piero": build_piero_elements,
    "cusa": build_cusa_elements,
    "fibonacci": build_fibonacci_elements,
    "ptolemy": build_ptolemy_elements,
    "klein": build_klein_elements,
    "poincare": build_poincare_elements,
    "thompson": build_thompson_elements,
    "hoenen": build_hoenen_elements,
    "walter_russell": build_walter_russell_elements,
    "apollonius": build_apollonius_elements,
    "heron": build_heron_elements,
    "nicomachus": build_nicomachus_elements,
    "mascheroni": build_mascheroni_elements,
    "staudt": build_staudt_elements,
    "feuerbach": build_feuerbach_elements,
    "casey": build_casey_elements,
    "ernst_haeckel": build_ernst_haeckel_elements,
    "petersen": build_petersen_elements,
    "lemoine": build_lemoine_elements,
    "pasch": build_pasch_elements,
    "livio": build_livio_elements,
}

MEDALLION_BUILDER_IDS = {
    "archimedes",
    "aquinas",
    "pascal",
    "steiner",
    "byrne",
    "hilbert",
    "bertrand_russell",
    "heath",
    "leonardo",
    "piero",
    "cusa",
    "fibonacci",
    "ptolemy",
    "klein",
    "poincare",
    "thompson",
    "hoenen",
    "walter_russell",
    "apollonius",
    "heron",
    "nicomachus",
    "mascheroni",
    "staudt",
    "feuerbach",
    "casey",
    "ernst_haeckel",
    "petersen",
    "lemoine",
    "pasch",
    "livio",
}


def test_portraits_manifest_loads_pantheon_and_thirty_seven_complete() -> None:
    """Verify resources/portraits.json loads the 48-slot Pantheon with 37 completed studies."""
    records = load_portraits()
    assert len(records) == 48
    ids = [rec.id for rec in records]
    assert ids[:7] == ["durer", "euclid", "plato", "aristotle", "pacioli", "kepler", "euler"]
    completed = [rec for rec in records if rec.status == "complete"]
    assert len(completed) == 37
    for rec in completed:
        assert "dark_svg" in rec.outputs
        assert "light_svg" in rec.outputs
    researched = [rec for rec in records if rec.status == "researched"]
    assert len(researched) == 11
    assert MEDALLION_SPEC["medallion_radius"] == 92.0


def test_empty_medallion_svg_is_bezier_free() -> None:
    """Verify the empty canonical medallion scaffold renders cleanly with zero Beziers."""
    svg = build_empty_medallion_svg("dark")
    assert 'viewBox="-102 -106 204 196"' in svg
    for path_d in re.findall(r'<path d="([^"]+)"', svg):
        assert not any(cmd in path_d for cmd in "CQSTcqst")


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


@pytest.mark.parametrize("portrait_id", sorted(MEDALLION_BUILDER_IDS))
def test_medallion_builder_studies_strictly_inside_medallion_bounds(portrait_id: str) -> None:
    """Verify every line and arc endpoint in Studies 08-25 stays inside MED_R = 92.0."""
    layers = PORTRAIT_BUILDERS[portrait_id]()
    med_cx, med_cy = MEDALLION_SPEC["medallion_center"]
    limit = float(MEDALLION_SPEC["medallion_radius"]) + 1.0
    for layer_name, items in layers.items():
        for el in items:
            kind = el["kind"]
            if kind == "line":
                for x_k, y_k in (("x1", "y1"), ("x2", "y2")):
                    dist = math.hypot(float(el[x_k]) - med_cx, float(el[y_k]) - med_cy)
                    assert dist <= limit, f"{portrait_id}/{layer_name} line exceeds MED_R: {dist:.2f}"
            elif kind == "arc":
                nums = [float(m) for m in re.findall(r"-?\d+(?:\.\d+)?", str(el["d"]))]
                for px, py in ((nums[0], nums[1]), (nums[-2], nums[-1])):
                    dist = math.hypot(px - med_cx, py - med_cy)
                    assert dist <= limit, f"{portrait_id}/{layer_name} arc exceeds MED_R: {dist:.2f}"


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


def test_durer_interactive_studio_and_live_poster_present() -> None:
    """Verify interactive studios and live Pantheon poster exist in repo."""
    assert (REPO_ROOT / "demos" / "durer_portrait_studio.html").is_file()
    assert (REPO_ROOT / "demos" / "portraits_gallery.html").is_file()
    assert (REPO_ROOT / "editions" / "posters" / "geometor_portraits_poster.png").is_file()
