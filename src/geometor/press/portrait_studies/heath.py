"""Study 15: Sir Thomas Little Heath (after c. 1910 portrait) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_heath_elements",
    "build_heath_svg",
    "write_heath_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_elements_scroll_golden_section_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw a classical *Elements* parchment scroll framing an exact Golden Section (II.11 / VI.30).

    Two concentric cylindrical scroll end-rolls frame an unrolled parchment panel
    carrying Euclid's exact right-triangle compass construction dividing segment AB
    at ``1 : phi`` with compass swing arcs and a filled golden division node.
    """
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    half_w = 10.8
    half_h = 9.5
    roll_r = 2.4

    # Left & right cylindrical scroll end-rolls (concentric end-caps + vertical shafts)
    lx = cx - half_w - roll_r
    rx = cx + half_w + roll_r
    top_y = cy - half_h
    bot_y = cy + half_h

    for sx in (lx, rx):
        mb.add_circle("golden", sx, top_y, roll_r)
        mb.add_circle("golden", sx, top_y, roll_r * 0.42)
        mb.add_line("golden", sx - roll_r, top_y, sx - roll_r, bot_y)
        mb.add_line("golden", sx + roll_r, top_y, sx + roll_r, bot_y)
        mb.add_arc_pts("golden", (sx - roll_r, bot_y), (sx + roll_r, bot_y), -roll_r * 0.85)

    # Top and bottom unrolled parchment edges connecting the two scroll rollers
    mb.add_line("golden", lx + roll_r, top_y, rx - roll_r, top_y)
    mb.add_line("golden", lx + roll_r, bot_y, rx - roll_r, bot_y)

    # Exact Golden Section compass construction inside the parchment panel
    seg_len = 15.6
    y_seg = cy + 3.6
    ax = cx - 0.5 * seg_len
    bx = cx + 0.5 * seg_len
    leg_h = 0.5 * seg_len  # L / 2
    cx_tri, cy_tri = bx, y_seg - leg_h

    # Base segment AB, perpendicular leg BC (length L/2), and hypotenuse AC
    mb.add_line("golden", ax, y_seg, bx, y_seg)
    mb.add_line("golden", bx, y_seg, cx_tri, cy_tri)
    mb.add_line("golden", ax, y_seg, cx_tri, cy_tri)

    # Compass arc 1: centered at C with radius L/2 swinging from B onto hypotenuse AC at D
    ang_b_from_c = 90.0
    ang_a_from_c = math.degrees(math.atan2(y_seg - cy_tri, ax - cx_tri))
    mb.add_arc("golden", cx_tri, cy_tri, leg_h, ang_b_from_c, ang_a_from_c)

    # Compass arc 2: centered at A with radius AD = L / phi swinging down onto AB at G
    r_gold = seg_len / phi
    ang_c_from_a = math.degrees(math.atan2(cy_tri - y_seg, cx_tri - ax))
    mb.add_arc("golden", ax, y_seg, r_gold, ang_c_from_a, 0.0)

    # Exact Golden Section division node G (AG : GB = phi) & endpoint markers
    gx = ax + r_gold
    mb.add_circle("golden", gx, y_seg, 1.15, filled=True)
    mb.add_circle("golden", ax, y_seg, 0.7)
    mb.add_circle("golden", bx, y_seg, 0.7)


def _add_book_xiii_pentagon_decagram_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 14.0,
) -> None:
    """Draw Euclid Book XIII's inscribed regular pentagon & decagram star in a circle."""
    mb.add_circle("golden", cx, cy, radius)

    # Five upright regular pentagon vertices & five inverted pentagon vertices (decagon)
    up_pts = [polar(cx, cy, radius, -90.0 + 72.0 * k) for k in range(5)]
    dn_pts = [polar(cx, cy, radius, 90.0 + 72.0 * k) for k in range(5)]

    # Inscribed regular pentagon
    for k in range(5):
        p1 = up_pts[k]
        p2 = up_pts[(k + 1) % 5]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
        mb.add_circle("golden", p1[0], p1[1], 0.85)

    # Decagram star (interlaced upright and inverted pentagrams {5/2})
    for k in range(5):
        u1 = up_pts[k]
        u2 = up_pts[(k + 2) % 5]
        mb.add_line("golden", u1[0], u1[1], u2[0], u2[1])

        d1 = dn_pts[k]
        d2 = dn_pts[(k + 2) % 5]
        mb.add_line("golden", d1[0], d1[1], d2[0], d2[1])

    mb.add_circle("golden", cx, cy, 1.05, filled=True)


