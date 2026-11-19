"""Study 11: Jakob Steiner (after August Weger engraving, 1881) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_steiner_elements",
    "build_steiner_svg",
    "write_steiner_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_steiner_porism_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    chain_r: float = 5.2,
) -> None:
    """Draw a closed n=6 Steiner Porism chain of mutually tangent circles.

    For ``n = 6`` symmetric circles, ``sin(30 deg) = 1/2``, giving exact tangency
    radii ``R_inner = chain_r``, ``R_mid = 2 * chain_r``, and ``R_outer = 3 * chain_r``.
    """
    r_inner = chain_r
    r_mid = 2.0 * chain_r
    r_outer = 3.0 * chain_r

    mb.add_circle("golden", cx, cy, r_outer)
    mb.add_circle("golden", cx, cy, r_inner)
    mb.add_circle("golden", cx, cy, 0.95, filled=True)

    for k in range(6):
        ang = 60.0 * k - 90.0
        px, py = polar(cx, cy, r_mid, ang)
        mb.add_circle("golden", px, py, chain_r)


def _add_poncelet_steiner_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.8,
) -> None:
    """Draw the Poncelet-Steiner single-circle & center straightedge pole-polar emblem.

    Shows the single given circle with its marked center, horizontal diameter,
    external pole with exact tangent lines, parallel polar chord, and crossed
    straightedge harmonic diagonals.
    """
    # Given circle & marked center dot (the sole compass requirement of Poncelet-Steiner)
    mb.add_circle("golden", cx, cy, radius)
    mb.add_circle("golden", cx, cy, 1.2, filled=True)

    # Horizontal diameter A-B through marked center
    a_pt = (cx - radius, cy)
    b_pt = (cx + radius, cy)
    mb.add_line("golden", a_pt[0], a_pt[1], b_pt[0], b_pt[1])

    # External pole P directly above center at distance d = 1.52 * radius
    d_pole = 1.52 * radius
    pole = (cx, cy - d_pole)
    mb.add_line("golden", cx, cy + radius, pole[0], pole[1])

    # Exact tangent contact points T1, T2 on the circle (y_polar = cy - r^2 / d)
    dy_polar = (radius * radius) / d_pole
    dx_polar = math.sqrt(max(0.0, radius * radius - dy_polar * dy_polar))
    t1 = (cx - dx_polar, cy - dy_polar)
    t2 = (cx + dx_polar, cy - dy_polar)

    # Exact tangent rays from pole P to T1, T2
    mb.add_line("golden", pole[0], pole[1], t1[0], t1[1])
    mb.add_line("golden", pole[0], pole[1], t2[0], t2[1])

    # Parallel polar chord extending cleanly past tangent points
    overhang = 3.2
    mb.add_line("golden", t1[0] - overhang, t1[1], t2[0] + overhang, t2[1])

    # Crossed straightedge harmonic diagonals A-T2 and B-T1
    mb.add_line("golden", a_pt[0], a_pt[1], t2[0], t2[1])
    mb.add_line("golden", b_pt[0], b_pt[1], t1[0], t1[1])

    for pt in (pole, t1, t2):
        mb.add_circle("golden", pt[0], pt[1], 0.95)


def build_steiner_elements(wave_angle_deg: float = 34.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Jakob Steiner medallion strictly from lines, circles, and circular arcs.

    Calibrated to August Weger's 1881 *Gesammelte Werke* frontispiece engraving,
    featuring Steiner's high forehead, knitted brows, direct piercing gaze, sculpted
    curling mustache, lush square-rounded philosopher's beard, notched frock-coat
    lapels, and folded arms.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc beard & hair waves.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-12.5,
        eye_rx=6.8,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Steiner Porism (Left) & Poncelet-Steiner Circle (Right)
    # -------------------------------------------------------------------------
    _add_steiner_porism_motif(mb, cx=-62.0, cy=-26.0, chain_r=5.2)
    _add_poncelet_steiner_motif(mb, cx=63.0, cy=-23.5, radius=12.8)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: High Forehead, Knitted Brows, Piercing Eyes, Nose & Ear
    # -------------------------------------------------------------------------
    # Left facial profile contour (temple -> cheekbone -> into beard)
    mb.add_arc_pts("primary", (-17.8, -45.0), (-19.2, -32.5), -1.0)
    mb.add_arc_pts("primary", (-19.2, -32.5), (-19.8, -21.0), -1.0)
    mb.add_arc_pts("primary", (-19.8, -21.0), (-18.2, -10.0), -1.1)

    # Right temple & cheek framing the high intellectual forehead
    mb.add_arc_pts("detail", (-17.8, -45.0), (-3.0, -53.2), 2.0)
    mb.add_arc_pts("detail", (-3.0, -53.2), (13.0, -51.0), 1.8)
    mb.add_arc_pts("detail", (13.0, -51.0), (22.5, -40.5), 1.6)
    mb.add_arc_pts("primary", (22.5, -40.5), (25.5, -26.5), 1.4)
    mb.add_arc_pts("primary", (25.5, -26.5), (24.5, -12.0), 1.1)

    # Forehead & pensive knitted glabella creases (subtle natural bow)
    mb.add_arc_pts("detail", (-11.5, -44.8), (10.5, -44.0), 1.4)
    mb.add_arc_pts("detail", (-12.5, -40.6), (11.5, -39.8), 1.4)
    mb.add_arc_pts("detail", (-4.4, -37.0), (-4.6, -29.8), -0.35)
    mb.add_arc_pts("detail", (-1.8, -36.6), (-2.0, -29.6), 0.35)

    # Expressive serious eyebrows knitted subtly over nose bridge
    mb.add_arc_pts("primary", (-19.5, -29.8), (-12.5, -32.0), 1.1)
    mb.add_arc_pts("primary", (-12.5, -32.0), (-5.5, -30.4), 0.9)
    mb.add_arc_pts("detail", (-18.8, -31.2), (-6.2, -31.8), 1.2)

    mb.add_arc_pts("primary", (-1.0, -30.2), (6.5, -31.8), 1.2)
    mb.add_arc_pts("primary", (6.5, -31.8), (16.0, -29.2), 1.1)
    mb.add_arc_pts("detail", (-0.2, -31.8), (15.0, -30.8), 1.3)

    # Piercing direct eyes right along the canonical eye-line y = -27
    # Viewer's left eye
    l_out = (-17.6, -26.5)
    l_in = (-7.2, -26.2)
    mb.add_arc_pts("primary", l_out, l_in, 1.9)
    mb.add_arc_pts("detail", (-18.0, -28.8), (-7.0, -28.4), 1.9)
    mb.add_arc_pts("detail", l_out, l_in, -1.2)
    mb.add_circle("detail", -12.6, -26.4, 1.9)
    mb.add_circle("primary", -12.8, -26.4, 0.95, filled=True)
    mb.add_arc_pts("detail", (-17.4, -22.6), (-8.0, -22.5), -1.1)

    # Viewer's right eye
    r_in = (0.6, -25.8)
    r_out = (13.2, -25.8)
    mb.add_arc_pts("primary", r_in, r_out, 2.0)
    mb.add_arc_pts("detail", (0.2, -28.4), (13.8, -28.0), 2.1)
    mb.add_arc_pts("detail", r_in, r_out, -1.3)
    mb.add_circle("detail", 6.7, -25.7, 2.0)
    mb.add_circle("primary", 6.5, -25.7, 1.0, filled=True)
    mb.add_arc_pts("detail", (1.2, -21.8), (13.8, -22.2), -1.4)
    mb.add_arc_pts("detail", (13.0, -25.2), (17.8, -24.6), 0.45)

    # Strong straight-sculpted nose
    mb.add_arc_pts("primary", (-4.5, -29.8), (-10.4, -13.0), -0.6)
    mb.add_arc_pts("detail", (-1.8, -24.5), (-3.0, -15.5), -0.45)
    mb.add_arc_pts("primary", (-10.4, -13.0), (-7.0, -10.8), -0.95)
    mb.add_arc_pts("primary", (-7.0, -10.8), (-2.8, -11.4), -0.65)
    mb.add_arc_pts("primary", (-2.8, -11.4), (0.2, -13.6), -0.8)
    mb.add_arc_pts("detail", (0.2, -13.6), (-0.8, -16.6), -0.55)
    mb.add_arc_pts("detail", (-7.8, -12.4), (-3.8, -12.8), 0.45)

    # Cheek nasolabial creases flowing into mustache
    mb.add_arc_pts("detail", (-16.2, -16.0), (-14.2, -8.5), -0.8)
    mb.add_arc_pts("detail", (1.5, -15.2), (10.5, -8.5), 1.2)

    # Right ear peeking beneath curly temple hair
    mb.add_arc_pts("primary", (27.8, -21.2), (33.8, -21.2), 1.6)
    mb.add_arc_pts("primary", (33.8, -21.2), (32.8, -13.0), 1.5)
    mb.add_arc_pts("primary", (32.8, -13.0), (27.6, -8.5), 1.4)
    mb.add_arc_pts("primary", (27.6, -8.5), (25.2, -11.0), 0.9)
    mb.add_arc_pts("detail", (28.2, -18.5), (31.2, -13.5), 1.2)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Side-Swept Curly Hair & High Crown
    # -------------------------------------------------------------------------
    # Crown & combed left-to-right sweep
    mb.add_arc_pts("primary", (-18.5, -49.0), (-6.5, -60.8), 2.6)
    mb.add_arc_pts("primary", (-6.5, -60.8), (8.5, -63.5), 2.4)
    mb.add_arc_pts("primary", (8.5, -63.5), (24.5, -57.5), 2.6)
    mb.add_arc_pts("primary", (24.5, -57.5), (33.8, -45.5), 2.4)

    # Right curly locks sweeping gracefully over temple & curling behind ear
    mb.add_arc_pts("primary", (33.8, -45.5), (37.8, -34.5), 2.0)
    mb.add_arc_pts("primary", (37.8, -34.5), (40.5, -29.2), 0.9)
    mb.add_arc_pts("primary", (40.5, -29.2), (35.8, -24.0), 2.0)
    mb.add_arc_pts("primary", (35.8, -24.0), (34.0, -17.5), 1.3)

    # Left temple curly locks & lively small outward tuft
    mb.add_arc_pts("primary", (-18.5, -49.0), (-24.0, -39.0), -2.0)
    mb.add_arc_pts("primary", (-24.0, -39.0), (-25.2, -29.5), -1.8)
    mb.add_arc_pts("primary", (-25.2, -29.5), (-22.0, -20.0), -1.6)
    mb.add_arc_pts("primary", (-22.0, -20.0), (-20.2, -12.0), -1.2)
    mb.add_arc_pts("detail", (-24.5, -34.0), (-29.0, -35.5), -1.2)

    # Interior combed crown & curly temple waves (Euclid III.12)
    mb.add_wave("detail", (-11.5, -56.2), (24.5, -50.8), 4, wave_angle_deg * 0.72, 1)
    mb.add_wave("detail", (-5.5, -59.8), (20.5, -56.5), 3, wave_angle_deg * 0.65, -1)
    mb.add_wave("detail", (24.5, -46.5), (36.5, -30.5), 3, wave_angle_deg * 0.85, 1)
    mb.add_wave("detail", (27.5, -41.0), (34.8, -25.0), 3, wave_angle_deg * 0.8, -1)
    mb.add_wave("detail", (-22.0, -39.5), (-20.5, -18.0), 3, wave_angle_deg * 0.8, 1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Sculpted Curled Mustache & Lush Square-Rounded Beard
    # -------------------------------------------------------------------------
    # Calm mouth peeking beneath the sculpted mustache
    mb.add_arc_pts("primary", (-10.2, -4.5), (-4.5, -4.0), 0.4)
    mb.add_arc_pts("primary", (-4.5, -4.0), (1.2, -4.6), -0.4)
    mb.add_arc_pts("detail", (-8.8, -2.0), (-2.2, -2.0), -0.65)

    # Sweeping mustache with iconic outward curled scroll tips braided into beard
    # Left wing
    mb.add_arc_pts("primary", (-5.5, -9.8), (-14.5, -6.2), -1.4)
    mb.add_arc_pts("primary", (-14.5, -6.2), (-18.5, -0.5), -1.8)
    mb.add_arc_pts("primary", (-18.5, -0.5), (-14.2, 2.2), -1.4)
    mb.add_arc_pts("detail", (-6.0, -7.8), (-15.0, -1.6), -1.2)
    mb.add_arc_pts("detail", (-14.2, 2.2), (-11.8, -0.2), -0.8)

    # Right wing
    mb.add_arc_pts("primary", (-5.5, -9.8), (5.0, -6.2), 1.5)
    mb.add_arc_pts("primary", (5.0, -6.2), (12.8, 0.8), 2.0)
    mb.add_arc_pts("primary", (12.8, 0.8), (8.2, 3.6), 1.5)
    mb.add_arc_pts("detail", (-4.5, -7.6), (8.5, -0.4), 1.4)
    mb.add_arc_pts("detail", (8.2, 3.6), (5.5, 1.0), 0.9)

    # Lush full square-rounded philosopher's beard silhouette
    mb.add_arc_pts("primary", (-20.2, -12.0), (-25.2, 2.0), -2.2)
    mb.add_arc_pts("primary", (-25.2, 2.0), (-26.0, 17.0), -2.2)
    mb.add_arc_pts("primary", (-26.0, 17.0), (-20.5, 28.8), -2.4)
    # Full rounded-square base of beard
    mb.add_arc_pts("primary", (-20.5, 28.8), (-2.0, 31.8), -2.2)
    mb.add_arc_pts("primary", (-2.0, 31.8), (16.5, 28.5), -2.2)
    # Right beard contour rising back to sideburn/ear
    mb.add_arc_pts("primary", (16.5, 28.5), (23.8, 16.5), -2.2)
    mb.add_arc_pts("primary", (23.8, 16.5), (26.2, 1.0), -2.0)
    mb.add_arc_pts("primary", (26.2, 1.0), (25.2, -11.0), -1.6)

    # Rich cascading Euclid III.12 beard waves (detail, strictly flowing downward)
    mb.add_wave("detail", (-20.0, 0.0), (-18.5, 26.5), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (-12.5, 3.0), (-11.0, 28.5), 4, wave_angle_deg, -1)
    mb.add_wave("detail", (-4.8, 1.0), (-4.0, 29.5), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (3.2, 3.5), (3.8, 29.0), 4, wave_angle_deg, -1)
    mb.add_wave("detail", (11.2, 3.5), (11.5, 27.5), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (19.5, -2.5), (18.0, 23.0), 4, wave_angle_deg * 0.9, -1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: 19th-Century Notched Frock-Coat Lapels, Waistcoat & Folded Arms
    # -------------------------------------------------------------------------
    # Right coat collar rising behind beard & sweeping into broad notched lapel
    mb.add_arc_pts("primary", (26.5, -5.5), (32.5, -3.5), 1.0)
    mb.add_arc_pts("primary", (32.5, -3.5), (46.2, 23.5), 2.2)
    mb.add_line("primary", 46.2, 23.5, 44.2, 32.5)
    mb.add_line("primary", 44.2, 32.5, 26.5, 31.2)
    # Broad right frock-coat lapel descending to folded arms
    mb.add_line("primary", 30.8, 32.0, 35.5, 47.0)
    mb.add_arc_pts("primary", (35.5, 47.0), (14.5, 62.5), 1.8)
    mb.add_arc_pts("primary", (26.5, 31.2), (10.5, 61.5), -1.6)
    mb.add_arc_pts("detail", (30.5, 4.0), (39.5, 27.5), 1.6)

    # Left coat collar & notched lapel
    mb.add_arc_pts("primary", (-25.0, 14.5), (-43.5, 25.0), -1.8)
    mb.add_line("primary", -43.5, 25.0, -41.5, 32.5)
    mb.add_line("primary", -41.5, 32.5, -34.5, 32.2)
    mb.add_line("primary", -39.5, 32.5, -49.0, 44.0)
    mb.add_arc_pts("primary", (-49.0, 44.0), (-36.5, 60.5), -1.4)
    mb.add_arc_pts("primary", (-34.5, 32.2), (-29.0, 58.5), 1.2)

    # Inner waistcoat (vest) lapels peeking between beard & folded arms
    mb.add_arc_pts("primary", (-22.0, 31.5), (-25.5, 58.5), -1.0)
    mb.add_arc_pts("primary", (13.5, 31.2), (-10.5, 59.0), 1.5)
    mb.add_arc_pts("detail", (-14.0, 33.5), (-18.0, 57.5), -0.8)
    mb.add_arc_pts("detail", (4.0, 33.5), (-13.5, 55.5), 1.0)

    # Tailored outer coat shoulders & sleeves hugging engraving slope cleanly to MED_R
    mb.add_arc_pts("primary", (-43.5, 25.0), (-70.0, 78.0), -4.5)
    mb.add_arc_pts("primary", (32.5, -3.5), (47.5, 11.5), 1.4)
    mb.add_arc_pts("primary", (47.5, 11.5), (65.5, 27.5), 2.6)
    mb.add_arc_pts("primary", (65.5, 27.5), (72.5, 56.5), 3.0)
    mb.add_arc_pts("primary", (72.5, 56.5), (65.0, 75.5), 1.8)

    # Iconic folded arms resting calmly across lower chest (smooth continuous arcs to MED_R)
    # Upper folded forearm (right arm crossing smoothly left-to-right)
    mb.add_arc_pts("primary", (-56.5, 70.5), (-16.0, 58.8), 3.4)
    mb.add_arc_pts("primary", (-16.0, 58.8), (49.5, 75.0), 4.2)
    # Lower tucked forearm edge (single graceful continuous arc along bottom)
    mb.add_arc_pts("primary", (-44.0, 79.0), (34.0, 82.0), 2.8)

    # Clean non-crossing coat & sleeve drapery folds (detail)
    mb.add_arc_pts("detail", (49.5, 22.0), (57.0, 62.5), 2.8)
    mb.add_arc_pts("detail", (59.5, 32.0), (63.5, 65.5), 2.2)
    mb.add_arc_pts("detail", (-50.0, 48.0), (-59.0, 70.5), -1.8)
    mb.add_arc_pts("detail", (-32.0, 69.5), (14.0, 72.5), 2.2)
    mb.add_arc_pts("detail", (30.5, 68.0), (58.0, 62.5), -2.0)

    return mb.build()


def build_steiner_svg(theme: str = "dark", wave_angle_deg: float = 34.0) -> str:
    """Render the Jakob Steiner medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_steiner_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_steiner_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 34.0,
) -> tuple[Path, Path]:
    """Write ``steiner_dark.svg`` and ``steiner_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "steiner_dark.svg"
    light_path = target_dir / "steiner_light.svg"
    dark_path.write_text(
        build_steiner_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_steiner_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
