"""Study 21: Felix Klein (after Gebruder Noelle, Gottingen, pre-1897) in lines and arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_klein_elements",
    "build_klein_svg",
    "write_klein_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _extend_chord_to_circle(
    cx: float,
    cy: float,
    r: float,
    p_start: tuple[float, float],
    p_through: tuple[float, float],
) -> tuple[float, float]:
    """Intersect the ray from ``p_start`` through ``p_through`` with circle ``(cx, cy, r)``."""
    dx = p_through[0] - p_start[0]
    dy = p_through[1] - p_start[1]
    ox = p_start[0] - cx
    oy = p_start[1] - cy
    a = dx * dx + dy * dy
    b = 2.0 * (ox * dx + oy * dy)
    c = ox * ox + oy * oy - r * r
    disc = max(0.0, b * b - 4.0 * a * c)
    t = (-b + math.sqrt(disc)) / (2.0 * a)
    return (p_start[0] + t * dx, p_start[1] + t * dy)


def _add_beltrami_klein_disk_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.8,
) -> None:
    """Draw the Beltrami-Klein hyperbolic disk model with limiting & ultra-parallel chords.

    Inside the ideal boundary circle, renders a hyperbolic geodesic chord ``l``,
    an external interior point ``P``, the two limiting (asymptotic) parallel
    chords through ``P`` meeting the ideal endpoints of ``l``, and an
    ultra-parallel geodesic chord through ``P``.
    """
    mb.add_circle("golden", cx, cy, radius)

    # Ideal boundary endpoints A and B of base hyperbolic line l
    ang_a = math.radians(150.0)
    ang_b = math.radians(30.0)
    pt_a = (cx + radius * math.cos(ang_a), cy + radius * math.sin(ang_a))
    pt_b = (cx + radius * math.cos(ang_b), cy + radius * math.sin(ang_b))
    mb.add_line("golden", pt_a[0], pt_a[1], pt_b[0], pt_b[1])

    # External interior point P in upper half of disk
    pt_p = (cx - 1.2, cy - 4.4)

    # Two limiting parallel chords through P to ideal endpoints A and B, extended across disk
    pt_a2 = _extend_chord_to_circle(cx, cy, radius, pt_a, pt_p)
    pt_b2 = _extend_chord_to_circle(cx, cy, radius, pt_b, pt_p)
    mb.add_line("golden", pt_a[0], pt_a[1], pt_a2[0], pt_a2[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_b2[0], pt_b2[1])

    # Horizontal ultra-parallel chord through P (disjoint from l inside and on boundary)
    dy_p = pt_p[1] - cy
    half_u = math.sqrt(max(0.0, radius * radius - dy_p * dy_p))
    mb.add_line("golden", cx - half_u, pt_p[1], cx + half_u, pt_p[1])

    # Ideal boundary nodes on A, B and filled interior point P
    mb.add_circle("golden", pt_a[0], pt_a[1], 0.78)
    mb.add_circle("golden", pt_b[0], pt_b[1], 0.78)
    mb.add_circle("golden", pt_p[0], pt_p[1], 1.0, filled=True)


def _add_erlangen_hierarchy_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 12.6,
) -> None:
    """Draw Klein's Erlangen Program nested transformation hierarchy.

    Nests an outer projective circle with a 4-ray cross-ratio pencil, an
    inscribed equilateral triangle with affine medial subdivision, and a
    concentric Euclidean incircle symbolizing Metric < Affine < Projective.
    """
    # Outer Projective circle (Cayley-Klein absolute)
    mb.add_circle("golden", cx, cy, radius)

    # Inscribed equilateral triangle (Affine & Metric symmetry)
    verts = [
        (
            cx + radius * math.cos(math.radians(-90.0 + 120.0 * k)),
            cy + radius * math.sin(math.radians(-90.0 + 120.0 * k)),
        )
        for k in range(3)
    ]
    for k in range(3):
        p1 = verts[k]
        p2 = verts[(k + 1) % 3]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Concentric Metric incircle (radius = R / 2, tangent to triangle sides)
    mb.add_circle("golden", cx, cy, 0.5 * radius)

    # Projective cross-ratio pencil from apex V0 through harmonic nodes on base V1-V2
    v0, v1, v2 = verts
    for frac in (0.28, 0.5, 0.72):
        bx = v1[0] + frac * (v2[0] - v1[0])
        by = v1[1] + frac * (v2[1] - v1[1])
        mb.add_line("golden", v0[0], v0[1], bx, by)
        mb.add_circle("golden", bx, by, 0.7)

    # Mid-height affine transversal chord across the pencil
    t_y = cy - 0.15 * radius
    half_t = math.sqrt(max(0.0, radius * radius - (t_y - cy) ** 2))
    mb.add_line("golden", cx - half_t, t_y, cx + half_t, t_y)

    mb.add_circle("golden", v0[0], v0[1], 0.9, filled=True)
    mb.add_circle("golden", cx, cy, 0.85, filled=True)


def build_klein_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the four-layer compass-and-straightedge geometry for Felix Klein.

    Uses ``MedallionBuilder`` so every line and circular arc is clipped cleanly
    within ``MED_R = 92.0`` with zero Bezier curves.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1 (Scaffold): Canonical medallion ring, eye line & golden circles
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-15.5,
        eye_rx=6.5,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Beltrami-Klein Disk (Left) & Erlangen Hierarchy (Right)
    # -------------------------------------------------------------------------
    _add_beltrami_klein_disk_motif(mb, cx=-63.5, cy=-26.0, radius=12.8)
    _add_erlangen_hierarchy_motif(mb, cx=64.5, cy=-26.0, radius=12.6)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Classical Left-Profile Skull, Short Hair & Sculpted Ear
    # -------------------------------------------------------------------------
    # Outer short-cropped 19th-century Gottingen hair silhouette
    mb.add_arc_pts("primary", (-11.2, -49.5), (-7.5, -57.2), -1.1)
    mb.add_arc_pts("primary", (-7.5, -57.2), (14.5, -59.5), 3.2)
    mb.add_arc_pts("primary", (14.5, -59.5), (34.5, -48.8), 3.0)
    mb.add_arc_pts("primary", (34.5, -48.8), (39.0, -28.0), 2.8)
    mb.add_arc_pts("primary", (39.0, -28.0), (34.2, -11.5), 1.8)
    mb.add_arc_pts("primary", (34.2, -11.5), (27.8, -1.5), 1.2)

    # Hairline across high intellectual forehead & right temple into sideburn
    mb.add_arc_pts("detail", (-11.2, -49.5), (4.5, -48.2), 1.8)
    mb.add_arc_pts("detail", (4.5, -48.2), (12.2, -39.2), 1.5)
    mb.add_arc_pts("detail", (12.2, -39.2), (14.8, -24.0), 1.1)

    # Disciplined short-cropped hair waves following the cranial contour
    mb.add_wave("detail", (-5.5, -54.5), (26.5, -48.8), 4, wave_angle_deg * 0.45, 1)
    mb.add_wave("detail", (6.5, -51.0), (34.2, -36.5), 4, wave_angle_deg * 0.45, -1)
    mb.add_wave("detail", (15.5, -42.5), (35.0, -22.5), 4, wave_angle_deg * 0.45, 1)
    mb.add_wave("detail", (25.5, -31.8), (30.8, -9.5), 3, wave_angle_deg * 0.45, -1)

    # Prominently sculpted left ear
    mb.add_arc_pts("primary", (17.5, -22.5), (24.2, -24.5), 1.8)
    mb.add_arc_pts("primary", (24.2, -24.5), (26.8, -17.0), 2.0)
    mb.add_arc_pts("primary", (26.8, -17.0), (23.8, -8.5), 1.6)
    mb.add_arc_pts("primary", (23.8, -8.5), (18.8, -5.8), 1.4)
    mb.add_arc_pts("primary", (18.8, -5.8), (16.2, -8.8), 0.9)
    mb.add_arc_pts("detail", (18.5, -20.5), (23.8, -18.5), 1.5)
    mb.add_arc_pts("detail", (23.8, -18.5), (21.5, -10.8), 1.4)
    mb.add_arc_pts("detail", (17.6, -16.8), (19.0, -14.2), 0.7)
    mb.add_arc_pts("detail", (19.0, -14.2), (17.5, -11.5), 0.7)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Profile Forehead, Nose, Keen Eye, Mustache & Pointed Beard
    # -------------------------------------------------------------------------
    # Classical left-profile brow & straight noble nose
    mb.add_arc_pts("primary", (-11.2, -49.5), (-16.8, -34.2), -1.1)
    mb.add_arc_pts("primary", (-16.8, -34.2), (-16.2, -28.0), 0.75)
    mb.add_arc_pts("primary", (-16.2, -28.0), (-21.0, -17.8), -0.55)
    mb.add_arc_pts("primary", (-21.0, -17.8), (-19.2, -14.8), -1.1)
    mb.add_arc_pts("primary", (-19.2, -14.8), (-13.5, -14.4), -0.6)
    mb.add_arc_pts("primary", (-13.5, -14.4), (-11.0, -15.4), 0.65)
    mb.add_arc_pts("detail", (-11.0, -15.4), (-12.0, -18.4), 0.55)
    mb.add_arc_pts("detail", (-17.2, -15.6), (-13.5, -15.6), -0.35)
    # Subtle far-side brow projection peeking at the nasion
    mb.add_arc_pts("detail", (-17.2, -32.2), (-18.4, -30.5), -0.45)

    # Expressive profile eyebrow & keen leftward-gazing eye on y = -27
    mb.add_arc_pts("primary", (-14.5, -31.2), (-7.2, -32.8), 1.1)
    mb.add_arc_pts("primary", (-7.2, -32.8), (1.5, -29.2), 1.2)
    mb.add_arc_pts("detail", (-13.8, -32.4), (0.8, -30.6), 1.4)

    e_in = (-11.0, -26.4)
    e_out = (-1.6, -24.8)
    mb.add_arc_pts("primary", e_in, e_out, 2.2)
    mb.add_arc_pts("detail", (-11.6, -28.8), (-1.0, -27.2), 2.1)
    mb.add_arc_pts("detail", e_in, e_out, -1.1)
    mb.add_circle("detail", -8.2, -26.0, 1.85)
    mb.add_circle("primary", -8.6, -26.0, 0.92, filled=True)
    mb.add_arc_pts("detail", (-10.4, -22.8), (-2.2, -21.8), -0.9)
    # Subtle cheekbone contour line
    mb.add_arc_pts("detail", (-6.2, -19.5), (3.5, -15.2), -0.9)

    # Full sweeping mustache & trimmed pointed professor's beard
    mb.add_arc_pts("primary", (-19.2, -14.8), (-20.4, -10.8), -0.8)
    mb.add_arc_pts("primary", (-14.5, -13.2), (-2.5, -4.5), 1.4)
    mb.add_arc_pts("detail", (-19.4, -10.4), (-11.5, -7.8), -0.9)
    mb.add_arc_pts("detail", (-18.2, -7.6), (-12.0, -6.8), -0.55)

    # Outer beard silhouette (front profile -> crisp pointed chin -> jawline to ear)
    mb.add_arc_pts("primary", (-20.4, -10.8), (-19.0, -2.5), -0.8)
    mb.add_arc_pts("primary", (-19.0, -2.5), (-19.8, 5.8), -0.8)
    mb.add_arc_pts("primary", (-19.8, 5.8), (-15.2, 13.2), -1.3)
    mb.add_arc_pts("primary", (-15.2, 13.2), (-5.2, 13.0), -1.5)
    mb.add_arc_pts("primary", (-5.2, 13.0), (6.5, 8.8), -1.4)
    mb.add_arc_pts("primary", (6.5, 8.8), (16.5, -2.8), -1.6)
    mb.add_arc_pts("primary", (16.5, -2.8), (18.8, -5.8), -0.5)

    # Beard cheek boundary line descending from sideburn toward mustache
    mb.add_arc_pts("detail", (14.8, -24.0), (11.5, -14.0), 1.0)
    mb.add_arc_pts("detail", (11.5, -14.0), (2.2, -6.5), 1.2)

    # Trimmed professor's beard wave texture (Euclid III.12 arcs)
    mb.add_wave("detail", (-15.5, -5.5), (-14.8, 11.2), 3, wave_angle_deg * 0.55, 1)
    mb.add_wave("detail", (-10.2, -5.2), (-8.5, 11.8), 3, wave_angle_deg * 0.55, -1)
    mb.add_wave("detail", (-3.5, -4.5), (-1.5, 10.2), 3, wave_angle_deg * 0.55, 1)
    mb.add_wave("detail", (3.5, -6.5), (5.2, 6.8), 3, wave_angle_deg * 0.52, -1)
    mb.add_wave("detail", (10.5, -12.0), (11.5, 1.8), 3, wave_angle_deg * 0.5, 1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Stiff Wing Collar, Knotted Bow Tie, Waistcoat & Frock Coat
    # -------------------------------------------------------------------------
    # Back of neck & stiff white wing collar
    mb.add_arc_pts("primary", (27.8, -1.5), (26.8, 5.2), 0.7)
    mb.add_arc_pts("primary", (-5.2, 13.0), (4.5, 19.2), -1.4)
    mb.add_arc_pts("primary", (4.5, 19.2), (19.5, 12.2), -1.8)
    mb.add_arc_pts("primary", (19.5, 12.2), (27.2, 3.2), -1.0)

    # Crisp collar wing tips & lower collar seam
    mb.add_arc_pts("primary", (-5.2, 13.0), (-3.8, 21.8), -0.6)
    mb.add_arc_pts("primary", (-3.8, 21.8), (2.5, 24.5), -0.7)
    mb.add_line("detail", 4.5, 19.2, 4.5, 24.2)
    mb.add_arc_pts("primary", (14.5, 20.8), (26.5, 11.5), -1.4)
    mb.add_arc_pts("primary", (26.5, 11.5), (27.2, 3.2), -0.7)

    # Crisp knotted 19th-century bow tie
    # Center knot
    mb.add_arc_pts("primary", (1.2, 24.4), (8.2, 24.2), 0.6)
    mb.add_arc_pts("primary", (8.2, 24.2), (8.4, 29.8), 0.6)
    mb.add_arc_pts("primary", (8.4, 29.8), (1.4, 29.8), 0.6)
    mb.add_arc_pts("primary", (1.4, 29.8), (1.2, 24.4), 0.6)
    # Left bow wing & hanging tail
    mb.add_arc_pts("primary", (1.2, 24.4), (-8.2, 21.8), 1.2)
    mb.add_arc_pts("primary", (-8.2, 21.8), (-9.2, 31.2), -1.4)
    mb.add_arc_pts("primary", (-9.2, 31.2), (1.4, 29.8), -1.0)
    mb.add_arc_pts("primary", (-7.2, 31.0), (-5.2, 37.8), -0.7)
    mb.add_arc_pts("primary", (-5.2, 37.8), (-0.8, 35.2), -0.6)
    mb.add_arc_pts("primary", (-0.8, 35.2), (1.4, 29.8), 0.5)
    mb.add_line("detail", -6.5, 26.8, 0.8, 27.0)
    # Right bow wing & hanging tail
    mb.add_arc_pts("primary", (8.2, 24.2), (17.2, 18.8), 1.2)
    mb.add_arc_pts("primary", (17.2, 18.8), (19.0, 27.2), 1.4)
    mb.add_arc_pts("primary", (19.0, 27.2), (8.4, 29.8), 1.0)
    mb.add_arc_pts("primary", (8.4, 29.8), (11.2, 38.2), 0.7)
    mb.add_arc_pts("primary", (11.2, 38.2), (16.2, 33.4), 0.8)
    mb.add_arc_pts("primary", (16.2, 33.4), (14.5, 28.4), 0.5)
    mb.add_line("detail", 9.0, 26.5, 16.5, 23.6)

    # White dress shirt front & waistcoat V-opening
    mb.add_line("detail", 3.5, 31.0, -1.5, 65.0)
    mb.add_circle("detail", 3.2, 42.5, 0.9)
    mb.add_arc_pts("primary", (-6.2, 36.2), (-2.2, 65.5), 1.0)
    mb.add_arc_pts("primary", (12.2, 36.8), (-2.2, 65.5), -1.2)
    mb.add_arc_pts("primary", (-2.2, 65.5), (-3.5, 88.0), 0.6)

    # Tailored dark frock coat shoulders clipped razor-flush to MED_R = 92.0
    mb.add_arc_pts("primary", (-6.8, 16.8), (-34.5, 26.0), -2.4)
    mb.add_arc_pts("primary", (-34.5, 26.0), (-67.5, 80.5), -7.6)
    mb.add_arc_pts("primary", (27.2, 6.2), (58.0, 25.5), 3.4)
    mb.add_arc_pts("primary", (58.0, 25.5), (86.5, 68.0), 5.4)

    # Crisp notched Victorian frock coat lapels
    # Left lapel
    mb.add_arc_pts("primary", (-6.8, 16.8), (-14.5, 33.5), -1.2)
    mb.add_line("primary", -14.5, 33.5, -11.2, 35.5)
    mb.add_line("primary", -11.2, 35.5, -17.5, 40.5)
    mb.add_arc_pts("primary", (-17.5, 40.5), (-6.2, 69.5), -2.0)
    mb.add_arc_pts("primary", (-6.2, 69.5), (-7.0, 88.0), -0.6)
    mb.add_arc_pts("detail", (-10.2, 37.5), (-6.2, 66.5), -1.0)

    # Right notched lapel (wide sweeping Victorian coat lapel)
    mb.add_arc_pts("primary", (27.2, 6.2), (31.5, 27.5), 1.4)
    mb.add_line("primary", 31.5, 27.5, 24.5, 30.2)
    mb.add_line("primary", 24.5, 30.2, 32.2, 38.5)
    mb.add_arc_pts("primary", (32.2, 38.5), (2.2, 69.5), 2.4)
    mb.add_arc_pts("primary", (2.2, 69.5), (4.5, 88.0), 0.8)
    mb.add_arc_pts("detail", (22.5, 32.0), (1.5, 64.5), 1.4)
    mb.add_line("detail", 20.5, 42.5, 25.5, 45.2)

    # Subtle tailored frock coat sleeve & chest drapery creases clipped to MED_R
    mb.add_arc_pts("detail", (-32.0, 34.0), (-44.0, 84.0), -2.5)
    mb.add_arc_pts("detail", (-24.5, 42.0), (-27.0, 87.5), -1.6)
    mb.add_arc_pts("detail", (42.5, 28.0), (56.5, 78.5), 3.1)
    mb.add_arc_pts("detail", (56.5, 36.0), (72.0, 71.0), 2.8)
    mb.add_arc_pts("detail", (24.5, 58.0), (36.5, 86.0), 1.8)

    return mb.build()


def build_klein_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Felix Klein medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_klein_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_klein_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``klein_dark.svg`` and ``klein_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "klein_dark.svg"
    light_path = target_dir / "klein_light.svg"
    dark_path.write_text(
        build_klein_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_klein_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
