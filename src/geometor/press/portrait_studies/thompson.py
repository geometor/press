"""Study 23: Sir D'Arcy Wentworth Thompson (after Robertson, Dundee, 1886)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_thompson_elements",
    "build_thompson_svg",
    "write_thompson_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"
PHI = (1.0 + math.sqrt(5.0)) / 2.0


def _add_nautilus_gnomon_spiral_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw D'Arcy Thompson's *On Growth and Form* Nautilus logarithmic gnomon spiral.

    Constructs an exact G1-continuous chain of eight ``90 deg`` circular arcs
    whose radii scale by ``sqrt(phi)`` per quarter-turn (exact golden ratio
    ``phi`` per half-turn), paired with radial gnomon rays and curved Nautilus
    chamber septa connecting successive whorls.
    """
    q = math.sqrt(PHI)
    r0 = 2.15
    # Generate 8 exact G1-tangent quarter-circle arcs (2 full revolutions)
    arcs: list[tuple[float, float, float, float, float]] = []
    cur_cx, cur_cy = 0.0, 0.0
    r = r0
    for k in range(8):
        a1 = 90.0 * k
        a2 = 90.0 * (k + 1)
        arcs.append((cur_cx, cur_cy, r, a1, a2))
        r_next = r * q
        end_rad = math.radians(a2)
        # Shift center along the endpoint normal so next arc is strictly G1-tangent
        cur_cx -= (r_next - r) * math.cos(end_rad)
        cur_cy -= (r_next - r) * math.sin(end_rad)
        r = r_next

    # Center the spiral bounding box neatly on (cx, cy)
    xs: list[float] = []
    ys: list[float] = []
    for acx, acy, ar, a1, a2 in arcs:
        for t in (0.0, 0.5, 1.0):
            rad = math.radians(a1 + t * (a2 - a1))
            xs.append(acx + ar * math.cos(rad))
            ys.append(acy + ar * math.sin(rad))
    off_x = cx - 0.5 * (min(xs) + max(xs))
    off_y = cy - 0.5 * (min(ys) + max(ys))

    shifted = [(acx + off_x, acy + off_y, ar, a1, a2) for acx, acy, ar, a1, a2 in arcs]
    for acx, acy, ar, a1, a2 in shifted:
        mb.add_arc("golden", acx, acy, ar, a1, a2)

    # Approximate asymptotic spiral pole inside the innermost whorl
    pole_x, pole_y = shifted[0][0], shifted[0][1]
    mb.add_circle("golden", pole_x, pole_y, 0.88, filled=True)

    # Radial gnomon rays and curved Nautilus chamber septa across the outer whorl
    for k in range(4, 8):
        inner = shifted[k - 4]
        outer = shifted[k]
        for frac in (0.0, 0.5):
            ang_in = math.radians(inner[3] + frac * (inner[4] - inner[3]))
            ang_out = math.radians(outer[3] + frac * (outer[4] - outer[3]))
            p_in = (
                inner[0] + inner[2] * math.cos(ang_in),
                inner[1] + inner[2] * math.sin(ang_in),
            )
            p_out = (
                outer[0] + outer[2] * math.cos(ang_out),
                outer[1] + outer[2] * math.sin(ang_out),
            )
            chord = math.hypot(p_out[0] - p_in[0], p_out[1] - p_in[1])
            mb.add_arc_pts("golden", p_in, p_out, -0.18 * chord)
            if frac == 0.0:
                mb.add_circle("golden", p_out[0], p_out[1], 0.65)

    # Closing radial mouth aperture from innermost pole to outer spiral tip
    last = shifted[-1]
    end_rad = math.radians(last[4])
    tip_x = last[0] + last[2] * math.cos(end_rad)
    tip_y = last[1] + last[2] * math.sin(end_rad)
    mb.add_line("golden", pole_x, pole_y, tip_x, tip_y)
    mb.add_circle("golden", tip_x, tip_y, 0.82, filled=True)


