"""Project Medallion: Phyllotaxis — Botanical Golden-Angle Growth.

Sacred geometric emblem for ``geometor/phyllotaxis`` framed within the unified
``R = 68`` graduated astrolabe seal:

1. **Exact Vogel Sunflower Lattice (``n = 1..55``)**: Every floret sits at
   exact golden-angle polar coordinates ``theta_n = n * 360 / phi^2``
   (``137.507764... deg``) and Fermat radius ``r_n = c * sqrt(n)``, scaled to
   fill the botanical receptacle ``R_rec = 60`` with 55 crisp non-overlapping
   circular florets.
2. **Opposing Fibonacci Parastichy Spirals (``8``-Fold & ``13``-Fold)**:
   Exact 3-point circular arcs (zero Beziers) thread every consecutive floret
   pair ``(n, n + 13)`` in crisp ``detail`` clockwise arms and ``(n, n + 8)``
   in luminous ``golden`` counter-clockwise arms, illuminating the dual
   Fibonacci phyllotactic lattice.
3. **Fibonacci Floret Jewels & Golden-Angle Wedge**: Florets indexed by the
   Fibonacci sequence ``(1, 2, 3, 5, 8, 13, 21, 34, 55)`` are crowned with
   radiant golden rings and filled cores, anchored by the central golden-angle
   divergence wedge ``137.508 deg``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_phyllotaxis_elements",
    "build_phyllotaxis_svg",
    "write_phyllotaxis_svgs",
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
    """Add an exact circular arc passing through ``p1 -> pm -> p2`` (fallback to line)."""
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
    if r > 1200.0:
        mb.add_line(layer, x1, y1, x3, y3)
        return
    ang1 = math.degrees(math.atan2(y1 - cy, x1 - cx))
    angm = math.degrees(math.atan2(y2 - cy, x2 - cx))
    ang2 = math.degrees(math.atan2(y3 - cy, x3 - cx))
    # Ensure short span traverses pm
    d12 = (ang2 - ang1 + 180.0) % 360.0 - 180.0
    d1m = (angm - ang1 + 180.0) % 360.0 - 180.0
    if (d12 > 0.0 and not (0.0 < d1m < d12)) or (d12 < 0.0 and not (d12 < d1m < 0.0)):
        mb.add_line(layer, x1, y1, x3, y3)
        return
    mb.add_arc(layer, cx, cy, r, ang1, ang1 + d12)


def build_phyllotaxis_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/phyllotaxis``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    phi = 0.5 * (1.0 + math.sqrt(5.0))
    golden_angle = 360.0 / (phi * phi)  # Exact 137.50776405003785 deg

    if abs(golden_angle - 137.50776405003785) > 1e-11:
        msg = f"Golden angle divergence mismatch: {golden_angle:.15f}"
        raise ValueError(msg)

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Vogel Sunflower Floret Lattice (n = 1..55)
    # ------------------------------------------------------------------
    n_florets = 55
    r_max = 54.5
    c_scale = r_max / math.sqrt(float(n_florets))
    base_deg = -90.0

    florets: dict[int, Point] = {}
    floret_angles: dict[int, float] = {}
    for n in range(1, n_florets + 1):
        rn = c_scale * math.sqrt(float(n))
        ang = base_deg + n * golden_angle
        florets[n] = polar(ox, oy, rn, ang)
        floret_angles[n] = ang

    # Botanical receptacle horizon rings
    mb.add_circle("detail", ox, oy, 59.8)
    mb.add_circle("primary", ox, oy, 61.8)

    # ------------------------------------------------------------------
    # 2. Opposing 13-Fold (Detail) & 8-Fold (Golden) Parastichy Spiral Arcs
    # ------------------------------------------------------------------
    dtheta_13 = ((13.0 * golden_angle + 180.0) % 360.0) - 180.0
    for n in range(1, n_florets - 13 + 1):
        p1 = florets[n]
        p2 = florets[n + 13]
        r_mid = c_scale * math.sqrt(n + 6.5)
        ang_mid = floret_angles[n] + 0.5 * dtheta_13
        pm = polar(ox, oy, r_mid, ang_mid)
        _add_arc_3pt(mb, "detail", p1, pm, p2)

    dtheta_8 = ((8.0 * golden_angle + 180.0) % 360.0) - 180.0
    for n in range(1, n_florets - 8 + 1):
        p1 = florets[n]
        p2 = florets[n + 8]
        r_mid = c_scale * math.sqrt(n + 4.0)
        ang_mid = floret_angles[n] + 0.5 * dtheta_8
        pm = polar(ox, oy, r_mid, ang_mid)
        _add_arc_3pt(mb, "golden", p1, pm, p2)

    # Central golden-angle divergence wedge between n=1 and n=2
    a1 = floret_angles[1]
    a2 = floret_angles[2]
    mb.add_line("golden", ox, oy, florets[1][0], florets[1][1])
    mb.add_line("golden", ox, oy, florets[2][0], florets[2][1])
    mb.add_arc("golden", ox, oy, 6.2, a1, a2)

    # ------------------------------------------------------------------
    # 3. 55 Crisp Circular Florets & Fibonacci Hero Jewels
    # ------------------------------------------------------------------
    fib_set = {1, 2, 3, 5, 8, 13, 21, 34, 55}
    for n in range(1, n_florets + 1):
        fx, fy = florets[n]
        rn = c_scale * math.sqrt(float(n))
        floret_r = 1.65 + 0.022 * rn
        if n in fib_set:
            mb.add_circle("golden", fx, fy, floret_r + 1.35)
            mb.add_circle("golden", fx, fy, floret_r * 0.62, filled=True)
            mb.add_circle("primary", fx, fy, floret_r)
        else:
            mb.add_circle("primary", fx, fy, floret_r)
            mb.add_circle("detail", fx, fy, 0.55, filled=True)

    # Central apical meristem jewel
    mb.add_circle("golden", ox, oy, 2.7)
    mb.add_circle("golden", ox, oy, 1.25, filled=True)

    return mb.build()


def build_phyllotaxis_svg(theme: str = "dark") -> str:
    """Render the Phyllotaxis project medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_phyllotaxis_elements()
    return render_medallion_svg(layers, theme=theme)


def write_phyllotaxis_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``phyllotaxis_dark.svg`` and ``phyllotaxis_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "phyllotaxis_dark.svg"
    light_path = target_dir / "phyllotaxis_light.svg"
    dark_path.write_text(build_phyllotaxis_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_phyllotaxis_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
