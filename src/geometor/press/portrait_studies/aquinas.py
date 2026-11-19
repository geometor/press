"""Study 09: St. Thomas Aquinas (after Carlo Crivelli, 1476) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_aquinas_elements",
    "build_aquinas_svg",
    "write_aquinas_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_sun_of_materia_intelligibilis(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    disk_r: float = 7.6,
    long_ray_r: float = 18.2,
    short_ray_r: float = 13.6,
) -> None:
    """Draw Aquinas's radiant 16-ray chest Sun of *Materia Intelligibilis*."""
    # Concentric golden solar boss
    mb.add_circle("golden", cx, cy, disk_r)
    mb.add_circle("golden", cx, cy, disk_r * 0.68)
    mb.add_circle("golden", cx, cy, 1.15)

    # 16 compass rays (8 principal cardinal/ordinal + 8 intermediate)
    for k in range(16):
        angle = k * 22.5
        r_end = long_ray_r if k % 2 == 0 else short_ray_r
        p1 = polar(cx, cy, disk_r + 0.6, angle)
        p2 = polar(cx, cy, r_end, angle)
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])


def _add_degrees_of_abstraction_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    side: float = 32.0,
) -> None:
    """Draw the Three Degrees of Abstraction Triangle (*Physica*, *Mathematica*, *Metaphysica*).

    Placed in the open left medallion margin toward which Aquinas lifts his gaze.
    Divided into three equal horizontal strata with an inscribed compass circle in
    the middle (*Mathematica*) tier.
    """
    height = side * math.sqrt(3.0) / 2.0
    y_apex = cy - (2.0 / 3.0) * height
    y_base = cy + (1.0 / 3.0) * height
    half_s = 0.5 * side

    apex = (cx, y_apex)
    bl = (cx - half_s, y_base)
    br = (cx + half_s, y_base)

    # Outer equilateral triangle
    mb.add_line("golden", apex[0], apex[1], bl[0], bl[1])
    mb.add_line("golden", apex[0], apex[1], br[0], br[1])
    mb.add_line("golden", bl[0], bl[1], br[0], br[1])

    # Three equal horizontal strata dividers
    y1 = y_apex + height / 3.0
    y2 = y_apex + 2.0 * height / 3.0
    hw1 = side / 6.0
    hw2 = side / 3.0
    mb.add_line("golden", cx - hw1, y1, cx + hw1, y1)
    mb.add_line("golden", cx - hw2, y2, cx + hw2, y2)

    # Inscribed compass circle in the middle Mathematica stratum (tangent to y1 & y2)
    mid_y = 0.5 * (y1 + y2)
    mid_r = height / 6.0
    mb.add_circle("golden", cx, mid_y, mid_r)
    mb.add_circle("golden", cx, mid_y, 0.95)

    # Three vertex nodes
    for vx, vy in (apex, bl, br):
        mb.add_circle("golden", vx, vy, 1.0)


