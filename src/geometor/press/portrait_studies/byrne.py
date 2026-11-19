"""Study 12: Oliver Byrne (after historic c. 1850 portrait) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_byrne_elements",
    "build_byrne_svg",
    "write_byrne_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_pythagorean_windmill_motif(
    mb: MedallionBuilder,
    hx: float,
    hy: float,
    scale: float = 2.4,
) -> None:
    """Draw Euclid I.47 (Pythagorean Windmill) in the open left medallion margin.

    Constructs an exact 3-4-5 right triangle with exterior squares on both legs
    and the horizontal hypotenuse, plus Euclid's altitude splitting the hypotenuse
    square into its two proportional area rectangles.
    """
    a_len = 3.0 * scale
    b_len = 4.0 * scale
    c_len = 5.0 * scale
    half_c = 0.5 * c_len

    # Hypotenuse A-B horizontal at y = hy; right-angle vertex C above
    a_pt = (hx - half_c, hy)
    b_pt = (hx + half_c, hy)
    proj_x = a_pt[0] + (a_len * a_len) / c_len
    alt_h = (a_len * b_len) / c_len
    c_pt = (proj_x, hy - alt_h)

    # Central right triangle
    mb.add_line("golden", a_pt[0], a_pt[1], b_pt[0], b_pt[1])
    mb.add_line("golden", b_pt[0], b_pt[1], c_pt[0], c_pt[1])
    mb.add_line("golden", c_pt[0], c_pt[1], a_pt[0], a_pt[1])

    # Hypotenuse exterior square (hanging below A-B)
    a_bot = (a_pt[0], hy + c_len)
    b_bot = (b_pt[0], hy + c_len)
    mb.add_line("golden", a_pt[0], a_pt[1], a_bot[0], a_bot[1])
    mb.add_line("golden", b_pt[0], b_pt[1], b_bot[0], b_bot[1])
    mb.add_line("golden", a_bot[0], a_bot[1], b_bot[0], b_bot[1])

    # Euclid's altitude line from C splitting the hypotenuse square into a^2 & b^2 rectangles
    mb.add_line("golden", c_pt[0], c_pt[1], c_pt[0], hy + c_len)

    # Left leg exterior square on A-C (outward normal rotated 90 deg CCW of A->C)
    dx_ac = c_pt[0] - a_pt[0]
    dy_ac = c_pt[1] - a_pt[1]
    nx_ac, ny_ac = dy_ac, -dx_ac
    a_ext = (a_pt[0] + nx_ac, a_pt[1] + ny_ac)
    c_ext_l = (c_pt[0] + nx_ac, c_pt[1] + ny_ac)
    mb.add_line("golden", a_pt[0], a_pt[1], a_ext[0], a_ext[1])
    mb.add_line("golden", c_pt[0], c_pt[1], c_ext_l[0], c_ext_l[1])
    mb.add_line("golden", a_ext[0], a_ext[1], c_ext_l[0], c_ext_l[1])

    # Right leg exterior square on B-C (outward normal rotated 90 deg CW of B->C)
    dx_bc = c_pt[0] - b_pt[0]
    dy_bc = c_pt[1] - b_pt[1]
    nx_bc, ny_bc = -dy_bc, dx_bc
    b_ext = (b_pt[0] + nx_bc, b_pt[1] + ny_bc)
    c_ext_r = (c_pt[0] + nx_bc, c_pt[1] + ny_bc)
    mb.add_line("golden", b_pt[0], b_pt[1], b_ext[0], b_ext[1])
    mb.add_line("golden", c_pt[0], c_pt[1], c_ext_r[0], c_ext_r[1])
    mb.add_line("golden", b_ext[0], b_ext[1], c_ext_r[0], c_ext_r[1])

    for vx, vy in (a_pt, b_pt, c_pt):
        mb.add_circle("golden", vx, vy, 0.9, filled=True)


def _add_visual_proof_triad_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.6,
) -> None:
    """Draw Byrne's Visual-Proof Triad (nested circle, square, and equilateral triangle)."""
    # Outer circumcircle & inner incircle of the equilateral triangle
    mb.add_circle("golden", cx, cy, radius)
    mb.add_circle("golden", cx, cy, 0.5 * radius)
    mb.add_circle("golden", cx, cy, 1.05, filled=True)

    # Inscribed upright square (vertices at 45, 135, 225, 315 deg)
    sq_pts = [polar(cx, cy, radius, 45.0 + 90.0 * k) for k in range(4)]
    for k in range(4):
        p1 = sq_pts[k]
        p2 = sq_pts[(k + 1) % 4]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Inscribed equilateral triangle (apex at -90 deg, tangent to inner circle)
    tri_pts = [polar(cx, cy, radius, -90.0 + 120.0 * k) for k in range(3)]
    for k in range(3):
        p1 = tri_pts[k]
        p2 = tri_pts[(k + 1) % 3]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
        mb.add_circle("golden", p1[0], p1[1], 0.95)


