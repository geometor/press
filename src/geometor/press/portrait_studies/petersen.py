"""Study 34: Julius Petersen (after the 19th-century Danish cabinet portrait)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_petersen_elements",
    "build_petersen_svg",
    "write_petersen_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_petersen_graph_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw the iconic Petersen Graph (10 vertices, 15 edges) in the open left margin.

    Constructs the canonical 5-fold symmetric embedding: an outer regular
    pentagon (5 edges), a concentric inner ``{5/2}`` pentagram star (5 edges),
    5 radial spokes linking corresponding vertices, and 10 crisp circular nodes.
    """
    r_out = 12.2
    r_in = 6.2
    outer: list[tuple[float, float]] = []
    inner: list[tuple[float, float]] = []
    for k in range(5):
        ang = math.radians(-90.0 + 72.0 * k)
        ca, sa = math.cos(ang), math.sin(ang)
        outer.append((cx + r_out * ca, cy + r_out * sa))
        inner.append((cx + r_in * ca, cy + r_in * sa))

    # 5 outer pentagon edges, 5 inner pentagram star edges, and 5 radial spokes
    for k in range(5):
        p_o1, p_o2 = outer[k], outer[(k + 1) % 5]
        p_i1, p_i2 = inner[k], inner[(k + 2) % 5]
        mb.add_line("golden", p_o1[0], p_o1[1], p_o2[0], p_o2[1])
        mb.add_line("golden", p_i1[0], p_i1[1], p_i2[0], p_i2[1])
        mb.add_line("golden", p_o1[0], p_o1[1], p_i1[0], p_i1[1])

    # 10 crisp circular graph vertices
    for vx, vy in outer + inner:
        mb.add_circle("golden", vx, vy, 0.82, filled=True)


