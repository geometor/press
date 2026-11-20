"""Study 38: Menelaus of Alexandria — Pure Sacred Geometric Emblem Medallion.

Unites both foundational breakthroughs of Menelaus's *Sphaerica* (c. 100 CE):

1. **Celestial Sphere & Spherical Triangle**: An astrolabe-framed stereographic
   celestial sphere (``R = 68``) centered at ``(0, -8)`` bearing an oblique
   meridian-and-parallel web and a sculpted spherical triangle ``ABC`` bounded
   by three exact stereographic great-circle arcs passing through antipodal
   points on the sphere limb.
2. **Planar & Spherical Menelaus Theorem**: Inscribed on the exact same
   vertices ``A, B, C``, the straight chordal triangle ``ABC`` with side ``BC``
   extended to external point ``F`` is crossed by the luminous golden Menelaus
   transversal ``D-E-F`` cutting internal side ``AB`` at ``D``, internal side
   ``AC`` at ``E``, and extended ``BC`` at ``F``, analytically verified so
   ``(|AD|/|DB|) * (|BF|/|FC|) * (|CE|/|EA|) = 1``. A companion stereographic
   great-circle transversal through ``(D, E)`` meets the extended great circle
   of ``BC`` at ``F_s``, illustrating the exact spherical-to-planar duality.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_menelaus_elements",
    "build_menelaus_svg",
    "write_menelaus_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _lerp(p1: Point, p2: Point, t: float) -> Point:
    """Linearly interpolate between ``p1`` (``t = 0``) and ``p2`` (``t = 1``)."""
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def _line_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Point:
    """Return the exact intersection of lines ``p1-p2`` and ``p3-p4``."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-12:
        msg = f"Parallel lines in _line_intersection: ({p1}, {p2}) and ({p3}, {p4})"
        raise ValueError(msg)
    det1 = x1 * y2 - y1 * x2
    det2 = x3 * y4 - y3 * x4
    px = (det1 * (x3 - x4) - (x1 - x2) * det2) / denom
    py = (det1 * (y3 - y4) - (y1 - y2) * det2) / denom
    return (px, py)


