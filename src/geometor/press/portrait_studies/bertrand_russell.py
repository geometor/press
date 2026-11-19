"""Study 14: Bertrand Russell (after 1907 Edwardian portrait) in lines and circular arcs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_bertrand_russell_elements",
    "build_bertrand_russell_svg",
    "write_bertrand_russell_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _intersect_lines(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> tuple[float, float]:
    """Compute exact intersection of straight lines ``p1-p2`` and ``p3-p4``."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-9:
        return (0.5 * (x1 + x3), 0.5 * (y1 + y3))
    det1 = x1 * y2 - y1 * x2
    det2 = x3 * y4 - y3 * x4
    px = (det1 * (x3 - x4) - (x1 - x2) * det2) / denom
    py = (det1 * (y3 - y4) - (y1 - y2) * det2) / denom
    return (px, py)


def _add_cross_ratio_pencil_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw a Projective Cross-Ratio Pencil ``(A, B; C, D)`` in the open left margin.

    Four straight rays radiate from an apex vertex and are cut cleanly by two
    distinct transversals, marking the invariant projective cross-ratio nodes
    honoring *An Essay on the Foundations of Geometry* (1897).
    """
    apex = (cx - 1.0, cy - 14.5)
    base_y = cy + 14.5
    ray_xs = (cx - 12.5, cx - 4.5, cx + 3.5, cx + 12.5)
    bases = [(rx, base_y) for rx in ray_xs]

    # Four concurrent projective rays from apex
    for bp in bases:
        mb.add_line("golden", apex[0], apex[1], bp[0], bp[1])

    # Two distinct non-parallel transversals cutting the pencil
    t1_a, t1_b = (cx - 13.0, cy + 0.5), (cx + 12.0, cy - 3.2)
    t2_a, t2_b = (cx - 14.5, cy + 8.8), (cx + 14.0, cy + 12.2)
    mb.add_line("golden", t1_a[0], t1_a[1], t1_b[0], t1_b[1])
    mb.add_line("golden", t2_a[0], t2_a[1], t2_b[0], t2_b[1])

    # Mark exact ray-transversal cross-ratio nodes & apex
    mb.add_circle("golden", apex[0], apex[1], 1.15, filled=True)
    for bp in bases:
        p_upper = _intersect_lines(apex, bp, t1_a, t1_b)
        p_lower = _intersect_lines(apex, bp, t2_a, t2_b)
        mb.add_circle("golden", p_upper[0], p_upper[1], 0.85)
        mb.add_circle("golden", p_lower[0], p_lower[1], 0.85)


def _add_logic_triad_venn_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    circle_r: float = 8.8,
    offset_r: float = 5.4,
) -> None:
    """Draw three mutually intersecting logic / set-theory circles (Triad Venn Diagram).

    Honors *The Principles of Mathematics* (1903) and *Principia Mathematica* with
    three congruent circles centered on an equilateral triangle around a marked
    intersection node.
    """
    for k in range(3):
        ang = -90.0 + 120.0 * k
        px, py = polar(cx, cy, offset_r, ang)
        mb.add_circle("golden", px, py, circle_r)
        mb.add_circle("golden", px, py, 0.7)

    mb.add_circle("golden", cx, cy, 1.15, filled=True)


def build_bertrand_russell_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Bertrand Russell medallion strictly from lines, circles, and circular arcs.

    Calibrated to the 1907 Edwardian portrait of Bertrand Russell, featuring his
    high aristocratic forehead, neatly side-parted wavy Edwardian hair, straight
    decisive brows over intense direct eyes, slender nose, thick drooping Edwardian
    walrus mustache, stiff rounded white club collar, knotted silk tie, waistcoat,
    and tailored dark suit lapels.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 Edwardian hair & mustache waves.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-11.2,
        eye_rx=7.0,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Cross-Ratio Pencil (Left) & Logic Triad Venn (Right)
    # -------------------------------------------------------------------------
    _add_cross_ratio_pencil_motif(mb, cx=-63.0, cy=-26.0)
    _add_logic_triad_venn_motif(mb, cx=63.0, cy=-26.0, circle_r=8.8, offset_r=5.4)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: High Forehead, Edwardian Face, Intense Eyes, Nose & Mustache
    # -------------------------------------------------------------------------
    # Left facial profile silhouette (lean aristocratic temple -> cheek -> chin)
    mb.add_arc_pts("primary", (-17.8, -45.5), (-19.6, -33.5), -1.1)
    mb.add_arc_pts("primary", (-19.6, -33.5), (-18.6, -23.0), -0.7)
    mb.add_arc_pts("primary", (-18.6, -23.0), (-16.8, -11.0), -0.9)
    mb.add_arc_pts("primary", (-16.8, -11.0), (-13.5, 0.5), -1.0)
    mb.add_arc_pts("primary", (-13.5, 0.5), (-7.5, 8.2), -1.4)
    mb.add_arc_pts("primary", (-7.5, 8.2), (-1.2, 11.2), -1.1)

    # Clean-shaven sculpted chin & crisp right jawline rising to ear
    mb.add_arc_pts("primary", (-1.2, 11.2), (11.5, 6.8), -1.6)
    mb.add_arc_pts("primary", (11.5, 6.8), (21.5, -2.5), -1.5)
    mb.add_arc_pts("primary", (21.5, -2.5), (27.0, -14.5), -1.3)
    mb.add_arc_pts("primary", (27.0, -14.5), (27.5, -29.5), -0.9)

    # Soft natural hairline across the high intellectual forehead
    mb.add_arc_pts("detail", (-17.8, -45.5), (-5.0, -53.8), 1.8)
    mb.add_arc_pts("detail", (-5.0, -53.8), (11.5, -53.2), 1.4)
    mb.add_arc_pts("detail", (11.5, -53.2), (21.5, -45.5), 1.4)
    mb.add_arc_pts("primary", (21.5, -45.5), (27.5, -29.5), 1.4)

    # Straight, decisive dark Edwardian eyebrows
    mb.add_arc_pts("primary", (-18.5, -31.8), (-12.0, -33.0), 0.9)
    mb.add_arc_pts("primary", (-12.0, -33.0), (-5.2, -31.5), 0.8)
    mb.add_arc_pts("detail", (-17.8, -33.0), (-6.0, -32.8), 1.0)

    mb.add_arc_pts("primary", (0.2, -31.8), (7.5, -33.4), 1.1)
    mb.add_arc_pts("primary", (7.5, -33.4), (16.5, -31.0), 1.0)
    mb.add_arc_pts("detail", (1.2, -33.2), (15.5, -32.4), 1.2)

    # Dark intense eyes right on canonical eye-line y = -27
    # Viewer's left eye
    l_out = (-16.2, -26.5)
    l_in = (-6.8, -26.8)
    mb.add_arc_pts("primary", l_out, l_in, 1.9)
    mb.add_arc_pts("detail", (-16.4, -29.0), (-6.6, -29.2), 1.8)
    mb.add_arc_pts("detail", l_out, l_in, -1.1)
    mb.add_circle("detail", -11.2, -26.6, 1.85)
    mb.add_circle("primary", -11.2, -26.6, 0.95, filled=True)
    mb.add_arc_pts("detail", (-15.8, -23.6), (-7.4, -23.8), -0.9)

    # Viewer's right eye
    r_in = (1.5, -26.8)
    r_out = (13.2, -26.8)
    mb.add_arc_pts("primary", r_in, r_out, 2.1)
    mb.add_arc_pts("detail", (1.2, -29.4), (13.6, -29.2), 2.1)
    mb.add_arc_pts("detail", r_in, r_out, -1.2)
    mb.add_circle("detail", 7.0, -26.8, 2.0)
    mb.add_circle("primary", 7.0, -26.8, 1.0, filled=True)
    mb.add_arc_pts("detail", (2.0, -23.4), (12.8, -23.4), -1.1)

    # Slender aristocratic nose
    mb.add_arc_pts("primary", (-3.2, -31.5), (-6.4, -14.8), -0.5)
    mb.add_arc_pts("detail", (-0.6, -25.2), (0.0, -16.0), -0.35)
    mb.add_arc_pts("primary", (-6.4, -14.8), (-4.2, -12.0), -0.95)
    mb.add_arc_pts("primary", (-4.2, -12.0), (-0.4, -12.2), -0.6)
    mb.add_arc_pts("primary", (-0.4, -12.2), (2.2, -14.2), -0.8)
    mb.add_arc_pts("detail", (2.2, -14.2), (1.4, -16.8), -0.5)
    mb.add_arc_pts("detail", (-4.5, -13.4), (-1.2, -13.6), 0.45)

    # Thick drooping Edwardian walrus mustache (natural heavy brush contour)
    mb.add_arc_pts("primary", (-15.0, -1.2), (-3.2, -9.8), 1.7)
    mb.add_arc_pts("primary", (-3.2, -9.8), (13.8, -2.5), 1.9)
    # Soft drooping outer corners & natural full horizontal brush bottom
    mb.add_arc_pts("primary", (-15.0, -1.2), (-14.2, 2.2), -0.9)
    mb.add_arc_pts("primary", (-14.2, 2.2), (-2.8, -1.0), 1.4)
    mb.add_arc_pts("primary", (-2.8, -1.0), (13.2, 1.5), 1.4)
    mb.add_arc_pts("primary", (13.2, 1.5), (13.8, -2.5), -0.9)
    # Groomed Edwardian mustache bristle flow & subtle lower-lip shadow
    mb.add_wave("detail", (-3.0, -7.0), (-12.5, 0.2), 3, wave_angle_deg * 0.6, -1)
    mb.add_wave("detail", (-1.5, -7.0), (11.5, -0.5), 3, wave_angle_deg * 0.6, 1)
    mb.add_arc_pts("detail", (-6.2, 1.8), (3.5, 1.5), -0.85)
    mb.add_arc_pts("detail", (-5.5, 5.2), (1.8, 5.0), -0.65)

    # Prominent sculpted right ear
    mb.add_arc_pts("primary", (27.5, -25.8), (37.5, -25.5), 2.0)
    mb.add_arc_pts("primary", (37.5, -25.5), (36.2, -14.8), 1.8)
    mb.add_arc_pts("primary", (36.2, -14.8), (29.8, -10.0), 1.5)
    mb.add_arc_pts("primary", (29.8, -10.0), (26.5, -12.8), 1.0)
    mb.add_arc_pts("detail", (29.2, -22.8), (34.2, -20.5), 1.4)
    mb.add_arc_pts("detail", (34.2, -20.5), (30.8, -13.2), 1.3)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Neatly Side-Parted Wavy Edwardian Hair
    # -------------------------------------------------------------------------
    # Outer crown & side-swept hair contour
    mb.add_arc_pts("primary", (-18.2, -45.5), (-20.0, -54.5), 1.5)
    mb.add_arc_pts("primary", (-20.0, -54.5), (-10.0, -62.5), 2.4)
    mb.add_arc_pts("primary", (-10.0, -62.5), (6.5, -64.0), 2.2)
    mb.add_arc_pts("primary", (6.5, -64.0), (22.0, -59.0), 2.4)
    mb.add_arc_pts("primary", (22.0, -59.0), (31.8, -48.0), 2.2)
    mb.add_arc_pts("primary", (31.8, -48.0), (36.2, -37.2), 1.8)
    # Crisp Edwardian hair flick behind upper right ear
    mb.add_arc_pts("primary", (36.2, -37.2), (39.0, -31.8), 0.9)
    mb.add_arc_pts("primary", (39.0, -31.8), (34.2, -27.2), 1.6)

    # Side-part crease & neat combed Edwardian waves (Euclid III.12)
    mb.add_arc_pts("detail", (11.5, -53.2), (16.5, -61.0), -0.9)
    mb.add_wave("detail", (-14.0, -57.5), (10.5, -57.2), 3, wave_angle_deg * 0.65, 1)
    mb.add_wave("detail", (14.5, -55.8), (34.0, -35.0), 4, wave_angle_deg * 0.75, -1)
    mb.add_wave("detail", (19.0, -50.8), (31.8, -31.0), 3, wave_angle_deg * 0.7, 1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Stiff Rounded White Club Collar, Silk Tie & 1907 Suit Coat
    # -------------------------------------------------------------------------
    # Neck edges descending into tall stiff collar
    mb.add_arc_pts("primary", (-11.2, 6.5), (-10.5, 16.0), 0.6)
    mb.add_arc_pts("primary", (24.5, -3.5), (26.5, 8.0), -0.7)

    # Iconic stiff white Edwardian rounded club collar (cleanly framing tie knot!)
    # High top collar rim around neck
    mb.add_arc_pts("primary", (-10.5, 15.8), (5.5, 16.8), -1.6)
    mb.add_arc_pts("primary", (5.5, 16.8), (26.8, 7.2), -2.2)
    # Left rounded club collar flap
    mb.add_arc_pts("primary", (-10.5, 15.8), (-13.0, 31.8), -0.8)
    mb.add_arc_pts("primary", (-13.0, 31.8), (-8.8, 36.2), -1.6)
    mb.add_arc_pts("primary", (-8.8, 36.2), (-4.0, 21.8), -1.2)
    # Right rounded club collar flap (prominent rounded Edwardian curve)
    mb.add_arc_pts("primary", (26.8, 7.2), (28.5, 18.8), 1.0)
    mb.add_arc_pts("primary", (28.5, 18.8), (11.5, 36.2), 2.2)
    mb.add_arc_pts("primary", (11.5, 36.2), (4.8, 37.2), 1.4)
    mb.add_arc_pts("primary", (4.8, 37.2), (1.8, 21.8), 1.2)

    # Knotted Edwardian dark silk necktie nestled cleanly inside collar opening
    mb.add_line("primary", -3.8, 22.8, 1.6, 22.8)
    mb.add_arc_pts("primary", (-3.8, 22.8), (-4.4, 32.5), -0.5)
    mb.add_arc_pts("primary", (1.6, 22.8), (2.2, 32.5), 0.5)
    mb.add_arc_pts("primary", (-4.4, 32.5), (2.2, 32.5), -0.8)
    # Tie blade descending cleanly into waistcoat V-opening
    mb.add_arc_pts("primary", (-4.2, 32.5), (-7.2, 66.5), -1.0)
    mb.add_arc_pts("primary", (2.0, 32.5), (3.8, 59.0), 0.8)
    # Subtle tie knot & silk sheen lines (detail)
    mb.add_arc_pts("detail", (-3.4, 27.2), (1.4, 27.2), -0.5)
    mb.add_arc_pts("detail", (-1.0, 34.0), (-2.0, 62.0), -0.5)

    # Unified waistcoat V-opening rising cleanly to the club collar underside
    mb.add_line("primary", -13.0, 31.8, -15.5, 49.0)
    mb.add_arc_pts("primary", (-15.5, 49.0), (-11.0, 86.0), 1.6)
    mb.add_arc_pts("primary", (20.8, 29.8), (-4.5, 72.0), -1.6)
    mb.add_arc_pts("primary", (-4.5, 72.0), (-6.5, 86.0), 0.7)

    # Formal 1907 Edwardian suit coat lapels & broad shoulders clipped flush to MED_R
    # Left collar & notched lapel
    mb.add_arc_pts("primary", (-12.5, 19.0), (-28.5, 31.8), -1.4)
    mb.add_line("primary", -28.5, 31.8, -21.8, 40.5)
    mb.add_line("primary", -21.8, 40.5, -29.8, 47.8)
    mb.add_arc_pts("primary", (-29.8, 47.8), (-18.5, 86.5), -2.0)

    # Right collar & notched lapel
    mb.add_arc_pts("primary", (29.0, 11.5), (38.8, 25.5), 1.5)
    mb.add_line("primary", 38.8, 25.5, 29.5, 34.2)
    mb.add_line("primary", 29.5, 34.2, 36.8, 41.8)
    mb.add_arc_pts("primary", (36.8, 41.8), (6.5, 87.0), 2.8)

    # Broad Edwardian shoulders descending flush to medallion rim
    mb.add_arc_pts("primary", (-28.5, 31.8), (-76.5, 78.0), -6.5)
    mb.add_arc_pts("primary", (29.0, 11.5), (84.0, 72.0), 6.8)

    # Clean non-crossing coat & sleeve drapery lines (detail)
    mb.add_arc_pts("detail", (-44.5, 42.0), (-54.5, 79.0), -2.0)
    mb.add_arc_pts("detail", (-33.5, 58.0), (-36.0, 84.5), -1.4)
    mb.add_arc_pts("detail", (46.5, 28.0), (60.5, 75.5), 2.6)
    mb.add_arc_pts("detail", (36.5, 50.0), (42.0, 82.5), 1.8)

    return mb.build()


def build_bertrand_russell_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Bertrand Russell medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_bertrand_russell_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_bertrand_russell_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``bertrand_russell_dark.svg`` and ``bertrand_russell_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "bertrand_russell_dark.svg"
    light_path = target_dir / "bertrand_russell_light.svg"
    dark_path.write_text(
        build_bertrand_russell_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_bertrand_russell_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
