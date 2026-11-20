"""Study 31: Karl Wilhelm Feuerbach (after the 19th-century Romantic pencil portrait)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_feuerbach_elements",
    "build_feuerbach_svg",
    "write_feuerbach_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _circumcircle(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
) -> tuple[float, float, float]:
    """Return exact circumcircle ``(cx, cy, r)`` through three non-collinear points."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-9:
        return (ax, ay, 0.0)
    a2 = ax * ax + ay * ay
    b2 = bx * bx + by * by
    c2 = cx * cx + cy * cy
    ux = (a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by)) / d
    uy = (a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax)) / d
    return (ux, uy, math.hypot(ax - ux, ay - uy))


def _project_onto_line(
    pt: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
) -> tuple[float, float]:
    """Return exact perpendicular foot from ``pt`` onto line ``p1-p2``."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    denom = dx * dx + dy * dy
    if denom < 1e-9:
        return p1
    t = ((pt[0] - p1[0]) * dx + (pt[1] - p1[1]) * dy) / denom
    return (p1[0] + t * dx, p1[1] + t * dy)


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
    px = (det1 * (x3 - x4) - (x1 - x2) * det2) / denom
    py = (det1 * (y3 - y4) - (y1 - y2) * det2) / denom
    return (px, py)


def _rotate_pt(
    pt: tuple[float, float],
    center: tuple[float, float],
    angle_deg: float,
) -> tuple[float, float]:
    """Rotate ``pt`` around ``center`` by ``angle_deg`` degrees."""
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    dx, dy = pt[0] - center[0], pt[1] - center[1]
    return (center[0] + dx * ca - dy * sa, center[1] + dx * sa + dy * ca)


def _add_feuerbach_theorem_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Feuerbach's Theorem (Nine-Point Circle tangent to Incircle & Excircle).

    Uses an exact poised scalene triangle scaled to harmonize with the right
    Nine-Point Circle motif so the Nine-Point Circle is visibly larger than the
    Incircle, internally tangent at the Feuerbach point ``X(11)``, and externally
    tangent to the compact excircle opposite side ``b``.
    """
    # Construct poised scalene triangle in local coordinates then scale & rotate
    scale = 0.82
    origin = (cx, cy)
    raw_a = (cx + scale * (-2.0), cy + scale * 9.0)
    raw_b = (cx + scale * 17.0, cy + scale * 7.5)
    raw_c = (cx + scale * (-4.5), cy + scale * (-3.5))
    pt_a = _rotate_pt(raw_a, origin, 35.0)
    pt_b = _rotate_pt(raw_b, origin, 35.0)
    pt_c = _rotate_pt(raw_c, origin, 35.0)

    # Exact side lengths a = |BC|, b = |CA|, c = |AB|
    side_a = math.hypot(pt_b[0] - pt_c[0], pt_b[1] - pt_c[1])
    side_b = math.hypot(pt_c[0] - pt_a[0], pt_c[1] - pt_a[1])
    side_c = math.hypot(pt_a[0] - pt_b[0], pt_a[1] - pt_b[1])
    perim = side_a + side_b + side_c
    semi = 0.5 * perim
    area = math.sqrt(max(0.0, semi * (semi - side_a) * (semi - side_b) * (semi - side_c)))

    # Exact Incircle (I, r)
    inradius = area / semi
    incenter = (
        (side_a * pt_a[0] + side_b * pt_b[0] + side_c * pt_c[0]) / perim,
        (side_a * pt_a[1] + side_b * pt_b[1] + side_c * pt_c[1]) / perim,
    )

    # Exact Excircle opposite shortest side b (I_b, r_b)
    denom_b = side_a - side_b + side_c
    exradius_b = area / (semi - side_b)
    excenter_b = (
        (side_a * pt_a[0] - side_b * pt_b[0] + side_c * pt_c[0]) / denom_b,
        (side_a * pt_a[1] - side_b * pt_b[1] + side_c * pt_c[1]) / denom_b,
    )

    # Exact Nine-Point Circle (N, r9) through the three side midpoints
    mid_a = (0.5 * (pt_b[0] + pt_c[0]), 0.5 * (pt_b[1] + pt_c[1]))
    mid_b = (0.5 * (pt_c[0] + pt_a[0]), 0.5 * (pt_c[1] + pt_a[1]))
    mid_c = (0.5 * (pt_a[0] + pt_b[0]), 0.5 * (pt_a[1] + pt_b[1]))
    nx, ny, r9 = _circumcircle(mid_a, mid_b, mid_c)

    # Reference triangle ABC and extended tangent rays kissing the excircle
    mb.add_line("golden", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_a[0], pt_a[1])
    foot_ab = _project_onto_line(excenter_b, pt_a, pt_b)
    foot_bc = _project_onto_line(excenter_b, pt_b, pt_c)
    mb.add_line("golden", pt_a[0], pt_a[1], foot_ab[0], foot_ab[1])
    mb.add_line("golden", pt_c[0], pt_c[1], foot_bc[0], foot_bc[1])

    # Three Feuerbach circles: Nine-Point Circle, Incircle, and Excircle
    mb.add_circle("golden", nx, ny, r9)
    mb.add_circle("golden", incenter[0], incenter[1], inradius)
    mb.add_circle("golden", excenter_b[0], excenter_b[1], exradius_b)

    # Exact Feuerbach internal tangency point X(11) along ray N -> I
    d_ni = math.hypot(incenter[0] - nx, incenter[1] - ny)
    if d_ni > 1e-6:
        fx_in = nx + r9 * (incenter[0] - nx) / d_ni
        fy_in = ny + r9 * (incenter[1] - ny) / d_ni
        mb.add_circle("golden", fx_in, fy_in, 0.95, filled=True)

    # Exact external Feuerbach tangency point along segment N -> I_b
    d_ne = math.hypot(excenter_b[0] - nx, excenter_b[1] - ny)
    if d_ne > 1e-6:
        fx_ex = nx + r9 * (excenter_b[0] - nx) / d_ne
        fy_ex = ny + r9 * (excenter_b[1] - ny) / d_ne
        mb.add_circle("golden", fx_ex, fy_ex, 0.90, filled=True)

    # Subtle open center marker for N
    mb.add_circle("golden", nx, ny, 0.62)


