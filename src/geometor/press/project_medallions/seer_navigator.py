"""Project Medallion: Seer Navigator — Reasoning Trajectory Browser TUI.

Sacred geometric emblem for ``geometor/seer_navigator`` framed within the
unified ``R = 68`` graduated astrolabe seal:

1. **8-Point Precision Navigational Compass Rose**: Four bold cardinal star
   blades (``N, E, S, W``) and four intercardinal blades (``NE, SE, SW, NW``)
   nested inside concentric navigational bearing rings, calibrated to evoke an
   exploratory reasoning instrument plate.
2. **Branching Search-Trajectory Tree**: A crisp multi-level search tree
   rises from the South Root node across five depth horizons toward the North
   Goal Star, depicting explored reasoning trials and cleanly pruned dead ends.
3. **Glowing Golden Winning Solution Path**: One uninterrupted golden winning
   trajectory threads through the tree from Root to the radiant North Goal
   Star, marked with double-ringed golden decision waypoints and directional
   compass arc indicators.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_seer_navigator_elements",
    "build_seer_navigator_svg",
    "write_seer_navigator_svgs",
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


def _add_star_blade(
    mb: MedallionBuilder,
    layer: str,
    ox: float,
    oy: float,
    tip_r: float,
    waist_r: float,
    deg: float,
    half_waist_deg: float,
) -> None:
    """Add one compass-rose star blade with tip at ``(tip_r, deg)`` and waist shoulders."""
    tip = polar(ox, oy, tip_r, deg)
    left = polar(ox, oy, waist_r, deg - half_waist_deg)
    right = polar(ox, oy, waist_r, deg + half_waist_deg)
    mb.add_line(layer, left[0], left[1], tip[0], tip[1])
    mb.add_line(layer, right[0], right[1], tip[0], tip[1])
    mb.add_line("detail", ox, oy, tip[0], tip[1])


def build_seer_navigator_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/seer_navigator``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. 8-Point Precision Navigational Compass Rose Instrument Plate
    # ------------------------------------------------------------------
    r_compass = 59.0
    mb.add_circle("detail", ox, oy, r_compass)
    mb.add_circle("detail", ox, oy, 42.0)
    mb.add_circle("detail", ox, oy, 18.0)

    # 16 fine compass bearing ticks around r_compass
    for k in range(16):
        deg = float(k * 22.5)
        r_in = r_compass - (3.5 if k % 2 == 0 else 2.0)
        p1 = polar(ox, oy, r_in, deg)
        p2 = polar(ox, oy, r_compass, deg)
        mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])

    # 4 Intercardinal blades (NE, SE, SW, NW) in crisp detail
    for deg in (-45.0, 45.0, 135.0, 225.0):
        _add_star_blade(mb, "detail", ox, oy, 43.0, 10.5, deg, 22.5)

    # 4 Cardinal blades (N, E, S, W) in crisp detail (framing the search tree)
    for deg in (-90.0, 0.0, 90.0, 180.0):
        _add_star_blade(mb, "detail", ox, oy, 58.0, 13.0, deg, 45.0)

    # Subtle East/West horizon cross-jewels
    for deg in (0.0, 180.0):
        pt = polar(ox, oy, 58.0, deg)
        mb.add_circle("detail", pt[0], pt[1], 1.8)

    # ------------------------------------------------------------------
    # 2. Crisp Branching Search-Trajectory Tree (South Root -> North Goal)
    # ------------------------------------------------------------------
    nodes: dict[str, Point] = {
        "root": (ox, oy + 46.0),
        # Depth 1
        "d1_l": (ox - 24.0, oy + 26.0),
        "d1_m": (ox - 2.0, oy + 24.0),
        "d1_r": (ox + 22.0, oy + 26.0),
        # Depth 2
        "d2_ll": (ox - 40.0, oy + 6.0),
        "d2_lm": (ox - 20.0, oy + 6.0),
        "d2_ml": (ox - 8.0, oy + 4.0),
        "d2_mr": (ox + 12.0, oy + 6.0),
        "d2_rl": (ox + 28.0, oy + 6.0),
        "d2_rr": (ox + 42.0, oy + 8.0),
        # Depth 3
        "d3_ll": (ox - 34.0, oy - 14.0),
        "d3_lm": (ox - 18.0, oy - 14.0),
        "d3_m": (ox - 6.0, oy - 14.0),
        "d3_rl": (ox + 12.0, oy - 14.0),
        "d3_rr": (ox + 30.0, oy - 14.0),
        # Depth 4
        "d4_l": (ox - 24.0, oy - 32.0),
        "d4_ml": (ox - 10.0, oy - 32.0),
        "d4_mr": (ox + 8.0, oy - 32.0),
        "d4_r": (ox + 24.0, oy - 32.0),
        # Depth 5 (North Goal Star)
        "goal": (ox, oy - 50.0),
    }

    # Verify all tree nodes lie safely inside the compass ring
    for name, (nx, ny) in nodes.items():
        if math.hypot(nx - ox, ny - oy) > r_compass - 2.0:
            msg = f"Trajectory node {name!r} exceeds compass ring boundary"
            raise ValueError(msg)

    winning_path = ["root", "d1_r", "d2_mr", "d3_m", "d4_mr", "goal"]
    winning_edges = set(zip(winning_path[:-1], winning_path[1:], strict=True))
    winning_nodes = set(winning_path)

    all_edges: list[tuple[str, str]] = [
        ("root", "d1_l"),
        ("root", "d1_m"),
        ("root", "d1_r"),
        ("d1_l", "d2_ll"),
        ("d1_l", "d2_lm"),
        ("d1_m", "d2_ml"),
        ("d1_m", "d2_mr"),
        ("d1_r", "d2_mr"),
        ("d1_r", "d2_rl"),
        ("d1_r", "d2_rr"),
        ("d2_lm", "d3_ll"),
        ("d2_lm", "d3_lm"),
        ("d2_ml", "d3_lm"),
        ("d2_mr", "d3_m"),
        ("d2_mr", "d3_rl"),
        ("d2_rl", "d3_rr"),
        ("d3_lm", "d4_l"),
        ("d3_m", "d4_ml"),
        ("d3_m", "d4_mr"),
        ("d3_rl", "d4_r"),
        ("d4_mr", "goal"),
    ]

    # Explored non-winning trajectory edges in bold primary
    for u, v in all_edges:
        if (u, v) in winning_edges:
            continue
        p1, p2 = nodes[u], nodes[v]
        mb.add_line("primary", p1[0], p1[1], p2[0], p2[1])

    # Explored non-winning nodes + subtle pruned dead-end ticks
    pruned_leaves = {"d2_ll", "d2_rr", "d3_ll", "d3_rr", "d4_l", "d4_ml", "d4_r"}
    for name, (nx, ny) in nodes.items():
        if name in winning_nodes:
            continue
        mb.add_circle("primary", nx, ny, 2.1)
        if name in pruned_leaves:
            mb.add_line("detail", nx - 1.6, ny - 4.2, nx + 1.6, ny - 4.2)

    # ------------------------------------------------------------------
    # 3. Luminous Golden Winning Solution Path & Goal Star
    # ------------------------------------------------------------------
    for u, v in zip(winning_path[:-1], winning_path[1:], strict=True):
        p1, p2 = nodes[u], nodes[v]
        # Main golden winning trajectory edge
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
        # Subtle parallel double-rail glow offset by +/- 0.95 units
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        seg_len = math.hypot(dx, dy)
        nx, ny = -dy / seg_len, dx / seg_len
        for s in (-0.95, 0.95):
            mb.add_line(
                "golden",
                p1[0] + s * nx,
                p1[1] + s * ny,
                p2[0] + s * nx,
                p2[1] + s * ny,
            )

    # Golden double-ringed waypoints along the winning path
    for name in winning_path[1:-1]:
        wx, wy = nodes[name]
        mb.add_circle("golden", wx, wy, 3.3)
        mb.add_circle("golden", wx, wy, 1.65, filled=True)

    # South Root launch jewel
    rx, ry = nodes["root"]
    mb.add_circle("golden", rx, ry, 4.0)
    mb.add_circle("golden", rx, ry, 2.0, filled=True)

    # North Goal Star (radiant 8-ray golden beacon)
    gx, gy = nodes["goal"]
    mb.add_circle("golden", gx, gy, 5.2)
    mb.add_circle("golden", gx, gy, 2.5, filled=True)
    for k in range(8):
        deg = float(k * 45)
        r_ray = 8.2 if k % 2 == 0 else 6.2
        p_in = polar(gx, gy, 3.0, deg)
        p_out = polar(gx, gy, r_ray, deg)
        mb.add_line("golden", p_in[0], p_in[1], p_out[0], p_out[1])

    # Compass center pivot jewel
    mb.add_circle("golden", ox, oy, 2.2)

    return mb.build()


def build_seer_navigator_svg(theme: str = "dark") -> str:
    """Render the Seer Navigator project medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_seer_navigator_elements()
    return render_medallion_svg(layers, theme=theme)


def write_seer_navigator_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``seer_navigator_dark.svg`` and ``seer_navigator_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "seer_navigator_dark.svg"
    light_path = target_dir / "seer_navigator_light.svg"
    dark_path.write_text(build_seer_navigator_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_seer_navigator_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
