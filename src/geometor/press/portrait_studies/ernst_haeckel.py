"""Study 33: Ernst Haeckel (after the archival German naturalist portrait)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_ernst_haeckel_elements",
    "build_ernst_haeckel_svg",
    "write_ernst_haeckel_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_radiolarian_icosahedron_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw Haeckel's Radiolarian Icosahedron (*Circogonia icosahedra*) in left margin.

    Renders the exact 3-fold orthographic projection of a regular icosahedron
    (outer regular hexagon of radius ``r_out`` and inner equilateral face of
    radius ``r_out / phi``) enclosed within a circular silica shell with six
    radial spines and central silica pore.
    """
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    r_out = 9.2
    r_in = r_out / phi
    r_spine = 13.0

    # Outer circular silica shell & central radiolarian pore
    mb.add_circle("golden", cx, cy, r_out)
    mb.add_circle("golden", cx, cy, 1.9)
    mb.add_circle("golden", cx, cy, 0.55, filled=True)

    # 6 outer icosahedral equatorial vertices (vertical spines at top & bottom)
    outer_pts: list[tuple[float, float]] = []
    for k in range(6):
        ang = math.radians(-90.0 + 60.0 * k)
        ox = cx + r_out * math.cos(ang)
        oy = cy + r_out * math.sin(ang)
        outer_pts.append((ox, oy))
        # Radial silica spine extending outward with terminal bead
        sx = cx + r_spine * math.cos(ang)
        sy = cy + r_spine * math.sin(ang)
        mb.add_line("golden", ox, oy, sx, sy)
        mb.add_circle("golden", sx, sy, 0.48, filled=True)

    # 3 front icosahedral face vertices (exact golden-ratio radius r_out / phi)
    inner_pts: list[tuple[float, float]] = []
    for k in range(3):
        ang = math.radians(-90.0 + 120.0 * k)
        inner_pts.append((cx + r_in * math.cos(ang), cy + r_in * math.sin(ang)))

    # Outer hexagon perimeter edges
    for k in range(6):
        p1 = outer_pts[k]
        p2 = outer_pts[(k + 1) % 6]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Front equilateral face triangle & 6 icosahedral ridge struts to outer hexagon
    for k in range(3):
        p1 = inner_pts[k]
        p2 = inner_pts[(k + 1) % 3]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
        mb.add_circle("golden", p1[0], p1[1], 0.52, filled=True)
        # Each inner vertex connects to its aligned outer vertex and its two adjacent ones
        o_main = outer_pts[2 * k]
        o_prev = outer_pts[(2 * k - 1) % 6]
        o_next = outer_pts[(2 * k + 1) % 6]
        mb.add_line("golden", p1[0], p1[1], o_main[0], o_main[1])
        mb.add_line("golden", p1[0], p1[1], o_prev[0], o_prev[1])
        mb.add_line("golden", p1[0], p1[1], o_next[0], o_next[1])


