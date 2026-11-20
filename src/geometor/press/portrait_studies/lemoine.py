"""Study 35: Émile Lemoine (after the 19th-century French portrait)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_lemoine_elements",
    "build_lemoine_svg",
    "write_lemoine_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _intersect_lines(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> tuple[float, float]:
    """Return exact intersection of lines ``p1-p2`` and ``p3-p4``."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-9:
        return (0.5 * (x1 + x3), 0.5 * (y1 + y3))
    det1 = x1 * y2 - y1 * x2
    det2 = x3 * y4 - y3 * x4
    return (
        (det1 * (x3 - x4) - (x1 - x2) * det2) / denom,
        (det1 * (y3 - y4) - (y1 - y2) * det2) / denom,
    )


def _circumcenter(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
) -> tuple[float, float]:
    """Return exact circumcenter of non-collinear triangle ``(p1, p2, p3)``."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    denom = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(denom) < 1e-9:
        return (ax, ay)
    a2 = ax * ax + ay * ay
    b2 = bx * bx + by * by
    c2 = cx * cx + cy * cy
    ux = (a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by)) / denom
    uy = (a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax)) / denom
    return (ux, uy)


def _add_lemoine_circle_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw the Lemoine / Symmedian Point ``K = X(6)`` and First Lemoine Circle.

    Constructs an acute scalene triangle ``ABC``, its exact symmedians meeting
    at ``K`` (barycentrics ``a^2 : b^2 : c^2``), the three chords through ``K``
    parallel to sides ``BC, CA, AB``, and the exact First Lemoine Circle
    centered at the midpoint of circumcenter ``O`` and ``K`` passing through all
    six side intersections.
    """
    pt_a = (cx - 12.2, cy + 8.6)
    pt_b = (cx + 12.2, cy + 8.6)
    pt_c = (cx - 3.4, cy - 12.2)

    side_a = math.hypot(pt_b[0] - pt_c[0], pt_b[1] - pt_c[1])
    side_b = math.hypot(pt_c[0] - pt_a[0], pt_c[1] - pt_a[1])
    side_c = math.hypot(pt_a[0] - pt_b[0], pt_a[1] - pt_b[1])
    sum_sq = side_a * side_a + side_b * side_b + side_c * side_c

    # Exact Lemoine / Symmedian Point K = X(6)
    pt_k = (
        (side_a * side_a * pt_a[0] + side_b * side_b * pt_b[0] + side_c * side_c * pt_c[0])
        / sum_sq,
        (side_a * side_a * pt_a[1] + side_b * side_b * pt_b[1] + side_c * side_c * pt_c[1])
        / sum_sq,
    )
    pt_o = _circumcenter(pt_a, pt_b, pt_c)

    # Exact symmedian feet on opposite sides
    sym_a = _intersect_lines(pt_a, pt_k, pt_b, pt_c)
    sym_b = _intersect_lines(pt_b, pt_k, pt_c, pt_a)
    sym_c = _intersect_lines(pt_c, pt_k, pt_a, pt_b)

    # Three exact Lemoine parallel chords through K -> 6 concyclic points
    p_ab = _intersect_lines(
        pt_k,
        (pt_k[0] + pt_b[0] - pt_c[0], pt_k[1] + pt_b[1] - pt_c[1]),
        pt_a,
        pt_b,
    )
    p_ac = _intersect_lines(
        pt_k,
        (pt_k[0] + pt_b[0] - pt_c[0], pt_k[1] + pt_b[1] - pt_c[1]),
        pt_a,
        pt_c,
    )
    p_bc = _intersect_lines(
        pt_k,
        (pt_k[0] + pt_c[0] - pt_a[0], pt_k[1] + pt_c[1] - pt_a[1]),
        pt_b,
        pt_c,
    )
    p_ba = _intersect_lines(
        pt_k,
        (pt_k[0] + pt_c[0] - pt_a[0], pt_k[1] + pt_c[1] - pt_a[1]),
        pt_b,
        pt_a,
    )
    p_ca = _intersect_lines(
        pt_k,
        (pt_k[0] + pt_a[0] - pt_b[0], pt_k[1] + pt_a[1] - pt_b[1]),
        pt_c,
        pt_a,
    )
    p_cb = _intersect_lines(
        pt_k,
        (pt_k[0] + pt_a[0] - pt_b[0], pt_k[1] + pt_a[1] - pt_b[1]),
        pt_c,
        pt_b,
    )

    # Exact First Lemoine Circle centered at midpoint(O, K)
    l1_cx = 0.5 * (pt_o[0] + pt_k[0])
    l1_cy = 0.5 * (pt_o[1] + pt_k[1])
    l1_r = math.hypot(p_ab[0] - l1_cx, p_ab[1] - l1_cy)

    # Triangle ABC, three symmedians, and three Lemoine parallel chords
    mb.add_line("golden", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_a[0], pt_a[1])
    mb.add_line("golden", pt_a[0], pt_a[1], sym_a[0], sym_a[1])
    mb.add_line("golden", pt_b[0], pt_b[1], sym_b[0], sym_b[1])
    mb.add_line("golden", pt_c[0], pt_c[1], sym_c[0], sym_c[1])
    mb.add_line("golden", p_ab[0], p_ab[1], p_ac[0], p_ac[1])
    mb.add_line("golden", p_bc[0], p_bc[1], p_ba[0], p_ba[1])
    mb.add_line("golden", p_ca[0], p_ca[1], p_cb[0], p_cb[1])

    # First Lemoine Circle & 6 concyclic nodes + Lemoine point K = X(6)
    mb.add_circle("golden", l1_cx, l1_cy, l1_r)
    for px, py in (p_ab, p_ac, p_bc, p_ba, p_ca, p_cb):
        mb.add_circle("golden", px, py, 0.56, filled=True)
    mb.add_circle("golden", pt_k[0], pt_k[1], 0.92)
    mb.add_circle("golden", pt_k[0], pt_k[1], 0.45, filled=True)


