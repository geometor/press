"""Project Medallion: Trees — Stern-Brocot & Farey Ford Circles.

Sacred geometric emblem for ``geometor/trees`` framed within the unified
``R = 68`` graduated astrolabe seal:

1. **Exact Mirrored Ford Circles (``r = S / (2 q^2)``)**: For every reduced
   Farey fraction ``p/q`` in ``[0, 1]`` up to order ``F_6`` (plus depth-3
   Stern-Brocot mediants), exact Ford circles tangent to the central horizontal
   baseline and mutually tangent for every Farey neighbor pair
   (``|p1*q2 - p2*q1| = 1``, verified to ``< 1e-11``) are mirrored symmetrically
   above and below the baseline.
2. **Cathedral Boundary Arcs (``0/1`` & ``1/1``)**: The two grand bounding Ford
   circles ``0/1`` and ``1/1`` (``r = S / 2``) are clipped strictly to the
   ``R = 68`` astrolabe seal, framing the central Farey chamber in exact
   tangency with ``1/2, 1/3, 2/3, 1/4, 3/4``.
3. **Golden Binary Stern-Brocot Tree**: Luminous golden binary branches link
   each Stern-Brocot parent center to its two mediant children mirrored above
   and below the baseline, united by a vertical golden trunk through ``1/2``
   and crowned with radiant center jewels.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_trees_elements",
    "build_trees_svg",
    "write_trees_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point = tuple[float, float]
Frac = tuple[int, int]


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


def _add_clipped_circle_to_seal(
    mb: MedallionBuilder,
    layer: str,
    cx: float,
    cy: float,
    r: float,
    r_seal: float,
) -> None:
    """Add the portion of circle ``(cx, cy, r)`` lying strictly inside ``r_seal``."""
    ox, oy = MED_CX, MED_CY
    d = math.hypot(cx - ox, cy - oy)
    if d + r <= r_seal:
        mb.add_circle(layer, cx, cy, r)
        return
    if d >= r + r_seal or r >= d + r_seal:
        return
    cos_val = (r * r + d * d - r_seal * r_seal) / (2.0 * r * d)
    cos_val = max(-1.0, min(1.0, cos_val))
    base = math.degrees(math.atan2(oy - cy, ox - cx))
    delta = math.degrees(math.acos(cos_val))
    # Inside span is centered on ``base`` (direction from circle center toward seal center)
    if delta <= 179.0:
        mb.add_arc(layer, cx, cy, r, base - delta, base + delta)
    else:
        mb.add_arc(layer, cx, cy, r, base - delta, base)
        mb.add_arc(layer, cx, cy, r, base, base + delta)


def _ford_geometry(frac: Frac, scale: float, sign: float) -> tuple[float, float, float]:
    """Return ``(cx, cy, r)`` for Ford circle ``p/q`` mirrored by ``sign`` (-1 top, +1 bottom)."""
    p, q = frac
    cx = MED_CX + (p / q - 0.5) * scale
    r = scale / (2.0 * q * q)
    cy = MED_CY + sign * r
    return (cx, cy, r)


def build_trees_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/trees``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    scale = 88.0  # [0, 1] maps to [-44, +44]; 0/1 & 1/1 centers sit cleanly inside R_seal

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Farey Sequence & Stern-Brocot Binary Tree Structure
    # ------------------------------------------------------------------
    # Complete Farey F_6 plus depth-3 Stern-Brocot mediants
    farey_set: set[Frac] = set()
    for q in range(1, 7):
        for p in range(0, q + 1):
            if math.gcd(p, q) == 1:
                farey_set.add((p, q))

    # Build Stern-Brocot binary edges on (0, 1) to depth 3
    sb_edges: list[tuple[Frac, Frac]] = []

    def _expand_sb(left: Frac, right: Frac, depth: int) -> Frac:
        med: Frac = (left[0] + right[0], left[1] + right[1])
        farey_set.add(med)
        if depth > 0:
            c_left = _expand_sb(left, med, depth - 1)
            c_right = _expand_sb(med, right, depth - 1)
            sb_edges.append((med, c_left))
            sb_edges.append((med, c_right))
        return med

    _expand_sb((0, 1), (1, 1), 3)

    # Verify exact Ford circle tangency on core Farey neighbors
    core_pairs: list[tuple[Frac, Frac]] = [
        ((0, 1), (1, 2)),
        ((1, 2), (1, 1)),
        ((0, 1), (1, 3)),
        ((1, 3), (1, 2)),
        ((1, 2), (2, 3)),
        ((2, 3), (1, 1)),
        ((1, 4), (1, 3)),
        ((2, 5), (1, 2)),
        ((1, 2), (3, 5)),
        ((2, 3), (3, 4)),
    ]
    for f1, f2 in core_pairs:
        c1x, c1y, r1 = _ford_geometry(f1, scale, -1.0)
        c2x, c2y, r2 = _ford_geometry(f2, scale, -1.0)
        d = math.hypot(c2x - c1x, c2y - c1y)
        if abs(d - (r1 + r2)) > 1e-11:
            msg = f"Ford circle tangency violated for {f1} & {f2}: {d:.12f} != {r1 + r2:.12f}"
            raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Central Baseline & Hyperbolic Farey Geodesic Semicircles
    # ------------------------------------------------------------------
    mb.add_line("primary", ox - r_seal, oy, ox + r_seal, oy)

    # Subtle hyperbolic Farey tessellation semicircles connecting Farey neighbors on baseline
    geodesic_pairs: list[tuple[Frac, Frac]] = [
        ((0, 1), (1, 1)),
        ((0, 1), (1, 2)),
        ((1, 2), (1, 1)),
        ((0, 1), (1, 3)),
        ((1, 3), (1, 2)),
        ((1, 2), (2, 3)),
        ((2, 3), (1, 1)),
    ]
    for f1, f2 in geodesic_pairs:
        x1 = ox + (f1[0] / f1[1] - 0.5) * scale
        x2 = ox + (f2[0] / f2[1] - 0.5) * scale
        mx = 0.5 * (x1 + x2)
        rg = 0.5 * abs(x2 - x1)
        mb.add_arc("detail", mx, oy, rg, 180.0, 360.0)
        mb.add_arc("detail", mx, oy, rg, 0.0, 180.0)

    # ------------------------------------------------------------------
    # 3. Exact Mirrored Ford Circles Above & Below Baseline
    # ------------------------------------------------------------------
    hero_fracs: set[Frac] = {(0, 1), (1, 1), (1, 2), (1, 3), (2, 3), (1, 4), (3, 4)}
    for sign in (-1.0, 1.0):
        for frac in sorted(farey_set, key=lambda f: (f[1], f[0])):
            cx, cy, r = _ford_geometry(frac, scale, sign)
            layer = "primary" if frac in hero_fracs else "detail"
            if frac in ((0, 1), (1, 1)):
                _add_clipped_circle_to_seal(mb, layer, cx, cy, r, r_seal)
            elif r >= 0.65:
                mb.add_circle(layer, cx, cy, r)

    # ------------------------------------------------------------------
    # 4. Golden Binary Stern-Brocot Tree Branches & Center Jewels
    # ------------------------------------------------------------------
    # Vertical golden axis linking upper & lower 1/2 centers through baseline midpoint
    top_half = _ford_geometry((1, 2), scale, -1.0)
    bot_half = _ford_geometry((1, 2), scale, 1.0)
    mb.add_line("golden", top_half[0], top_half[1], bot_half[0], bot_half[1])

    for sign in (-1.0, 1.0):
        # Connect 0/1 and 1/1 grand parent centers to 1/2 root center
        root_x, root_y, _ = _ford_geometry((1, 2), scale, sign)
        for boundary_frac in ((0, 1), (1, 1)):
            bx, by, _ = _ford_geometry(boundary_frac, scale, sign)
            mb.add_line("golden", bx, by, root_x, root_y)
            mb.add_circle("golden", bx, by, 3.0)
            mb.add_circle("golden", bx, by, 1.4, filled=True)

        # Binary Stern-Brocot tree branches connecting exact Ford circle centers
        for parent, child in sb_edges:
            px, py, _ = _ford_geometry(parent, scale, sign)
            cx, cy, _ = _ford_geometry(child, scale, sign)
            mb.add_line("golden", px, py, cx, cy)

        # Golden center jewels scaled by Farey denominator depth
        for frac in ((1, 2), (1, 3), (2, 3), (1, 4), (2, 5), (3, 5), (3, 4)):
            cx, cy, _ = _ford_geometry(frac, scale, sign)
            if frac == (1, 2):
                mb.add_circle("golden", cx, cy, 3.4)
                mb.add_circle("golden", cx, cy, 1.7, filled=True)
            elif frac[1] == 3:
                mb.add_circle("golden", cx, cy, 2.2)
                mb.add_circle("golden", cx, cy, 1.05, filled=True)
            else:
                mb.add_circle("golden", cx, cy, 1.1, filled=True)

    # Crisp golden tangency jewels along the baseline at 0/1, 1/3, 1/2, 2/3, 1/1
    for frac in ((0, 1), (1, 3), (1, 2), (2, 3), (1, 1)):
        tx = ox + (frac[0] / frac[1] - 0.5) * scale
        r_dot = 1.65 if frac == (1, 2) else 1.2
        mb.add_circle("golden", tx, oy, r_dot, filled=True)
        if frac == (1, 2):
            mb.add_circle("golden", tx, oy, 3.0)

    return mb.build()


def build_trees_svg(theme: str = "dark") -> str:
    """Render the Trees project medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_trees_elements()
    return render_medallion_svg(layers, theme=theme)


def write_trees_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``trees_dark.svg`` and ``trees_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "trees_dark.svg"
    light_path = target_dir / "trees_light.svg"
    dark_path.write_text(build_trees_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_trees_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