def _add_nine_point_circle_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw the Nine-Point Circle and all nine Euler-Feuerbach points in right margin.

    Constructs an acute scalene triangle ``ABC``, its three altitudes meeting
    at orthocenter ``H``, its exact Nine-Point Circle centered at ``N``, and
    all nine canonical nodes (3 side midpoints, 3 altitude feet, and 3 Euler
    midpoints between vertices and ``H``).
    """
    pt_a = (cx - 12.2, cy + 8.4)
    pt_b = (cx + 12.2, cy + 8.4)
    pt_c = (cx - 3.6, cy - 11.8)

    # 3 side midpoints
    mid_a = (0.5 * (pt_b[0] + pt_c[0]), 0.5 * (pt_b[1] + pt_c[1]))
    mid_b = (0.5 * (pt_c[0] + pt_a[0]), 0.5 * (pt_c[1] + pt_a[1]))
    mid_c = (0.5 * (pt_a[0] + pt_b[0]), 0.5 * (pt_a[1] + pt_b[1]))

    # 3 altitude feet & orthocenter H
    foot_a = _project_onto_line(pt_a, pt_b, pt_c)
    foot_b = _project_onto_line(pt_b, pt_c, pt_a)
    foot_c = _project_onto_line(pt_c, pt_a, pt_b)
    orth = _intersect_lines(pt_a, foot_a, pt_b, foot_b)

    # 3 Euler midpoints from vertices to orthocenter H
    eul_a = (0.5 * (pt_a[0] + orth[0]), 0.5 * (pt_a[1] + orth[1]))
    eul_b = (0.5 * (pt_b[0] + orth[0]), 0.5 * (pt_b[1] + orth[1]))
    eul_c = (0.5 * (pt_c[0] + orth[0]), 0.5 * (pt_c[1] + orth[1]))

    # Exact Nine-Point Circle (N, r9)
    nx, ny, r9 = _circumcircle(mid_a, mid_b, mid_c)

    # Triangle ABC & three altitudes meeting at orthocenter H
    mb.add_line("golden", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_a[0], pt_a[1])
    mb.add_line("golden", pt_a[0], pt_a[1], foot_a[0], foot_a[1])
    mb.add_line("golden", pt_b[0], pt_b[1], foot_b[0], foot_b[1])
    mb.add_line("golden", pt_c[0], pt_c[1], foot_c[0], foot_c[1])

    # Exact Nine-Point Circle
    mb.add_circle("golden", nx, ny, r9)

    # All nine canonical Euler-Feuerbach points on the circle
    for px, py in (mid_a, mid_b, mid_c, foot_a, foot_b, foot_c, eul_a, eul_b, eul_c):
        mb.add_circle("golden", px, py, 0.64, filled=True)

    # Open circle markers for Nine-Point Center N and orthocenter H
    mb.add_circle("golden", nx, ny, 0.78)
    mb.add_circle("golden", orth[0], orth[1], 0.58)


def build_feuerbach_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Karl Wilhelm Feuerbach.

    Calibrated to the 19th-century Romantic pencil portrait: youthful clean-
    shaven three-quarter left face with soulful direct gaze on ``y = -27``,
    side-parted wavy dark Romantic hair (``Euclid III.12`` tangent waves),
    high wrapped dark cravat with tailored bow, and dramatic high-collared
    Romantic greatcoat lapels sweeping smoothly to ``MED_R = 92.0``. Margin
    motifs display Feuerbach's Theorem (left) and the Nine-Point Circle (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-10.8,
        eye_rx=8.8,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN FEUERBACH MARGIN MOTIFS (open margins, zero face crossing) ---
    _add_feuerbach_theorem_motif(mb, cx=-60.5, cy=-27.5)
    _add_nine_point_circle_motif(mb, cx=63.8, cy=-25.0)

    # --- SWEEPING DARK ROMANTIC HAIR & CROWN ---
    # Sculpted Romantic hair silhouette matching the flatter swept crown
    mb.add_arc_pts("primary", (-21.0, -26.5), (-22.0, -39.0), 1.2)
    mb.add_arc_pts("primary", (-22.0, -39.0), (-20.0, -51.5), 1.6)
    mb.add_arc_pts("primary", (-20.0, -51.5), (-10.5, -58.8), 2.0)
    mb.add_arc_pts("primary", (-10.5, -58.8), (8.0, -60.8), 2.4)
    mb.add_arc_pts("primary", (8.0, -60.8), (22.5, -53.8), 2.4)
    mb.add_arc_pts("primary", (22.5, -53.8), (28.8, -39.5), 2.2)
    mb.add_arc_pts("primary", (28.8, -39.5), (28.0, -26.5), 1.4)
    mb.add_arc_pts("primary", (28.0, -26.5), (25.0, -19.0), 0.8)

    # Side-parted wavy forehead hairline & soft Romantic temple sideburns
    mb.add_arc_pts("primary", (-18.5, -28.0), (-17.5, -40.5), 0.9)
    mb.add_arc_pts("primary", (-17.5, -40.5), (-12.5, -48.5), 1.1)
    mb.add_arc_pts("primary", (-12.5, -48.5), (-2.5, -47.2), -1.0)
    mb.add_arc_pts("primary", (-2.5, -47.2), (9.5, -49.2), 1.3)
    mb.add_arc_pts("primary", (9.5, -49.2), (18.2, -45.0), 1.2)
    mb.add_arc_pts("primary", (18.2, -45.0), (21.5, -36.0), 1.0)
    mb.add_arc_pts("primary", (21.5, -36.0), (21.5, -25.5), 0.7)
    mb.add_arc_pts("detail", (21.5, -25.5), (19.5, -16.5), 0.7)
    mb.add_arc_pts("detail", (20.2, -22.0), (18.2, -13.5), 0.6)

    # Flowing Euclid III.12 Romantic hair waves
    mb.add_wave("detail", (-18.8, -44.0), (-10.2, -55.0), 3, wave_angle_deg + 3.0, 1)
    mb.add_wave("detail", (-9.5, -54.2), (15.5, -55.8), 4, wave_angle_deg + 1.0, -1)
    mb.add_wave("detail", (-1.5, -51.2), (22.5, -48.2), 4, wave_angle_deg + 1.0, 1)
    mb.add_wave("detail", (14.5, -50.2), (26.2, -33.0), 3, wave_angle_deg + 3.0, -1)
    mb.add_wave("detail", (22.2, -40.5), (25.5, -24.5), 3, wave_angle_deg + 5.0, 1)
    mb.add_arc_pts("detail", (-19.0, -34.0), (-20.0, -43.5), 0.8)

    # --- CLEAN-SHAVEN YOUTHFUL FACE CONTOUR (3/4 LEFT TURN) ---
    mb.add_arc_pts("primary", (-18.5, -28.0), (-19.2, -20.0), -0.8)
    mb.add_arc_pts("primary", (-19.2, -20.0), (-17.8, -10.5), -0.9)
    mb.add_arc_pts("primary", (-17.8, -10.5), (-12.8, -1.5), -1.1)
    mb.add_arc_pts("primary", (-12.8, -1.5), (-4.5, 3.8), -1.3)
    mb.add_arc_pts("primary", (-4.5, 3.8), (7.0, 1.8), -1.5)
    mb.add_arc_pts("primary", (7.0, 1.8), (17.2, -5.0), -1.4)
    mb.add_arc_pts("primary", (17.2, -5.0), (22.5, -14.2), -1.1)
    mb.add_arc_pts("primary", (22.5, -14.2), (23.0, -23.5), -0.8)

    # --- RIGHT EAR (VIEWER'S RIGHT) ---
    mb.add_arc_pts("primary", (23.0, -24.5), (26.8, -22.0), 1.1)
    mb.add_arc_pts("primary", (26.8, -22.0), (25.8, -15.5), 1.0)
    mb.add_arc_pts("primary", (25.8, -15.5), (22.5, -14.0), 0.8)
    mb.add_arc_pts("detail", (23.6, -21.5), (24.8, -16.8), 0.7)

    # --- RESOLUTE BROWS & SOULFUL CANONICAL EYES ON y = -27 ---
    mb.add_arc_pts("primary", (-17.8, -31.2), (-11.0, -32.2), 0.65)
    mb.add_arc_pts("primary", (-11.0, -32.2), (-5.5, -30.5), 0.5)
    mb.add_arc_pts("detail", (-16.8, -30.2), (-6.4, -29.8), 0.75)

    mb.add_arc_pts("primary", (2.2, -30.5), (9.5, -32.4), 0.7)
    mb.add_arc_pts("primary", (9.5, -32.4), (17.8, -31.0), 0.6)
    mb.add_arc_pts("detail", (3.2, -29.6), (16.8, -30.1), 0.8)

    # Calm, intense youthful gaze straddling y = -27 (uncluttered under-eye plane)
    mb.add_canonical_eye(
        -10.8,
        -26.9,
        width=9.4,
        upper_sag=1.95,
        lower_sag=-0.95,
        iris_r=2.05,
        pupil_r=1.10,
        gaze_dx=-0.25,
    )
    mb.add_canonical_eye(
        8.8,
        -26.6,
        width=10.8,
        upper_sag=2.05,
        lower_sag=-1.00,
        iris_r=2.15,
        pupil_r=1.15,
        gaze_dx=-0.45,
    )

    # --- STRAIGHT CLASSICAL NOSE & COMPOSED YOUTHFUL MOUTH ---
    mb.add_arc_pts("primary", (-2.0, -29.8), (-4.2, -22.5), 0.3)
    mb.add_arc_pts("primary", (-4.2, -22.5), (-6.5, -16.2), 0.3)
    mb.add_arc_pts("primary", (-6.5, -16.2), (-7.2, -13.8), -0.4)
    mb.add_arc_pts("primary", (-7.2, -13.8), (-5.2, -12.4), -0.65)
    mb.add_arc_pts("primary", (-5.2, -12.4), (-1.2, -12.6), -0.35)
    mb.add_arc_pts("primary", (-1.2, -12.6), (1.0, -13.8), -0.4)
    # Right nostril wing C-curve (viewer's right)
    mb.add_arc_pts("primary", (1.0, -13.8), (1.2, -15.6), -0.55)
    mb.add_arc_pts("primary", (1.2, -15.6), (-0.6, -16.2), -0.35)
    # Subtle far nostril hint
    mb.add_arc_pts("detail", (-7.4, -13.6), (-8.6, -14.8), -0.35)

    # Serious, composed youthful mouth (clean chin plane)
    mb.add_arc_pts("detail", (-8.5, -7.2), (-3.5, -7.6), 0.3)
    mb.add_arc_pts("detail", (-3.5, -7.6), (2.2, -7.0), 0.3)
    mb.add_arc_pts("primary", (-9.5, -6.2), (-3.5, -6.3), 0.22)
    mb.add_arc_pts("primary", (-3.5, -6.3), (3.2, -6.0), 0.22)
    mb.add_arc_pts("primary", (-6.2, -3.9), (-3.2, -3.4), -0.45)
    mb.add_arc_pts("primary", (-3.2, -3.4), (0.2, -3.9), -0.45)

    # --- HIGH WRAPPED DARK CRAVAT & DRAMATIC ROMANTIC GREATCOAT ---
    # Neck edges & high wrapped Romantic stock
    mb.add_arc_pts("primary", (-12.2, 1.5), (-10.8, 11.2), 0.7)
    mb.add_arc_pts("primary", (17.8, -5.8), (21.5, 2.2), -0.8)
    # Upper & lower cravat stock wraps across throat
    mb.add_arc_pts("primary", (-10.8, 9.8), (21.5, 2.2), -3.8)
    mb.add_arc_pts("primary", (-10.5, 16.2), (18.8, 8.2), -4.2)
    mb.add_arc_pts("detail", (-10.6, 13.0), (20.2, 5.2), -4.0)
    # Compact tailored cravat bow tucked cleanly at lower-left throat
    mb.add_arc_pts("primary", (-10.5, 16.2), (-11.2, 22.8), -0.9)
    mb.add_arc_pts("primary", (-11.2, 22.8), (-3.5, 21.8), -0.8)
    mb.add_arc_pts("primary", (-3.5, 21.8), (2.8, 16.0), -0.9)
    mb.add_arc_pts("detail", (-7.2, 16.6), (-5.8, 21.0), -0.4)

    # Dramatic high upturned Romantic greatcoat collar (viewer's right & left)
    mb.add_arc_pts("primary", (22.5, -10.5), (33.5, -9.8), 1.4)
    mb.add_arc_pts("primary", (33.5, -9.8), (37.2, 5.5), 2.1)
    mb.add_arc_pts("primary", (37.2, 5.5), (34.5, 13.0), 1.0)
    # Inner upturned collar crease rising behind neck
    mb.add_arc_pts("primary", (21.5, 2.2), (33.5, -9.8), -1.8)
    mb.add_arc_pts("detail", (23.5, 5.5), (33.5, -2.5), -1.2)

    # Sweeping right cape-lapel connected seamlessly at collar corner (34.5, 13.0)
    mb.add_arc_pts("primary", (34.5, 13.0), (-8.5, 56.5), 7.2)
    mb.add_arc_pts("primary", (-8.5, 56.5), (-36.0, 86.0), 3.4)
    mb.add_arc_pts("primary", (34.5, 13.0), (4.5, 88.0), 13.2)

    # Left upturned collar & wide sweeping Romantic lapel
    mb.add_arc_pts("primary", (-13.5, 2.5), (-23.8, 10.5), 1.6)
    mb.add_arc_pts("primary", (-23.8, 10.5), (-29.5, 31.5), -2.4)
    mb.add_arc_pts("primary", (-29.5, 31.5), (-8.5, 56.5), -3.2)
    mb.add_arc_pts("primary", (-15.0, 5.2), (-18.5, 27.5), -1.6)
    mb.add_arc_pts("primary", (-18.5, 27.5), (-8.5, 56.5), -2.2)
    mb.add_arc_pts("primary", (-8.5, 56.5), (-11.5, 88.0), 1.8)

    # Broad Romantic greatcoat / cape shoulders sweeping cleanly to MED_R
    mb.add_arc_pts("primary", (-23.8, 10.5), (-74.0, 62.0), -11.5)
    mb.add_arc_pts("primary", (34.5, 13.0), (72.0, 66.0), 10.5)

    # Clean Romantic cloak panel folds sweeping smoothly to MED_R
    mb.add_arc_pts("detail", (-42.5, 26.5), (-58.0, 78.0), -4.5)
    mb.add_arc_pts("detail", (-32.5, 42.5), (-42.0, 82.0), -2.2)
    mb.add_arc_pts("detail", (40.5, 27.5), (56.0, 78.0), 3.8)
    mb.add_arc_pts("detail", (31.5, 44.5), (40.0, 84.0), 2.4)
    mb.add_arc_pts("detail", (18.5, 64.5), (22.0, 86.0), 1.0)

    return mb.build()


def build_feuerbach_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Karl Wilhelm Feuerbach medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_feuerbach_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_feuerbach_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``feuerbach_dark.svg`` and ``feuerbach_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "feuerbach_dark.svg"
    light_path = target_dir / "feuerbach_light.svg"
    dark_path.write_text(
        build_feuerbach_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_feuerbach_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
