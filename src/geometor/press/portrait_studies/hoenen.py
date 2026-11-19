"""Study 24: Petrus Hoenen, S.J. (1930s clerical portrait) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_hoenen_elements",
    "build_hoenen_svg",
    "write_hoenen_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_noetic_triangle_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.6,
) -> None:
    """Draw Hoenen's Noetic Abstraction & Judgment Triangle (*Phantasma -> Intellectus -> Judicium*).

    Inscribes an equilateral triangle inside a circumcircle with a horizontal
    reflection base, a perpendicular constructive altitude bisecting the base
    with a right-angle square marker, and an inner inscribed circle of unity.
    """
    mb.add_circle("golden", cx, cy, radius)

    verts = [
        (
            cx + radius * math.cos(math.radians(-90.0 + 120.0 * k)),
            cy + radius * math.sin(math.radians(-90.0 + 120.0 * k)),
        )
        for k in range(3)
    ]
    v_top, v_br, v_bl = verts[0], verts[1], verts[2]

    # Equilateral triangle (Intellectus apex over Phantasma horizontal base)
    mb.add_line("golden", v_top[0], v_top[1], v_br[0], v_br[1])
    mb.add_line("golden", v_br[0], v_br[1], v_bl[0], v_bl[1])
    mb.add_line("golden", v_bl[0], v_bl[1], v_top[0], v_top[1])

    # Perpendicular constructive altitude from apex bisecting base at M
    base_y = v_br[1]
    mb.add_line("golden", cx, v_top[1], cx, cy + radius)

    # Crisp right-angle square marker at base midpoint M
    sq = 2.3
    mb.add_line("golden", cx, base_y - sq, cx + sq, base_y - sq)
    mb.add_line("golden", cx + sq, base_y - sq, cx + sq, base_y)

    # Horizontal mid-level abstraction chord (inscribed incircle tangent)
    mb.add_circle("golden", cx, cy, 0.5 * radius)

    # Key noetic nodes: filled apex & center, open base vertices & midpoint
    mb.add_circle("golden", v_top[0], v_top[1], 0.95, filled=True)
    mb.add_circle("golden", cx, cy, 0.85, filled=True)
    mb.add_circle("golden", v_br[0], v_br[1], 0.72)
    mb.add_circle("golden", v_bl[0], v_bl[1], 0.72)
    mb.add_circle("golden", cx, base_y, 0.65)


def _add_parallel_postulate_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Hoenen's constructive compass-arc Parallel Postulate (*De Noetica Geometriae*).

    Constructs two parallel straight lines crossed by a diagonal transversal
    with equal compass-transferred corresponding-angle arcs and intersection
    nodes honoring Hoenen's phenomenological defense of Euclidean intuition.
    """
    half_w = 12.2
    dy_par = 5.8
    y1 = cy - dy_par
    y2 = cy + dy_par

    # Two parallel horizontal straight lines
    mb.add_line("golden", cx - half_w, y1, cx + half_w, y1)
    mb.add_line("golden", cx - half_w, y2, cx + half_w, y2)

    # Diagonal transversal crossing both parallels at exact angle -54 deg
    ang_deg = -54.0
    ang_rad = math.radians(ang_deg)
    t_len = 13.4
    tx1 = cx - t_len * math.cos(ang_rad)
    ty1 = cy - t_len * math.sin(ang_rad)
    tx2 = cx + t_len * math.cos(ang_rad)
    ty2 = cy + t_len * math.sin(ang_rad)
    mb.add_line("golden", tx1, ty1, tx2, ty2)

    # Exact intersection points P1 (upper parallel) and P2 (lower parallel)
    cot_a = math.cos(ang_rad) / math.sin(ang_rad)
    p1x, p1y = cx + (y1 - cy) * cot_a, y1
    p2x, p2y = cx + (y2 - cy) * cot_a, y2

    # Equal compass-constructed corresponding-angle arcs at P1 and P2
    r_arc = 5.0
    r_arc_outer = 6.4
    for px, py in ((p1x, p1y), (p2x, p2y)):
        mb.add_arc("golden", px, py, r_arc, ang_deg, 0.0)
        mb.add_arc("golden", px, py, r_arc_outer, ang_deg, 0.0)
        mb.add_circle("golden", px, py, 0.9, filled=True)
        # Compass tick dots where inner arc meets parallel & transversal
        mb.add_circle("golden", px + r_arc, py, 0.55)
        mb.add_circle(
            "golden",
            px + r_arc * math.cos(ang_rad),
            py + r_arc * math.sin(ang_rad),
            0.55,
        )

    # Alternate interior angle arc at P1 mirroring P2
    mb.add_arc("golden", p1x, p1y, r_arc, 180.0 + ang_deg, 180.0)

    # Small parallel-line chevron ticks on the left ends of both parallels
    for py in (y1, y2):
        tick_x = cx - half_w + 3.2
        mb.add_line("golden", tick_x - 1.3, py - 1.2, tick_x, py)
        mb.add_line("golden", tick_x - 1.3, py + 1.2, tick_x, py)


