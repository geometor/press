"""Study 30: Karl Georg Christian von Staudt (after the 19th-century archival studio portrait)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_staudt_elements",
    "build_staudt_svg",
    "write_staudt_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _intersect_lines(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> tuple[float, float]:
    """Compute the exact intersection of lines ``p1-p2`` and ``p3-p4``."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-9:
        return (0.5 * (x1 + x3), 0.5 * (y1 + y3))
    det1 = x1 * y2 - y1 * x2
    det2 = x3 * y4 - y3 * x4
    px = (det1 * (x3 - x4) - (x1 - x2) * det2) / denom
    py = (det1 * (y3 - y4) - (y1 - y2) * det2) / denom
    return (px, py)


def _add_harmonic_quadrangle_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw von Staudt's Complete Quadrangle Harmonic Conjugate ``H(A, B; C, D)``.

    Constructs the purely projective non-metric harmonic throw: base line
    ``A-C-B-D``, external vertex ``P`` with rays ``PA, PB, PC``, interior point
    ``S`` on ``PC``, quadrangle vertices ``Q = AS ∩ PB`` and ``R = BS ∩ PA``,
    and the opposite side ``RQ`` meeting the base line at the exact fourth
    harmonic conjugate ``D``.
    """
    y_base = cy + 9.0
    pt_a = (cx - 13.5, y_base)
    pt_b = (cx + 2.5, y_base)
    # Exact internal point C dividing AB in ratio 27:11 so harmonic conjugate D = cx + 13.5
    pt_c = (cx - 81.0 / 38.0, y_base)
    pt_p = (cx - 6.0, cy - 12.8)
    pt_s = (
        pt_p[0] + 0.48 * (pt_c[0] - pt_p[0]),
        pt_p[1] + 0.48 * (pt_c[1] - pt_p[1]),
    )
    pt_q = _intersect_lines(pt_a, pt_s, pt_p, pt_b)
    pt_r = _intersect_lines(pt_b, pt_s, pt_p, pt_a)
    pt_d = _intersect_lines(pt_r, pt_q, pt_a, pt_b)

    # Projective base line A-C-B-D
    mb.add_line("golden", pt_a[0] - 0.8, y_base, pt_d[0] + 0.8, y_base)
    # Complete quadrangle rays & diagonals
    mb.add_line("golden", pt_p[0], pt_p[1], pt_a[0], pt_a[1])
    mb.add_line("golden", pt_p[0], pt_p[1], pt_b[0], pt_b[1])
    mb.add_line("golden", pt_p[0], pt_p[1], pt_c[0], pt_c[1])
    mb.add_line("golden", pt_a[0], pt_a[1], pt_q[0], pt_q[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_r[0], pt_r[1])
    mb.add_line("golden", pt_r[0], pt_r[1], pt_d[0], pt_d[1])

    # Four harmonic base nodes A, C, B, D (filled) & quadrangle vertices P, Q, R, S (open)
    for vx, vy in (pt_a, pt_c, pt_b, pt_d):
        mb.add_circle("golden", vx, vy, 0.8, filled=True)
    for vx, vy in (pt_p, pt_q, pt_r, pt_s):
        mb.add_circle("golden", vx, vy, 0.56)


def _add_pole_polar_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw von Staudt's Pole-and-Polar Circle Involution in the right margin.

    Constructs the reference conic/circle, external pole ``P``, exact tangent
    lines to ``T1`` and ``T2``, the extended polar line ``T1-T2``, and an
    oblique secant through ``P`` intersecting the circle at ``U, V`` and the
    polar at ``W`` in exact harmonic involution ``H(U, V; W, P) = -1``.
    """
    ox, oy = cx - 4.4, cy
    radius = 8.2
    px, py = cx + 12.6, cy
    dist_op = px - ox

    # Exact tangent points T1, T2 from external pole P to circle (O, r)
    cos_a = radius / dist_op
    sin_a = math.sqrt(max(0.0, 1.0 - cos_a * cos_a))
    t1 = (ox + radius * cos_a, oy - radius * sin_a)
    t2 = (ox + radius * cos_a, oy + radius * sin_a)

    # Reference conic/circle & subtle center node
    mb.add_circle("golden", ox, oy, radius)
    mb.add_circle("golden", ox, oy, 0.55, filled=True)

    # External pole P, tangents P-T1 & P-T2, and extended polar line T1-T2
    mb.add_line("golden", px, py, t1[0], t1[1])
    mb.add_line("golden", px, py, t2[0], t2[1])
    mb.add_line("golden", t1[0], t1[1] - 3.2, t2[0], t2[1] + 3.2)

    # Oblique harmonic secant through P cutting upper circle interior at U, V & polar at W
    sec_rad = math.radians(190.5)
    dx, dy = math.cos(sec_rad), math.sin(sec_rad)
    # Solve |(P + t*d) - O|^2 = r^2
    rx, ry = px - ox, py - oy
    b_coef = 2.0 * (rx * dx + ry * dy)
    c_coef = rx * rx + ry * ry - radius * radius
    disc = math.sqrt(max(0.0, b_coef * b_coef - 4.0 * c_coef))
    t_near = 0.5 * (-b_coef - disc)
    t_far = 0.5 * (-b_coef + disc)
    pt_v = (px + t_near * dx, py + t_near * dy)
    pt_u = (px + t_far * dx, py + t_far * dy)
    t_pol = (t1[0] - px) / dx
    pt_w = (t1[0], py + t_pol * dy)

    mb.add_line("golden", px, py, pt_u[0], pt_u[1])

    # Marked pole P, tangent points T1, T2, and harmonic secant nodes U, V, W
    mb.add_circle("golden", px, py, 0.88, filled=True)
    for vx, vy in (t1, t2, pt_u, pt_v):
        mb.add_circle("golden", vx, vy, 0.68, filled=True)
    mb.add_circle("golden", pt_w[0], pt_w[1], 0.8)


