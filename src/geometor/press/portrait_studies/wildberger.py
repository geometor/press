"""Study 48: Norman J. Wildberger — Pure Sacred Geometric Emblem Medallion.

Celebrates Norman J. Wildberger (b. 1957), author of *Divine Proportions:
Rational Trigonometry to Universal Geometry* (2005), replacing transcendental
lengths and angles with 100% exact algebraic **Quadrances** (``Q = dx^2 + dy^2``)
and **Spreads** (``s = sin^2(theta)``) inside the unified ``R = 68`` graduated
astrolabe seal:

1. **Exact ``13-14-15`` Heronian Rational Triangle & Three Outward Quadrance
   Squares**: Scaled cleanly on its exact rational circumcenter ``(7, 33/8)``
   aligned directly to ``(0, -8)``, the triangle ``A_1 A_2 A_3`` has exact
   integer quadrances ``Q_1 = 225``, ``Q_2 = 169``, ``Q_3 = 196``, with all
   three bold outward quadrance squares fitting completely inside ``R = 68``
   and subdivided as geometric area tiles (including the altitude split
   ``70 + 126 = 196`` inside ``Q_3``).
2. **Exact Rational Trigonometry Laws (Verified in ``fractions.Fraction``)**:
   Spreads ``s_1 = 144/169``, ``s_2 = 16/25``, ``s_3 = 3136/4225`` satisfy the
   Spread Law (``s_i / Q_i = 16/4225``), the Cross Law
   (``(Q_1 + Q_2 - Q_3)^2 = 4 Q_1 Q_2 (1 - s_3)``), and the Triple Spread
   Formula identically with zero rounding error.
3. **Golden Altitude, Spread-Law Circumcircle, & Vertex Spread Drops**: The
   exact rational altitude ``h = 12`` (splitting ``13-14-15`` into ``5-12-13``
   and ``9-12-15``), the Spread-Law Circumcircle (``R_c = 65/8 * u``,
   ``4 R_c^2 = Q_i / s_i``), and Wildberger's canonical vertex spread arcs with
   perpendicular drop chords ``s_i = Q_opp / Q_hyp`` gleam in radiant gold.
"""

from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_wildberger_elements",
    "build_wildberger_svg",
    "write_wildberger_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _angle_deg(cx: float, cy: float, pt: Point) -> float:
    """Return the angle in degrees of ``pt`` relative to ``(cx, cy)``."""
    return math.degrees(math.atan2(pt[1] - cy, pt[0] - cx))


