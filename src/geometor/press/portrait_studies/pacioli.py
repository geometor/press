"""Study 05: Fra Luca Pacioli (1495) in lines, circles, and circular arcs."""

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
    polar,
    render_medallion_svg,
)

__all__ = ["build_pacioli_elements", "build_pacioli_svg", "write_pacioli_svgs"]

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _arc_through(
    p1: tuple[float, float],
    p2: tuple[float, float],
    sagitta: float,
) -> tuple[float, float, float, float, float]:
    """Compute circular arc ``(cx, cy, r, a1, a2)`` from ``p1`` to ``p2`` with signed sagitta."""
    x1, y1 = p1
    x2, y2 = p2
    mx, my = 0.5 * (x1 + x2), 0.5 * (y1 + y2)
    dx, dy = x2 - x1, y2 - y1
    chord = math.hypot(dx, dy)
    half_c = 0.5 * chord
    s = abs(sagitta)
    r = (half_c * half_c + s * s) / (2.0 * s)
    nx, ny = -dy / chord, dx / chord
    sign = 1.0 if sagitta >= 0.0 else -1.0
    d_center = r - s
    cx = mx - sign * d_center * nx
    cy = my - sign * d_center * ny
    a1 = math.degrees(math.atan2(y1 - cy, x1 - cx))
    a2 = math.degrees(math.atan2(y2 - cy, x2 - cx))
    return cx, cy, r, a1, a2


def _line_circle_y(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    cx: float,
    cy: float,
    r: float,
) -> tuple[float, float]:
    """Return intersection of line ``(x1,y1)-(x2,y2)`` with circle ``(cx,cy,r)``."""
    dx, dy = x2 - x1, y2 - y1
    fx, fy = x1 - cx, y1 - cy
    a = dx * dx + dy * dy
    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - r * r
    disc = max(0.0, b * b - 4.0 * a * c)
    s = math.sqrt(disc)
    t1 = (-b - s) / (2.0 * a)
    t2 = (-b + s) / (2.0 * a)
    candidates = [t for t in (t1, t2) if -0.5 <= t <= 1.5]
    t = min(candidates, key=lambda v: abs(v - 0.5)) if candidates else t2
    return x1 + t * dx, y1 + t * dy


