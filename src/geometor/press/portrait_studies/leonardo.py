"""Study 16: Leonardo da Vinci (after Turin sanguine self-portrait, c. 1512) in lines and arcs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_leonardo_elements",
    "build_leonardo_svg",
    "write_leonardo_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_vitruvian_canon_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    circle_r: float = 12.3,
    square_s: float = 20.4,
) -> None:
    """Draw Leonardo's Vitruvian Circle-and-Square proportion canon in the left margin.

    The circle and square share the exact bottom tangent point, placing the
    circle's navel center slightly above the square's midpoint center in
    accordance with Leonardo's c. 1490 Gallerie dell'Accademia drawing.
    """
    y_bot = cy + circle_r
    c_cy = cy
    half_s = 0.5 * square_s
    sq_left = cx - half_s
    sq_right = cx + half_s
    sq_top = y_bot - square_s
    sq_mid_y = y_bot - half_s

    # Circumscribed Vitruvian circle & bottom-tangent square
    mb.add_circle("golden", cx, c_cy, circle_r)
    mb.add_line("golden", sq_left, sq_top, sq_right, sq_top)
    mb.add_line("golden", sq_right, sq_top, sq_right, y_bot)
    mb.add_line("golden", sq_right, y_bot, sq_left, y_bot)
    mb.add_line("golden", sq_left, y_bot, sq_left, sq_top)

    # Central vertical axis & proportional horizontal divisions (navel & square midpoint)
    mb.add_line("golden", cx, c_cy - circle_r, cx, y_bot)
    mb.add_line("golden", sq_left, c_cy, sq_right, c_cy)
    mb.add_line("golden", sq_left, sq_mid_y, sq_right, sq_mid_y)

    # Vitruvian outstretched diagonal rays from navel center to upper square corners & lower rim
    mb.add_line("golden", cx, c_cy, sq_left, sq_top)
    mb.add_line("golden", cx, c_cy, sq_right, sq_top)
    foot_l = polar(cx, c_cy, circle_r, 118.0)
    foot_r = polar(cx, c_cy, circle_r, 62.0)
    mb.add_line("golden", cx, sq_mid_y, foot_l[0], foot_l[1])
    mb.add_line("golden", cx, sq_mid_y, foot_r[0], foot_r[1])

    # Navel center node, square midpoint node, and shared bottom tangency point
    mb.add_circle("golden", cx, c_cy, 1.05, filled=True)
    mb.add_circle("golden", cx, sq_mid_y, 0.75)
    mb.add_circle("golden", cx, y_bot, 0.8)


def _add_codex_atlanticus_rosette_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.6,
) -> None:
    """Draw a Codex Atlanticus 6-petal Vesica compass rosette in the open right margin.

    Six congruent circles of radius ``R/2`` centered at ``60 deg`` intervals around
    the inner circle are internally tangent to the outer circle ``R`` and pass
    through the center, forming an exact Flower-of-Life 6-petal seed.
    """
    r_sub = 0.5 * radius
    mb.add_circle("golden", cx, cy, radius)
    mb.add_circle("golden", cx, cy, r_sub)

    for k in range(6):
        ang = -90.0 + 60.0 * k
        px, py = polar(cx, cy, r_sub, ang)
        mb.add_circle("golden", px, py, r_sub)
        tx, ty = polar(cx, cy, radius, ang)
        mb.add_circle("golden", tx, ty, 0.75)

    mb.add_circle("golden", cx, cy, 1.05, filled=True)


def build_leonardo_elements(wave_angle_deg: float = 32.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Leonardo da Vinci medallion strictly from lines, circles, and circular arcs.

    Calibrated to the Turin red-chalk presumed self-portrait (c. 1510-1515, Biblioteca
    Reale, Turin), featuring his noble high furrowed brow, heavy bushy overhanging
    eyebrows, deep-set sage eyes, aquiline nose, downturned solemn philosopher's mouth,
    and cascading Euclid III.12 locks of hair and flowing patriarch beard.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 hair and beard waves.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-10.8,
        eye_rx=12.2,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Vitruvian Canon (Left) & Codex Atlanticus Rosette (Right)
    # -------------------------------------------------------------------------
    _add_vitruvian_canon_motif(mb, cx=-65.0, cy=-28.0, circle_r=12.3, square_s=20.4)
    _add_codex_atlanticus_rosette_motif(mb, cx=65.0, cy=-28.0, radius=12.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Noble High Furrowed Brow, Right Profile, Deep Eyes & Nose
    # -------------------------------------------------------------------------
    # High receding sage cranial dome
    mb.add_arc_pts("primary", (-22.0, -47.5), (22.8, -42.5), 14.5)

    # Right three-quarter facial profile contour (brow boss -> cheekbone -> beard)
    mb.add_arc_pts("primary", (22.8, -42.5), (24.4, -33.0), 1.1)
    mb.add_arc_pts("primary", (24.4, -33.0), (23.4, -26.2), -0.6)
    mb.add_arc_pts("primary", (23.4, -26.2), (25.2, -16.5), 1.2)
    mb.add_arc_pts("primary", (25.2, -16.5), (22.8, -4.5), 1.2)

    # Left temple & cheek contour tucked behind cascading hair locks
    mb.add_arc_pts("primary", (-22.0, -47.5), (-25.0, -32.0), -1.6)
    mb.add_arc_pts("primary", (-25.0, -32.0), (-24.0, -14.0), -1.2)

    # Noble furrowed forehead lines & vertical glabella creases (detail)
    mb.add_arc_pts("detail", (-14.5, -45.5), (16.5, -45.0), 1.3)
    mb.add_arc_pts("detail", (-16.0, -40.5), (17.5, -40.0), 1.3)
    mb.add_arc_pts("detail", (0.5, -36.5), (0.8, -30.5), -0.3)
    mb.add_arc_pts("detail", (3.5, -36.0), (3.8, -30.2), 0.3)

    # Heavy bushy overhanging sage eyebrows (balanced bold primary ridge + bushy detail crest)
    # Viewer's left brow (thick overarching shelf)
    mb.add_arc_pts("primary", (-21.8, -29.8), (-10.5, -34.0), 1.6)
    mb.add_arc_pts("primary", (-10.5, -34.0), (-0.8, -30.5), 1.2)
    mb.add_arc_pts("detail", (-21.0, -32.4), (-10.2, -36.4), 1.5)
    mb.add_arc_pts("detail", (-10.2, -36.4), (-1.2, -33.0), 1.2)
    mb.add_arc_pts("detail", (-19.2, -31.6), (-2.5, -32.0), 1.9)

    # Viewer's right brow (bushy, foreshortened)
    mb.add_arc_pts("primary", (5.5, -30.5), (13.8, -33.2), 1.4)
    mb.add_arc_pts("primary", (13.8, -33.2), (22.0, -30.4), 1.1)
    mb.add_arc_pts("detail", (5.8, -32.8), (14.0, -35.4), 1.4)
    mb.add_arc_pts("detail", (14.0, -35.4), (21.5, -32.5), 1.1)

    # Deep-set penetrating sage eyes right on y = -27
    # Viewer's left eye (nearer eye, deep hooded socket)
    l_out = (-17.5, -26.5)
    l_in = (-4.8, -26.5)
    mb.add_arc_pts("primary", l_out, l_in, 1.8)
    mb.add_arc_pts("detail", (-17.8, -28.8), (-4.5, -28.8), 1.9)
    mb.add_arc_pts("detail", l_out, l_in, -1.2)
    mb.add_circle("detail", -10.8, -26.5, 1.9)
    mb.add_circle("primary", -10.4, -26.5, 0.95, filled=True)
    # Deep sage under-eye pouch & crow's-foot creases
    mb.add_arc_pts("detail", (-17.5, -21.8), (-5.2, -21.5), -1.8)
    mb.add_arc_pts("detail", (-18.5, -26.0), (-23.2, -25.2), 0.4)
    mb.add_arc_pts("detail", (-18.0, -24.2), (-22.8, -22.2), -0.4)

    # Viewer's right eye (further eye, deep beneath overhanging brow)
    r_in = (6.8, -26.5)
    r_out = (17.5, -26.8)
    mb.add_arc_pts("primary", r_in, r_out, 1.7)
    mb.add_arc_pts("detail", (6.6, -28.8), (17.8, -29.0), 1.7)
    mb.add_arc_pts("detail", r_in, r_out, -1.1)
    mb.add_circle("detail", 12.2, -26.6, 1.75)
    mb.add_circle("primary", 12.5, -26.6, 0.9, filled=True)
    mb.add_arc_pts("detail", (7.2, -21.8), (17.5, -22.5), -1.5)

    # Strong aquiline Renaissance nose (sloping cleanly down-right)
    mb.add_arc_pts("primary", (4.5, -30.8), (8.4, -20.5), -0.45)
    mb.add_arc_pts("primary", (8.4, -20.5), (11.4, -13.2), 0.6)
    mb.add_arc_pts("detail", (1.2, -24.8), (2.2, -15.8), 0.4)
    # Sculpted nose tip & left nostril wing
    mb.add_arc_pts("primary", (11.4, -13.2), (8.8, -9.4), 0.95)
    mb.add_arc_pts("primary", (8.8, -9.4), (3.8, -9.0), 0.65)
    mb.add_arc_pts("primary", (3.8, -9.0), (-1.2, -11.2), 0.85)
    mb.add_arc_pts("primary", (-1.2, -11.2), (-3.0, -14.2), 0.9)
    mb.add_arc_pts("detail", (-3.0, -14.2), (-1.6, -16.8), 0.5)
    mb.add_arc_pts("detail", (4.8, -11.2), (0.6, -12.0), -0.5)

    # Deep sage nasolabial folds framing cheeks into mustache
    mb.add_arc_pts("detail", (-3.8, -14.8), (-14.5, -4.5), -1.4)
    mb.add_arc_pts("detail", (12.2, -11.2), (19.5, -3.5), 1.0)

    # Solemn downturned philosopher's mouth & sweeping patriarch mustache
    mb.add_arc_pts("primary", (-6.2, 2.2), (4.5, -1.6), 1.4)
    mb.add_arc_pts("primary", (4.5, -1.6), (14.5, 2.4), 1.4)
    mb.add_arc_pts("detail", (-1.8, 2.6), (8.5, 2.6), -1.1)

    # Sweeping mustache draping around downturned mouth into beard
    mb.add_arc_pts("primary", (2.0, -7.2), (-8.5, -3.2), -1.4)
    mb.add_arc_pts("primary", (-8.5, -3.2), (-18.5, 4.8), -1.6)
    mb.add_arc_pts("primary", (5.5, -7.0), (14.8, -2.8), 1.4)
    mb.add_arc_pts("primary", (14.8, -2.8), (22.5, 4.5), 1.4)
    mb.add_wave("detail", (0.5, -5.2), (-15.5, 3.8), 3, wave_angle_deg * 0.65, -1)
    mb.add_wave("detail", (6.5, -5.2), (19.5, 3.5), 3, wave_angle_deg * 0.65, 1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Cascading Flowing Hair & Majestic Patriarch Beard (Euclid III.12)
    # -------------------------------------------------------------------------
    # Outer left cascading sage hair silhouette (smooth grand flow, clear of left motif!)
    mb.add_arc_pts("primary", (-22.0, -47.5), (-38.0, -33.0), -2.8)
    mb.add_arc_pts("primary", (-38.0, -33.0), (-49.5, 2.0), -2.6)
    mb.add_arc_pts("primary", (-49.5, 2.0), (-58.5, 44.0), -3.2)
    mb.add_arc_pts("primary", (-58.5, 44.0), (-54.5, 76.0), -2.4)

    # Right sparse flowing hair wisps & beard outer boundary (gracefully curving down to rim)
    mb.add_arc_pts("primary", (22.8, -42.5), (29.5, -28.0), 1.8)
    mb.add_arc_pts("primary", (29.5, -28.0), (28.0, -6.0), 1.8)
    mb.add_arc_pts("primary", (28.0, -6.0), (35.5, 36.0), 2.8)
    mb.add_arc_pts("primary", (35.5, 36.0), (31.5, 83.5), 2.4)

    # Cascading Euclid III.12 left hair waves (sweeping diagonally down-left)
    mb.add_wave("detail", (-33.5, -36.5), (-52.5, 56.0), 5, wave_angle_deg * 0.9, -1)
    mb.add_wave("detail", (-29.0, -28.0), (-45.5, 68.0), 5, wave_angle_deg * 0.85, 1)
    mb.add_wave("detail", (-25.5, -16.0), (-36.5, 76.5), 5, wave_angle_deg * 0.85, -1)
    # Subtle hair-to-beard boundary cascade from left cheek
    mb.add_wave("detail", (-22.0, -2.0), (-26.5, 82.0), 4, wave_angle_deg * 0.75, 1)

    # Majestic patriarch beard (broader, grander S-waves converging gently toward bottom rim)
    mb.add_wave("detail", (-14.5, 6.5), (-16.0, 84.5), 4, wave_angle_deg * 0.72, -1)
    mb.add_wave("detail", (-6.0, 6.0), (-6.5, 85.5), 4, wave_angle_deg * 0.68, 1)
    mb.add_wave("detail", (3.0, 5.5), (3.5, 85.5), 4, wave_angle_deg * 0.68, -1)
    mb.add_wave("detail", (12.5, 6.0), (14.5, 84.5), 4, wave_angle_deg * 0.72, 1)
    mb.add_wave("detail", (21.5, 4.5), (25.0, 80.5), 4, wave_angle_deg * 0.75, -1)

    # Flush sage cloak shoulders anchoring the lower medallion flanks cleanly to MED_R
    mb.add_arc_pts("primary", (-58.5, 44.0), (-75.5, 73.0), -3.0)
    mb.add_arc_pts("primary", (35.5, 36.0), (77.0, 71.0), 4.8)
    mb.add_arc_pts("detail", (44.0, 44.0), (59.5, 76.0), 2.2)

    return mb.build()


def build_leonardo_svg(theme: str = "dark", wave_angle_deg: float = 32.0) -> str:
    """Render the Leonardo da Vinci medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_leonardo_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_leonardo_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 32.0,
) -> tuple[Path, Path]:
    """Write ``leonardo_dark.svg`` and ``leonardo_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "leonardo_dark.svg"
    light_path = target_dir / "leonardo_light.svg"
    dark_path.write_text(
        build_leonardo_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_leonardo_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