def build_byrne_elements(wave_angle_deg: float = 34.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Oliver Byrne medallion strictly from lines, circles, and circular arcs.

    Calibrated to the historic c. 1850 Victorian Romantic portrait of Oliver Byrne,
    featuring his high domed forehead, visionary upward-gazing eyes, flared billowing
    curly side-wings, clean-shaven jaw with Victorian sideburns, upturned white wing
    collar, knotted dark cravat over ruffled shirtfront, and tailored coat lapels.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc Romantic side-curls.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    _ = math.pi
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-12.2,
        eye_rx=5.4,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Euclid I.47 Windmill (Left) & Visual-Proof Triad (Right)
    # -------------------------------------------------------------------------
    _add_pythagorean_windmill_motif(mb, hx=-62.5, hy=-24.5, scale=2.65)
    _add_visual_proof_triad_motif(mb, cx=68.0, cy=-26.0, radius=12.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: High Domed Forehead, Visionary Upward Gaze, Nose & Mouth
    # -------------------------------------------------------------------------
    # High smooth domed Victorian cranium (single pure Euclidean circular arc!)
    mb.add_arc_pts("primary", (-17.5, -42.0), (24.0, -39.5), 12.6)

    # Left facial profile contour (temple -> cheek -> refined clean-shaven chin)
    mb.add_arc_pts("primary", (-17.5, -42.0), (-18.5, -31.5), -0.9)
    mb.add_arc_pts("primary", (-18.5, -31.5), (-19.5, -21.5), -1.0)
    mb.add_arc_pts("primary", (-19.5, -21.5), (-18.2, -9.5), -1.2)
    mb.add_arc_pts("primary", (-18.2, -9.5), (-13.5, 1.5), -1.6)
    mb.add_arc_pts("primary", (-13.5, 1.5), (-3.0, 8.2), -2.2)

    # Firm sculpted chin & right jawline sweeping toward sculpted ear
    mb.add_arc_pts("primary", (-3.0, 8.2), (9.5, 5.5), -1.6)
    mb.add_arc_pts("primary", (9.5, 5.5), (19.5, -2.5), -1.6)
    mb.add_arc_pts("primary", (19.5, -2.5), (24.5, -14.5), -1.4)
    mb.add_arc_pts("primary", (24.5, -14.5), (25.2, -28.0), -1.0)

    # Subtle Victorian sideburn contour hugging the right cheek/jaw (detail)
    mb.add_arc_pts("detail", (22.5, -33.5), (20.0, -15.5), 1.4)
    mb.add_arc_pts("detail", (20.0, -15.5), (12.0, 2.0), 1.6)
    mb.add_wave("detail", (22.2, -26.5), (15.5, -1.5), 4, wave_angle_deg * 0.75, 1)

    # Sculpted right ear peeking behind sideburn & curls
    mb.add_arc_pts("primary", (24.8, -17.5), (30.2, -16.5), 1.6)
    mb.add_arc_pts("primary", (30.2, -16.5), (28.5, -8.0), 1.5)
    mb.add_arc_pts("primary", (28.5, -8.0), (23.2, -5.5), 1.2)
    mb.add_arc_pts("detail", (25.5, -15.0), (27.4, -9.8), 1.1)

    # Lifted, inspired Romantic eyebrows
    mb.add_arc_pts("primary", (-17.8, -32.2), (-12.2, -35.2), 1.2)
    mb.add_arc_pts("primary", (-12.2, -35.2), (-5.8, -32.0), 1.1)
    mb.add_arc_pts("detail", (-17.0, -33.6), (-6.8, -33.2), 1.3)

    mb.add_arc_pts("primary", (-0.2, -32.0), (6.8, -34.0), 1.4)
    mb.add_arc_pts("primary", (6.8, -34.0), (15.2, -29.8), 1.2)
    mb.add_arc_pts("detail", (0.8, -33.4), (14.4, -31.2), 1.5)

    # Visionary upward-gazing eyes (irises & pupils tucked cleanly under upper lids!)
    # Viewer's left eye
    l_out = (-16.6, -28.0)
    l_in = (-7.2, -26.8)
    mb.add_arc_pts("primary", l_out, l_in, 2.3)
    mb.add_arc_pts("detail", (-16.8, -30.5), (-7.0, -29.4), 2.2)
    mb.add_arc_pts("detail", l_out, l_in, -1.6)
    # Upward-lifted iris & pupil (leaving open sclera below for unmistakable upward gaze)
    mb.add_arc("detail", -12.2, -28.4, 1.9, -15.0, 195.0)
    mb.add_circle("primary", -12.3, -28.6, 0.95, filled=True)
    mb.add_arc_pts("detail", (-16.0, -24.6), (-7.8, -23.8), -1.0)

    # Viewer's right eye
    r_in = (0.2, -26.2)
    r_out = (12.2, -24.5)
    mb.add_arc_pts("primary", r_in, r_out, 2.6)
    mb.add_arc_pts("detail", (-0.4, -29.0), (12.8, -27.2), 2.5)
    mb.add_arc_pts("detail", r_in, r_out, -1.9)
    # Upward-lifted iris & pupil
    mb.add_arc("detail", 5.6, -26.5, 2.1, -15.0, 195.0)
    mb.add_circle("primary", 5.3, -26.7, 1.05, filled=True)
    mb.add_arc_pts("detail", (0.8, -21.8), (11.8, -20.8), -1.3)

    # Refined straight Victorian nose
    mb.add_arc_pts("primary", (-4.8, -31.2), (-12.0, -14.5), -0.6)
    mb.add_arc_pts("detail", (-2.2, -25.0), (-4.6, -16.8), -0.45)
    mb.add_arc_pts("primary", (-12.0, -14.5), (-8.4, -12.2), -1.0)
    mb.add_arc_pts("primary", (-8.4, -12.2), (-3.8, -12.5), -0.65)
    mb.add_arc_pts("primary", (-3.8, -12.5), (-0.8, -14.8), -0.8)
    mb.add_arc_pts("detail", (-0.8, -14.8), (-1.8, -17.5), -0.55)
    mb.add_arc_pts("detail", (-8.8, -13.6), (-4.5, -13.8), 0.45)

    # Expressive, composed Romantic mouth & sculpted chin
    mb.add_arc_pts("detail", (-7.6, -11.4), (-8.0, -7.8), 0.3)
    mb.add_arc_pts("detail", (-12.6, -6.4), (-8.0, -7.4), 0.65)
    mb.add_arc_pts("detail", (-8.0, -7.4), (-1.2, -5.0), 0.7)
    mb.add_arc_pts("primary", (-13.0, -5.8), (-7.4, -5.2), 0.45)
    mb.add_arc_pts("primary", (-7.4, -5.2), (-0.8, -4.6), -0.4)
    mb.add_arc_pts("detail", (-11.6, -3.5), (-7.0, -2.4), -0.8)
    mb.add_arc_pts("detail", (-7.0, -2.4), (-2.4, -3.2), -0.5)
    mb.add_arc_pts("detail", (-10.2, 1.0), (-5.0, 1.4), -0.7)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Signature Billowing Flared Side-Curls (Euclid III.12)
    # -------------------------------------------------------------------------
    # Left flared curly side-wing (negative sagittas puff curls OUTWARD!)
    mb.add_arc_pts("primary", (-13.5, -49.0), (-25.5, -45.5), -2.2)
    mb.add_arc_pts("primary", (-25.5, -45.5), (-31.5, -35.5), -2.6)
    mb.add_arc_pts("primary", (-31.5, -35.5), (-28.5, -24.5), -2.2)
    mb.add_arc_pts("primary", (-28.5, -24.5), (-23.8, -14.5), -1.8)
    mb.add_arc_pts("primary", (-23.8, -14.5), (-18.5, -9.5), -1.4)
    mb.add_wave("detail", (-26.5, -41.5), (-21.5, -17.5), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (-21.8, -44.0), (-19.8, -26.0), 3, wave_angle_deg * 0.85, -1)

    # Right billowing Romantic curly side-wing (iconic Byrne silhouette!)
    mb.add_arc_pts("primary", (17.2, -48.5), (32.5, -46.8), 2.4)
    mb.add_arc_pts("primary", (32.5, -46.8), (42.8, -40.0), 2.8)
    mb.add_arc_pts("primary", (42.8, -40.0), (45.8, -29.0), 2.8)
    mb.add_arc_pts("primary", (45.8, -29.0), (41.2, -17.5), 2.6)
    mb.add_arc_pts("primary", (41.2, -17.5), (33.5, -8.5), 2.2)
    mb.add_arc_pts("primary", (33.5, -8.5), (24.5, -4.5), 1.6)
    # Lush curly interior waves inside right wing
    mb.add_wave("detail", (23.5, -44.5), (40.5, -28.0), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (28.0, -45.0), (41.5, -21.5), 4, wave_angle_deg, -1)
    mb.add_wave("detail", (25.5, -36.5), (36.0, -12.0), 4, wave_angle_deg * 0.9, 1)
    mb.add_wave("detail", (26.5, -25.5), (31.5, -10.5), 3, wave_angle_deg * 0.8, -1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Upturned Wing Collar, Knotted Cravat & Victorian Frock Coat
    # -------------------------------------------------------------------------
    # Upturned white Victorian wing-collar points hugging jaw & throat
    mb.add_arc_pts("primary", (-16.8, 3.5), (-13.5, 13.5), 1.2)
    mb.add_line("primary", -13.5, 13.5, -4.5, 16.5)
    mb.add_arc_pts("primary", (19.5, -0.5), (19.5, 11.5), -1.2)
    mb.add_line("primary", 19.5, 11.5, 8.2, 16.5)

    # Broad knotted dark Romantic cravat & cascading bow tails (cleanly inside shirtfront!)
    mb.add_arc_pts("primary", (-15.5, 14.5), (1.0, 18.8), -1.6)
    mb.add_arc_pts("primary", (1.0, 18.8), (20.2, 12.2), -1.8)
    # Central cravat knot
    mb.add_arc_pts("primary", (-8.2, 18.5), (-7.2, 31.0), -1.2)
    mb.add_arc_pts("primary", (8.2, 18.0), (8.6, 30.8), 1.2)
    mb.add_arc_pts("primary", (-7.2, 31.0), (8.6, 30.8), -1.4)
    # Left cravat bow wing
    mb.add_arc_pts("primary", (-8.2, 20.5), (-16.5, 33.0), -1.4)
    mb.add_arc_pts("primary", (-16.5, 33.0), (-9.8, 42.2), -1.3)
    mb.add_arc_pts("primary", (-9.8, 42.2), (-5.2, 31.2), -0.9)
    # Right cascading cravat ribbon tail (tucked cleanly inside right shirtfront edge)
    mb.add_arc_pts("primary", (8.0, 26.5), (12.8, 45.0), 1.6)
    mb.add_arc_pts("primary", (12.8, 45.0), (9.8, 54.5), 1.1)
    mb.add_arc_pts("primary", (9.8, 54.5), (3.2, 43.5), 1.2)
    mb.add_arc_pts("primary", (3.2, 43.5), (1.2, 31.2), 0.8)
    # Cravat silk creases
    mb.add_arc_pts("detail", (-4.5, 21.5), (5.0, 22.5), -0.9)
    mb.add_arc_pts("detail", (-3.5, 26.0), (5.5, 26.8), -0.8)
    mb.add_arc_pts("detail", (5.5, 31.8), (9.2, 48.0), 1.0)

    # White ruffled Victorian shirtfront V-opening descending to medallion bottom
    mb.add_arc_pts("primary", (-15.5, 38.5), (-11.5, 86.0), 2.4)
    mb.add_arc_pts("primary", (16.5, 32.5), (12.0, 86.0), -2.4)
    # Crisp soft linen folds on bright shirtfront
    mb.add_arc_pts("detail", (-6.5, 39.5), (-5.5, 85.0), 1.4)
    mb.add_arc_pts("detail", (0.5, 36.5), (0.8, 86.0), -1.2)
    mb.add_arc_pts("detail", (6.5, 53.0), (6.5, 85.0), -1.0)

    # Tailored Victorian coat collar & crisp lapels connecting cleanly to shirtfront
    # Left coat collar & tailored lapel
    mb.add_arc_pts("primary", (-19.5, 5.5), (-35.0, 16.5), -1.6)
    mb.add_line("primary", -35.0, 16.5, -39.5, 37.5)
    mb.add_arc_pts("primary", (-39.5, 37.5), (-14.2, 56.5), -1.4)
    # Right coat collar & tailored lapel
    mb.add_arc_pts("primary", (24.5, 2.5), (37.5, 14.5), 1.6)
    mb.add_line("primary", 37.5, 14.5, 39.5, 36.5)
    mb.add_arc_pts("primary", (39.5, 36.5), (15.0, 56.0), 1.4)

    # Broad sweeping Victorian coat shoulders & sleeves clipped cleanly to MED_R
    mb.add_arc_pts("primary", (-35.0, 16.5), (-74.0, 38.0), -4.0)
    mb.add_arc_pts("primary", (-74.0, 38.0), (-78.0, 74.0), -2.6)
    mb.add_arc_pts("primary", (37.5, 14.5), (78.5, 64.0), 5.6)

    # Parallel non-crossing coat & sleeve folds (detail)
    mb.add_arc_pts("detail", (-49.0, 26.5), (-58.5, 74.0), -2.6)
    mb.add_arc_pts("detail", (-32.5, 48.0), (-34.5, 83.0), -1.8)
    mb.add_arc_pts("detail", (46.5, 28.0), (59.5, 73.5), 2.8)
    mb.add_arc_pts("detail", (31.5, 48.0), (35.5, 83.0), 1.8)

    return mb.build()


def build_byrne_svg(theme: str = "dark", wave_angle_deg: float = 34.0) -> str:
    """Render the Oliver Byrne medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_byrne_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_byrne_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 34.0,
) -> tuple[Path, Path]:
    """Write ``byrne_dark.svg`` and ``byrne_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "byrne_dark.svg"
    light_path = target_dir / "byrne_light.svg"
    dark_path.write_text(
        build_byrne_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_byrne_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