def build_pacioli_elements() -> dict[str, list[dict[str, Any]]]:
    """Construct Fra Luca Pacioli medallion strictly from lines, circles, and circular arcs.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``primary``, and ``detail`` primitive lists.
    """
    radius_head = 26.0
    phi = (1.0 + math.sqrt(5.0)) / 2.0

    scaffold: list[dict[str, Any]] = []
    golden: list[dict[str, Any]] = []
    detail: list[dict[str, Any]] = []
    primary: list[dict[str, Any]] = []

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

    def add_arc_pts(
        layer: list[dict[str, Any]],
        p1: tuple[float, float],
        p2: tuple[float, float],
        sagitta: float,
    ) -> None:
        cx, cy, r, a1, a2 = _arc_through(p1, p2, sagitta)
        add_arc(layer, cx, cy, r, a1, a2)

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    add_circle(scaffold, MED_CX, MED_CY, MED_R)
    add_line(scaffold, 0.0, -105.0, 0.0, 90.0)
    add_line(scaffold, -98.0, -27.0, 98.0, -27.0)
    add_line(scaffold, -98.0, 0.0, 98.0, 0.0)
    add_circle(scaffold, 0.0, -27.0, radius_head)
    add_circle(scaffold, 0.0, -27.0, radius_head * phi)
    add_circle(scaffold, 0.0, -27.0, radius_head * 2.0)
    add_circle(scaffold, -15.0, -27.0, radius_head / 2.0)
    add_circle(scaffold, 6.0, -27.0, radius_head / 2.0)

    # -------------------------------------------------------------------------
    # Layer 2: Golden Signature Motif
    #   (A) Suspended Glass Rhombicuboctahedron (upper-left)
    #   (B) Golden Ratio Dividers (upper-right)
    # -------------------------------------------------------------------------
    rcx, rcy = -57.0, -34.0
    rr = 17.0
    top_v = polar(rcx, rcy, rr, -90.0)
    add_line(golden, rcx, -69.5, top_v[0], top_v[1])

    outer_pts = [polar(rcx, rcy, rr, -90.0 + 45.0 * k) for k in range(8)]
    for k in range(8):
        p1 = outer_pts[k]
        p2 = outer_pts[(k + 1) % 8]
        add_line(golden, p1[0], p1[1], p2[0], p2[1])

    eq_y_top = rcy - 3.6
    eq_y_bot = rcy + 3.6
    eq_x_in = 6.8
    eq_x_out = rr * math.cos(math.radians(22.5))
    add_line(golden, rcx - eq_x_in, eq_y_top, rcx + eq_x_in, eq_y_top)
    add_line(golden, rcx - eq_x_in, eq_y_bot, rcx + eq_x_in, eq_y_bot)
    add_line(golden, rcx - eq_x_in, eq_y_top, rcx - eq_x_in, eq_y_bot)
    add_line(golden, rcx + eq_x_in, eq_y_top, rcx + eq_x_in, eq_y_bot)
    add_line(golden, rcx - eq_x_in, eq_y_top, outer_pts[6][0], outer_pts[6][1])
    add_line(golden, rcx - eq_x_in, eq_y_bot, outer_pts[6][0], outer_pts[6][1])
    add_line(golden, rcx + eq_x_in, eq_y_top, outer_pts[2][0], outer_pts[2][1])
    add_line(golden, rcx + eq_x_in, eq_y_bot, outer_pts[2][0], outer_pts[2][1])
    add_line(golden, rcx - eq_x_out, rcy, rcx + eq_x_out, rcy)

    up_y1, up_y2 = rcy - 12.6, rcy - 8.2
    up_x = 5.4
    add_line(golden, rcx - up_x, up_y1, rcx + up_x, up_y1)
    add_line(golden, rcx - up_x, up_y2, rcx + up_x, up_y2)
    add_line(golden, rcx - up_x, up_y1, rcx - up_x, up_y2)
    add_line(golden, rcx + up_x, up_y1, rcx + up_x, up_y2)
    add_line(golden, rcx - up_x, up_y1, outer_pts[0][0], outer_pts[0][1])
    add_line(golden, rcx + up_x, up_y1, outer_pts[0][0], outer_pts[0][1])
    add_line(golden, rcx - up_x, up_y1, outer_pts[7][0], outer_pts[7][1])
    add_line(golden, rcx + up_x, up_y1, outer_pts[1][0], outer_pts[1][1])
    add_line(golden, rcx - up_x, up_y2, outer_pts[7][0], outer_pts[7][1])
    add_line(golden, rcx + up_x, up_y2, outer_pts[1][0], outer_pts[1][1])
    add_line(golden, rcx - up_x, up_y2, rcx - eq_x_in, eq_y_top)
    add_line(golden, rcx + up_x, up_y2, rcx + eq_x_in, eq_y_top)

    lo_y1, lo_y2 = rcy + 8.2, rcy + 12.6
    lo_x = 5.4
    add_line(golden, rcx - lo_x, lo_y1, rcx + lo_x, lo_y1)
    add_line(golden, rcx - lo_x, lo_y2, rcx + lo_x, lo_y2)
    add_line(golden, rcx - lo_x, lo_y1, rcx - lo_x, lo_y2)
    add_line(golden, rcx + lo_x, lo_y1, rcx + lo_x, lo_y2)
    add_line(golden, rcx - lo_x, lo_y2, outer_pts[4][0], outer_pts[4][1])
    add_line(golden, rcx + lo_x, lo_y2, outer_pts[4][0], outer_pts[4][1])
    add_line(golden, rcx - lo_x, lo_y2, outer_pts[5][0], outer_pts[5][1])
    add_line(golden, rcx + lo_x, lo_y2, outer_pts[3][0], outer_pts[3][1])
    add_line(golden, rcx - lo_x, lo_y1, outer_pts[5][0], outer_pts[5][1])
    add_line(golden, rcx + lo_x, lo_y1, outer_pts[3][0], outer_pts[3][1])
    add_line(golden, rcx - lo_x, lo_y1, rcx - eq_x_in, eq_y_bot)
    add_line(golden, rcx + lo_x, lo_y1, rcx + eq_x_in, eq_y_bot)

    # (B) Golden Ratio Dividers (upper-right)
    px, py = 58.0, -34.0
    short_len = 13.0
    long_len = short_len * phi
    ang1, ang2 = 108.0, 66.0
    p_l_lo = polar(px, py, long_len, ang1)
    p_l_hi = polar(px, py, short_len, ang2 + 180.0)
    p_r_lo = polar(px, py, long_len, ang2)
    p_r_hi = polar(px, py, short_len, ang1 + 180.0)
    add_line(golden, p_l_hi[0], p_l_hi[1], p_r_lo[0], p_r_lo[1])
    add_line(golden, p_r_hi[0], p_r_hi[1], p_l_lo[0], p_l_lo[1])
    add_circle(golden, px, py, 1.8)
    add_circle(golden, p_l_hi[0], p_l_hi[1], 0.9)
    add_circle(golden, p_r_hi[0], p_r_hi[1], 0.9)
    add_arc(golden, px, py, long_len * 0.618, ang2, ang1)
    add_arc(golden, px, py, short_len * 0.618, ang2 + 180.0, ang1 + 180.0)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Face, Tonsure, Cowl Hood (Concentric Arcs), & Habit
    # -------------------------------------------------------------------------
    # Smooth face contour (all arcs bow outward cleanly)
    # Left cheek -> jaw -> chin -> right jaw -> right cheek
    add_arc_pts(primary, (-21.8, -38.5), (-21.8, -11.0), -1.6)   # left temple/cheek
    add_arc_pts(primary, (-21.8, -11.0), (-14.5, 6.5), -2.2)     # left lower cheek
    add_arc_pts(primary, (-14.5, 6.5), (-5.0, 13.4), -1.8)       # left jaw
    add_arc_pts(primary, (-5.0, 13.4), (4.5, 13.2), -1.2)        # chin base
    add_arc_pts(primary, (4.5, 13.2), (16.5, 5.5), -2.0)         # right jaw
    add_arc_pts(primary, (16.5, 5.5), (20.8, -14.0), -2.0)       # right lower cheek
    add_arc_pts(primary, (20.8, -14.0), (19.5, -38.0), -1.5)     # right temple/cheek

    # Tonsure bangs (horizontal fringe under hood)
    add_arc_pts(primary, (-20.8, -40.5), (19.2, -40.8), -2.2)
    add_arc_pts(detail, (-19.8, -43.8), (18.2, -44.0), -2.0)
    for bx in (-16.0, -12.0, -8.0, -4.0, 0.0, 4.0, 8.0, 12.0, 15.5):
        add_line(detail, bx, -44.2, bx - 0.3, -41.0)

    # Eyebrows
    add_arc_pts(primary, (-20.5, -32.2), (-9.2, -33.2), -1.6)
    add_arc_pts(primary, (-1.8, -33.2), (13.8, -32.0), -2.0)

    # Left eye (centered at -15.0, -27.5)
    add_arc(primary, -15.0, -21.5, 7.6, -132.0, -48.0)   # upper lash
    add_arc(detail, -15.0, -22.8, 7.4, -128.0, -52.0)    # upper lid fold
    add_arc(detail, -15.0, -32.2, 6.4, 54.0, 126.0)      # lower lid
    add_circle(detail, -15.2, -27.6, 2.2)                # iris
    add_circle(primary, -15.3, -27.6, 0.95, filled=True)  # pupil

    # Right eye (centered at +5.8, -27.2)
    add_arc(primary, 5.8, -20.2, 8.8, -134.0, -46.0)     # upper lash
    add_arc(detail, 5.8, -21.6, 8.6, -128.0, -52.0)      # upper lid fold
    add_arc(detail, 5.8, -32.4, 7.2, 54.0, 126.0)        # lower lid
    add_circle(detail, 5.6, -27.2, 2.35)                 # iris
    add_circle(primary, 5.5, -27.2, 1.0, filled=True)    # pupil

    # Nose (3/4 left)
    add_line(primary, -4.6, -29.5, -6.8, -11.5)
    add_line(detail, -0.8, -28.0, -1.6, -13.0)
    add_arc_pts(primary, (-7.2, -10.8), (-2.2, -10.8), -1.6)  # nose tip bows down
    add_arc(primary, -8.3, -10.2, 2.0, 65.0, 215.0)
    add_arc(primary, -1.5, -10.0, 2.1, -35.0, 125.0)

    # Mouth & facial creases
    add_arc_pts(primary, (-11.2, 1.8), (3.8, 2.0), -0.7)   # mouth bows gently down
    add_arc_pts(detail, (-9.2, 0.5), (1.8, 0.6), 0.4)      # upper lip bow
    add_arc_pts(detail, (-8.5, 4.2), (1.2, 4.3), -0.9)     # lower lip shadow
    add_line(detail, -10.5, -6.5, -14.8, 2.0)
    add_line(detail, 2.2, -6.0, 8.5, 4.5)
    add_arc_pts(detail, (-5.5, 8.8), (0.5, 8.8), -0.8)

    # Franciscan Cowl Hood — Smooth Concentric Circular Arcs
    # Outer hood: crown arc + smooth left/right cowl sweeps down to neck
    add_arc(primary, 0.5, -40.5, 28.0, -172.0, -8.0)       # crown dome (top at y=-68.5)
    # Left outer hood: (-27.2, -44.4) -> (-28.5, -12.0) -> (-26.0, 10.0) -> (-18.0, 22.0)
    add_arc_pts(primary, (-27.2, -44.4), (-28.5, -10.0), 1.6)
    add_arc_pts(primary, (-28.5, -10.0), (-20.0, 20.5), 4.2)
    # Right outer hood: (28.2, -44.4) -> (28.5, -10.0) -> (21.0, 20.5)
    add_arc_pts(primary, (28.2, -44.4), (28.5, -10.0), -1.6)
    add_arc_pts(primary, (28.5, -10.0), (21.0, 20.5), -4.2)

    # Inner hood opening: top arch + smooth left/right inner rims
    add_arc(primary, -0.5, -31.5, 22.2, -162.0, -18.0)     # inner arch top (y=-53.7)
    add_arc_pts(primary, (-21.6, -38.4), (-24.5, -10.0), 1.6)
    add_arc_pts(primary, (-24.5, -10.0), (-11.0, 18.0), 4.8)
    add_arc_pts(primary, (20.6, -38.4), (23.2, -10.0), -1.6)
    add_arc_pts(primary, (23.2, -10.0), (10.0, 18.0), -4.8)

    # Concentric hood seam & interior shadow arcs
    add_line(detail, 1.0, -68.5, 0.5, -53.7)               # center crown seam
    add_arc(detail, 0.0, -36.5, 25.2, -166.0, -14.0)       # concentric mid-hood arc
    add_arc(detail, 0.0, -28.0, 30.8, 174.0, 202.0)        # left concentric shadow
    add_arc(detail, 0.0, -28.0, 31.2, -22.0, 6.0)          # right concentric shadow

    # Neck cowl collar wrap
    add_arc_pts(primary, (-20.0, 20.5), (21.0, 20.5), -7.0)   # upper collar fold
    add_arc_pts(detail, (-18.5, 25.0), (19.5, 25.0), -6.5)    # lower collar fold

    # Franciscan Capelet (Mozzetta) — Entirely inside MED_R=92.0
    # Upward-bowed hem arc centered below at (1.0, 230.0), R=180.0 -> peaks at y=50.0
    hem_cx, hem_cy, hem_rad = 1.0, 230.0, 180.0
    hem_l = _line_circle_y(-44.0, 31.0, -63.0, 56.0, hem_cx, hem_cy, hem_rad)
    hem_r = _line_circle_y(44.0, 30.0, 64.0, 55.5, hem_cx, hem_cy, hem_rad)
    a_hem_l = math.degrees(math.atan2(hem_l[1] - hem_cy, hem_l[0] - hem_cx))
    a_hem_r = math.degrees(math.atan2(hem_r[1] - hem_cy, hem_r[0] - hem_cx))
    add_arc(primary, hem_cx, hem_cy, hem_rad, a_hem_l, a_hem_r)

    # Connected shoulder slopes from neck cowl to hem corners
    sh_l_mid = (-44.0, 31.0)
    sh_r_mid = (44.0, 30.0)
    add_arc_pts(primary, (-20.0, 20.5), sh_l_mid, 2.2)
    add_line(primary, sh_l_mid[0], sh_l_mid[1], hem_l[0], hem_l[1])
    add_arc_pts(primary, (21.0, 20.5), sh_r_mid, -2.2)
    add_line(primary, sh_r_mid[0], sh_r_mid[1], hem_r[0], hem_r[1])

    # Capelet center seam & drapery folds (ending cleanly on capelet hem)
    for (sx, sy), (ex, ey) in [
        ((1.5, 27.5), (9.0, 56.0)),
        ((-13.0, 25.5), (-20.0, 56.0)),
        ((-27.0, 24.5), (-38.0, 58.0)),
        ((-40.0, 30.0), (-53.0, 60.0)),
        ((16.0, 25.5), (24.0, 56.0)),
        ((29.0, 24.5), (41.0, 58.0)),
        ((41.0, 29.5), (55.0, 60.0)),
    ]:
        hx, hy = _line_circle_y(sx, sy, ex, ey, hem_cx, hem_cy, hem_rad)
        add_line(detail, sx, sy, hx, hy)

    # Lower habit folds below capelet (starting cleanly on capelet hem, clipped to MED_R)
    for layer_ref, (sx, sy), (ex, ey) in [
        (primary, (-52.0, 54.0), (-59.0, 86.0)),
        (primary, (-35.0, 52.0), (-39.0, 86.0)),
        (primary, (37.0, 52.0), (42.0, 86.0)),
        (primary, (54.0, 54.0), (62.0, 86.0)),
        (detail, (-20.0, 50.0), (-23.0, 86.0)),
        (detail, (-7.0, 50.0), (-8.5, 86.0)),
        (detail, (9.0, 50.0), (11.0, 86.0)),
        (detail, (22.0, 50.0), (25.0, 86.0)),
    ]:
        hx, hy = _line_circle_y(sx, sy, ex, ey, hem_cx, hem_cy, hem_rad)
        add_line(layer_ref, hx, hy, ex, ey)

    return {
        "scaffold": scaffold,
        "golden": golden,
        "detail": detail,
        "primary": primary,
    }


def build_pacioli_svg(theme: str = "dark") -> str:
    """Build the complete Fra Luca Pacioli medallion SVG for ``'dark'`` or ``'light'`` theme."""
    return render_medallion_svg(build_pacioli_elements(), theme=theme)


def write_pacioli_svgs(output_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``pacioli_dark.svg`` and ``pacioli_light.svg`` to ``output_dir``."""
    target_dir = output_dir or DEFAULT_OUTPUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "pacioli_dark.svg"
    light_path = target_dir / "pacioli_light.svg"
    dark_path.write_text(build_pacioli_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_pacioli_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