def _project_to_line(pt: Point, a: Point, b: Point) -> Point:
    """Return the orthogonal projection (foot) of ``pt`` onto line ``a-b``."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((pt[0] - a[0]) * dx + (pt[1] - a[1]) * dy) / (dx * dx + dy * dy)
    return (a[0] + t * dx, a[1] + t * dy)


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
    along_a: Point,
    along_b: Point,
    size: float = 2.6,
) -> None:
    """Draw a crisp perpendicular square tick at ``foot`` along rays to ``along_a``, ``along_b``."""
    ux, uy = along_a[0] - foot[0], along_a[1] - foot[1]
    lu = math.hypot(ux, uy)
    vx, vy = along_b[0] - foot[0], along_b[1] - foot[1]
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


def _verify_exact_rational_trigonometry() -> None:
    """Verify Spread Law, Cross Law, and Triple Spread Formula in exact ``Fraction`` arithmetic."""
    # Exact 13-14-15 Heronian rational triangle: A1=(0,0), A2=(14,0), A3=(5,12)
    q1 = Fraction(15 * 15)  # 225 (opposite A1)
    q2 = Fraction(13 * 13)  # 169 (opposite A2)
    q3 = Fraction(14 * 14)  # 196 (opposite A3)

    # Exact rational spreads s = sin^2(theta)
    s1 = Fraction(12, 13) ** 2  # 144 / 169
    s2 = Fraction(12, 15) ** 2  # 16 / 25
    s3 = Fraction(12 * 14, 13 * 15) ** 2  # 3136 / 4225

    # 1. Exact Spread Law: s1/Q1 == s2/Q2 == s3/Q3 == 16/4225 == 1 / (4 R_c^2)
    spread_const = Fraction(16, 4225)
    if not (s1 / q1 == s2 / q2 == s3 / q3 == spread_const):
        msg = "Exact Rational Spread Law failed"
        raise ValueError(msg)

    # 2. Exact Cross Law: (Q1 + Q2 - Q3)^2 == 4 * Q1 * Q2 * (1 - s3)
    for qa, qb, qc, sc in ((q1, q2, q3, s3), (q2, q3, q1, s1), (q3, q1, q2, s2)):
        if (qa + qb - qc) ** 2 != 4 * qa * qb * (1 - sc):
            msg = "Exact Rational Cross Law failed"
            raise ValueError(msg)

    # 3. Exact Triple Spread Formula: (s1 + s2 + s3)^2 == 2(s1^2 + s2^2 + s3^2) + 4 s1 s2 s3
    if (s1 + s2 + s3) ** 2 != 2 * (s1 * s1 + s2 * s2 + s3 * s3) + 4 * s1 * s2 * s3:
        msg = "Exact Triple Spread Formula failed"
        raise ValueError(msg)


def _add_quadrance_square(
    mb: MedallionBuilder,
    p1: Point,
    p2: Point,
    outward_sign: float,
    r_seal: float,
) -> tuple[Point, Point, Point]:
    """Erect outward quadrance square on ``p1-p2`` with subtle area grid; return outer corners & center."""
    ox, oy = MED_CX, MED_CY
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    # Perpendicular vector of identical length forming exact square
    nx, ny = outward_sign * (-dy), outward_sign * dx
    p3: Point = (p2[0] + nx, p2[1] + ny)
    p4: Point = (p1[0] + nx, p1[1] + ny)
    center: Point = (0.25 * (p1[0] + p2[0] + p3[0] + p4[0]), 0.25 * (p1[1] + p2[1] + p3[1] + p4[1]))

    for corner in (p3, p4):
        if _dist(corner, (ox, oy)) >= r_seal - 5.5:
            msg = f"Quadrance square corner {corner} too close to seal rim"
            raise ValueError(msg)

    # Subtle area diagonals on scaffold & quadrant midlines on detail
    mb.add_line("scaffold", p1[0], p1[1], p3[0], p3[1])
    mb.add_line("scaffold", p2[0], p2[1], p4[0], p4[1])
    m12 = (0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1]))
    m34 = (0.5 * (p3[0] + p4[0]), 0.5 * (p3[1] + p4[1]))
    m23 = (0.5 * (p2[0] + p3[0]), 0.5 * (p2[1] + p3[1]))
    m41 = (0.5 * (p4[0] + p1[0]), 0.5 * (p4[1] + p1[1]))
    mb.add_line("detail", m12[0], m12[1], m34[0], m34[1])
    mb.add_line("detail", m23[0], m23[1], m41[0], m41[1])

    # Bold primary outer three edges of the Quadrance Square
    mb.add_line("primary", p2[0], p2[1], p3[0], p3[1])
    mb.add_line("primary", p3[0], p3[1], p4[0], p4[1])
    mb.add_line("primary", p4[0], p4[1], p1[0], p1[1])

    return (p3, p4, center)


def _add_vertex_spread_measure(
    mb: MedallionBuilder,
    vertex: Point,
    adj1: Point,
    adj2: Point,
    r_spread: float,
) -> None:
    """Draw Wildberger's canonical spread arc & exact perpendicular drop chord at ``vertex``."""
    a1 = _angle_deg(vertex[0], vertex[1], adj1)
    a2 = _angle_deg(vertex[0], vertex[1], adj2)
    # Full spread circle softly in detail + interior spread arc boldly in golden
    mb.add_circle("detail", vertex[0], vertex[1], r_spread)
    mb.add_arc("golden", vertex[0], vertex[1], r_spread, a1, a2)

    # Point U on ray vertex -> adj1 at distance r_spread, dropped perpendicularly onto vertex -> adj2
    u_pt = polar(vertex[0], vertex[1], r_spread, a1)
    h_pt = _project_to_line(u_pt, vertex, adj2)
    mb.add_line("golden", u_pt[0], u_pt[1], h_pt[0], h_pt[1])
    mb.add_circle("golden", u_pt[0], u_pt[1], 1.15, filled=True)
    mb.add_circle("golden", h_pt[0], h_pt[1], 1.15, filled=True)
    _add_right_angle_tick(mb, h_pt, vertex, u_pt, size=2.0)