def build_hoenen_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the four-layer compass-and-straightedge geometry for Petrus Hoenen, S.J.

    Uses ``MedallionBuilder`` so every line and circular arc is clipped cleanly
    within ``MED_R = 92.0`` with zero Bezier curves.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1 (Scaffold): Canonical medallion ring, eye line & golden circles
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-14.2,
        eye_rx=4.6,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Noetic Triangle (Left) & Parallel Postulate (Right)
    # -------------------------------------------------------------------------
    _add_noetic_triangle_motif(mb, cx=-63.5, cy=-26.0, radius=12.6)
    _add_parallel_postulate_motif(mb, cx=64.5, cy=-26.0)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Neatly Slicked Parted Hair, Calm Forehead & Sculpted Ear
    # -------------------------------------------------------------------------
    # Outer slicked-back 1930s hair crown silhouette
    mb.add_arc_pts("primary", (-20.8, -33.0), (-20.2, -48.5), 1.4)
    mb.add_arc_pts("primary", (-20.2, -48.5), (-14.5, -59.5), 1.8)
    mb.add_arc_pts("primary", (-14.5, -59.5), (-9.2, -60.5), 0.7)
    mb.add_arc_pts("primary", (-9.2, -60.5), (14.5, -63.0), 3.4)
    mb.add_arc_pts("primary", (14.5, -63.0), (33.0, -50.0), 3.4)
    mb.add_arc_pts("primary", (33.0, -50.0), (35.8, -30.5), 2.4)

    # Broad calm intellectual forehead hairline & short sideburn
    mb.add_arc_pts("detail", (-19.8, -44.0), (-14.0, -52.5), 1.2)
    mb.add_arc_pts("detail", (-14.0, -52.5), (4.5, -54.5), 2.4)
    mb.add_arc_pts("detail", (4.5, -54.5), (21.5, -48.0), 2.2)
    mb.add_arc_pts("detail", (21.5, -48.0), (26.5, -30.0), 1.6)
    mb.add_arc_pts("detail", (-14.0, -52.5), (-9.2, -60.5), -0.8)

    # Slicked-back dark hair waves following the cranial contour
    mb.add_wave("detail", (-8.5, -56.8), (24.5, -53.0), 4, wave_angle_deg * 0.42, 1)
    mb.add_wave("detail", (2.0, -60.0), (30.5, -46.5), 4, wave_angle_deg * 0.42, -1)
    mb.add_wave("detail", (23.5, -46.5), (32.2, -31.5), 3, wave_angle_deg * 0.4, 1)

    # Prominently sculpted right ear
    mb.add_arc_pts("primary", (28.5, -26.5), (35.5, -28.8), 1.6)
    mb.add_arc_pts("primary", (35.5, -28.8), (38.2, -21.2), 2.0)
    mb.add_arc_pts("primary", (38.2, -21.2), (34.2, -12.0), 1.6)
    mb.add_arc_pts("primary", (34.2, -12.0), (29.5, -9.8), 1.2)
    mb.add_arc_pts("primary", (29.5, -9.8), (27.0, -12.5), 0.7)
    mb.add_arc_pts("detail", (29.8, -24.5), (34.8, -22.2), 1.4)
    mb.add_arc_pts("detail", (34.8, -22.2), (32.0, -14.2), 1.4)
    mb.add_arc_pts("detail", (28.5, -20.2), (30.2, -17.2), 0.7)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Three-Quarter Left Face, Round Spectacles, Nose & Mouth
    # -------------------------------------------------------------------------
    # Left three-quarter profile contour (temple -> cheek -> jaw -> solid chin)
    mb.add_arc_pts("primary", (-20.8, -33.0), (-21.2, -25.0), 0.4)
    mb.add_arc_pts("primary", (-21.2, -25.0), (-20.2, -14.5), -0.9)
    mb.add_arc_pts("primary", (-20.2, -14.5), (-18.5, -4.0), -1.0)
    mb.add_arc_pts("primary", (-18.5, -4.0), (-13.5, 5.5), -1.4)
    mb.add_arc_pts("primary", (-13.5, 5.5), (-2.5, 11.2), -1.8)

    # Broad clean right jawline rising smoothly to sculpted ear
    mb.add_arc_pts("primary", (-2.5, 11.2), (10.5, 9.8), -1.6)
    mb.add_arc_pts("primary", (10.5, 9.8), (22.5, 3.2), -1.6)
    mb.add_arc_pts("primary", (22.5, 3.2), (28.8, -7.0), -1.4)
    mb.add_arc_pts("primary", (28.8, -7.0), (29.5, -9.8), -0.4)

    # Calm horizontal eyebrows arching cleanly above the round spectacles
    mb.add_arc_pts("primary", (-20.4, -32.2), (-14.5, -34.2), 0.9)
    mb.add_arc_pts("primary", (-14.5, -34.2), (-8.5, -32.2), 0.8)
    mb.add_arc_pts("primary", (-0.8, -32.4), (5.5, -34.4), 1.0)
    mb.add_arc_pts("primary", (5.5, -34.4), (13.2, -32.6), 0.9)

    # Iconic perfectly circular round 1930s spectacles (pure compass circles!)
    mb.add_circle("primary", -14.5, -25.2, 6.2)
    mb.add_circle("primary", 4.5, -25.2, 6.3)
    # Curved nose bridge & horizontal temple arm reaching over right ear
    mb.add_arc_pts("primary", (-8.3, -26.5), (-1.8, -26.5), 1.4)
    mb.add_line("primary", 10.8, -26.2, 31.8, -28.6)
    mb.add_line("detail", 11.0, -25.2, 30.8, -27.5)

    # Steady scholarly eyes framed inside the circular lenses on y = -27
    # Viewer's left eye
    l_out = (-17.8, -26.0)
    l_in = (-10.4, -26.2)
    mb.add_arc_pts("primary", l_out, l_in, 1.55)
    mb.add_arc_pts("detail", (-18.0, -28.0), (-10.2, -28.2), 1.45)
    mb.add_arc_pts("detail", l_out, l_in, -0.95)
    mb.add_circle("detail", -14.0, -26.1, 1.72)
    mb.add_circle("primary", -14.0, -26.1, 0.88, filled=True)

    # Viewer's right eye
    r_in = (0.6, -26.4)
    r_out = (8.8, -26.2)
    mb.add_arc_pts("primary", r_in, r_out, 1.65)
    mb.add_arc_pts("detail", (0.4, -28.4), (9.0, -28.2), 1.55)
    mb.add_arc_pts("detail", r_in, r_out, -1.0)
    mb.add_circle("detail", 4.6, -26.3, 1.82)
    mb.add_circle("primary", 4.6, -26.3, 0.92, filled=True)

    # Firm straight nose & subtle character lines
    mb.add_arc_pts("primary", (-5.6, -24.5), (-9.2, -16.5), 0.25)
    mb.add_arc_pts("primary", (-9.2, -16.5), (-10.4, -11.8), -0.4)
    mb.add_arc_pts("primary", (-10.4, -11.8), (-7.8, -9.2), -0.8)
    mb.add_arc_pts("primary", (-7.8, -9.2), (-2.6, -9.2), -0.5)
    mb.add_arc_pts("primary", (-2.6, -9.2), (1.0, -11.2), -0.7)
    mb.add_arc_pts("detail", (1.0, -11.2), (0.4, -14.6), -0.45)
    mb.add_arc_pts("detail", (-1.0, -21.5), (-1.4, -15.2), -0.25)
    mb.add_arc_pts("detail", (-7.6, -10.5), (-4.2, -10.6), 0.35)
    mb.add_arc_pts("detail", (-13.6, -10.5), (-16.2, -2.0), -0.9)
    mb.add_arc_pts("detail", (3.6, -10.5), (9.8, -1.5), 1.1)

    # Composed serious Jesuit scholar mouth & strong chin
    mb.add_arc_pts("detail", (-5.0, -8.4), (-5.0, -5.6), 0.2)
    mb.add_arc_pts("detail", (-10.8, -4.0), (-4.6, -4.8), 0.45)
    mb.add_arc_pts("detail", (-4.6, -4.8), (4.2, -3.6), 0.45)
    mb.add_arc_pts("primary", (-12.2, -2.5), (5.4, -2.1), 0.85)
    mb.add_arc_pts("detail", (-9.4, -0.3), (-4.2, 0.4), -0.65)
    mb.add_arc_pts("detail", (-4.2, 0.4), (2.2, -0.5), -0.5)
    mb.add_arc_pts("detail", (-7.8, 4.4), (-0.8, 4.4), -0.55)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Jesuit Roman Clerical Collar & Dark Clerical Cassock
    # -------------------------------------------------------------------------
    # Neck sides & concentric Roman clerical collar band (closed cleanly at shoulders)
    mb.add_arc_pts("primary", (-14.8, 4.8), (-14.4, 8.8), -0.3)
    mb.add_arc_pts("primary", (23.8, 1.5), (26.2, 6.2), -0.5)
    mb.add_line("primary", -14.4, 8.8, -15.8, 11.4)
    mb.add_line("primary", 26.2, 6.2, 28.0, 9.0)

    # Concentric circular collar upper rim & lower clerical rabat seam
    mb.add_arc_pts("primary", (-14.4, 8.8), (26.2, 6.2), -5.4)
    mb.add_arc_pts("primary", (-15.8, 11.4), (28.0, 9.0), -7.6)

    # Signature crisp white Jesuit Roman clerical collar tab at throat center
    mb.add_line("primary", 0.2, 13.4, 1.4, 18.6)
    mb.add_line("primary", 6.2, 13.0, 5.4, 18.2)
    mb.add_line("primary", 1.4, 18.6, 5.4, 18.2)
    mb.add_arc_pts("detail", (-12.5, 11.2), (0.0, 15.6), -1.2)
    mb.add_arc_pts("detail", (6.5, 15.2), (24.5, 9.6), -1.4)

    # Dignified dark clerical cassock / coat shoulders clipped flush to MED_R
    mb.add_arc_pts("primary", (-15.8, 11.4), (-47.5, 27.0), -2.8)
    mb.add_arc_pts("primary", (-47.5, 27.0), (-74.0, 72.0), -6.2)
    mb.add_arc_pts("primary", (28.0, 9.0), (56.5, 27.0), 3.0)
    mb.add_arc_pts("primary", (56.5, 27.0), (76.5, 70.0), 5.6)

    # Sober Jesuit cassock vertical buttoned placket & subtle drapery folds
    mb.add_arc_pts("primary", (3.2, 18.6), (4.4, 88.0), -0.8)
    mb.add_arc_pts("detail", (6.8, 18.4), (8.2, 88.0), -0.8)
    for by in (31.5, 46.5, 61.5, 76.5):
        mb.add_circle("detail", 5.2, by, 1.35)

    # Clean clerical shoulder seams & vertical cassock folds clipped to MED_R
    mb.add_arc_pts("detail", (-22.0, 16.5), (-32.5, 84.0), -2.4)
    mb.add_arc_pts("detail", (-42.0, 32.0), (-56.5, 78.0), -2.6)
    mb.add_arc_pts("detail", (-10.5, 21.0), (-14.5, 87.5), -1.4)
    mb.add_arc_pts("detail", (22.5, 16.0), (28.5, 85.0), 2.0)
    mb.add_arc_pts("detail", (38.5, 22.0), (49.5, 78.0), 2.8)
    mb.add_arc_pts("detail", (52.5, 32.0), (65.5, 70.0), 2.5)

    return mb.build()


def build_hoenen_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Petrus Hoenen, S.J. medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_hoenen_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_hoenen_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``hoenen_dark.svg`` and ``hoenen_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "hoenen_dark.svg"
    light_path = target_dir / "hoenen_light.svg"
    dark_path.write_text(
        build_hoenen_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_hoenen_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