def build_aquinas_elements(wave_angle_deg: float = 32.0) -> dict[str, list[dict[str, Any]]]:
    """Construct St. Thomas Aquinas medallion strictly from lines, circles, and circular arcs.

    Calibrated to Carlo Crivelli's *St. Thomas Aquinas* (1476, National Gallery, London)
    with three-quarter left upward-lifted gaze, concentric Dominican tonsure crown,
    strong Roman nose, sculpted ear, black Dominican hood & scapular habit, and
    signature golden Sun of *Materia Intelligibilis*.

    Args:
        wave_angle_deg: Half-angle (degrees) reserved for subtle Euclid III.12 drapery/hair accents.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    _ = wave_angle_deg
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-12.5,
        eye_rx=1.5,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Radiant Chest Sun & Three Degrees of Abstraction
    # -------------------------------------------------------------------------
    _add_sun_of_materia_intelligibilis(
        mb,
        cx=-2.5,
        cy=43.0,
        disk_r=7.5,
        long_ray_r=17.4,
        short_ray_r=13.0,
    )
    _add_degrees_of_abstraction_motif(mb, cx=-60.0, cy=-28.0, side=32.0)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Cranial Dome, Dominican Tonsure Band & Sculpted Ear
    # -------------------------------------------------------------------------
    # Smooth rounded bald cranial dome above the tonsure
    mb.add_arc_pts("primary", (-12.5, -45.5), (0.0, -50.2), 2.1)
    mb.add_arc_pts("primary", (0.0, -50.2), (18.5, -49.0), 2.3)
    mb.add_arc_pts("primary", (18.5, -49.0), (33.5, -41.5), 2.2)
    mb.add_arc_pts("primary", (33.5, -41.5), (38.0, -28.0), 1.8)

    # Crisp Dominican tonsure crown band (concentric circular arcs)
    # Front central forehead tuft
    mb.add_arc_pts("primary", (-5.5, -48.5), (2.2, -43.8), -1.7)
    mb.add_arc_pts("primary", (2.2, -43.8), (8.5, -46.8), -1.3)
    # Main tonsure band wrapping over right temple toward back of head
    # Upper hairline edge of tonsure
    mb.add_arc_pts("primary", (9.5, -45.0), (24.5, -41.5), 1.8)
    mb.add_arc_pts("primary", (24.5, -41.5), (34.5, -31.0), 2.0)
    mb.add_arc_pts("primary", (34.5, -31.0), (38.0, -20.5), 1.5)
    # Lower forehead/temple hairline edge of tonsure
    mb.add_arc_pts("primary", (9.5, -45.0), (19.5, -37.5), -1.4)
    mb.add_arc_pts("primary", (19.5, -37.5), (26.0, -27.5), 1.4)
    mb.add_arc_pts("primary", (26.0, -27.5), (25.5, -18.5), 1.0)
    # Hair fringe behind ear tapering into nape/hood
    mb.add_arc_pts("primary", (28.0, -18.5), (35.5, -19.5), -1.2)
    mb.add_arc_pts("primary", (25.5, -8.5), (33.5, -14.0), -1.0)

    # Fine closely cropped radial tonsure fringe strokes (detail)
    for t_p1, t_p2 in (
        ((-3.2, -47.6), (-2.2, -45.2)),
        ((-0.8, -47.4), (-0.2, -44.6)),
        ((1.8, -47.2), (2.0, -44.4)),
        ((4.5, -47.0), (4.8, -44.8)),
        ((12.0, -43.8), (11.2, -41.4)),
        ((14.8, -43.2), (13.6, -40.2)),
        ((17.8, -42.4), (16.0, -38.8)),
        ((20.8, -41.2), (18.5, -37.2)),
        ((23.8, -39.6), (20.8, -35.2)),
        ((26.6, -37.6), (23.0, -32.8)),
        ((29.2, -35.0), (24.8, -30.2)),
        ((31.5, -32.0), (26.4, -27.4)),
        ((33.4, -28.8), (27.4, -24.4)),
        ((34.8, -25.4), (28.0, -21.8)),
        ((35.8, -22.2), (29.2, -19.8)),
    ):
        mb.add_line("detail", t_p1[0], t_p1[1], t_p2[0], t_p2[1])

    # Sculpted Quattrocento ear (right side of face)
    mb.add_arc_pts("primary", (22.0, -17.5), (29.2, -17.0), 2.0)
    mb.add_arc_pts("primary", (29.2, -17.0), (27.5, -8.0), 1.8)
    mb.add_arc_pts("primary", (27.5, -8.0), (21.5, -4.0), 1.6)
    mb.add_arc_pts("primary", (21.5, -4.0), (18.2, -6.5), 1.0)
    # Inner ear helix & concha
    mb.add_arc_pts("detail", (22.2, -15.2), (26.8, -14.2), 1.4)
    mb.add_arc_pts("detail", (26.8, -14.2), (24.2, -7.8), 1.4)
    mb.add_arc_pts("detail", (20.8, -12.5), (22.2, -8.0), -1.1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Three-Quarter Left Facial Profile, Eyes, Nose, Mouth & Jaw
    # -------------------------------------------------------------------------
    # Left facial profile silhouette (forehead -> brow -> cheek -> firm chin -> jawline)
    mb.add_arc_pts("primary", (-12.5, -45.5), (-14.5, -37.2), -0.9)
    mb.add_arc_pts("primary", (-14.5, -37.2), (-16.2, -31.5), 0.6)
    mb.add_arc_pts("primary", (-16.2, -31.5), (-19.6, -23.5), -1.1)
    mb.add_arc_pts("primary", (-19.6, -23.5), (-19.8, -14.5), -1.1)
    mb.add_arc_pts("primary", (-19.8, -14.5), (-19.0, -6.5), -0.9)
    mb.add_arc_pts("primary", (-19.0, -6.5), (-14.0, -0.5), -1.6)
    # Firm chin & sturdy jowl curving to below the ear
    mb.add_arc_pts("primary", (-14.0, -0.5), (-2.5, 2.0), -1.6)
    mb.add_arc_pts("primary", (-2.5, 2.0), (11.5, -0.5), -1.8)
    mb.add_arc_pts("primary", (11.5, -0.5), (18.5, -6.2), -1.2)
    # Secondary sturdy throat/chin crease (detail)
    mb.add_arc_pts("detail", (-11.5, 3.0), (4.5, 4.2), -1.6)
    mb.add_arc_pts("detail", (4.5, 4.2), (17.5, -1.5), -1.2)

    # Forehead & brow creases (subtle contemplative furrows)
    mb.add_arc_pts("detail", (-10.0, -42.5), (6.5, -37.2), -0.8)
    mb.add_arc_pts("detail", (-10.8, -39.2), (7.0, -34.2), -0.7)

    # Noble arched eyebrows
    # Viewer's left eyebrow (foreshortened)
    mb.add_arc_pts("primary", (-15.2, -35.8), (-11.5, -37.0), 0.9)
    mb.add_arc_pts("primary", (-11.5, -37.0), (-7.0, -33.6), 0.8)
    # Viewer's right eyebrow (broad, lifted slightly in contemplation)
    mb.add_arc_pts("primary", (-3.5, -32.2), (2.5, -32.6), 1.3)
    mb.add_arc_pts("primary", (2.5, -32.6), (9.8, -29.0), 1.1)
    mb.add_arc_pts("detail", (-2.8, -33.6), (9.2, -30.5), 1.5)

    # Eyes (three-quarter left gaze lifted slightly upward)
    # Viewer's left eye (foreshortened further eye)
    l_out = (-15.4, -31.2)
    l_in = (-8.5, -28.8)
    mb.add_arc_pts("primary", l_out, l_in, 1.8)
    mb.add_arc_pts("detail", (-15.4, -33.2), (-8.2, -30.6), 1.8)
    mb.add_arc_pts("detail", l_out, l_in, -1.1)
    mb.add_circle("detail", -12.4, -30.4, 1.65)
    mb.add_circle("primary", -12.8, -30.6, 0.85, filled=True)
    mb.add_arc_pts("detail", (-15.5, -28.0), (-9.0, -26.2), -0.9)

    # Viewer's right eye (nearer, clear upward-left contemplative gaze)
    r_in = (-3.2, -26.4)
    r_out = (6.8, -24.0)
    mb.add_arc_pts("primary", r_in, r_out, 2.3)
    mb.add_arc_pts("detail", (-3.8, -28.8), (7.6, -26.0), 2.3)
    mb.add_arc_pts("detail", r_in, r_out, -1.3)
    mb.add_circle("detail", 1.3, -25.4, 2.0)
    mb.add_circle("primary", 0.8, -25.6, 1.0, filled=True)
    # Sculpted Quattrocento lower-lid pouch & cheek crease
    mb.add_arc_pts("detail", (-3.2, -22.8), (7.2, -21.2), -1.4)
    mb.add_arc_pts("detail", (6.5, -23.0), (11.2, -22.2), 0.5)

    # Strong Roman aquiline nose (smooth Quattrocento bridge)
    mb.add_arc_pts("primary", (-6.5, -32.0), (-11.2, -25.2), 0.45)
    mb.add_arc_pts("primary", (-11.2, -25.2), (-16.6, -19.5), -0.55)
    # Rounded tip, nostril underside & alar wing
    mb.add_arc_pts("primary", (-16.6, -19.5), (-14.2, -17.4), -1.0)
    mb.add_arc_pts("primary", (-14.2, -17.4), (-10.2, -17.0), -0.6)
    mb.add_arc_pts("primary", (-10.2, -17.0), (-6.8, -18.2), -0.8)
    mb.add_arc_pts("primary", (-6.8, -18.2), (-7.6, -20.8), -0.8)
    mb.add_arc_pts("detail", (-13.5, -18.6), (-10.4, -18.0), 0.55)

    # Solemn, dignified mouth & sculpted chin (primary parting line; refined detail lips)
    mb.add_arc_pts("detail", (-13.2, -16.8), (-14.4, -13.5), 0.35)
    # Upper lip bow (detail so mouth stays composed, not heavy)
    mb.add_arc_pts("detail", (-17.5, -12.6), (-14.0, -13.0), 0.55)
    mb.add_arc_pts("detail", (-14.0, -13.0), (-7.8, -10.2), 0.7)
    # Crisp primary mouth parting line
    mb.add_arc_pts("primary", (-18.0, -11.4), (-13.0, -11.0), 0.5)
    mb.add_arc_pts("primary", (-13.0, -11.0), (-6.5, -7.8), 0.65)
    # Lower lip edge & mentolabial hollow (detail)
    mb.add_arc_pts("detail", (-16.8, -9.8), (-12.5, -8.5), -0.7)
    mb.add_arc_pts("detail", (-12.5, -8.5), (-8.5, -7.6), -0.5)
    mb.add_arc_pts("detail", (-16.8, -6.2), (-11.8, -4.6), -0.75)

    # Cheek nasolabial fold & restrained Quattrocento modeling line
    mb.add_arc_pts("detail", (-6.2, -17.0), (-2.5, -8.0), 1.3)
    mb.add_arc_pts("detail", (-2.5, -8.0), (-4.0, -1.5), 0.7)
    mb.add_arc_pts("detail", (6.0, -16.8), (4.6, -9.5), -0.7)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Black Dominican Hood, Cowl Collar & Monastic Habit
    # -------------------------------------------------------------------------
    # Sweeping hood outline behind head on the right
    mb.add_arc_pts("primary", (22.0, -47.5), (39.0, -41.5), 2.8)
    mb.add_arc_pts("primary", (39.0, -41.5), (47.5, -27.5), 2.6)
    mb.add_arc_pts("primary", (47.5, -27.5), (51.5, -10.0), 2.2)
    mb.add_arc_pts("primary", (51.5, -10.0), (54.8, 3.5), 1.6)
    mb.add_arc_pts("primary", (54.8, 3.5), (51.5, 10.0), 1.2)
    # Inner hood opening edge behind ear/neck
    mb.add_arc_pts("detail", (36.5, -35.0), (42.0, -12.0), 2.2)
    mb.add_arc_pts("detail", (42.0, -12.0), (37.5, 4.5), 1.8)

    # Left cowl & sweeping tailored shoulder (single grand arc to medallion rim)
    mb.add_arc_pts("primary", (-20.0, -3.5), (-33.0, 3.8), -2.0)
    mb.add_arc_pts("primary", (-33.0, 3.8), (-41.0, 14.0), -2.2)
    mb.add_arc_pts("primary", (-41.0, 14.0), (-48.5, 78.5), -5.0)

    # Right shoulder sweeping cleanly out and down to medallion rim
    mb.add_arc_pts("primary", (51.5, 10.0), (67.5, 27.5), 3.4)
    mb.add_arc_pts("primary", (67.5, 27.5), (82.0, 62.0), 3.2)

    # Layered Dominican cowl collar folds across neck & upper chest (above Sun)
    mb.add_arc_pts("primary", (-26.5, 0.5), (-5.0, 12.0), -2.5)
    mb.add_arc_pts("primary", (-5.0, 12.0), (22.0, 11.0), -2.3)
    mb.add_arc_pts("primary", (22.0, 11.0), (48.0, 6.5), -1.6)

    mb.add_arc_pts("primary", (-38.0, 12.0), (-11.5, 20.2), -2.3)
    mb.add_arc_pts("primary", (-11.5, 20.2), (20.5, 18.6), -2.1)
    mb.add_arc_pts("primary", (20.5, 18.6), (51.5, 10.0), -1.8)

    # Secondary cowl creases
    mb.add_arc_pts("detail", (-31.5, 6.5), (-8.0, 15.8), -2.0)
    mb.add_arc_pts("detail", (-8.0, 15.8), (21.5, 14.6), -1.8)
    mb.add_arc_pts("detail", (21.5, 14.6), (44.0, 8.8), -1.2)

    # Open black Dominican mantle lapels (single smooth continuous arcs to rim)
    mb.add_arc_pts("primary", (-24.5, 19.2), (-20.5, 86.0), 2.8)
    mb.add_arc_pts("primary", (22.0, 18.4), (35.5, 85.0), -3.2)

    # Sweeping drapery folds on left & right Dominican cloak (strictly non-crossing)
    mb.add_arc_pts("detail", (-37.0, 22.0), (-39.5, 79.0), -2.4)
    mb.add_arc_pts("detail", (-30.5, 24.0), (-31.5, 83.5), -1.8)

    mb.add_arc_pts("detail", (34.0, 19.5), (45.5, 77.0), 2.4)
    mb.add_arc_pts("detail", (45.0, 18.0), (59.5, 70.5), 2.8)
    mb.add_arc_pts("detail", (55.5, 22.0), (70.5, 64.5), 2.4)

    # Subtle vertical tunic folds below the Radiant Sun
    mb.add_arc_pts("detail", (-11.5, 63.0), (-10.0, 86.0), 0.9)
    mb.add_arc_pts("detail", (7.5, 63.0), (10.5, 85.5), -0.9)

    return mb.build()


def build_aquinas_svg(theme: str = "dark", wave_angle_deg: float = 32.0) -> str:
    """Render the St. Thomas Aquinas medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_aquinas_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_aquinas_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 32.0,
) -> tuple[Path, Path]:
    """Write ``aquinas_dark.svg`` and ``aquinas_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "aquinas_dark.svg"
    light_path = target_dir / "aquinas_light.svg"
    dark_path.write_text(
        build_aquinas_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_aquinas_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
