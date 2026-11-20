"""Study 27: Heron of Alexandria (after the classical Hellenic marble-bust engraving)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_heron_elements",
    "build_heron_svg",
    "write_heron_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_dashed_line(
    mb: MedallionBuilder,
    layer: str,
    p1: tuple[float, float],
    p2: tuple[float, float],
    *,
    dash_len: float = 1.8,
    gap_len: float = 1.4,
) -> None:
    """Draw a construction segment as evenly spaced short straight strokes."""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    if dist < 1e-6:
        return
    ux, uy = dx / dist, dy / dist
    step = dash_len + gap_len
    pos = 0.0
    while pos < dist - 0.35:
        seg_end = min(dist, pos + dash_len)
        mb.add_line(
            layer,
            x1 + ux * pos,
            y1 + uy * pos,
            x1 + ux * seg_end,
            y1 + uy * seg_end,
        )
        pos += step


def _project_onto_segment(
    pt: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
) -> tuple[float, float]:
    """Return the exact perpendicular foot from ``pt`` onto line ``p1-p2``."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    denom = dx * dx + dy * dy
    if denom < 1e-9:
        return p1
    t = ((pt[0] - p1[0]) * dx + (pt[1] - p1[1]) * dy) / denom
    return (p1[0] + t * dx, p1[1] + t * dy)


def _add_heron_area_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Heron's Area Triangle & Inscribed Circle (``A = r * s``) in left margin.

    Constructs a scalene triangle ``ABC`` with its exact geometric incircle,
    incenter ``I``, three perpendicular inradii to the tangency points on
    sides ``a, b, c``, and vertex-to-incenter angle bisectors partitioning
    the triangle into three sub-triangles of altitude ``r``.
    """
    pt_a = (cx - 12.5, cy + 7.5)
    pt_b = (cx + 13.0, cy + 7.5)
    pt_c = (cx - 3.5, cy - 12.5)

    side_a = math.hypot(pt_b[0] - pt_c[0], pt_b[1] - pt_c[1])
    side_b = math.hypot(pt_c[0] - pt_a[0], pt_c[1] - pt_a[1])
    side_c = math.hypot(pt_a[0] - pt_b[0], pt_a[1] - pt_b[1])
    perim = side_a + side_b + side_c
    semi = 0.5 * perim
    # Heron's formula: Area = sqrt(s(s - a)(s - b)(s - c)) = r * s
    area = math.sqrt(semi * (semi - side_a) * (semi - side_b) * (semi - side_c))
    inradius = area / semi

    incenter = (
        (side_a * pt_a[0] + side_b * pt_b[0] + side_c * pt_c[0]) / perim,
        (side_a * pt_a[1] + side_b * pt_b[1] + side_c * pt_c[1]) / perim,
    )

    # Outer scalene triangle ABC
    mb.add_line("golden", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_a[0], pt_a[1])

    # Exact geometric incircle
    mb.add_circle("golden", incenter[0], incenter[1], inradius)

    # Vertex-to-incenter angle bisectors
    for vtx in (pt_a, pt_b, pt_c):
        mb.add_line("golden", vtx[0], vtx[1], incenter[0], incenter[1])
        mb.add_circle("golden", vtx[0], vtx[1], 0.78, filled=True)

    # Three perpendicular inradii from I to tangency points on sides a, b, c
    for s1, s2 in ((pt_b, pt_c), (pt_c, pt_a), (pt_a, pt_b)):
        foot = _project_onto_segment(incenter, s1, s2)
        mb.add_line("golden", incenter[0], incenter[1], foot[0], foot[1])
        mb.add_circle("golden", foot[0], foot[1], 0.48, filled=True)

    # Incenter marker
    mb.add_circle("golden", incenter[0], incenter[1], 0.85, filled=True)


def _add_catoptrica_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Heron's *Catoptrica* equal-angle reflection and shortest-path proof.

    Constructs a horizontal mirror baseline, asymmetric source ``A`` and
    target ``B``, virtual reflection point ``B'`` below the mirror, the
    straight shortest path ``A-P-B'`` hitting mirror point ``P``, reflected
    ray ``P-B``, surface normal at ``P``, and equal incidence/reflection arcs.
    """
    y_mirror = cy + 2.2
    h_a = 13.0
    h_b = 8.6

    pt_a = (cx - 10.5, y_mirror - h_a)
    pt_b = (cx + 10.5, y_mirror - h_b)
    pt_b_prime = (cx + 10.5, y_mirror + h_b)

    # Exact shortest-path mirror intersection P along straight line A - B'
    t_hit = h_a / (h_a + h_b)
    pt_p = (pt_a[0] + t_hit * (pt_b_prime[0] - pt_a[0]), y_mirror)

    # Horizontal mirror baseline
    mb.add_line("golden", cx - 13.5, y_mirror, cx + 13.5, y_mirror)

    # Vertical normal at P and right-angle tick
    mb.add_line("golden", pt_p[0], y_mirror - 11.8, pt_p[0], y_mirror)

    # Actual reflected optical path A -> P -> B
    mb.add_line("golden", pt_a[0], pt_a[1], pt_p[0], pt_p[1])
    mb.add_line("golden", pt_p[0], pt_p[1], pt_b[0], pt_b[1])

    # Dashed virtual continuation P -> B' and perpendicular reflection B -> B'
    _add_dashed_line(mb, "golden", pt_p, pt_b_prime, dash_len=1.7, gap_len=1.3)
    _add_dashed_line(mb, "golden", pt_b, pt_b_prime, dash_len=1.7, gap_len=1.3)

    # Equal incidence and reflection angle arcs around the surface normal at P
    ang_a = math.degrees(math.atan2(pt_a[1] - pt_p[1], pt_a[0] - pt_p[0]))
    ang_b = math.degrees(math.atan2(pt_b[1] - pt_p[1], pt_b[0] - pt_p[0]))
    mb.add_arc("golden", pt_p[0], pt_p[1], 5.2, ang_a, -90.0)
    mb.add_arc("golden", pt_p[0], pt_p[1], 5.2, -90.0, ang_b)

    # Marked optical nodes: solid A, B, P and open virtual image B'
    mb.add_circle("golden", pt_a[0], pt_a[1], 0.85, filled=True)
    mb.add_circle("golden", pt_b[0], pt_b[1], 0.85, filled=True)
    mb.add_circle("golden", pt_p[0], pt_p[1], 0.85, filled=True)
    mb.add_circle("golden", pt_b_prime[0], pt_b_prime[1], 0.95)


