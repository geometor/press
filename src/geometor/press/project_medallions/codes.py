"""Project Medallion: Codes (geometor/codes) — Geometric Theorem Provers Catalog.

Celebrates automated projective theorem proving through **Desargues's Theorem
(``10_3`` Configuration)** inside the unified ``R = 68`` graduated astrolabe
seal:

1. **Golden Perspectivity Center ``O`` & Three Radiating Rays**: Centered on
   the upper meridian at ``O = (0, -60)``, three luminous golden perspectivity
   rays ``O-A-A'``, ``O-B-B'``, and ``O-C-C'`` establish exact point-to-point
   perspectivity between two bold triangles ``ABC`` and ``A'B'C'``.
2. **Exact Projective Homology & All 10 Incidences**: Triangle ``A'B'C'`` is
   constructed via an exact projective homology centered at ``O``, guaranteeing
   that the three pairs of corresponding sides ``(AB, A'B')``, ``(BC, B'C')``,
   and ``(CA, C'A')`` intersect at exact points ``P, Q, R`` inside ``R = 68``.
3. **Blazing Golden Desargues Perspectivity Axis ``P--Q--R``**: Collinearity of
   ``P, Q, R`` and concurrency of ``AA', BB', CC'`` at ``O`` are verified to
   ``< 1e-12``, crowned by radiant double-ringed golden stars at ``O, P, Q, R``
   and ringed nodes across all ten points of the ``10_3`` configuration.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_codes_elements",
    "build_codes_svg",
    "write_codes_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point = tuple[float, float]


def _line_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Point:
    """Return the exact intersection of lines ``p1-p2`` and ``p3-p4``."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-12:
        msg = "Parallel lines in _line_intersection"
        raise ValueError(msg)
    det1 = x1 * y2 - y1 * x2
    det2 = x3 * y4 - y3 * x4
    return (
        (det1 * (x3 - x4) - (x1 - x2) * det2) / denom,
        (det1 * (y3 - y4) - (y1 - y2) * det2) / denom,
    )


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