def _add_transformation_grid_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw D'Arcy Thompson's Chapter XVII Cartesian-to-polar transformation mesh.

    Constructs four concentric circular coordinate arcs crossed by five
    equally spaced radial rays converging toward a marked transformation pole.
    """
    pole_x = cx - 15.2
    pole_y = cy
    radii = (8.8, 13.8, 18.8, 23.8)
    angles_deg = (-36.0, -18.0, 0.0, 18.0, 36.0)

    # Four concentric transformed circular arcs
    for r in radii:
        mb.add_arc("golden", pole_x, pole_y, r, angles_deg[0], angles_deg[-1])

    # Five radial coordinate rays spanning the polar grid
    r_min, r_max = radii[0], radii[-1]
    for ang in angles_deg:
        rad = math.radians(ang)
        x1 = pole_x + r_min * math.cos(rad)
        y1 = pole_y + r_min * math.sin(rad)
        x2 = pole_x + r_max * math.cos(rad)
        y2 = pole_y + r_max * math.sin(rad)
        mb.add_line("golden", x1, y1, x2, y2)

    # Projection rays from transformation pole to inner corners
    for ang in (angles_deg[0], angles_deg[-1]):
        rad = math.radians(ang)
        mb.add_line(
            "golden",
            pole_x,
            pole_y,
            pole_x + r_min * math.cos(rad),
            pole_y + r_min * math.sin(rad),
        )

    # Mark transformation pole & central horizontal coordinate axis nodes
    mb.add_circle("golden", pole_x, pole_y, 0.95, filled=True)
    for r in radii:
        mb.add_circle("golden", pole_x + r, pole_y, 0.65)


def build_thompson_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the four-layer compass-and-straightedge geometry for D'Arcy Thompson.

    Uses ``MedallionBuilder`` so every line and circular arc is clipped cleanly
    within ``MED_R = 92.0`` with zero Bezier curves.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1 (Scaffold): Canonical medallion ring, eye line & golden circles
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-10.0,
        eye_rx=11.0,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Nautilus Gnomon Spiral (Left) & Polar Grid (Right)
    # -------------------------------------------------------------------------
    _add_nautilus_gnomon_spiral_motif(mb, cx=-63.5, cy=-26.0)
    _add_transformation_grid_motif(mb, cx=64.0, cy=-26.0)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Sweeping Parted Victorian Hair Wave, Sideburns & Ears
    # -------------------------------------------------------------------------
    # Sculpted parted hair crown silhouette (sweeping left wave + right curl)
    mb.add_arc_pts("primary", (-23.8, -31.0), (-27.8, -44.5), 2.2)
    mb.add_arc_pts("primary", (-27.8, -44.5), (-18.5, -60.5), 3.0)
    mb.add_arc_pts("primary", (-18.5, -60.5), (6.5, -60.0), 5.2)
    mb.add_arc_pts("primary", (6.5, -60.0), (24.5, -54.5), 3.2)
    mb.add_arc_pts("primary", (24.5, -54.5), (28.5, -38.5), 2.8)
    mb.add_arc_pts("primary", (28.5, -38.5), (25.0, -30.0), 1.4)

    # Flowing forehead hairline parting slightly right of center
    mb.add_arc_pts("detail", (-21.8, -36.5), (-18.8, -47.5), 1.4)
    mb.add_arc_pts("detail", (-18.8, -47.5), (6.2, -49.5), 3.4)
    mb.add_arc_pts("detail", (6.2, -49.5), (22.5, -44.0), 2.6)
    mb.add_arc_pts("detail", (22.5, -44.0), (23.2, -33.0), 1.0)
    mb.add_arc_pts("detail", (6.2, -49.5), (6.5, -60.0), -0.9)

    # Sculpted parted hair wave strokes (Euclid III.12)
    mb.add_wave("detail", (5.5, -55.0), (-21.5, -51.5), 4, wave_angle_deg * 0.62, 1)
    mb.add_wave("detail", (4.5, -59.0), (-18.5, -57.5), 3, wave_angle_deg * 0.58, -1)
    mb.add_wave("detail", (7.5, -54.8), (24.8, -47.5), 3, wave_angle_deg * 0.6, -1)
    mb.add_wave("detail", (-24.8, -47.0), (-23.2, -31.5), 2, wave_angle_deg * 0.5, 1)
    mb.add_wave("detail", (26.2, -45.5), (24.8, -31.0), 2, wave_angle_deg * 0.5, -1)

    # Smooth convex tucked frontal ears & tapered Victorian sideburns
    mb.add_arc_pts("primary", (-22.6, -30.5), (-25.8, -23.0), -1.4)
    mb.add_arc_pts("primary", (-25.8, -23.0), (-22.8, -15.5), -1.4)
    mb.add_arc_pts("primary", (-22.8, -15.5), (-20.4, -16.8), -0.7)
    mb.add_arc_pts("detail", (-22.0, -32.0), (-19.8, -16.5), -0.8)

    mb.add_arc_pts("primary", (23.8, -30.0), (26.8, -22.5), 1.4)
    mb.add_arc_pts("primary", (26.8, -22.5), (23.8, -15.5), 1.4)
    mb.add_arc_pts("primary", (23.8, -15.5), (21.5, -16.8), 0.7)
    mb.add_arc_pts("detail", (23.0, -32.0), (20.8, -16.5), 0.8)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Bilateral Frontal Face, Penetrating Eyes, Nose & Mustache
    # -------------------------------------------------------------------------
    # Clean symmetrical frontal cheek, jawline & strong rounded chin
    mb.add_arc_pts("primary", (-21.8, -36.5), (-22.2, -25.0), -0.8)
    mb.add_arc_pts("primary", (-22.2, -25.0), (-20.2, -13.5), -0.9)
    mb.add_arc_pts("primary", (-20.2, -13.5), (-17.8, -2.5), -1.0)
    mb.add_arc_pts("primary", (-17.8, -2.5), (-11.8, 6.2), -1.4)
    mb.add_arc_pts("primary", (-11.8, 6.2), (0.8, 11.2), -1.8)

    mb.add_arc_pts("primary", (0.8, 11.2), (13.2, 5.8), -1.8)
    mb.add_arc_pts("primary", (13.2, 5.8), (19.2, -3.5), -1.4)
    mb.add_arc_pts("primary", (19.2, -3.5), (21.5, -14.5), -1.0)
    mb.add_arc_pts("primary", (21.5, -14.5), (23.2, -26.0), -0.9)
    mb.add_arc_pts("primary", (23.2, -26.0), (22.5, -44.0), -0.8)

    # Subtle straight Scottish eyebrows
    mb.add_arc_pts("primary", (-19.2, -30.5), (-10.5, -32.2), 0.9)
    mb.add_arc_pts("primary", (-10.5, -32.2), (-2.8, -30.2), 0.8)
    mb.add_arc_pts("detail", (-18.4, -31.5), (-3.5, -31.2), 1.0)

    mb.add_arc_pts("primary", (4.0, -30.2), (11.8, -32.2), 0.8)
    mb.add_arc_pts("primary", (11.8, -32.2), (20.2, -30.5), 0.9)
    mb.add_arc_pts("detail", (4.8, -31.2), (19.2, -31.5), 1.0)

    # Bright clear penetrating frontal eyes right along y = -27
    # Viewer's left eye
    l_out = (-15.4, -26.8)
    l_in = (-4.8, -26.8)
    mb.add_arc_pts("primary", l_out, l_in, 1.95)
    mb.add_arc_pts("detail", (-15.8, -29.2), (-4.4, -29.2), 1.9)
    mb.add_arc_pts("detail", l_out, l_in, -1.3)
    mb.add_circle("detail", -10.0, -26.8, 2.05)
    mb.add_circle("primary", -10.0, -26.8, 0.96, filled=True)
    mb.add_arc_pts("detail", (-14.8, -23.4), (-5.2, -23.4), -1.0)

    # Viewer's right eye
    r_in = (5.8, -26.8)
    r_out = (16.4, -26.8)
    mb.add_arc_pts("primary", r_in, r_out, 1.95)
    mb.add_arc_pts("detail", (5.4, -29.2), (16.8, -29.2), 1.9)
    mb.add_arc_pts("detail", r_in, r_out, -1.3)
    mb.add_circle("detail", 11.0, -26.8, 2.05)
    mb.add_circle("primary", 11.0, -26.8, 0.96, filled=True)
    mb.add_arc_pts("detail", (6.2, -23.4), (15.8, -23.4), -1.0)

    # Classic straight frontal nose
    mb.add_arc_pts("detail", (-2.2, -26.5), (-3.0, -17.0), 0.35)
    mb.add_arc_pts("detail", (3.2, -26.5), (4.0, -17.0), -0.35)
    mb.add_arc_pts("primary", (-5.5, -15.2), (-6.0, -12.6), -0.65)
    mb.add_arc_pts("primary", (-6.0, -12.6), (-2.8, -11.6), -0.55)
    mb.add_arc_pts("primary", (-2.8, -11.6), (0.8, -11.2), -0.45)
    mb.add_arc_pts("primary", (0.8, -11.2), (4.5, -11.6), -0.45)
    mb.add_arc_pts("primary", (4.5, -11.6), (7.2, -12.8), -0.55)
    mb.add_arc_pts("primary", (7.2, -12.8), (6.5, -15.2), -0.65)
    mb.add_arc_pts("detail", (-4.4, -12.8), (-1.8, -12.6), 0.35)
    mb.add_arc_pts("detail", (2.8, -12.6), (5.4, -12.8), 0.35)

    # Lush drooping Victorian walrus mustache framing the mouth & chin
    mb.add_arc_pts("primary", (0.8, -9.2), (-14.2, -2.5), -2.4)
    mb.add_arc_pts("primary", (-14.2, -2.5), (-14.2, 2.4), -1.2)
    mb.add_arc_pts("primary", (-14.2, 2.4), (-9.8, 2.8), -0.8)
    mb.add_arc_pts("primary", (-9.8, 2.8), (-5.8, -1.8), -0.9)
    mb.add_arc_pts("primary", (-5.8, -1.8), (0.8, -3.0), 0.6)

    mb.add_arc_pts("primary", (0.8, -9.2), (15.2, -2.5), 2.4)
    mb.add_arc_pts("primary", (15.2, -2.5), (15.0, 2.2), 1.2)
    mb.add_arc_pts("primary", (15.0, 2.2), (10.8, 2.6), 0.8)
    mb.add_arc_pts("primary", (10.8, 2.6), (7.0, -1.8), 0.9)
    mb.add_arc_pts("primary", (7.0, -1.8), (0.8, -3.0), -0.6)

    # Flowing walrus mustache texture waves
    mb.add_wave("detail", (-0.5, -7.2), (-12.5, 0.2), 3, wave_angle_deg * 0.5, 1)
    mb.add_wave("detail", (-1.5, -5.0), (-9.8, 1.4), 2, wave_angle_deg * 0.45, -1)
    mb.add_wave("detail", (2.0, -7.2), (13.4, 0.2), 3, wave_angle_deg * 0.5, -1)
    mb.add_wave("detail", (3.0, -5.0), (10.6, 1.2), 2, wave_angle_deg * 0.45, 1)

    # Subtle lower lip & strong chin dimple beneath mustache
    mb.add_arc_pts("detail", (-4.6, -1.0), (0.8, -0.2), -0.75)
    mb.add_arc_pts("detail", (0.8, -0.2), (6.0, -1.0), -0.65)
    mb.add_arc_pts("detail", (-3.5, 3.2), (4.8, 3.2), -0.55)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Crisp Wing Collar, Broad Tie, Waistcoat & Tweed Jacket
    # -------------------------------------------------------------------------
    # Neck & crisp upturned Scottish Victorian white wing collar
    mb.add_arc_pts("primary", (-16.2, 0.5), (-18.2, 6.8), -0.5)
    mb.add_arc_pts("primary", (17.2, 1.0), (18.8, 7.2), 0.5)
    # Left wing flap
    mb.add_arc_pts("primary", (-18.2, 6.8), (-6.8, 14.8), -1.2)
    mb.add_line("primary", -6.8, 14.8, -7.8, 19.8)
    mb.add_line("primary", -7.8, 19.8, 4.5, 19.8)
    mb.add_line("primary", -6.8, 14.8, 5.2, 20.4)
    # Right wing flap
    mb.add_arc_pts("primary", (18.8, 7.2), (17.2, 12.2), 0.5)
    mb.add_line("primary", 17.2, 12.2, 22.5, 17.8)
    mb.add_line("primary", 22.5, 17.8, 9.8, 19.2)
    mb.add_line("primary", 17.2, 12.2, 5.2, 20.4)

    # Broad knotted Victorian tie / cravat
    mb.add_arc_pts("primary", (0.2, 22.2), (13.2, 21.2), -0.7)
    mb.add_arc_pts("primary", (13.2, 21.2), (15.6, 35.5), 1.2)
    mb.add_arc_pts("primary", (15.6, 35.5), (7.6, 36.2), 0.6)
    mb.add_arc_pts("primary", (7.6, 36.2), (0.2, 22.2), 1.0)
    # Lower tie blade tucking neatly into waistcoat V
    mb.add_line("primary", 7.6, 36.2, 12.4, 47.0)
    mb.add_line("primary", 15.6, 35.5, 17.2, 41.2)
    mb.add_line("detail", 4.0, 24.0, 10.8, 34.5)
    mb.add_arc_pts("detail", (-4.5, 22.5), (1.8, 25.0), -0.7)

    # Buttoned Scottish tweed waistcoat V-opening & center buttoned placket
    mb.add_arc_pts("primary", (-10.8, 21.8), (12.4, 48.2), 1.6)
    mb.add_arc_pts("primary", (20.2, 20.2), (24.2, 41.2), 1.2)
    mb.add_line("primary", 24.2, 41.2, 12.4, 48.2)
    mb.add_arc_pts("primary", (12.4, 48.2), (15.2, 88.0), 1.0)
    # Two waistcoat buttons along placket & two jacket buttons on left front
    for bx, by in ((15.2, 52.8), (16.8, 70.2)):
        mb.add_circle("primary", bx, by, 1.9)
        mb.add_circle("detail", bx, by, 0.75)
    for bx, by in ((1.6, 58.2), (2.2, 81.2)):
        mb.add_circle("primary", bx, by, 2.0)
        mb.add_circle("detail", bx, by, 0.8)

    # Broad tweed jacket shoulders matching Dundee portrait slope, clipped to MED_R
    mb.add_arc_pts("primary", (-18.2, 6.8), (-54.5, 28.5), -3.0)
    mb.add_arc_pts("primary", (-54.5, 28.5), (-68.5, 76.0), -4.5)
    mb.add_arc_pts("primary", (18.8, 10.8), (52.5, 27.5), 2.8)
    mb.add_arc_pts("primary", (52.5, 27.5), (67.5, 74.0), 4.2)

    # Crisp notched Scottish tweed jacket lapels
    # Viewer's left lapel
    mb.add_arc_pts("primary", (-18.2, 6.8), (-27.0, 26.8), -1.2)
    mb.add_line("primary", -27.0, 26.8, -19.8, 29.2)
    mb.add_line("primary", -19.8, 29.2, -26.8, 35.0)
    mb.add_arc_pts("primary", (-26.8, 35.0), (4.2, 51.8), -2.4)
    mb.add_arc_pts("primary", (4.2, 51.8), (5.8, 88.0), -0.8)
    mb.add_arc_pts("detail", (-19.2, 30.0), (2.5, 49.5), -1.4)

    # Viewer's right lapel
    mb.add_arc_pts("primary", (18.8, 10.8), (35.2, 24.5), 1.4)
    mb.add_line("primary", 35.2, 24.5, 28.5, 26.5)
    mb.add_line("primary", 28.5, 26.5, 36.2, 32.5)
    mb.add_arc_pts("primary", (36.2, 32.5), (34.8, 57.5), 1.8)
    mb.add_arc_pts("primary", (34.8, 57.5), (36.8, 86.0), 1.2)
    mb.add_arc_pts("detail", (28.0, 27.5), (27.5, 56.5), 1.2)

    # Tweed jacket sleeve & pocket handkerchief detail clipped to MED_R
    mb.add_arc_pts("detail", (-48.5, 34.0), (-56.5, 80.0), -2.5)
    mb.add_arc_pts("detail", (-36.5, 40.0), (-34.5, 86.0), -1.8)
    mb.add_arc_pts("detail", (-16.5, 52.0), (-14.5, 87.5), -1.2)
    mb.add_arc_pts("detail", (45.5, 30.0), (57.5, 76.0), 2.5)
    mb.add_arc_pts("detail", (45.2, 56.5), (53.2, 62.5), 1.4)
    mb.add_arc_pts("detail", (53.2, 62.5), (49.2, 68.5), 1.0)

    return mb.build()


def build_thompson_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Sir D'Arcy Wentworth Thompson medallion SVG for ``'dark'`` or ``'light'``."""
    layers = build_thompson_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_thompson_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``thompson_dark.svg`` and ``thompson_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "thompson_dark.svg"
    light_path = target_dir / "thompson_light.svg"
    dark_path.write_text(
        build_thompson_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_thompson_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