def _add_geometrographie_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Lemoine's *Géométrographie* compass-and-straightedge emblem in right margin.

    Depicts geometric compass-dividers poised over a graduated straightedge
    scale bar inscribing a golden circular arc, honoring Lemoine's elementary
    simplicity calculus (``R1, R2, C1, C2, C3``).
    """
    hinge = (cx, cy - 10.6)
    tip_l = (cx - 7.8, cy + 7.8)
    tip_r = (cx + 7.8, cy + 7.8)

    # Compass hinge crown ring, pivot pin, and upright finial handle
    mb.add_circle("golden", hinge[0], hinge[1], 2.0)
    mb.add_circle("golden", hinge[0], hinge[1], 0.68, filled=True)
    mb.add_line("golden", hinge[0], hinge[1] - 2.0, hinge[0], hinge[1] - 4.0)
    mb.add_circle("golden", hinge[0], hinge[1] - 4.4, 0.48, filled=True)

    # Left & right compass legs descending from hinge rim to needle tips
    for tip in (tip_l, tip_r):
        dx, dy = tip[0] - hinge[0], tip[1] - hinge[1]
        length = math.hypot(dx, dy)
        sx = hinge[0] + 2.0 * dx / length
        sy = hinge[1] + 2.0 * dy / length
        mb.add_line("golden", sx, sy, tip[0], tip[1])
        mb.add_circle("golden", tip[0], tip[1], 0.52, filled=True)

    # Wing-arc locking bar spanning between the two divider legs
    mb.add_arc_pts("golden", (cx - 4.8, cy - 0.8), (cx + 4.8, cy - 0.8), -1.8)

    # Inscribed golden C3 compass arc centered at left needle tip sweeping through right tip
    arc_r = tip_r[0] - tip_l[0]
    mb.add_arc("golden", tip_l[0], tip_l[1], arc_r, -62.0, 4.0)

    # Straightedge scale bar below the needle chord with 5 geometric graduation ticks
    bar_x1, bar_x2 = cx - 11.4, cx + 11.4
    bar_top, bar_bot = cy + 7.8, cy + 10.6
    mb.add_line("golden", bar_x1, bar_top, bar_x2, bar_top)
    mb.add_line("golden", bar_x1, bar_bot, bar_x2, bar_bot)
    mb.add_line("golden", bar_x1, bar_top, bar_x1, bar_bot)
    mb.add_line("golden", bar_x2, bar_top, bar_x2, bar_bot)
    for idx in range(5):
        tx = cx - 7.8 + idx * 3.9
        tick_h = 1.6 if (idx % 2 == 0) else 1.05
        mb.add_line("golden", tx, bar_top, tx, bar_top + tick_h)


def build_lemoine_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Émile Lemoine.

    Calibrated to the 19th-century French polytechnicien portrait: thick swept
    wavy silver-gray hair crowning a broad intellectual forehead, thin oval
    wire-rimmed spectacles resting cleanly across the nose with focused eyes on
    ``y = -27``, full sweeping bushy mustache and rounded scholar's beard
    (``Euclid III.12`` tangent waves), white collar & tiny shirt-front peek at
    throat, and broad French scholar's coat shoulders and lapels sweeping
    smoothly to ``MED_R = 92.0``. Margin motifs display the Lemoine Point
    ``K = X(6)`` & First Lemoine Circle (left) and *Géométrographie*
    compass-and-straightedge emblem (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-14.2,
        eye_rx=2.8,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN LEMOINE MARGIN MOTIFS (open margins, zero face crossing) ---
    _add_lemoine_circle_motif(mb, cx=-63.5, cy=-26.0)
    _add_geometrographie_motif(mb, cx=63.5, cy=-26.0)

    # --- THICK SWEPT WAVY SILVER-GRAY HAIR CROWN ---
    mb.add_arc_pts("primary", (-22.0, -37.0), (-23.2, -49.2), 1.4)
    mb.add_arc_pts("primary", (-23.2, -49.2), (-20.0, -60.5), 1.8)
    mb.add_arc_pts("primary", (-20.0, -60.5), (-9.2, -66.5), 2.2)
    mb.add_arc_pts("primary", (-9.2, -66.5), (5.8, -67.2), 2.4)
    mb.add_arc_pts("primary", (5.8, -67.2), (21.5, -60.2), 2.4)
    mb.add_arc_pts("primary", (21.5, -60.2), (31.5, -47.8), 2.3)
    mb.add_arc_pts("primary", (31.5, -47.8), (33.0, -34.8), 1.8)
    mb.add_arc_pts("primary", (33.0, -34.8), (29.5, -24.5), 1.3)
    mb.add_arc_pts("primary", (29.5, -24.5), (24.5, -16.5), 0.9)

    # Broad intellectual forehead hairline beneath swept silver hair
    mb.add_arc_pts("primary", (-22.0, -37.0), (-20.0, -46.5), 1.0)
    mb.add_arc_pts("primary", (-20.0, -46.5), (-13.2, -52.2), 1.2)
    mb.add_arc_pts("primary", (-13.2, -52.2), (2.2, -52.5), 1.1)
    mb.add_arc_pts("primary", (2.2, -52.5), (14.5, -48.2), 1.2)
    mb.add_arc_pts("primary", (14.5, -48.2), (20.2, -38.8), 1.1)
    mb.add_arc_pts("primary", (20.2, -38.8), (21.6, -27.8), 0.8)

    # Swept wavy silver hair texture strictly inside crown (zero wave crossings)
    mb.add_wave("detail", (-19.2, -53.8), (-7.5, -63.0), 3, wave_angle_deg + 2.0, 1)
    mb.add_wave("detail", (-8.5, -62.0), (15.5, -58.8), 4, wave_angle_deg + 1.0, -1)
    mb.add_wave("detail", (-12.5, -56.2), (14.5, -53.5), 4, wave_angle_deg + 1.0, 1)
    mb.add_wave("detail", (18.5, -50.8), (29.5, -35.5), 3, wave_angle_deg + 3.0, -1)
    mb.add_wave("detail", (22.8, -39.5), (28.0, -25.5), 3, wave_angle_deg + 4.0, 1)

    # --- CLEAR LEFT EAR (VIEWER'S RIGHT) & UPPER LEFT CHEEK ---
    mb.add_arc_pts("primary", (20.2, -26.5), (25.2, -23.8), 1.1)
    mb.add_arc_pts("primary", (25.2, -23.8), (24.2, -15.8), 1.1)
    mb.add_arc_pts("primary", (24.2, -15.8), (19.5, -12.5), 0.9)
    mb.add_arc_pts("detail", (21.0, -23.2), (22.2, -16.8), 0.8)

    # Left temple & upper cheek descending into bushy beard
    mb.add_arc_pts("primary", (-22.0, -37.0), (-22.6, -28.8), -0.7)
    mb.add_arc_pts("primary", (-22.6, -28.8), (-21.8, -19.2), -0.8)
    mb.add_arc_pts("primary", (-21.8, -19.2), (-22.5, -10.5), -0.7)

    # --- STRONG BROWS, FOCUSED EYES ON y = -27 & WIRE-RIMMED SPECTACLES ---
    mb.add_arc_pts("primary", (-21.0, -31.8), (-14.8, -33.2), 0.7)
    mb.add_arc_pts("primary", (-14.8, -33.2), (-8.8, -31.2), 0.55)
    mb.add_arc_pts("detail", (-20.0, -30.8), (-9.6, -30.5), 0.7)

    mb.add_arc_pts("primary", (-3.8, -31.2), (3.0, -33.2), 0.75)
    mb.add_arc_pts("primary", (3.0, -33.2), (11.5, -30.8), 0.65)
    mb.add_arc_pts("detail", (-2.8, -30.3), (10.5, -30.1), 0.75)

    # Clear focused eyes right on y = -27
    mb.add_canonical_eye(
        -14.2,
        -26.8,
        width=8.2,
        upper_sag=1.60,
        lower_sag=-0.80,
        iris_r=1.78,
        pupil_r=0.96,
        gaze_dx=-0.35,
    )
    mb.add_canonical_eye(
        2.8,
        -26.8,
        width=10.0,
        upper_sag=1.72,
        lower_sag=-0.84,
        iris_r=1.92,
        pupil_r=1.02,
        gaze_dx=-0.45,
    )

    # Delicate thin wire-rimmed oval spectacles seated cleanly below brows & upper lids
    mb.add_arc_pts("detail", (-19.8, -25.4), (-8.6, -25.4), 3.7)
    mb.add_arc_pts("detail", (-19.8, -25.4), (-8.6, -25.4), -3.7)
    mb.add_arc_pts("detail", (-3.4, -25.4), (9.2, -25.4), 3.9)
    mb.add_arc_pts("detail", (-3.4, -25.4), (9.2, -25.4), -3.9)
    mb.add_arc_pts("detail", (-8.6, -26.0), (-3.4, -26.0), 1.3)
    mb.add_arc_pts("detail", (9.2, -25.4), (21.4, -26.8), -0.5)

    # --- STRONG STRAIGHT NOSE ---
    mb.add_arc_pts("primary", (-6.8, -28.0), (-10.2, -21.2), 0.25)
    mb.add_arc_pts("primary", (-10.2, -21.2), (-13.6, -15.8), 0.25)
    mb.add_arc_pts("primary", (-13.6, -15.8), (-12.4, -13.4), -0.5)
    mb.add_arc_pts("primary", (-12.4, -13.4), (-7.8, -13.0), -0.35)
    mb.add_arc_pts("primary", (-7.8, -13.0), (-4.8, -14.2), -0.35)
    mb.add_arc_pts("primary", (-4.8, -14.2), (-4.2, -16.2), -0.5)
    mb.add_arc_pts("primary", (-4.2, -16.2), (-6.5, -16.8), -0.3)

    # --- FULL SWEEPING MUSTACHE & THICK ROUNDED SCHOLAR'S BEARD ---
    # Sweeping bushy mustache
    mb.add_arc_pts("primary", (-21.0, -6.5), (-15.2, -11.4), 0.75)
    mb.add_arc_pts("primary", (-15.2, -11.4), (-9.4, -11.6), 0.45)
    mb.add_arc_pts("primary", (-9.4, -11.6), (-2.4, -9.0), 0.65)
    mb.add_arc_pts("primary", (-2.4, -9.0), (2.2, -3.5), 0.75)
    mb.add_arc_pts("primary", (-20.0, -3.8), (-14.2, -6.8), -0.65)
    mb.add_arc_pts("primary", (-14.2, -6.8), (-8.8, -7.2), -0.45)
    mb.add_arc_pts("primary", (-8.8, -7.2), (-3.0, -5.2), -0.55)
    mb.add_arc_pts("primary", (-3.0, -5.2), (1.5, -1.8), -0.55)
    # Subtle lower lip glimpse tucked beneath mustache
    mb.add_arc_pts("detail", (-14.6, -3.2), (-9.0, -2.5), -0.4)
    mb.add_arc_pts("detail", (-9.0, -2.5), (-4.5, -3.2), -0.35)

    # Cheek-to-beard line on viewer's right
    mb.add_arc_pts("primary", (19.2, -15.0), (13.5, -11.2), 0.8)
    mb.add_arc_pts("primary", (13.5, -11.2), (5.8, -7.2), 0.85)
    mb.add_arc_pts("primary", (5.8, -7.2), (2.2, -3.5), 0.6)

    # Full rounded scholar's beard silhouette
    mb.add_arc_pts("primary", (-22.5, -10.5), (-25.8, 0.5), -1.0)
    mb.add_arc_pts("primary", (-25.8, 0.5), (-27.8, 10.8), -1.2)
    mb.add_arc_pts("primary", (-27.8, 10.8), (-21.5, 20.5), -1.6)
    mb.add_arc_pts("primary", (-21.5, 20.5), (-9.2, 24.8), -1.8)
    mb.add_arc_pts("primary", (-9.2, 24.8), (4.8, 21.2), -1.7)
    mb.add_arc_pts("primary", (4.8, 21.2), (16.5, 10.8), -1.5)
    mb.add_arc_pts("primary", (16.5, 10.8), (21.8, -2.5), -1.2)
    mb.add_arc_pts("primary", (21.8, -2.5), (21.2, -12.8), -0.9)

    # Lush scholar's beard & mustache texture via Euclid III.12 tangent waves
    mb.add_wave("detail", (-18.5, -8.5), (-4.2, -7.5), 3, wave_angle_deg + 3.0, 1)
    mb.add_wave("detail", (-22.5, -2.5), (-21.5, 16.5), 4, wave_angle_deg + 5.0, -1)
    mb.add_wave("detail", (-17.2, -1.8), (-14.5, 21.5), 4, wave_angle_deg + 5.0, 1)
    mb.add_wave("detail", (-10.8, -1.2), (-8.0, 22.8), 4, wave_angle_deg + 5.0, -1)
    mb.add_wave("detail", (-4.2, -1.5), (-1.2, 21.5), 4, wave_angle_deg + 5.0, 1)
    mb.add_wave("detail", (3.2, -3.5), (6.5, 17.5), 4, wave_angle_deg + 4.0, -1)
    mb.add_wave("detail", (10.5, -8.0), (14.2, 10.5), 3, wave_angle_deg + 4.0, 1)

    # --- WHITE COLLAR CORNER, BOW TIE & BROAD FRENCH SCHOLAR'S COAT ---
    # White collar corner & tiny signature white shirt V-peek below dark bow tie
    mb.add_arc_pts("primary", (20.2, 2.5), (14.5, 17.5), 1.1)
    mb.add_arc_pts("primary", (14.5, 17.5), (4.8, 21.2), 0.7)
    mb.add_arc_pts("primary", (-1.5, 24.0), (2.0, 29.2), -0.4)
    mb.add_arc_pts("primary", (2.0, 29.2), (6.0, 23.2), -0.4)
    mb.add_arc_pts("detail", (-6.5, 24.5), (12.0, 22.5), -1.2)

    # Broad dark French scholar's coat lapels & shoulders sweeping smoothly to MED_R
    # Viewer-right notched coat lapel
    mb.add_arc_pts("primary", (20.2, 2.5), (29.5, 10.5), -1.2)
    mb.add_arc_pts("primary", (29.5, 10.5), (34.5, 34.5), -1.4)
    mb.add_arc_pts("primary", (34.5, 34.5), (40.5, 39.5), 0.4)
    mb.add_arc_pts("primary", (40.5, 39.5), (34.5, 45.5), -0.5)
    mb.add_arc_pts("primary", (34.5, 45.5), (13.5, 86.0), 3.6)
    mb.add_arc_pts("primary", (14.5, 17.5), (4.8, 86.0), 3.8)

    # Viewer-left notched coat lapel
    mb.add_arc_pts("primary", (-25.5, 12.8), (-35.5, 19.5), 1.3)
    mb.add_arc_pts("primary", (-35.5, 19.5), (-38.5, 42.0), -1.5)
    mb.add_arc_pts("primary", (-38.5, 42.0), (-32.5, 46.8), -0.4)
    mb.add_arc_pts("primary", (-32.5, 46.8), (-16.5, 86.0), -2.8)
    mb.add_arc_pts("primary", (-18.5, 22.5), (-13.5, 86.0), -2.0)

    # Broad dark scholar's shoulders grounded cleanly to MED_R = 92.0
    mb.add_arc_pts("primary", (-35.5, 19.5), (-74.0, 58.0), -9.5)
    mb.add_arc_pts("primary", (29.5, 10.5), (74.0, 56.0), 10.5)

    # Clean French coat sleeve & waistcoat tailoring folds to MED_R
    mb.add_arc_pts("detail", (-48.0, 32.0), (-56.0, 78.0), -3.0)
    mb.add_arc_pts("detail", (-36.0, 54.0), (-38.5, 84.0), -1.4)
    mb.add_arc_pts("detail", (46.0, 28.0), (58.0, 76.0), 3.6)
    mb.add_arc_pts("detail", (32.0, 56.0), (26.0, 86.0), 1.6)
    mb.add_arc_pts("detail", (2.0, 29.2), (-2.0, 86.0), 1.0)

    return mb.build()


def build_lemoine_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Émile Lemoine medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_lemoine_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_lemoine_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``lemoine_dark.svg`` and ``lemoine_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "lemoine_dark.svg"
    light_path = target_dir / "lemoine_light.svg"
    dark_path.write_text(
        build_lemoine_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_lemoine_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