def build_staudt_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Karl Georg Christian von Staudt.

    Calibrated to the 19th-century Erlangen archival portrait: windswept curly
    silver hair rising over a broad brow, keen eyes on ``y = -27``, firm
    composed mouth, distinctive chinstrap/mutton-chop beard leaving the chin
    clean, wide silk bow tie over wing collar and pale waistcoat, and broad
    notched coat lapels grounded smoothly to ``MED_R = 92.0``. Margin motifs
    show von Staudt's Complete Quadrangle Harmonic Conjugate (left) and
    Pole-and-Polar Circle Involution (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-6.0,
        eye_rx=12.8,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN PROJECTIVE MARGIN MOTIFS (open margins, zero face crossing) ---
    _add_harmonic_quadrangle_motif(mb, cx=-63.0, cy=-26.0)
    _add_pole_polar_motif(mb, cx=63.0, cy=-26.0)

    # --- WINDSWEPT SILVER CURLY HAIR & CROWN ---
    # Lively windswept outer hair silhouette
    mb.add_arc_pts("primary", (-26.5, -24.0), (-29.2, -33.2), 1.6)
    mb.add_arc_pts("primary", (-29.2, -33.2), (-26.2, -42.5), 1.4)
    mb.add_arc_pts("primary", (-26.2, -42.5), (-27.0, -49.5), 1.5)
    mb.add_arc_pts("primary", (-27.0, -49.5), (-19.5, -56.8), 1.8)
    mb.add_arc_pts("primary", (-19.5, -56.8), (-9.5, -60.5), 1.6)
    mb.add_arc_pts("primary", (-9.5, -60.5), (3.5, -63.8), 1.9)
    mb.add_arc_pts("primary", (3.5, -63.8), (14.8, -60.5), 1.8)
    mb.add_arc_pts("primary", (14.8, -60.5), (22.0, -53.8), 1.6)
    mb.add_arc_pts("primary", (22.0, -53.8), (25.8, -45.0), 1.5)
    mb.add_arc_pts("primary", (25.8, -45.0), (26.2, -36.5), 1.2)
    mb.add_arc_pts("primary", (26.2, -36.5), (24.5, -28.0), 0.9)

    # Broad intelligent forehead hairline
    mb.add_arc_pts("primary", (-19.5, -27.5), (-19.0, -37.5), 1.1)
    mb.add_arc_pts("primary", (-19.0, -37.5), (-13.8, -46.2), 1.3)
    mb.add_arc_pts("primary", (-13.8, -46.2), (-3.5, -50.2), 1.4)
    mb.add_arc_pts("primary", (-3.5, -50.2), (8.2, -50.8), 1.3)
    mb.add_arc_pts("primary", (8.2, -50.8), (17.5, -46.2), 1.2)
    mb.add_arc_pts("primary", (17.5, -46.2), (21.8, -37.8), 1.0)
    mb.add_arc_pts("primary", (21.8, -37.8), (22.0, -29.0), 0.7)

    # Sweeping Euclid III.12 curly silver hair texture
    mb.add_wave("detail", (-24.5, -34.0), (-11.5, -56.0), 4, wave_angle_deg + 8.0, 1)
    mb.add_wave("detail", (-16.5, -51.5), (14.5, -56.5), 5, wave_angle_deg + 6.0, -1)
    mb.add_wave("detail", (-6.0, -55.5), (20.5, -49.0), 4, wave_angle_deg + 6.0, 1)
    mb.add_wave("detail", (16.5, -52.5), (24.0, -34.0), 3, wave_angle_deg + 8.0, -1)
    mb.add_arc_pts("detail", (-25.5, -44.0), (-19.0, -49.5), 1.3)

    # Subtle horizontal forehead furrows
    mb.add_arc_pts("detail", (-9.5, -43.2), (13.8, -42.8), 0.9)
    mb.add_arc_pts("detail", (-11.0, -38.8), (15.2, -38.6), 0.8)

    # --- LEFT EAR (VIEWER'S LEFT) ---
    mb.add_arc_pts("primary", (-22.0, -25.2), (-26.8, -22.2), -1.3)
    mb.add_arc_pts("primary", (-26.8, -22.2), (-25.8, -14.5), -1.3)
    mb.add_arc_pts("primary", (-25.8, -14.5), (-21.8, -11.5), -1.0)
    mb.add_arc_pts("detail", (-23.2, -22.5), (-24.4, -15.8), -0.9)

    # --- FACE CONTOUR & 19TH-CENTURY CHINSTRAP / MUTTON-CHOP WHISKERS ---
    # Outer face & whisker jawline silhouette
    mb.add_arc_pts("primary", (-21.8, -11.5), (-22.4, -3.5), -1.1)
    mb.add_arc_pts("primary", (-22.4, -3.5), (-17.2, 3.0), -1.4)
    mb.add_arc_pts("primary", (-17.2, 3.0), (-6.5, 6.8), -1.5)
    mb.add_arc_pts("primary", (-6.5, 6.8), (5.5, 7.2), -1.2)
    mb.add_arc_pts("primary", (5.5, 7.2), (15.5, 3.5), -1.4)
    mb.add_arc_pts("primary", (15.5, 3.5), (21.5, -4.5), -1.3)
    mb.add_arc_pts("primary", (21.5, -4.5), (24.4, -15.5), -1.1)
    mb.add_arc_pts("primary", (24.4, -15.5), (24.5, -28.0), -0.8)

    # Inner whisker contour leaving cheeks, upper lip & chin clean-shaven
    mb.add_arc_pts("detail", (-19.5, -27.5), (-16.8, -17.5), -0.8)
    mb.add_arc_pts("detail", (-16.8, -17.5), (-15.0, -8.5), -0.8)
    mb.add_arc_pts("detail", (-15.0, -8.5), (-9.5, -0.5), -0.9)
    mb.add_arc_pts("detail", (-9.5, -0.5), (4.5, 3.6), -1.2)
    mb.add_arc_pts("detail", (4.5, 3.6), (14.5, -0.5), -1.0)
    mb.add_arc_pts("detail", (14.5, -0.5), (18.8, -9.5), -0.8)
    mb.add_arc_pts("detail", (18.8, -9.5), (21.5, -19.5), -0.7)
    mb.add_arc_pts("detail", (21.5, -19.5), (22.0, -29.0), -0.5)

    # Crisp short wavy mutton-chop & chinstrap whisker texture
    mb.add_wave("detail", (-19.5, -11.5), (-14.5, 1.5), 3, wave_angle_deg + 4.0, 1)
    mb.add_wave("detail", (-13.5, 0.5), (-1.5, 5.2), 3, wave_angle_deg + 2.0, -1)
    mb.add_wave("detail", (2.5, 5.4), (14.5, 1.2), 3, wave_angle_deg + 2.0, 1)
    mb.add_wave("detail", (17.5, -1.5), (21.8, -14.5), 3, wave_angle_deg + 4.0, -1)

    # --- EYEBROWS & KEEN CANONICAL EYES ON y = -27 ---
    mb.add_arc_pts("primary", (-13.6, -31.8), (-5.5, -34.2), 1.0)
    mb.add_arc_pts("primary", (-5.5, -34.2), (1.8, -31.4), 0.7)
    mb.add_arc_pts("detail", (-12.5, -30.5), (1.0, -30.4), 1.3)

    mb.add_arc_pts("primary", (7.4, -31.4), (14.2, -34.5), 0.9)
    mb.add_arc_pts("primary", (14.2, -34.5), (20.5, -32.2), 0.7)
    mb.add_arc_pts("detail", (8.2, -30.2), (19.6, -31.0), 1.2)

    mb.add_canonical_eye(
        -6.0,
        -27.0,
        width=10.8,
        upper_sag=2.35,
        lower_sag=-1.15,
        iris_r=2.15,
        pupil_r=1.05,
        gaze_dx=0.35,
    )
    mb.add_canonical_eye(
        12.8,
        -27.2,
        width=9.2,
        upper_sag=2.2,
        lower_sag=-1.1,
        iris_r=2.0,
        pupil_r=1.0,
        gaze_dx=0.25,
    )
    # Under-eye character creases
    mb.add_arc_pts("detail", (-11.2, -23.6), (-1.0, -23.9), -0.8)
    mb.add_arc_pts("detail", (8.4, -23.9), (17.2, -24.1), -0.75)

    # --- CHARACTERFUL NOSE & FIRM COMPOSED MOUTH ---
    mb.add_arc_pts("primary", (4.5, -31.5), (5.8, -23.5), -0.45)
    mb.add_arc_pts("primary", (5.8, -23.5), (7.8, -17.4), -0.4)
    mb.add_arc_pts("primary", (7.8, -17.4), (8.6, -14.8), 0.55)
    mb.add_arc_pts("primary", (8.6, -14.8), (6.5, -13.2), 0.8)
    mb.add_arc_pts("primary", (6.5, -13.2), (2.0, -13.4), 0.45)
    mb.add_arc_pts("primary", (2.0, -13.4), (-0.4, -14.8), 0.45)
    # Left nostril wing C-curve
    mb.add_arc_pts("primary", (-0.4, -14.8), (-0.6, -16.8), 0.6)
    mb.add_arc_pts("primary", (-0.6, -16.8), (1.8, -17.3), 0.4)
    # Far nostril & bridge shadow
    mb.add_arc_pts("detail", (8.4, -14.5), (10.2, -16.0), 0.55)
    mb.add_arc_pts("detail", (10.2, -16.0), (8.6, -17.4), 0.4)
    mb.add_arc_pts("detail", (2.5, -27.5), (3.0, -20.5), 0.35)
    # Nasolabial character creases
    mb.add_arc_pts("detail", (-1.5, -15.8), (-7.2, -8.5), -0.8)
    mb.add_arc_pts("detail", (11.2, -16.2), (14.4, -9.2), 0.75)

    # Firm composed mouth & clean chin cleft
    mb.add_arc_pts("detail", (-3.8, -9.0), (3.8, -9.7), 0.4)
    mb.add_arc_pts("detail", (3.8, -9.7), (10.6, -9.0), 0.4)
    mb.add_arc_pts("primary", (-4.8, -7.8), (3.8, -8.0), 0.3)
    mb.add_arc_pts("primary", (3.8, -8.0), (11.8, -7.8), 0.3)
    mb.add_arc_pts("primary", (-2.4, -5.5), (3.8, -4.6), -0.75)
    mb.add_arc_pts("primary", (3.8, -4.6), (9.6, -5.5), -0.7)
    mb.add_arc_pts("detail", (0.5, -2.2), (6.8, -2.2), -0.45)

    # --- WHITE WING COLLAR, WIDE BOW TIE, WAISTCOAT & 19TH-C. COAT ---
    # White wing collar tips framing the bow tie
    mb.add_arc_pts("primary", (-12.5, 5.2), (-9.2, 16.0), 0.9)
    mb.add_arc_pts("primary", (-9.2, 16.0), (-3.8, 12.2), -0.5)
    mb.add_arc_pts("primary", (16.2, 3.2), (19.0, 14.8), -0.9)
    mb.add_arc_pts("primary", (19.0, 14.8), (12.5, 11.8), 0.5)

    # Wide dark 19th-century bow tie
    # Central knot
    mb.add_arc_pts("primary", (0.5, 12.2), (7.5, 12.0), 0.6)
    mb.add_arc_pts("primary", (7.5, 12.0), (7.0, 18.5), 0.6)
    mb.add_arc_pts("primary", (7.0, 18.5), (1.0, 18.6), 0.5)
    mb.add_arc_pts("primary", (1.0, 18.6), (0.5, 12.2), 0.6)
    # Left bow wing
    mb.add_arc_pts("primary", (0.5, 12.2), (-6.8, 14.5), 1.0)
    mb.add_arc_pts("primary", (-6.8, 14.5), (-8.2, 21.5), -1.1)
    mb.add_arc_pts("primary", (-8.2, 21.5), (1.0, 18.6), -0.9)
    mb.add_arc_pts("detail", (-5.2, 17.5), (0.2, 15.8), 0.5)
    # Right bow wing
    mb.add_arc_pts("primary", (7.5, 12.0), (15.2, 11.8), 1.0)
    mb.add_arc_pts("primary", (15.2, 11.8), (15.8, 19.2), 1.1)
    mb.add_arc_pts("primary", (15.8, 19.2), (7.0, 18.5), 0.9)
    mb.add_arc_pts("detail", (13.8, 15.6), (7.8, 15.4), -0.5)
    # Hanging bow-tie tails
    mb.add_arc_pts("primary", (-2.2, 19.8), (-5.2, 25.0), 0.5)
    mb.add_arc_pts("primary", (-5.2, 25.0), (0.6, 24.0), -0.4)
    mb.add_arc_pts("primary", (0.6, 24.0), (2.2, 18.6), 0.4)
    mb.add_arc_pts("primary", (7.6, 18.5), (12.2, 24.8), -0.5)
    mb.add_arc_pts("primary", (12.2, 24.8), (7.0, 24.6), 0.4)
    mb.add_arc_pts("primary", (7.0, 24.6), (5.8, 18.6), -0.4)

    # Pale V-neck waistcoat & crisp shirt front
    mb.add_arc_pts("primary", (-13.5, 14.5), (9.2, 54.0), -2.4)
    mb.add_arc_pts("primary", (19.0, 14.8), (9.2, 54.0), 1.8)
    mb.add_line("detail", 4.5, 25.5, 8.2, 51.0)
    mb.add_arc_pts("detail", (-8.5, 28.5), (8.5, 58.0), -1.5)

    # Broad 19th-century shoulders joined flush at coat collar & sweeping to MED_R
    mb.add_arc_pts("primary", (-18.5, 5.2), (-75.0, 58.0), -11.5)
    mb.add_arc_pts("primary", (21.5, 5.2), (63.5, 68.5), 10.5)
    # Short back-collar connections closing cleanly behind the jaw
    mb.add_arc_pts("primary", (-18.5, 5.2), (-15.5, 3.8), -0.3)
    mb.add_arc_pts("primary", (21.5, 5.2), (16.5, 2.8), 0.4)

    # Tailored left coat collar & notched lapel
    mb.add_arc_pts("primary", (-18.5, 5.2), (-27.5, 24.5), 1.4)
    mb.add_arc_pts("primary", (-27.5, 24.5), (-22.0, 27.2), -0.4)
    mb.add_arc_pts("primary", (-22.0, 27.2), (-29.2, 32.5), -0.6)
    mb.add_arc_pts("primary", (-29.2, 32.5), (12.0, 62.5), -2.4)
    mb.add_arc_pts("primary", (12.0, 62.5), (15.5, 85.0), 1.2)
    mb.add_arc_pts("detail", (-14.5, 11.0), (-12.5, 24.5), 0.8)

    # Tailored right coat collar & notched lapel
    mb.add_arc_pts("primary", (21.5, 5.2), (34.2, 22.0), -1.4)
    mb.add_arc_pts("primary", (34.2, 22.0), (29.2, 25.8), 0.4)
    mb.add_arc_pts("primary", (29.2, 25.8), (35.5, 31.2), 0.6)
    mb.add_arc_pts("primary", (35.5, 31.2), (21.0, 60.5), 1.8)
    mb.add_arc_pts("primary", (21.0, 60.5), (18.8, 84.5), 0.9)

    # Streamlined sleeve seams & tailored wool coat folds (detail)
    mb.add_arc_pts("detail", (-44.5, 26.5), (-52.5, 76.5), -4.2)
    mb.add_arc_pts("detail", (-28.5, 44.5), (-27.5, 83.0), -1.6)
    mb.add_arc_pts("detail", (40.5, 30.5), (47.5, 76.5), 3.6)
    mb.add_arc_pts("detail", (31.5, 48.5), (33.5, 82.0), 1.6)

    return mb.build()


def build_staudt_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Karl G. C. von Staudt medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_staudt_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_staudt_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``staudt_dark.svg`` and ``staudt_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "staudt_dark.svg"
    light_path = target_dir / "staudt_light.svg"
    dark_path.write_text(
        build_staudt_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_staudt_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
