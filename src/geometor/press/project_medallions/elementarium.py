"""Project Medallion: Elementarium (geometor/elementarium) — Passive Optical Archive.

Carves a zero-context Universal Geometric Primer Disc evoking a Voyager/Pioneer
stone-and-gold optical calibration tablet inside the unified ``R = 68``
graduated astrolabe seal:

1. **Central *Vesica Piscis* Core Chamber (``R_0 = 14.2``)**: Twin congruent
   circles (``r = 9.2``) cradling the genesis equilateral seed diamond inside
   the innermost calibration ring.
2. **Exact Tangent-Nested ``3, 4, 5, 6``-Gon Optical Rings**: Each regular
   polygon is simultaneously circumscribed tangent to the previous ring and
   inscribed in the next via exact secant progression:
   ``R_0 = 14.2 -> R_1 = R_0 * sec(60 deg) -> R_2 = R_1 * sec(45 deg) ->
   R_3 = R_2 * sec(36 deg) -> R_4 = R_3 * sec(30 deg) = 57.32 < 68.0``
   (verified to ``< 1e-12`` for exact circle-edge tangency at every tier).
3. **Voyager Optical Calibration Track (``R = 62.6``)**: Unary dot-bar glyph
   clusters (``3, 4, 5, 6`` encoded along the cardinal compass arcs) and crisp
   radial index ticks turn the rim into a self-decoding geometric primer.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_elementarium_elements",
    "build_elementarium_svg",
    "write_elementarium_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point = tuple[float, float]


def _dist_point_to_line(pt: Point, a: Point, b: Point) -> float:
    """Return the perpendicular distance from ``pt`` to infinite line ``a-b``."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    seg_len = math.hypot(dx, dy)
    if seg_len < 1e-12:
        return math.hypot(pt[0] - a[0], pt[1] - a[1])
    return abs((pt[0] - a[0]) * dy - (pt[1] - a[1]) * dx) / seg_len


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


def _add_polygon(mb: MedallionBuilder, layer: str, verts: list[Point]) -> None:
    """Draw a closed regular polygon connecting ``verts``."""
    n = len(verts)
    for k in range(n):
        p1 = verts[k]
        p2 = verts[(k + 1) % n]
        mb.add_line(layer, p1[0], p1[1], p2[0], p2[1])


