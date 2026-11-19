"""Study 20: Claudius Ptolemy (after Justus of Ghent & Pedro Berruguete, c. 1473-1476)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_ptolemy_elements",
    "build_ptolemy_svg",
    "write_ptolemy_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _intersect_lines(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> tuple[float, float]:
    """Compute exact intersection of lines ``p1-p2`` and ``p3-p4``."""
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


def _add_ptolemy_theorem_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 11.8,
) -> None:
    """Draw Ptolemy's Theorem cyclic quadrilateral ``ABCD`` with intersecting diagonals.

    Illustrates ``AC * BD = AB * CD + BC * DA`` using an asymmetric cyclic
    quadrilateral inscribed in a circle with marked vertex and crossing nodes.
    """
    mb.add_circle("golden", cx, cy, radius)
    angles_deg = (-142.0, -34.0, 28.0, 128.0)
    verts = [
        (
            cx + radius * math.cos(math.radians(ang)),
            cy + radius * math.sin(math.radians(ang)),
        )
        for ang in angles_deg
    ]

    # Four cyclic sides AB, BC, CD, DA
    for k in range(4):
        p1 = verts[k]
        p2 = verts[(k + 1) % 4]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Intersecting diagonals AC & BD
    mb.add_line("golden", verts[0][0], verts[0][1], verts[2][0], verts[2][1])
    mb.add_line("golden", verts[1][0], verts[1][1], verts[3][0], verts[3][1])

    # Marked vertices and diagonal intersection node
    for vx, vy in verts:
        mb.add_circle("golden", vx, vy, 0.85, filled=True)
    ix, iy = _intersect_lines(verts[0], verts[2], verts[1], verts[3])
    mb.add_circle("golden", ix, iy, 0.75)


def _add_epicycle_deferent_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    deferent_r: float = 10.0,
) -> None:
    """Draw Ptolemy's *Almagest* epicycle-on-deferent celestial orbit model.

    Constructs the deferent circle, eccentric Earth and equant nodes along the
    apsidal line, and two orbiting epicycles with planet markers on their rims.
    """
    # Outer deferent circle
    mb.add_circle("golden", cx, cy, deferent_r)

    # Apsidal diameter with eccentric Earth and equant points
    ang_aps = math.radians(18.0)
    dx_a = math.cos(ang_aps)
    dy_a = math.sin(ang_aps)
    mb.add_line(
        "golden",
        cx - deferent_r * dx_a,
        cy - deferent_r * dy_a,
        cx + deferent_r * dx_a,
        cy + deferent_r * dy_a,
    )
    # Deferent center, eccentric Earth, and equant
    mb.add_circle("golden", cx, cy, 0.55)
    earth_x, earth_y = cx - 2.6 * dx_a, cy - 2.6 * dy_a
    equant_x, equant_y = cx + 2.6 * dx_a, cy + 2.6 * dy_a
    mb.add_circle("golden", earth_x, earth_y, 1.15, filled=True)
    mb.add_circle("golden", equant_x, equant_y, 0.72)

    # Two orbiting epicycles positioned cleanly off the apsidal line
    epicycles: list[tuple[float, float, float]] = [
        (-56.0, 3.8, 35.0),    # upper-right primary epicycle + planet angle
        (132.0, 2.8, -135.0),  # lower-left secondary epicycle + planet angle
    ]
    for def_deg, epi_r, planet_deg in epicycles:
        rad = math.radians(def_deg)
        ex = cx + deferent_r * math.cos(rad)
        ey = cy + deferent_r * math.sin(rad)
        mb.add_circle("golden", ex, ey, epi_r)
        mb.add_circle("golden", ex, ey, 0.55)
        mb.add_line("golden", cx, cy, ex, ey)
        prad = math.radians(planet_deg)
        px = ex + epi_r * math.cos(prad)
        py = ey + epi_r * math.sin(prad)
        mb.add_line("golden", ex, ey, px, py)
        mb.add_circle("golden", px, py, 0.85, filled=True)


def _add_armillary_sphere(
    mb: MedallionBuilder,
    cx: float = 61.5,
    cy: float = 31.8,
    radius: float = 20.8,
) -> None:
    """Draw Ptolemy's Urbino golden armillary sphere in pure lines and circular arcs."""
    # Outer meridian ring & inner concentric rim
    mb.add_arc("golden", cx, cy, radius, 0.0, 180.0)
    mb.add_arc("golden", cx, cy, radius, 180.0, 360.0)
    mb.add_arc("golden", cx, cy, radius - 1.6, 0.0, 180.0)
    mb.add_arc("golden", cx, cy, radius - 1.6, 180.0, 360.0)

    # Polar axis rod, top celestial finial & lower support shaft
    mb.add_line("golden", cx + 0.6, cy - radius - 8.2, cx - 0.6, cy + radius + 14.0)
    mb.add_circle("golden", cx + 0.6, cy - radius - 5.2, 1.45)
    mb.add_circle("golden", cx + 0.6, cy - radius - 8.8, 0.9, filled=True)
    # Turned wooden/brass handle collar below sphere
    mb.add_line("golden", cx - 2.6, cy + radius + 2.2, cx + 1.8, cy + radius + 2.2)
    mb.add_line("golden", cx - 2.2, cy + radius + 4.8, cx + 1.4, cy + radius + 4.8)

    # Central geocentric Earth globe
    mb.add_circle("golden", cx, cy, 2.2, filled=True)

    # Meridional colure arcs curving from north to south pole
    p_north = (cx + 0.3, cy - radius + 1.6)
    p_south = (cx - 0.3, cy + radius - 1.6)
    for sag in (-11.0, -5.0, 5.0, 11.0):
        mb.add_arc_pts("golden", p_north, p_south, sag)

    # Horizontal celestial equator & tropics (Arctic, Cancer, Capricorn)
    mb.add_arc_pts("golden", (cx - radius + 1.8, cy), (cx + radius - 1.8, cy), -3.6)
    mb.add_arc_pts("golden", (cx - radius + 4.2, cy - 8.8), (cx + radius - 4.2, cy - 8.8), -2.6)
    mb.add_arc_pts("golden", (cx - radius + 4.2, cy + 8.8), (cx + radius - 4.2, cy + 8.8), -2.6)

    # Signature broad tilted zodiac / ecliptic band (front double-arc + back arc)
    e_l1 = (cx - radius + 2.2, cy - 7.8)
    e_r1 = (cx + radius - 1.8, cy + 2.8)
    e_l2 = (cx - radius + 1.6, cy - 3.0)
    e_r2 = (cx + radius - 2.4, cy + 7.4)
    mb.add_arc_pts("golden", e_l1, e_r1, -5.2)
    mb.add_arc_pts("golden", e_l2, e_r2, -5.2)
    mb.add_arc_pts("golden", e_l1, e_r1, 4.4)


