"""Project Medallion: Levels — Constructive Depth Stratification.

Sacred geometric emblem for ``geometor/levels`` framed within the unified
``R = 68`` graduated astrolabe seal:

1. **Five Concentric Constructive Depth Strata Rings (``L_0 .. L_4``)**:
   Harmonic stratification centered at ``(0, -8)`` charting the genealogy of
   exact ruler-and-compass generation:

   - ``L_0`` (``r = 11``): Seed Pair ``A, B`` and foundational baseline.
   - ``L_1`` (``r = 22``): Canonical *Vesica Piscis* circles centered at
     ``A, B`` with radius ``|AB| = 22``.
   - ``L_2`` (``r = 33``): 6-pointed Constructive Intersection Star inscribed
     on the outer Vesica envelope ``3a``.
   - ``L_3`` (``r = 44``): Six secondary constructive circles centered on the
     ``L_1`` hexagonal nodes reaching exact outer envelope ``4a``.
   - ``L_4`` (``r = 58``): Outer Constructive Horizon ring crowned with 12
     harmonic depth-horizon jewels.

2. **Radiating Golden Depth-Level Nodes**: Six constructive genealogy rays
   climb outward across all five strata rings with stepped golden node rings,
   connecting segments, and stratum transfer arcs.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_levels_elements",
    "build_levels_svg",
    "write_levels_svgs",
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


def build_levels_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/levels``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Five Concentric Constructive Depth Strata Rings (L_0 .. L_4)
    # ------------------------------------------------------------------
    a = 11.0  # Seed half-spacing
    r_l0 = a  # 11.0: Seed Pair ring
    r_l1 = 2.0 * a  # 22.0: Vesica radius ring
    r_l2 = 3.0 * a  # 33.0: Vesica outer envelope & intersection star
    r_l3 = 4.0 * a  # 44.0: Secondary circles outer envelope
    r_l4 = 58.0  # 58.0: Outer constructive horizon

    # Strata rings: alternate detail & primary for crisp visual hierarchy
    mb.add_circle("detail", ox, oy, r_l0)
    mb.add_circle("detail", ox, oy, r_l1)
    mb.add_circle("primary", ox, oy, r_l2)
    mb.add_circle("detail", ox, oy, r_l3)
    mb.add_circle("primary", ox, oy, r_l4)

    # ------------------------------------------------------------------
    # 2. L_0 Seed Pair & L_1 Vesica Piscis Circles
    # ------------------------------------------------------------------
    pt_a: Point = (ox - a, oy)
    pt_b: Point = (ox + a, oy)
    vesica_h = a * math.sqrt(3.0)
    pt_c: Point = (ox, oy - vesica_h)
    pt_d: Point = (ox, oy + vesica_h)

    # Verify exact equilateral Vesica geometry |AC| == |BC| == |AB| == 2a
    for dist in (
        math.hypot(pt_c[0] - pt_a[0], pt_c[1] - pt_a[1]),
        math.hypot(pt_c[0] - pt_b[0], pt_c[1] - pt_b[1]),
        math.hypot(pt_b[0] - pt_a[0], pt_b[1] - pt_a[1]),
    ):
        if abs(dist - 2.0 * a) > 1e-12:
            msg = f"L_1 Vesica equilateral invariant violated: {dist:.15f}"
            raise ValueError(msg)

    # L_1 Vesica circles centered at A and B with radius 2a (tangent to L_2 at +/-33)
    mb.add_circle("primary", pt_a[0], pt_a[1], 2.0 * a)
    mb.add_circle("primary", pt_b[0], pt_b[1], 2.0 * a)

    # ------------------------------------------------------------------
    # 3. L_2 6-Pointed Constructive Intersection Star (Hexagram)
    # ------------------------------------------------------------------
    star_angles = [-90.0 + 60.0 * k for k in range(6)]
    star_pts = [polar(ox, oy, r_l2, deg) for deg in star_angles]
    # Two interlocked equilateral triangles
    for offset in (0, 1):
        tri = [star_pts[offset], star_pts[offset + 2], star_pts[offset + 4]]
        for j in range(3):
            p1, p2 = tri[j], tri[(j + 1) % 3]
            mb.add_line("primary", p1[0], p1[1], p2[0], p2[1])

    # ------------------------------------------------------------------
    # 4. L_3 Six Secondary Constructive Circles (Centered on L_2, Tangent to L_3)
    # ------------------------------------------------------------------
    # Six secondary circles of radius a = 11 centered at the 6 star vertices on r_l2 = 33
    # reaching exact outer horizon r_l3 = 44 and inner envelope r_l1 = 22!
    for sx, sy in star_pts:
        mb.add_circle("detail", sx, sy, a)

    # Twelve subtle radial horizon ticks between L_3 and L_4
    for k in range(12):
        deg = -90.0 + 30.0 * k
        p_in = polar(ox, oy, r_l3, deg)
        p_out = polar(ox, oy, r_l4, deg)
        if k % 2 == 1:
            mb.add_line("detail", p_in[0], p_in[1], p_out[0], p_out[1])

    # ------------------------------------------------------------------
    # 5. Radiating Golden Depth-Level Genealogy Rays & Stepped Nodes
    # ------------------------------------------------------------------
    # Horizontal seed axis connecting A and B
    mb.add_line("golden", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    # Vertical Vesica axis through C and D
    mb.add_line("golden", pt_c[0], pt_c[1], pt_d[0], pt_d[1])

    # Six radiating golden depth-level climb spokes from L_1 through L_4
    for deg in star_angles:
        p_start = polar(ox, oy, r_l1, deg)
        p_end = polar(ox, oy, r_l4, deg)
        mb.add_line("golden", p_start[0], p_start[1], p_end[0], p_end[1])

    # Golden stepped arc brackets on each stratum celebrating the 5 depth layers
    for r_ring, span in ((r_l1, 14.0), (r_l2, 11.0), (r_l3, 9.0), (r_l4, 8.0)):
        for deg in (-90.0, 30.0, 150.0):
            mb.add_arc("golden", ox, oy, r_ring, deg - span, deg + span)

    # L_0 hero seed jewels at A and B
    for sx, sy in (pt_a, pt_b):
        mb.add_circle("golden", sx, sy, 3.6)
        mb.add_circle("golden", sx, sy, 1.85, filled=True)

    # L_1 Vesica apex jewels at C and D
    for vx, vy in (pt_c, pt_d):
        mb.add_circle("golden", vx, vy, 2.8)
        mb.add_circle("golden", vx, vy, 1.35, filled=True)

    # Climbing golden depth nodes on L_2, L_3, and L_4 along all 6 genealogy rays
    for deg in star_angles:
        p2 = polar(ox, oy, r_l2, deg)
        mb.add_circle("golden", p2[0], p2[1], 2.9)
        mb.add_circle("golden", p2[0], p2[1], 1.4, filled=True)

        p3 = polar(ox, oy, r_l3, deg)
        mb.add_circle("golden", p3[0], p3[1], 2.4)
        mb.add_circle("golden", p3[0], p3[1], 1.15, filled=True)

        p4 = polar(ox, oy, r_l4, deg)
        mb.add_circle("golden", p4[0], p4[1], 3.3)
        mb.add_circle("golden", p4[0], p4[1], 1.65, filled=True)

    # Intermediate L_4 horizon pearls at the 6 odd 30-deg points
    for k in range(6):
        p_mid = polar(ox, oy, r_l4, -60.0 + 60.0 * k)
        mb.add_circle("golden", p_mid[0], p_mid[1], 1.3, filled=True)

    # Origin pivot jewel
    mb.add_circle("golden", ox, oy, 1.5, filled=True)

    return mb.build()


def build_levels_svg(theme: str = "dark") -> str:
    """Render the Levels project medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_levels_elements()
    return render_medallion_svg(layers, theme=theme)


def write_levels_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``levels_dark.svg`` and ``levels_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "levels_dark.svg"
    light_path = target_dir / "levels_light.svg"
    dark_path.write_text(build_levels_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_levels_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
