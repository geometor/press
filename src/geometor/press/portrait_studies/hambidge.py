"""Study 42: Jay Hambidge — Pure Sacred Geometric Emblem Medallion.

Celebrates Jay Hambidge's *Dynamic Symmetry* (1920), uniting the compass-arc
unfolding of Root Rectangles (``1, sqrt(2), sqrt(3), sqrt(4), sqrt(5)``) with
the exact **Root-5 (``1 : sqrt(5)``)** and **Whirling-Square Golden Rectangle
(``1 : phi``)** reciprocal decompositions inside the unified ``R = 68``
graduated astrolabe seal:

1. **Root-5 Dynamic Rectangle, Central Unit Square, & Harmonic Circumcircles**:
   Centered at ``(0, -8)`` with unit height ``h = 50`` and exact width
   ``w = h * sqrt(5)``, partitioned into the central unit square (``1 x 1``)
   flanked symmetrically by two vertical Reciprocal Golden Rectangles
   (``1 x 1/phi``), framed by the exact circumcircles of the unit square
   (``R_sq = h / sqrt(2)``) and Root-5 rectangle (``R_r5 = h * sqrt(6) / 2``,
   ratio ``sqrt(3)``).
2. **Twin Generating Semicircles & Root-Rectangle Compass Unfolding**: Twin
   generating semicircles (centered on the base and crown midpoints, radius
   ``w/2``) sweep symmetrically through the unit square corners to establish
   ``1/phi + 1 + 1/phi = sqrt(5)``, while four compass-swing unfolding arcs
   from the bottom-left corner sweep ``1 -> sqrt(2) -> sqrt(3) -> sqrt(4) ->
   sqrt(5)`` onto calibrated exterior ruler ticks along the base.
3. **Golden Dynamic Symmetry Diagonals & Whirling-Square Spiral**: Exact
   orthogonal main and reciprocal diagonals meet at the Root-5 reciprocal pole
   ``E_L`` (left) and the Golden "Eye" pole ``E_R`` (right), into which a
   7-turn exact quarter-circle Whirling-Square Golden Spiral coils smoothly.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_hambidge_elements",
    "build_hambidge_svg",
    "write_hambidge_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _line_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Point:
    """Return the exact intersection of lines ``p1-p2`` and ``p3-p4``."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-12:
        msg = "Parallel lines in _line_intersection"
        raise ValueError(msg)
    det1 = x1 * y2 - y1 * x2
    det2 = x3 * y4 - y3 * x4
    px = (det1 * (x3 - x4) - (x1 - x2) * det2) / denom
    py = (det1 * (y3 - y4) - (y1 - y2) * det2) / denom
    return (px, py)


def _add_astrolabe_seal(mb: MedallionBuilder, r_seal: float) -> None:
    """Add the unified GEOMETOR Emblem Pantheon scaffold and graduated astrolabe seal."""
    ox, oy = MED_CX, MED_CY
    r_bezel = r_seal + 4.8

    # Subtle medallion-centered sacred scaffold rings & crosshairs
    mb.add_circle("scaffold", ox, oy, MED_R, clip=False)
    for r in (78.0, 52.0, 26.0):
        mb.add_circle("scaffold", ox, oy, r)
    mb.add_line("scaffold", ox, oy - MED_R, ox, oy + MED_R)
    mb.add_line("scaffold", ox - MED_R, oy, ox + MED_R, oy)
    for deg in (45.0, 135.0, 225.0, 315.0):
        p_in = polar(ox, oy, 78.0, deg)
        p_out = polar(ox, oy, MED_R, deg)
        mb.add_line("scaffold", p_in[0], p_in[1], p_out[0], p_out[1])

    # Bold outer seal ring & fine graduated astrolabe bezel
    mb.add_circle("primary", ox, oy, r_seal)
    mb.add_circle("detail", ox, oy, r_bezel)

    # 36 calibrated astrolabe degree ticks & 4 cardinal golden pins
    for k in range(36):
        deg = float(k * 10)
        if k % 9 == 0:
            p1 = polar(ox, oy, r_seal, deg)
            p2 = polar(ox, oy, r_bezel + 3.2, deg)
            mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
            tip = polar(ox, oy, r_bezel + 4.8, deg)
            mb.add_circle("golden", tip[0], tip[1], 1.15, filled=True)
        elif k % 3 == 0:
            p1 = polar(ox, oy, r_seal, deg)
            p2 = polar(ox, oy, r_bezel + 1.4, deg)
            mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])
        else:
            p1 = polar(ox, oy, r_seal + 1.1, deg)
            p2 = polar(ox, oy, r_bezel, deg)
            mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])


