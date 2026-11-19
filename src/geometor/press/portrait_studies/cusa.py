"""Study 18: Nicholas of Cusa (after Cusanusstift donor portrait, c. 1470) in lines and arcs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_cusa_elements",
    "build_cusa_svg",
    "write_cusa_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_coincidentia_polygons_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 11.8,
) -> None:
    """Draw *Coincidentia Oppositorum* (inscribed square/octagon & circumscribed square).

    Placed in the open left medallion margin, illustrating Cusa's *De Docta Ignorantia*
    limit in which inscribed and circumscribed regular polygons converge on the circle.
    """
    # Limit circle
    mb.add_circle("golden", cx, cy, radius)

    # Circumscribed square tangent at the four cardinal points
    mb.add_line("golden", cx - radius, cy - radius, cx + radius, cy - radius)
    mb.add_line("golden", cx + radius, cy - radius, cx + radius, cy + radius)
    mb.add_line("golden", cx + radius, cy + radius, cx - radius, cy + radius)
    mb.add_line("golden", cx - radius, cy + radius, cx - radius, cy - radius)

    # Inscribed regular octagon (8 vertices)
    oct_pts = [polar(cx, cy, radius, -90.0 + 45.0 * k) for k in range(8)]
    for k in range(8):
        p1 = oct_pts[k]
        p2 = oct_pts[(k + 1) % 8]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Inscribed square (4 cardinal vertices) highlighting the 4 -> 8 -> infinity progression
    sq_pts = [oct_pts[0], oct_pts[2], oct_pts[4], oct_pts[6]]
    for k in range(4):
        p1 = sq_pts[k]
        p2 = sq_pts[(k + 1) % 4]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
        mb.add_circle("golden", p1[0], p1[1], 0.8)

    mb.add_circle("golden", cx, cy, 1.0, filled=True)


def _add_infinite_circle_tangent_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw expanding internally tangent circles approaching the infinite straight line.

    Honors Cusa's celebrated proof (*De Docta Ignorantia*, Book I Ch. 13) that as a
    circle's radius grows without bound, its circumference coincides with its tangent line.
    """
    x_tan = cx + 11.8
    half_line = 14.8

    # Limiting vertical tangent line at contact point T = (x_tan, cy)
    mb.add_line("golden", x_tan, cy - half_line, x_tan, cy + half_line)

    # Three nested full circles internally tangent at T
    radii = (4.2, 7.8, 11.8)
    for r in radii:
        mb.add_circle("golden", x_tan - r, cy, r)
        mb.add_circle("golden", x_tan - r, cy, 0.55)

    # Fourth larger limiting circular arc (r = 25.0) flattening toward the tangent line
    r_lim = 25.0
    mb.add_arc("golden", x_tan - r_lim, cy, r_lim, -33.0, 33.0)

    # Horizontal axis of centers to the shared contact point T
    mb.add_line("golden", x_tan - 2.0 * radii[-1], cy, x_tan, cy)
    mb.add_circle("golden", x_tan, cy, 1.15, filled=True)


