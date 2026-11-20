"""Study 39: Pappus of Alexandria — Pure Sacred Geometric Emblem Medallion.

Unites the two crown jewels of Pappus's *Synagoge* (c. 340 CE) within the
calibrated astrolabe-seal framing language of the GEOMETOR Emblem Pantheon:

1. **Upper / Center — Pappus's Hexagon Theorem (Book VII, Prop. 139)**: Two
   bold slanted carrier lines ``l1`` (carrying ``A, B, C``) and ``l2``
   (carrying ``A', B', C'``) linked by the six cross-join segments
   ``(AB', A'B)``, ``(AC', A'C)``, and ``(BC', B'C)``. Their exact analytical
   intersections ``P, Q, R`` are verified collinear to ``< 1e-12``, blazing the
   luminous golden Pappus Line ``P-Q-R`` across the heart of the medallion.
2. **Lower Arch — Pappus's Arbelos & Tangent Circle Chain (Book IV)**: A crisp
   symmetric Arbelos cradling the lower arch inside ``R = 68``, populated with
   exact inversion-derived mutually tangent Pappus Chain circles
   (``C_1`` centered, flanked symmetrically by ``C_2..C_5`` into both cusps),
   verified to machine precision for all tangencies and Pappus's height law
   ``h_n = n * d_n``, illustrated with calibrated golden height-ratio ticks.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_pappus_elements",
    "build_pappus_svg",
    "write_pappus_svgs",
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


def _add_lower_semicircle(
    mb: MedallionBuilder,
    layer: str,
    cx: float,
    cy: float,
    r: float,
) -> None:
    """Draw a downward-arching semicircle (0 -> 90 -> 180 deg in SVG coordinates)."""
    mb.add_arc(layer, cx, cy, r, 0.0, 90.0)
    mb.add_arc(layer, cx, cy, r, 90.0, 180.0)


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


def _add_pappus_hexagon(mb: MedallionBuilder, r_seal: float) -> None:
    """Construct Pappus's Hexagon Theorem (Book VII, Prop. 139) in the upper/central field."""
    ox, oy = MED_CX, MED_CY

    # Two slanted projective carrier lines l1 (upper) and l2 (lower), cleanly
    # separated from the lower Arbelos diameter at y = +10.0.
    l1_start: Point = (-46.0, -42.0)
    l1_end: Point = (46.0, -53.0)
    l2_start: Point = (-48.0, -7.0)
    l2_end: Point = (48.0, 1.0)

    # Three well-spaced points A, B, C on l1 and A', B', C' on l2 tuned so
    # collinear intersections P, Q, R spread evenly across the seal width.
    pt_a = _lerp(l1_start, l1_end, 0.08)
    pt_b = _lerp(l1_start, l1_end, 0.45)
    pt_c = _lerp(l1_start, l1_end, 0.89)

    pt_ap = _lerp(l2_start, l2_end, 0.12)
    pt_bp = _lerp(l2_start, l2_end, 0.56)
    pt_cp = _lerp(l2_start, l2_end, 0.90)

    # Exact analytical Pappus cross-join intersections
    pt_p = _line_intersection(pt_a, pt_bp, pt_ap, pt_b)
    pt_q = _line_intersection(pt_a, pt_cp, pt_ap, pt_c)
    pt_r = _line_intersection(pt_b, pt_cp, pt_bp, pt_c)

    # Verify exact collinearity of P, Q, R to machine precision (< 1e-12)
    dx_pr, dy_pr = pt_r[0] - pt_p[0], pt_r[1] - pt_p[1]
    perp_err = abs((pt_q[0] - pt_p[0]) * dy_pr - (pt_q[1] - pt_p[1]) * dx_pr) / math.hypot(
        dx_pr, dy_pr
    )
    if perp_err > 1e-12:
        msg = f"Pappus collinearity check failed: error = {perp_err:.3e}"
        raise ValueError(msg)

    # Subtle carrier extensions to the seal rim (detail)
    l1_rim_1, l1_rim_2 = _line_circle_intersections(l1_start, l1_end, ox, oy, r_seal)
    l2_rim_1, l2_rim_2 = _line_circle_intersections(l2_start, l2_end, ox, oy, r_seal)
    mb.add_line("detail", l1_rim_1[0], l1_rim_1[1], pt_a[0], pt_a[1])
    mb.add_line("detail", pt_c[0], pt_c[1], l1_rim_2[0], l1_rim_2[1])
    mb.add_line("detail", l2_rim_1[0], l2_rim_1[1], pt_ap[0], pt_ap[1])
    mb.add_line("detail", pt_cp[0], pt_cp[1], l2_rim_2[0], l2_rim_2[1])

    # Bold primary carrier segments spanning A--C and A'--C'
    mb.add_line("primary", pt_a[0], pt_a[1], pt_c[0], pt_c[1])
    mb.add_line("primary", pt_ap[0], pt_ap[1], pt_cp[0], pt_cp[1])

    # Six crisp cross-join segments forming the Pappus hexagon
    for p1, p2 in (
        (pt_a, pt_bp),
        (pt_ap, pt_b),
        (pt_a, pt_cp),
        (pt_ap, pt_c),
        (pt_b, pt_cp),
        (pt_bp, pt_c),
    ):
        mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])

    # Luminous golden Pappus Line P-Q-R spanning the entire astrolabe seal
    p_rim_1, p_rim_2 = _line_circle_intersections(pt_p, pt_r, ox, oy, r_seal)
    mb.add_line("golden", p_rim_1[0], p_rim_1[1], p_rim_2[0], p_rim_2[1])
    mb.add_circle("golden", p_rim_1[0], p_rim_1[1], 1.45)
    mb.add_circle("golden", p_rim_2[0], p_rim_2[1], 1.45)

    # Crisp ringed carrier vertices A, B, C and A', B', C'
    for vx, vy in (pt_a, pt_b, pt_c, pt_ap, pt_bp, pt_cp):
        mb.add_circle("primary", vx, vy, 2.2)
        mb.add_circle("golden", vx, vy, 3.2)

    # Bold double-ringed golden Pappus collinear nodes P, Q, R
    for nx, ny in (pt_p, pt_q, pt_r):
        mb.add_circle("golden", nx, ny, 4.3)
        mb.add_circle("golden", nx, ny, 2.35, filled=True)


