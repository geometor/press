"""Study 13: David Hilbert (after 1912 Gottingen portrait) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_hilbert_elements",
    "build_hilbert_svg",
    "write_hilbert_svgs",
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


def _add_pappus_hilbert_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    half_w: float = 10.5,
    half_h: float = 9.5,
) -> None:
    """Draw the Pappus-Hilbert incidence configuration in the open left margin.

    Two collinear triples ``(A1, A2, A3)`` and ``(B1, B2, B3)`` joined crosswise
    yield three strictly collinear intersection points along the golden incidence
    axis—foundational to Hilbert's *Grundlagen der Geometrie* (1899).
    """
    tilt = 1.6
    a_pts = (
        (cx - half_w, cy - half_h + tilt),
        (cx, cy - half_h),
        (cx + half_w, cy - half_h - tilt),
    )
    b_pts = (
        (cx - half_w, cy + half_h - tilt),
        (cx, cy + half_h),
        (cx + half_w, cy + half_h + tilt),
    )

    # Upper & lower base incidence lines
    mb.add_line("golden", a_pts[0][0] - 1.5, a_pts[0][1] + 0.23, a_pts[2][0] + 1.5, a_pts[2][1] - 0.23)
    mb.add_line("golden", b_pts[0][0] - 1.5, b_pts[0][1] - 0.23, b_pts[2][0] + 1.5, b_pts[2][1] + 0.23)

    # Six cross-joins
    joins = (
        (a_pts[0], b_pts[1]),
        (a_pts[1], b_pts[0]),
        (a_pts[0], b_pts[2]),
        (a_pts[2], b_pts[0]),
        (a_pts[1], b_pts[2]),
        (a_pts[2], b_pts[1]),
    )
    for p1, p2 in joins:
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Three strictly collinear Pappus-Hilbert intersection nodes
    p_left = _intersect_lines(a_pts[0], b_pts[1], a_pts[1], b_pts[0])
    p_mid = _intersect_lines(a_pts[0], b_pts[2], a_pts[2], b_pts[0])
    p_right = _intersect_lines(a_pts[1], b_pts[2], a_pts[2], b_pts[1])

    dx = p_right[0] - p_left[0]
    dy = p_right[1] - p_left[1]
    norm = math.hypot(dx, dy)
    if norm > 1e-6:
        ux, uy = dx / norm, dy / norm
        overhang = 4.2
        mb.add_line(
            "golden",
            p_left[0] - ux * overhang,
            p_left[1] - uy * overhang,
            p_right[0] + ux * overhang,
            p_right[1] + uy * overhang,
        )

    for pt in (*a_pts, *b_pts):
        mb.add_circle("golden", pt[0], pt[1], 0.85)
    for pt in (p_left, p_mid, p_right):
        mb.add_circle("golden", pt[0], pt[1], 1.15, filled=True)


def _add_hilbert_curve_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    side: float = 21.6,
) -> None:
    """Draw an exact Order-2 Hilbert space-filling curve inside a golden square frame."""
    half = 0.5 * side
    left = cx - half
    right = cx + half
    top = cy - half
    bot = cy + half

    # Outer square frame
    mb.add_line("golden", left, top, right, top)
    mb.add_line("golden", right, top, right, bot)
    mb.add_line("golden", right, bot, left, bot)
    mb.add_line("golden", left, bot, left, top)

    # Exact 16-cell Order-2 Hilbert curve (15 orthogonal unit segments)
    grid_order = (
        (0, 3), (1, 3), (1, 2), (0, 2),
        (0, 1), (0, 0), (1, 0), (1, 1),
        (2, 1), (2, 0), (3, 0), (3, 1),
        (3, 2), (2, 2), (2, 3), (3, 3),
    )
    step = side / 4.0
    pts = [
        (left + (col + 0.5) * step, top + (row + 0.5) * step)
        for col, row in grid_order
    ]
    for p1, p2 in zip(pts[:-1], pts[1:], strict=False):
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Mark curve entry and exit terminals
    mb.add_circle("golden", pts[0][0], pts[0][1], 0.9, filled=True)
    mb.add_circle("golden", pts[-1][0], pts[-1][1], 0.9, filled=True)


def build_hilbert_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Construct David Hilbert medallion strictly from lines, circles, and circular arcs.

    Calibrated to the iconic 1912 Gottingen portrait featuring Hilbert's sweeping
    Panama hat with dark hatband, oval pince-nez spectacles, penetrating gaze,
    trimmed mustache and pointed goatee, stiff white wing collar, silk tie, and
    formal academic jacket lapels.

    Args:
        wave_angle_deg: Half-angle (degrees) for subtle Euclid III.12 beard/goatee accents.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-11.0,
        eye_rx=12.5,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Pappus-Hilbert (Left) & Order-2 Hilbert Curve (Right)
    # -------------------------------------------------------------------------
    _add_pappus_hilbert_motif(mb, cx=-66.0, cy=-4.0, half_w=10.5, half_h=9.5)
    _add_hilbert_curve_motif(mb, cx=66.0, cy=-4.0, side=21.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Iconic 1912 Panama Hat & Dark Grosgrain Hatband
    # -------------------------------------------------------------------------
    # High rounded Panama crown (outward-flush walls so hatband meets cleanly)
    mb.add_arc_pts("primary", (-24.0, -51.5), (-25.0, -72.0), 0.7)
    mb.add_arc_pts("primary", (-25.0, -72.0), (-16.0, -83.5), 2.8)
    mb.add_arc_pts("primary", (-16.0, -83.5), (17.5, -83.5), 3.6)
    mb.add_arc_pts("primary", (17.5, -83.5), (27.0, -71.0), 2.6)
    mb.add_arc_pts("primary", (27.0, -71.0), (29.8, -54.0), 1.4)
    # Subtle Panama crown dent
    mb.add_arc_pts("detail", (-9.0, -81.5), (10.5, -81.5), -1.2)

    # Dark grosgrain hatband (crisp parallel circular arcs flush with crown walls)
    mb.add_arc_pts("primary", (-24.8, -61.5), (28.5, -62.5), 7.2)
    mb.add_arc_pts("primary", (-24.0, -51.5), (29.8, -54.0), 6.8)
    mb.add_arc_pts("detail", (-24.5, -56.5), (29.2, -58.2), 7.0)

    # Sweeping wide-brimmed Panama hat silhouette
    # Upper brim sweep left & right
    mb.add_arc_pts("primary", (-24.0, -51.5), (-46.2, -24.8), 3.4)
    mb.add_arc_pts("primary", (29.8, -54.0), (52.5, -47.2), 2.2)
    # Front visor brim sweeping dynamically across the forehead above pince-nez
    mb.add_arc_pts("primary", (-46.2, -24.8), (52.5, -47.2), 5.8)
    # Left & right brim underside curling back behind temples
    mb.add_arc_pts("primary", (-46.2, -24.8), (-42.0, -16.2), -2.0)
    mb.add_arc_pts("primary", (-42.0, -16.2), (-23.0, -14.2), -1.4)
    mb.add_arc_pts("primary", (52.5, -47.2), (46.8, -37.2), 2.2)
    mb.add_arc_pts("primary", (46.8, -37.2), (38.5, -31.5), 1.4)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Pince-Nez Spectacles, Penetrating Eyes, Nose & Sculpted Ear
    # -------------------------------------------------------------------------
    # Expressive academic brows peeking cleanly beneath hat visor
    mb.add_arc_pts("primary", (-19.0, -29.8), (-4.8, -31.6), 1.4)
    mb.add_arc_pts("primary", (4.5, -32.8), (20.2, -33.2), 1.6)

    # Oval/circular wire pince-nez spectacles (pure circular arcs, subtle -6 deg tilt!)
    # Left lens rim
    mb.add_arc_pts("primary", (-19.2, -23.6), (-3.0, -25.4), 5.2)
    mb.add_arc_pts("primary", (-19.2, -23.6), (-3.0, -25.4), -5.2)
    # Right lens rim
    mb.add_arc_pts("primary", (4.2, -26.2), (20.8, -27.8), 5.2)
    mb.add_arc_pts("primary", (4.2, -26.2), (20.8, -27.8), -5.2)
    # Iconic arched pince-nez nose-bridge wire clip
    mb.add_arc_pts("primary", (-3.0, -25.4), (4.2, -26.2), 2.8)
    # Subtle pince-nez side cord on right
    mb.add_arc_pts("detail", (20.8, -27.8), (27.5, -24.5), -1.0)

    # Penetrating eyes inside the pince-nez lenses
    # Viewer's left eye
    l_out = (-16.0, -24.5)
    l_in = (-5.8, -25.4)
    mb.add_arc_pts("primary", l_out, l_in, 1.8)
    mb.add_arc_pts("detail", (-15.8, -26.8), (-5.8, -27.5), 1.6)
    mb.add_arc_pts("detail", l_out, l_in, -1.1)
    mb.add_circle("detail", -10.8, -24.9, 1.8)
    mb.add_circle("primary", -10.8, -24.9, 0.9, filled=True)

    # Viewer's right eye
    r_in = (6.6, -26.8)
    r_out = (18.0, -27.8)
    mb.add_arc_pts("primary", r_in, r_out, 1.9)
    mb.add_arc_pts("detail", (6.5, -29.2), (18.2, -30.0), 1.7)
    mb.add_arc_pts("detail", r_in, r_out, -1.1)
    mb.add_circle("detail", 12.4, -27.2, 1.85)
    mb.add_circle("primary", 12.4, -27.2, 0.95, filled=True)

    # Straight academic nose
    mb.add_arc_pts("primary", (0.4, -30.8), (-0.8, -14.0), -0.5)
    mb.add_arc_pts("detail", (3.0, -24.5), (3.8, -16.5), 0.4)
    mb.add_arc_pts("primary", (-4.8, -14.2), (-0.5, -12.0), -0.9)
    mb.add_arc_pts("primary", (-0.5, -12.0), (4.8, -14.6), -0.9)
    mb.add_arc_pts("detail", (-5.2, -16.8), (-4.8, -14.2), -0.6)
    mb.add_arc_pts("detail", (5.2, -17.0), (4.8, -14.6), 0.6)

    # Facial cheek contours & prominent sculpted right ear
    mb.add_arc_pts("primary", (-21.8, -22.5), (-20.0, -10.0), -1.0)
    mb.add_arc_pts("primary", (-20.0, -10.0), (-15.0, 1.5), -1.2)
    mb.add_arc_pts("primary", (27.8, -32.0), (28.2, -12.0), 1.0)
    mb.add_arc_pts("primary", (28.2, -12.0), (25.2, 1.5), 1.2)
    # Cheek creases framing the nose & mustache
    mb.add_arc_pts("detail", (-14.5, -15.5), (-12.5, -5.0), -0.9)
    mb.add_arc_pts("detail", (13.5, -16.5), (15.5, -6.0), 1.0)

    # Prominent right ear beneath hat brim
    mb.add_arc_pts("primary", (28.5, -30.5), (40.2, -29.2), 2.2)
    mb.add_arc_pts("primary", (40.2, -29.2), (38.0, -15.5), 2.0)
    mb.add_arc_pts("primary", (38.0, -15.5), (31.5, -9.2), 1.6)
    mb.add_arc_pts("primary", (31.5, -9.2), (28.2, -13.5), 1.0)
    mb.add_arc_pts("detail", (30.5, -26.8), (36.8, -25.0), 1.5)
    mb.add_arc_pts("detail", (36.8, -25.0), (33.0, -14.2), 1.5)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Crisp Trimmed Mustache & Pointed Academic Goatee
    # -------------------------------------------------------------------------
    # Mustache upper contour with natural philtrum dip & neat lower trim
    mb.add_arc_pts("primary", (-12.2, -3.5), (0.0, -8.5), 1.6)
    mb.add_arc_pts("primary", (0.0, -8.5), (13.8, -5.8), 1.6)
    mb.add_arc_pts("primary", (-10.8, -0.8), (0.8, -4.6), 1.1)
    mb.add_arc_pts("primary", (0.8, -4.6), (12.8, -2.8), 1.0)
    # Subtle lower lip glimpse beneath mustache
    mb.add_arc_pts("detail", (-4.5, -2.0), (6.2, -2.8), -0.8)

    # Trimmed pointed goatee & academic beard silhouette
    mb.add_arc_pts("primary", (-15.0, 1.5), (-8.5, 11.0), -1.4)
    mb.add_arc_pts("primary", (-8.5, 11.0), (3.8, 16.5), -1.8)
    mb.add_arc_pts("primary", (3.8, 16.5), (16.8, 11.5), -1.8)
    mb.add_arc_pts("primary", (16.8, 11.5), (25.2, 1.5), -1.6)

    # Neat groomed academic goatee & mustache trim strokes (clean short arcs)
    mb.add_wave("detail", (-9.5, 2.2), (-6.2, 10.2), 2, wave_angle_deg * 0.5, 1)
    mb.add_wave("detail", (-1.8, 2.2), (0.2, 13.0), 2, wave_angle_deg * 0.5, -1)
    mb.add_wave("detail", (5.5, 1.8), (6.2, 13.5), 2, wave_angle_deg * 0.5, 1)
    mb.add_wave("detail", (13.2, 1.2), (14.0, 10.2), 2, wave_angle_deg * 0.5, -1)
    mb.add_arc_pts("detail", (20.2, -4.5), (19.8, 5.2), 0.7)
    mb.add_arc_pts("detail", (-7.8, -5.2), (8.8, -5.8), 0.9)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Stiff White Wing Collar, Patterned Silk Tie & 1912 Jacket
    # -------------------------------------------------------------------------
    # Crisp stiff white wing collar
    mb.add_arc_pts("primary", (-13.5, 11.2), (4.5, 18.2), -1.6)
    mb.add_arc_pts("primary", (4.5, 18.2), (27.8, 4.2), -2.2)
    mb.add_arc_pts("primary", (-14.2, 10.2), (-10.5, 22.0), -0.8)
    mb.add_line("primary", -10.5, 22.0, 1.5, 28.8)
    mb.add_arc_pts("primary", (28.5, 2.5), (27.5, 16.5), 0.9)
    mb.add_line("primary", 27.5, 16.5, 12.2, 28.5)

    # Knotted patterned silk cravat / necktie (tucked cleanly behind waistcoat lapel!)
    mb.add_arc_pts("primary", (-10.0, 22.0), (1.5, 29.0), -1.2)
    mb.add_arc_pts("primary", (1.5, 29.0), (20.0, 21.0), -1.4)
    # Visible tie knot & blade framed strictly inside waistcoat V-opening
    mb.add_arc_pts("primary", (-4.8, 29.0), (-6.8, 41.0), -1.1)
    mb.add_arc_pts("primary", (-6.8, 41.0), (-0.8, 50.5), -0.9)
    # Diagonal silk stripes trimmed cleanly between left tie edge and right waistcoat lapel
    mb.add_line("detail", -4.6, 32.5, 11.2, 29.5)
    mb.add_line("detail", -5.8, 37.0, 8.8, 34.2)
    mb.add_line("detail", -5.2, 41.8, 5.2, 39.8)
    mb.add_line("detail", -3.2, 46.2, 1.8, 45.2)

    # Crisp white waistcoat V-vest cleanly overlapping right edge of tie
    mb.add_arc_pts("primary", (-11.2, 24.5), (-12.5, 86.0), 2.2)
    mb.add_arc_pts("primary", (19.5, 22.0), (-3.5, 58.0), -1.4)
    mb.add_arc_pts("primary", (-3.5, 58.0), (-5.5, 86.0), 1.0)

    # Formal 1912 Gottingen tailored jacket lapels & broad shoulders clipped flush to MED_R
    # Left collar & notched lapel
    mb.add_arc_pts("primary", (-14.5, 11.5), (-26.5, 22.5), -1.4)
    mb.add_line("primary", -26.5, 22.5, -21.5, 31.8)
    mb.add_line("primary", -21.5, 31.8, -29.8, 39.2)
    mb.add_arc_pts("primary", (-29.8, 39.2), (-15.5, 86.0), -2.4)

    # Right collar & notched lapel
    mb.add_arc_pts("primary", (30.5, 6.5), (43.5, 20.5), 1.6)
    mb.add_line("primary", 43.5, 20.5, 34.5, 29.5)
    mb.add_line("primary", 34.5, 29.5, 41.2, 38.5)
    mb.add_arc_pts("primary", (41.2, 38.5), (14.0, 86.5), 2.8)

    # Broad sweeping tailored shoulders descending flush to medallion rim
    mb.add_arc_pts("primary", (-26.5, 22.5), (-80.5, 68.0), -7.4)
    mb.add_arc_pts("primary", (30.5, 6.5), (82.5, 65.0), 6.5)

    # Clean non-crossing jacket & sleeve drapery lines (detail)
    mb.add_arc_pts("detail", (-46.5, 32.0), (-57.5, 76.0), -2.4)
    mb.add_arc_pts("detail", (-34.0, 50.0), (-36.5, 83.5), -1.6)
    mb.add_arc_pts("detail", (47.5, 26.5), (61.5, 74.5), 2.6)
    mb.add_arc_pts("detail", (37.5, 48.0), (43.0, 81.5), 1.8)

    return mb.build()


def build_hilbert_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the David Hilbert medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_hilbert_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_hilbert_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``hilbert_dark.svg`` and ``hilbert_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "hilbert_dark.svg"
    light_path = target_dir / "hilbert_light.svg"
    dark_path.write_text(
        build_hilbert_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_hilbert_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
