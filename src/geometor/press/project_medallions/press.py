"""Project Medallion: Press (geometor/press) — Digital Scriptorium Press.

Frames an open architectural Codex Book Spread and golden hinged compass inside
the unified ``R = 68`` graduated astrolabe seal:

1. **Open Codex Book Spread (`1 : sqrt(2)` Folio Canon)**: Twin facing pages
   with crisp architectural binding boards, stepped folio fore-edges, and a
   pure circular-arc curved spine cradle, fitting comfortably inside ``R = 68``.
2. **Exact *Van de Graaf* / Villard de Honnecourt Page-Margin Canon**: Full
   spread diagonals and single-page diagonals intersect analytically to carve
   out exact ``1/9`` inner/top and ``2/9`` outer/bottom margins on both facing
   pages (verified to ``< 1e-12``), enclosing two matching ``1 : sqrt(2)``
   golden-framed text blocks ruled with manuscript lines.
3. **Crowning Golden Hinged Compass**: Centered directly above the codex spine,
   a precision geometric compass with double-ring hinge joint, finial stem,
   tapered needle legs, and calibrated circular wing-arc presides over the
   spread.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_press_elements",
    "build_press_svg",
    "write_press_svgs",
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


def _add_rect(mb: MedallionBuilder, layer: str, x0: float, y0: float, x1: float, y1: float) -> None:
    """Draw an axis-aligned rectangle from ``(x0, y0)`` to ``(x1, y1)``."""
    mb.add_line(layer, x0, y0, x1, y0)
    mb.add_line(layer, x1, y0, x1, y1)
    mb.add_line(layer, x1, y1, x0, y1)
    mb.add_line(layer, x0, y1, x0, y0)


def build_press_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/press``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    sqrt2 = math.sqrt(2.0)

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Open Architectural Codex Book Spread (Exact 1 : sqrt(2) Page Ratio)
    # ------------------------------------------------------------------
    page_w = 40.0
    page_h = page_w * sqrt2  # 56.57 -> crisp 1 : sqrt(2) folio canon
    y_top = oy - 21.0
    y_bot = y_top + page_h

    tl: Point = (ox - page_w, y_top)
    ts: Point = (ox, y_top)
    tr: Point = (ox + page_w, y_top)
    bl: Point = (ox - page_w, y_bot)
    bs: Point = (ox, y_bot)
    br: Point = (ox + page_w, y_bot)

    # ------------------------------------------------------------------
    # 2. Exact Van de Graaf / Villard de Honnecourt Canon Construction
    # ------------------------------------------------------------------
    # Intersections of full spread diagonals with single-page diagonals (at 1/3, 1/3)
    a_r = _line_intersection(bl, tr, ts, br)
    a_l = _line_intersection(tl, br, ts, bl)
    t_r: Point = (a_r[0], y_top)
    t_l: Point = (a_l[0], y_top)

    # Right page text block via exact Van de Graaf cross-chord T_R -- A_L
    r_tl = _line_intersection(t_r, a_l, ts, br)
    r_tr = _line_intersection(r_tl, (r_tl[0] + 10.0, r_tl[1]), bl, tr)
    r_br = _line_intersection(r_tr, (r_tr[0], r_tr[1] + 10.0), ts, br)
    r_bl: Point = (r_tl[0], r_br[1])

    # Left page text block via exact Van de Graaf cross-chord T_L -- A_R
    l_tr = _line_intersection(t_l, a_r, ts, bl)
    l_tl = _line_intersection(l_tr, (l_tr[0] - 10.0, l_tr[1]), tl, br)
    l_bl = _line_intersection(l_tl, (l_tl[0], l_tl[1] + 10.0), ts, bl)
    l_br: Point = (l_tr[0], l_bl[1])

    # Verify exact 1/9 inner/top, 2/9 outer/bottom margins & 1 : sqrt(2) text block
    r_inner_margin = r_tl[0] - ox
    r_top_margin = r_tl[1] - y_top
    r_tb_w = r_tr[0] - r_tl[0]
    r_tb_h = r_br[1] - r_tr[1]
    if (
        abs(r_inner_margin - page_w / 9.0) > 1e-11
        or abs(r_top_margin - page_h / 9.0) > 1e-11
        or abs((r_tb_h / r_tb_w) - sqrt2) > 1e-11
    ):
        msg = "Van de Graaf 1/9 : 6/9 : 2/9 canon invariant violated"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 3. Detail Layer: Stepped Folio Fore-Edges, Bindings, & Manuscript Lines
    # ------------------------------------------------------------------
    # Outer architectural binding boards & stepped page block edges
    pad_x, pad_y = 3.2, 2.8
    _add_rect(mb, "detail", ox - page_w - pad_x, y_top - 1.4, ox + page_w + pad_x, y_bot + pad_y)
    mb.add_line("detail", ox - page_w - 1.6, y_top + 1.0, ox - page_w - 1.6, y_bot + 1.4)
    mb.add_line("detail", ox + page_w + 1.6, y_top + 1.0, ox + page_w + 1.6, y_bot + 1.4)
    mb.add_line("detail", ox - page_w - 1.6, y_bot + 1.4, ox + page_w + 1.6, y_bot + 1.4)

    # Curved spine cradle arcs at foot and head of the binding
    mb.add_arc_pts("detail", (ox - 5.5, y_bot + pad_y), (ox + 5.5, y_bot + pad_y), -2.4)
    mb.add_arc_pts("detail", (ox - 4.5, y_top - 1.4), (ox + 4.5, y_top - 1.4), -1.6)

    # Auxiliary Van de Graaf construction lines (verticals A -> T and cross-chords)
    mb.add_line("detail", a_r[0], a_r[1], t_r[0], t_r[1])
    mb.add_line("detail", a_l[0], a_l[1], t_l[0], t_l[1])
    mb.add_line("detail", t_r[0], t_r[1], a_l[0], a_l[1])
    mb.add_line("detail", t_l[0], t_l[1], a_r[0], a_r[1])

    # Fine ruled manuscript lines inside both facing text blocks (8 lines per page)
    for k in range(1, 9):
        t = k / 9.0
        yl = l_tl[1] + t * (l_bl[1] - l_tl[1])
        # Slightly shorten last paragraph line for authentic typographic cadence
        x_end_l = l_tr[0] - (5.0 if k == 8 else 1.4)
        x_end_r = r_tr[0] - (5.0 if k == 8 else 1.4)
        mb.add_line("detail", l_tl[0] + 1.4, yl, x_end_l, yl)
        mb.add_line("detail", r_tl[0] + 1.4, yl, x_end_r, yl)

    # ------------------------------------------------------------------
    # 4. Bold Primary Layer: Open Codex Pages, Spine, & Canon Diagonals
    # ------------------------------------------------------------------
    _add_rect(mb, "primary", ox - page_w, y_top, ox + page_w, y_bot)
    mb.add_line("primary", ts[0], ts[1], bs[0], bs[1])

    # Subtle gutter curves meeting the top and bottom of the central spine
    mb.add_arc_pts("primary", (ox - 8.0, y_top), ts, 1.4)
    mb.add_arc_pts("primary", ts, (ox + 8.0, y_top), 1.4)
    mb.add_arc_pts("primary", (ox - 8.0, y_bot), bs, 1.4)
    mb.add_arc_pts("primary", bs, (ox + 8.0, y_bot), 1.4)

    # Full-spread and single-page Van de Graaf diagonals
    mb.add_line("detail", bl[0], bl[1], tr[0], tr[1])
    mb.add_line("detail", tl[0], tl[1], br[0], br[1])
    mb.add_line("detail", ts[0], ts[1], br[0], br[1])
    mb.add_line("detail", ts[0], ts[1], bl[0], bl[1])

    # ------------------------------------------------------------------
    # 5. Luminous Golden Layer: Text Blocks, Canon Intersections, & Compass
    # ------------------------------------------------------------------
    # Golden Van de Graaf text-block frames on left & right pages
    _add_rect(mb, "golden", l_tl[0], l_tl[1], l_br[0], l_br[1])
    _add_rect(mb, "golden", r_tl[0], r_tl[1], r_br[0], r_br[1])

    # Golden canon diagonal highlights inside both text blocks
    mb.add_line("golden", l_tl[0], l_tl[1], l_br[0], l_br[1])
    mb.add_line("golden", r_tl[0], r_tl[1], r_br[0], r_br[1])

    # Canon intersection nodes at 1/3 anchors and inner text-block corners
    for pt in (a_l, a_r, l_tr, r_tl, l_bl, r_br):
        mb.add_circle("golden", pt[0], pt[1], 2.2)
        mb.add_circle("golden", pt[0], pt[1], 1.05, filled=True)

    # Crowning Golden Hinged Compass poised above the spine
    hinge: Point = (ox, oy - 48.0)
    crown_tip: Point = (ox, oy - 59.5)
    leg_len = 36.0
    half_open_deg = 27.0

    # Left & right compass needle tips (symmetric around vertical)
    tip_l = polar(hinge[0], hinge[1], leg_len, 90.0 + half_open_deg)
    tip_r = polar(hinge[0], hinge[1], leg_len, 90.0 - half_open_deg)

    # Tapered twin-edge compass legs (outer edge + inner edge meeting cleanly at needle tip)
    shoulder_l_out = polar(hinge[0], hinge[1], 4.6, 180.0 - 20.0)
    shoulder_l_in = polar(hinge[0], hinge[1], 3.8, 90.0 + half_open_deg - 16.0)
    shoulder_r_out = polar(hinge[0], hinge[1], 4.6, 20.0)
    shoulder_r_in = polar(hinge[0], hinge[1], 3.8, 90.0 - half_open_deg + 16.0)

    mb.add_line("golden", shoulder_l_out[0], shoulder_l_out[1], tip_l[0], tip_l[1])
    mb.add_line("golden", shoulder_l_in[0], shoulder_l_in[1], tip_l[0], tip_l[1])
    mb.add_line("golden", shoulder_r_out[0], shoulder_r_out[1], tip_r[0], tip_r[1])
    mb.add_line("golden", shoulder_r_in[0], shoulder_r_in[1], tip_r[0], tip_r[1])

    # Bold primary center-rib along each compass leg for architectural crispness
    mb.add_line("primary", hinge[0], hinge[1] + 4.5, tip_l[0], tip_l[1])
    mb.add_line("primary", hinge[0], hinge[1] + 4.5, tip_r[0], tip_r[1])

    # Calibrated circular wing-arc bridging the compass legs
    wing_r = 21.0
    mb.add_arc("golden", hinge[0], hinge[1], wing_r, 90.0 - half_open_deg - 5.0, 90.0 + half_open_deg + 5.0)
    mb.add_arc("detail", hinge[0], hinge[1], wing_r - 2.6, 90.0 - half_open_deg, 90.0 + half_open_deg)
    for deg_off in (-18.0, -9.0, 0.0, 9.0, 18.0):
        p_in = polar(hinge[0], hinge[1], wing_r - 2.6, 90.0 + deg_off)
        p_out = polar(hinge[0], hinge[1], wing_r + 1.2, 90.0 + deg_off)
        mb.add_line("golden", p_in[0], p_in[1], p_out[0], p_out[1])

    # Compass handle stem & double-ring hinge medallion
    mb.add_line("golden", hinge[0], hinge[1] - 4.8, crown_tip[0], crown_tip[1])
    mb.add_line("primary", hinge[0] - 1.3, hinge[1] - 4.8, hinge[0] - 1.0, crown_tip[1] + 2.0)
    mb.add_line("primary", hinge[0] + 1.3, hinge[1] - 4.8, hinge[0] + 1.0, crown_tip[1] + 2.0)
    mb.add_circle("golden", crown_tip[0], crown_tip[1], 2.2)
    mb.add_circle("golden", crown_tip[0], crown_tip[1], 1.1, filled=True)

    mb.add_circle("golden", hinge[0], hinge[1], 5.0)
    mb.add_circle("primary", hinge[0], hinge[1], 3.3)
    mb.add_circle("golden", hinge[0], hinge[1], 1.8, filled=True)

    # Golden needle tip jewels
    for tip in (tip_l, tip_r):
        mb.add_circle("golden", tip[0], tip[1], 1.5, filled=True)

    return mb.build()


def build_press_svg(theme: str = "dark") -> str:
    """Render the ``geometor/press`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_press_elements()
    return render_medallion_svg(layers, theme=theme)


def write_press_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``press_dark.svg`` and ``press_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "press_dark.svg"
    light_path = target_dir / "press_light.svg"
    dark_path.write_text(build_press_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_press_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
