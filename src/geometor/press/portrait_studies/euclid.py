"""Study 02: Euclid of Alexandria in lines, circles, and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import (
    MED_CX,
    MED_CY,
    MED_R,
    arc_path,
    clip_line_to_medallion,
    normalize_short_span,
    render_medallion_svg,
    tangent_wave_arcs,
)

__all__ = ["build_euclid_elements", "build_euclid_svg", "write_euclid_svgs"]

DEFAULT_PORTRAITS_STATIC_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"
)


def build_euclid_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Euclid of Alexandria medallion strictly from lines, circles, and circular arcs.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc beard & drapery waves.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``primary``, and ``detail`` primitive lists.
    """
    radius_head = 26.0
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    sqrt3 = math.sqrt(3.0)

    scaffold: list[dict[str, Any]] = []
    primary: list[dict[str, Any]] = []
    detail: list[dict[str, Any]] = []
    golden: list[dict[str, Any]] = []

    def add_circle(
        layer: list[dict[str, Any]],
        cx: float,
        cy: float,
        r: float,
        *,
        filled: bool = False,
    ) -> None:
        layer.append({"kind": "circle", "cx": cx, "cy": cy, "r": r, "filled": filled})

    def add_line(
        layer: list[dict[str, Any]],
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        clip: bool = True,
    ) -> None:
        if clip:
            clipped = clip_line_to_medallion(x1, y1, x2, y2)
            if clipped is None:
                return
            x1, y1, x2, y2 = clipped
        layer.append({"kind": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2})

    def add_arc(
        layer: list[dict[str, Any]],
        cx: float,
        cy: float,
        r: float,
        a1: float,
        a2: float,
    ) -> None:
        a1_n, a2_n = normalize_short_span(a1, a2)
        layer.append(
            {
                "kind": "arc",
                "d": arc_path(cx, cy, r, a1_n, a2_n),
                "cx": cx,
                "cy": cy,
                "r": r,
                "a1": a1_n,
                "a2": a2_n,
            }
        )

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    add_circle(scaffold, MED_CX, MED_CY, MED_R)
    add_line(scaffold, 0.0, -110.0, 0.0, 95.0)
    add_line(scaffold, -100.0, -27.0, 100.0, -27.0)
    add_line(scaffold, -100.0, 0.0, 100.0, 0.0)
    add_circle(scaffold, 0.0, -27.0, radius_head)
    add_circle(scaffold, 0.0, -27.0, radius_head * phi)
    add_circle(scaffold, 0.0, -27.0, radius_head * 2.0)
    add_circle(scaffold, -13.0, -27.0, radius_head / 2.0)
    add_circle(scaffold, 13.0, -27.0, radius_head / 2.0)
    add_circle(scaffold, 0.0, 0.0, 37.0)

    # -------------------------------------------------------------------------
    # Layer 4 (Gold Signature): Elements Book I, Prop. 1
    # Vesica Piscis + Equilateral Triangle <A B C>
    # -------------------------------------------------------------------------
    prop1_r = 18.0
    ax, ay = -67.0, -8.0
    bx, by = ax + prop1_r, ay
    cx_tri = 0.5 * (ax + bx)
    cy_top = ay - 0.5 * prop1_r * sqrt3
    cy_bot = ay + 0.5 * prop1_r * sqrt3

    add_circle(golden, ax, ay, prop1_r)
    add_circle(golden, bx, by, prop1_r)
    add_line(golden, ax, ay, bx, by)
    add_line(golden, ax, ay, cx_tri, cy_top)
    add_line(golden, bx, by, cx_tri, cy_top)
    add_line(golden, cx_tri, cy_top, cx_tri, cy_bot)
    add_circle(golden, ax, ay, 1.05, filled=True)
    add_circle(golden, bx, by, 1.05, filled=True)
    add_circle(golden, cx_tri, cy_top, 1.05, filled=True)

    # -------------------------------------------------------------------------
    # Layer 2 & 3: Cranium, Hairline, Forehead & Ears (3/4 left pose)
    # -------------------------------------------------------------------------
    # Outer crown & hair dome (continuous at apex x=-1.5, y=-71.0)
    add_arc(primary, -1.5, -44.0, 27.0, -155.0, -90.0)
    add_arc(primary, -1.5, -44.0, 27.0, -90.0, -24.0)

    # High scholar's hairline (continuous at x=-1.5, y=-64.0)
    add_arc(primary, -1.5, -42.0, 22.0, -145.0, -90.0)
    add_arc(primary, -1.5, -42.0, 22.0, -90.0, -35.0)

    # Temple hair / side contours descending to ear & cheekbone
    add_arc(primary, -8.5, -39.0, 20.8, -135.0, -195.0)
    add_arc(primary, 5.5, -39.0, 20.0, -45.0, 16.0)
    add_arc(detail, -10.0, -40.0, 23.0, -142.0, -188.0)
    add_arc(detail, 7.0, -40.0, 22.0, -38.0, 12.0)

    # Forehead thought lines & glabella furrows
    add_arc(detail, -1.0, -20.0, 29.0, -112.0, -72.0)
    add_arc(detail, -1.0, -16.0, 26.5, -114.0, -70.0)
    add_line(primary, -3.4, -36.0, -3.0, -29.2)
    add_line(detail, 1.2, -35.5, 0.8, -29.5)

    # Left ear (peeking from temple hair)
    add_arc(primary, -25.4, -21.0, 4.0, 110.0, 250.0)
    add_arc(detail, -25.6, -21.0, 2.0, 120.0, 240.0)

    # -------------------------------------------------------------------------
    # Eyes & Brows (Viewer's left eye centered at -13.8; right at +10.2)
    # -------------------------------------------------------------------------
    # Left eye & brow
    add_arc(primary, -13.5, -21.0, 14.0, -126.0, -56.0)
    add_arc(detail, -13.5, -19.8, 13.4, -122.0, -60.0)
    add_arc(detail, -13.8, -21.5, 8.6, -132.0, -48.0)
    add_arc(primary, -13.8, -20.5, 8.0, -136.0, -44.0)
    add_arc(detail, -13.8, -31.2, 7.2, 52.0, 128.0)
    add_circle(detail, -13.8, -26.0, 2.7)
    add_circle(primary, -13.8, -26.0, 1.15, filled=True)

    # Right eye & brow (reconstructed cleanly from chiaroscuro shadow)
    add_arc(primary, 10.2, -21.0, 13.0, -124.0, -54.0)
    add_arc(detail, 10.2, -19.8, 12.4, -120.0, -58.0)
    add_arc(detail, 10.2, -21.5, 8.0, -130.0, -46.0)
    add_arc(primary, 10.2, -20.5, 7.5, -134.0, -42.0)
    add_arc(detail, 10.2, -31.0, 6.8, 52.0, 128.0)
    add_circle(detail, 10.2, -26.0, 2.5)
    add_circle(primary, 10.2, -26.0, 1.1, filled=True)

    # -------------------------------------------------------------------------
    # Nose & Cheekbones
    # -------------------------------------------------------------------------
    add_line(primary, -5.0, -28.5, -4.2, -10.5)
    add_line(detail, 2.8, -27.5, 2.2, -10.5)
    add_arc(primary, -1.0, -10.5, 3.6, 25.0, 155.0)
    add_arc(primary, -5.2, -8.8, 2.2, 40.0, 200.0)
    add_arc(detail, 3.0, -8.8, 2.0, -20.0, 140.0)

    # Cheekbones (joining cleanly into beard side edges at y=-8.0)
    add_arc(primary, -6.5, -12.0, 18.2, 167.0, 212.0)
    add_arc(primary, 5.0, -12.0, 17.8, -32.0, 13.0)

    # -------------------------------------------------------------------------
    # Mustache, Mouth & Full Philosopher Beard (Euclid III.12 tangent arcs)
    # -------------------------------------------------------------------------
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-1.2, -5.2, -17.0, 1.5, 3, 26.0, 1):
        add_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-1.2, -5.2, 14.5, 1.5, 3, 26.0, -1):
        add_arc(primary, cx, cy, r, a1, a2)

    # Lower lip
    add_arc(primary, -1.0, -1.2, 4.5, 45.0, 135.0)

    # Outer beard silhouette (exact junction at (-16.5, 29.0) and (14.5, 29.0))
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-24.2, -8.0, -16.5, 29.0, 4, wave_angle_deg - 4.0, -1):
        add_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(22.2, -8.0, 14.5, 29.0, 4, wave_angle_deg - 4.0, 1):
        add_arc(primary, cx, cy, r, a1, a2)
    add_arc(primary, -1.0, 19.12, 18.38, 32.5, 147.5)

    # Interior wavy beard locks (Euclid III.12)
    for x_top, y_top, x_bot, y_bot, waves, sign in [
        (-15.5, 4.0, -12.8, 29.5, 4, 1),
        (-9.5, 5.5, -7.6, 33.5, 4, -1),
        (-1.5, 6.5, -1.0, 35.5, 5, 1),
        (5.5, 5.5, 4.4, 33.5, 4, -1),
        (12.0, 4.0, 10.0, 30.0, 4, 1),
    ]:
        for cx, cy, r, a1, a2 in tangent_wave_arcs(
            x_top, y_top, x_bot, y_bot, waves, wave_angle_deg - 2.0, sign
        ):
            add_arc(detail, cx, cy, r, a1, a2)

    # -------------------------------------------------------------------------
    # Open V-Tunic Collar, Shoulders & Draped Mantle
    # -------------------------------------------------------------------------
    # Inner open V-neck tunic lapels
    add_line(primary, -11.0, 35.5, -4.0, 63.0)
    add_line(primary, -4.0, 63.0, -0.5, 81.5)
    add_line(primary, 9.5, 35.5, 4.5, 59.0)
    add_line(primary, 4.5, 59.0, -0.5, 81.5)

    add_line(detail, -15.5, 34.5, -19.5, 54.0)
    add_line(detail, -19.5, 54.0, -14.5, 81.0)

    # Smooth rounded shoulders
    add_arc(primary, -16.0, 74.0, 41.0, -165.0, -99.0)
    add_arc(primary, 24.0, 90.0, 58.0, -94.0, -34.0)

    # Diagonal mantle folds across right chest & left sleeve
    add_line(primary, 48.0, 39.5, 10.5, 81.5)
    add_line(primary, 64.0, 46.0, 28.5, 79.5)
    add_line(detail, -35.0, 43.0, -52.0, 74.0)

    # Euclid III.12 drapery wave folds along mantle & sleeve
    for cx, cy, r, a1, a2 in tangent_wave_arcs(53.0, 43.0, 19.0, 80.5, 5, wave_angle_deg, 1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(71.0, 51.0, 43.0, 74.0, 4, wave_angle_deg, -1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-29.0, 41.0, -45.0, 75.0, 4, wave_angle_deg, -1):
        add_arc(detail, cx, cy, r, a1, a2)

    return {
        "scaffold": scaffold,
        "golden": golden,
        "primary": primary,
        "detail": detail,
    }


def build_euclid_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Build the complete SVG string for Euclid of Alexandria."""
    layers = build_euclid_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_euclid_svgs(output_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``euclid_dark.svg`` and ``euclid_light.svg`` to ``docsrc/_static/portraits``."""
    target_dir = output_dir or DEFAULT_PORTRAITS_STATIC_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "euclid_dark.svg"
    light_path = target_dir / "euclid_light.svg"
    dark_path.write_text(build_euclid_svg("dark"), encoding="utf-8")
    light_path.write_text(build_euclid_svg("light"), encoding="utf-8")
    return dark_path, light_path
