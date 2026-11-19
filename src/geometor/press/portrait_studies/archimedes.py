"""Study 08: Archimedes of Syracuse (after Domenico Fetti, 1620) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_archimedes_elements",
    "build_archimedes_svg",
    "write_archimedes_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_tombstone_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float,
) -> None:
    """Draw Archimedes' Tombstone Theorem (circumscribed cylinder & inscribed sphere, 2:3).

    Placed cleanly in the open left medallion margin using strictly straight segments,
    circles, and circular arcs.
    """
    # Inscribed sphere
    mb.add_circle("golden", cx, cy, radius)
    # Front equatorial meridian arc for spherical depth
    mb.add_arc_pts("golden", (cx - radius, cy), (cx + radius, cy), -3.0)

    # Circumscribed right circular cylinder walls (height = 2R, diameter = 2R)
    top_y = cy - radius
    bot_y = cy + radius
    left_x = cx - radius
    right_x = cx + radius
    mb.add_line("golden", left_x, top_y, left_x, bot_y)
    mb.add_line("golden", right_x, top_y, right_x, bot_y)

    # Top and bottom circular-arc cylinder rims
    rim_sag = 3.0
    mb.add_arc_pts("golden", (left_x, top_y), (right_x, top_y), rim_sag)
    mb.add_arc_pts("golden", (left_x, top_y), (right_x, top_y), -rim_sag)
    mb.add_arc_pts("golden", (left_x, bot_y), (right_x, bot_y), rim_sag)
    mb.add_arc_pts("golden", (left_x, bot_y), (right_x, bot_y), -rim_sag)

    # Vertical symmetry axis & four tangency contact nodes
    mb.add_line("golden", cx, top_y - 5.5, cx, bot_y + 5.5)
    for tx, ty in (
        (cx, top_y),
        (cx, bot_y),
        (left_x, cy),
        (right_x, cy),
    ):
        mb.add_circle("golden", tx, ty, 1.05)


def _add_exhaustion_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float,
) -> None:
    """Draw Archimedes' method of exhaustion (inscribed & circumscribed regular hexagons).

    Placed cleanly in the open right medallion margin, illustrating the classic
    Archimedean bounds on pi around a circle of radius ``radius``.
    """
    mb.add_circle("golden", cx, cy, radius)
    r_out = radius / math.cos(math.radians(30.0))

    in_pts = [polar(cx, cy, radius, 60.0 * k) for k in range(6)]
    out_pts = [polar(cx, cy, r_out, 60.0 * k) for k in range(6)]

    for k in range(6):
        p1 = in_pts[k]
        p2 = in_pts[(k + 1) % 6]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

        q1 = out_pts[k]
        q2 = out_pts[(k + 1) % 6]
        mb.add_line("golden", q1[0], q1[1], q2[0], q2[1])

    # Three principal diameters subdividing into six equilateral triangles
    for k in range(3):
        p1 = in_pts[k]
        p2 = in_pts[k + 3]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    mb.add_circle("golden", cx, cy, 1.1)


def build_archimedes_elements(wave_angle_deg: float = 34.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Archimedes of Syracuse medallion strictly from lines, circles, and circular arcs.

    Calibrated to Domenico Fetti's *Archimedes Thoughtful* (1620, Gemaldegalerie Alte Meister,
    Dresden) with downward-right contemplative gaze, furrowed scholar's brow, thick curly hair,
    bushy scholar beard, thoughtful hand resting under jaw/beard, and gathered white sleeve cuff.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc beard, hair, and
            drapery waves.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``detail``, and ``primary`` primitive lists.
    """
    mb = MedallionBuilder()

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    mb.add_scaffold_base(
        eye_lx=-8.5,
        eye_rx=10.0,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # -------------------------------------------------------------------------
    # Layer 2 (Golden): Margin-Placed Archimedean Signatures
    # -------------------------------------------------------------------------
    _add_tombstone_motif(mb, cx=-62.0, cy=-26.0, radius=13.5)
    _add_exhaustion_motif(mb, cx=62.0, cy=-26.0, radius=13.5)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Face, Furrowed Brow, Deep-Set Eyes, Nose & Mustache
    # -------------------------------------------------------------------------
    # Right facial contour (lit temple -> cheekbone -> transition into beard)
    mb.add_arc_pts("primary", (19.5, -42.0), (21.5, -31.5), -1.4)
    mb.add_arc_pts("primary", (21.5, -31.5), (19.8, -23.5), 0.7)
    mb.add_arc_pts("primary", (19.8, -23.5), (18.8, -13.0), -1.3)

    # Left facial contour (shadowed temple -> cheekbone -> tucking behind curled fingers)
    mb.add_arc_pts("primary", (-17.8, -44.8), (-20.2, -33.5), 1.4)
    mb.add_arc_pts("primary", (-20.2, -33.5), (-19.8, -18.5), 1.7)

    # Hairline framing the broad furrowed forehead (with iconic dark overhanging lock)
    mb.add_arc_pts("primary", (-17.8, -44.8), (-5.0, -51.2), 2.0)
    mb.add_arc_pts("primary", (-5.0, -51.2), (4.5, -50.2), 0.8)
    mb.add_arc_pts("primary", (4.5, -50.2), (16.5, -46.5), -1.2)
    mb.add_arc_pts("primary", (16.5, -46.5), (21.5, -40.5), 1.0)
    # Dark forehead lock lower edge sweeping across upper-right brow
    mb.add_arc_pts("detail", (3.5, -47.0), (19.5, -42.5), -1.4)

    # Furrowed scholar's forehead wrinkles (tilted ~11 deg with head)
    mb.add_arc_pts("detail", (-1.5, -45.0), (17.5, -40.5), -1.1)
    mb.add_arc_pts("detail", (-6.0, -41.5), (17.5, -36.5), -1.4)
    mb.add_arc_pts("detail", (-6.5, -38.0), (15.8, -33.2), -1.2)
    # Vertical glabella furrows between the knitted brows
    mb.add_arc_pts("detail", (0.8, -35.2), (1.2, -30.5), -0.4)
    mb.add_arc_pts("detail", (3.6, -34.2), (3.8, -29.8), 0.4)

    # Furrowed eyebrows
    # Viewer's left brow (knitted downward toward glabella)
    mb.add_arc_pts("primary", (-17.0, -33.0), (-8.8, -35.4), 1.2)
    mb.add_arc_pts("primary", (-8.8, -35.4), (-1.2, -32.4), 1.0)
    mb.add_arc_pts("detail", (-16.2, -34.6), (-2.0, -34.0), 1.5)

    # Viewer's right brow (arched over lit contemplative eye)
    mb.add_arc_pts("primary", (3.2, -31.5), (11.2, -31.2), 1.3)
    mb.add_arc_pts("primary", (11.2, -31.2), (18.2, -27.2), 1.1)
    mb.add_arc_pts("detail", (3.8, -33.0), (17.6, -28.8), 1.6)

    # Deep-set eyes with heavy hooded lids and downward-right contemplative gaze
    # Viewer's left eye (in shadow, tilted ~11 deg)
    l_out = (-14.2, -28.8)
    l_in = (-3.4, -26.5)
    mb.add_arc_pts("primary", l_out, l_in, 1.6)
    mb.add_arc_pts("detail", (-14.0, -30.6), (-3.2, -28.2), 1.8)
    mb.add_arc_pts("detail", l_out, l_in, -0.9)
    # Half-hooded iris & downward-right pupil nestled beneath upper lid
    mb.add_arc("detail", -8.0, -27.2, 1.8, -10.0, 195.0)
    mb.add_circle("primary", -7.8, -26.8, 0.95, filled=True)
    mb.add_arc_pts("detail", (-14.5, -25.4), (-4.0, -23.4), -1.1)

    # Viewer's right eye (lit, heavy hooded upper lid, contemplative downward gaze)
    r_in = (4.6, -24.8)
    r_out = (15.5, -22.5)
    mb.add_arc_pts("primary", r_in, r_out, 1.4)
    mb.add_arc_pts("detail", (4.3, -27.0), (16.0, -24.2), 2.0)
    mb.add_arc_pts("detail", r_in, r_out, -0.9)
    # Half-hooded iris & downward-right pupil nestled beneath upper lid
    mb.add_arc("detail", 10.3, -23.2, 1.8, -10.0, 195.0)
    mb.add_circle("primary", 10.5, -22.8, 0.95, filled=True)
    # Prominent lower lid / cheekbone crease on lit right cheek
    mb.add_arc_pts("detail", (5.2, -20.0), (16.5, -18.8), -1.5)
    mb.add_arc_pts("detail", (14.8, -21.0), (18.8, -20.3), 0.5)

    # Aquiline nose (following the clockwise head tilt)
    mb.add_arc_pts("primary", (2.2, -31.0), (-1.2, -13.0), -0.8)
    mb.add_arc_pts("detail", (4.0, -26.8), (2.2, -15.8), -0.5)
    # Nose tip & nostrils (clean smooth curves)
    mb.add_arc_pts("primary", (-1.2, -13.0), (1.8, -11.5), -0.8)
    mb.add_arc_pts("primary", (1.8, -11.5), (3.5, -13.8), -0.7)
    mb.add_arc_pts("detail", (3.5, -13.8), (2.4, -16.2), -0.5)
    mb.add_arc_pts("primary", (-1.2, -13.0), (-4.5, -14.8), -0.7)
    mb.add_arc_pts("detail", (-4.5, -14.8), (-4.0, -17.0), 0.5)

    # Cheek nasolabial creases flowing into mustache
    mb.add_arc_pts("detail", (4.8, -15.8), (14.5, -11.8), 1.1)
    mb.add_arc_pts("detail", (-6.0, -17.6), (-14.2, -14.8), -1.0)

    # Sweeping bushy mustache (blending organically into the beard at outer wings)
    mb.add_arc_pts("primary", (-1.0, -10.8), (10.8, -9.4), 1.5)
    mb.add_arc_pts("primary", (10.8, -9.4), (21.5, -3.2), 1.7)
    mb.add_arc_pts("primary", (-1.0, -10.8), (-10.0, -12.8), -1.2)
    mb.add_arc_pts("primary", (-10.0, -12.8), (-17.5, -13.5), -0.8)
    # Lower mustache margin & subtle mouth parting
    mb.add_arc_pts("primary", (-3.5, -7.2), (8.2, -4.6), 1.3)
    mb.add_arc_pts("primary", (8.2, -4.6), (17.5, -1.5), -0.9)
    mb.add_arc_pts("detail", (-7.5, -9.5), (-1.5, -7.2), -0.6)
    # Mustache strand texture
    mb.add_wave("detail", (0.5, -9.0), (17.5, -4.0), 3, wave_angle_deg * 0.68, 1)
    mb.add_wave("detail", (-1.8, -9.2), (-14.5, -11.8), 2, wave_angle_deg * 0.65, -1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Thick Curly Hair & Crown
    # -------------------------------------------------------------------------
    # Outer hair mass silhouette with organic curly tufts
    mb.add_arc_pts("primary", (-28.5, -15.5), (-30.2, -28.0), 2.2)
    mb.add_arc_pts("primary", (-30.2, -28.0), (-29.0, -42.5), 2.4)
    mb.add_arc_pts("primary", (-29.0, -42.5), (-25.8, -56.0), 2.6)
    mb.add_arc_pts("primary", (-25.8, -56.0), (-15.5, -70.5), 2.8)
    mb.add_arc_pts("primary", (-15.5, -70.5), (1.0, -76.0), 2.8)
    mb.add_arc_pts("primary", (1.0, -76.0), (17.5, -70.0), 2.6)
    mb.add_arc_pts("primary", (17.5, -70.0), (26.5, -57.5), 2.4)
    mb.add_arc_pts("primary", (26.5, -57.5), (27.5, -48.0), 1.4)
    # Iconic curling lock projecting at upper-right temple
    mb.add_arc_pts("primary", (27.5, -48.0), (31.5, -40.5), 2.0)
    mb.add_arc_pts("primary", (31.5, -40.5), (26.8, -32.0), 2.2)
    mb.add_arc_pts("primary", (26.8, -32.0), (24.5, -22.5), 1.6)
    mb.add_arc_pts("primary", (24.5, -22.5), (21.5, -15.0), 1.4)

    # Interior curly hair waves (Euclid III.12 tangent-arc locks)
    mb.add_wave("detail", (-16.0, -66.5), (16.5, -63.0), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (-22.5, -57.5), (22.5, -53.0), 5, wave_angle_deg, -1)
    mb.add_wave("detail", (-24.5, -46.5), (-13.0, -56.5), 3, wave_angle_deg * 0.85, 1)
    mb.add_wave("detail", (6.0, -56.0), (25.0, -47.0), 3, wave_angle_deg * 0.85, -1)
    mb.add_wave("detail", (-26.5, -39.0), (-23.5, -19.0), 3, wave_angle_deg * 0.8, 1)
    mb.add_wave("detail", (24.5, -44.0), (22.5, -24.0), 3, wave_angle_deg * 0.8, -1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Flowing Bushy Scholar Beard
    # -------------------------------------------------------------------------
    # Right beard contour (bright sweeping mass down to point and back to hand)
    mb.add_arc_pts("primary", (21.5, -15.0), (24.0, -5.0), 2.0)
    mb.add_arc_pts("primary", (24.0, -5.0), (20.5, 7.0), 2.2)
    mb.add_arc_pts("primary", (20.5, 7.0), (14.5, 17.5), 1.8)
    mb.add_arc_pts("primary", (14.5, 17.5), (6.5, 23.0), 1.6)
    mb.add_arc_pts("primary", (6.5, 23.0), (0.5, 18.0), 1.4)

    # Left beard mass (tucking behind curled fingers)
    mb.add_arc_pts("primary", (-28.5, -15.5), (-32.0, -7.5), -1.8)
    mb.add_arc_pts("primary", (-32.0, -7.5), (-27.5, -1.0), -1.5)

    # Interior bushy beard flow waves (Euclid III.12)
    mb.add_wave("detail", (1.5, -3.5), (15.5, 11.5), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (7.5, -4.0), (20.0, 5.5), 3, wave_angle_deg, -1)
    mb.add_wave("detail", (-2.0, -1.5), (9.5, 18.5), 4, wave_angle_deg * 0.9, 1)
    mb.add_wave("detail", (-1.5, 4.5), (4.5, 19.5), 3, wave_angle_deg * 0.8, -1)
    mb.add_wave("detail", (-14.5, -13.0), (-26.5, -5.5), 3, wave_angle_deg * 0.8, 1)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Contemplative Hand Resting Under Beard / Jaw
    # -------------------------------------------------------------------------
    # Right illuminated edge of hand (thumb/index pressing into beard -> wrist)
    mb.add_arc_pts("primary", (-10.8, -6.8), (-5.2, 2.5), 1.4)
    mb.add_arc_pts("primary", (-5.2, 2.5), (-0.5, 12.5), 1.3)
    mb.add_arc_pts("primary", (-0.5, 12.5), (1.8, 25.5), 1.1)
    mb.add_arc_pts("primary", (1.8, 25.5), (2.2, 30.0), 0.5)

    # Sculpted curled fingers stepping gracefully down-left into outer palm & wrist
    # Index finger arch & separation
    mb.add_arc_pts("primary", (-17.5, -7.2), (-10.8, -6.8), 1.4)
    mb.add_arc_pts("primary", (-17.5, -7.2), (-15.0, 5.5), -0.9)
    # Middle finger arch & separation
    mb.add_arc_pts("primary", (-23.8, -4.0), (-17.5, -7.2), 1.3)
    mb.add_arc_pts("primary", (-23.8, -4.0), (-21.0, 9.5), -1.0)
    # Ring & outer curled finger -> tapered palm -> left wrist
    mb.add_arc_pts("primary", (-29.5, 2.0), (-23.8, -4.0), 1.5)
    mb.add_arc_pts("primary", (-29.5, 2.0), (-30.5, 11.8), -1.5)
    mb.add_arc_pts("primary", (-30.5, 11.8), (-24.2, 21.5), -1.6)
    mb.add_arc_pts("primary", (-24.2, 21.5), (-19.8, 30.5), -0.9)
    mb.add_arc_pts("primary", (-19.8, 30.5), (-18.2, 39.5), -0.6)

    # Continuous sculpted knuckle & metacarpal tendon lines (no abrupt kinks)
    mb.add_arc_pts("detail", (-15.0, 5.5), (-9.2, 19.5), -1.2)
    mb.add_arc_pts("detail", (-21.0, 9.5), (-15.5, 24.0), -1.3)
    mb.add_arc_pts("detail", (-26.2, 8.8), (-21.8, 19.2), -1.0)
    mb.add_arc_pts("detail", (-9.0, 9.5), (-3.5, 25.0), 0.8)
    mb.add_arc_pts("detail", (-14.0, 24.5), (-8.5, 33.5), -0.7)

    # -------------------------------------------------------------------------
    # Layer 3 & 4: Gathered White Cuff Sleeve & Rustic Scholar's Robe
    # -------------------------------------------------------------------------
    # Gathered cuff rim wrapping around wrist
    mb.add_arc_pts("primary", (-18.5, 40.0), (-6.5, 36.5), 2.2)
    mb.add_arc_pts("primary", (-6.5, 36.5), (2.2, 28.5), 1.8)
    mb.add_arc_pts("primary", (2.2, 28.5), (5.5, 32.5), 1.2)
    mb.add_arc_pts("detail", (-16.5, 42.5), (3.8, 32.0), 1.5)

    # Puffed white sleeve outer boundaries descending cleanly to medallion rim
    mb.add_arc_pts("primary", (-18.5, 40.0), (-21.5, 56.5), -2.4)
    mb.add_arc_pts("primary", (-21.5, 56.5), (-15.5, 74.0), -2.0)
    mb.add_arc_pts("primary", (-15.5, 74.0), (-11.0, 86.0), -1.0)

    mb.add_arc_pts("primary", (5.5, 32.5), (14.5, 50.0), 2.6)
    mb.add_arc_pts("primary", (14.5, 50.0), (19.5, 68.5), 2.0)
    mb.add_arc_pts("primary", (19.5, 68.5), (23.0, 84.0), 1.2)

    # Crisp non-crossing gathered linen folds radiating from wrist cuff
    mb.add_arc_pts("detail", (-13.0, 40.5), (-14.5, 72.0), -2.5)
    mb.add_arc_pts("detail", (-7.5, 38.5), (-6.5, 78.0), -2.0)
    mb.add_arc_pts("detail", (-1.5, 35.5), (2.5, 80.0), 2.0)
    mb.add_arc_pts("detail", (3.2, 34.5), (12.5, 77.5), 2.6)
    mb.add_arc_pts("detail", (-12.5, 81.5), (21.0, 79.5), -2.2)

    # Right scholar's robe (warm ochre shoulder & bent upper arm)
    mb.add_arc_pts("primary", (22.5, -1.5), (38.0, 9.0), 3.4)
    mb.add_arc_pts("primary", (38.0, 9.0), (43.5, 29.0), 3.2)
    mb.add_arc_pts("primary", (43.5, 29.0), (38.5, 51.0), 2.8)
    mb.add_arc_pts("primary", (38.5, 51.0), (26.5, 65.0), 2.4)
    # Inner arm seam & lower robe drape clipped cleanly to medallion rim
    mb.add_arc_pts("primary", (14.5, 21.0), (17.5, 40.5), 1.6)
    mb.add_arc_pts("primary", (17.5, 40.5), (16.5, 55.5), -1.2)
    mb.add_arc_pts("primary", (26.5, 65.0), (47.5, 78.5), -1.8)
    # Right sleeve drapery folds (flowing cleanly with the arm)
    mb.add_arc_pts("detail", (28.5, 7.0), (36.5, 36.5), 2.6)
    mb.add_arc_pts("detail", (22.5, 16.0), (29.5, 47.5), 2.2)
    mb.add_arc_pts("detail", (21.0, 52.0), (36.0, 59.5), -2.0)

    # Left scholar's mantle (kept cleanly below the left golden Tombstone motif, clipped to rim)
    mb.add_arc_pts("primary", (-29.5, -1.5), (-48.0, 11.5), -3.2)
    mb.add_arc_pts("primary", (-48.0, 11.5), (-61.0, 32.5), -3.4)
    mb.add_arc_pts("primary", (-61.0, 32.5), (-68.5, 66.0), -2.6)
    # Diagonal robe folds flowing parallel down the shadowed left torso
    mb.add_arc_pts("detail", (-43.0, 14.0), (-58.5, 58.0), -2.8)
    mb.add_arc_pts("detail", (-35.5, 11.0), (-49.0, 68.0), -2.8)
    mb.add_arc_pts("detail", (-28.5, 24.0), (-38.5, 76.0), -2.2)
    mb.add_arc_pts("detail", (-23.0, 42.0), (-27.5, 81.0), -1.6)

    return mb.build()


def build_archimedes_svg(theme: str = "dark", wave_angle_deg: float = 34.0) -> str:
    """Render the Archimedes medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_archimedes_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_archimedes_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 34.0,
) -> tuple[Path, Path]:
    """Write ``archimedes_dark.svg`` and ``archimedes_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "archimedes_dark.svg"
    light_path = target_dir / "archimedes_light.svg"
    dark_path.write_text(
        build_archimedes_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_archimedes_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
