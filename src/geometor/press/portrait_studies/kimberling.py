"""Study 47: Clark Kimberling — Pure Sacred Geometric Emblem Medallion.

Celebrates Clark Kimberling (b. 1942), creator of the *Encyclopedia of Triangle
Centers* (``ETC``, ``X(1)`` through ``X(53,000+)``), uniting the foundational
**Classical Quartet of Triangle Centers** (``X(1)`` Incenter, ``X(2)`` Centroid,
``X(3)`` Circumcenter, ``X(4)`` Orthocenter) with ``X(5)`` Nine-Point Center,
``X(6)`` Symmedian Point, and ``X(11)`` Feuerbach Point inside the unified
``R = 68`` graduated astrolabe seal:

1. **Canonical Acute Scalene Triangle ``ABC`` & Circumcircle**: Inscribed in
   bold primary circumcircle ``(X(3), R_c = 54)`` centered at ``(0, -8)`` with
   strongly asymmetric acute angles (``29 deg, 64 deg, 87 deg``) tuned so every
   pair of the six featured centers is separated by ``> 7.2`` units.
2. **Four Foundational Center Systems**: Exact Incircle ``(X(1), r_in)`` with
   vertex angle-bisector arcs, subtle Medians concurring at ``X(2)``, crisp
   Altitudes concurring at ``X(4)`` with right-angle ticks, and the Nine-Point
   Circle ``(X(5), R_c / 2)`` kissing the Incircle internally at Feuerbach
   Point ``X(11)`` (verified ``|X(5)-X(1)| == R_9 - r_in`` to ``< 1e-11``).
3. **Blazing Golden Euler Line & Center Constellation**: Full rim-to-rim
   golden Euler Line analytically verified through ``X(3)-X(2)-X(5)-X(4)`` in
   exact ``2 : 1 : 3`` proportion (``< 1e-12``), linked by golden constellation
   axes to ``X(1)`` and ``X(6)`` with distinct radiant double-ringed stars
   crowning the Classical Quartet.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_kimberling_elements",
    "build_kimberling_svg",
    "write_kimberling_svgs",
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


def _project_to_line(pt: Point, a: Point, b: Point) -> Point:
    """Return the orthogonal projection (foot) of ``pt`` onto line ``a-b``."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((pt[0] - a[0]) * dx + (pt[1] - a[1]) * dy) / (dx * dx + dy * dy)
    return (a[0] + t * dx, a[1] + t * dy)


def _barycentric(
    wa: float,
    wb: float,
    wc: float,
    a: Point,
    b: Point,
    c: Point,
) -> Point:
    """Compute exact point from unnormalized barycentric weights ``(wa : wb : wc)``."""
    w_sum = wa + wb + wc
    return (
        (wa * a[0] + wb * b[0] + wc * c[0]) / w_sum,
        (wa * a[1] + wb * b[1] + wc * c[1]) / w_sum,
    )


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
        msg = "Euler line does not intersect seal boundary"
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


def _add_right_angle_tick(
    mb: MedallionBuilder,
    foot: Point,
    along_side: Point,
    along_alt: Point,
    size: float = 2.9,
) -> None:
    """Draw a crisp perpendicular right-angle square tick at an altitude foot."""
    ux, uy = along_side[0] - foot[0], along_side[1] - foot[1]
    lu = math.hypot(ux, uy)
    vx, vy = along_alt[0] - foot[0], along_alt[1] - foot[1]
    lv = math.hypot(vx, vy)
    if lu < 1e-9 or lv < 1e-9:
        return
    ux, uy = ux / lu, uy / lu
    vx, vy = vx / lv, vy / lv
    q1 = (foot[0] + size * ux, foot[1] + size * uy)
    q2 = (foot[0] + size * vx, foot[1] + size * vy)
    q3 = (q1[0] + size * vx, q1[1] + size * vy)
    mb.add_line("detail", q1[0], q1[1], q3[0], q3[1])
    mb.add_line("detail", q2[0], q2[1], q3[0], q3[1])


