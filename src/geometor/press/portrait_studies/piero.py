"""Study 17: Piero della Francesca (after Santi di Tito, c. 1590) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_piero_elements",
    "build_piero_svg",
    "write_piero_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _intersect_lines(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> tuple[float, float]:
    """Compute exact intersection of straight lines ``p1-p2`` and ``p3-p4``."""
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


def _add_perspective_grid_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Piero's *De Prospectiva Pingendi* one-point perspective floor grid.

    Uses exact projective intersections between orthogonal recession rays to
    central vanishing point ``V`` and a diagonal transversal to distance point
    ``D`` on the horizon line to generate mathematically foreshortened rows.
    """
    y_horizon = cy - 10.5
    y_base = cy + 12.2
    half_h = 14.2
    half_base = 11.6

    # Horizon line, central vanishing point V, and distance point D
    v_pt = (cx, y_horizon)
    d_pt = (cx + half_h, y_horizon)
    mb.add_line("golden", cx - half_h, y_horizon, d_pt[0], d_pt[1])

    # Five equally spaced baseline points on the front floor edge
    base_pts = [(cx - half_base + (2.0 * half_base) * (k / 4.0), y_base) for k in range(5)]
    mb.add_line("golden", base_pts[0][0], y_base, base_pts[-1][0], y_base)

    # Diagonal distance-point transversal from front-left corner to distance point D
    mb.add_line("golden", base_pts[0][0], y_base, d_pt[0], d_pt[1])

    # Compute exact foreshortened horizontal depths where diagonal meets each recession ray
    y_depths: list[float] = []
    for k in range(1, 5):
        ix, iy = _intersect_lines(base_pts[0], d_pt, base_pts[k], v_pt)
        y_depths.append(iy)
        mb.add_circle("golden", ix, iy, 0.7)

    # Back-most tile edge (clipped cleanly at deepest perspective row y_depths[-1])
    y_back = y_depths[-1]
    for bp in base_pts:
        # Draw full recession ray up to vanishing point V
        mb.add_line("golden", bp[0], bp[1], v_pt[0], v_pt[1])

    # Draw exact horizontal perspective floor rows spanning left-to-right outer rays
    for y_row in y_depths:
        lx, _ = _intersect_lines(base_pts[0], v_pt, (cx - 20.0, y_row), (cx + 20.0, y_row))
        rx, _ = _intersect_lines(base_pts[-1], v_pt, (cx - 20.0, y_row), (cx + 20.0, y_row))
        mb.add_line("golden", lx, y_row, rx, y_row)

    _ = y_back
    mb.add_circle("golden", v_pt[0], v_pt[1], 1.15, filled=True)
    mb.add_circle("golden", d_pt[0], d_pt[1], 0.9)


def _add_platonic_dual_solid_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 13.6,
) -> None:
    """Draw Piero's *De Quinque Corporibus Regularibus* dual Octahedron-in-Cube in a Sphere.

    Projects an exact 3D regular cube inscribed in the golden sphere together with
    its dual regular octahedron connecting all six cube face centers.
    """
    mb.add_circle("golden", cx, cy, radius)

    yaw = math.radians(26.0)
    pitch = math.radians(19.0)
    cos_y, sin_y = math.cos(yaw), math.sin(yaw)
    cos_p, sin_p = math.cos(pitch), math.sin(pitch)

    def proj(x: float, y: float, z: float) -> tuple[float, float]:
        xr = x * cos_y + z * sin_y
        zr = -x * sin_y + z * cos_y
        yr = y * cos_p - zr * sin_p
        return (cx + xr * radius, cy - yr * radius)

    # Inscribed cube vertices on unit sphere: (+-1, +-1, +-1) / sqrt(3)
    inv_s3 = 1.0 / math.sqrt(3.0)
    cube_3d = [
        (sx * inv_s3, sy * inv_s3, sz * inv_s3)
        for sx in (-1.0, 1.0)
        for sy in (-1.0, 1.0)
        for sz in (-1.0, 1.0)
    ]
    cube_2d = [proj(*v) for v in cube_3d]
    cube_edges = (
        (0, 1), (0, 2), (0, 4),
        (1, 3), (1, 5),
        (2, 3), (2, 6),
        (3, 7),
        (4, 5), (4, 6),
        (5, 7), (6, 7),
    )
    for i, j in cube_edges:
        mb.add_line("golden", cube_2d[i][0], cube_2d[i][1], cube_2d[j][0], cube_2d[j][1])

    # Dual regular octahedron vertices at exact centers of all 6 cube faces
    oct_3d = (
        (inv_s3, 0.0, 0.0),
        (-inv_s3, 0.0, 0.0),
        (0.0, inv_s3, 0.0),
        (0.0, -inv_s3, 0.0),
        (0.0, 0.0, inv_s3),
        (0.0, 0.0, -inv_s3),
    )
    oct_2d = [proj(*v) for v in oct_3d]
    for i in range(6):
        for j in range(i + 1, 6):
            # Connect non-opposite vertices (opposite pairs are (0,1), (2,3), (4,5))
            if i // 2 != j // 2:
                mb.add_line("golden", oct_2d[i][0], oct_2d[i][1], oct_2d[j][0], oct_2d[j][1])

    for vx, vy in oct_2d:
        mb.add_circle("golden", vx, vy, 0.75)
    mb.add_circle("golden", cx, cy, 0.95, filled=True)


