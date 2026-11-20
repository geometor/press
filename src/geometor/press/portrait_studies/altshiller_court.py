"""Study 43: Nathan Altshiller-Court — Pure Sacred Geometric Emblem Medallion.

Celebrates Nathan Altshiller-Court's *College Geometry* (1925 / 1952), the
classic modern Euclidean treatise on the **Orthocentric System ``{A, B, C, H}``**,
its **Four Congruent Circumcircles**, and its single shared **Nine-Point Circle**:

1. **Orthocentric Quartet ``{A, B, C, H}`` & Four Congruent Circumcircles**:
   Centered on the Nine-Point Center ``N = (0, -8)`` inside the unified
   ``R = 68`` graduated astrolabe seal, an upright acute scalene triangle
   ``ABC`` (angles ``50 deg, 60 deg, 70 deg``) and its three altitudes
   ``A-H-D``, ``B-H-E``, ``C-H-F`` (with exact right-angle ticks at feet
   ``D, E, F``) generate a complete, unbroken four-circle rosette of congruent
   circumcircles (``Omega_ABC``, ``Omega_HBC``, ``Omega_HCA``, ``Omega_HAB``),
   each of identical radius ``R_c`` and symmetric about ``N``.
2. **Shared Golden Nine-Point Circle & Orthic Triangle ``DEF``**: The luminous
   golden Nine-Point Circle (radius ``R_c / 2`` centered at ``N``) passes
   through all nine canonical points — three side midpoints, three altitude
   feet ``D, E, F``, and three Euler midpoints of ``HA, HB, HC`` — verified
   concyclic to ``< 1e-12``, framing the unobstructed golden Orthic Triangle
   ``DEF``, the Euler segment ``O_c-N-H``, and double-ringed golden stars at
   ``H`` and ``N``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_altshiller_court_elements",
    "build_altshiller_court_svg",
    "write_altshiller_court_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _mid(p1: Point, p2: Point) -> Point:
    """Return the midpoint of ``p1`` and ``p2``."""
    return (0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1]))


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
    along_side: Point,
    along_alt: Point,
    size: float = 2.8,
) -> None:
    """Draw a crisp perpendicular right-angle square tick at an altitude foot."""
    ux, uy = along_side[0] - foot[0], along_side[1] - foot[1]
    lu = math.hypot(ux, uy)
    vx, vy = along_alt[0] - foot[0], along_alt[1] - foot[1]
    lv = math.hypot(vx, vy)
    if lu < 1e-9 or lv < 1e-9:
        return
    ux, uy = ux / lu, uy / lu
    vx, vy = vx / lv, vy / lv
    p1 = (foot[0] + size * ux, foot[1] + size * uy)
    p2 = (foot[0] + size * vx, foot[1] + size * vy)
    p3 = (p1[0] + size * vx, p1[1] + size * vy)
    mb.add_line("detail", p1[0], p1[1], p3[0], p3[1])
    mb.add_line("detail", p2[0], p2[1], p3[0], p3[1])


def build_altshiller_court_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Nathan Altshiller-Court.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Upright Acute Scalene Orthocentric System {A, B, C, H}
    # ------------------------------------------------------------------
    # Interior angles: A = 50 deg, B = 60 deg, C = 70 deg (central arcs 100, 120, 140 deg).
    # Oriented upright with proud base BC and apex A crowning the upper seal.
    # R_c = 31.6 keeps ALL FOUR congruent circumcircles 100% complete inside R_seal = 68.0.
    r_c = 31.6
    ang_b = 144.0  # Lower-left
    ang_c = 44.0  # Lower-right (arc BC = 100 deg = 2*A)
    ang_a = ang_c - 120.0  # -76 deg, crowning upper seal (arc AC = 120 deg = 2*B; arc BA = 140 = 2*C)

    raw_a = polar(0.0, 0.0, r_c, ang_a)
    raw_b = polar(0.0, 0.0, r_c, ang_b)
    raw_c = polar(0.0, 0.0, r_c, ang_c)
    raw_h: Point = (raw_a[0] + raw_b[0] + raw_c[0], raw_a[1] + raw_b[1] + raw_c[1])
    raw_n: Point = (0.5 * raw_h[0], 0.5 * raw_h[1])

    # Translate so Nine-Point Center N lands directly at medallion center (0, -8)
    sx, sy = ox - raw_n[0], oy - raw_n[1]
    pt_o: Point = (sx, sy)
    pt_a: Point = (raw_a[0] + sx, raw_a[1] + sy)
    pt_b: Point = (raw_b[0] + sx, raw_b[1] + sy)
    pt_c: Point = (raw_c[0] + sx, raw_c[1] + sy)
    pt_h: Point = (raw_h[0] + sx, raw_h[1] + sy)
    pt_n: Point = (ox, oy)

    # Exact altitude feet D (on BC), E (on CA), F (on AB)
    pt_d = _project_to_line(pt_a, pt_b, pt_c)
    pt_e = _project_to_line(pt_b, pt_c, pt_a)
    pt_f = _project_to_line(pt_c, pt_a, pt_b)

    # Side midpoints and Euler midpoints (6 remaining Nine-Point Circle nodes)
    m_a, m_b, m_c = _mid(pt_b, pt_c), _mid(pt_c, pt_a), _mid(pt_a, pt_b)
    e_a, e_b, e_c = _mid(pt_h, pt_a), _mid(pt_h, pt_b), _mid(pt_h, pt_c)

    # Exact Nine-Point Circle radius R_9 = R_c / 2 & analytical concyclicity check
    r_9 = 0.5 * r_c
    nine_points = (pt_d, pt_e, pt_f, m_a, m_b, m_c, e_a, e_b, e_c)
    for idx, pt in enumerate(nine_points):
        err = abs(_dist(pt, pt_n) - r_9)
        if err > 1e-12:
            msg = f"Nine-Point Circle invariant violated at node {idx}: err={err:.3e}"
            raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Four Congruent Circumcircles (Omega_ABC, Omega_HBC, Omega_HCA, Omega_HAB)
    # ------------------------------------------------------------------
    o_a: Point = (pt_h[0] - (pt_a[0] - pt_o[0]), pt_h[1] - (pt_a[1] - pt_o[1]))
    o_b: Point = (pt_h[0] - (pt_b[0] - pt_o[0]), pt_h[1] - (pt_b[1] - pt_o[1]))
    o_cab: Point = (pt_h[0] - (pt_c[0] - pt_o[0]), pt_h[1] - (pt_c[1] - pt_o[1]))

    circle_specs: tuple[tuple[Point, tuple[Point, Point, Point]], ...] = (
        (pt_o, (pt_a, pt_b, pt_c)),
        (o_a, (pt_h, pt_b, pt_c)),
        (o_b, (pt_h, pt_c, pt_a)),
        (o_cab, (pt_h, pt_a, pt_b)),
    )
    for center, triple in circle_specs:
        for v in triple:
            if abs(_dist(center, v) - r_c) > 1e-12:
                msg = "Orthocentric congruent circumcircle radius invariant violated"
                raise ValueError(msg)
        if _dist(center, (ox, oy)) + r_c >= r_seal - 0.3:
            msg = f"Reflected circumcircle at {center} protrudes beyond R_seal = {r_seal}"
            raise ValueError(msg)
        mb.add_circle("detail", center[0], center[1], r_c)
        mb.add_circle("detail", center[0], center[1], 1.35)

    # ------------------------------------------------------------------
    # 3. Bold Primary Triangle ABC & Crisp Altitudes (detail)
    # ------------------------------------------------------------------
    # Keeping ABC bold primary and altitudes crisp detail gives the central
    # golden Nine-Point Circle, Orthic Triangle DEF, and Euler Line full clarity.
    mb.add_line("primary", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("primary", pt_c[0], pt_c[1], pt_a[0], pt_a[1])

    # Three concurrent altitudes A-H-D, B-H-E, C-H-F
    mb.add_line("detail", pt_a[0], pt_a[1], pt_d[0], pt_d[1])
    mb.add_line("detail", pt_b[0], pt_b[1], pt_e[0], pt_e[1])
    mb.add_line("detail", pt_c[0], pt_c[1], pt_f[0], pt_f[1])

    # Crisp perpendicular right-angle square ticks at altitude feet D, E, F
    _add_right_angle_tick(mb, pt_d, pt_b, pt_a, size=2.8)
    _add_right_angle_tick(mb, pt_e, pt_c, pt_b, size=2.8)
    _add_right_angle_tick(mb, pt_f, pt_a, pt_c, size=2.8)

    # ------------------------------------------------------------------
    # 4. Luminous Golden Nine-Point Circle, Orthic Triangle DEF, & Euler Line
    # ------------------------------------------------------------------
    mb.add_circle("golden", pt_n[0], pt_n[1], r_9)

    # Golden Orthic Triangle DEF inscribed inside the Nine-Point Circle
    mb.add_line("golden", pt_d[0], pt_d[1], pt_e[0], pt_e[1])
    mb.add_line("golden", pt_e[0], pt_e[1], pt_f[0], pt_f[1])
    mb.add_line("golden", pt_f[0], pt_f[1], pt_d[0], pt_d[1])

    # Golden Euler Line segment O_c -- N -- H
    mb.add_line("golden", pt_o[0], pt_o[1], pt_h[0], pt_h[1])

    # Crisp golden nodes at all 9 canonical points of the Nine-Point Circle
    for fx, fy in (pt_d, pt_e, pt_f):
        mb.add_circle("golden", fx, fy, 2.5)
        mb.add_circle("golden", fx, fy, 1.35, filled=True)
    for nx, ny in (m_a, m_b, m_c, e_a, e_b, e_c):
        mb.add_circle("golden", nx, ny, 1.45, filled=True)

    # Ringed triangle vertices A, B, C & circumcenter O_c
    for vx, vy in (pt_a, pt_b, pt_c):
        mb.add_circle("golden", vx, vy, 3.6)
        mb.add_circle("golden", vx, vy, 1.9, filled=True)
    mb.add_circle("golden", pt_o[0], pt_o[1], 2.1)

    # Radiant distinct double-ringed golden stars at Orthocenter H and Nine-Point Center N
    mb.add_circle("golden", pt_h[0], pt_h[1], 3.3)
    mb.add_circle("golden", pt_h[0], pt_h[1], 1.75, filled=True)
    mb.add_circle("golden", pt_n[0], pt_n[1], 2.9)
    mb.add_circle("golden", pt_n[0], pt_n[1], 1.45, filled=True)

    return mb.build()


def build_altshiller_court_svg(theme: str = "dark") -> str:
    """Render the Nathan Altshiller-Court medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_altshiller_court_elements()
    return render_medallion_svg(layers, theme=theme)


def write_altshiller_court_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``altshiller_court_dark.svg`` and ``altshiller_court_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "altshiller_court_dark.svg"
    light_path = target_dir / "altshiller_court_light.svg"
    dark_path.write_text(build_altshiller_court_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_altshiller_court_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
