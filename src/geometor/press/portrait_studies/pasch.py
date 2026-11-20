"""Study 36: Moritz Pasch (after the Giessen G. Backofen cabinet portrait)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_pasch_elements",
    "build_pasch_svg",
    "write_pasch_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_paschs_axiom_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Pasch's Axiom Transversal (1882) in the open left margin.

    Constructs a triangle ``ABC`` and a transversal line ``l`` avoiding all
    three vertices, entering strictly across open segment ``AB`` at ``P`` and
    necessarily exiting strictly across open segment ``AC`` at ``Q``.
    """
    pt_a = (cx - 1.8, cy - 11.4)
    pt_b = (cx - 11.4, cy + 9.0)
    pt_c = (cx + 11.4, cy + 9.0)

    # Exact betweenness points P on open segment AB and Q on open segment AC
    t_p = 0.58
    t_q = 0.36
    pt_p = (
        pt_a[0] + t_p * (pt_b[0] - pt_a[0]),
        pt_a[1] + t_p * (pt_b[1] - pt_a[1]),
    )
    pt_q = (
        pt_a[0] + t_q * (pt_c[0] - pt_a[0]),
        pt_a[1] + t_q * (pt_c[1] - pt_a[1]),
    )

    # Triangle ABC
    mb.add_line("golden", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_a[0], pt_a[1])

    # Transversal line l extending strictly beyond P and Q
    dx, dy = pt_q[0] - pt_p[0], pt_q[1] - pt_p[1]
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    l_start = (pt_p[0] - 5.2 * ux, pt_p[1] - 5.2 * uy)
    l_end = (pt_q[0] + 6.4 * ux, pt_q[1] + 6.4 * uy)
    mb.add_line("golden", l_start[0], l_start[1], l_end[0], l_end[1])

    # Subtle directional arrowhead on transversal tip l_end
    nx, ny = -uy, ux
    mb.add_line(
        "golden",
        l_end[0],
        l_end[1],
        l_end[0] - 2.0 * ux + 1.1 * nx,
        l_end[1] - 2.0 * uy + 1.1 * ny,
    )
    mb.add_line(
        "golden",
        l_end[0],
        l_end[1],
        l_end[0] - 2.0 * ux - 1.1 * nx,
        l_end[1] - 2.0 * uy - 1.1 * ny,
    )

    # Open vertex rings at A, B, C (strictly avoided by transversal l)
    for vx, vy in (pt_a, pt_b, pt_c):
        mb.add_circle("golden", vx, vy, 0.86)

    # Highlighted entry/exit betweenness nodes P and Q on segments AB and AC
    for ix, iy in (pt_p, pt_q):
        mb.add_circle("golden", ix, iy, 0.85, filled=True)
        mb.add_circle("golden", ix, iy, 1.55)