def build_piero_elements(wave_angle_deg: float = 32.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Piero della Francesca medallion strictly from lines, circles, and circular arcs.

    Calibrated to Santi di Tito's c. 1590 civic portrait (Museo Civico di Sansepolcro),
    featuring Piero's rounded Renaissance cap (*berretto*) with rolled fur brim over
    short curly bangs, calm three-quarter right gaze, strong nose, composed lips,
    crisp white collar rim, and voluminous dark fur-trimmed scholar's robe.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 fur-brim & lapel texture waves.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-5.8,
        eye_rx=13.5,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Perspective Grid (Left) & Platonic Dual Solid (Right)
    # -------------------------------------------------------------------------
    _add_perspective_grid_motif(mb, cx=-63.0, cy=-26.0)
    _add_platonic_dual_solid_motif(mb, cx=63.0, cy=-26.0, radius=13.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Renaissance Civic Cap (Berretto), Fur Brim & Curly Bangs
    # -------------------------------------------------------------------------
    # Rounded crimson civic cap crown
    mb.add_arc_pts("primary", (-24.5, -55.5), (-18.0, -68.5), 2.4)
    mb.add_arc_pts("primary", (-18.0, -68.5), (12.5, -70.0), 4.8)
    mb.add_arc_pts("primary", (12.5, -70.0), (21.5, -57.5), 2.2)
    mb.add_arc_pts("detail", (-10.0, -70.5), (7.0, -69.5), -1.0)

    # Rolled fur cap brim framing the forehead
    mb.add_arc_pts("primary", (-26.5, -53.2), (22.0, -56.5), 6.2)
    mb.add_arc_pts("primary", (-26.5, -53.2), (-23.8, -46.8), -1.4)
    mb.add_arc_pts("primary", (-23.8, -46.8), (20.8, -50.2), 5.6)
    mb.add_arc_pts("primary", (20.8, -50.2), (22.0, -56.5), -1.4)
    mb.add_wave("detail", (-21.5, -51.0), (18.5, -53.2), 5, wave_angle_deg * 0.72, 1)

    # Short curly Renaissance bangs & left temple hair peeking beneath cap brim
    mb.add_arc_pts("primary", (-23.5, -43.5), (-14.5, -47.6), 1.3)
    mb.add_arc_pts("primary", (-14.5, -47.6), (-4.0, -49.0), 1.1)
    mb.add_arc_pts("primary", (-4.0, -49.0), (3.8, -45.0), -1.3)
    mb.add_arc_pts("primary", (3.8, -45.0), (12.2, -48.2), -1.0)
    mb.add_arc_pts("primary", (12.2, -48.2), (18.8, -45.5), 0.9)
    mb.add_arc_pts("primary", (-24.0, -46.8), (-28.5, -38.5), -1.6)
    mb.add_arc_pts("primary", (-28.5, -38.5), (-26.5, -31.2), -1.3)
    mb.add_wave("detail", (-19.5, -49.2), (15.5, -50.2), 4, wave_angle_deg * 0.65, -1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Three-Quarter Right Renaissance Face, Eyes, Nose, Lips & Ear
    # -------------------------------------------------------------------------
    # Right three-quarter facial profile contour
    mb.add_arc_pts("primary", (18.8, -45.5), (20.8, -35.5), 1.0)
    mb.add_arc_pts("primary", (20.8, -35.5), (19.8, -28.0), -0.6)
    mb.add_arc_pts("primary", (19.8, -28.0), (20.6, -17.0), 1.1)
    mb.add_arc_pts("primary", (20.6, -17.0), (18.2, -5.8), 1.3)
    mb.add_arc_pts("primary", (18.2, -5.8), (11.5, 2.5), 1.5)
    mb.add_arc_pts("primary", (11.5, 2.5), (5.5, 4.5), 1.0)

    # Smooth rounded oval chin & left jawline rising to left ear
    mb.add_arc_pts("primary", (5.5, 4.5), (-7.5, 3.8), 1.6)
    mb.add_arc_pts("primary", (-7.5, 3.8), (-18.5, -2.5), 1.6)
    mb.add_arc_pts("primary", (-18.5, -2.5), (-24.5, -14.5), 1.5)
    mb.add_arc_pts("primary", (-24.5, -14.5), (-25.0, -29.5), 1.0)
    mb.add_arc_pts("primary", (-25.0, -29.5), (-23.5, -43.5), 0.9)

    # Sculpted left ear
    mb.add_arc_pts("primary", (-25.0, -31.5), (-32.8, -30.5), -1.8)
    mb.add_arc_pts("primary", (-32.8, -30.5), (-31.6, -19.2), -1.8)
    mb.add_arc_pts("primary", (-31.6, -19.2), (-26.6, -14.2), -1.4)
    mb.add_arc_pts("primary", (-26.6, -14.2), (-23.8, -17.0), -0.9)
    mb.add_arc_pts("detail", (-26.2, -27.5), (-29.8, -24.2), -1.2)
    mb.add_arc_pts("detail", (-29.8, -24.2), (-27.2, -17.5), -1.2)

    # Clean arched Renaissance eyebrows & subtle glabella crease
    mb.add_arc_pts("primary", (-15.5, -31.8), (-6.5, -34.4), 1.3)
    mb.add_arc_pts("primary", (-6.5, -34.4), (1.8, -31.2), 1.1)
    mb.add_arc_pts("detail", (-14.5, -33.2), (1.0, -32.6), 1.4)

    mb.add_arc_pts("primary", (8.2, -31.8), (14.8, -34.6), 1.1)
    mb.add_arc_pts("primary", (14.8, -34.6), (20.2, -33.0), 0.9)
    mb.add_arc_pts("detail", (4.5, -35.8), (5.2, -30.5), 0.3)

    # Serene direct Tuscan eyes right along y = -27
    # Viewer's left eye (nearer eye)
    l_out = (-11.8, -26.5)
    l_in = (0.0, -26.5)
    mb.add_arc_pts("primary", l_out, l_in, 2.2)
    mb.add_arc_pts("detail", (-12.2, -29.2), (0.4, -29.0), 2.1)
    mb.add_arc_pts("detail", l_out, l_in, -1.3)
    mb.add_circle("detail", -5.8, -26.5, 2.0)
    mb.add_circle("primary", -5.6, -26.5, 1.0, filled=True)
    mb.add_arc_pts("detail", (-11.2, -23.0), (-0.2, -23.0), -1.1)

    # Viewer's right eye (further eye)
    r_in = (8.5, -26.8)
    r_out = (18.5, -27.2)
    mb.add_arc_pts("primary", r_in, r_out, 2.0)
    mb.add_arc_pts("detail", (8.2, -29.4), (18.8, -29.6), 2.0)
    mb.add_arc_pts("detail", r_in, r_out, -1.2)
    mb.add_circle("detail", 13.5, -26.9, 1.85)
    mb.add_circle("primary", 13.7, -26.9, 0.95, filled=True)
    mb.add_arc_pts("detail", (8.8, -23.6), (18.0, -24.0), -1.0)

    # Refined sculptural Quattrocento nose
    mb.add_arc_pts("primary", (5.2, -31.2), (8.0, -21.5), -0.35)
    mb.add_arc_pts("primary", (8.0, -21.5), (10.8, -14.5), 0.5)
    mb.add_arc_pts("detail", (2.2, -25.2), (2.5, -16.5), 0.35)
    mb.add_arc_pts("primary", (10.8, -14.5), (8.2, -11.6), 0.9)
    mb.add_arc_pts("primary", (8.2, -11.6), (3.5, -11.5), 0.6)
    mb.add_arc_pts("primary", (3.5, -11.5), (0.4, -13.8), 0.75)
    mb.add_arc_pts("detail", (0.4, -13.8), (1.2, -16.8), 0.5)
    mb.add_arc_pts("detail", (7.4, -12.6), (3.8, -12.8), -0.45)

    # Composed Renaissance lips & smooth chin
    mb.add_arc_pts("detail", (5.8, -10.8), (6.2, -7.8), -0.3)
    mb.add_arc_pts("detail", (-0.8, -6.2), (5.8, -7.2), 0.7)
    mb.add_arc_pts("detail", (5.8, -7.2), (11.8, -6.5), 0.6)
    mb.add_arc_pts("primary", (-1.0, -5.5), (5.8, -5.2), 0.45)
    mb.add_arc_pts("primary", (5.8, -5.2), (12.2, -5.8), -0.45)
    mb.add_arc_pts("detail", (0.8, -3.2), (6.0, -2.4), -0.8)
    mb.add_arc_pts("detail", (6.0, -2.4), (10.5, -3.4), -0.5)
    mb.add_arc_pts("detail", (2.2, 0.2), (8.2, 0.0), -0.65)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Crisp White Collar Rim & Fur-Trimmed Civic Scholar's Robe
    # -------------------------------------------------------------------------
    # Neck & crisp white inner collar band
    mb.add_arc_pts("primary", (-22.0, -5.0), (-26.5, 4.5), -0.7)
    mb.add_arc_pts("primary", (10.5, 3.5), (8.2, 11.8), 0.6)
    mb.add_arc_pts("primary", (-26.0, 3.8), (-4.5, 14.2), -1.8)
    mb.add_arc_pts("primary", (-4.5, 14.2), (8.5, 11.2), -1.2)
    mb.add_arc_pts("detail", (-24.5, 2.2), (-4.5, 12.2), -1.6)
    mb.add_arc_pts("detail", (-4.5, 12.2), (7.5, 9.5), -1.0)

    # Voluminous civic scholar's robe shoulders clipped flush to MED_R
    mb.add_arc_pts("primary", (-26.5, 4.5), (-82.5, 66.0), -8.2)
    mb.add_arc_pts("primary", (8.5, 11.2), (80.0, 72.0), 7.6)

    # Iconic fur-trimmed scalloped collar flap & broad vertical fur borders (flush joins!)
    # Left fur shoulder lapel & vertical front trim meeting left shoulder cleanly
    mb.add_arc_pts("primary", (-56.8, 30.2), (-38.0, 42.5), -2.0)
    mb.add_arc_pts("primary", (-38.0, 42.5), (-14.5, 33.5), -1.8)
    mb.add_arc_pts("primary", (-14.5, 33.5), (-9.5, 86.5), 2.0)

    mb.add_arc_pts("primary", (-61.2, 36.2), (-38.5, 49.0), -2.0)
    mb.add_arc_pts("primary", (-38.5, 49.0), (-20.0, 40.5), -1.6)
    mb.add_arc_pts("primary", (-20.0, 40.5), (-16.5, 86.5), 1.8)
    # Soft fur waves inside left lapel & vertical border
    mb.add_wave("detail", (-54.5, 34.0), (-38.5, 45.4), 3, wave_angle_deg * 0.65, 1)
    mb.add_wave("detail", (-36.5, 44.5), (-18.5, 37.5), 3, wave_angle_deg * 0.65, -1)
    mb.add_wave("detail", (-17.2, 41.0), (-13.0, 85.0), 5, wave_angle_deg * 0.65, 1)

    # Right fur shoulder flap & broad vertical front trim meeting collar & shoulder flush
    mb.add_arc_pts("primary", (8.5, 11.2), (22.5, 35.5), 1.5)
    mb.add_arc_pts("primary", (22.5, 35.5), (42.5, 83.0), 2.4)
    mb.add_arc_pts("primary", (14.5, 14.5), (28.0, 33.5), 1.2)
    mb.add_arc_pts("primary", (28.0, 33.5), (51.5, 40.2), -1.4)
    mb.add_arc_pts("primary", (28.0, 40.5), (58.2, 46.8), -1.5)
    mb.add_arc_pts("primary", (28.0, 40.5), (48.5, 80.5), 2.2)
    # Soft fur waves inside right vertical border & shoulder flap
    mb.add_wave("detail", (25.5, 38.0), (45.2, 80.5), 5, wave_angle_deg * 0.65, -1)
    mb.add_wave("detail", (30.5, 37.5), (51.5, 42.5), 3, wave_angle_deg * 0.6, 1)

    # Center civic doublet pleats & outer robe folds (strictly non-crossing detail)
    mb.add_arc_pts("detail", (-3.5, 16.5), (1.5, 86.0), 1.4)
    mb.add_arc_pts("detail", (6.5, 16.5), (16.5, 85.0), 1.8)
    mb.add_arc_pts("detail", (-44.0, 49.0), (-49.5, 80.5), -1.8)
    mb.add_arc_pts("detail", (-62.5, 47.0), (-68.5, 73.5), -1.8)
    mb.add_arc_pts("detail", (52.5, 49.0), (64.5, 75.5), 2.0)

    return mb.build()


def build_piero_svg(theme: str = "dark", wave_angle_deg: float = 32.0) -> str:
    """Render the Piero della Francesca medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_piero_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_piero_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 32.0,
) -> tuple[Path, Path]:
    """Write ``piero_dark.svg`` and ``piero_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "piero_dark.svg"
    light_path = target_dir / "piero_light.svg"
    dark_path.write_text(
        build_piero_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_piero_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
