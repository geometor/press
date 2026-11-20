"""Project Medallion: Divine (geometor/divine) — Golden Ratio Discovery Engine.

Celebrates automated golden-section discovery inside the unified ``R = 68``
graduated astrolabe seal through the supreme fivefold geometry of ``phi``:

1. **Regular Pentagon & Inscribed ``{5/2}`` Pentagram Star**: Upright regular
   pentagon inscribed in circumcircle ``R_5 = 54`` with all five chords forming
   the radiant golden ``{5/2}`` pentagram, generating the exact inverted inner
   pentagon at ``R_5 / phi^2`` and a nested micro-pentagram at its heart.
2. **Exact ``1 : phi : phi^2`` Nested Golden Circles & Compass Arcs**: Three
   concentric golden-progression circles (``R_5 / phi^2``, ``R_5 / phi``,
   ``R_5``) paired with ten compass-transfer arcs from the pentagon vertices
   sweeping directly through the exact golden-cut intersections of every chord
   (all ratios verified to ``< 1e-12``).
3. **Harmonic Golden Chord Ticks & Star Jewels**: Calibrated golden ratio ticks
   along the horizontal pentagram chord illuminate ``1/phi : 1/phi^2 : 1/phi``,
   crowned by double-ringed golden nodes at all ten star vertices and center.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_divine_elements",
    "build_divine_svg",
    "write_divine_svgs",
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
    spacing = 2.1
    half_tick = 2.0
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


def build_divine_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/divine``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    phi = 0.5 * (1.0 + math.sqrt(5.0))

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Regular Pentagon & Inner Inverted Pentagon via Intersections
    # ------------------------------------------------------------------
    r_outer = 54.0
    r_mid = r_outer / phi
    r_inner = r_outer / (phi * phi)

    verts: list[Point] = [polar(ox, oy, r_outer, -90.0 + 72.0 * k) for k in range(5)]

    # Inner pentagon vertices U_k = intersection of chords (V_k, V_{k+2}) and (V_{k+1}, V_{k+4})
    inner: list[Point] = [
        _line_intersection(
            verts[k],
            verts[(k + 2) % 5],
            verts[(k + 1) % 5],
            verts[(k + 4) % 5],
        )
        for k in range(5)
    ]

    # Verify exact 1 : phi : phi^2 pentagram invariants to machine precision
    side_len = _dist(verts[0], verts[1])
    chord_len = _dist(verts[0], verts[2])
    wing_len = _dist(verts[0], inner[0])
    core_len = _dist(inner[0], inner[1])
    for val in (
        chord_len / side_len,
        side_len / wing_len,
        wing_len / core_len,
        r_outer / r_mid,
        r_mid / r_inner,
        r_inner / _dist((ox, oy), inner[0]) * phi / phi,
    ):
        if abs(val - phi) > 1e-11 and abs(val - 1.0) > 1e-11:
            msg = f"Pentagram golden invariant violated: {val:.15f}"
            raise ValueError(msg)
    if abs(_dist((ox, oy), inner[0]) - r_inner) > 1e-11:
        msg = "Inner pentagon circumradius invariant violated"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Detail Layer: 1 : phi : phi^2 Concentric Circles & Compass Arcs
    # ------------------------------------------------------------------
    mb.add_circle("detail", ox, oy, r_mid)
    mb.add_circle("detail", ox, oy, r_inner)
    mb.add_circle("detail", ox, oy, r_inner / phi)

    # Exact compass-section arcs from each outer vertex V_k sweeping across
    # the two adjacent inner golden cut nodes (radius = wing_len = side / phi)
    for k in range(5):
        vx, vy = verts[k]
        u_right = inner[k]
        u_left = inner[(k - 1) % 5]
        a1 = _angle_deg(vx, vy, u_right)
        a2 = _angle_deg(vx, vy, u_left)
        mb.add_arc("detail", vx, vy, wing_len, a1, a2)

    # Outer golden-transfer compass arcs centered on each vertex V_k of radius = side_len
    # sweeping gracefully inside the circumcircle between neighboring golden cuts
    for k in range(5):
        vx, vy = verts[k]
        target_a = inner[(k + 1) % 5]
        target_b = inner[(k - 2) % 5]
        a1 = _angle_deg(vx, vy, target_a)
        a2 = _angle_deg(vx, vy, target_b)
        mb.add_arc("golden", vx, vy, side_len, a1, a2)

    # Radial symmetry spokes from center through vertices in detail
    for vx, vy in verts:
        mb.add_line("detail", ox, oy, vx, vy)

    # ------------------------------------------------------------------
    # 3. Bold Primary Layer: Circumcircle, Outer Pentagon, & Inner Pentagon
    # ------------------------------------------------------------------
    mb.add_circle("primary", ox, oy, r_outer)
    for k in range(5):
        p_cur = verts[k]
        p_nxt = verts[(k + 1) % 5]
        mb.add_line("primary", p_cur[0], p_cur[1], p_nxt[0], p_nxt[1])

    for k in range(5):
        u_cur = inner[k]
        u_nxt = inner[(k + 1) % 5]
        mb.add_line("primary", u_cur[0], u_cur[1], u_nxt[0], u_nxt[1])

    # ------------------------------------------------------------------
    # 4. Luminous Golden Layer: {5/2} Pentagram, Nested Micro-Star & Jewels
    # ------------------------------------------------------------------
    for k in range(5):
        p_cur = verts[k]
        p_star = verts[(k + 2) % 5]
        mb.add_line("golden", p_cur[0], p_cur[1], p_star[0], p_star[1])

    # Nested inner {5/2} micro-pentagram inside inner pentagon
    for k in range(5):
        u_cur = inner[k]
        u_star = inner[(k + 2) % 5]
        mb.add_line("golden", u_cur[0], u_cur[1], u_star[0], u_star[1])

    # Harmonic ratio ticks on horizontal pentagram chord V_4 -- U_3 -- U_0 -- V_1
    _add_ratio_tick(mb, verts[4], inner[4], 2)
    _add_ratio_tick(mb, inner[4], inner[0], 1)
    _add_ratio_tick(mb, inner[0], verts[1], 2)

    # Outer pentagon double-ringed golden vertex stars
    for vx, vy in verts:
        mb.add_circle("golden", vx, vy, 3.9)
        mb.add_circle("golden", vx, vy, 2.0, filled=True)

    # Five golden inner pentagram intersection jewels
    for ux, uy in inner:
        mb.add_circle("golden", ux, uy, 2.8)
        mb.add_circle("golden", ux, uy, 1.4, filled=True)

    # Central golden sun jewel
    mb.add_circle("golden", ox, oy, 3.2)
    mb.add_circle("golden", ox, oy, 1.6, filled=True)

    return mb.build()


def build_divine_svg(theme: str = "dark") -> str:
    """Render the ``geometor/divine`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_divine_elements()
    return render_medallion_svg(layers, theme=theme)


def write_divine_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``divine_dark.svg`` and ``divine_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "divine_dark.svg"
    light_path = target_dir / "divine_light.svg"
    dark_path.write_text(build_divine_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_divine_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
