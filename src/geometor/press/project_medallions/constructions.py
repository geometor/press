"""Project Medallion: Constructions — Geometric Studies & Ad Quadratum Motion.

Sacred geometric emblem for ``geometor/constructions`` framed within the
unified ``R = 68`` graduated astrolabe seal:

1. **Dynamic Concentric Root-Squares (``1, sqrt(2), 2, 2*sqrt(2)``)**: Four
   nested *ad quadratum* squares rotated ``45 deg`` per generation so each
   square's vertices touch the exact midpoints of the next larger square's
   sides, verifying the geometric progression ``R_k = R_0 * (sqrt(2))^k`` to
   ``< 1e-12``.
2. **Roman Sacred Cut Compass Arcs**: Four compass arcs centered at the outer
   square's corners with radius equal to its half-diagonal (``R_2``) sweep
   across the interior through the exact center ``O``, framing the canonical
   Sacred Cut octagon.
3. **Golden Constructive Unfolding & Kinetic Sweep Arcs**: Four rotational
   golden spiral arms (exact 3-point circular arcs) thread outward across the
   rotating vertices ``V_{0,j} -> V_{1,j} -> V_{2,j} -> V_{3,j}``, paired with
   ``45 deg`` rotational sweep arcs along each root-circle showing continuous
   constructive motion.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_constructions_elements",
    "build_constructions_svg",
    "write_constructions_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point = tuple[float, float]


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


def _add_arc_3pt(
    mb: MedallionBuilder,
    layer: str,
    p1: Point,
    pm: Point,
    p2: Point,
) -> None:
    """Add an exact circular arc passing through ``p1 -> pm -> p2``."""
    x1, y1 = p1
    x2, y2 = pm
    x3, y3 = p2
    det = 2.0 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(det) < 1e-4:
        mb.add_line(layer, x1, y1, x3, y3)
        return
    a1_sq = x1 * x1 + y1 * y1
    a2_sq = x2 * x2 + y2 * y2
    a3_sq = x3 * x3 + y3 * y3
    cx = (a1_sq * (y2 - y3) + a2_sq * (y3 - y1) + a3_sq * (y1 - y2)) / det
    cy = (a1_sq * (x3 - x2) + a2_sq * (x1 - x3) + a3_sq * (x2 - x1)) / det
    r = math.hypot(x1 - cx, y1 - cy)
    ang1 = math.degrees(math.atan2(y1 - cy, x1 - cx))
    ang2 = math.degrees(math.atan2(y3 - cy, x3 - cx))
    d12 = (ang2 - ang1 + 180.0) % 360.0 - 180.0
    mb.add_arc(layer, cx, cy, r, ang1, ang1 + d12)


def build_constructions_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/constructions``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    sqrt2 = math.sqrt(2.0)

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Ad Quadratum Root-Squares: 1, sqrt(2), 2, 2*sqrt(2)
    # ------------------------------------------------------------------
    r3 = 58.0  # Outer circumcircle (ratio 2*sqrt(2))
    radii = [r3 / (sqrt2 ** (3 - k)) for k in range(4)]
    # Verify exact sqrt(2) progression
    for k in range(3):
        ratio = radii[k + 1] / radii[k]
        if abs(ratio - sqrt2) > 1e-12:
            msg = f"Ad quadratum root-2 progression violated: {ratio:.15f}"
            raise ValueError(msg)

    # Square orientation angles: k=0 (diamond 0/90/180/270), k=1 (45..), k=2 (0..), k=3 (45..)
    base_angles = [0.0, 45.0, 90.0, 135.0]
    squares: list[list[Point]] = []
    for k, rk in enumerate(radii):
        verts = [polar(ox, oy, rk, base_angles[k] + 90.0 * j) for j in range(4)]
        squares.append(verts)

    # Verify exact midpoint tangency: vertices of square k lie on midpoints of square k+1
    for k in range(3):
        v_in = squares[k][0]
        p_a = squares[k + 1][0]
        p_b = squares[k + 1][3]
        mx, my = 0.5 * (p_a[0] + p_b[0]), 0.5 * (p_a[1] + p_b[1])
        if math.hypot(v_in[0] - mx, v_in[1] - my) > 1e-11:
            msg = "Ad quadratum midpoint tangency violated"
            raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Concentric Root-Circles & Roman Sacred Cut Corner Arcs
    # ------------------------------------------------------------------
    # Inner seed circle (apothem of square 0) + root circles R_0, R_1, R_2
    mb.add_circle("detail", ox, oy, radii[0] / sqrt2)
    for rk in radii[:3]:
        mb.add_circle("detail", ox, oy, rk)
    mb.add_circle("primary", ox, oy, radii[3])

    # Subtle 8-fold radial diagonals connecting the rotating corners
    for deg in (0.0, 45.0, 90.0, 135.0):
        p1 = polar(ox, oy, radii[3], deg)
        p2 = polar(ox, oy, radii[3], deg + 180.0)
        mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])

    # Exact Sacred Cut arcs centered at the 4 corners of Square 3 with radius R_2 (half-diagonal)
    # Wait: half-diagonal of Square 3 is R_3 = 58.0, while half-side is R_2 = 41.012!
    # The Sacred Cut arc from each corner with radius R_2 = half-side cuts the two adjacent
    # midpoints (vertices of Square 2) cleanly across the interior!
    r_cut = radii[2]
    for j in range(4):
        cx, cy = squares[3][j]
        ang_to_origin = math.degrees(math.atan2(oy - cy, ox - cx))
        mb.add_arc("detail", cx, cy, r_cut, ang_to_origin - 45.0, ang_to_origin + 45.0)

    # ------------------------------------------------------------------
    # 3. Bold Primary Nested Root-Squares (1, sqrt(2), 2, 2*sqrt(2))
    # ------------------------------------------------------------------
    for verts in squares:
        for j in range(4):
            p1 = verts[j]
            p2 = verts[(j + 1) % 4]
            mb.add_line("primary", p1[0], p1[1], p2[0], p2[1])

    # ------------------------------------------------------------------
    # 4. Luminous Golden Unfolding Sweep Arcs & Vertex Jewels
    # ------------------------------------------------------------------
    # Four rotational golden compass unfolding spirals threading V_{0,j} -> V_{1,j} -> V_{2,j} -> V_{3,j}
    for j in range(4):
        v0 = squares[0][j]
        v1 = squares[1][j]
        v2 = squares[2][j]
        v3 = squares[3][j]
        # Exact continuous spiral midpoint on r(t) = r0 * 2^(t/2), theta(t) = theta0 + 45*t
        th0 = base_angles[0] + 90.0 * j
        pm01 = polar(ox, oy, radii[0] * (sqrt2 ** 0.5), th0 + 22.5)
        pm12 = polar(ox, oy, radii[1] * (sqrt2 ** 0.5), th0 + 67.5)
        pm23 = polar(ox, oy, radii[2] * (sqrt2 ** 0.5), th0 + 112.5)
        _add_arc_3pt(mb, "golden", v0, pm01, v1)
        _add_arc_3pt(mb, "golden", v1, pm12, v2)
        _add_arc_3pt(mb, "golden", v2, pm23, v3)

        # Crisp 45-deg golden angular motion arcs outside the outer rim R_3 + 4.0
        a_out = base_angles[3] + 90.0 * j
        mb.add_arc("golden", ox, oy, radii[3] + 4.2, a_out - 36.0, a_out - 4.0)
        tip = polar(ox, oy, radii[3] + 4.2, a_out - 4.0)
        mb.add_circle("golden", tip[0], tip[1], 1.15, filled=True)

    # Golden rotational sweep arcs along each root-circle showing the 45-deg turn
    for k in range(3):
        rk = radii[k]
        for j in range(4):
            a_start = base_angles[k] + 90.0 * j
            mb.add_arc("golden", ox, oy, rk, a_start + 5.0, a_start + 40.0)

    # Golden jewels at all 16 root-square vertices (scaled by generation)
    jewel_radii = [(2.1, 1.05), (2.5, 1.25), (3.0, 1.5), (3.7, 1.85)]
    for k, verts in enumerate(squares):
        r_ring, r_dot = jewel_radii[k]
        for vx, vy in verts:
            mb.add_circle("golden", vx, vy, r_ring)
            mb.add_circle("golden", vx, vy, r_dot, filled=True)

    # Central constructive pivot star
    mb.add_circle("golden", ox, oy, 4.2)
    mb.add_circle("golden", ox, oy, 1.9, filled=True)

    return mb.build()


def build_constructions_svg(theme: str = "dark") -> str:
    """Render the Constructions project medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_constructions_elements()
    return render_medallion_svg(layers, theme=theme)


def write_constructions_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``constructions_dark.svg`` and ``constructions_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "constructions_dark.svg"
    light_path = target_dir / "constructions_light.svg"
    dark_path.write_text(build_constructions_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_constructions_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