def build_heath_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Sir Thomas Little Heath medallion strictly from lines, circles, and circular arcs.

    Calibrated to the c. 1910 studio portrait of Sir Thomas Little Heath, featuring
    his sweeping parted silver-white hair with sculpted temple wave, calm three-quarter
    left scholarly gaze, straight classical nose, neatly trimmed British brush mustache,
    sculpted right ear, high white rounded Edwardian collar, silk tie, waistcoat,
    and tailored dark coat lapels.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 silver hair waves.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-13.5,
        eye_rx=4.0,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Elements Scroll & Golden Section (Left), Book XIII Star (Right)
    # -------------------------------------------------------------------------
    _add_elements_scroll_golden_section_motif(mb, cx=-63.0, cy=-26.0)
    _add_book_xiii_pentagon_decagram_motif(mb, cx=63.0, cy=-26.0, radius=14.0)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Noble Brow, Calm Three-Quarter Left Gaze, Nose & Brush Mustache
    # -------------------------------------------------------------------------
    # Left facial profile silhouette (rounded brow -> temple -> firm cheek -> chin)
    mb.add_arc_pts("primary", (-18.8, -46.5), (-19.8, -34.5), -1.1)
    mb.add_arc_pts("primary", (-19.8, -34.5), (-19.4, -24.5), -0.6)
    mb.add_arc_pts("primary", (-19.4, -24.5), (-18.6, -12.5), -0.9)
    mb.add_arc_pts("primary", (-18.6, -12.5), (-16.8, -1.0), -1.1)
    mb.add_arc_pts("primary", (-16.8, -1.0), (-12.5, 7.5), -1.5)
    mb.add_arc_pts("primary", (-12.5, 7.5), (-5.0, 11.2), -1.3)

    # Firm rounded chin & dignified right jawline rising to ear
    mb.add_arc_pts("primary", (-5.0, 11.2), (8.0, 9.0), -1.6)
    mb.add_arc_pts("primary", (8.0, 9.0), (19.8, 0.5), -1.6)
    mb.add_arc_pts("primary", (19.8, 0.5), (26.5, -12.0), -1.4)
    mb.add_arc_pts("primary", (26.5, -12.0), (27.2, -26.5), -1.0)

    # Soft natural silver-white hairline across rounded scholar's brow
    mb.add_arc_pts("detail", (-18.8, -46.5), (-5.5, -53.2), 1.8)
    mb.add_arc_pts("detail", (-5.5, -53.2), (11.5, -51.5), 1.5)
    mb.add_arc_pts("detail", (11.5, -51.5), (21.5, -42.5), 1.4)
    mb.add_arc_pts("primary", (21.5, -42.5), (27.2, -26.5), 1.4)

    # Calm scholar's eyebrows
    mb.add_arc_pts("primary", (-19.0, -30.5), (-13.5, -32.2), 1.0)
    mb.add_arc_pts("primary", (-13.5, -32.2), (-7.8, -30.5), 0.8)
    mb.add_arc_pts("detail", (-18.4, -31.8), (-8.5, -31.8), 1.0)

    mb.add_arc_pts("primary", (-2.8, -30.5), (4.5, -32.2), 1.1)
    mb.add_arc_pts("primary", (4.5, -32.2), (13.8, -29.8), 1.0)
    mb.add_arc_pts("detail", (-1.8, -32.0), (12.8, -31.2), 1.2)

    # Calm three-quarter left scholarly eyes right along y = -27
    # Viewer's left eye (further eye)
    l_out = (-17.8, -26.5)
    l_in = (-8.5, -26.5)
    mb.add_arc_pts("primary", l_out, l_in, 1.8)
    mb.add_arc_pts("detail", (-18.0, -29.0), (-8.2, -29.0), 1.8)
    mb.add_arc_pts("detail", l_out, l_in, -1.1)
    mb.add_circle("detail", -13.6, -26.5, 1.8)
    mb.add_circle("primary", -14.0, -26.5, 0.9, filled=True)
    mb.add_arc_pts("detail", (-17.4, -23.5), (-9.0, -23.6), -0.9)

    # Viewer's right eye (nearer, serene dignified gaze left-ward)
    r_in = (-1.0, -26.5)
    r_out = (10.5, -26.5)
    mb.add_arc_pts("primary", r_in, r_out, 2.0)
    mb.add_arc_pts("detail", (-1.4, -29.2), (11.2, -29.0), 2.0)
    mb.add_arc_pts("detail", r_in, r_out, -1.2)
    mb.add_circle("detail", 4.0, -26.5, 1.95)
    mb.add_circle("primary", 3.5, -26.5, 0.95, filled=True)
    mb.add_arc_pts("detail", (-0.5, -22.8), (10.5, -23.0), -1.2)

    # Classic straight British nose
    mb.add_arc_pts("primary", (-6.2, -31.0), (-12.0, -15.5), -0.5)
    mb.add_arc_pts("detail", (-3.5, -25.2), (-4.0, -16.2), -0.35)
    mb.add_arc_pts("primary", (-12.0, -15.5), (-9.4, -12.4), -0.95)
    mb.add_arc_pts("primary", (-9.4, -12.4), (-4.8, -12.5), -0.6)
    mb.add_arc_pts("primary", (-4.8, -12.5), (-1.8, -14.5), -0.8)
    mb.add_arc_pts("detail", (-1.8, -14.5), (-2.5, -17.2), -0.5)
    mb.add_arc_pts("detail", (-8.8, -13.6), (-5.2, -13.6), 0.45)

    # Neatly trimmed silver-gray British brush mustache (soft open corners & outward-sweeping strands)
    mb.add_arc_pts("primary", (-14.5, -4.8), (-6.8, -10.2), 1.4)
    mb.add_arc_pts("primary", (-6.8, -10.2), (5.8, -5.0), 1.5)
    mb.add_arc_pts("primary", (-13.6, -3.2), (-6.5, -4.4), 0.9)
    mb.add_arc_pts("primary", (-6.5, -4.4), (5.0, -3.0), 0.9)
    # Outward-sweeping natural brush-mustache strands (left wing down-left, right wing down-right)
    mb.add_arc_pts("detail", (-7.5, -8.8), (-13.0, -4.2), -0.6)
    mb.add_arc_pts("detail", (-6.8, -8.5), (-10.5, -4.4), -0.4)
    mb.add_arc_pts("detail", (-6.0, -8.5), (-2.2, -4.4), 0.4)
    mb.add_arc_pts("detail", (-4.8, -8.8), (1.8, -4.2), 0.5)
    mb.add_arc_pts("detail", (-2.2, -8.4), (4.6, -4.0), 0.6)

    mb.add_arc_pts("detail", (-10.5, -1.2), (-1.5, -1.5), -0.8)
    mb.add_arc_pts("detail", (-11.0, 2.8), (-3.5, 3.0), -0.7)
    mb.add_arc_pts("detail", (4.5, -13.5), (10.5, -3.5), 1.1)

    # Sculpted right ear
    mb.add_arc_pts("primary", (27.4, -25.8), (35.8, -25.2), 1.8)
    mb.add_arc_pts("primary", (35.8, -25.2), (34.4, -15.0), 1.7)
    mb.add_arc_pts("primary", (34.4, -15.0), (28.5, -10.5), 1.4)
    mb.add_arc_pts("primary", (28.5, -10.5), (26.0, -13.0), 0.9)
    mb.add_arc_pts("detail", (28.8, -22.5), (32.5, -20.0), 1.3)
    mb.add_arc_pts("detail", (32.5, -20.0), (29.8, -13.8), 1.2)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Sweeping Silver-White Hair & Sculpted Temple Wave
    # -------------------------------------------------------------------------
    # Grand parted silver-white crown & temple silhouette
    mb.add_arc_pts("primary", (-18.8, -46.5), (-19.6, -54.0), 1.5)
    mb.add_arc_pts("primary", (-19.6, -54.0), (-9.5, -62.0), 2.5)
    mb.add_arc_pts("primary", (-9.5, -62.0), (7.5, -63.5), 2.3)
    mb.add_arc_pts("primary", (7.5, -63.5), (23.5, -58.8), 2.4)
    mb.add_arc_pts("primary", (23.5, -58.8), (33.5, -49.5), 2.2)
    # Sculpted right temple wave curling crisply above right ear
    mb.add_arc_pts("primary", (33.5, -49.5), (38.2, -36.5), 2.4)
    mb.add_arc_pts("primary", (38.2, -36.5), (33.2, -27.8), 2.0)

    # Clean side part & sweeping Euclid III.12 silver hair waves (detail)
    mb.add_arc_pts("detail", (20.8, -51.5), (27.5, -56.5), -0.9)
    mb.add_wave("detail", (-13.5, -56.2), (19.5, -54.5), 4, wave_angle_deg * 0.65, 1)
    mb.add_wave("detail", (-7.5, -59.6), (18.5, -58.2), 3, wave_angle_deg * 0.6, -1)
    mb.add_wave("detail", (22.5, -49.2), (35.2, -35.8), 3, wave_angle_deg * 0.72, 1)
    mb.add_wave("detail", (25.5, -43.5), (33.2, -31.2), 3, wave_angle_deg * 0.68, -1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: High Rounded Edwardian Collar, Silk Tie, Waistcoat & Suit Coat
    # -------------------------------------------------------------------------
    # Neck edges descending into stiff white collar
    mb.add_arc_pts("primary", (-8.5, 10.5), (-7.5, 17.8), 0.5)
    mb.add_arc_pts("primary", (24.5, -1.5), (28.6, 7.5), -0.7)

    # Crisp high white Edwardian rounded club collar (cleanly framing tie knot!)
    mb.add_arc_pts("primary", (-7.5, 17.6), (7.5, 17.8), -1.6)
    mb.add_arc_pts("primary", (7.5, 17.8), (28.6, 7.5), -2.2)
    # Left rounded club collar flap
    mb.add_arc_pts("primary", (-7.5, 17.6), (-8.5, 31.2), -0.7)
    mb.add_arc_pts("primary", (-8.5, 31.2), (-4.0, 34.8), -1.5)
    mb.add_arc_pts("primary", (-4.0, 34.8), (0.2, 22.8), -1.1)
    # Right rounded club collar flap (broad, dignified curve)
    mb.add_arc_pts("primary", (28.6, 7.5), (30.5, 18.2), 1.0)
    mb.add_arc_pts("primary", (30.5, 18.2), (13.8, 36.2), 2.2)
    mb.add_arc_pts("primary", (13.8, 36.2), (7.0, 36.5), 1.4)
    mb.add_arc_pts("primary", (7.0, 36.5), (4.6, 22.8), 1.1)

    # Silk ascot / necktie nestled cleanly inside collar opening
    mb.add_line("primary", 0.4, 23.5, 4.6, 23.5)
    mb.add_arc_pts("primary", (0.4, 23.5), (-0.2, 33.8), -0.5)
    mb.add_arc_pts("primary", (4.6, 23.5), (5.2, 33.8), 0.5)
    mb.add_arc_pts("primary", (-0.2, 33.8), (5.2, 33.8), -0.8)
    # Broad silk tie blade descending cleanly behind waistcoat V
    mb.add_arc_pts("primary", (-0.2, 33.8), (-6.8, 60.0), -1.4)
    mb.add_arc_pts("primary", (5.2, 33.8), (4.8, 49.5), 1.0)
    # Silk knot & blade pleat (detail)
    mb.add_arc_pts("detail", (0.6, 28.0), (4.4, 28.0), -0.5)
    mb.add_arc_pts("detail", (2.2, 35.0), (-2.0, 56.5), -0.7)

    # Tailored waistcoat V-opening merging cleanly into single buttoned placket
    mb.add_line("primary", -8.5, 31.2, -7.2, 65.0)
    mb.add_arc_pts("primary", (21.5, 31.2), (-7.2, 65.0), -1.6)
    mb.add_arc_pts("primary", (-7.2, 65.0), (-11.2, 86.0), 0.8)
    mb.add_circle("detail", -6.4, 72.5, 1.2)
    mb.add_circle("detail", -7.8, 80.5, 1.2)

    # Formal Edwardian suit coat lapels & broad shoulders clipped flush to MED_R
    # Left collar & notched lapel
    mb.add_arc_pts("primary", (-10.8, 17.8), (-22.8, 32.0), -1.4)
    mb.add_line("primary", -22.8, 32.0, -16.8, 40.5)
    mb.add_line("primary", -16.8, 40.5, -24.0, 48.2)
    mb.add_arc_pts("primary", (-24.0, 48.2), (-16.5, 86.5), -1.8)

    # Right collar & notched lapel
    mb.add_arc_pts("primary", (31.2, 11.0), (37.8, 27.5), 1.5)
    mb.add_line("primary", 37.8, 27.5, 28.8, 36.5)
    mb.add_line("primary", 28.8, 36.5, 35.8, 44.5)
    mb.add_arc_pts("primary", (35.8, 44.5), (4.5, 87.0), 2.8)

    # Broad Edwardian gentleman's shoulders descending flush to medallion rim
    mb.add_arc_pts("primary", (-22.8, 32.0), (-75.5, 79.0), -6.5)
    mb.add_arc_pts("primary", (31.2, 11.0), (84.0, 71.0), 6.8)

    # Clean non-crossing coat & sleeve drapery folds (detail)
    mb.add_arc_pts("detail", (-42.0, 42.0), (-52.5, 80.0), -2.2)
    mb.add_arc_pts("detail", (-31.5, 58.0), (-34.5, 84.5), -1.5)
    mb.add_arc_pts("detail", (46.5, 28.0), (60.5, 76.0), 2.6)
    mb.add_arc_pts("detail", (36.5, 50.0), (42.0, 82.5), 1.8)

    return mb.build()


def build_heath_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Sir Thomas Little Heath medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_heath_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_heath_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``heath_dark.svg`` and ``heath_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "heath_dark.svg"
    light_path = target_dir / "heath_light.svg"
    dark_path.write_text(
        build_heath_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_heath_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
