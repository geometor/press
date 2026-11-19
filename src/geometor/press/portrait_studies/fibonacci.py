"""Study 19: Leonardo Pisano / Fibonacci (after c. 1850 engraving) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_fibonacci_elements",
    "build_fibonacci_svg",
    "write_fibonacci_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"
PHI = (1.0 + math.sqrt(5.0)) / 2.0


def _add_fibonacci_spiral_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    unit: float = 1.92,
) -> None:
    """Draw the Fibonacci whirling squares (1, 1, 2, 3, 5, 8) and quarter-circle spiral.

    Constructs an exact ``8 x 13`` Fibonacci rectangle partitioned into squares of
    sides ``8, 5, 3, 2, 1, 1`` with a G1-continuous chain of ``90 deg`` circular
    arcs spiraling cleanly into the unit-square eye.
    """
    x0 = cx - 4.0 * unit
    y0 = cy - 6.5 * unit

    def pt(gx: float, gy: float) -> tuple[float, float]:
        return (x0 + gx * unit, y0 + gy * unit)

    # Outer 8 x 13 Fibonacci rectangle
    p_tl = pt(0.0, 0.0)
    p_tr = pt(8.0, 0.0)
    p_br = pt(8.0, 13.0)
    p_bl = pt(0.0, 13.0)
    mb.add_line("golden", p_tl[0], p_tl[1], p_tr[0], p_tr[1])
    mb.add_line("golden", p_tr[0], p_tr[1], p_br[0], p_br[1])
    mb.add_line("golden", p_br[0], p_br[1], p_bl[0], p_bl[1])
    mb.add_line("golden", p_bl[0], p_bl[1], p_tl[0], p_tl[1])

    # Internal square partitions: 8 | 5 | 3 | 2 | 1 | 1
    partitions: list[tuple[tuple[float, float], tuple[float, float]]] = [
        (pt(0.0, 8.0), pt(8.0, 8.0)),   # below square 8
        (pt(5.0, 8.0), pt(5.0, 13.0)),  # right of square 5
        (pt(5.0, 10.0), pt(8.0, 10.0)), # above square 3
        (pt(6.0, 8.0), pt(6.0, 10.0)),  # left of square 2
        (pt(5.0, 9.0), pt(6.0, 9.0)),   # between the two unit squares
    ]
    for a, b in partitions:
        mb.add_line("golden", a[0], a[1], b[0], b[1])

    # Exact G1-continuous quarter-circle Fibonacci spiral arcs
    spiral_arcs: list[tuple[float, float, float, float, float]] = [
        (8.0, 8.0, 8.0, 270.0, 180.0),   # square 8: (8, 0) -> (0, 8)
        (5.0, 8.0, 5.0, 180.0, 90.0),    # square 5: (0, 8) -> (5, 13)
        (5.0, 10.0, 3.0, 90.0, 0.0),     # square 3: (5, 13) -> (8, 10)
        (6.0, 10.0, 2.0, 0.0, -90.0),    # square 2: (8, 10) -> (6, 8)
        (6.0, 9.0, 1.0, -90.0, -180.0),  # square 1b: (6, 8) -> (5, 9)
        (6.0, 9.0, 1.0, 180.0, 90.0),    # square 1a: (5, 9) -> (6, 10)
    ]
    for gcx, gcy, gr, a1, a2 in spiral_arcs:
        acx, acy = pt(gcx, gcy)
        mb.add_arc("golden", acx, acy, gr * unit, a1, a2)

    # Highlight tangent join nodes and the inner spiral pole
    for gx, gy in ((8.0, 0.0), (0.0, 8.0), (5.0, 13.0), (8.0, 10.0)):
        nx, ny = pt(gx, gy)
        mb.add_circle("golden", nx, ny, 0.6)
    eye_x, eye_y = pt(6.0, 9.0)
    mb.add_circle("golden", eye_x, eye_y, 0.65, filled=True)


def _add_golden_pentagram_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.6,
) -> None:
    """Draw an inscribed regular pentagram with golden-section nodes and a ``1 : phi`` bar.

    Every diagonal intersection divides the star chords in exact extreme-and-mean
    ratio ``1 : phi``, paired below with a calibrated golden division segment.
    """
    mb.add_circle("golden", cx, cy, radius)

    verts: list[tuple[float, float]] = []
    for k in range(5):
        ang = math.radians(-90.0 + 72.0 * k)
        verts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))

    # Inscribed regular pentagon
    for k in range(5):
        p1 = verts[k]
        p2 = verts[(k + 1) % 5]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Inscribed regular pentagram (chords stepping by 2)
    for k in range(5):
        p1 = verts[k]
        p2 = verts[(k + 2) % 5]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Inner golden pentagon vertices at radius R / phi^2 (rotated 36 deg from outer)
    r_inner = radius / (PHI * PHI)
    mb.add_circle("golden", cx, cy, r_inner)
    for k in range(5):
        ang = math.radians(-54.0 + 72.0 * k)
        ix = cx + r_inner * math.cos(ang)
        iy = cy + r_inner * math.sin(ang)
        mb.add_circle("golden", ix, iy, 0.62)

    mb.add_circle("golden", cx, cy, 0.8, filled=True)

    # Extreme-and-mean division bar (1 : phi) directly beneath the circumcircle
    bar_y = cy + radius + 3.4
    bar_half = 10.4
    x_l = cx - bar_half
    x_r = cx + bar_half
    x_phi = x_l + (2.0 * bar_half) / PHI
    mb.add_line("golden", x_l, bar_y, x_r, bar_y)
    mb.add_line("golden", x_l, bar_y - 1.5, x_l, bar_y + 1.5)
    mb.add_line("golden", x_r, bar_y - 1.5, x_r, bar_y + 1.5)
    mb.add_line("golden", x_phi, bar_y - 2.0, x_phi, bar_y + 2.0)
    mb.add_circle("golden", x_phi, bar_y, 0.78, filled=True)


def build_fibonacci_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the four-layer compass-and-straightedge geometry for Fibonacci.

    Uses ``MedallionBuilder`` so every line and circular arc is clipped cleanly
    within ``MED_R = 92.0`` with zero Bezier curves.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1 (Scaffold): Canonical medallion ring, eye line & golden circles
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-14.6,
        eye_rx=6.6,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Whirling Squares Spiral (Left) & Golden Pentagram (Right)
    # -------------------------------------------------------------------------
    _add_fibonacci_spiral_motif(mb, cx=-65.0, cy=-26.0, unit=1.92)
    _add_golden_pentagram_motif(mb, cx=65.0, cy=-26.0, radius=12.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Medieval Tuscan Chaperon Hood & Hanging Cloth Tail
    # -------------------------------------------------------------------------
    # Upper draped crown silhouette (continuous sweeping arcs, no mid-crown pinch)
    mb.add_arc_pts("primary", (-36.5, -36.5), (-26.8, -48.5), 1.5)
    mb.add_arc_pts("primary", (-26.8, -48.5), (-33.5, -54.5), -1.1)
    mb.add_arc_pts("primary", (-33.5, -54.5), (3.5, -69.5), 6.2)
    mb.add_arc_pts("primary", (3.5, -69.5), (38.8, -47.5), 7.8)

    # Left overhanging chaperon brim flap returning smoothly to left temple
    mb.add_arc_pts("primary", (-36.5, -36.5), (-23.2, -31.8), -1.0)
    mb.add_arc_pts("detail", (-33.2, -37.2), (-23.5, -39.5), 1.0)

    # Smooth single-sweep rolled front brow band (bourrelet) framing the forehead
    mb.add_arc_pts("primary", (-22.6, -42.5), (20.8, -43.5), 6.8)
    mb.add_arc_pts("primary", (-26.8, -48.5), (26.0, -51.8), 9.2)

    # Concentric interior cloth creases across the hood crown & rolled brim
    mb.add_arc_pts("detail", (-29.5, -54.2), (24.5, -57.8), 8.2)
    mb.add_arc_pts("detail", (-21.0, -45.8), (19.5, -46.8), 6.8)
    mb.add_arc_pts("detail", (-16.5, -63.0), (19.5, -62.5), 4.6)

    # Signature hanging medieval cloth tail draping gracefully down the right side
    mb.add_arc_pts("primary", (26.0, -51.8), (30.2, -21.0), 1.6)
    mb.add_arc_pts("primary", (30.2, -21.0), (37.6, 12.2), -1.2)

    mb.add_arc_pts("primary", (38.8, -47.5), (44.8, -16.5), 2.2)
    mb.add_arc_pts("primary", (44.8, -16.5), (44.6, 11.8), 0.9)
    mb.add_arc_pts("primary", (37.6, 12.2), (44.6, 11.8), -0.7)

    # Flowing concentric vertical drapery folds inside the hanging hood scarf
    mb.add_arc_pts("detail", (29.8, -50.2), (34.8, -18.0), 1.6)
    mb.add_arc_pts("detail", (34.8, -18.0), (39.6, 11.4), -0.8)
    mb.add_arc_pts("detail", (34.4, -48.5), (40.2, -16.5), 1.8)
    mb.add_arc_pts("detail", (40.2, -16.5), (42.4, 11.5), 0.4)
    mb.add_wave("detail", (32.4, -44.5), (37.2, 8.8), 4, wave_angle_deg * 0.42, 1)

    # Dark hair tufts peeking beneath the chaperon along both temples
    mb.add_arc_pts("primary", (-22.6, -42.5), (-24.8, -32.0), -1.0)
    mb.add_arc_pts("primary", (-24.8, -32.0), (-22.5, -21.8), -0.8)
    mb.add_arc_pts("primary", (20.8, -43.5), (26.0, -32.2), 1.4)
    mb.add_arc_pts("primary", (26.0, -32.2), (26.8, -19.5), 1.1)
    mb.add_arc_pts("primary", (26.8, -19.5), (25.0, -11.5), 0.8)
    mb.add_wave("detail", (22.4, -40.2), (25.6, -16.5), 3, wave_angle_deg * 0.52, -1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Youthful Three-Quarter Left Tuscan Face, Eyes, Nose & Smile
    # -------------------------------------------------------------------------
    # Left three-quarter profile contour (temple -> cheek -> jaw -> rounded chin)
    mb.add_arc_pts("primary", (-22.6, -42.5), (-22.0, -32.5), -0.6)
    mb.add_arc_pts("primary", (-22.0, -32.5), (-21.4, -25.0), 0.45)
    mb.add_arc_pts("primary", (-21.4, -25.0), (-21.4, -14.2), -0.95)
    mb.add_arc_pts("primary", (-21.4, -14.2), (-17.8, -3.2), -1.15)
    mb.add_arc_pts("primary", (-17.8, -3.2), (-10.8, 6.4), -1.35)
    mb.add_arc_pts("primary", (-10.8, 6.4), (-1.5, 11.0), -1.75)

    # Broad clean right jawline rising smoothly back to right temple
    mb.add_arc_pts("primary", (-1.5, 11.0), (10.5, 9.0), -1.45)
    mb.add_arc_pts("primary", (10.5, 9.0), (20.5, 1.0), -1.55)
    mb.add_arc_pts("primary", (20.5, 1.0), (24.6, -10.5), -1.45)
    mb.add_arc_pts("primary", (24.6, -10.5), (24.6, -24.5), -0.95)
    mb.add_arc_pts("primary", (24.6, -24.5), (22.6, -36.5), -0.75)
    mb.add_arc_pts("primary", (22.6, -36.5), (20.8, -43.5), -0.55)

    # Subtle right earlobe tucked beneath temple hair
    mb.add_arc_pts("detail", (24.8, -14.5), (27.8, -16.8), -0.85)
    mb.add_arc_pts("detail", (27.8, -16.8), (26.2, -10.8), 0.95)

    # Expressive arched eyebrows
    mb.add_arc_pts("primary", (-21.2, -31.8), (-15.2, -33.8), 0.95)
    mb.add_arc_pts("primary", (-15.2, -33.8), (-8.4, -31.5), 0.95)
    mb.add_arc_pts("detail", (-20.2, -33.0), (-9.0, -32.6), 1.1)

    mb.add_arc_pts("primary", (-0.8, -32.2), (6.8, -35.4), 1.25)
    mb.add_arc_pts("primary", (6.8, -35.4), (16.4, -32.8), 1.15)
    mb.add_arc_pts("detail", (0.0, -33.4), (15.6, -33.8), 1.3)

    # Large clear expressive eyes right along y = -27 (upper lid kissing top of iris)
    # Viewer's left eye (further eye in 3/4 left turn)
    l_out = (-19.8, -25.6)
    l_in = (-9.8, -26.2)
    mb.add_arc_pts("primary", l_out, l_in, 1.95)
    mb.add_arc_pts("detail", (-20.2, -28.0), (-9.4, -28.6), 1.85)
    mb.add_arc_pts("detail", l_out, l_in, -1.35)
    mb.add_circle("detail", -14.6, -26.1, 1.95)
    mb.add_circle("primary", -14.6, -26.1, 0.96, filled=True)
    mb.add_arc_pts("detail", (-19.2, -22.5), (-10.2, -23.0), -0.95)

    # Viewer's right eye (nearer eye, serene direct gaze)
    r_in = (-0.2, -26.2)
    r_out = (13.4, -26.0)
    mb.add_arc_pts("primary", r_in, r_out, 2.35)
    mb.add_arc_pts("detail", (-0.6, -28.8), (13.8, -28.6), 2.2)
    mb.add_arc_pts("detail", r_in, r_out, -1.45)
    mb.add_circle("detail", 6.6, -26.3, 2.15)
    mb.add_circle("primary", 6.6, -26.3, 1.04, filled=True)
    mb.add_arc_pts("detail", (0.4, -22.8), (12.6, -22.8), -1.05)

    # Classic straight Tuscan nose
    mb.add_arc_pts("primary", (-5.2, -31.5), (-9.0, -20.5), 0.28)
    mb.add_arc_pts("primary", (-9.0, -20.5), (-11.4, -12.4), -0.35)
    mb.add_arc_pts("primary", (-11.4, -12.4), (-9.2, -9.6), -0.78)
    mb.add_arc_pts("primary", (-9.2, -9.6), (-4.8, -9.5), -0.48)
    mb.add_arc_pts("primary", (-4.8, -9.5), (-1.0, -11.6), -0.7)
    mb.add_arc_pts("detail", (-1.0, -11.6), (-1.6, -14.8), -0.45)
    mb.add_arc_pts("detail", (-2.2, -25.2), (-2.6, -16.4), -0.25)
    mb.add_arc_pts("detail", (-9.2, -10.8), (-6.2, -10.8), 0.35)
    mb.add_arc_pts("detail", (-4.4, -10.8), (-2.2, -11.3), 0.35)

    # Gentle composed smile with Cupid's bow & sculpted youthful chin
    mb.add_arc_pts("detail", (-6.2, -8.5), (-5.8, -5.2), 0.2)
    mb.add_arc_pts("detail", (-11.4, -3.0), (-5.6, -4.1), 0.65)
    mb.add_arc_pts("detail", (-5.6, -4.1), (3.4, -3.3), 0.65)
    mb.add_arc_pts("primary", (-11.6, -2.6), (-5.4, -1.7), -0.42)
    mb.add_arc_pts("primary", (-5.4, -1.7), (3.9, -3.1), -0.58)
    mb.add_arc_pts("detail", (-9.6, 0.2), (-4.6, 0.8), -0.78)
    mb.add_arc_pts("detail", (-4.6, 0.8), (1.8, -0.5), -0.62)
    mb.add_arc_pts("detail", (-7.6, 3.8), (-1.4, 3.6), -0.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Neck, Gathered Medieval Collar & Pleated Scholar's Tunic
    # -------------------------------------------------------------------------
    # Neck contours & subtle throat/jaw shadow
    mb.add_arc_pts("primary", (-10.8, 6.4), (-4.0, 17.8), -0.75)
    mb.add_arc_pts("primary", (21.0, 1.4), (31.5, 11.2), -1.0)
    mb.add_arc_pts("detail", (-5.8, 12.6), (12.5, 9.0), -0.95)
    mb.add_arc_pts("detail", (16.5, 5.2), (11.5, 16.2), 0.65)

    # Gathered medieval tunic collar band
    mb.add_arc_pts("primary", (-4.0, 17.8), (-0.8, 22.8), -0.7)
    mb.add_arc_pts("primary", (-0.8, 22.8), (19.5, 17.2), -2.2)
    mb.add_arc_pts("primary", (19.5, 17.2), (32.0, 10.5), -1.2)
    mb.add_arc_pts("detail", (-2.6, 15.2), (0.2, 19.6), -0.6)
    mb.add_arc_pts("detail", (0.2, 19.6), (18.5, 14.5), -2.0)
    mb.add_arc_pts("detail", (18.5, 14.5), (29.8, 8.2), -1.0)

    # Shoulders & medieval scholar tunic clipped razor-flush to MED_R = 92.0
    mb.add_arc_pts("primary", (-4.0, 17.8), (-31.0, 32.5), -2.8)
    mb.add_arc_pts("primary", (-31.0, 32.5), (-68.0, 74.0), -6.5)
    mb.add_arc_pts("primary", (32.0, 10.5), (56.0, 26.5), 3.0)
    mb.add_arc_pts("primary", (56.0, 26.5), (78.5, 62.0), 4.8)

    # Center placket & tunic buttons (clipped flush at bottom medallion rim)
    mb.add_arc_pts("primary", (-0.8, 22.8), (1.0, 88.0), -1.1)
    mb.add_arc_pts("detail", (3.2, 22.4), (5.2, 88.0), -1.1)
    for by in (43.5, 57.5, 71.5):
        mb.add_circle("detail", 1.8, by, 1.3)

    # Gathered vertical scholar tunic pleats radiating cleanly to MED_R = 92.0
    mb.add_arc_pts("primary", (-11.5, 22.5), (-27.0, 86.0), -2.6)
    mb.add_arc_pts("primary", (16.5, 18.2), (25.5, 86.0), 2.2)
    mb.add_arc_pts("detail", (-6.2, 21.5), (-12.8, 87.0), -1.7)
    mb.add_arc_pts("detail", (-21.5, 28.5), (-42.5, 82.0), -3.0)
    mb.add_arc_pts("detail", (-32.5, 40.5), (-52.5, 77.5), -2.5)
    mb.add_arc_pts("detail", (9.5, 20.5), (15.0, 87.0), 1.7)
    mb.add_arc_pts("detail", (24.5, 15.8), (39.5, 82.0), 2.6)
    mb.add_arc_pts("detail", (34.5, 15.5), (54.5, 74.5), 3.0)
    mb.add_arc_pts("detail", (46.5, 23.0), (66.5, 67.0), 2.8)

    # Subtle woven wool cadence along shoulder folds
    mb.add_wave("detail", (-26.5, 34.0), (-43.5, 76.0), 4, wave_angle_deg * 0.45, 1)
    mb.add_wave("detail", (28.5, 21.0), (45.5, 72.5), 4, wave_angle_deg * 0.45, -1)

    return mb.build()


def build_fibonacci_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Leonardo Pisano (Fibonacci) medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_fibonacci_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_fibonacci_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``fibonacci_dark.svg`` and ``fibonacci_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "fibonacci_dark.svg"
    light_path = target_dir / "fibonacci_light.svg"
    dark_path.write_text(
        build_fibonacci_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_fibonacci_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