def build_kimberling_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Clark Kimberling.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Canonical Acute Scalene Triangle ABC (29 deg, 64 deg, 87 deg)
    # ------------------------------------------------------------------
    # Central arcs: 2A = 58 deg (BC), 2B = 128 deg (CA), 2C = 174 deg (AB).
    # Strongly asymmetric acute angles guarantee wide separation (> 7.2 units)
    # across all six featured ETC centers X(1)..X(6).
    r_c = 54.0
    x3: Point = (ox, oy)  # Circumcenter X(3)
    pt_a = polar(ox, oy, r_c, 160.0)  # Lower-left base corner (angle A = 29 deg)
    pt_b = polar(ox, oy, r_c, -14.0)  # Right-upper corner (angle B = 64 deg; arc AB = 174 = 2*87)
    pt_c = polar(ox, oy, r_c, -72.0)  # Top-right apex (angle C = 87 deg; arc BC = 58 = 2*29)

    side_a = _dist(pt_b, pt_c)
    side_b = _dist(pt_c, pt_a)
    side_c = _dist(pt_a, pt_b)
    semi_p = 0.5 * (side_a + side_b + side_c)
    area = math.sqrt(semi_p * (semi_p - side_a) * (semi_p - side_b) * (semi_p - side_c))
    r_in = area / semi_p
    r_9 = 0.5 * r_c

    # Classical Quartet & Foundational ETC Centers
    x1 = _barycentric(side_a, side_b, side_c, pt_a, pt_b, pt_c)  # Incenter X(1)
    x2 = _barycentric(1.0, 1.0, 1.0, pt_a, pt_b, pt_c)  # Centroid X(2)
    x4: Point = (
        ox + (pt_a[0] - ox) + (pt_b[0] - ox) + (pt_c[0] - ox),
        oy + (pt_a[1] - oy) + (pt_b[1] - oy) + (pt_c[1] - oy),
    )  # Orthocenter X(4)
    x5 = _mid(x3, x4)  # Nine-Point Center X(5)
    x6 = _barycentric(
        side_a * side_a, side_b * side_b, side_c * side_c, pt_a, pt_b, pt_c
    )  # Symmedian Point X(6)

    # Analytical Verification of Euler Line Collinearity & Exact 2 : 1 : 3 Spacing
    d_34 = _dist(x3, x4)
    d_32 = _dist(x3, x2)
    d_25 = _dist(x2, x5)
    d_54 = _dist(x5, x4)
    if (
        abs(d_32 / d_34 - 1.0 / 3.0) > 1e-12
        or abs(d_25 / d_34 - 1.0 / 6.0) > 1e-12
        or abs(d_54 / d_34 - 0.5) > 1e-12
    ):
        msg = "Euler line 2:1:3 spacing invariant violated"
        raise ValueError(msg)

    dx_34, dy_34 = x4[0] - x3[0], x4[1] - x3[1]
    for label, pt in (("X(2)", x2), ("X(5)", x5)):
        err = abs((pt[0] - x3[0]) * dy_34 - (pt[1] - x3[1]) * dx_34) / d_34
        if err > 1e-12:
            msg = f"Euler line collinearity failed for {label}: {err:.3e}"
            raise ValueError(msg)

    # Verify Feuerbach's Theorem: Nine-Point Circle & Incircle are internally tangent at X(11)
    d_51 = _dist(x5, x1)
    if abs(d_51 - (r_9 - r_in)) > 1e-11:
        msg = f"Feuerbach tangency invariant violated: {d_51:.12f} != {r_9 - r_in:.12f}"
        raise ValueError(msg)
    x11: Point = (
        x5[0] + r_9 * (x1[0] - x5[0]) / d_51,
        x5[1] + r_9 * (x1[1] - x5[1]) / d_51,
    )

    # ------------------------------------------------------------------
    # 2. Four Foundational Construction Systems (detail & airy scaffold)
    # ------------------------------------------------------------------
    # (a) Exact Incircle (X(1), r_in) & vertex angle-bisector arcs
    mb.add_circle("detail", x1[0], x1[1], r_in)
    for vertex, adj1, adj2 in ((pt_a, pt_b, pt_c), (pt_b, pt_c, pt_a), (pt_c, pt_a, pt_b)):
        a1 = _angle_deg(vertex[0], vertex[1], adj1)
        a2 = _angle_deg(vertex[0], vertex[1], adj2)
        mb.add_arc("detail", vertex[0], vertex[1], 10.0, a1, a2)
        mb.add_arc("detail", vertex[0], vertex[1], 12.2, a1, a2)

    # (b) Exact Nine-Point Circle (X(5), R_c / 2) kissing Incircle at X(11)
    mb.add_circle("detail", x5[0], x5[1], r_9)

    # (c) Medians concurring at X(2) softly on scaffold + crisp midpoint rings on detail
    m_a, m_b, m_c = _mid(pt_b, pt_c), _mid(pt_c, pt_a), _mid(pt_a, pt_b)
    for v, m in ((pt_a, m_a), (pt_b, m_b), (pt_c, m_c)):
        mb.add_line("scaffold", v[0], v[1], m[0], m[1])
        mb.add_circle("detail", m[0], m[1], 1.45)

    # (d) Altitudes concurring at X(4) with crisp perpendicular feet ticks
    f_a = _project_to_line(pt_a, pt_b, pt_c)
    f_b = _project_to_line(pt_b, pt_c, pt_a)
    f_c = _project_to_line(pt_c, pt_a, pt_b)
    mb.add_line("detail", pt_a[0], pt_a[1], f_a[0], f_a[1])
    mb.add_line("detail", pt_b[0], pt_b[1], f_b[0], f_b[1])
    mb.add_line("detail", pt_c[0], pt_c[1], f_c[0], f_c[1])
    _add_right_angle_tick(mb, f_a, pt_b, pt_a, size=2.9)
    _add_right_angle_tick(mb, f_b, pt_c, pt_b, size=2.9)
    _add_right_angle_tick(mb, f_c, pt_a, pt_c, size=2.9)

    # ------------------------------------------------------------------
    # 3. Bold Primary Circumcircle & Canonical Acute Scalene Triangle ABC
    # ------------------------------------------------------------------
    mb.add_circle("primary", x3[0], x3[1], r_c)
    mb.add_line("primary", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("primary", pt_c[0], pt_c[1], pt_a[0], pt_a[1])

    # ------------------------------------------------------------------
    # 4. Blazing Golden Euler Line & ETC Center Constellation
    # ------------------------------------------------------------------
    eu_1, eu_2 = _line_circle_intersections(x3, x4, ox, oy, r_seal)
    mb.add_line("golden", eu_1[0], eu_1[1], eu_2[0], eu_2[1])
    mb.add_circle("golden", eu_1[0], eu_1[1], 1.5)
    mb.add_circle("golden", eu_2[0], eu_2[1], 1.5)

    # Golden constellation links off the Euler Line: X(3)-X(1), X(1)-X(2), & Brocard X(3)-X(6)
    mb.add_line("golden", x3[0], x3[1], x1[0], x1[1])
    mb.add_line("golden", x1[0], x1[1], x2[0], x2[1])
    mb.add_line("golden", x3[0], x3[1], x6[0], x6[1])

    # Crisp golden vertex rings at A, B, C
    for vx, vy in (pt_a, pt_b, pt_c):
        mb.add_circle("golden", vx, vy, 3.4)
        mb.add_circle("golden", vx, vy, 1.75, filled=True)

    # Secondary golden jewels for X(5) Nine-Point Center, X(6) Symmedian Point, & X(11) Feuerbach
    for jx, jy in (x5, x6):
        mb.add_circle("golden", jx, jy, 2.3)
        mb.add_circle("golden", jx, jy, 1.2, filled=True)
    mb.add_circle("golden", x11[0], x11[1], 1.55, filled=True)

    # Radiant distinct double-ringed golden stars crowning the Classical Quartet X(1)..X(4)
    for qx, qy in (x1, x2, x3, x4):
        mb.add_circle("golden", qx, qy, 3.35)
        mb.add_circle("golden", qx, qy, 1.75, filled=True)

    return mb.build()


def build_kimberling_svg(theme: str = "dark") -> str:
    """Render the Clark Kimberling medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_kimberling_elements()
    return render_medallion_svg(layers, theme=theme)


def write_kimberling_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``kimberling_dark.svg`` and ``kimberling_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "kimberling_dark.svg"
    light_path = target_dir / "kimberling_light.svg"
    dark_path.write_text(build_kimberling_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_kimberling_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
