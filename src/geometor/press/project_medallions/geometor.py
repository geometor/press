"""Project Medallion: GEOMETOR (geometor.com) — Central Brand Seal.

The canonical GEOMETOR *Vesica Piscis* to Golden Section (``phi``) construction
framed within the unified ``R = 68`` graduated astrolabe seal:

1. **Twin Congruent Vesica Piscis Circles (``r = 32``)**: Centered on baseline
   ``A = (-16, -8)`` and ``B = (+16, -8)`` (``|AB| = 32``), intersecting at the
   upper and lower equilateral apices ``P`` and ``Q`` to form the twin
   equilateral triangles ``ABP`` and ``ABQ`` and central square scaffold on
   ``AB``.
2. **Exact Golden Section Diameter ``C--A--B--D``**: Swinging the exact
   half-diagonal radius ``|M B_top| = (sqrt(5) / 2) * r`` from midpoint
   ``M = (0, -8)`` cuts the extended baseline at ``C`` and ``D``, satisfying
   ``|AB| / |BD| = |AD| / |AB| = |AB| / |CA| = |CB| / |AB| = phi`` (verified
   to ``< 1e-12``).
3. **Outer Golden Halo ``R * phi`` & Double-Ringed Golden Nodes**: Crowned by
   the golden sweep circle ``(M, r * sqrt(5) / 2)``, the outer golden circle
   ``(M, r * phi)``, golden ratio ticks, and radiant double-ringed nodes at
   ``C, A, M, B, D, P, Q``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_geometor_elements",
    "build_geometor_svg",
    "write_geometor_svgs",
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
    half_tick = 2.3
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


def build_geometor_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for GEOMETOR (geometor.com).

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    sqrt3 = math.sqrt(3.0)
    sqrt5 = math.sqrt(5.0)
    phi = 0.5 * (1.0 + sqrt5)

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Vesica Piscis (r = 32) & Golden Section Coordinates
    # ------------------------------------------------------------------
    r_v = 32.0
    half_r = 0.5 * r_v
    pt_m: Point = (ox, oy)
    pt_a: Point = (ox - half_r, oy)
    pt_b: Point = (ox + half_r, oy)
    pt_p: Point = (ox, oy - half_r * sqrt3)
    pt_q: Point = (ox, oy + half_r * sqrt3)

    # Square corners on AB (upper & lower) whose half-diagonal from M equals r_v * sqrt(5) / 2
    sq_tl: Point = (ox - half_r, oy - r_v)
    sq_tr: Point = (ox + half_r, oy - r_v)
    sq_bl: Point = (ox - half_r, oy + r_v)
    sq_br: Point = (ox + half_r, oy + r_v)

    r_gold_sweep = 0.5 * sqrt5 * r_v
    r_outer_phi = r_v * phi

    pt_c: Point = (ox - r_gold_sweep, oy)
    pt_d: Point = (ox + r_gold_sweep, oy)
    ext_l: Point = (ox - 1.5 * r_v, oy)
    ext_r: Point = (ox + 1.5 * r_v, oy)

    # Verify exact Golden Section invariants to machine precision
    ab_len = _dist(pt_a, pt_b)
    bd_len = _dist(pt_b, pt_d)
    ca_len = _dist(pt_c, pt_a)
    ad_len = _dist(pt_a, pt_d)
    cb_len = _dist(pt_c, pt_b)
    for ratio_val in (ab_len / bd_len, ad_len / ab_len, ab_len / ca_len, cb_len / ab_len):
        if abs(ratio_val - phi) > 1e-12:
            msg = f"GEOMETOR Vesica golden ratio invariant violated: {ratio_val:.15f}"
            raise ValueError(msg)
    if abs(_dist(pt_m, sq_tr) - r_gold_sweep) > 1e-12:
        msg = "Half-diagonal sweep radius invariant violated"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Detail Construction Scaffold: Vertical Axis, Square, & Inner Circle
    # ------------------------------------------------------------------
    mb.add_circle("detail", ox, oy, half_r)  # Central circle on diameter AB
    mb.add_line("detail", ox, oy - r_outer_phi, ox, oy + r_outer_phi)
    mb.add_line("detail", ox - r_seal, oy, pt_c[0], pt_c[1])
    mb.add_line("detail", pt_d[0], pt_d[1], ox + r_seal, oy)

    # Vertical tangents / square construction on AB
    mb.add_line("detail", sq_tl[0], sq_tl[1], sq_bl[0], sq_bl[1])
    mb.add_line("detail", sq_tr[0], sq_tr[1], sq_br[0], sq_br[1])
    mb.add_line("detail", sq_tl[0], sq_tl[1], sq_tr[0], sq_tr[1])
    mb.add_line("detail", sq_bl[0], sq_bl[1], sq_br[0], sq_br[1])

    # Half-diagonal rays from M to square corners establishing sqrt(5)/2 * r
    for corner in (sq_tl, sq_tr, sq_bl, sq_br):
        mb.add_line("detail", ox, oy, corner[0], corner[1])
        mb.add_circle("detail", corner[0], corner[1], 1.2, filled=True)

    # Compass transfer ticks at outer Vesica extremities E_L and E_R
    for ext in (ext_l, ext_r):
        mb.add_circle("detail", ext[0], ext[1], 2.0)

    # ------------------------------------------------------------------
    # 3. Bold Primary Geometry: Twin Vesica Circles & Equilateral Triangles
    # ------------------------------------------------------------------
    mb.add_circle("primary", pt_a[0], pt_a[1], r_v)
    mb.add_circle("primary", pt_b[0], pt_b[1], r_v)

    # Twin equilateral triangles ABP and ABQ
    mb.add_line("primary", pt_a[0], pt_a[1], pt_p[0], pt_p[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_p[0], pt_p[1])
    mb.add_line("primary", pt_a[0], pt_a[1], pt_q[0], pt_q[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_q[0], pt_q[1])
    mb.add_line("primary", pt_p[0], pt_p[1], pt_q[0], pt_q[1])

    # ------------------------------------------------------------------
    # 4. Luminous Golden Layer: Extended Golden Diameter, R*phi Circle & Nodes
    # ------------------------------------------------------------------
    mb.add_circle("golden", ox, oy, r_gold_sweep)
    mb.add_circle("golden", ox, oy, r_outer_phi)

    # Highlighted golden transfer arcs sweeping from square corners down to C and D
    ang_tr = _angle_deg(ox, oy, sq_tr)
    ang_tl = _angle_deg(ox, oy, sq_tl)
    mb.add_arc("golden", ox, oy, r_gold_sweep, ang_tr, 0.0)
    mb.add_arc("golden", ox, oy, r_gold_sweep, 180.0, ang_tl)

    # Radiant extended golden diameter C--A--B--D
    mb.add_line("golden", pt_c[0], pt_c[1], pt_d[0], pt_d[1])
    _add_ratio_tick(mb, pt_c, pt_a, 1)
    _add_ratio_tick(mb, pt_a, pt_b, 2)
    _add_ratio_tick(mb, pt_b, pt_d, 1)

    # Cardinal intersection jewels on the outer R*phi golden circle
    for deg in (0.0, 90.0, 180.0, 270.0):
        gp = polar(ox, oy, r_outer_phi, deg)
        mb.add_circle("golden", gp[0], gp[1], 2.5)
        mb.add_circle("golden", gp[0], gp[1], 1.2, filled=True)

    # Equilateral apices P and Q
    for vx, vy in (pt_p, pt_q):
        mb.add_circle("golden", vx, vy, 3.6)
        mb.add_circle("golden", vx, vy, 1.85, filled=True)

    # Four double-ringed golden hero nodes along C--A--B--D
    for nx_pt, ny_pt in (pt_c, pt_a, pt_b, pt_d):
        mb.add_circle("golden", nx_pt, ny_pt, 4.2)
        mb.add_circle("golden", nx_pt, ny_pt, 2.2, filled=True)

    # Central origin jewel M
    mb.add_circle("golden", ox, oy, 2.8)
    mb.add_circle("golden", ox, oy, 1.35, filled=True)

    return mb.build()


def build_geometor_svg(theme: str = "dark") -> str:
    """Render the GEOMETOR central brand seal SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_geometor_elements()
    return render_medallion_svg(layers, theme=theme)


def write_geometor_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``geometor_dark.svg`` and ``geometor_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "geometor_dark.svg"
    light_path = target_dir / "geometor_light.svg"
    dark_path.write_text(build_geometor_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_geometor_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
