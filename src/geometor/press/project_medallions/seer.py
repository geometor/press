"""Project Medallion: Seer — ARC-AGI Visual Reasoning Engine.

Sacred geometric emblem for ``geometor/seer`` framed within the unified
``R = 68`` graduated astrolabe seal:

1. **Luminous Horizontal *Vesica Piscis* "Eye of Reasoning" Lens**: Two exact
   equilateral Vesica circles (``R_v = 64``, center offset ``d = 32``) form a
   sweeping horizontal eye lens of width ``64 * sqrt(3)`` and height ``64``,
   framed by a concentric circular iris ring and golden lens aura arcs.
2. **Bold ``3 x 3`` Geometric Pattern-Transformation Grid**: Centered cleanly
   within the iris of the eye (side ``36``, cell ``12 x 12``), with crisp
   structural grid lines and geometric ARC pattern motifs across all nine cells.
3. **Golden Symmetry Diagonals & Pattern Highlight Cells**: Radiant golden
   symmetry diagonals cut through the grid and iris, illuminating the central
   reasoning pupil diamond, four cardinal highlight squares, corner symmetry
   chevrons, and twin golden eye-corner jewels.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_seer_elements",
    "build_seer_svg",
    "write_seer_svgs",
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


def _add_rect(
    mb: MedallionBuilder,
    layer: str,
    cx: float,
    cy: float,
    half_w: float,
    half_h: float,
) -> None:
    """Add an axis-aligned rectangle centered at ``(cx, cy)``."""
    x0, x1 = cx - half_w, cx + half_w
    y0, y1 = cy - half_h, cy + half_h
    mb.add_line(layer, x0, y0, x1, y0)
    mb.add_line(layer, x1, y0, x1, y1)
    mb.add_line(layer, x1, y1, x0, y1)
    mb.add_line(layer, x0, y1, x0, y0)


def _add_diamond(
    mb: MedallionBuilder,
    layer: str,
    cx: float,
    cy: float,
    r: float,
) -> None:
    """Add a 45-degree diamond centered at ``(cx, cy)`` with half-diagonal ``r``."""
    pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    for k in range(4):
        p1, p2 = pts[k], pts[(k + 1) % 4]
        mb.add_line(layer, p1[0], p1[1], p2[0], p2[1])


def build_seer_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/seer``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Horizontal Vesica Piscis "Eye of Reasoning" Lens
    # ------------------------------------------------------------------
    rv = 64.0
    dv = 32.0  # Exact equilateral Vesica ratio (d = R / 2)
    eye_half_w = dv * math.sqrt(3.0)  # 55.4256...
    eye_half_h = rv - dv  # 32.0

    # Verify exact Vesica corner intersections
    if abs(math.hypot(eye_half_w, dv) - rv) > 1e-12:
        msg = "Vesica lens intersection invariant violated"
        raise ValueError(msg)

    # Bold primary Vesica eye contour (upper & lower 120-deg circular arcs)
    mb.add_arc("primary", ox, oy + dv, rv, -150.0, -30.0)
    mb.add_arc("primary", ox, oy - dv, rv, 30.0, 150.0)

    # Luminous parallel golden inner/outer lens aura arcs
    rv_in = rv - 3.0
    a_span = math.degrees(math.acos(dv / rv_in))
    mb.add_arc("golden", ox, oy + dv, rv_in, -90.0 - a_span + 6.0, -90.0 + a_span - 6.0)
    mb.add_arc("golden", ox, oy - dv, rv_in, 90.0 - a_span + 6.0, 90.0 + a_span - 6.0)

    # Subtle outer Vesica framing arcs & concentric circular iris ring
    mb.add_arc("detail", ox, oy + dv, rv + 4.5, -142.0, -38.0)
    mb.add_arc("detail", ox, oy - dv, rv + 4.5, 38.0, 142.0)
    r_iris = 31.0
    mb.add_circle("detail", ox, oy, r_iris)
    mb.add_circle("detail", ox, oy, 28.0)

    # Left & right optical wing symmetry arcs inside the sclera
    mb.add_arc("detail", ox - eye_half_w, oy, 18.0, -35.0, 35.0)
    mb.add_arc("detail", ox + eye_half_w, oy, 18.0, 145.0, 215.0)
    mb.add_arc("golden", ox - eye_half_w, oy, 12.0, -32.0, 32.0)
    mb.add_arc("golden", ox + eye_half_w, oy, 12.0, 148.0, 212.0)

    # ------------------------------------------------------------------
    # 2. Golden Symmetry Diagonals & Optical Sightlines
    # ------------------------------------------------------------------
    # Horizontal optical axis through eye corners
    mb.add_line("detail", ox - eye_half_w, oy, ox + eye_half_w, oy)
    # Vertical symmetry axis through Vesica apexes
    mb.add_line("detail", ox, oy - eye_half_h - 16.0, ox, oy + eye_half_h + 16.0)

    # Golden symmetry diagonals slicing cleanly through the 3x3 grid and iris
    diag_r = 38.0
    for deg in (45.0, 135.0):
        p1 = polar(ox, oy, diag_r, deg)
        p2 = polar(ox, oy, diag_r, deg + 180.0)
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # ------------------------------------------------------------------
    # 3. Bold 3x3 Geometric Pattern-Transformation Grid
    # ------------------------------------------------------------------
    cell = 11.6
    grid_half = 1.5 * cell  # 17.4 (corner radius 24.6 < r_iris = 28.0)
    _add_rect(mb, "primary", ox, oy, grid_half, grid_half)
    for offset in (-0.5 * cell, 0.5 * cell):
        mb.add_line("primary", ox + offset, oy - grid_half, ox + offset, oy + grid_half)
        mb.add_line("primary", ox - grid_half, oy + offset, ox + grid_half, oy + offset)

    # ------------------------------------------------------------------
    # 4. Pattern Highlight Cells (ARC Symmetry Transformation Motifs)
    # ------------------------------------------------------------------
    for row in (-1, 0, 1):
        for col in (-1, 0, 1):
            cx = ox + col * cell
            cy = oy + row * cell
            if row == 0 and col == 0:
                # Center cell: Luminous Golden Pupil of Reasoning
                _add_diamond(mb, "golden", cx, cy, 4.4)
                mb.add_circle("golden", cx, cy, 2.4)
                mb.add_circle("golden", cx, cy, 1.2, filled=True)
            elif row == 0 or col == 0:
                # 4 Cardinal highlight cells: Nested golden transformation frames
                _add_rect(mb, "golden", cx, cy, 3.8, 3.8)
                _add_rect(mb, "golden", cx, cy, 1.9, 1.9)
                mb.add_circle("golden", cx, cy, 0.9, filled=True)
            else:
                # 4 Corner cells: Crisp diagonal symmetry target circles & inner dots
                mb.add_circle("detail", cx, cy, 3.5)
                mb.add_circle("golden", cx, cy, 1.45, filled=True)

    # ------------------------------------------------------------------
    # 5. Radiant Golden Eye Corners & Crown Apex Jewels
    # ------------------------------------------------------------------
    for ex, ey in ((ox - eye_half_w, oy), (ox + eye_half_w, oy)):
        mb.add_circle("golden", ex, ey, 3.8)
        mb.add_circle("golden", ex, ey, 1.9, filled=True)

    for ax, ay in ((ox, oy - eye_half_h), (ox, oy + eye_half_h)):
        mb.add_circle("golden", ax, ay, 2.8)
        mb.add_circle("golden", ax, ay, 1.35, filled=True)

    # Four outer grid corner stars
    for sx in (-grid_half, grid_half):
        for sy in (-grid_half, grid_half):
            mb.add_circle("golden", ox + sx, oy + sy, 2.0)

    return mb.build()


def build_seer_svg(theme: str = "dark") -> str:
    """Render the Seer project medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_seer_elements()
    return render_medallion_svg(layers, theme=theme)


def write_seer_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``seer_dark.svg`` and ``seer_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "seer_dark.svg"
    light_path = target_dir / "seer_light.svg"
    dark_path.write_text(build_seer_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_seer_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