def build_elementarium_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/elementarium``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    sqrt3 = math.sqrt(3.0)

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Keplerian Secant-Nested Radii for 3 -> 4 -> 5 -> 6 Polygons
    # ------------------------------------------------------------------
    r0 = 14.2
    r1 = r0 / math.cos(math.pi / 3.0)  # 28.40 (3-gon circumradius)
    r2 = r1 / math.cos(math.pi / 4.0)  # 40.16 (4-gon circumradius)
    r3 = r2 / math.cos(math.pi / 5.0)  # 49.64 (5-gon circumradius)
    r4 = r3 / math.cos(math.pi / 6.0)  # 57.32 (6-gon circumradius)
    r_track = 62.6

    poly3: list[Point] = [polar(ox, oy, r1, -90.0 + 120.0 * k) for k in range(3)]
    poly4: list[Point] = [polar(ox, oy, r2, -45.0 + 90.0 * k) for k in range(4)]
    poly5: list[Point] = [polar(ox, oy, r3, -90.0 + 72.0 * k) for k in range(5)]
    poly6: list[Point] = [polar(ox, oy, r4, -90.0 + 60.0 * k) for k in range(6)]

    # Verify exact circle-polygon tangency at every nested level to machine precision
    for r_in, verts in ((r0, poly3), (r1, poly4), (r2, poly5), (r3, poly6)):
        inradius = _dist_point_to_line((ox, oy), verts[0], verts[1])
        if abs(inradius - r_in) > 1e-11:
            msg = f"Nested polygon tangency invariant violated: {inradius:.12f} != {r_in:.12f}"
            raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Concentric Optical Calibration Disc Rings & Radial Pulse Ticks
    # ------------------------------------------------------------------
    for r_ring in (r0, r1, r2, r3, r4):
        mb.add_circle("detail", ox, oy, r_ring)

    # Outer Voyager optical track ring (4 segmented calibration arcs + unary glyphs)
    for base_deg in (-90.0, 0.0, 90.0, 180.0):
        mb.add_arc("detail", ox, oy, r_track, base_deg + 16.0, base_deg + 74.0)

    # Four unary numeric glyph clusters encoding 3 (N), 4 (E), 5 (S), 6 (W)
    for count, center_deg in ((3, -90.0), (4, 0.0), (5, 90.0), (6, 180.0)):
        step_deg = 4.2
        start_deg = center_deg - 0.5 * (count - 1) * step_deg
        for idx in range(count):
            ang = start_deg + idx * step_deg
            dot = polar(ox, oy, r_track, ang)
            mb.add_circle("golden", dot[0], dot[1], 1.15, filled=True)
            t_in = polar(ox, oy, r_track - 2.8, ang)
            t_out = polar(ox, oy, r_track - 1.5, ang)
            mb.add_line("detail", t_in[0], t_in[1], t_out[0], t_out[1])

    # Subtle radial optical index ticks bridging R_4 to R_track every 15 degrees
    for k in range(24):
        deg = float(k * 15)
        if k % 6 == 0:
            continue
        p_in = polar(ox, oy, r4, deg)
        p_out = polar(ox, oy, r4 + 2.6, deg)
        mb.add_line("detail", p_in[0], p_in[1], p_out[0], p_out[1])

    # ------------------------------------------------------------------
    # 3. Central Vesica Piscis Core Chamber (Inside R_0 = 14.2)
    # ------------------------------------------------------------------
    r_v = 9.0
    v_l: Point = (ox - 0.5 * r_v, oy)
    v_r: Point = (ox + 0.5 * r_v, oy)
    v_top: Point = (ox, oy - 0.5 * r_v * sqrt3)
    v_bot: Point = (ox, oy + 0.5 * r_v * sqrt3)

    mb.add_circle("primary", v_l[0], v_l[1], r_v)
    mb.add_circle("primary", v_r[0], v_r[1], r_v)
    mb.add_line("golden", v_l[0], v_l[1], v_r[0], v_r[1])
    mb.add_line("golden", v_top[0], v_top[1], v_bot[0], v_bot[1])
    mb.add_line("golden", v_l[0], v_l[1], v_top[0], v_top[1])
    mb.add_line("golden", v_top[0], v_top[1], v_r[0], v_r[1])
    mb.add_line("golden", v_r[0], v_r[1], v_bot[0], v_bot[1])
    mb.add_line("golden", v_bot[0], v_bot[1], v_l[0], v_l[1])

    # ------------------------------------------------------------------
    # 4. Nested 3, 4, 5, 6-Gon Optical Tracks (Alternating Primary & Golden)
    # ------------------------------------------------------------------
    _add_polygon(mb, "golden", poly3)
    _add_polygon(mb, "primary", poly4)
    _add_polygon(mb, "golden", poly5)
    _add_polygon(mb, "primary", poly6)

    # Tangency contact ticks & golden vertex nodes across all four polygon tiers
    for verts, r_node in ((poly3, 2.6), (poly4, 2.5), (poly5, 2.7), (poly6, 2.9)):
        for vx, vy in verts:
            mb.add_circle("golden", vx, vy, r_node)
            mb.add_circle("golden", vx, vy, 0.5 * r_node, filled=True)

    # Central Vesica foci jewels
    for pt in (v_l, v_r, v_top, v_bot):
        mb.add_circle("golden", pt[0], pt[1], 1.25, filled=True)
    mb.add_circle("golden", ox, oy, 1.6, filled=True)

    return mb.build()


def build_elementarium_svg(theme: str = "dark") -> str:
    """Render the ``geometor/elementarium`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_elementarium_elements()
    return render_medallion_svg(layers, theme=theme)


def write_elementarium_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``elementarium_dark.svg`` and ``elementarium_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "elementarium_dark.svg"
    light_path = target_dir / "elementarium_light.svg"
    dark_path.write_text(build_elementarium_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_elementarium_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
