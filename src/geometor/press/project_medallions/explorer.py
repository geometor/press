"""Project Medallion: Explorer (geometor/explorer) — Interactive SVG Workbench.

Frames an active golden circle-line intersection construction inside a
precision optical surveying reticle and interactive SVG workbench lens within
the unified ``R = 68`` graduated astrolabe seal:

1. **Calibrated Reticle Lens & Degree Ticks**: Concentric optical lens rings
   (``R = 56`` and ``R = 51``) graduated at ``0, 30, 45, 60, 90`` degrees across
   all four quadrants, paired with ruled Cartesian coordinate axes and corner
   viewfinder arc brackets.
2. **Active Circle-Line Intersection Construction**: Two intersecting
   construction circles pierced by a bold golden secant chord generating exact
   analytical circle-line (``I_1..I_4``) and circle-circle (``P_1, P_2``)
   intersection nodes (verified to ``< 1e-12``).
3. **Concentric Selection Target Rings**: Multi-ring optical target crosshairs
   lock onto the hero focus intersections, evoking interactive geometric
   inspection and live SVG coordinate telemetry.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_explorer_elements",
    "build_explorer_svg",
    "write_explorer_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _circle_circle_intersections(
    c1: Point,
    r1: float,
    c2: Point,
    r2: float,
) -> tuple[Point, Point]:
    """Return the two exact intersection points of circles ``(c1, r1)`` and ``(c2, r2)``."""
    dx = c2[0] - c1[0]
    dy = c2[1] - c1[1]
    d = math.hypot(dx, dy)
    if d < 1e-12 or d >= r1 + r2 or d <= abs(r1 - r2):
        msg = f"Circles do not intersect cleanly: d={d:.6f}"
        raise ValueError(msg)
    a = (r1 * r1 - r2 * r2 + d * d) / (2.0 * d)
    h = math.sqrt(max(0.0, r1 * r1 - a * a))
    mx = c1[0] + a * dx / d
    my = c1[1] + a * dy / d
    rx = -dy * (h / d)
    ry = dx * (h / d)
    return ((mx + rx, my + ry), (mx - rx, my - ry))


def _line_circle_intersections(
    p1: Point,
    p2: Point,
    cx: float,
    cy: float,
    r: float,
) -> tuple[Point, Point]:
    """Return the two intersections of infinite line ``p1-p2`` with circle ``(cx, cy, r)``."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    fx, fy = p1[0] - cx, p1[1] - cy
    a = dx * dx + dy * dy
    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - r * r
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        msg = "Secant line does not intersect target circle"
        raise ValueError(msg)
    s = math.sqrt(disc)
    t1 = (-b - s) / (2.0 * a)
    t2 = (-b + s) / (2.0 * a)
    return ((p1[0] + t1 * dx, p1[1] + t1 * dy), (p1[0] + t2 * dx, p1[1] + t2 * dy))


def _add_astrolabe_seal(mb: MedallionBuilder, r_seal: float) -> None:
    """Add the unified GEOMETOR Emblem Pantheon scaffold and graduated astrolabe seal."""
    ox, oy = MED_CX, MED_CY
    r_bezel = r_seal + 4.8

    mb.add_circle("scaffold", ox, oy, MED_R, clip=False)
    for r in (78.0, 52.0, 26.0):
        mb.add_circle("scaffold", ox, oy, r)
    mb.add_line("scaffold", ox, oy - MED_R, ox, oy + MED_R)
    mb.add_line("scaffold", ox - MED_R, oy, ox + MED_R, oy)
    for deg in (45.0, 135.0, 225.0, 315.0):
        p_in = polar(ox, oy, 78.0, deg)
        p_out = polar(ox, oy, MED_R, deg)
        mb.add_line("scaffold", p_in[0], p_in[1], p_out[0], p_out[1])

    mb.add_circle("primary", ox, oy, r_seal)
    mb.add_circle("detail", ox, oy, r_bezel)

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


def _add_selection_target(mb: MedallionBuilder, pt: Point, outer_r: float = 8.4) -> None:
    """Draw concentric golden interactive selection target rings with crosshair ticks."""
    cx, cy = pt
    mb.add_circle("golden", cx, cy, 2.0, filled=True)
    mb.add_circle("golden", cx, cy, 4.7)
    for deg in (20.0, 110.0, 200.0, 290.0):
        mb.add_arc("golden", cx, cy, outer_r, deg, deg + 50.0)
    for deg in (0.0, 90.0, 180.0, 270.0):
        p_in = polar(cx, cy, outer_r - 1.8, deg)
        p_out = polar(cx, cy, outer_r + 2.2, deg)
        mb.add_line("golden", p_in[0], p_in[1], p_out[0], p_out[1])