def build_heron_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Heron of Alexandria.

    Calibrated to the classical Hellenic marble-bust engraving: short sculpted
    curly locks framing the crown, calm three-quarter right gaze on ``y = -27``,
    classical Greek nose, full curly philosopher's mustache and rounded beard
    modeled with ``Euclid III.12`` tangent wave strands, and a dignified Greek
    chiton/himation neckline descending smoothly to the medallion rim.
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-3.2,
        eye_rx=16.5,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN MARGIN MOTIFS (open left & right margins, zero face crossing) ---
    _add_heron_area_motif(mb, cx=-63.0, cy=-26.0)
    _add_catoptrica_motif(mb, cx=63.0, cy=-26.0)

    # --- SHORT SCULPTED HELLENISTIC CURLY HAIR & CROWN ---
    # Outer sculpted curly hair silhouette
    mb.add_arc_pts("primary", (-28.8, -26.5), (-30.6, -34.8), 1.4)
    mb.add_arc_pts("primary", (-30.6, -34.8), (-28.0, -44.2), 1.6)
    mb.add_arc_pts("primary", (-28.0, -44.2), (-22.2, -52.2), 1.7)
    mb.add_arc_pts("primary", (-22.2, -52.2), (-13.2, -57.8), 1.6)
    mb.add_arc_pts("primary", (-13.2, -57.8), (-2.0, -60.5), 1.7)
    mb.add_arc_pts("primary", (-2.0, -60.5), (9.5, -59.0), 1.6)
    mb.add_arc_pts("primary", (9.5, -59.0), (18.8, -53.2), 1.7)
    mb.add_arc_pts("primary", (18.8, -53.2), (23.6, -44.2), 1.5)
    mb.add_arc_pts("primary", (23.6, -44.2), (24.5, -36.5), 1.1)
    mb.add_arc_pts("primary", (24.5, -36.5), (22.8, -31.2), 0.7)

    # Interior hairline framing the broad brow (sculpted Hellenistic curls)
    mb.add_arc_pts("primary", (-21.5, -25.0), (-22.2, -33.5), 1.0)
    mb.add_arc_pts("primary", (-22.2, -33.5), (-18.5, -43.0), -1.1)
    mb.add_arc_pts("primary", (-18.5, -43.0), (-10.8, -49.0), 1.3)
    mb.add_arc_pts("primary", (-10.8, -49.0), (-1.5, -49.6), 1.4)
    mb.add_arc_pts("primary", (-1.5, -49.6), (9.8, -49.8), 1.3)
    mb.add_arc_pts("primary", (9.8, -49.8), (18.4, -46.2), 1.2)
    mb.add_arc_pts("primary", (18.4, -46.2), (21.6, -38.5), 0.8)
    mb.add_arc_pts("primary", (21.6, -38.5), (21.5, -31.5), 0.5)

    # Sculpted curly locks across the crown (Euclid III.12 waves + lock curves)
    mb.add_wave("detail", (-25.5, -32.0), (-13.0, -54.5), 4, wave_angle_deg + 8.0, 1)
    mb.add_wave("detail", (-19.5, -48.5), (14.5, -54.0), 5, wave_angle_deg + 6.0, -1)
    mb.add_wave("detail", (-12.0, -54.5), (19.0, -47.5), 4, wave_angle_deg + 6.0, 1)
    mb.add_arc_pts("detail", (-27.0, -37.5), (-22.0, -43.5), 1.4)
    mb.add_arc_pts("detail", (-24.2, -29.0), (-25.8, -35.5), 1.2)
    mb.add_arc_pts("detail", (17.5, -48.5), (22.5, -41.5), 1.2)
    mb.add_arc_pts("detail", (-3.5, -53.8), (2.2, -50.2), -1.1)

    # --- RIGHT FACE CONTOUR (VIEWER'S RIGHT, 3/4 VIEW) ---
    mb.add_arc_pts("primary", (22.8, -31.2), (23.4, -26.5), 0.8)
    mb.add_arc_pts("primary", (23.4, -26.5), (22.4, -21.8), -0.6)
    mb.add_arc_pts("primary", (22.4, -21.8), (24.0, -15.0), 1.2)
    mb.add_arc_pts("primary", (24.0, -15.0), (22.8, -8.5), 0.8)

    # --- FOREHEAD CALM FURROWS ---
    mb.add_arc_pts("detail", (-11.0, -42.5), (15.5, -42.2), 0.9)
    mb.add_arc_pts("detail", (-13.0, -37.8), (17.0, -37.8), 0.8)
    mb.add_arc_pts("detail", (6.5, -35.5), (6.8, -31.0), 0.25)

    # --- LEFT EAR (VIEWER'S LEFT) ---
    mb.add_arc_pts("primary", (-22.8, -26.8), (-28.8, -24.2), -1.5)
    mb.add_arc_pts("primary", (-28.8, -24.2), (-28.5, -15.2), -1.5)
    mb.add_arc_pts("primary", (-28.5, -15.2), (-24.0, -7.8), -1.5)
    mb.add_arc_pts("primary", (-24.0, -7.8), (-21.0, -10.5), -0.8)
    mb.add_arc_pts("detail", (-24.0, -24.2), (-26.8, -19.2), -1.1)
    mb.add_arc_pts("detail", (-26.8, -19.2), (-24.6, -12.2), -1.1)
    mb.add_arc_pts("detail", (-22.4, -19.8), (-23.2, -15.0), 0.7)

    # --- EYEBROWS & CANONICAL EYES (y = -27) ---
    # Viewer's left brow (calm arched classical brow)
    mb.add_arc_pts("primary", (-12.5, -30.5), (-3.5, -34.2), 1.2)
    mb.add_arc_pts("primary", (-3.5, -34.2), (4.2, -32.2), 0.8)
    mb.add_arc_pts("detail", (-11.5, -29.2), (-3.2, -32.4), 0.9)
    mb.add_arc_pts("detail", (-3.2, -32.4), (3.8, -30.9), 0.6)

    # Viewer's right brow (foreshortened)
    mb.add_arc_pts("primary", (11.5, -32.2), (17.2, -34.2), 0.9)
    mb.add_arc_pts("primary", (17.2, -34.2), (22.5, -31.2), 0.7)
    mb.add_arc_pts("detail", (11.8, -30.8), (17.2, -32.5), 0.7)
    mb.add_arc_pts("detail", (17.2, -32.5), (22.0, -30.2), 0.5)

    # Canonical eyes on y = -27
    mb.add_canonical_eye(
        -3.2,
        -27.0,
        width=11.4,
        upper_sag=2.6,
        lower_sag=-1.3,
        iris_r=2.3,
        pupil_r=1.1,
        gaze_dx=0.55,
    )
    mb.add_canonical_eye(
        16.5,
        -27.2,
        width=8.6,
        upper_sag=2.3,
        lower_sag=-1.15,
        iris_r=1.95,
        pupil_r=0.95,
        gaze_dx=0.45,
    )
    # Under-eye classical lid folds
    mb.add_arc_pts("detail", (-8.5, -23.5), (2.0, -23.8), -0.9)
    mb.add_arc_pts("detail", (12.4, -24.0), (20.4, -24.0), -0.8)

    # --- CLASSICAL GREEK NOSE & CHEEK PLANES ---
    mb.add_arc_pts("primary", (7.8, -32.0), (10.0, -23.8), -0.5)
    mb.add_arc_pts("primary", (10.0, -23.8), (12.8, -16.2), -0.4)
    mb.add_arc_pts("primary", (12.8, -16.2), (14.4, -12.8), 0.6)
    mb.add_arc_pts("primary", (14.4, -12.8), (12.2, -10.8), 0.9)
    mb.add_arc_pts("primary", (12.2, -10.8), (7.6, -11.0), 0.5)
    mb.add_arc_pts("primary", (7.6, -11.0), (5.0, -12.4), 0.5)
    # Left nostril wing C-curve
    mb.add_arc_pts("primary", (5.0, -12.4), (4.6, -14.8), 0.65)
    mb.add_arc_pts("primary", (4.6, -14.8), (7.0, -15.4), 0.45)
    # Subtle nasal shadow & far nostril
    mb.add_arc_pts("detail", (7.8, -12.0), (10.8, -11.8), -0.4)
    mb.add_arc_pts("detail", (13.8, -12.2), (15.6, -13.6), 0.5)
    mb.add_arc_pts("detail", (5.8, -28.0), (6.8, -20.5), 0.4)
    mb.add_arc_pts("detail", (6.8, -20.5), (6.4, -16.0), -0.3)
    # Cheek & nasolabial folds
    mb.add_arc_pts("detail", (3.6, -14.6), (-2.2, -9.5), -0.8)
    mb.add_arc_pts("detail", (-15.2, -21.0), (-12.8, -12.2), 0.9)

    # --- FULL MUSTACHE, MOUTH & ROUNDED HELLENISTIC BEARD ---
    # Sweeping upper mustache wings
    mb.add_arc_pts("primary", (9.5, -9.4), (2.2, -8.2), -1.2)
    mb.add_arc_pts("primary", (2.2, -8.2), (-4.2, -3.5), -1.3)
    mb.add_arc_pts("primary", (-4.2, -3.5), (-7.8, 3.8), -1.0)

    mb.add_arc_pts("primary", (9.5, -9.4), (16.5, -8.2), 1.1)
    mb.add_arc_pts("primary", (16.5, -8.2), (21.6, -4.0), 1.2)
    mb.add_arc_pts("primary", (21.6, -4.0), (24.8, 1.5), 0.8)

    # Inner mustache arch framing mouth
    mb.add_arc_pts("primary", (9.5, -6.4), (3.8, -5.2), -0.8)
    mb.add_arc_pts("primary", (3.8, -5.2), (-0.5, -1.2), -0.9)
    mb.add_arc_pts("primary", (-0.5, -1.2), (-3.2, 4.2), -0.6)

    mb.add_arc_pts("primary", (9.5, -6.4), (15.0, -5.2), 0.8)
    mb.add_arc_pts("primary", (15.0, -5.2), (19.0, -1.2), 0.8)
    mb.add_arc_pts("primary", (19.0, -1.2), (21.2, 3.4), 0.5)

    # Mustache interior wave texture
    mb.add_arc_pts("detail", (7.2, -8.0), (-2.5, -2.5), -1.1)
    mb.add_arc_pts("detail", (12.2, -7.8), (20.5, -2.2), 1.0)

    # Calm mouth & lower lip
    mb.add_arc_pts("primary", (3.6, -3.2), (9.8, -3.8), 0.4)
    mb.add_arc_pts("primary", (9.8, -3.8), (15.6, -3.1), 0.4)
    mb.add_arc_pts("primary", (4.8, -0.8), (9.8, 0.4), -0.8)
    mb.add_arc_pts("primary", (9.8, 0.4), (14.6, -0.8), -0.7)
    mb.add_arc_pts("detail", (6.8, 2.0), (12.8, 1.8), -0.5)

    # Left cheek-to-beard transition line
    mb.add_arc_pts("detail", (-19.8, -13.5), (-15.2, -7.8), -0.9)
    mb.add_arc_pts("detail", (-15.2, -7.8), (-10.2, -2.2), -0.8)
    mb.add_arc_pts("detail", (-10.2, -2.2), (-7.0, 3.2), -0.6)

    # Full rounded Hellenistic philosopher's beard outer contour
    mb.add_arc_pts("primary", (-21.0, -10.5), (-22.6, -1.0), -1.1)
    mb.add_arc_pts("primary", (-22.6, -1.0), (-21.0, 9.5), -1.4)
    mb.add_arc_pts("primary", (-21.0, 9.5), (-15.5, 18.8), -1.6)
    mb.add_arc_pts("primary", (-15.5, 18.8), (-5.5, 25.0), -1.5)
    mb.add_arc_pts("primary", (-5.5, 25.0), (5.5, 27.6), -1.3)
    mb.add_arc_pts("primary", (5.5, 27.6), (14.8, 25.0), -1.3)
    mb.add_arc_pts("primary", (14.8, 25.0), (21.8, 18.0), -1.5)
    mb.add_arc_pts("primary", (21.8, 18.0), (25.2, 9.0), -1.3)
    mb.add_arc_pts("primary", (25.2, 9.0), (25.2, 0.8), -0.9)
    mb.add_arc_pts("primary", (25.2, 0.8), (22.8, -8.5), -0.8)

    # Sculpted Euclid III.12 tangent wave strands filling the rounded beard
    mb.add_wave("detail", (-19.2, -7.5), (-16.2, 14.5), 3, wave_angle_deg + 4.0, 1)
    mb.add_wave("detail", (-15.0, -3.5), (-11.5, 20.5), 4, wave_angle_deg + 2.0, -1)
    mb.add_wave("detail", (-10.0, 1.5), (-6.2, 23.8), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (-4.5, 4.0), (-0.8, 25.8), 4, wave_angle_deg - 2.0, -1)
    mb.add_wave("detail", (1.2, 3.8), (4.6, 26.5), 4, wave_angle_deg - 2.0, 1)
    mb.add_wave("detail", (7.0, 3.5), (9.8, 25.5), 4, wave_angle_deg - 2.0, -1)
    mb.add_wave("detail", (12.8, 3.2), (14.8, 23.0), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (18.2, 2.5), (19.8, 17.5), 3, wave_angle_deg + 2.0, -1)
    mb.add_wave("detail", (22.2, 2.0), (23.0, 12.0), 2, wave_angle_deg + 4.0, 1)

    # --- NECK & CLASSICAL GREEK CHITON / HIMATION DRAPERY ---
    # Smooth sculpted neck-to-trapezius transitions descending from behind beard
    mb.add_arc_pts("primary", (-20.4, 11.2), (-29.5, 26.8), 1.6)
    mb.add_arc_pts("primary", (21.6, 18.2), (29.8, 28.8), -1.4)
    mb.add_arc_pts("detail", (-16.2, 19.5), (-20.8, 28.5), 0.9)
    mb.add_arc_pts("detail", (17.2, 24.5), (21.5, 31.2), -0.8)

    # Broad classical shoulders sweeping cleanly to MED_R
    mb.add_arc_pts("primary", (-29.5, 26.8), (-73.0, 62.5), -8.8)
    mb.add_arc_pts("primary", (29.8, 28.8), (72.0, 63.5), 8.6)

    # Seamless Greek chiton curved neckline & inner double-hem trim
    mb.add_arc_pts("primary", (-27.8, 27.2), (28.8, 28.8), -13.6)
    mb.add_arc_pts("detail", (-25.5, 29.8), (26.8, 31.5), -13.0)

    # Fluid single-arc himation diagonal mantle draped across the chest
    mb.add_arc_pts("primary", (-35.5, 29.5), (38.0, 80.5), -9.2)
    mb.add_arc_pts("primary", (-44.5, 33.8), (14.5, 88.0), -8.6)

    # Outer left cloak vertical fall & right tunic drape grounded cleanly to rim
    mb.add_arc_pts("primary", (-54.8, 40.5), (-46.5, 84.5), -4.2)
    mb.add_arc_pts("primary", (40.5, 33.8), (47.5, 81.5), 3.8)

    # Refined classical marble drapery detail folds (single continuous curves)
    mb.add_arc_pts("detail", (-39.8, 32.8), (26.0, 84.5), -8.8)
    mb.add_arc_pts("detail", (-31.5, 57.5), (-25.5, 85.5), -1.5)
    mb.add_arc_pts("detail", (-45.8, 50.5), (-39.0, 82.5), -1.8)
    mb.add_arc_pts("detail", (-62.0, 50.0), (-58.0, 74.5), -1.5)
    mb.add_arc_pts("detail", (10.5, 48.0), (29.5, 67.5), -1.8)
    mb.add_arc_pts("detail", (24.5, 41.0), (36.5, 74.5), 1.8)
    mb.add_arc_pts("detail", (53.0, 44.5), (56.8, 73.5), 1.6)

    return mb.build()


def build_heron_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Heron of Alexandria medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_heron_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_heron_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``heron_dark.svg`` and ``heron_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "heron_dark.svg"
    light_path = target_dir / "heron_light.svg"
    dark_path.write_text(
        build_heron_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_heron_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
