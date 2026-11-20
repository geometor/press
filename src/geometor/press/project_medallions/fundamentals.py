"""Project Medallion: Fundamentals (geometor/fundamentals) — Axiomatic Primer.

Presents the Classical Triad of elementary compass-and-straightedge
constructions inside the unified ``R = 68`` graduated astrolabe seal:

1. **Shared Circumcircle ``R = 54`` & Classical Polygon Triad**: Regular
   hexagon (``6``-gon), inscribed square (``4``-gon), and upright equilateral
   triangle (``3``-gon) all sharing one exact circumcircle centered at
   ``(0, -8)``.
2. **Perpendicular-Bisector & Seed-of-Life Compass Arcs**: Six compass-radius
   arcs centered on the hexagon vertices sweep through the center inside
   ``R = 54``, paired with orthogonal perpendicular-bisector axes and exact
   inscribed circles of the square (``R / sqrt(2)``) and triangle (``R / 2``).
3. **Golden Angle-Bisector Construction Arcs**: Exact paired angle-bisector
   compass arcs from the cardinal points locate the ``45 deg`` diagonals to
   the square vertices, uniting perpendicularity, bisection, and threefold,
   fourfold, and sixfold symmetry in one emblem.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_fundamentals_elements",
    "build_fundamentals_svg",
    "write_fundamentals_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _angle_deg(cx: float, cy: float, pt: Point) -> float:
    """Return the angle in degrees of ``pt`` relative to ``(cx, cy)``."""
    return math.degrees(math.atan2(pt[1] - cy, pt[0] - cx))


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
        msg = f"Compass arcs do not intersect cleanly: d={d:.6f}"
        raise ValueError(msg)
    a = (r1 * r1 - r2 * r2 + d * d) / (2.0 * d)
    h = math.sqrt(max(0.0, r1 * r1 - a * a))
    mx = c1[0] + a * dx / d
    my = c1[1] + a * dy / d
    rx = -dy * (h / d)
    ry = dx * (h / d)
    return ((mx + rx, my + ry), (mx - rx, my - ry))


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


def build_fundamentals_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/fundamentals``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Shared Circumcircle (R = 54) & Classical Triad Vertices
    # ------------------------------------------------------------------
    r_c = 54.0
    hex_verts: list[Point] = [polar(ox, oy, r_c, -90.0 + 60.0 * k) for k in range(6)]
    tri_verts: list[Point] = [hex_verts[0], hex_verts[2], hex_verts[4]]
    sq_verts: list[Point] = [polar(ox, oy, r_c, -45.0 + 90.0 * k) for k in range(4)]

    # Verify exact regular side-length invariants
    hex_side = _dist(hex_verts[0], hex_verts[1])
    sq_side = _dist(sq_verts[0], sq_verts[1])
    tri_side = _dist(tri_verts[0], tri_verts[1])
    if (
        abs(hex_side - r_c) > 1e-11
        or abs(sq_side - r_c * math.sqrt(2.0)) > 1e-11
        or abs(tri_side - r_c * math.sqrt(3.0)) > 1e-11
    ):
        msg = "Classical Triad regular polygon invariants violated"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Detail Layer: Perpendicular Bisectors, Incircles & Seed-of-Life Arcs
    # ------------------------------------------------------------------
    # Incircles of square (R / sqrt(2)) and equilateral triangle (R / 2)
    mb.add_circle("detail", ox, oy, r_c / math.sqrt(2.0))
    mb.add_circle("detail", ox, oy, 0.5 * r_c)

    # Orthogonal perpendicular-bisector diameters & 45 deg angle-bisector diagonals
    mb.add_line("detail", ox - r_c, oy, ox + r_c, oy)
    mb.add_line("detail", ox, oy - r_c, ox, oy + r_c)
    mb.add_line("detail", sq_verts[0][0], sq_verts[0][1], sq_verts[2][0], sq_verts[2][1])
    mb.add_line("detail", sq_verts[1][0], sq_verts[1][1], sq_verts[3][0], sq_verts[3][1])

    # Six compass-construction arcs (radius R_c) centered at each hexagon vertex
    # sweeping smoothly across the center between adjacent vertices (Seed of Life)
    for k in range(6):
        vx, vy = hex_verts[k]
        prev_v = hex_verts[(k - 1) % 6]
        next_v = hex_verts[(k + 1) % 6]
        a1 = _angle_deg(vx, vy, next_v)
        a2 = _angle_deg(vx, vy, prev_v)
        mb.add_arc("detail", vx, vy, r_c, a1, a2)

    # Exact perpendicular-bisector compass ticks locating the vertical & horizontal axes
    r_bis = 0.62 * r_c
    east_pt = polar(ox, oy, 0.5 * r_c, 0.0)
    west_pt = polar(ox, oy, 0.5 * r_c, 180.0)
    pb_top, pb_bot = _circle_circle_intersections(east_pt, r_bis, west_pt, r_bis)
    for ctr in (east_pt, west_pt):
        for target in (pb_top, pb_bot):
            ang = _angle_deg(ctr[0], ctr[1], target)
            mb.add_arc("detail", ctr[0], ctr[1], r_bis, ang - 11.0, ang + 11.0)

    # Crisp central right-angle square marking exact perpendicularity at O
    sq_tick = 4.2
    mb.add_line("detail", ox + sq_tick, oy, ox + sq_tick, oy - sq_tick)
    mb.add_line("detail", ox, oy - sq_tick, ox + sq_tick, oy - sq_tick)

    # ------------------------------------------------------------------
    # 3. Bold Primary Layer: Circumcircle, Regular Hexagon, & Inscribed Square
    # ------------------------------------------------------------------
    mb.add_circle("primary", ox, oy, r_c)

    for k in range(6):
        p_cur = hex_verts[k]
        p_nxt = hex_verts[(k + 1) % 6]
        mb.add_line("primary", p_cur[0], p_cur[1], p_nxt[0], p_nxt[1])

    for k in range(4):
        s_cur = sq_verts[k]
        s_nxt = sq_verts[(k + 1) % 4]
        mb.add_line("primary", s_cur[0], s_cur[1], s_nxt[0], s_nxt[1])

    # ------------------------------------------------------------------
    # 4. Luminous Golden Layer: Equilateral Triangle & Angle-Bisector Arcs
    # ------------------------------------------------------------------
    for k in range(3):
        t_cur = tri_verts[k]
        t_nxt = tri_verts[(k + 1) % 3]
        mb.add_line("golden", t_cur[0], t_cur[1], t_nxt[0], t_nxt[1])

    # Exact angle-bisector construction arcs from the 4 cardinal anchor points
    # on R/2 crossing cleanly on the 45 deg diagonals toward the square corners
    cardinals: list[Point] = [polar(ox, oy, 0.5 * r_c, -90.0 + 90.0 * k) for k in range(4)]
    r_ab = 0.42 * r_c
    for k in range(4):
        c_a = cardinals[k]
        c_b = cardinals[(k + 1) % 4]
        i1, i2 = _circle_circle_intersections(c_a, r_ab, c_b, r_ab)
        outer_bis = i1 if _dist((ox, oy), i1) > _dist((ox, oy), i2) else i2
        ang_a = _angle_deg(c_a[0], c_a[1], outer_bis)
        ang_b = _angle_deg(c_b[0], c_b[1], outer_bis)
        mb.add_arc("golden", c_a[0], c_a[1], r_ab, ang_a - 14.0, ang_a + 14.0)
        mb.add_arc("golden", c_b[0], c_b[1], r_ab, ang_b - 14.0, ang_b + 14.0)
        mb.add_circle("golden", outer_bis[0], outer_bis[1], 1.5, filled=True)

    # Double-ringed golden stars at the 3 equilateral triangle vertices
    for vx, vy in tri_verts:
        mb.add_circle("golden", vx, vy, 4.0)
        mb.add_circle("golden", vx, vy, 2.0, filled=True)

    # Ringed golden nodes at remaining hexagon vertices and square vertices
    for vx, vy in (hex_verts[1], hex_verts[3], hex_verts[5]):
        mb.add_circle("golden", vx, vy, 2.7)
        mb.add_circle("golden", vx, vy, 1.35, filled=True)

    for sx, sy in sq_verts:
        mb.add_circle("golden", sx, sy, 3.0)
        mb.add_circle("golden", sx, sy, 1.5, filled=True)

    # Central origin jewel
    mb.add_circle("golden", ox, oy, 3.2)
    mb.add_circle("golden", ox, oy, 1.55, filled=True)

    return mb.build()


def build_fundamentals_svg(theme: str = "dark") -> str:
    """Render the ``geometor/fundamentals`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_fundamentals_elements()
    return render_medallion_svg(layers, theme=theme)


def write_fundamentals_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``fundamentals_dark.svg`` and ``fundamentals_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "fundamentals_dark.svg"
    light_path = target_dir / "fundamentals_light.svg"
    dark_path.write_text(build_fundamentals_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_fundamentals_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
