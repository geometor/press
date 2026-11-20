"""Author Medallion: Ron Knott — Fibonacci Numbers & Golden Section.

Sacred geometric emblem celebrating Ron Knott's *Fibonacci Numbers and the
Golden Section*, framed within the unified ``R = 68`` graduated astrolabe seal:

1. **Full-Medallion Fibonacci Whirling Squares (``1, 1, 2, 3, 5, 8, 13``)**:
   Exact ``21 x 13`` golden-approximant rectangle (``21 / 13 = 1.61538...``)
   inscribed symmetrically inside its circumcircle ``R_c = 57.42``, dissected
   cleanly into all seven Fibonacci squares from ``13 x 13`` down to the twin
   ``1 x 1`` seed squares.
2. **Continuous ``G1``-Smooth Golden Spiral Chain**: Seven consecutive
   ``90 deg`` circular quarter-arcs sweep seamlessly through every Fibonacci
   square with exact tangent continuity at each stitch corner (zero Beziers),
   accented with double-line golden radiance and stitch jewels.
3. **Homologous Diagonals & Golden Eye Pole**: The two quasi-orthogonal
   whirling-rectangle diagonals intersect at the exact limiting Golden Eye Pole
   ``(441/29, 273/29)`` inside the twin ``1 x 1`` seed chamber, crowned with a
   radiant golden pole star.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_knott_elements",
    "build_knott_svg",
    "write_knott_svgs",
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


def build_knott_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Ron Knott.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact 21 x 13 Fibonacci Golden Rectangle Geometry
    # ------------------------------------------------------------------
    u = 4.65  # Unit Fibonacci grid scale (half-diagonal = 57.42 < 68.0)
    x0 = ox - 10.5 * u
    y0 = oy - 6.5 * u

    def _pt(gx: float, gy: float) -> Point:
        return (x0 + gx * u, y0 + gy * u)

    r_circ = 0.5 * math.hypot(21.0 * u, 13.0 * u)
    mb.add_circle("detail", ox, oy, r_circ)

    # Euclidean golden-rectangle swing arc centered at square-13 base midpoint (6.5, 13)
    m_base = _pt(6.5, 13.0)
    r_euclid = math.hypot(6.5 * u, 13.0 * u)
    a_top = math.degrees(math.atan2(-13.0, 6.5))
    mb.add_arc("detail", m_base[0], m_base[1], r_euclid, a_top, 0.0)
    mb.add_line("detail", m_base[0], m_base[1], _pt(13.0, 0.0)[0], _pt(13.0, 0.0)[1])
    mb.add_circle("detail", m_base[0], m_base[1], 1.4)

    # Subtle internal square diagonals for structural rhythm
    diag_pairs: list[tuple[tuple[float, float], tuple[float, float]]] = [
        ((0.0, 13.0), (13.0, 0.0)),  # Square 13 diagonal
        ((13.0, 0.0), (21.0, 8.0)),  # Square 8 diagonal
        ((21.0, 8.0), (16.0, 13.0)),  # Square 5 diagonal
        ((16.0, 13.0), (13.0, 10.0)),  # Square 3 diagonal
    ]
    for g1, g2 in diag_pairs:
        p1, p2 = _pt(*g1), _pt(*g2)
        mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])

    # ------------------------------------------------------------------
    # 2. Bold Primary 21 x 13 Frame & All 7 Fibonacci Whirling Squares
    # ------------------------------------------------------------------
    # Outer rectangle frame
    c_tl = _pt(0.0, 0.0)
    c_tr = _pt(21.0, 0.0)
    c_br = _pt(21.0, 13.0)
    c_bl = _pt(0.0, 13.0)
    for p1, p2 in ((c_tl, c_tr), (c_tr, c_br), (c_br, c_bl), (c_bl, c_tl)):
        mb.add_line("primary", p1[0], p1[1], p2[0], p2[1])

    # Exact Fibonacci partition cuts: 13 | 8 | 5 | 3 | 2 | 1 | 1
    cuts: list[tuple[tuple[float, float], tuple[float, float]]] = [
        ((13.0, 0.0), (13.0, 13.0)),  # Separates 13 from 8x13
        ((13.0, 8.0), (21.0, 8.0)),  # Separates 8 from 8x5
        ((16.0, 8.0), (16.0, 13.0)),  # Separates 5 from 3x5
        ((13.0, 10.0), (16.0, 10.0)),  # Separates 3 from 3x2
        ((15.0, 8.0), (15.0, 10.0)),  # Separates 2 from 1x2
        ((15.0, 9.0), (16.0, 9.0)),  # Separates twin 1x1 seed squares
    ]
    for g1, g2 in cuts:
        p1, p2 = _pt(*g1), _pt(*g2)
        mb.add_line("primary", p1[0], p1[1], p2[0], p2[1])

    # ------------------------------------------------------------------
    # 3. Homologous Diagonals & Exact Golden Eye Pole (441/29, 273/29)
    # ------------------------------------------------------------------
    # Main diagonal (0, 0) -> (21, 13) and rotated sub-diagonal (21, 0) -> (13, 13)
    d1_a, d1_b = _pt(0.0, 0.0), _pt(21.0, 13.0)
    d2_a, d2_b = _pt(21.0, 0.0), _pt(13.0, 13.0)
    mb.add_line("golden", d1_a[0], d1_a[1], d1_b[0], d1_b[1])
    mb.add_line("golden", d2_a[0], d2_a[1], d2_b[0], d2_b[1])

    pole_gx = 441.0 / 29.0
    pole_gy = 273.0 / 29.0
    # Verify exact collinearity on both diagonals
    err1 = abs(pole_gy - (13.0 / 21.0) * pole_gx)
    err2 = abs(pole_gy - (-13.0 / 8.0) * (pole_gx - 21.0))
    if err1 > 1e-12 or err2 > 1e-12:
        msg = f"Golden eye pole intersection violated: err1={err1}, err2={err2}"
        raise ValueError(msg)
    pole = _pt(pole_gx, pole_gy)

    # ------------------------------------------------------------------
    # 4. Continuous G1-Smooth Chain of Seven 90-deg Golden Spiral Arcs
    # ------------------------------------------------------------------
    # Each entry: (center_gx, center_gy, radius_u, start_deg, end_deg)
    spiral_arcs: list[tuple[float, float, float, float, float]] = [
        (13.0, 13.0, 13.0, 180.0, 270.0),  # Square 13: (0,13) -> (13,0)
        (13.0, 8.0, 8.0, -90.0, 0.0),  # Square 8:  (13,0) -> (21,8)
        (16.0, 8.0, 5.0, 0.0, 90.0),  # Square 5:  (21,8) -> (16,13)
        (16.0, 10.0, 3.0, 90.0, 180.0),  # Square 3:  (16,13) -> (13,10)
        (15.0, 10.0, 2.0, 180.0, 270.0),  # Square 2:  (13,10) -> (15,8)
        (15.0, 9.0, 1.0, -90.0, 0.0),  # Square 1a: (15,8) -> (16,9)
        (15.0, 9.0, 1.0, 0.0, 90.0),  # Square 1b: (16,9) -> (15,10)
    ]

    # Verify exact G1 endpoint continuity between consecutive 90-deg circular arcs
    prev_end: Point | None = None
    for cgx, cgy, ru, a1, a2 in spiral_arcs:
        cx, cy = _pt(cgx, cgy)
        rad = ru * u
        p_start = polar(cx, cy, rad, a1)
        p_end = polar(cx, cy, rad, a2)
        if prev_end is not None and math.hypot(p_start[0] - prev_end[0], p_start[1] - prev_end[1]) > 1e-10:
            msg = "Fibonacci spiral G1 stitch continuity violated"
            raise ValueError(msg)
        prev_end = p_end

        # Primary golden arc + luminous twin highlight track for squares >= 2
        mb.add_arc("golden", cx, cy, rad, a1, a2)
        if ru >= 2.0:
            mb.add_arc("golden", cx, cy, rad - 1.15, a1, a2)

    # Golden stitch jewels at every G1 tangent transition point
    stitch_grid_pts: list[tuple[float, float]] = [
        (0.0, 13.0),
        (13.0, 0.0),
        (21.0, 8.0),
        (16.0, 13.0),
        (13.0, 10.0),
        (15.0, 8.0),
    ]
    for idx, (gx, gy) in enumerate(stitch_grid_pts):
        sx, sy = _pt(gx, gy)
        r_ring = 3.2 if idx < 3 else 2.2
        r_dot = 1.55 if idx < 3 else 1.05
        mb.add_circle("golden", sx, sy, r_ring)
        mb.add_circle("golden", sx, sy, r_dot, filled=True)

    # Four golden rectangle corner pearls
    for vx, vy in (c_tl, c_tr, c_br, c_bl):
        mb.add_circle("golden", vx, vy, 2.4)
        mb.add_circle("golden", vx, vy, 1.15, filled=True)

    # Radiant Golden Eye Pole star
    mb.add_circle("golden", pole[0], pole[1], 3.8)
    mb.add_circle("golden", pole[0], pole[1], 1.75, filled=True)

    return mb.build()


def build_knott_svg(theme: str = "dark") -> str:
    """Render the Ron Knott medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_knott_elements()
    return render_medallion_svg(layers, theme=theme)


def write_knott_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``knott_dark.svg`` and ``knott_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "knott_dark.svg"
    light_path = target_dir / "knott_light.svg"
    dark_path.write_text(build_knott_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_knott_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