def _add_right_angle_mark(
    mb: MedallionBuilder,
    layer: str,
    vertex: Point,
    dir1: Point,
    dir2: Point,
    size: float = 3.0,
) -> None:
    """Draw a crisp orthogonal right-angle square tick at ``vertex`` along two unit directions."""
    vx, vy = vertex
    p1 = (vx + size * dir1[0], vy + size * dir1[1])
    p2 = (vx + size * dir2[0], vy + size * dir2[1])
    p3 = (p1[0] + size * dir2[0], p1[1] + size * dir2[1])
    mb.add_line(layer, p1[0], p1[1], p3[0], p3[1])
    mb.add_line(layer, p2[0], p2[1], p3[0], p3[1])


def build_hambidge_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Jay Hambidge.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    sqrt5 = math.sqrt(5.0)
    phi = 0.5 * (1.0 + sqrt5)

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Root-5 Rectangle (1 : sqrt(5)) & Central Unit Square (1 x 1)
    # ------------------------------------------------------------------
    h = 50.0
    w = h * sqrt5
    half_h = 0.5 * h
    half_w = 0.5 * w

    x_left = ox - half_w
    x_right = ox + half_w
    x_sq_l = ox - half_h
    x_sq_r = ox + half_h
    y_top = oy - half_h
    y_bot = oy + half_h

    r_sq_circ = half_h * math.sqrt(2.0)  # Exact circumcircle of central unit square
    r_r5_circ = math.hypot(half_w, half_h)  # Exact circumcircle of Root-5 rectangle

    # Verify exact corner clearance inside R_seal = 68.0, golden reciprocal ratio,
    # and circumcircle ratio R_r5 / R_sq == sqrt(3)
    if r_r5_circ >= r_seal - 6.0:
        msg = "Root-5 corners too close to seal rim"
        raise ValueError(msg)
    recip_w = x_right - x_sq_r
    if abs((h / recip_w) - phi) > 1e-12:
        msg = f"Reciprocal golden rectangle ratio violated: {h / recip_w} != {phi}"
        raise ValueError(msg)
    if abs((r_r5_circ / r_sq_circ) - math.sqrt(3.0)) > 1e-12:
        msg = "Root-5 to unit-square circumcircle ratio violated"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Concentric Circumcircles, Twin Generating Semicircles, & Unfolding
    # ------------------------------------------------------------------
    # Exact circumcircles of the Root-5 rectangle and central unit square
    # give balanced sculptural presence across the full vertical seal diameter.
    mb.add_circle("detail", ox, oy, r_r5_circ)
    mb.add_circle("detail", ox, oy, r_sq_circ)

    # Twin generating semicircles (radius w/2) centered at base & crown midpoints,
    # sweeping symmetrically through the unit square corners.
    r_semi = half_w
    if abs(_dist((ox, y_bot), (x_sq_r, y_top)) - r_semi) > 1e-12:
        msg = "Generating semicircle does not pass through unit square corners"
        raise ValueError(msg)
    # Upper generating semicircle centered at (ox, y_bot)
    mb.add_arc("detail", ox, y_bot, r_semi, 180.0, 270.0)
    mb.add_arc("detail", ox, y_bot, r_semi, 270.0, 360.0)
    # Mirror lower generating semicircle centered at (ox, y_top)
    mb.add_arc("detail", ox, y_top, r_semi, 0.0, 90.0)
    mb.add_arc("detail", ox, y_top, r_semi, 90.0, 180.0)

    # Classical compass-swing unfolding 1 -> sqrt(2) -> sqrt(3) -> sqrt(4) -> sqrt(5)
    # anchored at bottom-left corner BL = (x_left, y_bot) with crisp exterior ticks
    bl: Point = (x_left, y_bot)
    for k in (1, 2, 3, 4):
        x_cur = x_left + h * math.sqrt(float(k))
        rad_k = h * math.sqrt(float(k + 1))
        ang_top = math.degrees(math.atan2(y_top - y_bot, x_cur - x_left))
        mb.add_arc("detail", bl[0], bl[1], rad_k, ang_top, 0.0)
        # Calibrated exterior ruler tick below the base edge at each root station
        mb.add_line("golden", x_cur, y_bot + 1.4, x_cur, y_bot + 4.8)
        mb.add_line("scaffold", x_cur, y_top, x_cur, y_bot)

    # ------------------------------------------------------------------
    # 3. Bold Primary Root-5 Outer Frame & Central Unit Square
    # ------------------------------------------------------------------
    mb.add_line("primary", x_left, y_top, x_right, y_top)
    mb.add_line("primary", x_left, y_bot, x_right, y_bot)
    mb.add_line("primary", x_left, y_top, x_left, y_bot)
    mb.add_line("primary", x_right, y_top, x_right, y_bot)
    mb.add_line("primary", x_sq_l, y_top, x_sq_l, y_bot)
    mb.add_line("primary", x_sq_r, y_top, x_sq_r, y_bot)

    # ------------------------------------------------------------------
    # 4. Golden Dynamic Symmetry Diagonals & Exact Orthogonal Reciprocals
    # ------------------------------------------------------------------
    # (a) Right Golden Rectangle S U G_R (x in [x_sq_l, x_right], exact 1 : phi)
    g_tl: Point = (x_sq_l, y_top)
    g_br: Point = (x_right, y_bot)
    gr_bl: Point = (x_sq_r, y_bot)
    gr_tr: Point = (x_right, y_top)

    v_main = (g_br[0] - g_tl[0], g_br[1] - g_tl[1])
    v_rec = (gr_tr[0] - gr_bl[0], gr_tr[1] - gr_bl[1])
    if abs(v_main[0] * v_rec[0] + v_main[1] * v_rec[1]) > 1e-10:
        msg = "Golden rectangle main & reciprocal diagonals not orthogonal"
        raise ValueError(msg)

    eye_r = _line_intersection(g_tl, g_br, gr_bl, gr_tr)
    mb.add_line("golden", g_tl[0], g_tl[1], g_br[0], g_br[1])
    mb.add_line("golden", gr_bl[0], gr_bl[1], gr_tr[0], gr_tr[1])

    # (b) Left Root-5 Full Diagonal (BL -> TR) & Exact Orthogonal Reciprocal
    r5_tl: Point = (x_left, y_top)
    r5_rec_bot: Point = (x_left + h / sqrt5, y_bot)
    v_r5 = (gr_tr[0] - bl[0], gr_tr[1] - bl[1])
    v_r5_rec = (r5_rec_bot[0] - r5_tl[0], r5_rec_bot[1] - r5_tl[1])
    if abs(v_r5[0] * v_r5_rec[0] + v_r5[1] * v_r5_rec[1]) > 1e-10:
        msg = "Root-5 main & reciprocal diagonals not orthogonal"
        raise ValueError(msg)
    eye_l = _line_intersection(bl, gr_tr, r5_tl, r5_rec_bot)
    mb.add_line("detail", bl[0], bl[1], gr_tr[0], gr_tr[1])
    mb.add_line("golden", r5_tl[0], r5_tl[1], r5_rec_bot[0], r5_rec_bot[1])

    l_r5 = math.hypot(*v_r5)
    l_r5_rec = math.hypot(*v_r5_rec)
    _add_right_angle_mark(
        mb,
        "detail",
        eye_l,
        (v_r5[0] / l_r5, v_r5[1] / l_r5),
        (v_r5_rec[0] / l_r5_rec, v_r5_rec[1] / l_r5_rec),
        size=3.0,
    )

    # ------------------------------------------------------------------
    # 5. Exact 7-Turn Whirling-Square Quarter-Circle Golden Spiral into E_R
    # ------------------------------------------------------------------
    rx0, rx1, ry0, ry1 = x_sq_l, x_right, y_top, y_bot
    for step in range(7):
        orient = step % 4
        if orient == 0:
            s = ry1 - ry0
            cx, cy = rx0 + s, ry1
            mb.add_arc("golden", cx, cy, s, 180.0, 270.0)
            if step > 0:
                mb.add_line("detail", rx0 + s, ry0, rx0 + s, ry1)
            rx0 += s
        elif orient == 1:
            s = rx1 - rx0
            cx, cy = rx0, ry0 + s
            mb.add_arc("golden", cx, cy, s, 270.0, 360.0)
            mb.add_line("detail", rx0, ry0 + s, rx1, ry0 + s)
            ry0 += s
        elif orient == 2:
            s = ry1 - ry0
            cx, cy = rx1 - s, ry0
            mb.add_arc("golden", cx, cy, s, 0.0, 90.0)
            mb.add_line("detail", rx1 - s, ry0, rx1 - s, ry1)
            rx1 -= s
        else:
            s = rx1 - rx0
            cx, cy = rx1, ry1 - s
            mb.add_arc("golden", cx, cy, s, 90.0, 180.0)
            mb.add_line("detail", rx0, ry1 - s, rx1, ry1 - s)
            ry1 -= s

    if not (rx0 - 1e-6 <= eye_r[0] <= rx1 + 1e-6 and ry0 - 1e-6 <= eye_r[1] <= ry1 + 1e-6):
        msg = f"Golden Eye Pole {eye_r} outside nested whirling box [{rx0},{rx1}]x[{ry0},{ry1}]"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 6. Luminous Golden Corner Nodes & Dynamic Symmetry Poles
    # ------------------------------------------------------------------
    for vx, vy in (
        (x_left, y_top),
        (x_right, y_top),
        (x_left, y_bot),
        (x_right, y_bot),
    ):
        mb.add_circle("golden", vx, vy, 3.2)
        mb.add_circle("golden", vx, vy, 1.55, filled=True)

    for vx, vy in (
        (x_sq_l, y_top),
        (x_sq_r, y_top),
        (x_sq_l, y_bot),
        (x_sq_r, y_bot),
        (ox, y_top),
        (ox, y_bot),
    ):
        mb.add_circle("golden", vx, vy, 2.3)
        mb.add_circle("golden", vx, vy, 1.1, filled=True)

    # Left Root-5 reciprocal pole E_L
    mb.add_circle("golden", eye_l[0], eye_l[1], 3.8)
    mb.add_circle("golden", eye_l[0], eye_l[1], 1.9, filled=True)

    # Radiant double-ringed Golden Eye Pole E_R (whirling-square convergence jewel)
    mb.add_circle("golden", eye_r[0], eye_r[1], 4.5)
    mb.add_circle("golden", eye_r[0], eye_r[1], 2.3, filled=True)

    return mb.build()


def build_hambidge_svg(theme: str = "dark") -> str:
    """Render the Jay Hambidge medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_hambidge_elements()
    return render_medallion_svg(layers, theme=theme)


def write_hambidge_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``hambidge_dark.svg`` and ``hambidge_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "hambidge_dark.svg"
    light_path = target_dir / "hambidge_light.svg"
    dark_path.write_text(build_hambidge_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_hambidge_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
