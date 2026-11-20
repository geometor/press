"""Study 28: Nicomachus of Gerasa (after the 12th-century Cambridge MS miniature)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_nicomachus_elements",
    "build_nicomachus_svg",
    "write_nicomachus_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_tetractys_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    step: float = 4.8,
) -> None:
    """Draw the Pythagorean Tetractys (``1 + 2 + 3 + 4 = 10``) in the left margin.

    Encloses four rows of ``1, 2, 3, 4`` crisp golden figurate circles inside
    an exact circumscribing equilateral triangle.
    """
    sqrt3 = math.sqrt(3.0)
    h_row = 0.5 * sqrt3 * step
    pad = 2.65

    # Position the 4 pebble rows so the enclosing equilateral triangle centers on (cx, cy)
    y_top_dot = cy - 1.5 * h_row + 0.85
    y_bot_dot = y_top_dot + 3.0 * h_row

    # Exact outer equilateral triangle offset outward by ``pad`` from outer row centers
    half_base = 1.5 * step + pad * sqrt3
    apex = (cx, y_top_dot - 2.0 * pad)
    base_l = (cx - half_base, y_bot_dot + pad)
    base_r = (cx + half_base, y_bot_dot + pad)

    mb.add_line("golden", apex[0], apex[1], base_l[0], base_l[1])
    mb.add_line("golden", base_l[0], base_l[1], base_r[0], base_r[1])
    mb.add_line("golden", base_r[0], base_r[1], apex[0], apex[1])

    # Four rows of 1, 2, 3, 4 crisp golden circles
    for row in range(4):
        ry = y_top_dot + row * h_row
        start_x = cx - 0.5 * row * step
        for col in range(row + 1):
            rx = start_x + col * step
            mb.add_circle("golden", rx, ry, 1.45)


def _add_square_gnomon_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    cell: float = 5.0,
) -> None:
    """Draw the ``4 x 4`` Square Gnomon Lattice (``1 + 3 + 5 + 7 = 4^2``).

    Constructs the outer square frame, three nested L-shaped odd-gnomon
    brackets anchored at the lower-left origin, and sixteen figurate pebble
    nodes alternating filled/open by gnomon layer to display the odd sums.
    """
    side = 4.0 * cell
    x0 = cx - 0.5 * side
    y0 = cy + 0.5 * side  # Bottom-left origin in SVG coords (x right, y down)

    # Outer 4x4 square frame
    mb.add_line("golden", x0, y0, x0 + side, y0)
    mb.add_line("golden", x0 + side, y0, x0 + side, y0 - side)
    mb.add_line("golden", x0 + side, y0 - side, x0, y0 - side)
    mb.add_line("golden", x0, y0 - side, x0, y0)

    # Nested L-shaped gnomon brackets for n = 1, 2, 3
    for n in (1, 2, 3):
        d = n * cell
        mb.add_line("golden", x0, y0 - d, x0 + d, y0 - d)
        mb.add_line("golden", x0 + d, y0 - d, x0 + d, y0)

    # 16 figurate pebble nodes alternating filled/open by gnomon layer k = max(i, j)
    for i in range(4):
        for j in range(4):
            px = x0 + (i + 0.5) * cell
            py = y0 - (j + 0.5) * cell
            gnomon_idx = max(i, j)
            if gnomon_idx % 2 == 0:
                mb.add_circle("golden", px, py, 0.95, filled=True)
            else:
                mb.add_circle("golden", px, py, 1.08)


def build_nicomachus_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Nicomachus of Gerasa.

    Calibrated to the 12th-century Cambridge illuminated manuscript miniature:
    youthful beardless scholar in three-quarter left gaze straddling ``y = -27``,
    center-parted shoulder-length wavy medieval curls, ornate circular throat
    clasp, draped liturgical scholar's cloak, and an open *Arithmetica* codex
    held at his chest. Margin motifs display the Pythagorean Tetractys (left)
    and the ``4 x 4`` Square Gnomon Lattice (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-10.8,
        eye_rx=4.8,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN MARGIN MOTIFS (open left & right margins, zero face crossing) ---
    _add_tetractys_motif(mb, cx=-64.0, cy=-28.0, step=4.8)
    _add_square_gnomon_motif(mb, cx=64.0, cy=-28.0, cell=5.0)

    # --- CROWN & CENTER-PARTED MEDIEVAL WAVY CURLS ---
    # Smooth outer cranium / hair dome curving from left temple over crown to right back
    mb.add_arc_pts("primary", (-27.8, -34.5), (-16.0, -53.8), 3.6)
    mb.add_arc_pts("primary", (-16.0, -53.8), (15.5, -60.8), 5.0)
    mb.add_arc_pts("primary", (15.5, -60.8), (35.8, -33.5), 6.2)

    # Left temple hair puff framing far brow/cheek
    mb.add_arc_pts("primary", (-27.8, -34.5), (-29.2, -26.0), -1.4)
    mb.add_arc_pts("primary", (-29.2, -26.0), (-24.5, -18.5), -1.3)
    mb.add_arc_pts("primary", (-24.5, -18.5), (-20.2, -17.5), -0.6)

    # Billowing shoulder-length rolled curls behind right ear & neck (viewer's right)
    mb.add_arc_pts("primary", (35.8, -33.5), (43.8, -24.5), 2.4)
    mb.add_arc_pts("primary", (43.8, -24.5), (44.8, -14.5), 2.2)
    mb.add_arc_pts("primary", (44.8, -14.5), (36.5, -5.5), 2.4)
    mb.add_arc_pts("primary", (36.5, -5.5), (25.5, -4.0), 1.6)
    mb.add_arc_pts("primary", (25.5, -4.0), (19.5, -7.8), 0.9)

    # Center-parted hairline framing the forehead
    mb.add_arc_pts("detail", (14.5, -60.5), (4.5, -45.5), -1.6)
    mb.add_arc_pts("primary", (-19.5, -36.5), (-8.5, -44.8), 1.8)
    mb.add_arc_pts("primary", (-8.5, -44.8), (4.5, -45.5), 1.4)
    mb.add_arc_pts("primary", (4.5, -45.5), (16.8, -42.5), 1.5)
    mb.add_arc_pts("primary", (16.8, -42.5), (22.2, -34.5), 1.2)
    mb.add_arc_pts("primary", (22.2, -34.5), (22.0, -24.5), 0.8)

    # Flowing Euclid III.12 medieval hair waves across crown and rolled curls
    mb.add_wave("detail", (11.5, -56.5), (-18.5, -44.0), 4, wave_angle_deg + 4.0, 1)
    mb.add_wave("detail", (16.5, -55.0), (31.5, -35.5), 3, wave_angle_deg + 4.0, -1)
    mb.add_wave("detail", (22.5, -46.5), (36.5, -24.0), 3, wave_angle_deg + 6.0, 1)
    mb.add_wave("detail", (26.5, -28.0), (39.5, -13.5), 3, wave_angle_deg + 8.0, -1)
    mb.add_arc_pts("detail", (24.5, -14.0), (37.0, -10.5), -2.2)
    mb.add_arc_pts("detail", (-25.5, -34.5), (-22.5, -22.5), -1.4)

    # --- YOUTHFUL BEARDLESS FACE CONTOUR (3/4 LEFT TURN) ---
    mb.add_arc_pts("primary", (-16.8, -39.5), (-18.0, -33.2), -0.6)
    mb.add_arc_pts("primary", (-18.0, -33.2), (-17.2, -27.5), 0.45)
    mb.add_arc_pts("primary", (-17.2, -27.5), (-19.4, -19.2), -1.1)
    mb.add_arc_pts("primary", (-19.4, -19.2), (-18.8, -11.2), -0.9)
    # Refined youthful jaw & rounded chin sweeping smoothly up to right ear
    mb.add_arc_pts("primary", (-18.8, -11.2), (-14.0, -2.8), -1.2)
    mb.add_arc_pts("primary", (-14.0, -2.8), (-4.8, 1.8), -1.5)
    mb.add_arc_pts("primary", (-4.8, 1.8), (8.8, -0.8), -1.7)
    mb.add_arc_pts("primary", (8.8, -0.8), (19.5, -11.5), -1.6)

    # --- RIGHT EAR (VIEWER'S RIGHT) ---
    mb.add_arc_pts("primary", (21.5, -24.2), (25.8, -20.5), 1.3)
    mb.add_arc_pts("primary", (25.8, -20.5), (24.8, -13.5), 1.2)
    mb.add_arc_pts("primary", (24.8, -13.5), (19.5, -11.5), 1.0)
    mb.add_arc_pts("detail", (22.2, -21.2), (23.8, -15.5), 0.9)

    # --- EYEBROWS & CANONICAL EYES (3/4 LEFT GAZE STRADDLING y = -27) ---
    # Viewer's left brow (calm classical arch)
    mb.add_arc_pts("primary", (-16.8, -32.4), (-11.2, -34.5), 0.85)
    mb.add_arc_pts("primary", (-11.2, -34.5), (-5.5, -31.8), 0.65)
    mb.add_arc_pts("detail", (-15.8, -31.2), (-6.4, -31.0), 1.15)

    # Viewer's right brow (serene scholar's arch)
    mb.add_arc_pts("primary", (-0.6, -31.2), (5.8, -33.0), 0.9)
    mb.add_arc_pts("primary", (5.8, -33.0), (13.4, -29.0), 0.85)
    mb.add_arc_pts("detail", (0.2, -30.0), (12.4, -28.2), 1.2)

    # Expressive canonical eyes looking three-quarters left
    mb.add_canonical_eye(
        -10.8,
        -27.6,
        width=8.4,
        upper_sag=2.25,
        lower_sag=-1.1,
        iris_r=1.9,
        pupil_r=0.95,
        gaze_dx=-0.75,
    )
    mb.add_canonical_eye(
        4.8,
        -26.2,
        width=11.0,
        upper_sag=2.55,
        lower_sag=-1.25,
        iris_r=2.25,
        pupil_r=1.1,
        gaze_dx=-1.1,
    )
    # Subtle under-eye lid lines & calm forehead arc
    mb.add_arc_pts("detail", (-14.5, -24.5), (-7.2, -24.9), -0.65)
    mb.add_arc_pts("detail", (-0.2, -23.0), (9.8, -22.7), -0.75)
    mb.add_arc_pts("detail", (-9.5, -39.2), (10.5, -38.6), 0.8)

    # --- NOSE, CHEEK & COMPOSED YOUTHFUL MOUTH ---
    mb.add_arc_pts("primary", (-3.8, -31.2), (-6.2, -24.0), 0.45)
    mb.add_arc_pts("primary", (-6.2, -24.0), (-9.4, -18.0), 0.35)
    mb.add_arc_pts("primary", (-9.4, -18.0), (-10.5, -15.2), -0.5)
    mb.add_arc_pts("primary", (-10.5, -15.2), (-9.0, -13.4), -0.75)
    mb.add_arc_pts("primary", (-9.0, -13.4), (-5.4, -13.6), -0.4)
    mb.add_arc_pts("primary", (-5.4, -13.6), (-3.2, -15.0), -0.45)
    # Right nostril wing C-curve (viewer's right)
    mb.add_arc_pts("primary", (-3.2, -15.0), (-2.8, -17.0), -0.55)
    mb.add_arc_pts("primary", (-2.8, -17.0), (-4.8, -17.6), -0.4)
    # Subtle bridge & cheek modeling
    mb.add_arc_pts("detail", (-1.8, -27.2), (-3.4, -20.5), -0.35)
    mb.add_arc_pts("detail", (10.5, -18.5), (6.5, -10.5), -0.9)
    mb.add_arc_pts("detail", (-2.2, -14.8), (1.8, -10.2), 0.65)

    # Composed youthful mouth & chin cleft
    mb.add_arc_pts("detail", (-13.8, -10.0), (-9.6, -10.5), 0.35)
    mb.add_arc_pts("detail", (-9.6, -10.5), (-5.5, -9.0), 0.35)
    mb.add_arc_pts("primary", (-14.4, -9.0), (-9.5, -9.2), 0.3)
    mb.add_arc_pts("primary", (-9.5, -9.2), (-5.0, -8.2), 0.3)
    mb.add_arc_pts("primary", (-12.8, -6.8), (-9.4, -6.1), -0.65)
    mb.add_arc_pts("primary", (-9.4, -6.1), (-6.2, -6.8), -0.55)
    mb.add_arc_pts("detail", (-11.0, -3.5), (-8.2, -3.2), -0.4)

    # --- NECK, JEWELED CIRCULAR CLASP & LITURGICAL SCHOLAR'S CLOAK ---
    # Neck edges descending into embroidered collar
    mb.add_arc_pts("primary", (-12.5, 0.4), (-11.5, 10.2), 0.8)
    mb.add_arc_pts("primary", (17.2, -5.8), (22.5, 6.2), -1.1)
    mb.add_arc_pts("detail", (4.0, 2.5), (7.5, 11.5), -0.6)

    # Ornate circular jeweled mantle clasp (fibula) at throat
    mb.add_circle("primary", 11.5, 18.5, 6.0)
    mb.add_circle("detail", 11.5, 18.5, 3.8)
    mb.add_circle("primary", 11.5, 18.5, 1.35, filled=True)

    # Embroidered medieval collar band connecting neck & shoulders cleanly to clasp
    mb.add_arc_pts("primary", (-11.5, 10.2), (5.8, 17.0), -2.2)
    mb.add_arc_pts("primary", (-16.5, 15.2), (6.5, 22.2), -2.4)
    mb.add_arc_pts("primary", (17.2, 16.5), (27.8, 3.8), -1.8)
    mb.add_arc_pts("primary", (17.5, 21.8), (35.8, 7.2), -2.2)
    # Subtle jeweled collar medallions
    mb.add_circle("detail", -5.2, 15.5, 1.55)
    mb.add_circle("detail", 1.2, 18.0, 1.55)
    mb.add_circle("detail", 24.0, 12.8, 1.55)

    # Smooth single-arc draped left shoulder & wide medieval sleeve sweeping to MED_R
    mb.add_arc_pts("primary", (-11.5, 10.2), (-76.5, 38.5), -8.6)
    # Embroidered sleeve cuff bands meeting the upper sleeve flush
    mb.add_arc_pts("primary", (-51.2, 20.8), (-53.8, 56.2), -2.8)
    mb.add_arc_pts("primary", (-58.2, 24.4), (-60.8, 57.6), -2.8)
    mb.add_circle("detail", -56.0, 33.0, 1.7)
    mb.add_circle("detail", -56.0, 44.0, 1.7)
    # Lower draped sleeve hem curving smoothly into left torso cloak
    mb.add_arc_pts("primary", (-69.5, 58.5), (-23.5, 52.5), -2.8)
    mb.add_arc_pts("primary", (-23.5, 52.5), (-29.5, 82.0), -2.6)

    # Right shoulder & full draped scholar's mantle descending cleanly to MED_R
    mb.add_arc_pts("primary", (27.8, 3.8), (76.5, 52.0), 11.2)
    # Broad decorative right mantle stole / lapel sweeping smoothly down past codex
    mb.add_arc_pts("primary", (16.5, 23.5), (58.5, 76.0), 8.2)
    mb.add_arc_pts("primary", (35.8, 7.2), (67.5, 65.5), 7.6)

    # Crisp liturgical cloak drapery folds (detail)
    mb.add_arc_pts("detail", (-16.5, 15.2), (-46.0, 34.0), -2.2)
    mb.add_arc_pts("detail", (-48.5, 42.0), (-20.5, 43.0), -1.8)
    mb.add_arc_pts("detail", (-36.5, 24.5), (-14.5, 38.5), -1.8)
    mb.add_arc_pts("detail", (-48.5, 58.5), (-46.5, 79.0), -1.2)
    mb.add_arc_pts("detail", (-36.5, 56.5), (-37.5, 82.5), -1.2)
    mb.add_arc_pts("detail", (10.5, 24.5), (12.0, 44.5), 0.9)
    mb.add_arc_pts("detail", (28.5, 24.0), (47.0, 55.5), 2.0)
    mb.add_arc_pts("detail", (45.0, 18.0), (63.5, 47.0), 2.2)
    mb.add_arc_pts("detail", (40.5, 50.5), (47.0, 80.5), 1.4)

    # --- OPEN ARITHMETICA / MUSICA CODEX HELD AT CHEST ---
    # Central book spine
    mb.add_line("primary", 12.0, 46.5, 7.5, 84.0)
    # Left open page (top curved edge, outer page edge, and outer cover rim)
    mb.add_arc_pts("primary", (12.0, 46.5), (-10.5, 40.5), -3.2)
    mb.add_line("primary", -10.5, 40.5, -19.2, 82.0)
    mb.add_line("detail", -12.8, 42.2, -21.8, 82.5)
    # Right open page (top curved edge, outer page edge, and outer cover rim)
    mb.add_arc_pts("primary", (12.0, 46.5), (35.5, 48.2), 2.6)
    mb.add_line("primary", 35.5, 48.2, 31.2, 82.5)
    mb.add_line("detail", 37.8, 49.6, 33.6, 82.0)

    # Illuminated manuscript ruling lines across left & right codex pages
    for k in range(4):
        frac = 0.22 + 0.19 * k
        # Left page ruled text line
        lx1 = -10.5 + (-19.2 - (-10.5)) * frac + 3.2
        ly1 = 40.5 + (82.0 - 40.5) * frac
        lx2 = 12.0 + (7.5 - 12.0) * frac - 2.6
        ly2 = 46.5 + (84.0 - 46.5) * frac
        mb.add_arc_pts("detail", (lx1, ly1), (lx2, ly2), 1.4)
        # Right page ruled text line
        rx1 = 12.0 + (7.5 - 12.0) * frac + 2.6
        ry1 = 46.5 + (84.0 - 46.5) * frac
        rx2 = 35.5 + (31.2 - 35.5) * frac - 3.0
        ry2 = 48.2 + (82.5 - 48.2) * frac
        mb.add_arc_pts("detail", (rx1, ry1), (rx2, ry2), 1.2)

    return mb.build()


def build_nicomachus_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Nicomachus of Gerasa medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_nicomachus_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_nicomachus_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``nicomachus_dark.svg`` and ``nicomachus_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "nicomachus_dark.svg"
    light_path = target_dir / "nicomachus_light.svg"
    dark_path.write_text(
        build_nicomachus_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_nicomachus_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
