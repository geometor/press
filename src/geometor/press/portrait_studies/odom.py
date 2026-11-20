"""Study 46: George Odom — Pure Sacred Geometric Emblem Medallion.

Celebrates George Odom (1941-2010), polyhedral sculptor and discoverer of the
most minimal Golden Section construction in all of Euclidean geometry
(*American Mathematical Monthly* E3007, 1983), framed within the unified
``R = 68`` graduated astrolabe seal:

1. **Equilateral Triangle ``PQR`` & Circumcircle ``(O, R_c = 55)``**: Upright
   equilateral triangle inscribed in its bold primary circumcircle centered at
   ``(0, -8)``, accompanied by its exact ``4 : 2 : 1`` octave-nested incircle
   (``R_c / 2``) and medial incircle (``R_c / 4``), compass-construction arcs
   from ``P, Q, R`` locating exact side midpoints ``A, B, M``, and the two
   3-fold symmetric sister Odom chords forming the 6-pointed Star of Odom.
2. **Heroic Golden Midpoint-Chord ``D-A-B-C``**: Extending segment ``AB``
   (joining midpoints of ``PQ`` and ``PR``) horizontally to cut the
   circumcircle at ``D`` and ``C`` produces the exact golden division
   ``|AB|/|BC| = |AC|/|AB| = |AB|/|DA| = |DB|/|AB| = phi`` and
   ``|DC|/|AB| = sqrt(5)`` (verified to ``< 1e-12``), crowned by four radiant
   double-ringed golden stars at ``D, A, B, C`` and golden ratio transfer arcs.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_odom_elements",
    "build_odom_svg",
    "write_odom_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _mid(p1: Point, p2: Point) -> Point:
    """Return the midpoint of ``p1`` and ``p2``."""
    return (0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1]))


def _angle_deg(cx: float, cy: float, pt: Point) -> float:
    """Return the angle in degrees of ``pt`` relative to ``(cx, cy)``."""
    return math.degrees(math.atan2(pt[1] - cy, pt[0] - cx))


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
        msg = "Chord line does not intersect circumcircle"
        raise ValueError(msg)
    s = math.sqrt(disc)
    t1 = (-b - s) / (2.0 * a)
    t2 = (-b + s) / (2.0 * a)
    return ((p1[0] + t1 * dx, p1[1] + t1 * dy), (p1[0] + t2 * dx, p1[1] + t2 * dy))


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


def _add_ratio_tick(mb: MedallionBuilder, p1: Point, p2: Point, count: int) -> None:
    """Add ``count`` crisp perpendicular golden ratio ticks centered on segment ``p1-p2``."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    seg_len = math.hypot(dx, dy)
    if seg_len < 1e-6:
        return
    ux, uy = dx / seg_len, dy / seg_len
    nx, ny = -uy, ux
    mx, my = 0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1])
    spacing = 2.5
    half_tick = 2.2
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


