"""Study 45: H. E. Huntley — Pure Sacred Geometric Emblem Medallion.

Celebrates H. E. Huntley's *The Divine Proportion: A Study in Mathematical
Beauty* (1970), uniting two of Huntley's signature golden constructions across
a shared diameter ``AB`` inside the unified ``R = 68`` graduated astrolabe seal:

1. **Upper Semicircle — ``3-4-5`` Right-Triangle Angle-Bisector Golden Section**:
   Inscribed on horizontal diameter ``AB = 5u``, right triangle ``ABC``
   (``AC = 3u``, ``BC = 4u``, ``AB = 5u``) has internal angle bisector of
   ``angle A`` meeting leg ``BC`` at ``D`` (``CD = 1.5u``, ``DB = 2.5u``).
   The golden circle ``(D, r = DC)`` is simultaneously tangent to leg ``AC`` at
   ``C`` and hypotenuse ``AB`` at ``T``, cutting ray ``AD`` at ``P`` and ``Q``
   in exact golden proportion:
   ``|AQ|/|AC| = |AC|/|AP| = |AQ|/|PQ| = |PQ|/|AP| = phi`` (verified ``< 1e-12``).
2. **Lower Semicircle — Golden Gnomon, Golden Triangle (``36-72-72``), &
   ``G1``-Smooth *Spira Mirabilis***: Sharing base ``AB``, the obtuse Golden
   Gnomon ``ABW`` (``108-36-36``) subdivides at golden-section point ``K`` into
   a ``36-72-72`` Golden Triangle ``BKW`` and recursive golden triangles whose
   seven ``108 deg`` circular arcs connect with exact ``G1`` tangency into the
   luminous golden spiral pole.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_huntley_elements",
    "build_huntley_svg",
    "write_huntley_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _angle_deg(cx: float, cy: float, pt: Point) -> float:
    """Return the angle in degrees of ``pt`` relative to ``(cx, cy)``."""
    return math.degrees(math.atan2(pt[1] - cy, pt[0] - cx))


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
    vertex: Point,
    p_a: Point,
    p_b: Point,
    size: float = 3.8,
) -> None:
    """Draw a crisp perpendicular square tick at ``vertex`` along rays to ``p_a`` and ``p_b``."""
    ux, uy = p_a[0] - vertex[0], p_a[1] - vertex[1]
    lu = math.hypot(ux, uy)
    vx, vy = p_b[0] - vertex[0], p_b[1] - vertex[1]
    lv = math.hypot(vx, vy)
    ux, uy = ux / lu, uy / lu
    vx, vy = vx / lv, vy / lv
    q1 = (vertex[0] + size * ux, vertex[1] + size * uy)
    q2 = (vertex[0] + size * vx, vertex[1] + size * vy)
    q3 = (q1[0] + size * vx, q1[1] + size * vy)
    mb.add_line("detail", q1[0], q1[1], q3[0], q3[1])
    mb.add_line("detail", q2[0], q2[1], q3[0], q3[1])


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


def build_huntley_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for H. E. Huntley.

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
    # 1. Exact 3-4-5 Right Triangle ABC Inscribed in Circumcircle (O, 2.5u)
    # ------------------------------------------------------------------
    u = 20.2
    r_c = 2.5 * u  # 50.5: heroic circumcircle centered at (0, -8)

    pt_a: Point = (ox - r_c, oy)
    pt_b: Point = (ox + r_c, oy)
    # Exact Pythagorean vertex C: AC = 3u, BC = 4u, AB = 5u, |C - O| = 2.5u
    pt_c: Point = (ox - 0.7 * u, oy - 2.4 * u)

    # Internal angle bisector of angle A hits leg BC at D (CD = 1.5u, DB = 2.5u)
    pt_d: Point = (ox + 0.5 * u, oy - 1.5 * u)
    r_bis = 1.5 * u  # Radius of circle (D, DC) tangent to BOTH AC at C and AB at T
    pt_t: Point = (ox + 0.5 * u, oy)  # Exact tangency foot on hypotenuse AB

    # Ray A -> D meets circle (D, r_bis) at internal P and external Q
    dx_ad, dy_ad = pt_d[0] - pt_a[0], pt_d[1] - pt_a[1]
    len_ad = math.hypot(dx_ad, dy_ad)
    ux_ad, uy_ad = dx_ad / len_ad, dy_ad / len_ad
    pt_p: Point = (pt_d[0] - r_bis * ux_ad, pt_d[1] - r_bis * uy_ad)
    pt_q: Point = (pt_d[0] + r_bis * ux_ad, pt_d[1] + r_bis * uy_ad)

    # Analytical verification of 3-4-5 right triangle & all 4 golden ratios
    ac_len, bc_len, ab_len = _dist(pt_a, pt_c), _dist(pt_b, pt_c), _dist(pt_a, pt_b)
    if (
        abs(ac_len - 3.0 * u) > 1e-11
        or abs(bc_len - 4.0 * u) > 1e-11
        or abs(ab_len - 5.0 * u) > 1e-11
    ):
        msg = "3-4-5 side length invariant violated"
        raise ValueError(msg)
    if abs(_dist(pt_d, pt_c) - r_bis) > 1e-11 or abs(_dist(pt_d, pt_t) - r_bis) > 1e-11:
        msg = "Bisector circle tangency invariant violated"
        raise ValueError(msg)

    ap_len = _dist(pt_a, pt_p)
    pq_len = _dist(pt_p, pt_q)
    aq_len = _dist(pt_a, pt_q)
    for ratio_val in (aq_len / ac_len, ac_len / ap_len, aq_len / pq_len, pq_len / ap_len):
        if abs(ratio_val - phi) > 1e-12:
            msg = f"Huntley 3-4-5 golden ratio invariant violated: {ratio_val:.15f} != {phi:.15f}"
            raise ValueError(msg)

    if _dist(pt_d, (ox, oy)) + r_bis >= r_seal - 4.5:
        msg = "Bisector tangent circle too close to seal rim"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Circumcircle, 3-4-5 Right Triangle ABC, & Golden Bisector Construction
    # ------------------------------------------------------------------
    mb.add_circle("detail", ox, oy, r_c)

    # Bold primary 3-4-5 Right Triangle ABC
    mb.add_line("primary", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("primary", pt_a[0], pt_a[1], pt_c[0], pt_c[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_c[0], pt_c[1])

    # Crisp perpendicular right-angle ticks at C and T (on right side away from spiral)
    _add_right_angle_mark(mb, pt_c, pt_a, pt_b, size=4.0)
    _add_right_angle_mark(mb, pt_t, pt_b, pt_d, size=2.9)
    mb.add_line("detail", pt_d[0], pt_d[1], pt_t[0], pt_t[1])

    # Luminous golden Bisector Tangent Circle (D, r = DC) & Golden Ray A-P-D-Q
    mb.add_circle("golden", pt_d[0], pt_d[1], r_bis)
    mb.add_line("golden", pt_a[0], pt_a[1], pt_q[0], pt_q[1])

    # Subtle golden equal-radius ticks on PD & DQ and AC = PQ
    _add_ratio_tick(mb, pt_p, pt_d, 1)
    _add_ratio_tick(mb, pt_d, pt_q, 1)
    _add_ratio_tick(mb, pt_a, pt_c, 2)

    # Calibrated compass ratio arcs centered at A transferring AC = AT = PQ = 3u
    ang_ac = _angle_deg(pt_a[0], pt_a[1], pt_c)
    ang_ad = _angle_deg(pt_a[0], pt_a[1], pt_d)
    mb.add_arc("detail", pt_a[0], pt_a[1], ac_len, ang_ac, 0.0)
    mb.add_arc("detail", pt_a[0], pt_a[1], ap_len, ang_ad - 12.0, ang_ad + 12.0)

    # ------------------------------------------------------------------
    # 3. Lower Semicircle: Golden Gnomon ABW, Golden Triangle BKW, & Spira Mirabilis
    # ------------------------------------------------------------------
    h_gnomon = r_c * math.tan(math.radians(36.0))
    pt_w: Point = (ox, oy + h_gnomon)

    if abs((ab_len / _dist(pt_b, pt_w)) - phi) > 1e-12:
        msg = "Golden Gnomon ratio |AB|/|BW| != phi"
        raise ValueError(msg)

    pt_k: Point = (pt_b[0] - ab_len / phi, oy)

    mb.add_line("primary", pt_a[0], pt_a[1], pt_w[0], pt_w[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_w[0], pt_w[1])
    mb.add_line("detail", pt_k[0], pt_k[1], pt_w[0], pt_w[1])

    # Recursive 36-72-72 Golden Triangle subdivision & G1-smooth 108-deg Spira Mirabilis
    p_apex, p_v1, p_v2 = pt_b, pt_w, pt_k
    pole_approx: Point = p_v2
    for step in range(7):
        leg_len = _dist(p_apex, p_v2)
        base_len = _dist(p_v1, p_v2)
        if abs((leg_len / base_len) - phi) > 1e-10:
            msg = f"Recursive Golden Triangle ratio drifted at step {step}"
            raise ValueError(msg)
        t_cut = base_len / leg_len
        p_new: Point = (
            p_apex[0] + t_cut * (p_v2[0] - p_apex[0]),
            p_apex[1] + t_cut * (p_v2[1] - p_apex[1]),
        )
        if step < 5:
            mb.add_line("detail", p_v1[0], p_v1[1], p_new[0], p_new[1])
        rad_arc = _dist(p_new, p_apex)
        a_start = _angle_deg(p_new[0], p_new[1], p_apex)
        a_end = _angle_deg(p_new[0], p_new[1], p_v1)
        mb.add_arc("golden", p_new[0], p_new[1], rad_arc, a_start, a_end)

        p_apex, p_v1, p_v2 = p_v1, p_v2, p_new
        pole_approx = p_new

    # ------------------------------------------------------------------
    # 4. Luminous Golden Nodes & Double-Ringed Theorem Stars
    # ------------------------------------------------------------------
    for vx, vy in (pt_a, pt_b, pt_c, pt_w):
        mb.add_circle("golden", vx, vy, 3.6)
        mb.add_circle("golden", vx, vy, 1.85, filled=True)

    # Sleek tangent jewel at T and golden section marker at K
    mb.add_circle("golden", pt_t[0], pt_t[1], 1.55, filled=True)
    mb.add_circle("golden", pt_k[0], pt_k[1], 2.4)
    mb.add_circle("golden", pt_k[0], pt_k[1], 1.2, filled=True)

    # Radiant double-ringed golden stars at Golden Section points P, D, Q
    for sx_pt, sy_pt in (pt_p, pt_d, pt_q):
        mb.add_circle("golden", sx_pt, sy_pt, 4.2)
        mb.add_circle("golden", sx_pt, sy_pt, 2.2, filled=True)

    # Golden eye pole of the Spira Mirabilis
    mb.add_circle("golden", pole_approx[0], pole_approx[1], 3.3)
    mb.add_circle("golden", pole_approx[0], pole_approx[1], 1.65, filled=True)

    return mb.build()


def build_huntley_svg(theme: str = "dark") -> str:
    """Render the H. E. Huntley medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_huntley_elements()
    return render_medallion_svg(layers, theme=theme)


def write_huntley_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``huntley_dark.svg`` and ``huntley_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "huntley_dark.svg"
    light_path = target_dir / "huntley_light.svg"
    dark_path.write_text(build_huntley_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_huntley_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