def _add_order_betweenness_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Pasch's Axioms of Order / Betweenness Triad in the open right margin.

    Depicts a directed order line carrying four strictly ordered points
    ``A < B < C < D`` framed by nested semicircular separation arcs and
    half-plane separator ticks illustrating linear betweenness ``[A * B * C]``.
    """
    # Directed horizontal order line
    x_left, x_right = cx - 12.2, cx + 12.2
    mb.add_line("golden", x_left, cy, x_right, cy)
    mb.add_line("golden", x_right, cy, x_right - 2.1, cy - 1.2)
    mb.add_line("golden", x_right, cy, x_right - 2.1, cy + 1.2)

    # Four strictly ordered points A, B, C, D spaced evenly at step 6.0
    pt_a = (cx - 9.0, cy)
    pt_b = (cx - 3.0, cy)
    pt_c = (cx + 3.0, cy)
    pt_d = (cx + 9.0, cy)

    # Nested symmetric order & separation bracket arcs via exact chord endpoints
    # Upper arcs: [A..D] outer span & [A..C] betweenness triad [A * B * C]
    mb.add_arc_pts("golden", pt_a, pt_d, 8.8)
    mb.add_arc_pts("golden", pt_a, pt_c, 4.8)
    # Lower arcs: [B..D] betweenness triad [B * C * D] & [B..C] inner span
    mb.add_arc_pts("golden", pt_b, pt_d, -4.8)
    mb.add_arc_pts("golden", pt_b, pt_c, -2.5)

    # Subtle vertical half-plane separator ticks at interior points B and C
    mb.add_line("golden", pt_b[0], cy - 1.8, pt_b[0], cy + 1.8)
    mb.add_line("golden", pt_c[0], cy - 1.8, pt_c[0], cy + 1.8)

    # Open rings at outer bounds A, D and bold filled dots at interior nodes B, C
    for ox, oy in (pt_a, pt_d):
        mb.add_circle("golden", ox, oy, 0.88)
    for ix, iy in (pt_b, pt_c):
        mb.add_circle("golden", ix, iy, 0.88, filled=True)


def build_pasch_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Moritz Pasch.

    Calibrated to the Giessen G. Backofen cabinet portrait: smooth high domed
    forehead framed by neatly rounded wavy side and crown hair, direct calm
    eyes on ``y = -27`` framed by delicate thin pince-nez oval lenses with the
    iconic fine vertical pince-nez cord hanging gracefully straight down past
    his left cheek to the collar, straight nose, dense rounded full dark
    scholar's beard and mustache (``Euclid III.12`` tangent waves), crisp
    folded white collar with wide dark silk bow tie over a pale dress shirt,
    and tailored notched German academic jacket lapels grounded smoothly to
    ``MED_R = 92.0``. Margin motifs display Pasch's Axiom Transversal (left)
    and Axioms of Order / Betweenness Triad (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-9.2,
        eye_rx=9.4,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN PASCH AXIOMATIC MARGIN MOTIFS (zero face crossing) ---
    _add_paschs_axiom_motif(mb, cx=-63.5, cy=-26.0)
    _add_order_betweenness_motif(mb, cx=63.5, cy=-26.0)

    # --- HIGH DOMED FOREHEAD & NEATLY ROUNDED WAVY HAIR ---
    mb.add_arc_pts("primary", (-22.0, -27.5), (-26.8, -37.5), 1.5)
    mb.add_arc_pts("primary", (-26.8, -37.5), (-24.0, -49.2), 1.8)
    mb.add_arc_pts("primary", (-24.0, -49.2), (-15.0, -57.2), 1.9)
    mb.add_arc_pts("primary", (-15.0, -57.2), (0.5, -59.8), 2.2)
    mb.add_arc_pts("primary", (0.5, -59.8), (16.2, -57.2), 2.1)
    mb.add_arc_pts("primary", (16.2, -57.2), (24.5, -48.2), 1.8)
    mb.add_arc_pts("primary", (24.5, -48.2), (26.0, -36.5), 1.6)
    mb.add_arc_pts("primary", (26.0, -36.5), (22.5, -26.8), 1.1)

    # Smooth high domed forehead hairline
    mb.add_arc_pts("primary", (-20.2, -28.0), (-19.4, -40.2), 0.9)
    mb.add_arc_pts("primary", (-19.4, -40.2), (-13.5, -49.5), 1.3)
    mb.add_arc_pts("primary", (-13.5, -49.5), (0.5, -53.5), 1.7)
    mb.add_arc_pts("primary", (0.5, -53.5), (14.2, -49.2), 1.6)
    mb.add_arc_pts("primary", (14.2, -49.2), (20.0, -39.5), 1.2)
    mb.add_arc_pts("primary", (20.0, -39.5), (21.0, -27.0), 0.8)

    # Soft wavy hair texture strictly inside crown/sides via Euclid III.12 waves
    mb.add_wave("detail", (-23.8, -36.0), (-21.0, -48.5), 3, wave_angle_deg + 2.0, 1)
    mb.add_wave("detail", (-14.2, -55.8), (14.8, -55.8), 4, wave_angle_deg - 4.0, -1)
    mb.add_wave("detail", (21.5, -47.5), (23.8, -34.5), 3, wave_angle_deg + 2.0, -1)

    # --- BOTH EARS CLEARLY VISIBLE ---
    # Viewer-left ear
    mb.add_arc_pts("primary", (-21.2, -27.5), (-25.5, -24.2), -1.1)
    mb.add_arc_pts("primary", (-25.5, -24.2), (-24.5, -16.5), -1.0)
    mb.add_arc_pts("primary", (-24.5, -16.5), (-20.5, -13.8), -0.8)
    mb.add_arc_pts("detail", (-22.0, -24.5), (-23.0, -18.2), -0.7)

    # Viewer-right ear
    mb.add_arc_pts("primary", (21.5, -27.0), (25.8, -23.8), 1.1)
    mb.add_arc_pts("primary", (25.8, -23.8), (24.5, -15.5), 1.0)
    mb.add_arc_pts("primary", (24.5, -15.5), (20.8, -12.8), 0.8)
    mb.add_arc_pts("detail", (22.2, -24.0), (23.2, -17.5), 0.7)

    # --- CALM DIRECT EYES ON y = -27, BROWS & PINCE-NEZ WITH VERTICAL CORD ---
    mb.add_arc_pts("primary", (-16.8, -30.8), (-9.4, -32.6), 0.7)
    mb.add_arc_pts("primary", (-9.4, -32.6), (-2.6, -30.6), 0.55)
    mb.add_arc_pts("detail", (-15.8, -29.9), (-3.5, -29.8), 0.7)

    mb.add_arc_pts("primary", (2.8, -30.6), (9.6, -32.6), 0.7)
    mb.add_arc_pts("primary", (9.6, -32.6), (17.2, -30.8), 0.55)
    mb.add_arc_pts("detail", (3.8, -29.8), (16.2, -29.9), 0.7)

    mb.add_canonical_eye(
        -9.2,
        -26.8,
        width=9.2,
        upper_sag=1.62,
        lower_sag=-0.80,
        iris_r=1.82,
        pupil_r=0.96,
        gaze_dx=0.0,
    )
    mb.add_canonical_eye(
        9.4,
        -26.8,
        width=9.2,
        upper_sag=1.62,
        lower_sag=-0.80,
        iris_r=1.82,
        pupil_r=0.96,
        gaze_dx=0.0,
    )

    # Delicate thin pince-nez oval lenses + curved bridge + vertical hanging cord
    mb.add_arc_pts("detail", (-15.2, -25.4), (-3.6, -25.4), 3.7)
    mb.add_arc_pts("detail", (-15.2, -25.4), (-3.6, -25.4), -3.7)
    mb.add_arc_pts("detail", (3.8, -25.4), (15.4, -25.4), 3.7)
    mb.add_arc_pts("detail", (3.8, -25.4), (15.4, -25.4), -3.7)
    mb.add_arc_pts("detail", (-3.6, -26.0), (3.8, -26.0), 1.5)
    # Tiny pince-nez eyelet on left outer rim & fine vertical cord ending cleanly on collar
    mb.add_circle("detail", -16.1, -24.2, 0.85)
    mb.add_line("detail", -16.1, -23.3, -15.6, 17.0)

    # --- STRAIGHT CLASSICAL NOSE ---
    mb.add_arc_pts("primary", (-0.8, -29.2), (-1.8, -21.8), 0.22)
    mb.add_arc_pts("primary", (-1.8, -21.8), (-2.6, -16.4), 0.22)
    mb.add_arc_pts("primary", (-2.6, -16.4), (-1.4, -14.2), -0.45)
    mb.add_arc_pts("primary", (-1.4, -14.2), (1.8, -14.2), -0.35)
    mb.add_arc_pts("primary", (1.8, -14.2), (4.2, -15.4), -0.35)
    mb.add_arc_pts("primary", (4.2, -15.4), (4.5, -17.2), -0.45)
    mb.add_arc_pts("primary", (4.5, -17.2), (2.6, -17.8), -0.3)
    mb.add_arc_pts("detail", (-2.8, -15.8), (-4.0, -17.0), -0.3)

    # --- DENSE ROUNDED FULL DARK SCHOLAR'S BEARD & MUSTACHE ---
    # Full sweeping mustache
    mb.add_arc_pts("primary", (-14.2, -8.4), (-6.8, -12.0), 0.65)
    mb.add_arc_pts("primary", (-6.8, -12.0), (0.2, -11.8), 0.38)
    mb.add_arc_pts("primary", (0.2, -11.8), (7.2, -11.6), 0.38)
    mb.add_arc_pts("primary", (7.2, -11.6), (14.2, -8.2), 0.65)
    mb.add_arc_pts("primary", (-13.6, -5.8), (-6.2, -8.0), -0.5)
    mb.add_arc_pts("primary", (-6.2, -8.0), (0.2, -8.2), -0.35)
    mb.add_arc_pts("primary", (0.2, -8.2), (6.6, -7.8), -0.35)
    mb.add_arc_pts("primary", (6.6, -7.8), (13.6, -5.6), -0.5)
    # Subtle lower lip glimpse beneath mustache
    mb.add_arc_pts("detail", (-5.0, -4.8), (0.2, -4.2), -0.35)
    mb.add_arc_pts("detail", (0.2, -4.2), (5.2, -4.8), -0.35)

    # Seamless cheek-to-beard boundaries flowing cleanly into mustache corners
    mb.add_arc_pts("primary", (-20.2, -16.2), (-14.2, -8.4), -1.0)
    mb.add_arc_pts("primary", (20.6, -15.8), (14.2, -8.2), 1.0)

    # Full rounded scholar's beard silhouette
    mb.add_arc_pts("primary", (-20.5, -14.0), (-20.0, -4.2), -0.8)
    mb.add_arc_pts("primary", (-20.0, -4.2), (-16.6, 6.2), -1.1)
    mb.add_arc_pts("primary", (-16.6, 6.2), (-8.5, 13.5), -1.4)
    mb.add_arc_pts("primary", (-8.5, 13.5), (0.5, 14.8), -1.5)
    mb.add_arc_pts("primary", (0.5, 14.8), (9.8, 12.8), -1.5)
    mb.add_arc_pts("primary", (9.8, 12.8), (17.6, 5.2), -1.2)
    mb.add_arc_pts("primary", (17.6, 5.2), (21.0, -5.2), -1.0)
    mb.add_arc_pts("primary", (21.0, -5.2), (21.0, -13.8), -0.7)

    # Lush rhythmic scholar's beard & mustache waves via Euclid III.12
    mb.add_wave("detail", (-11.5, -9.2), (-1.5, -10.2), 2, wave_angle_deg, 1)
    mb.add_wave("detail", (1.8, -10.2), (11.5, -9.0), 2, wave_angle_deg, -1)
    mb.add_wave("detail", (-16.2, -6.5), (-12.5, 9.2), 3, wave_angle_deg + 4.0, -1)
    mb.add_wave("detail", (-11.0, -5.5), (-7.2, 12.2), 4, wave_angle_deg + 5.0, 1)
    mb.add_wave("detail", (-5.2, -5.0), (-2.2, 13.5), 4, wave_angle_deg + 5.0, -1)
    mb.add_wave("detail", (0.8, -5.0), (2.2, 13.5), 4, wave_angle_deg + 5.0, 1)
    mb.add_wave("detail", (6.5, -5.2), (8.2, 11.8), 4, wave_angle_deg + 5.0, -1)
    mb.add_wave("detail", (12.2, -6.0), (14.2, 8.2), 3, wave_angle_deg + 4.0, 1)

    # --- FOLDED WHITE COLLAR, WIDE BOW TIE, SHIRT FRONT & ACADEMIC JACKET ---
    # Neck & crisp folded white collar
    mb.add_arc_pts("primary", (-12.2, 11.2), (-13.2, 18.8), 0.6)
    mb.add_arc_pts("primary", (-13.2, 18.8), (-15.5, 27.2), -0.6)
    mb.add_arc_pts("primary", (-13.2, 18.8), (-4.5, 22.8), -0.8)
    mb.add_arc_pts("primary", (15.2, 8.2), (19.0, 14.2), -0.7)
    mb.add_arc_pts("primary", (19.0, 14.2), (9.5, 25.5), 1.1)
    mb.add_arc_pts("primary", (9.5, 25.5), (-0.2, 22.8), -0.7)

    # Wide dark silk bow tie centered cleanly at throat
    mb.add_arc_pts("primary", (-5.0, 22.5), (-0.2, 22.8), 0.35)
    mb.add_arc_pts("primary", (-0.2, 22.8), (-0.5, 27.6), 0.35)
    mb.add_arc_pts("primary", (-0.5, 27.6), (-5.2, 27.4), 0.35)
    mb.add_arc_pts("primary", (-5.2, 27.4), (-5.0, 22.5), 0.35)
    # Left bow wing
    mb.add_arc_pts("primary", (-5.0, 22.5), (-14.2, 27.2), 0.9)
    mb.add_arc_pts("primary", (-14.2, 27.2), (-14.4, 33.0), -0.7)
    mb.add_arc_pts("primary", (-14.4, 33.0), (-5.2, 27.4), -0.8)
    mb.add_arc_pts("detail", (-5.8, 25.2), (-12.8, 29.8), 0.4)
    # Right bow wing
    mb.add_arc_pts("primary", (-0.2, 22.8), (9.2, 26.8), -0.9)
    mb.add_arc_pts("primary", (9.2, 26.8), (7.6, 33.2), 0.7)
    mb.add_arc_pts("primary", (7.6, 33.2), (-0.5, 27.6), 0.8)
    mb.add_arc_pts("detail", (0.4, 25.4), (7.4, 29.8), -0.4)

    # Pale dress shirt front & central placket descending to waistcoat V
    mb.add_arc_pts("detail", (-3.2, 27.8), (-10.5, 65.5), 1.4)
    mb.add_circle("detail", -6.5, 44.5, 0.88)

    # Tailored notched German academic jacket lapels & broad shoulders to MED_R
    # Viewer-right notched jacket lapel
    mb.add_arc_pts("primary", (19.0, 14.2), (26.2, 18.8), -1.0)
    mb.add_arc_pts("primary", (26.2, 18.8), (26.8, 34.5), -1.0)
    mb.add_arc_pts("primary", (26.8, 34.5), (33.8, 36.5), 0.4)
    mb.add_arc_pts("primary", (33.8, 36.5), (24.8, 42.5), -0.5)
    mb.add_arc_pts("primary", (24.8, 42.5), (-14.5, 86.0), 4.2)
    mb.add_arc_pts("primary", (9.5, 25.5), (-11.2, 65.5), 2.4)
    mb.add_arc_pts("primary", (-11.2, 65.5), (-19.2, 86.0), 1.0)

    # Viewer-left notched jacket lapel
    mb.add_arc_pts("primary", (-13.8, 15.2), (-22.5, 20.5), 1.2)
    mb.add_arc_pts("primary", (-22.5, 20.5), (-28.5, 36.5), -1.4)
    mb.add_arc_pts("primary", (-28.5, 36.5), (-34.2, 39.2), -0.4)
    mb.add_arc_pts("primary", (-34.2, 39.2), (-28.2, 44.5), 0.5)
    mb.add_arc_pts("primary", (-28.2, 44.5), (-19.2, 86.0), -2.4)
    mb.add_arc_pts("primary", (-15.5, 27.2), (-15.2, 54.0), -1.0)
    mb.add_arc_pts("primary", (-15.2, 54.0), (-11.2, 65.5), -0.7)

    # Broad academic shoulders sweeping cleanly to MED_R = 92.0 (cabinet frame omitted)
    mb.add_arc_pts("primary", (-22.5, 20.5), (-66.0, 66.0), -9.2)
    mb.add_arc_pts("primary", (26.2, 18.8), (70.0, 62.0), 10.5)

    # Clean academic jacket sleeve seams & tailoring folds to MED_R
    mb.add_arc_pts("detail", (-39.5, 36.0), (-48.5, 79.0), -2.6)
    mb.add_arc_pts("detail", (-29.5, 58.0), (-32.5, 84.0), -1.2)
    mb.add_arc_pts("detail", (42.5, 32.0), (54.5, 76.0), 3.4)
    mb.add_arc_pts("detail", (22.0, 56.0), (14.5, 86.0), 1.8)

    return mb.build()


def build_pasch_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Moritz Pasch medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_pasch_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_pasch_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``pasch_dark.svg`` and ``pasch_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "pasch_dark.svg"
    light_path = target_dir / "pasch_light.svg"
    dark_path.write_text(
        build_pasch_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_pasch_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
