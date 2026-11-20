"""Study 41: Giovanni Ceva — Pure Sacred Geometric Emblem Medallion.

Celebrates Giovanni Ceva's *De lineis rectis se invicem secantibus statica
constructio* (1678), proving **Ceva's Concurrency Theorem** via barycentric
statics and illuminating the projective harmonic duality between **Ceva** and
**Menelaus**:

1. **Heroic Scalene Triangle ``ABC`` & Circumcircle**: Centered prominently
   inside the unified ``R = 68`` graduated astrolabe seal with its exact
   circumcircle and compass ratio arcs along each side.
2. **Three Exact Concurrent Cevians (``m_A : m_B : m_C = 3 : 2 : 5``)**:
   Luminous golden cevians ``A-P-D``, ``B-P-E``, ``C-P-F`` meeting at the
   radiant off-center concurrency star ``P`` near the heart of the medallion,
   analytically verified so ``(|AF|/|FB|) * (|BD|/|DC|) * (|CE|/|EA|) = 1``.
3. **Inscribed Cevian Triangle ``DEF`` & Harmonic Trilinear Polar**: Crisp
   cevian triangle ``DEF`` whose extended side ``EF`` meets extended ``BC`` at
   the exact harmonic conjugate ``X`` (``H(B, C; D, X) = -1``), anchoring the
   slanted luminous golden trilinear polar line ``X-Y-Z`` (verified collinear
   with ``Y = FD ∩ CA`` and ``Z = DE ∩ AB`` to ``< 1e-11``).
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_ceva_elements",
    "build_ceva_svg",
    "write_ceva_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _angle_deg(cx: float, cy: float, pt: Point) -> float:
    """Return the angle in degrees of ``pt`` relative to ``(cx, cy)``."""
    return math.degrees(math.atan2(pt[1] - cy, pt[0] - cx))


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
        msg = "Line does not intersect seal boundary"
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
    spacing = 2.4
    half_tick = 2.1
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


def build_ceva_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Giovanni Ceva.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Heroic Scalene Triangle ABC & Barycentric Ceva Point P (3 : 2 : 5)
    # ------------------------------------------------------------------
    # Positioned so ABC & its circumcircle command the heart of the seal,
    # concurrency star P sits right near (0, -8), and harmonic conjugate X
    # with slanted Trilinear Polar X-Y-Z sweeps cleanly across the right wing.
    pt_a: Point = (4.0, -56.0)
    pt_b: Point = (-45.0, 24.0)
    pt_c: Point = (13.0, 20.0)

    # Barycentric weights (statics mass points from Ceva's 1678 treatise)
    m_a, m_b, m_c = 3.0, 2.0, 5.0
    m_tot = m_a + m_b + m_c

    pt_p: Point = (
        (m_a * pt_a[0] + m_b * pt_b[0] + m_c * pt_c[0]) / m_tot,
        (m_a * pt_a[1] + m_b * pt_b[1] + m_c * pt_c[1]) / m_tot,
    )
    pt_d: Point = (
        (m_b * pt_b[0] + m_c * pt_c[0]) / (m_b + m_c),
        (m_b * pt_b[1] + m_c * pt_c[1]) / (m_b + m_c),
    )
    pt_e: Point = (
        (m_c * pt_c[0] + m_a * pt_a[0]) / (m_c + m_a),
        (m_c * pt_c[1] + m_a * pt_a[1]) / (m_c + m_a),
    )
    pt_f: Point = (
        (m_a * pt_a[0] + m_b * pt_b[0]) / (m_a + m_b),
        (m_a * pt_a[1] + m_b * pt_b[1]) / (m_a + m_b),
    )

    # Analytical verification of exact concurrency and Ceva's Theorem:
    # (|AF| / |FB|) * (|BD| / |DC|) * (|CE| / |EA|) == 1.000000000000
    p_check_1 = _line_intersection(pt_a, pt_d, pt_b, pt_e)
    p_check_2 = _line_intersection(pt_b, pt_e, pt_c, pt_f)
    if _dist(pt_p, p_check_1) > 1e-11 or _dist(pt_p, p_check_2) > 1e-11:
        msg = "Ceva concurrency invariant violated"
        raise ValueError(msg)

    ceva_prod = (
        (_dist(pt_a, pt_f) / _dist(pt_f, pt_b))
        * (_dist(pt_b, pt_d) / _dist(pt_d, pt_c))
        * (_dist(pt_c, pt_e) / _dist(pt_e, pt_a))
    )
    if abs(ceva_prod - 1.0) > 1e-12:
        msg = f"Ceva product invariant violated: {ceva_prod:.15f}"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Harmonic Trilinear Polar X-Y-Z & Harmonic Conjugate H(B, C; D, X)
    # ------------------------------------------------------------------
    pt_x = _line_intersection(pt_e, pt_f, pt_b, pt_c)
    pt_y = _line_intersection(pt_f, pt_d, pt_c, pt_a)
    pt_z = _line_intersection(pt_d, pt_e, pt_a, pt_b)

    # Verify exact harmonic conjugate cross-ratio (|BD|/|DC|) / (|BX|/|XC|) == 1
    harm_ratio = (_dist(pt_b, pt_d) / _dist(pt_d, pt_c)) / (_dist(pt_b, pt_x) / _dist(pt_x, pt_c))
    if abs(harm_ratio - 1.0) > 1e-12:
        msg = f"Harmonic conjugate invariant violated: {harm_ratio:.15f}"
        raise ValueError(msg)

    # Verify exact collinearity of X, Y, Z (the Trilinear Polar of P)
    dx_yz, dy_yz = pt_z[0] - pt_y[0], pt_z[1] - pt_y[1]
    polar_err = abs((pt_x[0] - pt_y[0]) * dy_yz - (pt_x[1] - pt_y[1]) * dx_yz) / math.hypot(
        dx_yz, dy_yz
    )
    if polar_err > 1e-11:
        msg = f"Trilinear polar collinearity violated: {polar_err:.3e}"
        raise ValueError(msg)

    if _dist(pt_x, (ox, oy)) >= r_seal - 8.0:
        msg = f"Harmonic conjugate X={pt_x} too close to seal rim"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 3. Circumcircle of ABC & Compass Ratio Construction Arcs (detail)
    # ------------------------------------------------------------------
    ccx, ccy, ccr = _circumcircle(pt_a, pt_b, pt_c)
    mb.add_circle("detail", ccx, ccy, ccr)
    mb.add_circle("detail", ccx, ccy, 1.35)

    # Delicate compass ratio arcs centered at A, B, C sweeping across F, D, E
    for center, target, half_sweep in (
        (pt_a, pt_f, 12.0),
        (pt_a, pt_e, 12.0),
        (pt_b, pt_f, 10.0),
        (pt_b, pt_d, 10.0),
        (pt_c, pt_d, 13.0),
        (pt_c, pt_e, 13.0),
    ):
        rad = _dist(center, target)
        ang = _angle_deg(center[0], center[1], target)
        mb.add_arc("detail", center[0], center[1], rad, ang - half_sweep, ang + half_sweep)

    # ------------------------------------------------------------------
    # 4. Inscribed Cevian Triangle DEF, Harmonic Extensions, & Trilinear Polar
    # ------------------------------------------------------------------
    # Crisp Cevian Triangle DEF in detail so primary ABC & golden Cevians dominate
    mb.add_line("detail", pt_d[0], pt_d[1], pt_e[0], pt_e[1])
    mb.add_line("detail", pt_e[0], pt_e[1], pt_f[0], pt_f[1])
    mb.add_line("detail", pt_f[0], pt_f[1], pt_d[0], pt_d[1])

    # Extend BC -> X and FE -> X cleanly to their exact harmonic intersection X
    mb.add_line("detail", pt_c[0], pt_c[1], pt_x[0], pt_x[1])
    mb.add_line("detail", pt_e[0], pt_e[1], pt_x[0], pt_x[1])
    bc_r1, bc_r2 = _line_circle_intersections(pt_b, pt_c, ox, oy, r_seal)
    mb.add_line("detail", bc_r1[0], bc_r1[1], pt_b[0], pt_b[1])
    mb.add_line("detail", pt_x[0], pt_x[1], bc_r2[0], bc_r2[1])

    # Luminous golden Trilinear Polar Line (X-Y-Z) spanning the astrolabe seal
    pol_1, pol_2 = _line_circle_intersections(pt_x, pt_y, ox, oy, r_seal)
    mb.add_line("golden", pol_1[0], pol_1[1], pol_2[0], pol_2[1])
    mb.add_circle("golden", pol_1[0], pol_1[1], 1.45)
    mb.add_circle("golden", pol_2[0], pol_2[1], 1.45)

    # ------------------------------------------------------------------
    # 5. Bold Scalene Triangle ABC (primary) & Concurrent Golden Cevians
    # ------------------------------------------------------------------
    mb.add_line("primary", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("primary", pt_c[0], pt_c[1], pt_a[0], pt_a[1])

    # Three bold concurrent golden Cevians A-P-D, B-P-E, C-P-F
    mb.add_line("golden", pt_a[0], pt_a[1], pt_d[0], pt_d[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_e[0], pt_e[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_f[0], pt_f[1])

    # Golden side-ratio ticks (1, 2, 3 notches echoing Menelaus's visual language)
    _add_ratio_tick(mb, pt_a, pt_f, 1)
    _add_ratio_tick(mb, pt_f, pt_b, 2)
    _add_ratio_tick(mb, pt_b, pt_d, 3)
    _add_ratio_tick(mb, pt_d, pt_c, 1)
    _add_ratio_tick(mb, pt_c, pt_e, 2)
    _add_ratio_tick(mb, pt_e, pt_a, 3)

    # Crisp ringed triangle vertices A, B, C
    for vx, vy in (pt_a, pt_b, pt_c):
        mb.add_circle("golden", vx, vy, 3.8)
        mb.add_circle("golden", vx, vy, 2.0, filled=True)

    # Crisp golden cevian foot nodes D, E, F
    for fx, fy in (pt_d, pt_e, pt_f):
        mb.add_circle("golden", fx, fy, 3.6)
        mb.add_circle("golden", fx, fy, 1.9, filled=True)

    # Bold double-ringed golden harmonic conjugate node X on the Trilinear Polar
    mb.add_circle("golden", pt_x[0], pt_x[1], 4.4)
    mb.add_circle("golden", pt_x[0], pt_x[1], 2.4, filled=True)

    # Radiant triple-ringed golden Ceva Concurrency Star at P
    mb.add_circle("golden", pt_p[0], pt_p[1], 5.8)
    mb.add_circle("golden", pt_p[0], pt_p[1], 3.6)
    mb.add_circle("golden", pt_p[0], pt_p[1], 2.2, filled=True)

    return mb.build()


def build_ceva_svg(theme: str = "dark") -> str:
    """Render the Giovanni Ceva medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_ceva_elements()
    return render_medallion_svg(layers, theme=theme)


def write_ceva_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``ceva_dark.svg`` and ``ceva_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "ceva_dark.svg"
    light_path = target_dir / "ceva_light.svg"
    dark_path.write_text(build_ceva_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_ceva_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