def _add_homothety_loci_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Petersen's Method of Homothety / Similitude in the open right margin.

    Constructs an exact center of similitude ``O`` with two homothetic circles
    ``C1`` and ``C2`` (scaling ratio ``k = 2.0``), their exact common external
    tangent rays, the center-line ray through ``O, M1, M2``, and parallel
    corresponding homothetic chords illustrating geometric loci scaling.
    """
    origin = (cx - 12.2, cy - 10.6)
    dx1, dy1 = 10.2, 6.8
    dist1 = math.hypot(dx1, dy1)
    r1 = 3.4
    scale_k = 2.02
    r2 = scale_k * r1
    m1 = (origin[0] + dx1, origin[1] + dy1)
    m2 = (origin[0] + scale_k * dx1, origin[1] + scale_k * dy1)

    # Exact homothetic circles C1 and C2
    mb.add_circle("golden", m1[0], m1[1], r1)
    mb.add_circle("golden", m2[0], m2[1], r2)

    # Common external tangent rays from center of similitude O
    axis_ang = math.atan2(dy1, dx1)
    half_spread = math.asin(r1 / dist1)
    t_len1 = math.sqrt(dist1 * dist1 - r1 * r1)
    t_len2 = scale_k * t_len1
    ray_ext = t_len2 + 2.2
    for sign in (-1.0, 1.0):
        ang = axis_ang + sign * half_spread
        ca, sa = math.cos(ang), math.sin(ang)
        mb.add_line(
            "golden",
            origin[0],
            origin[1],
            origin[0] + ray_ext * ca,
            origin[1] + ray_ext * sa,
        )
        # Exact tangency points on C1 and C2
        t1 = (origin[0] + t_len1 * ca, origin[1] + t_len1 * sa)
        t2 = (origin[0] + t_len2 * ca, origin[1] + t_len2 * sa)
        mb.add_circle("golden", t1[0], t1[1], 0.56, filled=True)
        mb.add_circle("golden", t2[0], t2[1], 0.64, filled=True)

    # Center-line ray through O -> M1 -> M2
    ux, uy = dx1 / dist1, dy1 / dist1
    mb.add_line(
        "golden",
        origin[0],
        origin[1],
        m2[0] + (r2 + 1.4) * ux,
        m2[1] + (r2 + 1.4) * uy,
    )

    # Parallel corresponding homothetic chords inside C1 and C2
    a1_ang = axis_ang - 1.05
    b1_ang = axis_ang + 1.35
    a1 = (m1[0] + r1 * math.cos(a1_ang), m1[1] + r1 * math.sin(a1_ang))
    b1 = (m1[0] + r1 * math.cos(b1_ang), m1[1] + r1 * math.sin(b1_ang))
    a2 = (m2[0] + r2 * math.cos(a1_ang), m2[1] + r2 * math.sin(a1_ang))
    b2 = (m2[0] + r2 * math.cos(b1_ang), m2[1] + r2 * math.sin(b1_ang))
    mb.add_line("golden", a1[0], a1[1], b1[0], b1[1])
    mb.add_line("golden", a2[0], a2[1], b2[0], b2[1])

    # Center markers for O, M1, and M2
    mb.add_circle("golden", origin[0], origin[1], 0.88)
    mb.add_circle("golden", origin[0], origin[1], 0.44, filled=True)
    mb.add_circle("golden", m1[0], m1[1], 0.54, filled=True)
    mb.add_circle("golden", m2[0], m2[1], 0.60, filled=True)


def build_petersen_elements(wave_angle_deg: float = 32.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Julius Petersen.

    Calibrated to the 19th-century Danish cabinet portrait: tall voluminous
    curly swept-up Victorian hair crowning a clean broad forehead, calm direct
    eyes on ``y = -27``, straight nose, neat full 19th-century mustache and
    small soul-patch above a clean tapered chin, crisp folded white collar and
    knotted ascot tie over a buttoned pale waistcoat, and tailored dark
    Victorian coat lapels & sloped shoulders sweeping cleanly to ``MED_R = 92.0``.
    Margin motifs display the Petersen Graph (left) and Petersen's Method of
    Homothety (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-10.0,
        eye_rx=6.2,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN PETERSEN MARGIN MOTIFS (open margins, zero face crossing) ---
    _add_petersen_graph_motif(mb, cx=-63.5, cy=-26.0)
    _add_homothety_loci_motif(mb, cx=63.2, cy=-26.2)

    # --- TALL VOLUMINOUS CURLY SWEPT-UP VICTORIAN HAIR ---
    # Sculpted tall curly Victorian pompadour crown rising to y = -71
    mb.add_arc_pts("primary", (-20.2, -28.0), (-24.8, -39.0), 1.6)
    mb.add_arc_pts("primary", (-24.8, -39.0), (-24.2, -52.0), 1.9)
    mb.add_arc_pts("primary", (-24.2, -52.0), (-16.2, -64.0), 2.2)
    mb.add_arc_pts("primary", (-16.2, -64.0), (-2.5, -71.2), 2.6)
    mb.add_arc_pts("primary", (-2.5, -71.2), (13.8, -68.8), 2.6)
    mb.add_arc_pts("primary", (13.8, -68.8), (24.8, -58.0), 2.3)
    mb.add_arc_pts("primary", (24.8, -58.0), (29.8, -43.5), 2.1)
    mb.add_arc_pts("primary", (29.8, -43.5), (27.2, -31.5), 1.5)
    mb.add_arc_pts("primary", (27.2, -31.5), (22.8, -24.5), 0.9)

    # Clean broad forehead hairline beneath the curly crown
    mb.add_arc_pts("primary", (-18.5, -28.5), (-18.0, -39.5), 0.9)
    mb.add_arc_pts("primary", (-18.0, -39.5), (-13.2, -47.2), 1.1)
    mb.add_arc_pts("primary", (-13.2, -47.2), (-1.0, -48.8), 1.2)
    mb.add_arc_pts("primary", (-1.0, -48.8), (12.8, -47.0), 1.2)
    mb.add_arc_pts("primary", (12.8, -47.0), (18.8, -38.5), 1.1)
    mb.add_arc_pts("primary", (18.8, -38.5), (19.6, -26.5), 0.8)

    # Lush Victorian curls strictly inside crown via Euclid III.12 tangent waves
    mb.add_wave("detail", (-20.8, -48.5), (-11.5, -62.0), 3, wave_angle_deg + 4.0, 1)
    mb.add_wave("detail", (-12.0, -62.0), (13.0, -63.2), 4, wave_angle_deg + 4.0, -1)
    mb.add_wave("detail", (-15.0, -55.0), (17.5, -55.8), 5, wave_angle_deg + 4.0, 1)
    mb.add_wave("detail", (-9.0, -51.8), (16.5, -50.8), 4, wave_angle_deg + 3.0, -1)
    mb.add_wave("detail", (19.8, -50.5), (26.2, -35.5), 3, wave_angle_deg + 4.0, 1)
    mb.add_wave("detail", (-21.8, -34.5), (-20.6, -45.5), 3, wave_angle_deg + 4.0, -1)

    # --- CLEAN TAPERED FACE CONTOUR & RIGHT EAR ---
    mb.add_arc_pts("primary", (-18.5, -28.5), (-18.5, -18.5), -0.7)
    mb.add_arc_pts("primary", (-18.5, -18.5), (-16.2, -8.2), -1.0)
    mb.add_arc_pts("primary", (-16.2, -8.2), (-9.5, 0.5), -1.2)
    mb.add_arc_pts("primary", (-9.5, 0.5), (-2.5, 4.5), -1.3)
    mb.add_arc_pts("primary", (-2.5, 4.5), (7.5, 1.5), -1.4)
    mb.add_arc_pts("primary", (7.5, 1.5), (16.0, -6.5), -1.3)
    mb.add_arc_pts("primary", (16.0, -6.5), (19.8, -16.5), -1.0)
    mb.add_arc_pts("primary", (19.8, -16.5), (20.2, -25.0), -0.7)

    # Right ear (viewer's right)
    mb.add_arc_pts("primary", (20.2, -25.0), (24.0, -23.0), 1.0)
    mb.add_arc_pts("primary", (24.0, -23.0), (22.8, -16.0), 1.0)
    mb.add_arc_pts("primary", (22.8, -16.0), (19.2, -14.2), 0.8)
    mb.add_arc_pts("detail", (20.8, -22.2), (21.8, -17.2), 0.7)

    # --- CALM DIRECT EYES ON y = -27 & STRAIGHT BROWS ---
    mb.add_arc_pts("primary", (-16.8, -30.8), (-10.2, -32.2), 0.65)
    mb.add_arc_pts("primary", (-10.2, -32.2), (-4.5, -30.6), 0.5)
    mb.add_arc_pts("detail", (-15.8, -30.0), (-5.4, -29.8), 0.65)

    mb.add_arc_pts("primary", (0.6, -30.6), (6.5, -32.2), 0.65)
    mb.add_arc_pts("primary", (6.5, -32.2), (14.2, -30.5), 0.55)
    mb.add_arc_pts("detail", (1.6, -29.8), (13.2, -29.8), 0.65)

    mb.add_canonical_eye(
        -10.0,
        -26.8,
        width=9.2,
        upper_sag=1.80,
        lower_sag=-0.88,
        iris_r=1.92,
        pupil_r=1.02,
        gaze_dx=-0.15,
    )
    mb.add_canonical_eye(
        6.2,
        -26.8,
        width=9.8,
        upper_sag=1.85,
        lower_sag=-0.90,
        iris_r=1.98,
        pupil_r=1.05,
        gaze_dx=-0.22,
    )

    # --- STRAIGHT CLASSICAL NOSE ---
    mb.add_arc_pts("primary", (-2.6, -29.5), (-4.2, -22.2), 0.25)
    mb.add_arc_pts("primary", (-4.2, -22.2), (-5.8, -16.5), 0.25)
    mb.add_arc_pts("primary", (-5.8, -16.5), (-5.2, -14.5), -0.45)
    mb.add_arc_pts("primary", (-5.2, -14.5), (-1.8, -14.2), -0.35)
    mb.add_arc_pts("primary", (-1.8, -14.2), (0.8, -15.2), -0.35)
    mb.add_arc_pts("primary", (0.8, -15.2), (1.2, -16.8), -0.5)
    mb.add_arc_pts("primary", (1.2, -16.8), (-0.6, -17.4), -0.3)
    mb.add_arc_pts("detail", (-6.0, -15.6), (-7.0, -16.6), -0.3)

    # --- NEAT FULL 19TH-CENTURY MUSTACHE, MOUTH & SMALL SOUL-PATCH ---
    # Sculpted sweeping Victorian mustache with subtle central philtrum dip
    mb.add_arc_pts("primary", (-12.5, -7.8), (-7.6, -11.4), 0.7)
    mb.add_arc_pts("primary", (-7.6, -11.4), (-3.0, -11.2), 0.35)
    mb.add_arc_pts("primary", (-3.0, -11.2), (2.2, -11.2), 0.35)
    mb.add_arc_pts("primary", (2.2, -11.2), (7.5, -7.5), 0.7)
    mb.add_arc_pts("primary", (-12.5, -7.8), (-7.5, -8.9), -0.42)
    mb.add_arc_pts("primary", (-7.5, -8.9), (-3.0, -9.2), -0.28)
    mb.add_arc_pts("primary", (-3.0, -9.2), (2.0, -8.7), -0.28)
    mb.add_arc_pts("primary", (2.0, -8.7), (7.5, -7.5), -0.42)
    # Fine brushed mustache strands in detail
    mb.add_arc_pts("detail", (-10.6, -8.6), (-4.2, -10.3), 0.35)
    mb.add_arc_pts("detail", (-1.8, -10.3), (5.5, -8.4), 0.35)

    # Composed lower lip & refined small Victorian soul-patch wisps
    mb.add_arc_pts("primary", (-7.0, -6.4), (-2.8, -5.8), 0.25)
    mb.add_arc_pts("primary", (-2.8, -5.8), (1.6, -6.3), 0.25)
    mb.add_arc_pts("primary", (-5.4, -3.9), (-2.6, -3.4), -0.4)
    mb.add_arc_pts("primary", (-2.6, -3.4), (0.3, -3.9), -0.4)
    # Soft vertical soul-patch wisps below lower lip
    mb.add_arc_pts("detail", (-4.0, -2.3), (-3.2, 0.8), -0.25)
    mb.add_line("detail", -2.7, -2.4, -2.7, 1.1)
    mb.add_arc_pts("detail", (-1.4, -2.3), (-2.1, 0.8), 0.25)

    # --- FOLDED WHITE COLLAR, KNOTTED ASCOT, BUTTONED WAISTCOAT & COAT ---
    # Neck & crisp folded white collar
    mb.add_arc_pts("primary", (-8.5, 2.2), (-9.5, 11.5), 0.6)
    mb.add_arc_pts("primary", (14.5, -4.5), (19.2, 2.5), -0.7)
    mb.add_arc_pts("primary", (19.2, 2.5), (5.0, 22.8), 1.4)
    mb.add_arc_pts("primary", (5.0, 22.8), (-6.5, 14.5), -0.7)
    mb.add_arc_pts("detail", (14.2, 0.2), (-5.2, 13.8), -1.1)
    mb.add_arc_pts("primary", (-9.5, 11.5), (-10.5, 17.5), -0.5)
    mb.add_arc_pts("primary", (-10.5, 17.5), (-6.5, 14.5), -0.5)

    # Knotted silk ascot tie nestled cleanly under the white collar
    mb.add_arc_pts("primary", (-6.5, 14.5), (-11.2, 21.8), 0.7)
    mb.add_arc_pts("primary", (-11.2, 21.8), (-5.0, 26.8), 0.6)
    mb.add_arc_pts("primary", (-5.0, 26.8), (2.8, 21.2), 0.7)
    mb.add_arc_pts("detail", (-7.8, 16.5), (-6.8, 25.2), 0.4)
    mb.add_arc_pts("detail", (-4.5, 16.8), (-1.2, 23.8), -0.4)
    mb.add_arc_pts("detail", (-10.5, 22.5), (-12.8, 35.5), 0.7)

    # Pale buttoned waistcoat (flanking placket seams + 3 crisp buttons)
    mb.add_arc_pts("primary", (-13.2, 20.5), (-26.5, 86.0), 2.6)
    mb.add_arc_pts("primary", (-7.6, 26.2), (-21.8, 86.0), 2.4)
    mb.add_arc_pts("detail", (-12.0, 26.8), (-25.8, 86.0), 2.4)
    for bx, by in ((-10.2, 34.5), (-13.5, 50.0), (-16.8, 65.5)):
        mb.add_circle("primary", bx, by, 1.45)
        mb.add_circle("primary", bx, by, 0.58, filled=True)

    # Dark tailored Victorian coat lapels & sloped shoulders sweeping to MED_R
    # Viewer-right sweeping tailored lapel framing the pale waistcoat
    mb.add_arc_pts("primary", (19.2, 2.5), (25.2, 7.5), -1.0)
    mb.add_arc_pts("primary", (25.2, 7.5), (-22.5, 86.0), 7.2)
    mb.add_arc_pts("primary", (25.2, 7.5), (16.5, 42.0), 1.8)
    mb.add_arc_pts("primary", (16.5, 42.0), (-9.5, 86.0), 3.6)

    # Viewer-left tailored lapel & sloped shoulder sweeping cleanly to MED_R
    mb.add_arc_pts("primary", (-10.5, 11.5), (-24.5, 20.5), 1.4)
    mb.add_arc_pts("primary", (-24.5, 20.5), (-37.5, 58.0), -2.6)
    mb.add_arc_pts("primary", (-37.5, 58.0), (-31.0, 84.0), -1.2)
    mb.add_arc_pts("primary", (-11.8, 15.2), (-29.5, 84.0), 3.0)

    # Faithful sloped Victorian shoulders grounded cleanly to MED_R (chair omitted)
    mb.add_arc_pts("primary", (-24.5, 20.5), (-58.0, 74.0), -6.2)
    mb.add_arc_pts("primary", (25.2, 7.5), (66.0, 64.0), 12.2)

    # Clean Victorian coat sleeve seams & tailoring lines to MED_R
    mb.add_arc_pts("detail", (-39.0, 39.0), (-46.5, 79.0), -2.2)
    mb.add_arc_pts("detail", (36.5, 24.0), (48.0, 80.0), 4.2)
    mb.add_arc_pts("detail", (22.5, 52.0), (14.0, 86.0), 2.2)
    mb.add_arc_pts("detail", (48.0, 46.0), (58.0, 74.0), 2.0)

    return mb.build()


def build_petersen_svg(theme: str = "dark", wave_angle_deg: float = 32.0) -> str:
    """Render the Julius Petersen medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_petersen_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_petersen_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 32.0,
) -> tuple[Path, Path]:
    """Write ``petersen_dark.svg`` and ``petersen_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "petersen_dark.svg"
    light_path = target_dir / "petersen_light.svg"
    dark_path.write_text(
        build_petersen_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_petersen_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