def build_cusa_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Nicholas of Cusa medallion strictly from lines, circles, and circular arcs.

    Calibrated to the Cusanusstift Bernkastel-Kues donor portrait (c. 1460-1480),
    featuring Cusa's serene three-quarter left devotional gaze, tonsured bald crown,
    refined ascetic features, slung crimson cardinal's *galero* hat with diagonal cord,
    white surplice V-collar, flowing cardinal mantle, and gracefully raised hands.

    Args:
        wave_angle_deg: Half-angle (degrees) reserved for subtle Euclid III.12 mantle accents.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    _ = wave_angle_deg
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-10.8,
        eye_rx=3.0,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Coincidentia Polygons (Left) & Infinite Circle Limit (Right)
    # -------------------------------------------------------------------------
    _add_coincidentia_polygons_motif(mb, cx=-63.0, cy=-26.0, radius=11.8)
    _add_infinite_circle_tangent_motif(mb, cx=63.0, cy=-29.5)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Tonsured Bald Dome, Ascetic Three-Quarter Left Face & Ear
    # -------------------------------------------------------------------------
    # Smooth rounded tonsured bald cranial dome & back of head
    mb.add_arc_pts("primary", (-11.5, -45.5), (24.0, -48.5), 6.6)
    mb.add_arc_pts("primary", (24.0, -48.5), (35.5, -36.0), 2.4)
    mb.add_arc_pts("primary", (35.5, -36.0), (35.8, -19.0), 1.8)
    mb.add_arc_pts("primary", (35.8, -19.0), (31.5, -9.5), 1.2)

    # Short cropped monastic tonsure fringe framing right temple & nape
    mb.add_arc_pts("primary", (14.5, -44.8), (27.5, -38.8), 1.6)
    mb.add_arc_pts("primary", (27.5, -38.8), (34.8, -26.0), 1.6)
    mb.add_arc_pts("primary", (14.5, -44.8), (23.2, -35.2), -1.2)
    mb.add_arc_pts("primary", (23.2, -35.2), (24.5, -20.5), 1.2)
    mb.add_arc_pts("primary", (24.5, -20.5), (22.5, -14.5), 0.7)
    for t_p1, t_p2 in (
        ((16.8, -43.6), (15.8, -41.4)),
        ((19.5, -42.6), (18.2, -39.8)),
        ((22.2, -41.4), (20.4, -38.0)),
        ((24.8, -39.8), (22.4, -36.0)),
        ((27.2, -38.0), (24.0, -33.5)),
        ((29.5, -35.5), (25.0, -30.5)),
        ((31.4, -32.4), (25.8, -27.2)),
        ((32.8, -28.8), (26.4, -23.8)),
        ((33.6, -24.8), (26.8, -20.4)),
    ):
        mb.add_line("detail", t_p1[0], t_p1[1], t_p2[0], t_p2[1])

    # Sculpted right ear
    mb.add_arc_pts("primary", (20.5, -15.0), (27.5, -14.2), 1.8)
    mb.add_arc_pts("primary", (27.5, -14.2), (26.0, -5.5), 1.6)
    mb.add_arc_pts("primary", (26.0, -5.5), (20.2, -1.5), 1.5)
    mb.add_arc_pts("primary", (20.2, -1.5), (17.5, -4.5), 0.9)
    mb.add_arc_pts("detail", (21.2, -12.5), (24.8, -10.5), 1.2)
    mb.add_arc_pts("detail", (24.8, -10.5), (22.2, -5.0), 1.2)

    # Left ascetic facial profile silhouette (tilted ~12 deg clockwise)
    mb.add_arc_pts("primary", (-11.5, -45.5), (-13.8, -37.2), -0.8)
    mb.add_arc_pts("primary", (-13.8, -37.2), (-15.5, -31.5), 0.5)
    mb.add_arc_pts("primary", (-15.5, -31.5), (-18.8, -23.0), -1.1)
    mb.add_arc_pts("primary", (-18.8, -23.0), (-19.2, -14.5), -1.0)
    mb.add_arc_pts("primary", (-19.2, -14.5), (-18.2, -6.5), -0.8)
    mb.add_arc_pts("primary", (-18.2, -6.5), (-14.2, 1.0), -1.4)
    # Refined chin & sturdy prelate jawline rising to right ear
    mb.add_arc_pts("primary", (-14.2, 1.0), (-3.0, 5.2), -1.6)
    mb.add_arc_pts("primary", (-3.0, 5.2), (11.5, 2.5), -1.6)
    mb.add_arc_pts("primary", (11.5, 2.5), (19.5, -3.5), -1.2)
    mb.add_arc_pts("detail", (-10.0, 6.2), (6.5, 7.2), -1.4)

    # Subtle ascetic forehead creases (detail)
    mb.add_arc_pts("detail", (-8.5, -42.0), (8.5, -37.5), -0.8)
    mb.add_arc_pts("detail", (-9.5, -39.0), (9.0, -34.5), -0.7)

    # Gentle contemplative eyebrows
    mb.add_arc_pts("primary", (-14.2, -36.2), (-10.2, -37.2), 0.8)
    mb.add_arc_pts("primary", (-10.2, -37.2), (-5.8, -33.8), 0.7)

    mb.add_arc_pts("primary", (-2.0, -32.2), (4.0, -32.4), 1.2)
    mb.add_arc_pts("primary", (4.0, -32.4), (11.8, -28.8), 1.0)
    mb.add_arc_pts("detail", (-1.2, -33.6), (11.0, -30.2), 1.3)

    # Serene devotional eyes lifted slightly upward-left along y = -27
    # Viewer's left eye (further eye)
    l_out = (-14.2, -31.8)
    l_in = (-6.8, -29.2)
    mb.add_arc_pts("primary", l_out, l_in, 1.8)
    mb.add_arc_pts("detail", (-14.2, -33.8), (-6.6, -31.2), 1.8)
    mb.add_arc_pts("detail", l_out, l_in, -1.0)
    mb.add_circle("detail", -10.8, -30.6, 1.6)
    mb.add_circle("primary", -11.2, -30.8, 0.85, filled=True)
    mb.add_arc_pts("detail", (-14.0, -28.6), (-7.2, -26.5), -0.8)

    # Viewer's right eye (nearer eye)
    r_in = (-1.8, -26.5)
    r_out = (8.8, -24.2)
    mb.add_arc_pts("primary", r_in, r_out, 2.2)
    mb.add_arc_pts("detail", (-2.4, -28.8), (9.4, -26.4), 2.2)
    mb.add_arc_pts("detail", r_in, r_out, -1.2)
    mb.add_circle("detail", 3.0, -25.4, 1.95)
    mb.add_circle("primary", 2.5, -25.7, 0.95, filled=True)
    mb.add_arc_pts("detail", (-1.8, -23.0), (8.8, -21.5), -1.3)

    # Refined ascetic nose
    mb.add_arc_pts("primary", (-5.0, -32.0), (-10.2, -24.8), 0.45)
    mb.add_arc_pts("primary", (-10.2, -24.8), (-14.8, -19.0), -0.55)
    mb.add_arc_pts("primary", (-14.8, -19.0), (-12.2, -16.5), -0.95)
    mb.add_arc_pts("primary", (-12.2, -16.5), (-8.2, -16.2), -0.6)
    mb.add_arc_pts("primary", (-8.2, -16.2), (-5.5, -17.8), -0.8)
    mb.add_arc_pts("detail", (-5.5, -17.8), (-6.5, -20.2), -0.55)
    mb.add_arc_pts("detail", (-11.5, -17.8), (-8.5, -17.4), 0.45)

    # Resolute contemplative mouth & ascetic cheek line
    mb.add_arc_pts("detail", (-11.5, -15.8), (-12.5, -12.5), 0.3)
    mb.add_arc_pts("detail", (-16.2, -12.0), (-12.0, -12.4), 0.55)
    mb.add_arc_pts("detail", (-12.0, -12.4), (-6.0, -9.8), 0.65)
    mb.add_arc_pts("primary", (-16.8, -11.0), (-11.5, -10.5), 0.45)
    mb.add_arc_pts("primary", (-11.5, -10.5), (-5.2, -7.2), 0.6)
    mb.add_arc_pts("detail", (-15.4, -9.2), (-10.8, -7.8), -0.7)
    mb.add_arc_pts("detail", (-10.8, -7.8), (-6.8, -6.8), -0.45)
    mb.add_arc_pts("detail", (-15.5, -5.5), (-10.5, -4.2), -0.7)
    mb.add_arc_pts("detail", (-5.2, -16.5), (-2.0, -8.0), 1.1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Slung Cardinal Galero Hat, White Surplice & Crimson Mantle
    # -------------------------------------------------------------------------
    # Broad-brimmed crimson cardinal's galero hat slung cleanly behind right shoulder
    mb.add_arc_pts("primary", (36.0, -17.5), (55.5, 4.0), 3.6)
    mb.add_arc_pts("primary", (55.5, 4.0), (66.5, 36.5), 4.2)
    mb.add_arc_pts("primary", (66.5, 36.5), (61.5, 74.0), 3.2)
    mb.add_arc_pts("primary", (36.0, -17.5), (43.5, 11.5), -1.8)
    # Raised rounded hat crown boss on outer brim & galero cord button
    mb.add_arc_pts("primary", (51.0, 10.5), (63.5, 22.5), 3.0)
    mb.add_arc_pts("primary", (63.5, 22.5), (61.0, 40.5), 2.6)
    mb.add_circle("detail", 57.5, 17.5, 1.4)

    # Diagonal cardinal hat cord slinging flush from mantle/galero across crimson robe
    mb.add_arc_pts("primary", (45.2, 22.5), (1.5, 82.0), -2.4)
    mb.add_arc_pts("detail", (46.5, 24.5), (3.5, 83.0), -2.4)

    # White surplice / rochet collar & V-front opening
    mb.add_arc_pts("primary", (-11.2, 9.2), (3.5, 17.8), -1.8)
    mb.add_arc_pts("primary", (3.5, 17.8), (36.5, -2.5), -2.4)
    mb.add_arc_pts("detail", (-9.5, 7.2), (3.5, 15.2), -1.6)
    mb.add_arc_pts("detail", (3.5, 15.2), (34.0, -4.0), -2.2)

    # Crimson cardinal mantle lapels framing the white surplice
    mb.add_arc_pts("primary", (-11.2, 9.2), (-20.8, 35.0), -1.4)
    mb.add_arc_pts("primary", (-20.8, 35.0), (-20.0, 56.5), -0.8)
    mb.add_arc_pts("primary", (36.5, -2.5), (19.5, 36.5), -2.0)
    mb.add_arc_pts("primary", (19.5, 36.5), (-3.5, 74.5), -1.8)

    # Pleated white surplice folds (detail)
    mb.add_arc_pts("detail", (-4.5, 18.0), (-10.0, 54.0), -1.4)
    mb.add_arc_pts("detail", (5.5, 17.5), (-1.5, 62.0), -1.4)
    mb.add_arc_pts("detail", (15.5, 14.0), (6.5, 50.0), -1.2)

    # Flowing crimson cardinal shoulders & robe (cleanly occluded behind raised left hand!)
    mb.add_arc_pts("primary", (-11.2, 9.2), (-38.0, 28.5), -2.6)
    mb.add_arc_pts("primary", (-44.5, 57.5), (-49.8, 80.0), -1.4)
    mb.add_arc_pts("primary", (36.5, -2.5), (55.0, 79.0), 4.8)
    mb.add_arc_pts("detail", (35.5, 22.0), (43.5, 80.5), 2.4)
    mb.add_arc_pts("detail", (22.5, 42.0), (26.5, 84.5), 1.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Gracefully Raised Hands in Devotional Contemplation
    # -------------------------------------------------------------------------
    # Viewer's left hand (raised gently at left shoulder; negative sagittas round fingertips!)
    # Thumb on right side of hand
    mb.add_arc_pts("primary", (-37.5, 39.0), (-38.2, 25.0), 0.9)
    mb.add_arc_pts("primary", (-38.2, 25.0), (-41.4, 25.2), -1.1)
    mb.add_arc_pts("primary", (-41.4, 25.2), (-42.5, 36.0), 0.6)
    # Slender upturned Gothic-Renaissance fingers with rounded convex tips
    mb.add_arc_pts("primary", (-42.5, 36.0), (-50.5, 18.0), 0.7)
    mb.add_arc_pts("primary", (-50.5, 18.0), (-53.5, 19.6), -1.1)
    mb.add_arc_pts("primary", (-53.5, 19.6), (-46.8, 36.8), -0.6)
    mb.add_arc_pts("primary", (-53.5, 19.6), (-57.2, 22.8), -1.1)
    mb.add_arc_pts("primary", (-57.2, 22.8), (-51.2, 41.0), -0.7)
    mb.add_arc_pts("primary", (-57.2, 22.8), (-58.6, 30.8), -1.1)
    mb.add_arc_pts("primary", (-58.6, 30.8), (-52.8, 49.0), -1.0)
    mb.add_arc_pts("primary", (-52.8, 49.0), (-44.5, 57.5), -1.2)
    mb.add_arc_pts("detail", (-49.2, 39.0), (-43.0, 50.5), -0.8)

    # Viewer's right hand (resting gracefully across lower chest with rounded fingertips!)
    # Thumb lifting smoothly on right
    mb.add_arc_pts("primary", (-10.8, 64.5), (-14.2, 48.2), 1.1)
    mb.add_arc_pts("primary", (-14.2, 48.2), (-17.6, 49.5), -1.1)
    mb.add_arc_pts("primary", (-17.6, 49.5), (-16.8, 62.5), 0.6)
    # Slender prayer fingers angling up-left across chest
    mb.add_arc_pts("primary", (-16.8, 62.5), (-35.5, 47.0), 0.9)
    mb.add_arc_pts("primary", (-35.5, 47.0), (-37.8, 49.6), -1.1)
    mb.add_arc_pts("primary", (-37.8, 49.6), (-22.0, 64.5), -0.7)
    mb.add_arc_pts("primary", (-37.8, 49.6), (-39.0, 53.2), -1.0)
    mb.add_arc_pts("primary", (-39.0, 53.2), (-23.8, 68.8), -0.7)
    mb.add_arc_pts("primary", (-39.0, 53.2), (-37.2, 58.5), -1.0)
    mb.add_arc_pts("primary", (-37.2, 58.5), (-23.5, 76.0), -1.2)
    # Wrist & lower palm descending cleanly to bottom medallion rim
    mb.add_arc_pts("primary", (-23.5, 76.0), (-13.0, 86.0), -1.2)
    mb.add_arc_pts("primary", (-10.8, 64.5), (-1.5, 86.0), 1.2)
    mb.add_arc_pts("detail", (-20.5, 68.0), (-11.5, 80.0), -0.8)

    return mb.build()


def build_cusa_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Nicholas of Cusa medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_cusa_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_cusa_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``cusa_dark.svg`` and ``cusa_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "cusa_dark.svg"
    light_path = target_dir / "cusa_light.svg"
    dark_path.write_text(
        build_cusa_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_cusa_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
