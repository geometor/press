"""Study 44: Hans Kayser — Pure Sacred Geometric Emblem Medallion.

Celebrates Hans Kayser (1891-1964), founder of modern *Harmonik* (*Lehrbuch der
Harmonik*, 1950), and the **Pythagorean-Kayser Lambdoma (``n/m`` Harmonic Ratio
Lattice)** uniting musical overtone/undertone proportions with exact projective
geometry inside the unified ``R = 68`` graduated astrolabe seal:

1. **Diamond-Rotated ``6 x 6`` Lambdoma Ratio Lattice**: Anchored beneath the
   ``0/0`` apex origin at ``(0, -65)``, the ``45 deg``-rotated square lattice
   of nodes ``(m, n)`` (``1 <= m, n <= 6``) spans symmetrically around
   ``(0, -8)`` with bold primary Undertone (``1/1..1/6``) and Overtone
   (``1/1..6/1``) outer axes and a crisp internal ``detail`` ratio grid.
2. **Radiating Golden Harmonic Interval Rays**: From the unobstructed ``0/0``
   golden star apex, exact constant-ratio projective rays blaze through all
   equivalent fraction nodes (verified collinear to ``< 1e-12``): Unison
   (``1/1..6/6``), Octave (``2/1, 1/2``), Twelfth (``3/1, 1/3``), Perfect
   Fifth (``3/2, 2/3``), Perfect Fourth (``4/3, 3/4``), and Major Third
   (``5/4, 4/5``).
3. **Acoustic Monochord Wave-Front Arcs**: Sweeping concentric circular arcs
   centered at the ``0/0`` origin pass strictly through the unison nodes
   ``(k, k)`` inside the full ``45 deg`` acoustic horn extending cleanly to
   the ``R = 68`` astrolabe rim.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_hans_kayser_elements",
    "build_hans_kayser_svg",
    "write_hans_kayser_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"

Point = tuple[float, float]


def _circle_circle_intersections(
    c1x: float,
    c1y: float,
    r1: float,
    c2x: float,
    c2y: float,
    r2: float,
) -> list[Point]:
    """Return exact intersection points of two circles."""
    dx, dy = c2x - c1x, c2y - c1y
    d = math.hypot(dx, dy)
    if d < 1e-9 or d > r1 + r2 + 1e-9 or d < abs(r1 - r2) - 1e-9:
        return []
    a = (r1 * r1 - r2 * r2 + d * d) / (2.0 * d)
    h_sq = max(0.0, r1 * r1 - a * a)
    h = math.sqrt(h_sq)
    mx = c1x + a * dx / d
    my = c1y + a * dy / d
    if h < 1e-9:
        return [(mx, my)]
    rx = -dy * h / d
    ry = dx * h / d
    return [(mx + rx, my + ry), (mx - rx, my - ry)]


def _ray_circle_intersection(
    origin: Point,
    deg: float,
    cx: float,
    cy: float,
    r: float,
) -> Point:
    """Return the forward intersection of ray ``(origin, deg)`` with circle ``(cx, cy, r)``."""
    rad = math.radians(deg)
    dx, dy = math.cos(rad), math.sin(rad)
    fx, fy = origin[0] - cx, origin[1] - cy
    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - r * r
    disc = b * b - 4.0 * c
    if disc < 0.0:
        msg = "Acoustic cone ray does not intersect seal rim"
        raise ValueError(msg)
    t = 0.5 * (-b + math.sqrt(disc))
    return (origin[0] + t * dx, origin[1] + t * dy)


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


def _add_clipped_wave_arc(
    mb: MedallionBuilder,
    layer: str,
    ax: float,
    ay: float,
    rad: float,
    r_seal: float,
) -> None:
    """Draw a monochord arc centered at ``(ax, ay)`` inside ``[45, 135] deg`` and ``r_seal``."""
    ox, oy = MED_CX, MED_CY
    a_lo, a_hi = 45.0, 135.0
    hits = _circle_circle_intersections(ax, ay, rad, ox, oy, r_seal)
    if len(hits) == 2:
        angs = sorted(math.degrees(math.atan2(hy - ay, hx - ax)) for hx, hy in hits)
        a_lo = max(a_lo, angs[0])
        a_hi = min(a_hi, angs[1])
    if a_hi > a_lo + 1.0:
        mb.add_arc(layer, ax, ay, rad, a_lo, a_hi)


def build_hans_kayser_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Hans Kayser.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Diamond-Rotated 6 x 6 Lambdoma Lattice Coordinates
    # ------------------------------------------------------------------
    step = 9.5
    y0 = oy - 6.0 * step  # -65.0 (11.0 units inside R_seal = 68.0)
    apex: Point = (ox, y0)
    r_apex_halo = 4.1

    def node(m: float, n: float) -> Point:
        """Map Lambdoma ratio coordinates ``(m=undertone, n=overtone)`` to SVG ``(x, y)``."""
        return (ox + (n - m) * step, y0 + (m + n) * step)

    if math.hypot(node(3, 3)[0] - ox, node(3, 3)[1] - oy) > 1e-12:
        msg = "Lambdoma unison center (3, 3) not aligned with medallion center"
        raise ValueError(msg)
    for corner in (apex, node(1, 1), node(6, 1), node(1, 6), node(6, 6)):
        if math.hypot(corner[0] - ox, corner[1] - oy) >= r_seal - 8.0:
            msg = f"Lambdoma corner {corner} too close to seal rim"
            raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Acoustic Horn Cone (45 deg -> R_seal) & Monochord Wave-Fronts
    # ------------------------------------------------------------------
    # Start cone rays cleanly outside the 0/0 golden halo so the apex jewel gleams purely,
    # and run all the way to the astrolabe rim R_seal = 68.0.
    for cone_deg in (45.0, 135.0):
        p_start = polar(apex[0], apex[1], r_apex_halo, cone_deg)
        p_rim = _ray_circle_intersection(apex, cone_deg, ox, oy, r_seal)
        mb.add_line("detail", p_start[0], p_start[1], p_rim[0], p_rim[1])
        mb.add_circle("detail", p_rim[0], p_rim[1], 1.45)

    # Concentric monochord wave-fronts passing strictly through unison nodes (k, k)
    for k in (1, 2, 3, 4, 5):
        rad_k = 2.0 * k * step
        pt_kk = node(k, k)
        if abs(math.hypot(pt_kk[0] - apex[0], pt_kk[1] - apex[1]) - rad_k) > 1e-12:
            msg = f"Monochord wave-front radius mismatch at k={k}"
            raise ValueError(msg)
        _add_clipped_wave_arc(mb, "detail", apex[0], apex[1], rad_k, r_seal)

    # ------------------------------------------------------------------
    # 3. Internal 6 x 6 Lambdoma Grid (detail) & Bold Diamond Frame (primary)
    # ------------------------------------------------------------------
    for k in range(2, 6):
        p_m1, p_m2 = node(k, 1), node(k, 6)
        p_n1, p_n2 = node(1, k), node(6, k)
        mb.add_line("detail", p_m1[0], p_m1[1], p_m2[0], p_m2[1])
        mb.add_line("detail", p_n1[0], p_n1[1], p_n2[0], p_n2[1])

    p11, p61, p16, p66 = node(1, 1), node(6, 1), node(1, 6), node(6, 6)
    mb.add_line("primary", p11[0], p11[1], p61[0], p61[1])
    mb.add_line("primary", p11[0], p11[1], p16[0], p16[1])
    mb.add_line("primary", p61[0], p61[1], p66[0], p66[1])
    mb.add_line("primary", p16[0], p16[1], p66[0], p66[1])

    # ------------------------------------------------------------------
    # 4. Radiating Golden Harmonic Interval Rays from 0/0 Halo
    # ------------------------------------------------------------------
    # Central Unison / Identity Axis 1/1 = 2/2 = 3/3 = 4/4 = 5/5 = 6/6
    mb.add_line("golden", apex[0], apex[1], p66[0], p66[1])

    # Symmetric constant-ratio harmonic rays radiating cleanly from the 0/0 halo
    interval_ratios: tuple[tuple[int, int], ...] = (
        (1, 2),  # Octave (2/1 & 1/2)
        (1, 3),  # Twelfth (3/1 & 1/3)
        (2, 3),  # Perfect Fifth (3/2 & 2/3)
        (3, 4),  # Perfect Fourth (4/3 & 3/4)
        (4, 5),  # Major Third (5/4 & 4/5)
    )
    golden_nodes: set[tuple[int, int]] = {(k, k) for k in range(1, 7)}
    for m_base, n_base in interval_ratios:
        for m_r, n_r in ((m_base, n_base), (n_base, m_base)):
            scale = 6.0 / float(max(m_r, n_r))
            end_pt = node(m_r * scale, n_r * scale)
            dx_e, dy_e = end_pt[0] - apex[0], end_pt[1] - apex[1]
            ray_len = math.hypot(dx_e, dy_e)
            # Start each flanking ray at the outer perimeter of the 0/0 halo for crispness
            start_r = r_apex_halo if (m_base <= 2) else (r_apex_halo + 4.5)
            start_pt = (
                apex[0] + start_r * dx_e / ray_len,
                apex[1] + start_r * dy_e / ray_len,
            )
            mb.add_line("golden", start_pt[0], start_pt[1], end_pt[0], end_pt[1])

            # Analytically verify every equivalent fraction (k*m_r, k*n_r) lies strictly on the ray
            k = 1
            while k * m_r <= 6 and k * n_r <= 6:
                pt_k = node(k * m_r, k * n_r)
                err = abs((pt_k[0] - apex[0]) * dy_e - (pt_k[1] - apex[1]) * dx_e) / ray_len
                if err > 1e-12:
                    msg = f"Harmonic ray collinearity failed at ({k * m_r}, {k * n_r}): {err:.3e}"
                    raise ValueError(msg)
                golden_nodes.add((k * m_r, k * n_r))
                k += 1

    # ------------------------------------------------------------------
    # 5. Lattice Consonance Nodes & Radiant Unison Jewels
    # ------------------------------------------------------------------
    for m in range(1, 7):
        for n in range(1, 7):
            nx, ny = node(m, n)
            if m == n:
                if m in (1, 3, 6):
                    mb.add_circle("golden", nx, ny, 4.0 if m == 3 else 3.5)
                    mb.add_circle("golden", nx, ny, 2.1 if m == 3 else 1.85, filled=True)
                else:
                    mb.add_circle("golden", nx, ny, 2.6)
                    mb.add_circle("golden", nx, ny, 1.45, filled=True)
            elif (m, n) in golden_nodes:
                mb.add_circle("golden", nx, ny, 1.6, filled=True)
            elif m == 1 or n == 1:
                mb.add_circle("golden", nx, ny, 2.15)
                mb.add_circle("primary", nx, ny, 0.95, filled=True)
            else:
                mb.add_circle("detail", nx, ny, 1.2)

    # Radiant unobstructed double-ringed golden 0/0 Origin Star at the apex
    mb.add_circle("golden", apex[0], apex[1], r_apex_halo)
    mb.add_circle("golden", apex[0], apex[1], 2.2, filled=True)

    return mb.build()


def build_hans_kayser_svg(theme: str = "dark") -> str:
    """Render the Hans Kayser medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_hans_kayser_elements()
    return render_medallion_svg(layers, theme=theme)


def write_hans_kayser_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``hans_kayser_dark.svg`` and ``hans_kayser_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "hans_kayser_dark.svg"
    light_path = target_dir / "hans_kayser_light.svg"
    dark_path.write_text(build_hans_kayser_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_hans_kayser_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