def _add_arbelos_and_pappus_chain(mb: MedallionBuilder) -> None:
    """Construct Pappus's Arbelos & exact inversion-derived tangent circle chain (Book IV)."""
    ox, oy = MED_CX, MED_CY
    y_base = oy + 18.0  # +10.0, cleanly below Pappus lower carrier line l2
    r_arb = 46.0  # Bottom apex at y = +56.0 (4.0 units inside R_seal = 68.0)
    r_in = 0.5 * r_arb  # Symmetric Arbelos: r = 1/2 -> C_1 centered, twin chains into both cusps

    # Horizontal base diameter & three downward-arching Arbelos semicircles in bold primary
    mb.add_line("primary", ox - r_arb, y_base, ox + r_arb, y_base)
    _add_lower_semicircle(mb, "primary", ox, y_base, r_arb)
    _add_lower_semicircle(mb, "primary", ox - r_in, y_base, r_in)
    _add_lower_semicircle(mb, "primary", ox + r_in, y_base, r_in)

    # Crisp cusp vertex rings at left cusp, central cusp, and right cusp
    for cx_cusp in (ox - r_arb, ox, ox + r_arb):
        mb.add_circle("golden", cx_cusp, y_base, 2.2)
        mb.add_circle("primary", cx_cusp, y_base, 1.1, filled=True)

    # Exact inversion formula for symmetric Arbelos (r = 1/2):
    # For n >= 1, measured from left cusp (ox - r_arb, y_base):
    #   denom = n^2 * (1/4) + 1/2
    #   x_local = r_arb * (3/4) / denom
    #   h_n     = 2 * n * r_arb * (1/4) / denom
    #   r_n     = r_arb * (1/4) / denom
    # Notice h_n == n * (2 * r_n) == n * d_n identically!
    ratio = 0.5
    left_chain: list[tuple[float, float, float, int]] = []
    for n in range(1, 6):
        denom = n * n * (1.0 - ratio) ** 2 + ratio
        x_local = r_arb * ratio * (1.0 + ratio) / denom
        h_n = 2.0 * n * r_arb * ratio * (1.0 - ratio) / denom
        r_n = r_arb * ratio * (1.0 - ratio) / denom
        cx = (ox - r_arb) + x_local
        cy = y_base + h_n

        # Verify exact internal tangency to outer circle, external tangency to
        # left inner circle, and Pappus height law h_n == n * (2 * r_n)
        err_outer = abs(_dist((cx, cy), (ox, y_base)) - (r_arb - r_n))
        err_inner = abs(_dist((cx, cy), (ox - r_in, y_base)) - (r_in + r_n))
        err_height = abs(h_n - n * (2.0 * r_n))
        if max(err_outer, err_inner, err_height) > 1e-10:
            msg = (
                f"Pappus chain invariant failed at n={n}: "
                f"outer={err_outer:.3e}, inner={err_inner:.3e}, height={err_height:.3e}"
            )
            raise ValueError(msg)
        if left_chain:
            prev_cx, prev_cy, prev_r, _ = left_chain[-1]
            err_mut = abs(_dist((cx, cy), (prev_cx, prev_cy)) - (r_n + prev_r))
            if err_mut > 1e-10:
                msg = f"Pappus chain mutual tangency failed at n={n}: {err_mut:.3e}"
                raise ValueError(msg)
        left_chain.append((cx, cy, r_n, n))

    # Draw central circle C_1 and symmetric left/right cascading chains C_2..C_5
    for cx, cy, r_n, n in left_chain:
        if n == 1:
            mb.add_circle("golden", cx, cy, r_n)
            mb.add_circle("detail", cx, cy, r_n * 0.72)
            mb.add_circle("golden", cx, cy, 1.8, filled=True)
        else:
            mb.add_circle("golden", cx, cy, r_n)
            if n <= 3:
                mb.add_circle("golden", cx, cy, 1.15 if n == 2 else 0.85, filled=True)
            rx = 2.0 * ox - cx
            mb.add_circle("golden", rx, cy, r_n)
            if n <= 3:
                mb.add_circle("golden", rx, cy, 1.15 if n == 2 else 0.85, filled=True)

    # Delicate vertical height-law plumb lines h_n = n * d_n on C_1, C'_2, C'_3
    # with crisp golden diameter-unit tick marks
    for cx, cy, r_n, n in left_chain[:3]:
        px = cx if n == 1 else (2.0 * ox - cx)
        d_n = 2.0 * r_n
        mb.add_line("detail", px, y_base, px, cy)
        tick_hw = 1.9 if n == 1 else (1.65 if n == 2 else 1.35)
        if n == 1:
            # Mark single diameter half-step at top tangent of C_1
            mb.add_line("golden", px - tick_hw, y_base + r_n, px + tick_hw, y_base + r_n)
        else:
            for k in range(1, n):
                ty = y_base + k * d_n
                mb.add_line("golden", px - tick_hw, ty, px + tick_hw, ty)


def build_pappus_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Pappus of Alexandria.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)
    _add_pappus_hexagon(mb, r_seal)
    _add_arbelos_and_pappus_chain(mb)

    return mb.build()


def build_pappus_svg(theme: str = "dark") -> str:
    """Render the Pappus of Alexandria medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_pappus_elements()
    return render_medallion_svg(layers, theme=theme)


def write_pappus_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``pappus_dark.svg`` and ``pappus_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "pappus_dark.svg"
    light_path = target_dir / "pappus_light.svg"
    dark_path.write_text(build_pappus_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_pappus_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
