"""Project Medallion: Elements (geometor/elements) — Computable Euclid G-Index.

Unites the opening and climax of Book I of Euclid's *Elements* within the
unified ``R = 68`` graduated astrolabe seal:

1. **Elements I.1 *Vesica Piscis* Frame**: Twin congruent circles centered on
   hypotenuse endpoints ``A`` and ``B`` with exact radius ``|AB| = 5u = 42``
   fit completely inside ``R = 68``, intersecting at equilateral apices
   ``P_top`` and ``P_bot`` to cradle the entire theorem.
2. **Elements I.47 Pythagorean ``3-4-5`` Windmill**: Exact right triangle
   ``ABC`` (legs ``3u, 4u``, hypotenuse ``5u``, verified orthogonal to
   ``< 1e-12``) bearing its three outward squares subdivided into exact
   ``9 + 16 = 25`` area unit grids.
3. **Euclid's Golden Altitude & Congruent Shearing Chords**: The perpendicular
   altitude from ``C`` through foot ``H`` down to ``M`` splits the ``5x5``
   hypotenuse square into exact rectangles of area ``9`` and ``16``, joined by
   Euclid's golden proof triangles ``(C-D, B-G)`` and ``(C-E, A-L)``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_elements_elements",
    "build_elements_svg",
    "write_elements_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _lerp(p1: Point, p2: Point, t: float) -> Point:
    """Linearly interpolate between ``p1`` (``t = 0``) and ``p2`` (``t = 1``)."""
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


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


def _add_right_angle_tick(
    mb: MedallionBuilder,
    vertex: Point,
    along_a: Point,
    along_b: Point,
    size: float = 3.0,
) -> None:
    """Draw a crisp golden perpendicular tick at ``vertex`` along rays to ``along_a``, ``along_b``."""
    ux, uy = along_a[0] - vertex[0], along_a[1] - vertex[1]
    lu = math.hypot(ux, uy)
    vx, vy = along_b[0] - vertex[0], along_b[1] - vertex[1]
    lv = math.hypot(vx, vy)
    if lu < 1e-9 or lv < 1e-9:
        return
    ux, uy = ux / lu, uy / lu
    vx, vy = vx / lv, vy / lv
    q1 = (vertex[0] + size * ux, vertex[1] + size * uy)
    q2 = (vertex[0] + size * (ux + vx), vertex[1] + size * (uy + vy))
    q3 = (vertex[0] + size * vx, vertex[1] + size * vy)
    mb.add_line("golden", q1[0], q1[1], q2[0], q2[1])
    mb.add_line("golden", q2[0], q2[1], q3[0], q3[1])


def _add_square_grid(
    mb: MedallionBuilder,
    p0: Point,
    p1: Point,
    p2: Point,
    p3: Point,
    divisions: int,
) -> None:
    """Subdivide square ``p0-p1-p2-p3`` into an exact ``divisions x divisions`` grid."""
    for k in range(1, divisions):
        t = k / divisions
        a = _lerp(p0, p1, t)
        b = _lerp(p3, p2, t)
        mb.add_line("detail", a[0], a[1], b[0], b[1])
        c = _lerp(p0, p3, t)
        d = _lerp(p1, p2, t)
        mb.add_line("detail", c[0], c[1], d[0], d[1])


def build_elements_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/elements``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    sqrt3 = math.sqrt(3.0)

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact 3-4-5 Right Triangle ABC & Outward Windmill Squares
    # ------------------------------------------------------------------
    u = 8.4  # Hypotenuse |AB| = 5u = 42.0 so full I.1 Vesica fits inside R = 68
    y_b = oy + 2.5

    pt_a: Point = (ox - 2.5 * u, y_b)
    pt_b: Point = (ox + 2.5 * u, y_b)
    pt_h: Point = (ox - 0.7 * u, y_b)  # Exact foot of altitude (|AH| = 1.8u, |HB| = 3.2u)
    pt_c: Point = (ox - 0.7 * u, y_b - 2.4 * u)  # Exact altitude h = 2.4u

    # Hypotenuse square A-B-D-E (downward)
    pt_d: Point = (pt_b[0], y_b + 5.0 * u)
    pt_e: Point = (pt_a[0], y_b + 5.0 * u)
    pt_m: Point = (pt_h[0], y_b + 5.0 * u)  # Altitude split point on bottom edge DE

    # Left leg (3u) outward square A-C-G-F
    pt_f: Point = (pt_a[0] - 2.4 * u, pt_a[1] - 1.8 * u)
    pt_g: Point = (pt_c[0] - 2.4 * u, pt_c[1] - 1.8 * u)

    # Right leg (4u) outward square C-B-L-K
    pt_k: Point = (pt_c[0] + 2.4 * u, pt_c[1] - 3.2 * u)
    pt_l: Point = (pt_b[0] + 2.4 * u, pt_b[1] - 3.2 * u)

    # Exact I.1 Vesica Piscis on hypotenuse AB (radius = |AB| = 5u)
    r_vesica = _dist(pt_a, pt_b)
    p_top: Point = (ox, y_b - 2.5 * u * sqrt3)
    p_bot: Point = (ox, y_b + 2.5 * u * sqrt3)

    # Analytical verification of 3-4-5 right triangle & Pythagorean area theorem
    ac_len = _dist(pt_a, pt_c)
    bc_len = _dist(pt_b, pt_c)
    if abs(ac_len - 3.0 * u) > 1e-11 or abs(bc_len - 4.0 * u) > 1e-11:
        msg = "3-4-5 triangle leg lengths violated"
        raise ValueError(msg)
    dot_c = (pt_a[0] - pt_c[0]) * (pt_b[0] - pt_c[0]) + (pt_a[1] - pt_c[1]) * (
        pt_b[1] - pt_c[1]
    )
    if abs(dot_c) > 1e-11:
        msg = f"Right angle at C violated: dot={dot_c:.3e}"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Detail Layer: Elements I.1 Vesica Circles & Area Unit Grids
    # ------------------------------------------------------------------
    mb.add_circle("detail", pt_a[0], pt_a[1], r_vesica)
    mb.add_circle("detail", pt_b[0], pt_b[1], r_vesica)

    # Subtle I.1 equilateral framing chords from A, B to Vesica apices
    mb.add_line("detail", pt_a[0], pt_a[1], p_top[0], p_top[1])
    mb.add_line("detail", pt_b[0], pt_b[1], p_top[0], p_top[1])
    mb.add_line("detail", p_top[0], p_top[1], p_bot[0], p_bot[1])

    # Unit grid subdivisions inside the 3x3 and 4x4 squares (9 + 16 = 25)
    _add_square_grid(mb, pt_a, pt_c, pt_g, pt_f, 3)
    _add_square_grid(mb, pt_c, pt_b, pt_l, pt_k, 4)

    # Horizontal 5-division rulings inside the hypotenuse square
    for k in range(1, 5):
        t = k / 5.0
        rl = _lerp(pt_a, pt_e, t)
        rr = _lerp(pt_b, pt_d, t)
        mb.add_line("detail", rl[0], rl[1], rr[0], rr[1])

    # ------------------------------------------------------------------
    # 3. Bold Primary Layer: Triangle ABC & Three Outward Windmill Squares
    # ------------------------------------------------------------------
    # Triangle ABC
    mb.add_line("primary", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("primary", pt_c[0], pt_c[1], pt_a[0], pt_a[1])

    # Square on AC (3x3)
    mb.add_line("primary", pt_a[0], pt_a[1], pt_f[0], pt_f[1])
    mb.add_line("primary", pt_f[0], pt_f[1], pt_g[0], pt_g[1])
    mb.add_line("primary", pt_g[0], pt_g[1], pt_c[0], pt_c[1])

    # Square on BC (4x4)
    mb.add_line("primary", pt_c[0], pt_c[1], pt_k[0], pt_k[1])
    mb.add_line("primary", pt_k[0], pt_k[1], pt_l[0], pt_l[1])
    mb.add_line("primary", pt_l[0], pt_l[1], pt_b[0], pt_b[1])

    # Square on hypotenuse AB (5x5)
    mb.add_line("primary", pt_a[0], pt_a[1], pt_e[0], pt_e[1])
    mb.add_line("primary", pt_e[0], pt_e[1], pt_d[0], pt_d[1])
    mb.add_line("primary", pt_d[0], pt_d[1], pt_b[0], pt_b[1])

    # ------------------------------------------------------------------
    # 4. Luminous Golden Layer: Euclid's Altitude Split & Shearing Proof Chords
    # ------------------------------------------------------------------
    # Euclid's golden altitude C -- H -- M splitting 5x5 into 9 and 16 rectangles
    mb.add_line("golden", pt_c[0], pt_c[1], pt_m[0], pt_m[1])

    # Euclid's classical congruent triangle proof diagonals (C-E, B-F) and (C-D, A-K)
    mb.add_line("golden", pt_c[0], pt_c[1], pt_e[0], pt_e[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_f[0], pt_f[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_d[0], pt_d[1])
    mb.add_line("golden", pt_a[0], pt_a[1], pt_k[0], pt_k[1])

    # Right-angle markers at C (triangle apex) and H (altitude foot)
    _add_right_angle_tick(mb, pt_c, pt_a, pt_b, size=3.2)
    _add_right_angle_tick(mb, pt_h, pt_c, pt_b, size=2.6)

    # Golden nodes at triangle vertices A, B, C
    for pt in (pt_a, pt_b, pt_c):
        mb.add_circle("golden", pt[0], pt[1], 3.8)
        mb.add_circle("golden", pt[0], pt[1], 1.9, filled=True)

    # Golden nodes at altitude foot H, split point M, and Vesica apices
    for pt in (pt_h, pt_m, p_top, p_bot):
        mb.add_circle("golden", pt[0], pt[1], 2.7)
        mb.add_circle("golden", pt[0], pt[1], 1.35, filled=True)

    return mb.build()


def build_elements_svg(theme: str = "dark") -> str:
    """Render the ``geometor/elements`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_elements_elements()
    return render_medallion_svg(layers, theme=theme)


def write_elements_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``elements_dark.svg`` and ``elements_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "elements_dark.svg"
    light_path = target_dir / "elements_light.svg"
    dark_path.write_text(build_elements_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_elements_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