def _circumcircle(p1: Point, p2: Point, p3: Point) -> tuple[float, float, float]:
    """Return the exact circumcircle ``(cx, cy, r)`` through three non-collinear points."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-12:
        msg = f"Collinear points in _circumcircle: {p1}, {p2}, {p3}"
        raise ValueError(msg)
    a2 = ax * ax + ay * ay
    b2 = bx * bx + by * by
    c2 = cx * cx + cy * cy
    ux = (a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by)) / d
    uy = (a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax)) / d
    r = math.hypot(ax - ux, ay - uy)
    return (ux, uy, r)


def _stereographic_great_circle(
    p1: Point,
    p2: Point,
    ox: float,
    oy: float,
    r_sphere: float,
) -> tuple[float, float, float]:
    """Return the unique stereographic great circle ``(cx, cy, r)`` through ``p1`` and ``p2``.

    In stereographic projection onto a disk of radius ``r_sphere`` centered at
    ``(ox, oy)``, a circle represents a great circle on the sphere if and only if
    its power with respect to ``(ox, oy)`` equals ``-r_sphere**2`` (equivalently,
    it passes through antipodal points on the boundary circle and through the
    anti-inversion ``p1* = O - (r_sphere**2 / |p1 - O|^2) * (p1 - O)``).
    """
    dx1, dy1 = p1[0] - ox, p1[1] - oy
    d1_sq = dx1 * dx1 + dy1 * dy1
    if d1_sq < 1e-9:
        dx1, dy1 = p2[0] - ox, p2[1] - oy
        d1_sq = dx1 * dx1 + dy1 * dy1
    scale = -(r_sphere * r_sphere) / d1_sq
    p_anti = (ox + scale * dx1, oy + scale * dy1)
    cx, cy, r = _circumcircle(p1, p2, p_anti)
    # Exact stereographic great-circle invariant: |C - O|^2 - r^2 == -R^2
    power = (cx - ox) ** 2 + (cy - oy) ** 2 - r * r
    if abs(power + r_sphere * r_sphere) > 1e-4:
        msg = f"Great-circle power check failed: {power} != {-r_sphere * r_sphere}"
        raise ValueError(msg)
    return (cx, cy, r)


def _circle_circle_intersections(
    c1x: float,
    c1y: float,
    r1: float,
    c2x: float,
    c2y: float,
    r2: float,
) -> list[Point]:
    """Return the exact intersection points of two circles."""
    dx, dy = c2x - c1x, c2y - c1y
    d = math.hypot(dx, dy)
    if d < 1e-9 or d > r1 + r2 + 1e-9 or d < abs(r1 - r2) - 1e-9:
        return []
    a = (r1 * r1 - r2 * r2 + d * d) / (2.0 * d)
    h_sq = max(0.0, r1 * r1 - a * a)
    h = math.sqrt(h_sq)
    mx = c1x + a * dx / d
    my = c1y + a * dy / d
    if h < 1e-9:
        return [(mx, my)]
    rx = -dy * h / d
    ry = dx * h / d
    return [(mx + rx, my + ry), (mx - rx, my - ry)]


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
        msg = "Line does not intersect sphere boundary"
        raise ValueError(msg)
    s = math.sqrt(disc)
    t1 = (-b - s) / (2.0 * a)
    t2 = (-b + s) / (2.0 * a)
    return ((p1[0] + t1 * dx, p1[1] + t1 * dy), (p1[0] + t2 * dx, p1[1] + t2 * dy))


def _angle_deg(cx: float, cy: float, pt: Point) -> float:
    """Return the angle in degrees of ``pt`` relative to ``(cx, cy)``."""
    return math.degrees(math.atan2(pt[1] - cy, pt[0] - cx))


def _add_scaffold(mb: MedallionBuilder) -> None:
    """Add medallion-centered sacred scaffold rings, crosshairs, and outer ticks."""
    mb.add_circle("scaffold", MED_CX, MED_CY, MED_R, clip=False)
    for r in (78.0, 52.0, 26.0):
        mb.add_circle("scaffold", MED_CX, MED_CY, r)
    # Cardinal crosshairs through medallion center
    mb.add_line("scaffold", MED_CX, MED_CY - MED_R, MED_CX, MED_CY + MED_R)
    mb.add_line("scaffold", MED_CX - MED_R, MED_CY, MED_CX + MED_R, MED_CY)
    # Subtle 45-degree diagonal axes extending between R=78 and R=92
    for deg in (45.0, 135.0, 225.0, 315.0):
        p_in = polar(MED_CX, MED_CY, 78.0, deg)
        p_out = polar(MED_CX, MED_CY, MED_R, deg)
        mb.add_line("scaffold", p_in[0], p_in[1], p_out[0], p_out[1])


def _add_astrolabe_sphere_and_web(mb: MedallionBuilder, r_sphere: float) -> None:
    """Draw the celestial sphere limb, calibrated astrolabe bezel, and tilted spherical web."""
    ox, oy = MED_CX, MED_CY
    r_bezel = r_sphere + 4.8

    # Bold outer sphere limb & fine astrolabe bezel ring
    mb.add_circle("primary", ox, oy, r_sphere)
    mb.add_circle("detail", ox, oy, r_bezel)

    # 36 astrolabe degree ticks (every 10 deg; emphasized every 30 deg & cardinal)
    for k in range(36):
        deg = float(k * 10)
        if k % 9 == 0:
            p1 = polar(ox, oy, r_sphere, deg)
            p2 = polar(ox, oy, r_bezel + 3.2, deg)
            mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
            tip = polar(ox, oy, r_bezel + 4.8, deg)
            mb.add_circle("golden", tip[0], tip[1], 1.15, filled=True)
        elif k % 3 == 0:
            p1 = polar(ox, oy, r_sphere, deg)
            p2 = polar(ox, oy, r_bezel + 1.4, deg)
            mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])
        else:
            p1 = polar(ox, oy, r_sphere + 1.1, deg)
            p2 = polar(ox, oy, r_bezel, deg)
            mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])

    # Atmospheric oblique meridian & parallel web rendered softly on scaffold
    # so the primary spherical triangle and golden transversal command the eye.
    tilt_deg = -16.0
    north_deg = -90.0 + tilt_deg
    south_deg = 90.0 + tilt_deg
    p_north = polar(ox, oy, r_sphere, north_deg)
    p_south = polar(ox, oy, r_sphere, south_deg)

    mb.add_line("scaffold", p_north[0], p_north[1], p_south[0], p_south[1])
    eq_w = polar(ox, oy, r_sphere, tilt_deg + 180.0)
    eq_e = polar(ox, oy, r_sphere, tilt_deg)
    mb.add_line("scaffold", eq_w[0], eq_w[1], eq_e[0], eq_e[1])

    # Two symmetric tilted meridians (exact stereographic great circles through N & S poles)
    tilt_rad = math.radians(tilt_deg)
    ex, ey = math.cos(tilt_rad), math.sin(tilt_rad)
    for frac in (-0.48, 0.48):
        mid_pt = (ox + frac * r_sphere * ex, oy + frac * r_sphere * ey)
        gcx, gcy, gr = _circumcircle(p_north, p_south, mid_pt)
        a1 = _angle_deg(gcx, gcy, p_north)
        a2 = _angle_deg(gcx, gcy, p_south)
        mb.add_arc("scaffold", gcx, gcy, gr, a1, a2)

    # Exact orthogonal stereographic parallels (latitude circles +/-38 deg)
    nx, ny = math.cos(math.radians(north_deg)), math.sin(math.radians(north_deg))
    for lat_deg in (-38.0, 38.0):
        lat_rad = math.radians(abs(lat_deg))
        sign = 1.0 if lat_deg > 0 else -1.0
        dist_c = r_sphere / math.sin(lat_rad)
        rad_p = r_sphere / math.tan(lat_rad)
        pcx = ox + sign * dist_c * nx
        pcy = oy + sign * dist_c * ny
        hits = _circle_circle_intersections(ox, oy, r_sphere, pcx, pcy, rad_p)
        if len(hits) == 2:
            a1 = _angle_deg(pcx, pcy, hits[0])
            a2 = _angle_deg(pcx, pcy, hits[1])
            mb.add_arc("scaffold", pcx, pcy, rad_p, a1, a2)


def _add_ratio_tick(mb: MedallionBuilder, p1: Point, p2: Point, count: int) -> None:
    """Add ``count`` crisp perpendicular golden ratio ticks centered on segment ``p1-p2``."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    seg_len = math.hypot(dx, dy)
    if seg_len < 1e-6:
        return
    ux, uy = dx / seg_len, dy / seg_len
    nx, ny = -uy, ux
    mx, my = 0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1])
    spacing = 2.4
    half_tick = 2.0
    offset0 = -0.5 * (count - 1) * spacing
    for k in range(count):
        s = offset0 + k * spacing
        cx = mx + s * ux
        cy = my + s * uy
        mb.add_line(
            "golden",
            cx - half_tick * nx,
            cy - half_tick * ny,
            cx + half_tick * nx,
            cy + half_tick * ny,
        )