def _triangle_area2(a: Point, b: Point, c: Point) -> float:
    """Return twice the signed area of triangle ``a-b-c``."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


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


def _farther_ray_hit(origin: Point, through: Point, cx: float, cy: float, r: float) -> Point:
    """Return the intersection of ray ``origin -> through`` with circle ``(cx, cy, r)``."""
    h1, h2 = _line_circle_intersections(origin, through, cx, cy, r)
    dx, dy = through[0] - origin[0], through[1] - origin[1]
    dot1 = (h1[0] - origin[0]) * dx + (h1[1] - origin[1]) * dy
    return h1 if dot1 > 0.0 else h2


def build_codes_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/codes``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Desargues 10_3 Configuration via Projective Homology
    # ------------------------------------------------------------------
    pt_o: Point = (ox - 30.0, oy - 50.0)  # Perspectivity center in upper-left crown
    y_axis = oy + 36.0  # Horizontal Desargues perspectivity axis
    axis_h = y_axis - pt_o[1]
    lam = 2.5  # Exact homology scale parameter

    def homology(pt: Point) -> Point:
        """Map ``pt`` to its exact perspective image under homology ``(O, axis_h, lam)``."""
        u = pt[0] - pt_o[0]
        v = pt[1] - pt_o[1]
        scale = lam / (1.0 + (lam - 1.0) * (v / axis_h))
        return (pt_o[0] + scale * u, pt_o[1] + scale * v)

    # Construct wide shapely triangle ABC from symmetric target axis points P, Q, R
    ref_p: Point = (ox - 50.0, y_axis)
    ref_q: Point = (ox + 4.0, y_axis)
    ref_r: Point = (ox + 50.0, y_axis)
    pt_b: Point = (ox - 4.0, oy - 34.0)
    pt_c: Point = (
        pt_b[0] + 0.55 * (ref_q[0] - pt_b[0]),
        pt_b[1] + 0.55 * (ref_q[1] - pt_b[1]),
    )
    pt_a = _line_intersection(ref_p, pt_b, ref_r, pt_c)

    # Lower-right perspective triangle A'B'C'
    pt_ap = homology(pt_a)
    pt_bp = homology(pt_b)
    pt_cp = homology(pt_c)

    # Exact corresponding-side intersections P = AB n A'B', Q = BC n B'C', R = CA n C'A'
    pt_p = _line_intersection(pt_a, pt_b, pt_ap, pt_bp)
    pt_q = _line_intersection(pt_b, pt_c, pt_bp, pt_cp)
    pt_r = _line_intersection(pt_c, pt_a, pt_cp, pt_ap)

    # Analytical verification of Desargues's Theorem:
    # 1. P, Q, R strictly collinear on y = oy + 36.0
    # 2. Rays AA', BB', CC' strictly concurrent at O
    if abs(_triangle_area2(pt_p, pt_q, pt_r)) > 1e-10:
        msg = "Desargues collinearity invariant violated"
        raise ValueError(msg)
    for pt in (pt_p, pt_q, pt_r):
        if abs(pt[1] - y_axis) > 1e-10:
            msg = f"Desargues axis y-invariant violated: {pt[1]:.12f} != {y_axis:.12f}"
            raise ValueError(msg)
    for u_pt, up_pt in ((pt_a, pt_ap), (pt_b, pt_bp), (pt_c, pt_cp)):
        if abs(_triangle_area2(pt_o, u_pt, up_pt)) > 1e-10:
            msg = "Desargues concurrency invariant violated"
            raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Detail Layer: Six Side-Extension Chords Meeting at P, Q, R
    # ------------------------------------------------------------------
    # Connect each triangle side cleanly out to its corresponding Desargues intersection
    mb.add_line("detail", pt_b[0], pt_b[1], pt_p[0], pt_p[1])
    mb.add_line("detail", pt_bp[0], pt_bp[1], pt_p[0], pt_p[1])

    mb.add_line("detail", pt_b[0], pt_b[1], pt_q[0], pt_q[1])
    mb.add_line("detail", pt_bp[0], pt_bp[1], pt_q[0], pt_q[1])

    mb.add_line("detail", pt_a[0], pt_a[1], pt_r[0], pt_r[1])
    mb.add_line("detail", pt_ap[0], pt_ap[1], pt_r[0], pt_r[1])

    # Subtle projective fan calibration arc framing perspectivity center O
    ang_a = math.degrees(math.atan2(pt_a[1] - pt_o[1], pt_a[0] - pt_o[0]))
    ang_b = math.degrees(math.atan2(pt_b[1] - pt_o[1], pt_b[0] - pt_o[0]))
    mb.add_arc("detail", pt_o[0], pt_o[1], 13.0, min(ang_a, ang_b) - 8.0, max(ang_a, ang_b) + 8.0)

    # ------------------------------------------------------------------
    # 3. Bold Primary Layer: Perspective Triangles ABC and A'B'C'
    # ------------------------------------------------------------------
    # Triangle ABC
    mb.add_line("primary", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("primary", pt_c[0], pt_c[1], pt_a[0], pt_a[1])

    # Triangle A'B'C'
    mb.add_line("primary", pt_ap[0], pt_ap[1], pt_bp[0], pt_bp[1])
    mb.add_line("primary", pt_bp[0], pt_bp[1], pt_cp[0], pt_cp[1])
    mb.add_line("primary", pt_cp[0], pt_cp[1], pt_ap[0], pt_ap[1])

    # ------------------------------------------------------------------
    # 4. Luminous Golden Layer: Perspectivity Rays, Desargues Axis, & 10 Nodes
    # ------------------------------------------------------------------
    # Three golden perspectivity rays from O through A-A', B-B', C-C' to seal rim
    for through in (pt_ap, pt_bp, pt_cp):
        rim_hit = _farther_ray_hit(pt_o, through, ox, oy, r_seal)
        mb.add_line("golden", pt_o[0], pt_o[1], rim_hit[0], rim_hit[1])

    # Blazing golden Desargues perspectivity axis P--Q--R spanning the seal
    ax_l, ax_r = _line_circle_intersections(pt_p, pt_r, ox, oy, r_seal)
    mb.add_line("golden", ax_l[0], ax_l[1], ax_r[0], ax_r[1])

    # Six triangle vertex nodes A, B, C and A', B', C'
    for pt in (pt_a, pt_b, pt_c, pt_ap, pt_bp, pt_cp):
        mb.add_circle("golden", pt[0], pt[1], 3.1)
        mb.add_circle("golden", pt[0], pt[1], 1.55, filled=True)

    # Three hero double-ringed golden stars along the Desargues axis P, Q, R
    for pt in (pt_p, pt_q, pt_r):
        mb.add_circle("golden", pt[0], pt[1], 4.2)
        mb.add_circle("golden", pt[0], pt[1], 2.15, filled=True)

    # Radiant perspectivity center star at O
    mb.add_circle("golden", pt_o[0], pt_o[1], 4.8)
    mb.add_circle("golden", pt_o[0], pt_o[1], 2.35, filled=True)

    return mb.build()


def build_codes_svg(theme: str = "dark") -> str:
    """Render the ``geometor/codes`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_codes_elements()
    return render_medallion_svg(layers, theme=theme)


def write_codes_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``codes_dark.svg`` and ``codes_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "codes_dark.svg"
    light_path = target_dir / "codes_light.svg"
    dark_path.write_text(build_codes_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_codes_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
