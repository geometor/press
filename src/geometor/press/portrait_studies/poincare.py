"""Study 22: Henri Poincare (after Eugene Pirou, Paris, 1887) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_poincare_elements",
    "build_poincare_svg",
    "write_poincare_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_orthogonal_disk_geodesic(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    disk_r: float,
    ang1_deg: float,
    ang2_deg: float,
) -> None:
    """Add an exact orthogonal circular-arc geodesic inside disk ``(cx, cy, disk_r)``.

    Connects two ideal boundary points at ``ang1_deg`` and ``ang2_deg`` with the
    unique circular arc meeting the boundary circle at exact right angles.
    """
    diff = ((ang2_deg - ang1_deg + 180.0) % 360.0) - 180.0
    half_rad = math.radians(0.5 * abs(diff))
    if abs(abs(diff) - 180.0) < 1e-3:
        a1 = math.radians(ang1_deg)
        a2 = math.radians(ang2_deg)
        mb.add_line(
            "golden",
            cx + disk_r * math.cos(a1),
            cy + disk_r * math.sin(a1),
            cx + disk_r * math.cos(a2),
            cy + disk_r * math.sin(a2),
        )
        return

    mid_rad = math.radians(ang1_deg + 0.5 * diff)
    d_center = disk_r / math.cos(half_rad)
    r_geo = disk_r * math.tan(half_rad)
    gcx = cx + d_center * math.cos(mid_rad)
    gcy = cy + d_center * math.sin(mid_rad)

    p1x = cx + disk_r * math.cos(math.radians(ang1_deg))
    p1y = cy + disk_r * math.sin(math.radians(ang1_deg))
    p2x = cx + disk_r * math.cos(math.radians(ang2_deg))
    p2y = cy + disk_r * math.sin(math.radians(ang2_deg))
    a1_geo = math.degrees(math.atan2(p1y - gcy, p1x - gcx))
    a2_geo = math.degrees(math.atan2(p2y - gcy, p2x - gcx))
    mb.add_arc("golden", gcx, gcy, r_geo, a1_geo, a2_geo)


def _add_poincare_disk_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 13.0,
) -> None:
    """Draw the Poincare hyperbolic disk with an ideal triangle and orthogonal geodesic.

    Constructs the unit boundary circle, three exact orthogonal geodesic arcs
    meeting at three ideal vertices spaced ``120 deg`` apart (``d = 2R``,
    ``r = R * sqrt(3)``), and a crossing orthogonal hyperbolic geodesic arc.
    """
    mb.add_circle("golden", cx, cy, radius)

    ideal_angles = (-90.0, 30.0, 150.0)
    for k in range(3):
        _add_orthogonal_disk_geodesic(
            mb,
            cx,
            cy,
            radius,
            ideal_angles[k],
            ideal_angles[(k + 1) % 3],
        )

    # Crossing orthogonal hyperbolic geodesic chord (ideal endpoints at 205 deg & -25 deg)
    _add_orthogonal_disk_geodesic(mb, cx, cy, radius, 205.0, -25.0)
    # Hyperbolic vertical symmetry diameter from apex ideal vertex
    mb.add_line("golden", cx, cy - radius, cx, cy + radius)

    # Ideal boundary vertex rings and hyperbolic center dot
    for ang_deg in ideal_angles:
        rad = math.radians(ang_deg)
        mb.add_circle("golden", cx + radius * math.cos(rad), cy + radius * math.sin(rad), 0.8)
    mb.add_circle("golden", cx, cy, 0.85, filled=True)


def _add_three_body_orbit_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.8,
) -> None:
    """Draw Poincare's three-body periodic orbit & homoclinic loop phase portrait.

    Combines two concentric phase circles with three internally tangent
    homoclinic circular loops meeting at the central hyperbolic saddle and
    three equilateral three-body / Lagrangian equilibrium nodes.
    """
    mb.add_circle("golden", cx, cy, radius)
    r_inner = 0.62 * radius
    mb.add_circle("golden", cx, cy, r_inner)

    r_lobe = 0.5 * radius
    node_angles = (-90.0, 30.0, 150.0)
    for ang_deg in node_angles:
        rad = math.radians(ang_deg)
        # Homoclinic loop tangent to outer circle & passing through central saddle
        lcx = cx + r_lobe * math.cos(rad)
        lcy = cy + r_lobe * math.sin(rad)
        mb.add_circle("golden", lcx, lcy, r_lobe)
        # Equilateral three-body node on outer tangency point
        nx = cx + radius * math.cos(rad)
        ny = cy + radius * math.sin(rad)
        mb.add_circle("golden", nx, ny, 0.95, filled=True)
        # Complementary Lagrangian node on inner phase ring (rotated 60 deg)
        lrad = math.radians(ang_deg + 60.0)
        mb.add_circle(
            "golden",
            cx + r_inner * math.cos(lrad),
            cy + r_inner * math.sin(lrad),
            0.68,
        )

    mb.add_circle("golden", cx, cy, 0.9, filled=True)


def build_poincare_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the four-layer compass-and-straightedge geometry for Henri Poincare.

    Uses ``MedallionBuilder`` so every line and circular arc is clipped cleanly
    within ``MED_R = 92.0`` with zero Bezier curves.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1 (Scaffold): Canonical medallion ring, eye line & golden circles
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-9.5,
        eye_rx=11.8,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Poincare Hyperbolic Disk (Left) & Three-Body Orbit (Right)
    # -------------------------------------------------------------------------
    _add_poincare_disk_motif(mb, cx=-64.0, cy=-26.0, radius=13.0)
    _add_three_body_orbit_motif(mb, cx=64.0, cy=-26.0, radius=12.8)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Rounded Cropped Hair, Short Fringe & Sculpted Left Ear
    # -------------------------------------------------------------------------
    # Rounded 1887 Parisian cropped hair crown silhouette (smooth convex arcs)
    mb.add_arc_pts("primary", (-34.8, -26.5), (-35.2, -43.0), 2.0)
    mb.add_arc_pts("primary", (-35.2, -43.0), (-25.0, -58.5), 2.6)
    mb.add_arc_pts("primary", (-25.0, -58.5), (-4.5, -66.0), 3.6)
    mb.add_arc_pts("primary", (-4.5, -66.0), (16.5, -59.0), 3.4)
    mb.add_arc_pts("primary", (16.5, -59.0), (22.2, -44.5), 2.2)
    mb.add_arc_pts("primary", (22.2, -44.5), (21.5, -37.5), 0.7)

    # Short straight combed fringe across broad forehead & left temple hairline
    mb.add_arc_pts("detail", (-25.5, -34.5), (-21.8, -46.2), 1.2)
    mb.add_arc_pts("detail", (-21.8, -46.2), (-2.0, -49.6), 2.0)
    mb.add_arc_pts("detail", (-2.0, -49.6), (15.8, -48.0), 1.6)
    mb.add_arc_pts("detail", (15.8, -48.0), (21.5, -42.0), 1.0)

    # Smooth short cropped hair & combed fringe waves
    mb.add_wave("detail", (-27.5, -50.8), (15.5, -52.5), 5, wave_angle_deg * 0.42, 1)
    mb.add_wave("detail", (-24.0, -57.2), (12.5, -58.2), 4, wave_angle_deg * 0.4, -1)
    mb.add_wave("detail", (-32.2, -42.5), (-26.8, -27.5), 3, wave_angle_deg * 0.45, 1)

    # Prominently sculpted left ear
    mb.add_arc_pts("primary", (-25.8, -27.5), (-34.2, -28.8), -1.8)
    mb.add_arc_pts("primary", (-34.2, -28.8), (-35.5, -20.5), -2.0)
    mb.add_arc_pts("primary", (-35.5, -20.5), (-31.5, -12.0), -1.6)
    mb.add_arc_pts("primary", (-31.5, -12.0), (-26.2, -9.8), -1.3)
    mb.add_arc_pts("primary", (-26.2, -9.8), (-23.8, -12.8), -0.8)
    mb.add_arc_pts("detail", (-27.4, -25.2), (-32.2, -22.2), -1.4)
    mb.add_arc_pts("detail", (-32.2, -22.2), (-29.5, -14.2), -1.3)
    mb.add_arc_pts("detail", (-26.2, -20.5), (-27.8, -17.5), -0.7)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Three-Quarter Right Face, Eyes, Straight Nose & Pointed Beard
    # -------------------------------------------------------------------------
    # Right facial contour (forehead -> orbit -> cheekbone -> beard)
    mb.add_arc_pts("primary", (21.5, -42.0), (21.8, -33.0), 0.9)
    mb.add_arc_pts("primary", (21.8, -33.0), (20.2, -26.5), -0.55)
    mb.add_arc_pts("primary", (20.2, -26.5), (21.2, -17.0), 1.0)
    mb.add_arc_pts("primary", (21.2, -17.0), (19.6, -7.5), 0.9)

    # Left temple & cheek descending into sideburn/beard
    mb.add_arc_pts("primary", (-25.8, -34.5), (-25.0, -24.5), -0.7)
    mb.add_arc_pts("primary", (-24.5, -14.0), (-23.2, -4.0), -0.8)

    # Thoughtful level French eyebrows
    mb.add_arc_pts("primary", (-19.2, -31.5), (-10.5, -33.2), 1.0)
    mb.add_arc_pts("primary", (-10.5, -33.2), (-2.2, -31.2), 0.9)
    mb.add_arc_pts("detail", (-18.4, -32.6), (-3.0, -32.4), 1.2)

    mb.add_arc_pts("primary", (5.2, -31.5), (12.5, -34.0), 1.1)
    mb.add_arc_pts("primary", (12.5, -34.0), (19.2, -32.2), 0.9)
    mb.add_arc_pts("detail", (5.8, -32.8), (18.4, -33.2), 1.1)

    # Thoughtful three-quarter right eyes right along y = -27
    # Viewer's left eye (nearer eye)
    l_out = (-16.0, -25.8)
    l_in = (-4.8, -26.5)
    mb.add_arc_pts("primary", l_out, l_in, 2.0)
    mb.add_arc_pts("detail", (-16.4, -28.4), (-4.4, -29.0), 1.9)
    mb.add_arc_pts("detail", l_out, l_in, -1.25)
    mb.add_circle("detail", -9.6, -26.2, 2.0)
    mb.add_circle("primary", -9.3, -26.2, 1.0, filled=True)
    mb.add_arc_pts("detail", (-15.2, -22.6), (-5.2, -23.0), -1.0)

    # Viewer's right eye (further eye)
    r_in = (6.0, -27.2)
    r_out = (16.4, -27.8)
    mb.add_arc_pts("primary", r_in, r_out, 1.9)
    mb.add_arc_pts("detail", (5.6, -29.6), (16.8, -30.2), 1.8)
    mb.add_arc_pts("detail", r_in, r_out, -1.1)
    mb.add_circle("detail", 11.6, -27.4, 1.85)
    mb.add_circle("primary", 11.9, -27.4, 0.92, filled=True)
    mb.add_arc_pts("detail", (6.4, -24.0), (15.8, -24.6), -0.95)

    # Classic straight sculpted nose
    mb.add_arc_pts("primary", (2.5, -31.2), (6.5, -20.5), -0.3)
    mb.add_arc_pts("primary", (6.5, -20.5), (9.8, -14.2), 0.4)
    mb.add_arc_pts("primary", (9.8, -14.2), (7.2, -11.4), 0.8)
    mb.add_arc_pts("primary", (7.2, -11.4), (2.2, -11.6), 0.5)
    mb.add_arc_pts("primary", (2.2, -11.6), (-1.5, -13.6), 0.7)
    mb.add_arc_pts("detail", (-1.5, -13.6), (-0.6, -16.8), 0.45)
    mb.add_arc_pts("detail", (-1.0, -25.8), (-0.4, -17.0), 0.28)
    mb.add_arc_pts("detail", (6.2, -12.8), (2.6, -13.0), -0.38)

    # Full neatly trimmed mustache & pointed Parisian professor's beard
    mb.add_arc_pts("primary", (3.8, -9.2), (-11.8, -2.5), -1.5)
    mb.add_arc_pts("primary", (3.8, -9.2), (15.5, -3.8), 1.4)
    mb.add_arc_pts("primary", (-4.8, -5.2), (4.0, -4.8), 0.38)
    mb.add_arc_pts("primary", (4.0, -4.8), (10.8, -5.8), -0.38)
    mb.add_arc_pts("detail", (-2.6, -2.4), (4.2, -2.0), -0.7)
    mb.add_arc_pts("detail", (4.2, -2.0), (8.6, -3.2), -0.45)

    # Cheek-to-beard transition line
    mb.add_arc_pts("detail", (-24.0, -13.5), (-16.2, -5.0), -1.1)
    mb.add_arc_pts("detail", (-16.2, -5.0), (-9.8, -2.5), -0.6)

    # Outer neatly trimmed pointed beard silhouette
    mb.add_arc_pts("primary", (-23.2, -4.0), (-19.8, 6.2), -1.2)
    mb.add_arc_pts("primary", (-19.8, 6.2), (-9.5, 14.2), -1.5)
    mb.add_arc_pts("primary", (-9.5, 14.2), (1.2, 17.0), -1.2)
    mb.add_arc_pts("primary", (1.2, 17.0), (13.0, 12.2), -1.5)
    mb.add_arc_pts("primary", (13.0, 12.2), (18.8, 2.0), -1.3)
    mb.add_arc_pts("primary", (18.8, 2.0), (19.6, -7.5), -0.85)

    # Disciplined trimmed beard wave texture (Euclid III.12 arcs)
    mb.add_wave("detail", (-19.0, -3.5), (-15.0, 9.8), 3, wave_angle_deg * 0.55, 1)
    mb.add_wave("detail", (-12.5, -1.8), (-7.8, 13.5), 3, wave_angle_deg * 0.55, -1)
    mb.add_wave("detail", (-4.8, -0.5), (-0.6, 15.5), 3, wave_angle_deg * 0.55, 1)
    mb.add_wave("detail", (3.8, -0.5), (6.5, 14.0), 3, wave_angle_deg * 0.55, -1)
    mb.add_wave("detail", (11.2, -2.5), (13.6, 9.5), 3, wave_angle_deg * 0.52, 1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Upturned Collar, Small Bow Tie & Broad Double-Breasted Coat
    # -------------------------------------------------------------------------
    # Neck & crisp upturned white collar
    mb.add_arc_pts("primary", (-23.8, 3.2), (-23.0, 10.5), -0.6)
    mb.add_arc_pts("primary", (-23.0, 10.5), (-11.5, 24.5), -1.5)
    mb.add_arc_pts("primary", (18.2, 8.0), (12.5, 19.5), 1.0)
    mb.add_arc_pts("detail", (-18.5, 11.5), (-4.5, 22.0), -1.2)
    mb.add_arc_pts("detail", (-4.5, 22.0), (11.5, 15.8), -1.0)

    # Neat small Parisian bow tie & crisp shirt front V
    mb.add_arc_pts("primary", (-4.8, 22.6), (0.6, 22.4), 0.5)
    mb.add_arc_pts("primary", (0.6, 22.4), (0.8, 27.2), 0.5)
    mb.add_arc_pts("primary", (0.8, 27.2), (-4.6, 27.4), 0.5)
    mb.add_arc_pts("primary", (-4.6, 27.4), (-4.8, 22.6), 0.5)
    # Left & right bow wings
    mb.add_arc_pts("primary", (-4.8, 22.6), (-12.8, 23.0), 1.0)
    mb.add_arc_pts("primary", (-12.8, 23.0), (-11.6, 29.5), -1.2)
    mb.add_arc_pts("primary", (-11.6, 29.5), (-4.6, 27.4), -0.8)
    mb.add_arc_pts("primary", (0.6, 22.4), (8.2, 20.6), 1.0)
    mb.add_arc_pts("primary", (8.2, 20.6), (9.0, 26.8), 1.2)
    mb.add_arc_pts("primary", (9.0, 26.8), (0.8, 27.2), 0.8)
    mb.add_line("detail", -10.8, 26.0, -5.2, 25.2)
    mb.add_line("detail", 1.4, 24.8, 7.2, 23.8)
    # Shirt front triangle visible beneath bow tie
    mb.add_line("primary", -11.5, 29.5, -4.5, 37.5)
    mb.add_line("primary", -4.5, 37.5, 3.8, 27.5)

    # Broad Parisian coat shoulders clipped razor-flush to MED_R = 92.0
    mb.add_arc_pts("primary", (-25.5, 8.5), (-56.5, 26.5), -3.2)
    mb.add_arc_pts("primary", (-56.5, 26.5), (-86.0, 76.0), -6.8)
    mb.add_arc_pts("primary", (19.5, 6.0), (52.5, 22.5), 3.4)
    mb.add_arc_pts("primary", (52.5, 22.5), (84.5, 69.0), 5.8)

    # Broad diagonal double-breasted Parisian coat lapels
    # Viewer's left notched lapel tucked beneath broad overlapping right lapel
    mb.add_arc_pts("primary", (-25.5, 8.5), (-28.0, 30.0), -1.4)
    mb.add_line("primary", -28.0, 30.0, -21.2, 31.8)
    mb.add_line("primary", -21.2, 31.8, -34.2, 37.5)
    mb.add_arc_pts("primary", (-34.2, 37.5), (-11.5, 51.8), -2.2)
    mb.add_arc_pts("detail", (-21.0, 32.0), (-8.5, 48.0), -1.2)

    # Viewer's right broad diagonal overlapping double-breasted lapel
    mb.add_arc_pts("primary", (19.5, 6.0), (21.5, 21.8), 1.2)
    mb.add_line("primary", 21.5, 21.8, 14.5, 23.8)
    mb.add_line("primary", 14.5, 23.8, 24.2, 30.5)
    mb.add_arc_pts("primary", (24.2, 30.5), (-11.5, 51.8), 2.8)
    mb.add_arc_pts("primary", (-11.5, 51.8), (-42.0, 88.0), 3.2)

    # Inner double-breasted lapel roll crease & tailored coat details
    mb.add_arc_pts("detail", (13.8, 24.5), (-16.0, 52.5), 2.2)
    mb.add_arc_pts("detail", (-16.0, 52.5), (-32.0, 85.0), 1.8)
    mb.add_line("detail", 10.5, 31.0, 15.8, 33.8)
    mb.add_circle("detail", 11.5, 63.5, 2.0)
    mb.add_circle("detail", -1.5, 76.5, 2.0)

    # Coat sleeve & chest drapery folds clipped flush to MED_R = 92.0
    mb.add_arc_pts("detail", (-52.0, 34.0), (-67.5, 80.0), -3.4)
    mb.add_arc_pts("detail", (-40.5, 42.0), (-53.0, 84.0), -2.5)
    mb.add_arc_pts("detail", (36.5, 24.0), (52.5, 80.5), 3.2)
    mb.add_arc_pts("detail", (52.5, 34.0), (72.5, 73.0), 3.0)
    mb.add_arc_pts("detail", (22.5, 48.0), (35.5, 87.0), 2.2)

    return mb.build()


def build_poincare_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Henri Poincare medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_poincare_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_poincare_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``poincare_dark.svg`` and ``poincare_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "poincare_dark.svg"
    light_path = target_dir / "poincare_light.svg"
    dark_path.write_text(
        build_poincare_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_poincare_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