def _add_diatom_rosette_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw a concentric 12-spoke Diatom Star (*Actinoptychus*) in the right margin.

    Combines concentric silica rings, 12 radial spokes, a 6-fold hexagonal pore
    ring, and alternating scalloped outer circular arcs inspired by Haeckel's
    *Kunstformen der Natur*.
    """
    r_outer = 12.2
    r_mid = 8.4
    r_hub = 3.0
    r_pore_ring = 5.7
    r_pore = 1.45

    # Concentric circular diatom valves & central nucleus
    mb.add_circle("golden", cx, cy, r_outer)
    mb.add_circle("golden", cx, cy, r_mid)
    mb.add_circle("golden", cx, cy, r_hub)
    mb.add_circle("golden", cx, cy, 0.65, filled=True)

    # 12 radial spokes (6 primary full spokes + 6 alternating outer sector dividers)
    outer_nodes: list[tuple[float, float]] = []
    for k in range(12):
        ang = math.radians(-90.0 + 30.0 * k)
        ca, sa = math.cos(ang), math.sin(ang)
        r_start = r_hub if (k % 2 == 0) else r_mid
        mb.add_line(
            "golden",
            cx + r_start * ca,
            cy + r_start * sa,
            cx + r_outer * ca,
            cy + r_outer * sa,
        )
        nx = cx + r_outer * ca
        ny = cy + r_outer * sa
        outer_nodes.append((nx, ny))
        if k % 2 == 0:
            mb.add_circle("golden", nx, ny, 0.50, filled=True)

    # Hexagonal ring of 6 circular diatom pores inside the mid-ring
    for k in range(6):
        ang = math.radians(-60.0 + 60.0 * k)
        px = cx + r_pore_ring * math.cos(ang)
        py = cy + r_pore_ring * math.sin(ang)
        mb.add_circle("golden", px, py, r_pore)

    # Alternating scalloped circular arcs weaving around the outer 12-fold margin
    for k in range(12):
        p1 = outer_nodes[k]
        p2 = outer_nodes[(k + 1) % 12]
        sag = -1.25 if (k % 2 == 0) else 0.85
        mb.add_arc_pts("golden", p1, p2, sag)


def build_ernst_haeckel_elements(
    wave_angle_deg: float = 30.0,
) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Ernst Haeckel.

    Calibrated to the archival German naturalist portrait: noble near-profile
    three-quarter-left gaze with high receding forehead, swept-back silver hair
    over a clear ear, bushy brows and steady eyes on ``y = -27``, classic
    aquiline nose, full flowing naturalist's mustache and curling silver beard
    (``Euclid III.12`` tangent waves), crisp standing white shirt collar, dark
    knotted tie, buttoned high-cut waistcoat with three circular buttons, and
    dark professor's coat lapels sweeping cleanly to ``MED_R = 92.0``. Margin
    motifs display *Circogonia icosahedra* (left) and *Actinoptychus* diatom
    star (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-14.0,
        eye_rx=8.0,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN KUNSTFORMEN DER NATUR MARGIN MOTIFS (zero face crossing) ---
    _add_radiolarian_icosahedron_motif(mb, cx=-63.5, cy=-26.0)
    _add_diatom_rosette_motif(mb, cx=63.5, cy=-26.0)

    # --- HIGH RECEDING FOREHEAD & SWEPT-BACK SILVER HAIR ---
    # Noble forehead profile sweeping smoothly upward
    mb.add_arc_pts("primary", (-19.5, -31.8), (-18.8, -40.0), 0.7)
    mb.add_arc_pts("primary", (-18.8, -40.0), (-13.2, -49.0), 0.9)
    mb.add_arc_pts("primary", (-13.2, -49.0), (-7.2, -53.5), 0.7)

    # Swept-back outer silver hair crown wrapping over ear to nape
    mb.add_arc_pts("primary", (-7.2, -53.5), (-4.2, -56.5), 0.7)
    mb.add_arc_pts("primary", (-4.2, -56.5), (5.8, -57.8), 1.4)
    mb.add_arc_pts("primary", (5.8, -57.8), (18.5, -53.8), 1.9)
    mb.add_arc_pts("primary", (18.5, -53.8), (28.5, -42.5), 2.2)
    mb.add_arc_pts("primary", (28.5, -42.5), (32.5, -29.0), 1.8)
    mb.add_arc_pts("primary", (32.5, -29.0), (29.8, -18.0), 1.3)
    mb.add_arc_pts("primary", (29.8, -18.0), (21.5, -6.0), 1.1)

    # Swept-back silver hairline curving around high temple to ear
    mb.add_arc_pts("detail", (-7.2, -53.5), (5.5, -51.8), 1.1)
    mb.add_arc_pts("detail", (5.5, -51.8), (14.2, -46.0), 1.1)
    mb.add_arc_pts("detail", (14.2, -46.0), (16.2, -38.5), 0.9)
    mb.add_arc_pts("detail", (16.2, -38.5), (11.8, -33.0), -0.8)
    mb.add_arc_pts("detail", (11.8, -33.0), (14.8, -24.5), 0.7)

    # Flowing swept-back silver hair strands via Euclid III.12 waves
    mb.add_wave("detail", (-3.5, -54.5), (16.5, -51.5), 3, wave_angle_deg - 2.0, -1)
    mb.add_wave("detail", (8.5, -52.8), (27.5, -36.2), 3, wave_angle_deg, 1)
    mb.add_wave("detail", (16.5, -44.8), (29.5, -26.0), 3, wave_angle_deg + 2.0, -1)
    mb.add_wave("detail", (18.5, -34.0), (27.5, -18.5), 2, wave_angle_deg + 4.0, 1)

    # --- CLEAR LEFT EAR (VIEWER'S RIGHT) ---
    mb.add_arc_pts("primary", (16.2, -24.5), (23.2, -23.5), 1.0)
    mb.add_arc_pts("primary", (23.2, -23.5), (22.6, -16.2), 1.1)
    mb.add_arc_pts("primary", (22.6, -16.2), (16.5, -11.5), 1.0)
    mb.add_arc_pts("primary", (16.5, -11.5), (13.5, -13.5), 0.6)
    mb.add_arc_pts("detail", (17.2, -22.0), (20.2, -17.2), 0.9)
    mb.add_arc_pts("detail", (20.2, -17.2), (16.2, -14.2), 0.7)

    # --- BUSHY BROWS & STEADY NATURALIST EYES ON y = -27 ---
    # Far overhanging brow tuft on left profile
    mb.add_arc_pts("primary", (-21.0, -31.5), (-17.5, -32.2), 0.55)
    mb.add_arc_pts("primary", (-17.5, -32.2), (-15.2, -30.5), 0.4)
    # Near bushy brow arching over main eye
    mb.add_arc_pts("primary", (-13.6, -30.5), (-6.5, -32.2), 0.75)
    mb.add_arc_pts("primary", (-6.5, -32.2), (0.6, -29.4), 0.6)
    mb.add_arc_pts("detail", (-12.5, -29.6), (-0.4, -28.8), 0.85)

    # Steady near-profile gaze right on y = -27
    mb.add_canonical_eye(
        -17.6,
        -26.8,
        width=5.2,
        upper_sag=1.35,
        lower_sag=-0.65,
        iris_r=1.35,
        pupil_r=0.78,
        gaze_dx=-0.4,
    )
    mb.add_canonical_eye(
        -6.8,
        -26.7,
        width=9.6,
        upper_sag=1.80,
        lower_sag=-0.85,
        iris_r=1.90,
        pupil_r=1.02,
        gaze_dx=-0.6,
    )
    # Subtle wisdom lines at outer eye corner & cheek
    mb.add_arc_pts("detail", (-1.0, -25.2), (2.8, -24.2), -0.3)
    mb.add_arc_pts("detail", (-9.8, -21.2), (-3.8, -16.5), -0.5)

    # --- CLASSIC AQUILINE NOSE ---
    mb.add_arc_pts("primary", (-15.6, -29.2), (-18.8, -22.5), -0.35)
    mb.add_arc_pts("primary", (-18.8, -22.5), (-21.6, -16.4), -0.3)
    mb.add_arc_pts("primary", (-21.6, -16.4), (-20.0, -13.6), -0.65)
    mb.add_arc_pts("primary", (-20.0, -13.6), (-15.2, -13.8), -0.45)
    mb.add_arc_pts("primary", (-15.2, -13.8), (-12.0, -15.0), -0.4)
    # Crisp near nostril wing C-curve
    mb.add_arc_pts("primary", (-12.0, -15.0), (-11.4, -17.0), -0.55)
    mb.add_arc_pts("primary", (-11.4, -17.0), (-13.8, -17.6), -0.35)

    # --- FULL FLOWING MUSTACHE & SILVER-GRAY NATURALIST BEARD ---
    # Sweeping thick mustache springing beneath nose
    mb.add_arc_pts("primary", (-19.6, -13.2), (-14.5, -11.8), 0.7)
    mb.add_arc_pts("primary", (-14.5, -11.8), (-6.8, -9.0), 0.9)
    mb.add_arc_pts("primary", (-6.8, -9.0), (-3.5, -5.2), 0.8)
    mb.add_arc_pts("primary", (-20.2, -9.2), (-14.2, -7.8), -0.7)
    mb.add_arc_pts("primary", (-14.2, -7.8), (-7.5, -6.2), -0.65)
    mb.add_arc_pts("primary", (-7.5, -6.2), (-3.5, -3.5), -0.5)
    # Glimpse of firm lower lip beneath mustache
    mb.add_arc_pts("detail", (-17.5, -5.8), (-12.5, -5.2), -0.4)

    # Cheek-to-beard boundary separating clean cheekbone from beard
    mb.add_arc_pts("primary", (13.2, -24.2), (10.0, -16.2), 0.9)
    mb.add_arc_pts("primary", (10.0, -16.2), (4.8, -9.8), 1.0)
    mb.add_arc_pts("primary", (4.8, -9.8), (-3.5, -5.2), 0.9)

    # Sculpted outer naturalist beard silhouette
    mb.add_arc_pts("primary", (-20.2, -9.2), (-20.8, -1.2), -0.8)
    mb.add_arc_pts("primary", (-20.8, -1.2), (-23.2, 6.0), -1.1)
    mb.add_arc_pts("primary", (-23.2, 6.0), (-19.5, 13.2), -1.4)
    mb.add_arc_pts("primary", (-19.5, 13.2), (-11.2, 18.2), -1.6)
    mb.add_arc_pts("primary", (-11.2, 18.2), (-1.8, 18.8), -1.5)
    mb.add_arc_pts("primary", (-1.8, 18.8), (8.2, 14.0), -1.4)
    mb.add_arc_pts("primary", (8.2, 14.0), (16.5, 5.5), -1.3)
    mb.add_arc_pts("primary", (16.5, 5.5), (21.5, -6.0), -1.0)

    # Lush curling beard & mustache strands via Euclid III.12 tangent waves
    mb.add_wave("detail", (-18.2, -10.5), (-6.2, -6.8), 3, wave_angle_deg + 4.0, 1)
    mb.add_wave("detail", (-19.2, -2.5), (-15.2, 13.8), 4, wave_angle_deg + 6.0, -1)
    mb.add_wave("detail", (-14.5, -3.0), (-9.2, 16.5), 4, wave_angle_deg + 6.0, 1)
    mb.add_wave("detail", (-8.5, -3.5), (-2.2, 17.0), 4, wave_angle_deg + 6.0, -1)
    mb.add_wave("detail", (-2.0, -4.5), (4.8, 13.2), 4, wave_angle_deg + 5.0, 1)
    mb.add_wave("detail", (5.2, -9.0), (11.8, 8.2), 4, wave_angle_deg + 4.0, -1)
    mb.add_wave("detail", (11.0, -14.5), (16.2, 1.5), 3, wave_angle_deg + 4.0, 1)

    # --- STANDING WHITE COLLAR, KNOTTED TIE, 3-BUTTON WAISTCOAT & COAT ---
    # Crisp standing white pointed shirt collar
    mb.add_arc_pts("primary", (21.5, -6.0), (21.8, 4.2), -0.8)
    mb.add_arc_pts("primary", (21.8, 4.2), (11.2, 25.2), 1.4)
    mb.add_arc_pts("primary", (11.2, 25.2), (-0.5, 19.2), -0.8)
    mb.add_arc_pts("detail", (14.8, 8.5), (0.8, 18.6), -1.0)
    mb.add_arc_pts("primary", (-11.2, 18.2), (-10.4, 23.0), -0.5)
    mb.add_arc_pts("primary", (-10.4, 23.0), (-0.5, 19.2), -0.6)

    # Dark knotted professor's necktie nestled naturally inside collar V
    mb.add_arc_pts("primary", (-0.5, 19.2), (-5.2, 26.8), 0.7)
    mb.add_arc_pts("primary", (-0.5, 19.2), (5.5, 27.2), -0.7)
    mb.add_arc_pts("detail", (-2.0, 20.5), (-1.8, 29.8), 0.4)
    mb.add_arc_pts("detail", (0.8, 21.0), (2.4, 28.5), -0.4)
    mb.add_arc_pts("detail", (-5.8, 23.2), (5.2, 24.0), -0.6)

    # High-cut buttoned waistcoat with 3 crisp circular buttons centered cleanly in placket
    mb.add_arc_pts("primary", (-10.4, 23.0), (-1.8, 30.8), -0.8)
    mb.add_arc_pts("primary", (-1.8, 30.8), (11.2, 25.2), -0.9)
    # Tailored placket seams flanking the 3 buttons (zero stroke crossing buttons)
    mb.add_arc_pts("primary", (-5.2, 30.2), (-15.5, 86.0), 2.2)
    mb.add_arc_pts("detail", (0.8, 30.2), (-9.2, 86.0), 2.2)
    # Three crisp circular waistcoat buttons
    for bx, by in ((-2.4, 36.5), (-5.0, 52.2), (-8.0, 68.0)):
        mb.add_circle("primary", bx, by, 1.85)
        mb.add_circle("primary", bx, by, 0.72, filled=True)
    # Left waistcoat edge beside professor's coat
    mb.add_arc_pts("primary", (-12.2, 22.8), (-23.8, 86.0), 2.8)

    # Dark professor's coat lapels & broad shoulders sweeping to MED_R = 92.0
    # Viewer-right notched lapel & sweeping coat front
    mb.add_arc_pts("primary", (21.8, 4.2), (28.5, 10.0), -1.0)
    mb.add_arc_pts("primary", (28.5, 10.0), (31.2, 29.5), -1.2)
    mb.add_arc_pts("primary", (31.2, 29.5), (37.5, 34.8), 0.4)
    mb.add_arc_pts("primary", (37.5, 34.8), (31.5, 40.5), -0.5)
    mb.add_arc_pts("primary", (31.5, 40.5), (-8.5, 88.0), 4.2)
    # Inner right lapel crease framing the waistcoat
    mb.add_arc_pts("primary", (21.8, 4.2), (17.5, 29.5), 1.2)
    mb.add_arc_pts("primary", (17.5, 29.5), (-11.0, 88.0), 3.6)

    # Viewer-left coat lapel & smoothly rounded broad shoulders to MED_R
    mb.add_arc_pts("primary", (-19.5, 13.2), (-46.5, 25.0), -1.4)
    mb.add_arc_pts("primary", (-46.5, 25.0), (-72.0, 62.0), -5.8)
    mb.add_arc_pts("primary", (-15.8, 17.5), (-29.5, 86.0), 2.8)
    mb.add_arc_pts("primary", (28.5, 10.0), (74.0, 58.0), 10.5)

    # Clean professor's coat tailoring folds sweeping smoothly to MED_R
    mb.add_arc_pts("detail", (-46.5, 25.0), (-54.0, 78.0), -2.6)
    mb.add_arc_pts("detail", (-36.0, 42.0), (-41.5, 84.0), -1.8)
    mb.add_arc_pts("detail", (45.0, 32.0), (56.0, 78.0), 3.4)
    mb.add_arc_pts("detail", (28.0, 56.0), (22.5, 86.0), 1.8)

    return mb.build()


def build_ernst_haeckel_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Ernst Haeckel medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_ernst_haeckel_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_ernst_haeckel_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``ernst_haeckel_dark.svg`` and ``ernst_haeckel_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "ernst_haeckel_dark.svg"
    light_path = target_dir / "ernst_haeckel_light.svg"
    dark_path.write_text(
        build_ernst_haeckel_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_ernst_haeckel_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
