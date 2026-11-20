"""Study 32: John Casey (after the 19th-century Irish studio portrait)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_casey_elements",
    "build_casey_svg",
    "write_casey_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _external_tangent_segment(
    c1: tuple[float, float, float],
    c2: tuple[float, float, float],
    side: float = 1.0,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return exact endpoints of an external common tangent between circles ``c1`` and ``c2``.

    ``side`` (``+1.0`` or ``-1.0``) selects which of the two external common
    tangents is returned relative to the directed center-to-center vector.
    """
    x1, y1, r1 = c1
    x2, y2, r2 = c2
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    cos_beta = max(-1.0, min(1.0, (r1 - r2) / max(dist, 1e-9)))
    alpha = math.atan2(dy, dx)
    beta = math.acos(cos_beta)
    phi = alpha + side * beta
    p1 = (x1 + r1 * math.cos(phi), y1 + r1 * math.sin(phi))
    p2 = (x2 + r2 * math.cos(phi), y2 + r2 * math.sin(phi))
    return (p1, p2)


def _add_caseys_theorem_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Casey's Theorem in the open left margin.

    Constructs an enclosing circle ``O`` with four unequal, non-overlapping
    circles ``C1..C4`` strictly internally tangent to ``O``, along with the
    cyclic external common tangent chords ``t12, t23, t34, t41`` and diagonals
    ``t13, t24`` satisfying ``t12*t34 + t23*t41 = t13*t24``.
    """
    outer_r = 12.6
    mb.add_circle("golden", cx, cy, outer_r)

    # Four unequal circles strictly internally tangent to O at well-spaced angles
    specs: list[tuple[float, float]] = [
        (-142.0, 3.1),
        (-44.0, 4.1),
        (36.0, 2.8),
        (134.0, 3.7),
    ]
    circles: list[tuple[float, float, float]] = []
    for ang_deg, rad_i in specs:
        rad = math.radians(ang_deg)
        cix = cx + (outer_r - rad_i) * math.cos(rad)
        ciy = cy + (outer_r - rad_i) * math.sin(rad)
        circles.append((cix, ciy, rad_i))
        mb.add_circle("golden", cix, ciy, rad_i)
        # Exact internal tangency point on enclosing circle O
        tx = cx + outer_r * math.cos(rad)
        ty = cy + outer_r * math.sin(rad)
        mb.add_circle("golden", tx, ty, 0.56, filled=True)

    # Cyclic external common tangent sides (t12, t23, t34, t41) on outer rim side
    for idx in range(4):
        c_a = circles[idx]
        c_b = circles[(idx + 1) % 4]
        p1, p2 = _external_tangent_segment(c_a, c_b, side=-1.0)
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # External common tangent diagonals (t13, t24) crossing inside O
    for i_idx, j_idx, side in ((0, 2, -1.0), (1, 3, -1.0)):
        p1, p2 = _external_tangent_segment(circles[i_idx], circles[j_idx], side=side)
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])


def _add_radical_orthogonal_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Casey's Sequel motif: intersecting circles, radical axis, and orthogonal circle.

    Constructs two intersecting circles ``S1`` and ``S2``, their exact radical
    axis through intersections ``P`` and ``Q``, a pole ``K`` on the radical
    axis, and the exact orthogonal circle centered at ``K`` cutting both
    ``S1`` and ``S2`` at right angles at tangency points ``T1`` and ``T2``.
    """
    o1 = (cx - 4.4, cy + 3.8)
    r1 = 7.8
    o2 = (cx + 5.2, cy + 3.8)
    r2 = 6.2
    dist = o2[0] - o1[0]

    # Exact radical axis x-coordinate and intersection points P, Q
    x_rad = o1[0] + (dist * dist + r1 * r1 - r2 * r2) / (2.0 * dist)
    dy_int = math.sqrt(max(0.0, r1 * r1 - (x_rad - o1[0]) ** 2))
    pt_p = (x_rad, o1[1] - dy_int)
    pt_q = (x_rad, o1[1] + dy_int)

    # Pole K on the radical axis & exact orthogonal circle radius (equal tangent length)
    pole_k = (x_rad, cy - 5.2)
    r_orth = math.sqrt(
        max(0.0, (pole_k[0] - o1[0]) ** 2 + (pole_k[1] - o1[1]) ** 2 - r1 * r1)
    )

    # Exact tangency points T1 on S1 and T2 on S2 (where orthogonal circle cuts at 90 deg)
    def _circle_intersections(
        ca: tuple[float, float],
        ra: float,
        cb: tuple[float, float],
        rb: float,
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        dx, dy = cb[0] - ca[0], cb[1] - ca[1]
        d_ab = math.hypot(dx, dy)
        a_len = (ra * ra - rb * rb + d_ab * d_ab) / (2.0 * d_ab)
        h_len = math.sqrt(max(0.0, ra * ra - a_len * a_len))
        mx = ca[0] + a_len * dx / d_ab
        my = ca[1] + a_len * dy / d_ab
        rx, ry = -dy * h_len / d_ab, dx * h_len / d_ab
        return ((mx + rx, my + ry), (mx - rx, my - ry))

    t1_a, t1_b = _circle_intersections(pole_k, r_orth, o1, r1)
    t1 = t1_a if t1_a[0] < t1_b[0] else t1_b
    t2_a, t2_b = _circle_intersections(pole_k, r_orth, o2, r2)
    t2 = t2_a if t2_a[0] > t2_b[0] else t2_b

    # Base intersecting circles S1, S2 and orthogonal circle around K
    mb.add_circle("golden", o1[0], o1[1], r1)
    mb.add_circle("golden", o2[0], o2[1], r2)
    mb.add_circle("golden", pole_k[0], pole_k[1], r_orth)

    # Radical axis through P, Q, and K, plus orthogonal tangent rays K-T1 and K-T2
    mb.add_line("golden", x_rad, pole_k[1] - r_orth - 1.0, x_rad, pt_q[1] + 3.4)
    mb.add_line("golden", pole_k[0], pole_k[1], t1[0], t1[1])
    mb.add_line("golden", pole_k[0], pole_k[1], t2[0], t2[1])
    mb.add_line("golden", o1[0], o1[1], t1[0], t1[1])
    mb.add_line("golden", o2[0], o2[1], t2[0], t2[1])

    # Canonical nodes: intersections P, Q, orthogonal cuts T1, T2, and center K
    for px, py in (pt_p, pt_q, t1, t2):
        mb.add_circle("golden", px, py, 0.58, filled=True)
    mb.add_circle("golden", pole_k[0], pole_k[1], 0.72)


def build_casey_elements(wave_angle_deg: float = 28.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of John Casey.

    Calibrated to the 19th-century Irish studio portrait: dignified three-quarter
    right-facing scholarly head with high smooth forehead, neatly combed
    side-swept hair, fine Victorian sideburns along the jaw, steady resolute
    eyes on ``y = -27``, strong nose and firm composed mouth, crisp standing
    white collar, folded silk necktie with oval tiepin over a buttoned waistcoat,
    and tailored Victorian coat lapels sweeping smoothly down to ``MED_R = 92.0``.
    Margin motifs display Casey's Theorem (left) and Orthogonal Radical Circles
    (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-9.5,
        eye_rx=13.5,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN CASEY MARGIN MOTIFS (open margins, zero face crossing) ---
    _add_caseys_theorem_motif(mb, cx=-63.5, cy=-26.0)
    _add_radical_orthogonal_motif(mb, cx=63.5, cy=-26.0)

    # --- HIGH SCHOLARLY FOREHEAD, CRANIUM & SIDE-SWEPT HAIR ---
    # Smooth outer cranium & back-left hair contour
    mb.add_arc_pts("primary", (-24.0, -28.0), (-26.5, -40.5), 1.4)
    mb.add_arc_pts("primary", (-26.5, -40.5), (-21.0, -53.5), 1.8)
    mb.add_arc_pts("primary", (-21.0, -53.5), (-7.0, -62.5), 2.4)
    mb.add_arc_pts("primary", (-7.0, -62.5), (9.5, -60.5), 2.2)
    mb.add_arc_pts("primary", (9.5, -60.5), (19.5, -51.5), 1.8)
    mb.add_arc_pts("primary", (19.5, -51.5), (23.2, -39.5), 1.2)

    # Receding high-forehead hairline sweeping naturally from ear to crown
    mb.add_arc_pts("primary", (-23.5, -27.5), (-20.8, -39.5), 0.8)
    mb.add_arc_pts("detail", (-20.8, -39.5), (-12.5, -49.5), 1.2)
    mb.add_arc_pts("detail", (-12.5, -49.5), (1.5, -55.8), 1.1)
    mb.add_arc_pts("detail", (1.5, -55.8), (12.0, -54.5), 0.7)

    # Neatly combed side-swept hair texture via Euclid III.12 tangent waves
    mb.add_wave("detail", (-23.8, -38.5), (-14.5, -53.8), 3, wave_angle_deg + 2.0, 1)
    mb.add_wave("detail", (-16.2, -53.0), (4.5, -59.0), 3, wave_angle_deg, -1)
    mb.add_wave("detail", (-22.8, -32.0), (-18.8, -44.0), 3, wave_angle_deg + 4.0, -1)
    mb.add_arc_pts("detail", (-19.2, -46.0), (-6.0, -57.0), 1.0)

    # --- LEFT EAR (VIEWER'S LEFT) ---
    mb.add_arc_pts("primary", (-24.0, -28.0), (-26.8, -22.5), -1.2)
    mb.add_arc_pts("primary", (-26.8, -22.5), (-24.8, -15.5), -1.1)
    mb.add_arc_pts("primary", (-24.8, -15.5), (-20.5, -13.2), -0.9)
    mb.add_arc_pts("detail", (-23.5, -25.0), (-24.2, -17.5), -0.8)

    # --- THREE-QUARTER RIGHT FACE CONTOUR & VICTORIAN SIDEBURNS ---
    mb.add_arc_pts("primary", (23.2, -39.5), (24.0, -31.5), 0.7)
    mb.add_arc_pts("primary", (24.0, -31.5), (22.8, -26.5), -0.5)
    mb.add_arc_pts("primary", (22.8, -26.5), (24.2, -19.0), 0.9)
    mb.add_arc_pts("primary", (24.2, -19.0), (23.0, -10.0), 0.9)
    mb.add_arc_pts("primary", (23.0, -10.0), (20.8, -2.0), 0.8)
    mb.add_arc_pts("primary", (20.8, -2.0), (15.5, 4.5), 1.1)
    mb.add_arc_pts("primary", (15.5, 4.5), (6.5, 7.0), 1.4)
    mb.add_arc_pts("primary", (6.5, 7.0), (-3.5, 4.8), 1.3)
    mb.add_arc_pts("primary", (-3.5, 4.8), (-12.5, -1.5), 1.2)
    mb.add_arc_pts("primary", (-12.5, -1.5), (-20.5, -13.2), 1.2)

    # Fine Victorian sideburns hugging the left cheek/jaw (detail texture)
    mb.add_wave("detail", (-20.0, -25.5), (-14.0, -7.0), 4, wave_angle_deg + 4.0, 1)
    mb.add_wave("detail", (-17.5, -21.0), (-10.8, -3.8), 3, wave_angle_deg + 4.0, -1)
    mb.add_arc_pts("detail", (-15.0, -12.0), (-6.5, 1.5), 0.8)

    # --- DIGNIFIED BROWS & STEADY RESOLUTE EYES ON y = -27 ---
    mb.add_arc_pts("primary", (-2.6, -30.8), (3.8, -33.0), 0.65)
    mb.add_arc_pts("primary", (3.8, -33.0), (10.6, -31.4), 0.5)
    mb.add_arc_pts("detail", (-1.4, -30.1), (9.6, -30.6), 0.65)

    mb.add_arc_pts("primary", (14.6, -31.3), (19.2, -32.6), 0.5)
    mb.add_arc_pts("primary", (19.2, -32.6), (23.0, -31.0), 0.4)
    mb.add_arc_pts("detail", (15.2, -30.5), (22.2, -30.3), 0.55)

    # Steady 3/4-right scholarly gaze right on y = -27
    mb.add_canonical_eye(
        3.2,
        -26.8,
        width=10.0,
        upper_sag=1.78,
        lower_sag=-0.88,
        iris_r=1.95,
        pupil_r=1.02,
        gaze_dx=0.5,
    )
    mb.add_canonical_eye(
        18.2,
        -26.6,
        width=7.4,
        upper_sag=1.55,
        lower_sag=-0.78,
        iris_r=1.65,
        pupil_r=0.90,
        gaze_dx=0.45,
    )

    # --- STRONG NOSE, NASOLABIAL FOLD & FIRM COMPOSED MOUTH ---
    mb.add_arc_pts("primary", (13.4, -29.2), (16.5, -21.5), -0.35)
    mb.add_arc_pts("primary", (16.5, -21.5), (19.6, -15.2), -0.35)
    mb.add_arc_pts("primary", (19.6, -15.2), (19.4, -13.2), 0.55)
    mb.add_arc_pts("primary", (19.4, -13.2), (14.5, -12.4), 0.5)
    mb.add_arc_pts("primary", (14.5, -12.4), (10.8, -13.2), 0.4)
    # Left nostril wing C-curve (viewer's left)
    mb.add_arc_pts("primary", (10.8, -13.2), (10.2, -15.2), 0.55)
    mb.add_arc_pts("primary", (10.2, -15.2), (12.2, -15.8), 0.35)
    # Characteristic dignified nasolabial line
    mb.add_arc_pts("detail", (8.8, -14.2), (2.2, -5.8), -0.8)

    # Firm composed mouth & resolute clean-shaven chin
    mb.add_arc_pts("detail", (8.4, -6.0), (13.2, -6.5), 0.25)
    mb.add_arc_pts("detail", (13.2, -6.5), (17.6, -5.9), 0.22)
    mb.add_arc_pts("primary", (3.2, -3.8), (12.8, -5.1), 0.45)
    mb.add_arc_pts("primary", (12.8, -5.1), (19.8, -4.7), 0.25)
    mb.add_arc_pts("primary", (8.2, -1.6), (14.2, -1.7), -0.45)
    mb.add_arc_pts("primary", (14.2, -1.7), (18.4, -2.5), -0.42)
    mb.add_arc_pts("detail", (10.8, 1.8), (17.2, 1.0), -0.38)

    # --- STANDING WHITE COLLAR, SILK NECKTIE WITH TIEPIN & WAISTCOAT ---
    # Crisp standing white winged collar on viewer's left and peek on right
    mb.add_arc_pts("primary", (-20.8, -3.5), (-21.8, 12.2), -1.1)
    mb.add_arc_pts("primary", (-21.8, 12.2), (-7.8, 15.8), -1.2)
    mb.add_arc_pts("primary", (-7.8, 15.8), (-11.8, 1.5), -0.9)
    mb.add_arc_pts("primary", (17.5, 3.8), (21.2, 9.8), 0.8)
    mb.add_arc_pts("primary", (21.2, 9.8), (14.8, 14.2), 0.7)
    # Dark collar band across throat base
    mb.add_arc_pts("primary", (-7.8, 15.8), (4.5, 16.5), -0.8)
    mb.add_arc_pts("primary", (4.5, 16.5), (16.5, 12.8), -0.9)
    mb.add_arc_pts("detail", (-6.0, 12.8), (14.2, 10.6), -1.0)

    # Folded silk necktie / ascot with crisp Victorian oval tiepin at (4.5, 40.5)
    mb.add_arc_pts("primary", (-7.8, 15.8), (3.8, 38.9), 0.85)
    mb.add_arc_pts("primary", (4.2, 42.2), (-3.8, 72.5), 1.3)
    mb.add_arc_pts("primary", (15.5, 13.5), (22.5, 86.0), 2.4)
    mb.add_arc_pts("detail", (1.2, 16.2), (10.8, 41.0), 0.8)
    mb.add_arc_pts("detail", (10.8, 41.0), (14.8, 84.0), 1.6)
    # Crisp Victorian tiepin seated cleanly on the silk ascot crossing
    mb.add_circle("primary", 4.5, 40.5, 1.7)
    mb.add_circle("primary", 4.5, 40.5, 0.72, filled=True)

    # Buttoned waistcoat inner V-edges sweeping cleanly to MED_R
    mb.add_arc_pts("primary", (-21.2, 13.5), (-14.5, 46.5), -1.6)
    mb.add_arc_pts("primary", (-14.5, 46.5), (1.5, 86.0), -2.4)
    mb.add_arc_pts("primary", (21.8, 11.5), (27.8, 46.5), 1.6)
    mb.add_arc_pts("primary", (27.8, 46.5), (26.5, 86.0), 1.1)
    mb.add_arc_pts("detail", (-10.5, 58.0), (-5.5, 86.0), -0.9)

    # --- TAILORED VICTORIAN COAT LAPELS & BROAD SHOULDERS TO MED_R ---
    # Left notched frock-coat lapel (clean classic Victorian notch, zero loose spike)
    mb.add_arc_pts("primary", (-21.2, -1.8), (-32.5, 4.5), 1.2)
    mb.add_arc_pts("primary", (-32.5, 4.5), (-46.5, 26.5), 1.8)
    mb.add_arc_pts("primary", (-46.5, 26.5), (-36.5, 34.5), 0.5)
    mb.add_arc_pts("primary", (-36.5, 34.5), (-21.8, 16.5), -1.0)
    mb.add_arc_pts("primary", (-21.8, 16.5), (-19.2, 52.0), -1.4)
    mb.add_arc_pts("primary", (-19.2, 52.0), (-16.8, 88.0), -1.0)

    # Right tailored frock-coat lapel (smooth continuous sweep to MED_R)
    mb.add_arc_pts("primary", (19.5, 6.2), (28.5, 11.2), -1.1)
    mb.add_arc_pts("primary", (28.5, 11.2), (40.5, 86.0), -4.2)
    mb.add_arc_pts("primary", (21.8, 11.5), (33.5, 86.0), -2.8)

    # Broad Victorian shoulders sweeping cleanly to MED_R = 92.0
    mb.add_arc_pts("primary", (-32.5, 4.5), (-76.0, 56.0), -11.5)
    mb.add_arc_pts("primary", (28.5, 11.2), (74.0, 58.0), 10.8)

    # Clean Victorian coat sleeve seams & lapel tailoring lines to MED_R
    mb.add_arc_pts("detail", (-46.5, 26.5), (-56.0, 78.0), -3.2)
    mb.add_arc_pts("detail", (-36.5, 34.5), (-38.5, 84.0), -1.8)
    mb.add_arc_pts("detail", (48.0, 32.0), (58.0, 76.0), 3.4)
    mb.add_arc_pts("detail", (42.0, 52.0), (46.5, 82.0), 1.6)

    return mb.build()


def build_casey_svg(theme: str = "dark", wave_angle_deg: float = 28.0) -> str:
    """Render the John Casey medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_casey_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_casey_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 28.0,
) -> tuple[Path, Path]:
    """Write ``casey_dark.svg`` and ``casey_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "casey_dark.svg"
    light_path = target_dir / "casey_light.svg"
    dark_path.write_text(
        build_casey_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_casey_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