def build_ptolemy_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the four-layer compass-and-straightedge geometry for Claudius Ptolemy.

    Uses ``MedallionBuilder`` so every line and circular arc is clipped cleanly
    within ``MED_R = 92.0`` with zero Bezier curves.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1 (Scaffold): Canonical medallion ring, eye line & golden circles
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-3.2,
        eye_rx=11.8,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Ptolemy's Theorem (Left), Epicycle-Deferent (Right)
    # & Urbino Armillary Sphere (Lower Right)
    # -------------------------------------------------------------------------
    _add_ptolemy_theorem_motif(mb, cx=-68.5, cy=-33.0, radius=11.6)
    _add_epicycle_deferent_motif(mb, cx=64.0, cy=-33.0, deferent_r=9.8)
    _add_armillary_sphere(mb, cx=61.5, cy=31.8, radius=20.8)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Astronomer-King Diadem, Rolled Turban & Flowing Hair
    # -------------------------------------------------------------------------
    # Subtle Renaissance astronomer-king diadem rising behind the rolled turban
    mb.add_arc_pts("primary", (-36.5, -55.0), (19.0, -57.5), 11.0)
    crown_spires: list[tuple[tuple[float, float], tuple[float, float], tuple[float, float]]] = [
        ((-36.5, -55.0), (-36.2, -66.5), (-28.8, -61.0)),
        ((-28.8, -61.0), (-22.5, -71.5), (-15.0, -64.5)),
        ((-15.0, -64.5), (-6.8, -75.0), (1.2, -65.0)),
        ((1.2, -65.0), (8.2, -72.0), (13.5, -62.5)),
        ((13.5, -62.5), (19.5, -66.8), (19.0, -57.5)),
    ]
    for p_l, p_tip, p_r in crown_spires:
        mb.add_line("primary", p_l[0], p_l[1], p_tip[0], p_tip[1])
        mb.add_line("primary", p_tip[0], p_tip[1], p_r[0], p_r[1])
        mb.add_circle("detail", p_tip[0], p_tip[1] - 0.8, 0.75)

    # Subtle jeweled band accents along the diadem base
    for jx, jy in ((-29.5, -57.8), (-18.5, -62.2), (-6.5, -64.0), (5.5, -62.5), (15.0, -59.2)):
        mb.add_circle("detail", jx, jy, 1.0)

    # Rolled white Renaissance turban wrap
    mb.add_arc_pts("primary", (-42.5, -42.5), (-2.0, -64.0), 8.2)
    mb.add_arc_pts("primary", (-2.0, -64.0), (25.5, -37.0), 8.8)
    mb.add_arc_pts("primary", (-26.5, -40.5), (21.5, -41.5), 8.6)
    mb.add_arc_pts("primary", (21.5, -41.5), (25.5, -37.0), 1.4)

    # Layered diagonal linen wraps across the turban
    mb.add_arc_pts("detail", (-37.5, -43.0), (23.0, -47.5), 11.2)
    mb.add_arc_pts("detail", (-32.5, -51.5), (23.5, -51.5), 9.6)
    mb.add_arc_pts("detail", (-22.5, -58.0), (18.5, -56.8), 6.2)
    mb.add_arc_pts("detail", (-25.5, -43.8), (20.2, -44.2), 8.2)

    # Soft outward-puffed left turban knot & hanging folded linen cloth tail
    mb.add_arc_pts("primary", (-42.5, -47.2), (-48.8, -52.5), 1.6)
    mb.add_arc_pts("primary", (-48.8, -52.5), (-44.2, -58.0), 1.8)
    mb.add_arc_pts("primary", (-44.2, -58.0), (-36.5, -55.0), 1.4)
    mb.add_arc_pts("detail", (-46.5, -53.2), (-40.5, -52.2), 1.2)

    mb.add_arc_pts("primary", (-42.5, -42.5), (-55.0, -24.5), 2.2)
    mb.add_arc_pts("primary", (-55.0, -24.5), (-57.8, -11.5), 1.4)
    mb.add_arc_pts("primary", (-57.8, -11.5), (-52.8, -7.8), -1.0)
    mb.add_arc_pts("primary", (-52.8, -7.8), (-44.5, -24.5), -1.6)
    mb.add_arc_pts("primary", (-44.5, -24.5), (-32.0, -39.5), -1.4)
    mb.add_arc_pts("detail", (-43.0, -39.5), (-54.2, -10.5), 2.2)

    # Full flowing wavy scholar locks framing both sides of the face
    mb.add_arc_pts("primary", (-48.5, -13.5), (-46.5, 4.0), -2.4)
    mb.add_arc_pts("primary", (-46.5, 4.0), (-32.0, 14.5), -2.2)
    mb.add_arc_pts("primary", (25.5, -37.0), (26.5, -15.5), 1.6)
    mb.add_arc_pts("primary", (26.5, -15.5), (21.5, 3.5), 1.5)
    mb.add_wave("detail", (-42.0, -22.5), (-38.5, 9.5), 4, wave_angle_deg * 0.65, 1)
    mb.add_wave("detail", (-34.5, -32.0), (-30.5, 10.5), 5, wave_angle_deg * 0.65, -1)
    mb.add_wave("detail", (-26.5, -34.0), (-24.5, 4.5), 4, wave_angle_deg * 0.6, 1)
    mb.add_wave("detail", (23.5, -32.0), (21.5, -2.5), 3, wave_angle_deg * 0.55, -1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Contemplative Three-Quarter Right Face, Eyes, Nose & Beard
    # -------------------------------------------------------------------------
    # Right facial contour (forehead -> orbit -> cheekbone -> beard transition)
    mb.add_arc_pts("primary", (19.5, -42.5), (21.5, -33.5), 1.0)
    mb.add_arc_pts("primary", (21.5, -33.5), (20.2, -26.0), -0.6)
    mb.add_arc_pts("primary", (20.2, -26.0), (21.2, -17.0), 1.0)
    mb.add_arc_pts("primary", (21.2, -17.0), (18.5, -7.0), 1.1)

    # Left temple & sunlit cheek curve descending into beard
    mb.add_arc_pts("primary", (-18.5, -42.0), (-20.8, -28.0), -1.1)
    mb.add_arc_pts("primary", (-20.8, -28.0), (-19.2, -14.0), -1.0)
    mb.add_arc_pts("detail", (-16.2, -19.5), (-11.0, -9.5), -1.0)

    # Wise furrowed forehead creases & expressive arched brows
    mb.add_arc_pts("detail", (-12.0, -40.5), (14.5, -39.5), 2.0)
    mb.add_arc_pts("detail", (-10.0, -37.5), (13.0, -36.8), 1.6)
    mb.add_arc_pts("detail", (4.5, -35.8), (5.0, -30.5), 0.25)
    mb.add_arc_pts("detail", (7.2, -35.2), (7.5, -30.2), -0.25)

    mb.add_arc_pts("primary", (-13.2, -32.0), (-5.0, -35.6), 1.1)
    mb.add_arc_pts("primary", (-5.0, -35.6), (2.2, -32.5), 1.0)
    mb.add_arc_pts("detail", (-12.2, -33.2), (1.2, -33.6), 1.2)

    mb.add_arc_pts("primary", (9.2, -31.8), (15.0, -33.6), 1.0)
    mb.add_arc_pts("primary", (15.0, -33.6), (20.2, -30.8), 0.9)

    # Contemplative downward-right eyes along y = -27
    # Viewer's left eye (nearer eye, heavy upper eyelid gazing down-right)
    l_out = (-9.8, -27.2)
    l_in = (0.4, -26.4)
    mb.add_arc_pts("primary", l_out, l_in, 1.9)
    mb.add_arc_pts("detail", (-10.5, -30.2), (1.0, -29.2), 2.1)
    mb.add_arc_pts("detail", l_out, l_in, -1.25)
    mb.add_circle("detail", -3.4, -26.6, 1.85)
    mb.add_circle("primary", -3.1, -26.5, 0.92, filled=True)
    mb.add_arc_pts("detail", (-9.8, -23.4), (0.0, -23.0), -1.0)

    # Viewer's right eye (further eye, gazing down-right toward armillary sphere)
    r_in = (8.5, -25.4)
    r_out = (17.2, -25.6)
    mb.add_arc_pts("primary", r_in, r_out, 1.75)
    mb.add_arc_pts("detail", (8.2, -28.4), (17.6, -28.4), 1.9)
    mb.add_arc_pts("detail", r_in, r_out, -1.1)
    mb.add_circle("detail", 12.0, -25.5, 1.7)
    mb.add_circle("primary", 12.2, -25.4, 0.85, filled=True)
    mb.add_arc_pts("detail", (8.8, -22.4), (16.8, -22.8), -0.95)

    # Sculpted noble Renaissance nose
    mb.add_arc_pts("primary", (4.5, -31.2), (7.2, -20.0), -0.35)
    mb.add_arc_pts("primary", (7.2, -20.0), (8.6, -13.5), 0.4)
    mb.add_arc_pts("primary", (8.6, -13.5), (5.8, -10.8), 0.8)
    mb.add_arc_pts("primary", (5.8, -10.8), (1.4, -11.0), 0.5)
    mb.add_arc_pts("primary", (1.4, -11.0), (-1.5, -13.2), 0.7)
    mb.add_arc_pts("detail", (-1.5, -13.2), (-0.6, -16.4), 0.45)
    mb.add_arc_pts("detail", (1.0, -25.8), (1.4, -16.8), 0.3)
    mb.add_arc_pts("detail", (5.2, -12.2), (2.2, -12.4), -0.4)

    # Sweeping moustache, contemplative lips & full scholar's beard
    mb.add_arc_pts("primary", (2.2, -8.8), (-11.2, -3.5), -1.6)
    mb.add_arc_pts("primary", (2.2, -8.8), (13.4, -4.4), 1.4)
    mb.add_arc_pts("primary", (-6.8, -5.0), (1.5, -4.4), 0.4)
    mb.add_arc_pts("primary", (1.5, -4.4), (8.2, -5.2), -0.35)
    mb.add_arc_pts("detail", (-4.8, -2.5), (1.8, -1.8), -0.75)
    mb.add_arc_pts("detail", (1.8, -1.8), (6.5, -2.8), -0.5)

    # Full flowing Renaissance beard contour & wave texture
    mb.add_arc_pts("primary", (-19.2, -14.0), (-23.0, 2.5), -1.8)
    mb.add_arc_pts("primary", (-23.0, 2.5), (-11.5, 13.5), -2.2)
    mb.add_arc_pts("primary", (-11.5, 13.5), (3.5, 16.5), -2.0)
    mb.add_arc_pts("primary", (3.5, 16.5), (15.5, 10.5), -2.0)
    mb.add_arc_pts("primary", (15.5, 10.5), (20.2, -0.5), -1.4)
    mb.add_arc_pts("primary", (20.2, -0.5), (18.5, -7.0), -0.8)

    mb.add_wave("detail", (-16.5, -6.0), (-12.0, 11.0), 3, wave_angle_deg * 0.65, 1)
    mb.add_wave("detail", (-9.5, -2.0), (-4.5, 14.0), 3, wave_angle_deg * 0.65, -1)
    mb.add_wave("detail", (-1.0, 0.5), (2.5, 14.8), 3, wave_angle_deg * 0.65, 1)
    mb.add_wave("detail", (7.5, -1.5), (10.5, 11.8), 3, wave_angle_deg * 0.6, -1)
    mb.add_wave("detail", (14.5, -4.0), (16.5, 7.0), 2, wave_angle_deg * 0.55, 1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Jeweled Shoulder Collar, Buttoned Robe & Contemplative Hands
    # -------------------------------------------------------------------------
    # Broad brocade jeweled shoulder collar
    mb.add_arc_pts("primary", (-76.5, 22.0), (-58.0, 8.5), 2.8)
    mb.add_arc_pts("primary", (-58.0, 8.5), (-32.0, 14.5), 1.8)
    mb.add_arc_pts("primary", (-76.5, 22.0), (-48.5, 31.5), -2.0)
    mb.add_arc_pts("primary", (-48.5, 31.5), (-14.0, 21.0), -1.6)
    mb.add_arc_pts("primary", (-14.0, 21.0), (14.0, 22.5), -1.2)
    mb.add_arc_pts("primary", (14.0, 22.5), (25.5, 28.5), 1.0)
    mb.add_arc_pts("primary", (25.5, 28.5), (29.5, 21.0), -1.2)
    mb.add_arc_pts("primary", (29.5, 21.0), (15.5, 10.5), -1.4)

    # Pearl studs along left collar border & right clasp pearl
    for px, py in ((-71.5, 19.8), (-64.8, 22.0), (-58.2, 24.4), (-51.5, 26.8), (22.5, 22.8)):
        mb.add_circle("detail", px, py, 1.8)
    mb.add_arc_pts("detail", (-65.0, 14.0), (-26.5, 20.0), -1.6)

    # Outer scholar robe shoulders & sleeves clipped cleanly to MED_R = 92.0
    mb.add_arc_pts("primary", (-76.5, 22.0), (-86.0, 48.0), -3.5)
    mb.add_arc_pts("primary", (-86.0, 48.0), (-78.0, 76.0), -3.2)
    mb.add_arc_pts("primary", (25.5, 28.5), (31.0, 41.2), 1.4)

    # Iconic three round jeweled medallion buttons cleanly seated inside MED_R
    for bx, by in ((-7.8, 27.0), (-2.2, 53.5), (1.8, 77.8)):
        mb.add_circle("primary", bx, by, 3.8)
        mb.add_circle("detail", bx, by, 1.9)

    # Flowing Renaissance robe drapery pleats clipped flush to MED_R
    mb.add_arc_pts("primary", (-48.5, 31.5), (-30.5, 88.0), 3.6)
    mb.add_arc_pts("detail", (-68.0, 32.0), (-61.5, 82.0), -2.5)
    mb.add_arc_pts("detail", (-56.0, 35.0), (-47.0, 86.0), 2.9)
    mb.add_arc_pts("detail", (-32.5, 28.0), (-17.5, 88.0), 2.5)
    mb.add_arc_pts("detail", (-21.0, 26.0), (-8.5, 88.0), 1.8)
    mb.add_arc_pts("detail", (6.0, 24.0), (10.5, 58.0), 1.4)
    mb.add_wave("detail", (-42.0, 36.0), (-29.0, 83.0), 4, wave_angle_deg * 0.42, 1)

    # Raised contemplative right hand resting on chest toward the armillary sphere
    mb.add_arc_pts("primary", (10.2, 86.0), (12.8, 60.0), -1.6)
    mb.add_arc_pts("primary", (12.8, 60.0), (17.2, 48.5), -1.2)
    # Index finger
    mb.add_arc_pts("primary", (17.2, 48.5), (35.5, 39.2), 1.4)
    mb.add_arc_pts("primary", (35.5, 39.2), (37.2, 42.2), 0.9)
    mb.add_arc_pts("primary", (37.2, 42.2), (25.2, 53.5), -0.9)
    # Middle finger
    mb.add_arc_pts("primary", (35.0, 44.5), (39.4, 46.2), 0.8)
    mb.add_arc_pts("primary", (39.4, 46.2), (38.8, 49.5), 0.7)
    mb.add_arc_pts("primary", (38.8, 49.5), (27.8, 60.5), -0.9)
    # Ring finger
    mb.add_arc_pts("primary", (36.5, 52.0), (40.5, 53.5), 0.7)
    mb.add_arc_pts("primary", (40.5, 53.5), (39.8, 56.8), 0.7)
    mb.add_arc_pts("primary", (39.8, 56.8), (30.5, 67.2), -0.8)
    # Little finger & outer palm edge descending cleanly to cuff
    mb.add_arc_pts("primary", (36.8, 59.8), (39.2, 62.5), 0.7)
    mb.add_arc_pts("primary", (39.2, 62.5), (33.5, 76.5), 1.4)
    mb.add_arc_pts("primary", (33.5, 76.5), (30.2, 86.0), 0.8)
    mb.add_arc_pts("detail", (17.5, 63.5), (24.5, 54.0), 0.8)
    mb.add_arc_pts("detail", (21.0, 70.0), (28.5, 60.8), 0.8)

    # Subtle right robe sleeve fold descending cleanly into the lower medallion rim
    mb.add_arc_pts("primary", (34.8, 72.5), (56.5, 68.5), -1.8)
    mb.add_arc_pts("detail", (33.0, 79.0), (50.5, 75.5), -1.4)

    return mb.build()


def build_ptolemy_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Claudius Ptolemy medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_ptolemy_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_ptolemy_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``ptolemy_dark.svg`` and ``ptolemy_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "ptolemy_dark.svg"
    light_path = target_dir / "ptolemy_light.svg"
    dark_path.write_text(
        build_ptolemy_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_ptolemy_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
