"""Study 10: Blaise Pascal (after Francois II Quesnel, 1691) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_pascal_elements",
    "build_pascal_svg",
    "write_pascal_svgs",
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


def _add_hexagrammum_mysticum(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 14.5,
) -> None:
    """Draw Pascal's *Hexagrammum Mysticum* in the open right medallion margin.

    Six vertices on a circle define an inscribed hexagon whose three pairs of
    opposite sides meet at three strictly collinear points along the golden
    Pascal Line.
    """
    mb.add_circle("golden", cx, cy, radius)

    # Six vertices on the circle (3 upper, 3 lower) yielding 3 crisp interior intersections
    u1 = polar(cx, cy, radius, -148.0)
    u2 = polar(cx, cy, radius, -94.0)
    u3 = polar(cx, cy, radius, -32.0)
    l1 = polar(cx, cy, radius, 142.0)
    l2 = polar(cx, cy, radius, 84.0)
    l3 = polar(cx, cy, radius, 28.0)

    # Inscribed hexagon cycle: U1 -> L2 -> U3 -> L1 -> U2 -> L3 -> U1
    verts = (u1, l2, u3, l1, u2, l3)
    for k in range(6):
        a = verts[k]
        b = verts[(k + 1) % 6]
        mb.add_line("golden", a[0], a[1], b[0], b[1])
        mb.add_circle("golden", a[0], a[1], 0.85)

    # Three opposite-side intersections (guaranteed collinear by Pascal's Theorem)
    p_left = _intersect_lines(u1, l2, l1, u2)
    p_mid = _intersect_lines(u3, l1, l3, u1)
    p_right = _intersect_lines(l2, u3, u2, l3)

    # Extend the golden Pascal Line symmetrically past both sides of the circle
    dx = p_right[0] - p_left[0]
    dy = p_right[1] - p_left[1]
    norm = math.hypot(dx, dy)
    if norm > 1e-6:
        ux, uy = dx / norm, dy / norm
        # Project circle center onto the Pascal Line for balanced overhang on both sides
        t_center = (cx - p_left[0]) * ux + (cy - p_left[1]) * uy
        proj_x = p_left[0] + t_center * ux
        proj_y = p_left[1] + t_center * uy
        half_len = radius + 3.4
        mb.add_line(
            "golden",
            proj_x - ux * half_len,
            proj_y - uy * half_len,
            proj_x + ux * half_len,
            proj_y + uy * half_len,
        )

    for pt in (p_left, p_mid, p_right):
        mb.add_circle("golden", pt[0], pt[1], 1.15, filled=True)


def _add_pascals_triangle_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    pitch: float = 8.4,
    node_r: float = 1.6,
) -> None:
    """Draw a 4-row binomial lattice (Pascal's Triangle: 1 / 1 1 / 1 2 1 / 1 3 3 1)."""
    row_h = pitch * math.sqrt(3.0) / 2.0
    rows: list[list[tuple[float, float]]] = []
    for r in range(4):
        ry = cy + (r - 1.5) * row_h
        row_pts = [(cx + (k - 0.5 * r) * pitch, ry) for k in range(r + 1)]
        rows.append(row_pts)

    # Connect each parent to its two binomial children below (trimmed at node perimeters)
    for r in range(3):
        for k, p1 in enumerate(rows[r]):
            for p2 in (rows[r + 1][k], rows[r + 1][k + 1]):
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                dist = math.hypot(dx, dy)
                if dist > 2.0 * node_r:
                    ux, uy = dx / dist, dy / dist
                    mb.add_line(
                        "golden",
                        p1[0] + ux * node_r,
                        p1[1] + uy * node_r,
                        p2[0] - ux * node_r,
                        p2[1] - uy * node_r,
                    )

    # Nodes (interior binomial sums highlighted with subtle center dot)
    for r, row_pts in enumerate(rows):
        for k, (nx, ny) in enumerate(row_pts):
            mb.add_circle("golden", nx, ny, node_r)
            if 0 < k < r:
                mb.add_circle("golden", nx, ny, 0.55, filled=True)


def build_pascal_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Blaise Pascal medallion strictly from lines, circles, and circular arcs.

    Calibrated to the Palace of Versailles portrait after Francois II Quesnel (1691),
    capturing his refined Baroque three-quarter left gaze, aquiline French nose,
    flowing shoulder-length wavy hair, pointed white *rabat* collar, and draped cloak.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc Baroque hair waves.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-15.5,
        eye_rx=2.2,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Hexagrammum Mysticum (Right) & Pascal's Triangle (Left)
    # -------------------------------------------------------------------------
    _add_pascals_triangle_motif(mb, cx=-62.0, cy=-26.0, pitch=8.4, node_r=1.6)
    _add_hexagrammum_mysticum(mb, cx=63.0, cy=-26.0, radius=14.5)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Refined Baroque Three-Quarter Left Face
    # -------------------------------------------------------------------------
    # Left facial profile silhouette (high forehead -> temple -> soft cheek -> refined chin)
    mb.add_arc_pts("primary", (-13.5, -51.5), (-19.8, -40.0), -1.6)
    mb.add_arc_pts("primary", (-19.8, -40.0), (-21.0, -28.0), -0.8)
    mb.add_arc_pts("primary", (-21.0, -28.0), (-20.2, -15.0), -1.1)
    mb.add_arc_pts("primary", (-20.2, -15.0), (-16.8, -2.5), -1.4)
    mb.add_arc_pts("primary", (-16.8, -2.5), (-7.0, 7.5), -2.2)

    # Graceful chin & right jawline sweeping back into Baroque hair
    mb.add_arc_pts("primary", (-7.0, 7.5), (5.5, 6.2), -1.6)
    mb.add_arc_pts("primary", (5.5, 6.2), (17.5, -1.5), -1.8)
    mb.add_arc_pts("primary", (17.5, -1.5), (23.2, -16.5), -1.6)

    # Soft natural Baroque hairline across the high noble forehead (detail on crown, primary framing cheek)
    mb.add_arc_pts("detail", (-13.5, -51.5), (-1.5, -55.8), 1.8)
    mb.add_arc_pts("detail", (-1.5, -55.8), (11.5, -51.8), 1.6)
    mb.add_arc_pts("detail", (11.5, -51.8), (18.8, -42.5), 1.4)
    mb.add_arc_pts("primary", (18.8, -42.5), (22.5, -28.0), 1.4)
    mb.add_arc_pts("primary", (22.5, -28.0), (23.2, -16.5), 1.0)

    # High, clean arched Baroque eyebrows
    # Viewer's left eyebrow (foreshortened)
    mb.add_arc_pts("primary", (-20.0, -33.2), (-15.2, -35.6), 1.1)
    mb.add_arc_pts("primary", (-15.2, -35.6), (-10.0, -32.2), 1.0)
    # Viewer's right eyebrow (lifted, serene arc)
    mb.add_arc_pts("primary", (-4.2, -31.8), (3.0, -34.0), 1.5)
    mb.add_arc_pts("primary", (3.0, -34.0), (12.2, -30.2), 1.3)
    mb.add_arc_pts("detail", (-3.2, -33.2), (11.2, -31.5), 1.6)

    # Large, contemplative luminous eyes gazing directly at the viewer
    # Viewer's left eye (foreshortened further eye)
    l_out = (-19.4, -27.8)
    l_in = (-11.2, -27.2)
    mb.add_arc_pts("primary", l_out, l_in, 2.0)
    mb.add_arc_pts("detail", (-19.4, -30.4), (-11.0, -29.8), 2.0)
    mb.add_arc_pts("detail", l_out, l_in, -1.1)
    mb.add_circle("detail", -15.4, -27.8, 1.8)
    mb.add_circle("primary", -15.6, -27.8, 0.95, filled=True)
    mb.add_arc_pts("detail", (-18.8, -25.0), (-12.0, -24.6), -0.8)

    # Viewer's right eye (nearer, large luminous almond Baroque eye)
    r_in = (-3.2, -26.2)
    r_out = (8.5, -25.6)
    mb.add_arc_pts("primary", r_in, r_out, 2.4)
    mb.add_arc_pts("detail", (-4.0, -29.2), (9.2, -28.2), 2.4)
    mb.add_arc_pts("detail", r_in, r_out, -1.2)
    mb.add_circle("detail", 2.2, -26.3, 2.1)
    mb.add_circle("primary", 1.9, -26.3, 1.05, filled=True)
    mb.add_arc_pts("detail", (-2.8, -22.6), (8.0, -22.4), -1.1)

    # Prominent, refined aquiline French nose
    mb.add_arc_pts("primary", (-5.8, -31.5), (-10.2, -22.5), 0.5)
    mb.add_arc_pts("primary", (-10.2, -22.5), (-14.6, -14.2), -0.65)
    mb.add_arc_pts("detail", (-4.2, -25.5), (-7.2, -16.8), -0.45)
    # Sculpted nose tip & delicate alar wing
    mb.add_arc_pts("primary", (-14.6, -14.2), (-11.6, -12.0), -1.0)
    mb.add_arc_pts("primary", (-11.6, -12.0), (-7.4, -12.5), -0.65)
    mb.add_arc_pts("primary", (-7.4, -12.5), (-4.8, -14.6), -0.85)
    mb.add_arc_pts("detail", (-4.8, -14.6), (-5.8, -17.2), -0.6)
    mb.add_arc_pts("detail", (-10.8, -13.6), (-7.4, -14.0), 0.5)

    # Delicate sculpted Baroque lips & serene chin
    mb.add_arc_pts("detail", (-9.4, -11.5), (-9.8, -7.2), 0.3)
    # Upper lip Cupid's bow (detail)
    mb.add_arc_pts("detail", (-13.4, -5.2), (-9.2, -6.2), 0.65)
    mb.add_arc_pts("detail", (-9.2, -6.2), (0.2, -4.4), 0.75)
    # Primary calm mouth parting line
    mb.add_arc_pts("primary", (-13.6, -4.6), (-7.8, -4.2), 0.45)
    mb.add_arc_pts("primary", (-7.8, -4.2), (0.6, -4.2), -0.45)
    # Soft lower lip & chin hollow (detail)
    mb.add_arc_pts("detail", (-12.0, -2.5), (-6.8, -1.6), -0.85)
    mb.add_arc_pts("detail", (-6.8, -1.6), (-1.8, -2.6), -0.55)
    mb.add_arc_pts("detail", (-10.2, 2.0), (-4.8, 2.2), -0.7)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Soft Shoulder-Length Baroque Wavy Hair
    # -------------------------------------------------------------------------
    # Outer hair mass silhouette
    # Left falling locks curling gently behind collar edge
    mb.add_arc_pts("primary", (-15.5, -57.5), (-25.8, -44.0), -2.4)
    mb.add_arc_pts("primary", (-25.8, -44.0), (-27.8, -26.0), -2.2)
    mb.add_arc_pts("primary", (-27.8, -26.0), (-26.8, -6.0), -2.0)
    mb.add_arc_pts("primary", (-26.8, -6.0), (-21.8, 12.0), -1.6)
    mb.add_arc_pts("primary", (-21.8, 12.0), (-16.2, 13.8), -0.9)

    # Crown & full right flowing Baroque mane
    mb.add_arc_pts("primary", (-15.5, -57.5), (3.5, -63.2), 2.8)
    mb.add_arc_pts("primary", (3.5, -63.2), (23.0, -57.5), 2.8)
    mb.add_arc_pts("primary", (23.0, -57.5), (35.5, -44.0), 2.6)
    mb.add_arc_pts("primary", (35.5, -44.0), (41.2, -25.0), 2.6)
    mb.add_arc_pts("primary", (41.2, -25.0), (40.2, -6.0), 2.4)
    mb.add_arc_pts("primary", (40.2, -6.0), (34.5, 11.5), 2.0)

    # Flowing Euclid III.12 Baroque hair waves (detail)
    mb.add_wave("detail", (-13.0, -57.0), (20.5, -55.5), 4, wave_angle_deg * 0.8, 1)
    mb.add_wave("detail", (-23.8, -39.0), (-22.0, 5.5), 4, wave_angle_deg * 0.8, -1)
    mb.add_wave("detail", (24.5, -47.0), (31.5, 4.5), 5, wave_angle_deg, 1)
    mb.add_wave("detail", (30.5, -42.5), (36.8, 3.0), 5, wave_angle_deg, -1)
    mb.add_wave("detail", (22.0, -28.0), (26.5, 5.0), 4, wave_angle_deg * 0.85, 1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Iconic 17th-Century White Rabat Collar & Draped Cloak
    # -------------------------------------------------------------------------
    # Neck edges descending into crisp collar
    mb.add_arc_pts("primary", (-14.5, 4.5), (-15.8, 14.5), 0.7)
    mb.add_arc_pts("primary", (20.0, -3.5), (27.5, 3.5), -0.9)

    # Collar neckband wrapping cleanly around throat
    mb.add_arc_pts("primary", (-15.8, 14.5), (2.0, 14.5), -1.6)
    mb.add_arc_pts("primary", (2.0, 14.5), (27.5, 3.5), -2.2)

    # Iconic starched pointed white rabat collar wings (crisp straight-edged linen!)
    # Left wing
    mb.add_arc_pts("primary", (-15.8, 14.5), (-26.5, 25.5), 1.0)
    mb.add_arc_pts("primary", (-26.5, 25.5), (-10.2, 29.8), -0.6)
    mb.add_arc_pts("primary", (-10.2, 29.8), (-1.2, 45.8), 0.5)
    # Center front parting seam of rabat
    mb.add_line("primary", 1.8, 14.8, -1.2, 45.8)
    # Right wing (crisp taut diagonal edge to center point)
    mb.add_arc_pts("primary", (27.5, 3.5), (34.2, 11.2), 1.1)
    mb.add_arc_pts("primary", (34.2, 11.2), (-1.2, 45.8), -0.8)

    # Crisp linen pleats inside the white rabat collar
    mb.add_arc_pts("detail", (-9.0, 16.0), (-14.8, 26.5), 0.8)
    mb.add_arc_pts("detail", (10.5, 12.2), (2.5, 38.0), 0.9)
    mb.add_arc_pts("detail", (20.5, 8.2), (8.5, 33.5), 0.9)

    # Sweeping Baroque scholar's cloak & diagonal mantle sash (grand smooth arcs to MED_R)
    # Left shoulder sweeping cleanly to medallion rim
    mb.add_arc_pts("primary", (-26.5, 25.5), (-65.0, 65.0), -4.2)

    # Right shoulder sweeping cleanly out and down to medallion rim
    mb.add_arc_pts("primary", (34.2, 11.2), (80.5, 62.0), 5.6)

    # Iconic diagonal Baroque mantle lapel sweeping smoothly across lower chest
    mb.add_arc_pts("primary", (34.2, 11.2), (-1.2, 46.8), -1.8)
    mb.add_arc_pts("primary", (-1.2, 46.8), (-19.5, 59.5), -1.4)
    mb.add_arc_pts("primary", (-19.5, 59.5), (-63.0, 61.5), -2.4)

    # Second deep cloak fold framing the right lapel smoothly to bottom rim
    mb.add_arc_pts("primary", (40.5, 16.5), (-14.5, 86.5), -4.5)

    # Parallel non-crossing Baroque drapery folds (detail)
    mb.add_arc_pts("detail", (48.0, 23.0), (14.5, 86.0), -3.2)
    mb.add_arc_pts("detail", (58.0, 32.0), (36.5, 82.0), -2.8)
    mb.add_arc_pts("detail", (65.5, 44.0), (55.5, 76.0), -2.0)
    mb.add_arc_pts("detail", (-16.5, 67.5), (-56.0, 68.5), -2.2)
    mb.add_arc_pts("detail", (-12.0, 76.5), (-45.5, 77.5), -1.8)
    mb.add_arc_pts("detail", (-36.5, 36.5), (-48.5, 58.0), -1.8)

    return mb.build()


def build_pascal_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Blaise Pascal medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_pascal_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_pascal_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``pascal_dark.svg`` and ``pascal_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "pascal_dark.svg"
    light_path = target_dir / "pascal_light.svg"
    dark_path.write_text(
        build_pascal_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_pascal_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
