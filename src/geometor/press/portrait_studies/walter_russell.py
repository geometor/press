"""Study 25: Walter Russell (after archival circular studio portrait) in lines and arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_walter_russell_elements",
    "build_walter_russell_svg",
    "write_walter_russell_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_wave_field_octave_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.6,
) -> None:
    """Draw Walter Russell's concentric wave-field octave & standing sine wave (Euclid III.12).

    Constructs a horizontal equilibrium axis crossed by twin counter-phase
    G1-smooth tangent circular waves (``mb.add_wave``), concentric wave-crest
    circles around both antinodes, and three marked octave stillness nodes.
    """
    # Outer octave boundary circle, inner octave ring & horizontal equilibrium axis
    mb.add_circle("golden", cx, cy, radius)
    mb.add_circle("golden", cx, cy, 0.56 * radius)
    p_left = (cx - radius, cy)
    p_right = (cx + radius, cy)
    mb.add_line("golden", p_left[0], p_left[1], p_right[0], p_right[1])

    # Crisp full-amplitude G1-smooth standing sine wave (Euclid III.12 tangent arcs)
    mb.add_wave("golden", p_left, p_right, 2, 88.0, 1)
    mb.add_wave("golden", p_left, p_right, 4, 48.0, -1)

    # Concentric wave-crest octave circles seated cleanly on the positive & negative crests
    half_r = 0.5 * radius
    mb.add_circle("golden", cx - half_r, cy - 4.2, 2.2)
    mb.add_circle("golden", cx + half_r, cy + 4.2, 2.2)

    # Three marked zero-stillness wave-octave nodes along the equilibrium axis
    mb.add_circle("golden", p_left[0], p_left[1], 0.85, filled=True)
    mb.add_circle("golden", cx, cy, 1.0, filled=True)
    mb.add_circle("golden", p_right[0], p_right[1], 0.85, filled=True)


def _add_cubic_wave_field_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.6,
) -> None:
    """Draw Walter Russell's Cubic Wave-Field & Inscribed Sphere dual orthographic projection.

    Projects an exact cube of half-edge ``a = R / sqrt(3)`` inside its
    circumscribed sphere ``R``, paired with the inner inscribed sphere ``r = a``
    and three mutually orthogonal axial diameters meeting at the zero-stillness
    fulcrum center.
    """
    mb.add_circle("golden", cx, cy, radius)
    half_edge = radius / math.sqrt(3.0)
    mb.add_circle("golden", cx, cy, half_edge)

    # Crisp orthographic 3D rotation (yaw = 28 deg, pitch = 20 deg)
    yaw = math.radians(28.0)
    pitch = math.radians(20.0)
    cyaw, syaw = math.cos(yaw), math.sin(yaw)
    cpit, spit = math.cos(pitch), math.sin(pitch)

    def proj(x: float, y: float, z: float) -> tuple[float, float]:
        xr = x * cyaw + z * syaw
        zr = -x * syaw + z * cyaw
        yr = y * cpit - zr * spit
        return (cx + xr, cy - yr)

    # Project all 8 cube vertices and draw all 12 cube edges
    verts = [
        proj(sx * half_edge, sy * half_edge, sz * half_edge)
        for sx in (-1.0, 1.0)
        for sy in (-1.0, 1.0)
        for sz in (-1.0, 1.0)
    ]
    edges = (
        (0, 1), (2, 3), (4, 5), (6, 7),
        (0, 2), (1, 3), (4, 6), (5, 7),
        (0, 4), (1, 5), (2, 6), (3, 7),
    )
    for i, j in edges:
        mb.add_line("golden", verts[i][0], verts[i][1], verts[j][0], verts[j][1])

    # Three mutually orthogonal axial diameters extending through face centers
    axis_len = half_edge * 1.18
    for ax, ay, az in ((axis_len, 0.0, 0.0), (0.0, axis_len, 0.0), (0.0, 0.0, axis_len)):
        p_neg = proj(-ax, -ay, -az)
        p_pos = proj(ax, ay, az)
        mb.add_line("golden", p_neg[0], p_neg[1], p_pos[0], p_pos[1])
        mb.add_circle("golden", p_pos[0], p_pos[1], 0.58)

    # Central zero-stillness fulcrum dot
    mb.add_circle("golden", cx, cy, 0.95, filled=True)


def build_walter_russell_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the four-layer compass-and-straightedge geometry for Walter Russell.

    Uses ``MedallionBuilder`` so every line and circular arc is clipped cleanly
    within ``MED_R = 92.0`` with zero Bezier curves.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1 (Scaffold): Canonical medallion ring, eye line & golden circles
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-3.2,
        eye_rx=14.2,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Wave-Field Octave (Left) & Cubic Wave-Field (Right)
    # -------------------------------------------------------------------------
    _add_wave_field_octave_motif(mb, cx=-64.5, cy=-28.0, radius=12.6)
    _add_cubic_wave_field_motif(mb, cx=64.0, cy=-28.0, radius=12.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Noble Domed Cranium, Swept Side Hair & Sculpted Left Ear
    # -------------------------------------------------------------------------
    # Seamless single-sweep high noble domed forehead & cranium
    mb.add_arc_pts("primary", (-25.5, -53.0), (15.0, -50.2), 10.0)
    mb.add_arc_pts("primary", (15.0, -50.2), (18.8, -34.5), 1.8)

    # Swept dark side hair framing left temple & behind ear
    mb.add_arc_pts("primary", (-35.2, -28.0), (-33.8, -42.5), 2.0)
    mb.add_arc_pts("primary", (-33.8, -42.5), (-25.5, -53.0), 1.6)
    mb.add_arc_pts("primary", (-35.2, -19.5), (-34.0, -12.5), 0.9)
    mb.add_arc_pts("detail", (-25.5, -53.0), (-20.8, -43.5), 1.4)
    mb.add_arc_pts("detail", (-20.8, -43.5), (-26.5, -28.5), -1.4)
    mb.add_wave("detail", (-31.8, -45.5), (-25.2, -32.0), 3, wave_angle_deg * 0.5, 1)
    mb.add_wave("detail", (-29.2, -50.0), (-22.8, -38.5), 3, wave_angle_deg * 0.45, -1)

    # Prominently sculpted sunlit left ear
    mb.add_arc_pts("primary", (-26.5, -34.2), (-33.8, -36.5), -1.8)
    mb.add_arc_pts("primary", (-33.8, -36.5), (-35.5, -28.0), -2.0)
    mb.add_arc_pts("primary", (-35.5, -28.0), (-31.5, -19.5), -1.6)
    mb.add_arc_pts("primary", (-31.5, -19.5), (-26.2, -17.2), -1.3)
    mb.add_arc_pts("primary", (-26.2, -17.2), (-24.0, -20.0), -0.8)
    mb.add_arc_pts("detail", (-28.0, -32.2), (-32.4, -29.0), -1.4)
    mb.add_arc_pts("detail", (-32.4, -29.0), (-29.5, -21.8), -1.3)
    mb.add_arc_pts("detail", (-26.2, -27.5), (-27.8, -24.5), -0.7)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Three-Quarter Right Face, Shadowed Gaze, Nose & Mustache
    # -------------------------------------------------------------------------
    # Right facial contour & left sunlit cheek/jawline down to chin
    mb.add_arc_pts("primary", (18.8, -34.5), (17.8, -27.2), -0.5)
    mb.add_arc_pts("primary", (17.8, -27.2), (19.0, -18.0), 0.9)
    mb.add_arc_pts("primary", (19.0, -18.0), (17.8, -8.5), 0.9)

    mb.add_arc_pts("primary", (-25.2, -18.2), (-23.8, -8.5), -0.9)
    mb.add_arc_pts("primary", (-23.8, -8.5), (-16.8, 1.5), -1.4)
    mb.add_arc_pts("primary", (-16.8, 1.5), (-5.8, 8.8), -1.6)
    mb.add_arc_pts("primary", (-5.8, 8.8), (4.8, 10.6), -1.5)
    mb.add_arc_pts("primary", (4.8, 10.6), (11.2, 8.2), -1.0)

    # Strong visionary brows & subtle forehead contemplation lines
    mb.add_arc_pts("detail", (-11.0, -40.5), (11.5, -39.5), 1.6)
    mb.add_arc_pts("primary", (-12.2, -31.8), (-3.5, -34.0), 1.1)
    mb.add_arc_pts("primary", (-3.5, -34.0), (4.2, -31.5), 1.0)
    mb.add_arc_pts("detail", (-11.2, -33.0), (3.2, -32.8), 1.2)

    mb.add_arc_pts("primary", (8.8, -31.8), (14.8, -33.8), 1.0)
    mb.add_arc_pts("primary", (14.8, -33.8), (19.8, -31.5), 0.9)

    # Deeply shaded contemplative eyes reconstructed cleanly along y = -27
    # Viewer's left eye (nearer eye)
    l_out = (-9.6, -26.2)
    l_in = (2.0, -26.5)
    mb.add_arc_pts("primary", l_out, l_in, 1.95)
    mb.add_arc_pts("detail", (-10.2, -29.2), (2.6, -29.4), 2.0)
    mb.add_arc_pts("detail", l_out, l_in, -1.25)
    mb.add_circle("detail", -3.2, -26.4, 1.95)
    mb.add_circle("primary", -2.9, -26.4, 0.96, filled=True)
    mb.add_arc_pts("detail", (-9.2, -22.8), (1.8, -23.0), -1.1)

    # Viewer's right eye (further eye in dramatic shadow)
    r_in = (9.6, -26.8)
    r_out = (18.6, -27.2)
    mb.add_arc_pts("primary", r_in, r_out, 1.75)
    mb.add_arc_pts("detail", (9.2, -29.4), (19.0, -29.6), 1.8)
    mb.add_arc_pts("detail", r_in, r_out, -1.1)
    mb.add_circle("detail", 14.2, -27.0, 1.78)
    mb.add_circle("primary", 14.5, -27.0, 0.88, filled=True)
    mb.add_arc_pts("detail", (10.0, -23.6), (18.2, -24.0), -1.0)

    # Strong sculpted nose
    mb.add_arc_pts("primary", (5.5, -31.0), (10.2, -20.5), -0.35)
    mb.add_arc_pts("primary", (10.2, -20.5), (13.4, -14.8), 0.45)
    mb.add_arc_pts("primary", (13.4, -14.8), (10.5, -11.4), 0.85)
    mb.add_arc_pts("primary", (10.5, -11.4), (5.0, -11.6), 0.55)
    mb.add_arc_pts("primary", (5.0, -11.6), (1.0, -13.8), 0.75)
    mb.add_arc_pts("detail", (1.0, -13.8), (1.8, -17.0), 0.5)
    mb.add_arc_pts("detail", (2.4, -25.8), (2.8, -17.2), 0.3)
    mb.add_arc_pts("detail", (9.4, -12.8), (5.4, -13.0), -0.4)

    # Neatly trimmed mustache & calm composed mouth/chin
    mb.add_arc_pts("primary", (6.2, -9.8), (-6.8, -6.2), -1.5)
    mb.add_arc_pts("primary", (6.2, -9.8), (13.5, -7.8), 1.1)
    mb.add_arc_pts("detail", (-6.2, -6.2), (12.6, -6.6), 0.9)
    mb.add_wave("detail", (-5.5, -7.2), (11.5, -7.8), 3, wave_angle_deg * 0.42, 1)
    mb.add_arc_pts("primary", (-3.8, -4.4), (10.8, -5.0), 0.55)
    mb.add_arc_pts("detail", (-1.5, -2.0), (5.2, -1.6), -0.7)
    mb.add_arc_pts("detail", (5.2, -1.6), (9.2, -2.6), -0.5)
    mb.add_arc_pts("detail", (-0.5, 3.2), (6.8, 3.0), -0.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Thoughtful Hand Resting Near Chin/Jaw
    # -------------------------------------------------------------------------
    # Index finger resting smoothly near right cheek/jaw
    mb.add_arc_pts("primary", (12.5, -5.2), (19.8, -5.2), 1.0)
    mb.add_arc_pts("primary", (19.8, -5.2), (21.6, -2.0), 0.9)
    mb.add_arc_pts("primary", (21.6, -2.0), (11.8, 4.4), -0.9)
    # Middle finger curled below
    mb.add_arc_pts("primary", (19.8, -1.8), (24.6, 1.4), 0.8)
    mb.add_arc_pts("primary", (24.6, 1.4), (24.2, 4.8), 0.8)
    mb.add_arc_pts("primary", (24.2, 4.8), (13.0, 10.6), -0.9)
    # Ring finger curled below
    mb.add_arc_pts("primary", (22.5, 5.2), (26.6, 8.2), 0.8)
    mb.add_arc_pts("primary", (26.6, 8.2), (25.5, 11.8), 0.8)
    mb.add_arc_pts("primary", (25.5, 11.8), (15.5, 16.8), -0.8)
    # Outer palm & wrist descending smoothly into right coat sleeve
    mb.add_arc_pts("primary", (25.5, 11.8), (28.5, 24.5), 1.4)
    mb.add_arc_pts("primary", (28.5, 24.5), (24.2, 34.5), 1.0)
    mb.add_arc_pts("primary", (11.2, 8.2), (11.8, 19.5), -0.9)
    mb.add_arc_pts("primary", (11.8, 19.5), (15.2, 30.5), -0.8)
    mb.add_arc_pts("detail", (16.5, 18.0), (23.2, 13.5), 0.7)
    mb.add_arc_pts("detail", (18.5, 24.5), (25.2, 20.5), 0.7)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Crisp White Collar & Mid-Century Dark Suit (Clipped to MED_R)
    # -------------------------------------------------------------------------
    # Diagonal crisp white shirt collar & knotted mid-century necktie
    mb.add_arc_pts("primary", (-34.0, -12.5), (-18.5, 2.5), -1.2)
    mb.add_arc_pts("primary", (-18.5, 2.5), (-4.5, 15.8), -1.4)
    mb.add_arc_pts("primary", (-4.5, 15.8), (11.5, 20.8), -1.2)
    mb.add_arc_pts("primary", (-36.5, -8.5), (-20.2, 7.2), -1.4)
    mb.add_arc_pts("primary", (-20.2, 7.2), (-6.2, 21.8), -1.4)
    mb.add_arc_pts("primary", (-6.2, 21.8), (12.2, 26.8), -1.2)
    mb.add_line("primary", -34.0, -12.5, -36.5, -8.5)
    # Classic knotted necktie tapering neatly between collar & lapels
    mb.add_line("primary", -4.2, 22.8, 0.4, 30.8)
    mb.add_line("primary", 5.8, 25.6, 0.4, 30.8)
    mb.add_line("primary", -2.2, 29.2, -5.8, 49.5)
    mb.add_line("primary", 3.2, 29.5, 3.8, 50.5)
    mb.add_line("detail", 0.4, 30.8, -0.8, 48.0)

    # Broad tailored mid-century suit shoulders clipped razor-flush to MED_R = 92.0
    mb.add_arc_pts("primary", (-36.5, -8.5), (-65.5, 14.5), -3.5)
    mb.add_arc_pts("primary", (-65.5, 14.5), (-79.5, 58.0), -5.8)
    mb.add_arc_pts("primary", (27.5, 18.5), (56.5, 32.5), 3.0)
    mb.add_arc_pts("primary", (56.5, 32.5), (76.0, 68.0), 4.6)

    # Broad tailored dark suit lapels & buttoned closure
    # Left notched lapel
    mb.add_arc_pts("primary", (-36.5, -8.5), (-32.5, 24.5), -2.2)
    mb.add_line("primary", -32.5, 24.5, -24.8, 27.2)
    mb.add_line("primary", -24.8, 27.2, -33.5, 34.5)
    mb.add_arc_pts("primary", (-33.5, 34.5), (-3.8, 56.5), -2.6)
    mb.add_arc_pts("primary", (-3.8, 56.5), (-4.5, 88.0), -0.8)
    mb.add_arc_pts("detail", (-24.0, 28.0), (-5.5, 52.5), -1.5)

    # Right lapel emerging smoothly beneath resting wrist
    mb.add_arc_pts("primary", (24.2, 34.5), (27.8, 42.2), 1.0)
    mb.add_arc_pts("primary", (27.8, 42.2), (-3.8, 56.5), 2.0)
    mb.add_arc_pts("primary", (3.5, 57.5), (4.8, 88.0), 0.7)
    mb.add_arc_pts("detail", (17.5, 36.5), (-1.5, 52.5), 1.2)

    # Two tailored suit buttons & clean sleeve/chest drapery folds clipped to MED_R
    for bx, by in ((0.2, 64.5), (1.0, 79.5)):
        mb.add_circle("primary", bx, by, 1.9)
        mb.add_circle("detail", bx, by, 0.75)

    mb.add_arc_pts("detail", (-58.0, 24.0), (-68.5, 72.0), -3.2)
    mb.add_arc_pts("detail", (-44.5, 34.0), (-48.5, 82.0), -2.4)
    mb.add_arc_pts("detail", (-24.5, 48.0), (-25.5, 86.5), -1.4)
    mb.add_arc_pts("detail", (42.5, 34.0), (54.5, 78.0), 2.8)
    mb.add_arc_pts("detail", (56.5, 42.0), (68.0, 70.0), 2.4)
    mb.add_arc_pts("detail", (22.5, 54.0), (30.5, 85.0), 1.8)

    return mb.build()


def build_walter_russell_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Walter Russell medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_walter_russell_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_walter_russell_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``walter_russell_dark.svg`` and ``walter_russell_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "walter_russell_dark.svg"
    light_path = target_dir / "walter_russell_light.svg"
    dark_path.write_text(
        build_walter_russell_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_walter_russell_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