def build_menelaus_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Menelaus of Alexandria.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_sphere = 68.0

    _add_scaffold(mb)
    _add_astrolabe_sphere_and_web(mb, r_sphere)

    # ------------------------------------------------------------------
    # 1. Exact Triangle ABC & Planar Menelaus Configuration (D, E, F)
    # ------------------------------------------------------------------
    # Vertices balanced so O=(0,-8) sits comfortably inside ABC (giving all
    # three spherical triangle sides graceful outward curvature) while external
    # point F sits cleanly 13+ units inside the sphere limb R = 68.
    pt_a: Point = (-3.0, -52.0)
    pt_b: Point = (-45.0, 16.0)
    pt_c: Point = (19.0, 15.0)

    # External collinear point F on ray B -> C beyond C
    t_f = 1.48
    pt_f: Point = _lerp(pt_b, pt_c, t_f)
    if _dist(pt_f, (ox, oy)) >= r_sphere - 10.0:
        msg = f"External point F={pt_f} lacks breathing room inside sphere limb"
        raise ValueError(msg)

    # Internal point D on side AB, exact intersection E of transversal DF with AC
    t_d = 0.34
    pt_d: Point = _lerp(pt_a, pt_b, t_d)
    pt_e: Point = _line_intersection(pt_d, pt_f, pt_a, pt_c)

    # Analytical verification of Menelaus's Theorem:
    # (|AD| / |DB|) * (|BF| / |FC|) * (|CE| / |EA|) == 1.0 (signed product = -1)
    menelaus_prod = (
        (_dist(pt_a, pt_d) / _dist(pt_d, pt_b))
        * (_dist(pt_b, pt_f) / _dist(pt_f, pt_c))
        * (_dist(pt_c, pt_e) / _dist(pt_e, pt_a))
    )
    if abs(menelaus_prod - 1.0) > 1e-11:
        msg = f"Menelaus invariant violated: product = {menelaus_prod:.15f}"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Exact Sculpted Spherical Triangle ABC (3 Stereographic Great Circles)
    # ------------------------------------------------------------------
    great_circles: list[tuple[Point, Point, tuple[float, float, float]]] = []
    for p1, p2 in ((pt_a, pt_b), (pt_b, pt_c), (pt_c, pt_a)):
        gc = _stereographic_great_circle(p1, p2, ox, oy, r_sphere)
        great_circles.append((p1, p2, gc))
        gcx, gcy, gr = gc

        # Full great-circle continuation to antipodal points on R_sphere (detail)
        antipodes = _circle_circle_intersections(ox, oy, r_sphere, gcx, gcy, gr)
        if len(antipodes) == 2:
            a_u = _angle_deg(gcx, gcy, antipodes[0])
            a_v = _angle_deg(gcx, gcy, antipodes[1])
            mb.add_arc("detail", gcx, gcy, gr, a_u, a_v)
            for ap in antipodes:
                mb.add_circle("detail", ap[0], ap[1], 1.55)

        # Highlighted sculpted spherical triangle side arc between vertices (primary)
        a1 = _angle_deg(gcx, gcy, p1)
        a2 = _angle_deg(gcx, gcy, p2)
        mb.add_arc("primary", gcx, gcy, gr, a1, a2)

    # ------------------------------------------------------------------
    # 3. Spherical-to-Planar Menelaus Duality (4th Great Circle through D & E)
    # ------------------------------------------------------------------
    gc_de = _stereographic_great_circle(pt_d, pt_e, ox, oy, r_sphere)
    gc_bc = great_circles[1][2]
    de_antipodes = _circle_circle_intersections(ox, oy, r_sphere, gc_de[0], gc_de[1], gc_de[2])
    if len(de_antipodes) == 2:
        mb.add_arc(
            "detail",
            gc_de[0],
            gc_de[1],
            gc_de[2],
            _angle_deg(gc_de[0], gc_de[1], de_antipodes[0]),
            _angle_deg(gc_de[0], gc_de[1], de_antipodes[1]),
        )
    # Exact spherical Menelaus intersection F_s inside the sphere
    fs_hits = _circle_circle_intersections(
        gc_de[0], gc_de[1], gc_de[2], gc_bc[0], gc_bc[1], gc_bc[2]
    )
    fs_inside = [pt for pt in fs_hits if _dist(pt, (ox, oy)) <= r_sphere + 0.5]
    if fs_inside:
        pt_fs = fs_inside[0]
        mb.add_arc(
            "golden",
            gc_de[0],
            gc_de[1],
            gc_de[2],
            _angle_deg(gc_de[0], gc_de[1], pt_d),
            _angle_deg(gc_de[0], gc_de[1], pt_fs),
        )
        mb.add_circle("golden", pt_fs[0], pt_fs[1], 2.2)
        mb.add_circle("golden", pt_fs[0], pt_fs[1], 0.95, filled=True)
        mb.add_line("detail", pt_f[0], pt_f[1], pt_fs[0], pt_fs[1])

    # ------------------------------------------------------------------
    # 4. Planar Menelaus Triangle ABC, Extended Side BC->F, & Golden Transversal
    # ------------------------------------------------------------------
    # Core planar triangle ABC in bold primary
    mb.add_line("primary", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("primary", pt_c[0], pt_c[1], pt_a[0], pt_a[1])

    # Extended side C -> F in primary, continuing softly to sphere limb in detail
    mb.add_line("primary", pt_c[0], pt_c[1], pt_f[0], pt_f[1])
    bc_limb_1, bc_limb_2 = _line_circle_intersections(pt_b, pt_c, ox, oy, r_sphere)
    mb.add_line("detail", bc_limb_1[0], bc_limb_1[1], pt_b[0], pt_b[1])
    mb.add_line("detail", pt_f[0], pt_f[1], bc_limb_2[0], bc_limb_2[1])

    # Luminous golden Menelaus Transversal Line D-E-F spanning the sphere chord
    tr_limb_1, tr_limb_2 = _line_circle_intersections(pt_d, pt_f, ox, oy, r_sphere)
    mb.add_line("golden", tr_limb_1[0], tr_limb_1[1], tr_limb_2[0], tr_limb_2[1])
    mb.add_circle("golden", tr_limb_1[0], tr_limb_1[1], 1.45)
    mb.add_circle("golden", tr_limb_2[0], tr_limb_2[1], 1.45)

    # ------------------------------------------------------------------
    # 5. Compass Ratio Construction Arcs, Ratio Ticks, & Luminous Nodes
    # ------------------------------------------------------------------
    for center, target, half_sweep in (
        (pt_a, pt_d, 13.0),
        (pt_a, pt_e, 13.0),
        (pt_b, pt_d, 10.0),
        (pt_c, pt_e, 14.0),
        (pt_c, pt_f, 12.0),
    ):
        rad = _dist(center, target)
        ang = _angle_deg(center[0], center[1], target)
        mb.add_arc("detail", center[0], center[1], rad, ang - half_sweep, ang + half_sweep)

    # Crisp golden ratio tick marks on the divided segments
    _add_ratio_tick(mb, pt_a, pt_d, 1)
    _add_ratio_tick(mb, pt_d, pt_b, 2)
    _add_ratio_tick(mb, pt_a, pt_e, 1)
    _add_ratio_tick(mb, pt_e, pt_c, 2)
    _add_ratio_tick(mb, pt_c, pt_f, 3)

    # Golden ringed triangle vertices A, B, C
    for vx, vy in (pt_a, pt_b, pt_c):
        mb.add_circle("golden", vx, vy, 3.8)
        mb.add_circle("golden", vx, vy, 2.0, filled=True)

    # Bold golden collinear Menelaus transversal nodes D, E, F
    for nx, ny in (pt_d, pt_e, pt_f):
        mb.add_circle("golden", nx, ny, 4.4)
        mb.add_circle("golden", nx, ny, 2.5, filled=True)

    # Subtle center pole jewel at (0, -8)
    mb.add_circle("detail", ox, oy, 2.0)
    mb.add_circle("golden", ox, oy, 0.9, filled=True)

    return mb.build()


def build_menelaus_svg(theme: str = "dark") -> str:
    """Render the Menelaus of Alexandria medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_menelaus_elements()
    return render_medallion_svg(layers, theme=theme)


def write_menelaus_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``menelaus_dark.svg`` and ``menelaus_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "menelaus_dark.svg"
    light_path = target_dir / "menelaus_light.svg"
    dark_path.write_text(build_menelaus_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_menelaus_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