def build_wildberger_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Norman J. Wildberger.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    _verify_exact_rational_trigonometry()

    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Scaled Exact 13-14-15 Heronian Rational Triangle Centered on O_c
    # ------------------------------------------------------------------
    # Math coords: A1=(0, 0), A2=(14, 0), A3=(5, 12); circumcenter O_c=(7, 33/8), R_c=65/8.
    # Map (mx, my) -> (ox + u * (mx - 7.0), oy - u * (my - 33/8)) so O_c sits at (0, -8)!
    u = 3.12
    cx_m, cy_m = 7.0, 33.0 / 8.0

    def to_svg(mx: float, my: float) -> Point:
        """Transform rational grid ``(mx, my)`` (+y up) to SVG coordinates centered on ``O_c``."""
        return (ox + u * (mx - cx_m), oy - u * (my - cy_m))

    a1 = to_svg(0.0, 0.0)
    a2 = to_svg(14.0, 0.0)
    a3 = to_svg(5.0, 12.0)
    foot_f = to_svg(5.0, 0.0)
    r_circ = (65.0 / 8.0) * u  # Exact rational Spread-Law circumradius (4*R_c^2 = Q_i / s_i)

    for v in (a1, a2, a3):
        if abs(_dist(v, (ox, oy)) - r_circ) > 1e-11:
            msg = "Rational circumradius check failed"
            raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Three Exact Outward Quadrance Squares (Q1 = 225, Q2 = 169, Q3 = 196)
    # ------------------------------------------------------------------
    # In SVG coords (x right, y down), A1(bot-left) -> A2(bot-right) -> A3(top) is CCW,
    # so the outward right-hand normal for directed side (dx, dy) is (-dy, +dx),
    # i.e., outward_sign = +1.0!
    _, _, c_q3 = _add_quadrance_square(mb, a1, a2, outward_sign=1.0, r_seal=r_seal)
    _, _, c_q1 = _add_quadrance_square(mb, a2, a3, outward_sign=1.0, r_seal=r_seal)
    _, _, c_q2 = _add_quadrance_square(mb, a3, a1, outward_sign=1.0, r_seal=r_seal)

    # Extend exact rational altitude A3 -> F straight through bottom square Q3 (70 + 126 = 196)
    f_bot = to_svg(5.0, -14.0)
    mb.add_line("detail", foot_f[0], foot_f[1], f_bot[0], f_bot[1])

    # ------------------------------------------------------------------
    # 3. Bold Primary 13-14-15 Rational Triangle A1-A2-A3
    # ------------------------------------------------------------------
    mb.add_line("primary", a1[0], a1[1], a2[0], a2[1])
    mb.add_line("primary", a2[0], a2[1], a3[0], a3[1])
    mb.add_line("primary", a3[0], a3[1], a1[0], a1[1])

    # ------------------------------------------------------------------
    # 4. Golden Spread-Law Circumcircle, Rational Altitude h=12, & Spread Drops
    # ------------------------------------------------------------------
    # Spread-Law Circumcircle (4 R_c^2 = Q_1/s_1 = Q_2/s_2 = Q_3/s_3 = 4225/16)
    mb.add_circle("golden", ox, oy, r_circ)

    # Exact rational altitude A3 -> F (h = 12, splitting 13-14-15 into 5-12-13 & 9-12-15)
    mb.add_line("golden", a3[0], a3[1], foot_f[0], foot_f[1])
    _add_right_angle_tick(mb, foot_f, a2, a3, size=3.3)

    # Wildberger's canonical vertex Spread Circles & perpendicular drop chords at A1, A2, A3
    r_spread = 10.2
    _add_vertex_spread_measure(mb, a1, a3, a2, r_spread)
    _add_vertex_spread_measure(mb, a2, a3, a1, r_spread)
    _add_vertex_spread_measure(mb, a3, a1, a2, r_spread)

    # ------------------------------------------------------------------
    # 5. Radiant Golden Stars & Quadrance Center Jewels
    # ------------------------------------------------------------------
    # Quadrance square center jewels at centroids of Q1, Q2, Q3
    for qcx, qcy in (c_q1, c_q2, c_q3):
        mb.add_circle("golden", qcx, qcy, 2.3)
        mb.add_circle("golden", qcx, qcy, 1.15, filled=True)

    # Radiant double-ringed golden stars at A1, A2, A3, altitude foot F, & circumcenter O_c
    for vx, vy in (a1, a2, a3):
        mb.add_circle("golden", vx, vy, 3.8)
        mb.add_circle("golden", vx, vy, 2.0, filled=True)

    mb.add_circle("golden", foot_f[0], foot_f[1], 3.2)
    mb.add_circle("golden", foot_f[0], foot_f[1], 1.65, filled=True)

    mb.add_circle("golden", ox, oy, 3.2)
    mb.add_circle("golden", ox, oy, 1.65, filled=True)

    return mb.build()


def build_wildberger_svg(theme: str = "dark") -> str:
    """Render the Norman J. Wildberger medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_wildberger_elements()
    return render_medallion_svg(layers, theme=theme)


def write_wildberger_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``wildberger_dark.svg`` and ``wildberger_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "wildberger_dark.svg"
    light_path = target_dir / "wildberger_light.svg"
    dark_path.write_text(build_wildberger_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_wildberger_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
