"""Project Medallion: Heptadecagon (geometor/heptadecagon) — Gauss's 17-Gon (1796).

Celebrates Carl Friedrich Gauss's breakthrough ruler-and-compass construction
of the regular 17-gon inside the unified ``R = 68`` graduated astrolabe seal:

1. **Exact Regular 17-Gon Inscribed in ``R = 54``**: Seventeen vertices
   ``P_0..P_16`` anchored at ``P_0 = (R, 0)`` on the horizontal diameter,
   rendered with crisp perimeter edges in ``primary`` and vertex jewels.
2. **Luminous Nested ``{17/5}`` & ``{17/7}`` Star Polygons**: Radiant golden
   ``{17/5}`` heptadecagram paired with a contrasting fine ``{17/7}`` inner
   star polygon revealing the 17-fold harmonic rosette.
3. **Gauss-Richmond Carlyle Construction Circles on the Diameter**: Exact
   quarter-point ``J = (0, -R/4)``, quarter-angle ``E`` and ``45 deg``
   conjugate ``F`` on the horizontal diameter, first Carlyle circle on
   diameter ``F-P_0`` cutting vertical axis at ``K``, and second circle
   ``(E, |EK|)`` cutting the horizontal diameter at ``N_3`` and ``N_5`` —
   whose perpendicular lifts hit exact vertices ``P_3`` and ``P_5`` (verified
   to ``< 1e-12``).
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_heptadecagon_elements",
    "build_heptadecagon_svg",
    "write_heptadecagon_svgs",
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


def build_heptadecagon_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/heptadecagon``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    r_c = 54.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Regular 17-Gon Vertices (P_0 at East, counter-clockwise upward)
    # ------------------------------------------------------------------
    verts: list[Point] = [
        (
            ox + r_c * math.cos(2.0 * math.pi * k / 17.0),
            oy - r_c * math.sin(2.0 * math.pi * k / 17.0),
        )
        for k in range(17)
    ]

    # ------------------------------------------------------------------
    # 2. Exact Gauss-Richmond / Carlyle Construction Along Horizontal Diameter
    # ------------------------------------------------------------------
    pt_j: Point = (ox, oy - 0.25 * r_c)
    theta = 0.25 * math.atan(4.0)  # Exact quarter-angle of angle O-J-P_0
    e_dx = 0.25 * r_c * math.tan(theta)
    f_dx = -0.25 * r_c * math.tan(0.25 * math.pi - theta)

    pt_e: Point = (ox + e_dx, oy)
    pt_f: Point = (ox + f_dx, oy)

    # First Carlyle circle on diameter F--P_0
    m1_x = ox + 0.5 * (f_dx + r_c)
    r_carlyle_1 = 0.5 * (r_c - f_dx)

    # Intersection K with upper vertical axis
    k_dy = math.sqrt(-f_dx * r_c)
    pt_k: Point = (ox, oy - k_dy)

    # Second Carlyle circle centered at E through K (radius |EK|)
    r_carlyle_2 = math.hypot(e_dx, k_dy)
    pt_n3: Point = (ox + e_dx + r_carlyle_2, oy)
    pt_n5: Point = (ox + e_dx - r_carlyle_2, oy)

    # Analytical verification of Gauss's 1796 theorem: N_3_x == P_3_x and N_5_x == P_5_x
    if abs(pt_n3[0] - verts[3][0]) > 1e-11 or abs(pt_n5[0] - verts[5][0]) > 1e-11:
        msg = (
            f"Gauss 17-gon Carlyle invariant violated: "
            f"dN3={abs(pt_n3[0] - verts[3][0]):.3e}, dN5={abs(pt_n5[0] - verts[5][0]):.3e}"
        )
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 3. Detail Layer: {17/7} Inner Star Rosette & Axis Construction Rays
    # ------------------------------------------------------------------
    # Orthogonal diameters inside the 17-gon circumcircle
    mb.add_line("detail", ox - r_c, oy, ox + r_c, oy)
    mb.add_line("detail", ox, oy - r_c, ox, oy + r_c)

    # Nested {17/7} heptadecagram star polygon in fine silver detail
    for k in range(17):
        p_cur = verts[k]
        p_nxt = verts[(k + 7) % 17]
        mb.add_line("detail", p_cur[0], p_cur[1], p_nxt[0], p_nxt[1])

    # Gauss quarter-angle construction rays from J to P_0, E, and F
    mb.add_line("detail", pt_j[0], pt_j[1], verts[0][0], verts[0][1])
    mb.add_line("detail", pt_j[0], pt_j[1], pt_e[0], pt_e[1])
    mb.add_line("detail", pt_j[0], pt_j[1], pt_f[0], pt_f[1])

    # ------------------------------------------------------------------
    # 4. Bold Primary Layer: Circumcircle, Regular 17-Gon, & Carlyle Circles
    # ------------------------------------------------------------------
    mb.add_circle("primary", ox, oy, r_c)
    for k in range(17):
        p_cur = verts[k]
        p_nxt = verts[(k + 1) % 17]
        mb.add_line("primary", p_cur[0], p_cur[1], p_nxt[0], p_nxt[1])

    # Gauss's two Carlyle construction circles along the horizontal diameter
    mb.add_circle("primary", m1_x, oy, r_carlyle_1)
    mb.add_circle("primary", pt_e[0], pt_e[1], r_carlyle_2)

    # ------------------------------------------------------------------
    # 5. Luminous Golden Layer: {17/5} Star Polygon, Vertical Lifts, & Nodes
    # ------------------------------------------------------------------
    for k in range(17):
        p_cur = verts[k]
        p_nxt = verts[(k + 5) % 17]
        mb.add_line("golden", p_cur[0], p_cur[1], p_nxt[0], p_nxt[1])

    # Golden perpendicular lifts from Carlyle cuts N_3 -> P_3 and N_5 -> P_5
    mb.add_line("golden", pt_n3[0], pt_n3[1], verts[3][0], verts[3][1])
    mb.add_line("golden", pt_n5[0], pt_n5[1], verts[5][0], verts[5][1])

    # Golden segment F -- P_0 highlighting the Carlyle diameter
    mb.add_line("golden", pt_f[0], pt_f[1], verts[0][0], verts[0][1])

    # Vertex jewels on all 17 vertices (hero double-ringed stars at P_0, P_3, P_5)
    hero_indices = {0, 3, 5}
    for k, (vx, vy) in enumerate(verts):
        if k in hero_indices:
            mb.add_circle("golden", vx, vy, 3.8)
            mb.add_circle("golden", vx, vy, 1.9, filled=True)
        else:
            mb.add_circle("golden", vx, vy, 1.5, filled=True)

    # Carlyle diameter & axis construction jewels
    for pt in (pt_j, pt_k, pt_e, pt_f, pt_n3, pt_n5):
        mb.add_circle("golden", pt[0], pt[1], 2.4)
        mb.add_circle("golden", pt[0], pt[1], 1.15, filled=True)

    # Central origin jewel
    mb.add_circle("golden", ox, oy, 2.6)
    mb.add_circle("golden", ox, oy, 1.25, filled=True)

    return mb.build()


def build_heptadecagon_svg(theme: str = "dark") -> str:
    """Render the ``geometor/heptadecagon`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_heptadecagon_elements()
    return render_medallion_svg(layers, theme=theme)


def write_heptadecagon_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``heptadecagon_dark.svg`` and ``heptadecagon_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "heptadecagon_dark.svg"
    light_path = target_dir / "heptadecagon_light.svg"
    dark_path.write_text(build_heptadecagon_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_heptadecagon_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