def build_explorer_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/explorer``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Calibrated Optical Reticle Lens & Graduated Coordinate Axes
    # ------------------------------------------------------------------
    r_lens = 56.0
    r_inner_scale = 51.0

    mb.add_circle("primary", ox, oy, r_lens)
    mb.add_circle("detail", ox, oy, r_inner_scale)

    # Degree ticks at 0, 30, 45, 60, 90 across all four quadrants (+ 15 deg minor ticks)
    key_angles = {0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330}
    for deg_i in range(0, 360, 15):
        deg = float(deg_i)
        if deg_i % 90 == 0:
            p1 = polar(ox, oy, r_inner_scale - 2.6, deg)
            p2 = polar(ox, oy, r_lens + 2.6, deg)
            mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
        elif deg_i in key_angles:
            p1 = polar(ox, oy, r_inner_scale - 0.8, deg)
            p2 = polar(ox, oy, r_lens, deg)
            mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])
        else:
            p1 = polar(ox, oy, r_inner_scale + 1.8, deg)
            p2 = polar(ox, oy, r_lens, deg)
            mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])

    # Four viewfinder corner arc brackets framing the reticle at 45/135/225/315 deg
    for center_deg in (45.0, 135.0, 225.0, 315.0):
        mb.add_arc("primary", ox, oy, r_lens + 4.8, center_deg - 10.0, center_deg + 10.0)

    # Graduated Cartesian crosshair axes inside the lens
    mb.add_line("detail", ox - r_lens, oy, ox + r_lens, oy)
    mb.add_line("detail", ox, oy - r_lens, ox, oy + r_lens)
    for step in (-40.0, -32.0, -24.0, -16.0, -8.0, 8.0, 16.0, 24.0, 32.0, 40.0):
        half_tick = 2.4 if (int(abs(step)) % 16 == 0) else 1.3
        mb.add_line("detail", ox + step, oy - half_tick, ox + step, oy + half_tick)
        mb.add_line("detail", ox - half_tick, oy + step, ox + half_tick, oy + step)

    # ------------------------------------------------------------------
    # 2. Active Circle-Line Intersection Construction inside the Lens
    # ------------------------------------------------------------------
    c1: Point = (ox - 10.0, oy + 5.0)
    r1 = 27.0
    c2: Point = (ox + 15.0, oy - 9.0)
    r2 = 23.0

    # Active golden secant passing cleanly across both circles
    sec_ref1: Point = (ox - 30.0, oy + 18.0)
    sec_ref2: Point = (ox + 30.0, oy - 16.0)
    sec_a, sec_b = _line_circle_intersections(sec_ref1, sec_ref2, ox, oy, r_lens)

    i1, i2 = _line_circle_intersections(sec_a, sec_b, c1[0], c1[1], r1)
    i3, i4 = _line_circle_intersections(sec_a, sec_b, c2[0], c2[1], r2)
    p1, p2 = _circle_circle_intersections(c1, r1, c2, r2)

    # Verify exact analytical incidences
    for pt, ctr, rad in (
        (i1, c1, r1),
        (i2, c1, r1),
        (i3, c2, r2),
        (i4, c2, r2),
        (p1, c1, r1),
        (p1, c2, r2),
        (p2, c1, r1),
        (p2, c2, r2),
    ):
        if abs(_dist(pt, ctr) - rad) > 1e-11:
            msg = "Explorer intersection incidence invariant violated"
            raise ValueError(msg)

    # Radical chord connecting circle-circle intersections P1 -- P2
    rad_a, rad_b = _line_circle_intersections(p1, p2, ox, oy, r_inner_scale)
    mb.add_line("detail", rad_a[0], rad_a[1], rad_b[0], rad_b[1])
    mb.add_line("detail", c1[0], c1[1], c2[0], c2[1])

    # Primary active circles
    mb.add_circle("primary", c1[0], c1[1], r1)
    mb.add_circle("primary", c2[0], c2[1], r2)

    # Active golden secant line & perpendicular projection drop from origin O
    mb.add_line("golden", sec_a[0], sec_a[1], sec_b[0], sec_b[1])

    # Pick the two opposite golden secant hits on C_1 for spacious concentric target rings
    p_top = p1 if p1[1] < p2[1] else p2
    p_bot = p2 if p1[1] < p2[1] else p1
    i_focus = i2 if i2[0] > i1[0] else i1
    i_other = i1 if i2[0] > i1[0] else i2

    _add_selection_target(mb, i_focus, outer_r=8.6)
    _add_selection_target(mb, i_other, outer_r=7.2)

    # Secondary golden nodes at remaining exact intersections and circle centers
    for node in (p_top, i3, i4, p_bot):
        mb.add_circle("golden", node[0], node[1], 3.0)
        mb.add_circle("golden", node[0], node[1], 1.5, filled=True)

    for ctr in (c1, c2):
        mb.add_circle("golden", ctr[0], ctr[1], 2.4)
        mb.add_circle("golden", ctr[0], ctr[1], 1.1, filled=True)

    # Central crosshair reticle origin jewel
    mb.add_circle("golden", ox, oy, 2.2)
    mb.add_circle("golden", ox, oy, 1.0, filled=True)

    return mb.build()


def build_explorer_svg(theme: str = "dark") -> str:
    """Render the ``geometor/explorer`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_explorer_elements()
    return render_medallion_svg(layers, theme=theme)


def write_explorer_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``explorer_dark.svg`` and ``explorer_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "explorer_dark.svg"
    light_path = target_dir / "explorer_light.svg"
    dark_path.write_text(build_explorer_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_explorer_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
