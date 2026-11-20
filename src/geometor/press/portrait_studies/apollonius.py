"""Study 26: Apollonius of Perga (after the 1537 Venice woodcut portrait)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_apollonius_elements",
    "build_apollonius_svg",
    "write_apollonius_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_apollonian_gasket_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    outer_r: float = 13.0,
) -> None:
    """Draw an exact Apollonian gasket in the left open medallion margin.

    Constructs the outer enclosing Soddy circle, three mutually tangent
    primary circles in equilateral symmetry, the inner central Soddy circle,
    and three secondary Soddy circles nestled in the outer curvilinear cusps
    using exact Descartes Circle Theorem radii.
    """
    sqrt3 = math.sqrt(3.0)
    r_main = outer_r / (1.0 + 2.0 / sqrt3)
    d_main = 2.0 * r_main / sqrt3
    r_in = d_main - r_main
    # Exact Descartes curvature solution for outer cusp circles:
    # k_s = (9 - 4*sqrt(3)) / r_main => r_sec = r_main * (9 + 4*sqrt(3)) / 33
    r_sec = r_main * (9.0 + 4.0 * sqrt3) / 33.0
    d_sec = outer_r - r_sec

    # Outer enclosing Soddy circle & inner central Soddy circle
    mb.add_circle("golden", cx, cy, outer_r)
    mb.add_circle("golden", cx, cy, r_in)

    # Three mutually tangent primary circles
    for deg in (-90.0, 30.0, 150.0):
        rad = math.radians(deg)
        mx = cx + d_main * math.cos(rad)
        my = cy + d_main * math.sin(rad)
        mb.add_circle("golden", mx, my, r_main)

    # Three secondary outer-cusp Soddy circles
    for deg in (90.0, -30.0, -150.0):
        rad = math.radians(deg)
        sx = cx + d_sec * math.cos(rad)
        sy = cy + d_sec * math.sin(rad)
        mb.add_circle("golden", sx, sy, r_sec)


def _add_apollonius_circles_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    focus_a: float = 4.5,
) -> None:
    """Draw the Circle of Apollonius coaxal pencil and conic-section axes.

    Constructs two focus/limit nodes ``A`` and ``B`` along the horizontal
    focal axis, the vertical radical axis, nested Apollonian circles for
    constant distance ratios ``|PA| / |PB| = k``, and a symmetric pair of
    exact orthogonal coaxal circles passing through both foci.
    """
    # Horizontal focal axis and vertical radical axis
    mb.add_line("golden", cx - 14.2, cy, cx + 14.2, cy)
    mb.add_line("golden", cx, cy - 13.0, cx, cy + 13.0)

    # Focus / limit points A and B
    mb.add_circle("golden", cx - focus_a, cy, 0.85, filled=True)
    mb.add_circle("golden", cx + focus_a, cy, 0.85, filled=True)

    # Nested Apollonian circles around A and B (ratio k = |PA|/|PB|)
    for k in (2.0, 3.3):
        xc_off = focus_a * (k * k + 1.0) / (k * k - 1.0)
        rk = (2.0 * focus_a * k) / (k * k - 1.0)
        mb.add_circle("golden", cx - xc_off, cy, rk)
        mb.add_circle("golden", cx + xc_off, cy, rk)

    # Symmetric pair of exact orthogonal coaxal circles passing through A and B
    orth_offset = 4.2
    orth_r = math.hypot(focus_a, orth_offset)
    mb.add_circle("golden", cx, cy - orth_offset, orth_r)
    mb.add_circle("golden", cx, cy + orth_offset, orth_r)


def build_apollonius_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Apollonius of Perga.

    Calibrated to the 1537 Venice woodcut bust: high domed forehead with
    contemplation furrows, curly framing hair, three-quarter right-turned
    gaze on ``y = -27``, long tapered philosopher's beard crafted with
    ``Euclid III.12`` tangent wave arcs, draped scholar's robe, and the
    foreground geometric diagram disc & dividers. Margin motifs display an
    exact Apollonian gasket (left) and coaxal Circles of Apollonius (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=1.5,
        eye_rx=16.4,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN MARGIN MOTIFS (open left & right margins, zero face crossing) ---
    _add_apollonian_gasket_motif(mb, cx=-63.0, cy=-26.0, outer_r=13.0)
    _add_apollonius_circles_motif(mb, cx=63.0, cy=-26.0, focus_a=4.5)

    # --- CRANIUM, BALD DOMED FOREHEAD & RIGHT FACE CONTOUR ---
    # Single smooth continuous circular arch across the high domed cranium
    mb.add_arc_pts("primary", (-15.5, -62.5), (21.0, -56.8), 8.6)
    # Right temple curly hair puff
    mb.add_arc_pts("primary", (21.0, -56.8), (25.5, -51.0), 1.6)
    mb.add_arc_pts("primary", (25.5, -51.0), (23.8, -45.5), 1.2)
    mb.add_arc_pts("primary", (23.8, -45.5), (21.5, -41.5), 0.7)
    mb.add_arc_pts("detail", (20.2, -55.2), (21.8, -47.5), 0.8)
    mb.add_arc_pts("detail", (21.8, -47.5), (21.5, -41.5), 0.5)
    # Right temple, brow prominence, orbit & cheekbone into beard
    mb.add_arc_pts("primary", (21.5, -41.5), (23.4, -34.2), 1.1)
    mb.add_arc_pts("primary", (23.4, -34.2), (21.6, -27.8), -0.8)
    mb.add_arc_pts("primary", (21.6, -27.8), (23.6, -20.5), 1.3)
    mb.add_arc_pts("primary", (23.6, -20.5), (21.8, -13.0), 0.9)

    # --- CURLY FRAMING HAIR MASS (VIEWER'S LEFT / BACK OF HEAD) ---
    # Scalloped curly outer silhouette
    mb.add_arc_pts("primary", (-15.5, -62.5), (-23.8, -57.5), -1.7)
    mb.add_arc_pts("primary", (-23.8, -57.5), (-28.8, -49.5), -1.9)
    mb.add_arc_pts("primary", (-28.8, -49.5), (-27.6, -43.2), -0.9)
    mb.add_arc_pts("primary", (-27.6, -43.2), (-31.8, -36.8), -1.8)
    mb.add_arc_pts("primary", (-31.8, -36.8), (-28.2, -30.2), -1.5)
    mb.add_arc_pts("primary", (-28.2, -30.2), (-23.5, -25.8), -1.0)
    # Lower hair behind ear to collar nape
    mb.add_arc_pts("primary", (-23.8, -16.8), (-26.0, -11.8), -1.1)
    mb.add_arc_pts("primary", (-26.0, -11.8), (-22.0, -8.5), -0.9)

    # Interior hairline along left temple down to front of ear
    mb.add_arc_pts("primary", (-15.5, -62.5), (-18.6, -52.0), -1.0)
    mb.add_arc_pts("primary", (-18.6, -52.0), (-19.2, -42.0), 1.0)
    mb.add_arc_pts("primary", (-19.2, -42.0), (-16.2, -33.5), -1.2)
    mb.add_arc_pts("primary", (-16.2, -33.5), (-16.8, -28.0), 0.7)

    # Curly interior hair texture via Euclid III.12 waves
    mb.add_wave("detail", (-17.5, -59.5), (-25.5, -45.5), 3, wave_angle_deg + 8.0, 1)
    mb.add_wave("detail", (-21.0, -54.5), (-28.5, -36.0), 3, wave_angle_deg + 10.0, -1)
    mb.add_wave("detail", (-21.5, -44.0), (-25.0, -28.0), 3, wave_angle_deg + 6.0, 1)
    mb.add_arc_pts("detail", (-18.5, -58.0), (-24.0, -53.5), -1.3)
    mb.add_arc_pts("detail", (-22.5, -36.5), (-28.0, -33.0), -1.2)

    # --- FOREHEAD CONTEMPLATION FURROWS ---
    mb.add_arc_pts("detail", (-6.0, -51.5), (13.0, -51.0), 1.2)
    mb.add_arc_pts("detail", (-9.0, -46.2), (16.2, -45.6), 1.1)
    mb.add_arc_pts("detail", (-6.5, -41.0), (15.8, -40.6), 0.8)
    # Subtle glabella vertical creases between the brows
    mb.add_arc_pts("detail", (9.6, -37.8), (9.4, -32.2), 0.3)
    mb.add_arc_pts("detail", (11.6, -37.4), (11.4, -32.4), -0.3)

    # --- LEFT EAR (VIEWER'S LEFT, 3/4 PROFILE) ---
    mb.add_arc_pts("primary", (-16.8, -28.0), (-22.8, -25.4), -1.4)
    mb.add_arc_pts("primary", (-22.8, -25.4), (-23.2, -18.0), -1.3)
    mb.add_arc_pts("primary", (-23.2, -18.0), (-18.5, -13.0), -1.5)
    mb.add_arc_pts("primary", (-18.5, -13.0), (-15.0, -15.2), -0.8)
    mb.add_arc_pts("detail", (-18.0, -25.6), (-21.0, -21.8), -1.1)
    mb.add_arc_pts("detail", (-21.0, -21.8), (-19.2, -16.2), -1.0)
    mb.add_arc_pts("detail", (-16.6, -22.8), (-17.8, -18.5), 0.7)

    # --- EYEBROWS & CANONICAL EYES (y = -27) ---
    # Viewer's left brow (strong primary upper arch + softer detail underside)
    mb.add_arc_pts("primary", (-6.8, -32.2), (2.0, -34.6), 1.0)
    mb.add_arc_pts("primary", (2.0, -34.6), (7.8, -33.9), 0.5)
    mb.add_arc_pts("detail", (-6.0, -31.0), (2.2, -33.2), 0.8)
    mb.add_arc_pts("detail", (2.2, -33.2), (7.6, -32.7), 0.4)

    # Viewer's right brow (foreshortened)
    mb.add_arc_pts("primary", (12.6, -34.0), (17.6, -35.0), 0.7)
    mb.add_arc_pts("primary", (17.6, -35.0), (22.4, -33.0), 0.6)
    mb.add_arc_pts("detail", (12.8, -32.7), (17.6, -33.4), 0.5)
    mb.add_arc_pts("detail", (17.6, -33.4), (22.0, -32.0), 0.5)

    # Canonical eyes on y = -27 with thoughtful right-ward gaze
    mb.add_canonical_eye(
        1.5,
        -27.2,
        width=10.4,
        upper_sag=2.5,
        lower_sag=-1.2,
        iris_r=2.15,
        pupil_r=1.05,
        gaze_dx=0.9,
    )
    mb.add_canonical_eye(
        16.4,
        -27.0,
        width=7.8,
        upper_sag=2.2,
        lower_sag=-1.05,
        iris_r=1.85,
        pupil_r=0.95,
        gaze_dx=0.6,
    )
    # Under-eye character creases
    mb.add_arc_pts("detail", (-3.5, -24.2), (6.0, -24.5), -0.8)
    mb.add_arc_pts("detail", (12.8, -24.3), (20.0, -24.6), -0.7)

    # --- NOSE & CHEEK PLANES ---
    mb.add_arc_pts("primary", (10.5, -32.5), (12.0, -25.0), -0.5)
    mb.add_arc_pts("primary", (12.0, -25.0), (14.8, -18.2), -0.4)
    mb.add_arc_pts("primary", (14.8, -18.2), (16.4, -14.6), 0.6)
    mb.add_arc_pts("primary", (16.4, -14.6), (14.8, -12.4), 0.9)
    mb.add_arc_pts("primary", (14.8, -12.4), (10.6, -12.3), 0.5)
    mb.add_arc_pts("primary", (10.6, -12.3), (8.4, -13.4), 0.5)
    # Clean C-curve left nostril wing
    mb.add_arc_pts("primary", (8.4, -13.4), (8.2, -15.6), 0.6)
    mb.add_arc_pts("primary", (8.2, -15.6), (10.2, -16.1), 0.4)
    # Subtle nasal shadow & right nostril edge
    mb.add_arc_pts("detail", (10.4, -13.3), (12.8, -13.1), -0.4)
    mb.add_arc_pts("detail", (15.8, -13.5), (17.2, -14.5), 0.5)
    mb.add_arc_pts("detail", (8.8, -28.5), (9.6, -21.0), 0.4)
    mb.add_arc_pts("detail", (9.6, -21.0), (9.0, -16.8), -0.3)
    # Cheek & nasolabial character creases
    mb.add_arc_pts("detail", (6.2, -15.4), (1.8, -10.2), -0.8)
    mb.add_arc_pts("detail", (-9.6, -22.5), (-8.5, -13.2), 0.9)

    # --- MUSTACHE & MOUTH ---
    # Mustache upper wings sweeping down from philtrum
    mb.add_arc_pts("primary", (11.5, -10.8), (5.5, -9.2), -1.1)
    mb.add_arc_pts("primary", (5.5, -9.2), (0.6, -4.4), -1.2)
    mb.add_arc_pts("primary", (0.6, -4.4), (-2.2, 2.2), -0.8)

    mb.add_arc_pts("primary", (11.5, -10.8), (17.2, -9.5), 1.0)
    mb.add_arc_pts("primary", (17.2, -9.5), (20.8, -4.6), 1.0)
    mb.add_arc_pts("primary", (20.8, -4.6), (22.0, 0.8), 0.6)

    # Mustache inner arch framing the lips
    mb.add_arc_pts("primary", (11.5, -8.4), (6.5, -7.2), -0.7)
    mb.add_arc_pts("primary", (6.5, -7.2), (3.2, -3.5), -0.8)
    mb.add_arc_pts("primary", (3.2, -3.5), (1.6, 2.0), -0.5)

    mb.add_arc_pts("primary", (11.5, -8.4), (16.2, -7.4), 0.7)
    mb.add_arc_pts("primary", (16.2, -7.4), (18.6, -3.8), 0.7)
    mb.add_arc_pts("primary", (18.6, -3.8), (19.2, 0.8), 0.4)

    # Mustache texture
    mb.add_arc_pts("detail", (9.2, -9.5), (2.2, -3.8), -0.9)
    mb.add_arc_pts("detail", (13.8, -9.4), (19.5, -4.0), 0.8)

    # Mouth & lower lip beneath mustache arch
    mb.add_arc_pts("detail", (6.8, -6.5), (11.5, -7.1), 0.4)
    mb.add_arc_pts("detail", (11.5, -7.1), (15.6, -6.2), 0.4)
    mb.add_arc_pts("primary", (6.2, -5.8), (11.5, -6.2), 0.4)
    mb.add_arc_pts("primary", (11.5, -6.2), (16.0, -5.3), 0.3)
    mb.add_arc_pts("primary", (7.0, -3.5), (11.5, -2.4), -0.8)
    mb.add_arc_pts("primary", (11.5, -2.4), (15.4, -3.4), -0.7)
    mb.add_arc_pts("detail", (8.6, -0.8), (14.0, -0.8), -0.5)

    # --- LONG CASCADING PHILOSOPHER'S BEARD ---
    # Left cheek-to-beard line (detail)
    mb.add_arc_pts("detail", (-14.8, -15.0), (-11.0, -8.2), -0.8)
    mb.add_arc_pts("detail", (-11.0, -8.2), (-6.2, -3.2), -0.7)
    mb.add_arc_pts("detail", (-6.2, -3.2), (-2.2, 2.2), -0.5)

    # Outer left beard silhouette (primary)
    mb.add_arc_pts("primary", (-15.5, -15.0), (-15.8, -4.0), -0.8)
    mb.add_arc_pts("primary", (-15.8, -4.0), (-17.8, 7.5), -1.3)
    mb.add_arc_pts("primary", (-17.8, 7.5), (-16.2, 21.5), -1.4)
    mb.add_arc_pts("primary", (-16.2, 21.5), (-13.0, 36.5), -1.2)
    mb.add_arc_pts("primary", (-13.0, 36.5), (-8.4, 51.5), -1.1)
    mb.add_arc_pts("primary", (-8.4, 51.5), (-3.0, 63.5), -0.9)
    mb.add_arc_pts("primary", (-3.0, 63.5), (1.4, 70.0), -0.7)

    # Outer right beard silhouette (primary)
    mb.add_arc_pts("primary", (21.8, -13.0), (23.6, -2.0), 1.0)
    mb.add_arc_pts("primary", (23.6, -2.0), (22.6, 10.5), 1.3)
    mb.add_arc_pts("primary", (22.6, 10.5), (20.0, 24.0), 1.3)
    mb.add_arc_pts("primary", (20.0, 24.0), (15.6, 38.5), 1.2)
    mb.add_arc_pts("primary", (15.6, 38.5), (10.4, 52.5), 1.1)
    mb.add_arc_pts("primary", (10.4, 52.5), (5.6, 63.5), 0.9)
    mb.add_arc_pts("primary", (5.6, 63.5), (1.4, 70.0), 0.7)

    # Flowing Euclid III.12 tangent wave strands throughout the long beard
    mb.add_wave("detail", (-13.5, -11.5), (-12.5, 25.0), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (-9.8, -6.0), (-9.2, 42.0), 5, wave_angle_deg - 2.0, -1)
    mb.add_wave("detail", (-5.5, -1.0), (-5.2, 55.5), 5, wave_angle_deg - 3.0, 1)
    mb.add_wave("detail", (-1.0, 2.0), (-1.4, 64.5), 6, wave_angle_deg - 4.0, -1)
    mb.add_wave("detail", (3.8, 1.0), (1.4, 67.5), 6, wave_angle_deg - 4.0, 1)
    mb.add_wave("detail", (8.8, 0.5), (4.5, 61.5), 5, wave_angle_deg - 3.0, -1)
    mb.add_wave("detail", (13.8, 0.0), (8.8, 50.0), 5, wave_angle_deg - 2.0, 1)
    mb.add_wave("detail", (18.2, 0.5), (14.2, 36.0), 4, wave_angle_deg, -1)

    # --- SCHOLAR'S DRAPED ROBE & SHOULDERS ---
    # Left shoulder outer contour descending flush to medallion rim
    mb.add_arc_pts("primary", (-22.0, -8.5), (-37.0, -4.5), -1.6)
    mb.add_arc_pts("primary", (-37.0, -4.5), (-51.5, 5.5), -2.4)
    mb.add_arc_pts("primary", (-51.5, 5.5), (-63.2, 20.0), -2.2)
    mb.add_arc_pts("primary", (-63.2, 20.0), (-70.8, 38.0), -1.8)
    mb.add_arc_pts("primary", (-70.8, 38.0), (-75.5, 58.0), -1.4)

    # Wide left scholar's lapel / shawl folds grounded flush to lower rim
    mb.add_arc_pts("primary", (-20.5, -8.0), (-27.5, 8.5), -1.6)
    mb.add_arc_pts("primary", (-27.5, 8.5), (-29.5, 26.5), -1.4)
    mb.add_arc_pts("primary", (-29.5, 26.5), (-25.5, 46.5), -1.4)
    mb.add_arc_pts("primary", (-25.5, 46.5), (-19.2, 66.5), -1.2)
    mb.add_arc_pts("primary", (-19.2, 66.5), (-13.5, 86.0), -0.8)

    mb.add_arc_pts("primary", (-31.5, -6.0), (-42.5, 10.5), -1.8)
    mb.add_arc_pts("primary", (-42.5, 10.5), (-45.5, 28.5), -1.6)
    mb.add_arc_pts("primary", (-45.5, 28.5), (-38.5, 48.5), -1.8)
    mb.add_arc_pts("primary", (-38.5, 48.5), (-28.5, 83.0), -1.5)

    # Left sleeve & drapery interior folds (cleanly nested within cloth panels)
    mb.add_arc_pts("primary", (-45.5, 28.5), (-56.5, 46.5), -1.8)
    mb.add_arc_pts("primary", (-56.5, 46.5), (-60.5, 72.0), -1.4)
    mb.add_arc_pts("detail", (-52.5, 16.0), (-62.5, 39.0), -1.6)
    mb.add_arc_pts("detail", (-62.5, 39.0), (-66.5, 65.0), -1.2)
    mb.add_arc_pts("detail", (-36.5, 18.0), (-33.5, 45.0), -1.2)
    mb.add_arc_pts("detail", (-33.5, 45.0), (-24.5, 78.0), -1.0)
    mb.add_arc_pts("detail", (-22.5, 30.0), (-15.5, 58.0), -1.1)

    # Right shoulder outer contour meeting the geometric disc
    mb.add_arc_pts("primary", (23.4, -0.5), (35.5, 3.8), 1.5)
    mb.add_arc_pts("primary", (35.5, 3.8), (47.5, 13.0), 1.8)
    mb.add_arc_pts("primary", (47.5, 13.0), (55.5, 26.0), 1.4)

    # Right lapel & chest drapery folds
    mb.add_arc_pts("primary", (22.8, 4.5), (34.5, 15.2), 1.4)
    mb.add_arc_pts("primary", (34.5, 15.2), (43.8, 27.2), 1.1)
    mb.add_arc_pts("detail", (20.8, 14.5), (31.2, 24.5), 1.2)
    mb.add_arc_pts("detail", (31.2, 24.5), (36.8, 31.8), 0.9)
    mb.add_arc_pts("detail", (32.5, 6.0), (45.0, 18.0), 1.3)

    # --- LOWER-RIGHT FOREGROUND: GEOMETRIC DIAGRAM DISC, DIVIDERS & HAND ---
    # Circular geometric diagram / celestial-conic disc held in foreground
    mb.add_arc("primary", 55.0, 65.0, 39.0, -170.0, -18.0)
    mb.add_arc("detail", 55.0, 65.0, 36.2, -166.0, -22.0)

    # Clean woodcut-faithful inscribed triangle & upper conic arc on disc
    mb.add_line("detail", 60.0, 32.5, 78.2, 62.5)
    mb.add_line("detail", 78.2, 62.5, 41.0, 64.8)
    mb.add_line("detail", 60.0, 32.5, 45.8, 55.2)
    mb.add_arc_pts("detail", (24.8, 42.5), (42.8, 30.2), -2.2)

    # Open geometric dividers / compass held in foreground hand
    mb.add_circle("primary", 24.5, 68.5, 2.0)
    mb.add_circle("detail", 24.5, 68.5, 0.8)
    # Upper divider blade pointing to diagram apex
    mb.add_line("primary", 23.6, 66.8, 58.2, 35.2)
    mb.add_line("primary", 26.2, 67.6, 58.2, 35.2)
    # Lower divider blade spanning right side of triangle
    mb.add_line("primary", 26.2, 69.2, 68.5, 51.0)
    mb.add_line("primary", 25.8, 71.2, 68.5, 51.0)

    # Foreground right hand gripping the dividers
    mb.add_arc_pts("primary", (-7.5, 75.5), (6.5, 70.5), 1.2)
    # Thumb arching over the pivot
    mb.add_arc_pts("primary", (6.5, 70.5), (16.5, 63.0), 1.4)
    mb.add_arc_pts("primary", (16.5, 63.0), (23.8, 62.6), 1.0)
    mb.add_arc_pts("primary", (23.8, 62.6), (24.2, 65.6), 0.7)
    mb.add_arc_pts("primary", (24.2, 65.6), (16.8, 69.5), -0.8)
    # Extended supporting fingers beneath pivot
    mb.add_arc_pts("primary", (14.5, 73.2), (32.8, 71.4), 0.9)
    mb.add_arc_pts("primary", (32.8, 71.4), (36.8, 73.4), 0.8)
    mb.add_arc_pts("primary", (36.8, 73.4), (34.5, 76.2), 0.7)
    mb.add_arc_pts("primary", (34.5, 76.2), (15.5, 77.5), -0.8)
    # Lower curled fingers and palm base
    mb.add_arc_pts("primary", (14.0, 77.8), (31.5, 77.5), 0.7)
    mb.add_arc_pts("primary", (31.5, 77.5), (33.2, 80.4), 0.7)
    mb.add_arc_pts("primary", (33.2, 80.4), (12.0, 83.0), -0.8)
    mb.add_arc_pts("primary", (12.0, 83.0), (-3.0, 83.5), -0.6)
    mb.add_arc_pts("detail", (8.0, 74.0), (15.5, 72.5), 0.5)
    mb.add_arc_pts("detail", (6.5, 79.0), (14.8, 77.8), 0.5)

    return mb.build()


def build_apollonius_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Apollonius of Perga medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_apollonius_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_apollonius_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``apollonius_dark.svg`` and ``apollonius_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "apollonius_dark.svg"
    light_path = target_dir / "apollonius_light.svg"
    dark_path.write_text(
        build_apollonius_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_apollonius_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