def build_odom_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for George Odom.

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
    # 1. Exact Equilateral Triangle PQR, Circumcircle (O, R_c), & Midpoints
    # ------------------------------------------------------------------
    r_c = 55.0  # Bold primary circumcircle with 13-unit celestial halo inside R_seal = 68
    pt_p = polar(ox, oy, r_c, -90.0)
    pt_q = polar(ox, oy, r_c, 150.0)
    pt_r = polar(ox, oy, r_c, 30.0)

    pt_a = _mid(pt_p, pt_q)  # Left midpoint
    pt_b = _mid(pt_p, pt_r)  # Right midpoint
    pt_m = _mid(pt_q, pt_r)  # Base midpoint

    # Exact Odom horizontal midpoint chord D--A--B--C cutting circumcircle (O, R_c)
    pt_d, pt_c = _line_circle_intersections(pt_a, pt_b, ox, oy, r_c)

    # Analytical verification of Odom's Golden Section Theorem (E3007):
    # |AB|/|BC| == |AC|/|AB| == |AB|/|DA| == |DB|/|AB| == phi, |DC|/|AB| == sqrt(5)
    ab_len = _dist(pt_a, pt_b)
    bc_len = _dist(pt_b, pt_c)
    da_len = _dist(pt_d, pt_a)
    ac_len = _dist(pt_a, pt_c)
    db_len = _dist(pt_d, pt_b)
    dc_len = _dist(pt_d, pt_c)
    for ratio_val in (ab_len / bc_len, ac_len / ab_len, ab_len / da_len, db_len / ab_len):
        if abs(ratio_val - phi) > 1e-12:
            msg = f"Odom golden section invariant violated: {ratio_val:.15f} != {phi:.15f}"
            raise ValueError(msg)
    if abs((dc_len / ab_len) - sqrt5) > 1e-12:
        msg = f"Odom sqrt(5) full-chord invariant violated: {dc_len / ab_len:.15f}"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Octave-Nested Incircle (R_c/2), Medial Incircle (R_c/4), & Compass Arcs
    # ------------------------------------------------------------------
    mb.add_circle("detail", ox, oy, 0.5 * r_c)  # Incircle of PQR / circumcircle of ABM
    mb.add_circle("detail", ox, oy, 0.25 * r_c)  # Incircle of medial triangle ABM

    # Self-proving compass construction arcs from P, Q, R sweeping across midpoints A, B, M
    half_side = 0.5 * _dist(pt_p, pt_q)
    for vertex, m1, m2 in ((pt_p, pt_a, pt_b), (pt_q, pt_a, pt_m), (pt_r, pt_b, pt_m)):
        for mid_pt in (m1, m2):
            ang = _angle_deg(vertex[0], vertex[1], mid_pt)
            mb.add_arc("detail", vertex[0], vertex[1], half_side, ang - 7.5, ang + 7.5)

    # Two 3-fold symmetric sister Odom golden chords (through AM and BM) in crisp detail,
    # forming the complete 6-pointed Star of Odom with golden rim jewels!
    sister_rim_pts: list[Point] = []
    for m1, m2 in ((pt_a, pt_m), (pt_b, pt_m)):
        s1, s2 = _line_circle_intersections(m1, m2, ox, oy, r_c)
        # Verify exact 3-fold Odom golden wing symmetry (|s1 - m1| == |DA| == |BC|)
        d_wing = min(_dist(s1, m1), _dist(s2, m1))
        if abs(d_wing - da_len) > 1e-11:
            msg = f"3-fold Odom wing symmetry violated: {d_wing:.12f} != {da_len:.12f}"
            raise ValueError(msg)
        mb.add_line("detail", s1[0], s1[1], s2[0], s2[1])
        sister_rim_pts.extend((s1, s2))

    # ------------------------------------------------------------------
    # 3. Bold Primary Odom Circumcircle & Upright Equilateral Triangle PQR
    # ------------------------------------------------------------------
    mb.add_circle("primary", ox, oy, r_c)
    mb.add_line("primary", pt_p[0], pt_p[1], pt_q[0], pt_q[1])
    mb.add_line("primary", pt_q[0], pt_q[1], pt_r[0], pt_r[1])
    mb.add_line("primary", pt_r[0], pt_r[1], pt_p[0], pt_p[1])

    # ------------------------------------------------------------------
    # 4. Luminous Golden Odom Chord D--A--B--C, Ratio Transfer Arcs, & Stars
    # ------------------------------------------------------------------
    mb.add_line("golden", pt_d[0], pt_d[1], pt_c[0], pt_c[1])

    # Delicate golden ratio transfer arcs centered at A (r = DA) and B (r = BC)
    # swinging the outer golden wing segments onto the interior segment AB
    mb.add_arc("golden", pt_a[0], pt_a[1], da_len, 180.0, 270.0)
    mb.add_arc("golden", pt_a[0], pt_a[1], da_len, 270.0, 360.0)
    mb.add_arc("golden", pt_b[0], pt_b[1], bc_len, 180.0, 270.0)
    mb.add_arc("golden", pt_b[0], pt_b[1], bc_len, 270.0, 360.0)

    # Golden ratio tick notches illustrating DA : AB : BC = 1/phi : 1 : 1/phi
    _add_ratio_tick(mb, pt_d, pt_a, 1)
    _add_ratio_tick(mb, pt_a, pt_b, 2)
    _add_ratio_tick(mb, pt_b, pt_c, 1)

    # Crisp golden interior transfer cuts G_A and G_B where arcs meet AB
    pt_ga: Point = (pt_a[0] + da_len, pt_a[1])
    pt_gb: Point = (pt_b[0] - bc_len, pt_b[1])
    mb.add_circle("golden", pt_ga[0], pt_ga[1], 1.5, filled=True)
    mb.add_circle("golden", pt_gb[0], pt_gb[1], 1.5, filled=True)

    # Ringed triangle vertices P, Q, R and third midpoint M
    for vx, vy in (pt_p, pt_q, pt_r):
        mb.add_circle("golden", vx, vy, 3.5)
        mb.add_circle("golden", vx, vy, 1.8, filled=True)
    mb.add_circle("golden", pt_m[0], pt_m[1], 2.5)
    mb.add_circle("golden", pt_m[0], pt_m[1], 1.25, filled=True)

    # Crisp golden rim jewels at the 4 symmetric Star-of-Odom circumcircle hits
    for rx, ry in sister_rim_pts:
        mb.add_circle("golden", rx, ry, 2.3)
        mb.add_circle("golden", rx, ry, 1.15, filled=True)

    # Four radiant double-ringed golden stars at hero Odom nodes D, A, B, C
    for sx_pt, sy_pt in (pt_d, pt_a, pt_b, pt_c):
        mb.add_circle("golden", sx_pt, sy_pt, 4.3)
        mb.add_circle("golden", sx_pt, sy_pt, 2.3, filled=True)

    # Central symmetry jewel at O = (0, -8)
    mb.add_circle("golden", ox, oy, 2.8)
    mb.add_circle("golden", ox, oy, 1.35, filled=True)

    return mb.build()


def build_odom_svg(theme: str = "dark") -> str:
    """Render the George Odom medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_odom_elements()
    return render_medallion_svg(layers, theme=theme)


def write_odom_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``odom_dark.svg`` and ``odom_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "odom_dark.svg"
    light_path = target_dir / "odom_light.svg"
    dark_path.write_text(build_odom_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_odom_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
