"""Study 29: Lorenzo Mascheroni (after the Neoclassical profile engraving by F. Redenti)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_mascheroni_elements",
    "build_mascheroni_svg",
    "write_mascheroni_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_napoleon_quartering_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    radius: float = 9.8,
) -> None:
    """Draw Napoleon's compass-only circle quartering (Mascheroni construction).

    Uses strictly circles and circular arcs (zero straight lines):
    1. Base circle ``(O, r)`` with starting vertex ``A`` at top (``-90 deg``).
    2. Radius-``r`` compass steps from ``A`` and antipode ``D`` marking hexagonal
       chords inside the circle.
    3. Two intersecting radius-``r*sqrt(3)`` arcs centered at ``A`` and ``D``
       locating point ``M = (cx + r*sqrt(2), cy)``.
    4. Final compass swing centered at ``A`` with radius ``OM = r*sqrt(2)``
       cutting the base circle at the exact quarter-circle vertices ``E, F``.
    """
    pt_a = (cx, cy - radius)
    pt_d = (cx, cy + radius)
    pt_e = (cx - radius, cy)
    pt_f = (cx + radius, cy)
    r_sqrt2 = radius * math.sqrt(2.0)
    r_sqrt3 = radius * math.sqrt(3.0)
    pt_m = (cx + r_sqrt2, cy)

    # 1. Base circle and center O
    mb.add_circle("golden", cx, cy, radius)
    mb.add_circle("golden", cx, cy, 0.6, filled=True)

    # 2. Internal radius-r stepping arcs from A and D (establishing diameter AD)
    mb.add_arc("golden", pt_a[0], pt_a[1], radius, 30.0, 150.0)
    mb.add_arc("golden", pt_d[0], pt_d[1], radius, -150.0, -30.0)

    # 3. Intersecting radius-r*sqrt(3) arcs from A and D meeting at M
    ang_a_to_m = math.degrees(math.atan2(pt_m[1] - pt_a[1], pt_m[0] - pt_a[0]))
    ang_d_to_m = math.degrees(math.atan2(pt_m[1] - pt_d[1], pt_m[0] - pt_d[0]))
    mb.add_arc("golden", pt_a[0], pt_a[1], r_sqrt3, ang_a_to_m - 22.0, ang_a_to_m + 20.0)
    mb.add_arc("golden", pt_d[0], pt_d[1], r_sqrt3, ang_d_to_m - 20.0, ang_d_to_m + 22.0)

    # 4. Final compass swing of radius OM = r*sqrt(2) centered at A cutting E & F
    mb.add_arc("golden", pt_a[0], pt_a[1], r_sqrt2, 40.0, 140.0)

    # Marked quarter-circle square vertices A, F, D, E and auxiliary node M
    for vx, vy in (pt_a, pt_f, pt_d, pt_e):
        mb.add_circle("golden", vx, vy, 0.9, filled=True)
    mb.add_circle("golden", pt_m[0], pt_m[1], 0.85)


def _add_seed_of_life_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
    petal_r: float = 6.2,
) -> None:
    """Draw the compass-only Six-Petal Rosette (Seed of Life) in the right margin.

    Constructs the central circle of radius ``petal_r``, six congruent circles
    centered on its hexagonal vertices, and the enclosing outer compass circle
    of radius ``2 * petal_r`` (zero straight lines).
    """
    mb.add_circle("golden", cx, cy, petal_r)
    mb.add_circle("golden", cx, cy, 2.0 * petal_r)
    for k in range(6):
        rad = math.radians(60.0 * k - 90.0)
        mb.add_circle(
            "golden",
            cx + petal_r * math.cos(rad),
            cy + petal_r * math.sin(rad),
            petal_r,
        )
    mb.add_circle("golden", cx, cy, 0.65, filled=True)


def build_mascheroni_elements(wave_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Lorenzo Mascheroni.

    Calibrated to F. Redenti's Neoclassical pure left-profile engraving:
    sculpted forehead, straight classical nose, composed lips, rounded chin,
    profile eye on ``y = -27``, flowing late-18th-century wavy back hair
    modeled with ``Euclid III.12`` tangent wave strands, wrapped white cravat,
    and tailored double-breasted coat collar & lapels grounded to ``MED_R``.
    Both golden margin motifs are strictly compass-only (zero straight lines).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-12.5,
        eye_rx=8.5,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- PURE COMPASS-ONLY GOLDEN MARGIN MOTIFS (zero face crossing) ---
    _add_napoleon_quartering_motif(mb, cx=-65.5, cy=-26.0, radius=9.8)
    _add_seed_of_life_motif(mb, cx=63.0, cy=-26.0, petal_r=6.2)

    # --- PURE LEFT PROFILE FACE CONTOUR ---
    # Noble Neoclassical forehead down to brow ridge & nasal bridge
    mb.add_arc_pts("primary", (-11.5, -46.5), (-16.2, -34.0), -1.1)
    mb.add_arc_pts("primary", (-16.2, -34.0), (-15.8, -29.2), 0.5)
    # Straight classical nose bridge to tip and subnasale
    mb.add_arc_pts("primary", (-15.8, -29.2), (-23.4, -18.6), -0.45)
    mb.add_arc_pts("primary", (-23.4, -18.6), (-22.0, -16.2), -0.8)
    mb.add_arc_pts("primary", (-22.0, -16.2), (-18.4, -15.8), -0.3)
    # Delicate profile nostril wing & crease
    mb.add_arc_pts("primary", (-19.2, -16.8), (-16.2, -17.4), 0.55)
    mb.add_arc_pts("primary", (-16.2, -17.4), (-15.4, -16.1), 0.4)
    mb.add_arc_pts("detail", (-19.8, -16.4), (-17.2, -16.3), -0.35)
    # Philtrum, composed lips & rounded chin
    mb.add_arc_pts("primary", (-18.4, -15.8), (-19.4, -12.6), 0.45)
    mb.add_arc_pts("primary", (-19.4, -12.6), (-17.8, -10.8), -0.4)
    mb.add_arc_pts("primary", (-17.8, -10.8), (-13.2, -11.0), -0.35)
    mb.add_arc_pts("detail", (-13.2, -11.0), (-11.8, -11.6), 0.25)
    mb.add_arc_pts("primary", (-17.8, -10.8), (-18.5, -8.8), -0.45)
    mb.add_arc_pts("primary", (-18.5, -8.8), (-16.8, -7.2), 0.45)
    mb.add_arc_pts("primary", (-16.8, -7.2), (-17.5, -3.4), -0.6)
    mb.add_arc_pts("primary", (-17.5, -3.4), (-14.2, -0.2), -0.9)
    # Chin underside & throat line meeting cravat
    mb.add_arc_pts("primary", (-14.2, -0.2), (-5.2, 1.5), -1.1)
    mb.add_arc_pts("primary", (-5.2, 1.5), (-7.2, 6.2), -0.5)
    # Soft jawline & cheek plane modeling (detail)
    mb.add_arc_pts("detail", (6.2, -12.5), (-0.5, -3.5), -1.0)
    mb.add_arc_pts("detail", (-0.5, -3.5), (-9.5, -0.8), -0.7)
    mb.add_arc_pts("detail", (-14.0, -14.2), (-11.5, -10.2), 0.45)

    # --- PROFILE EYEBROW & EYE ON y = -27 (LOOKING LEFT) ---
    mb.add_arc_pts("primary", (-15.5, -33.2), (-11.0, -33.6), 0.65)
    mb.add_arc_pts("primary", (-11.0, -33.6), (-6.2, -30.6), 0.55)
    mb.add_arc_pts("detail", (-14.8, -32.2), (-7.0, -29.8), 0.75)

    # Pure profile eye: upper lid, fold, lower lid, cornea/iris curve & filled pupil
    mb.add_arc_pts("primary", (-14.8, -28.0), (-7.6, -26.2), 1.65)
    mb.add_arc_pts("detail", (-14.8, -29.6), (-7.4, -27.8), 1.45)
    mb.add_arc_pts("detail", (-14.2, -25.4), (-7.6, -26.2), -0.95)
    mb.add_arc_pts("detail", (-13.6, -23.4), (-8.4, -23.6), -0.65)
    mb.add_arc_pts("detail", (-13.2, -28.2), (-13.0, -25.3), -0.85)
    mb.add_arc_pts("detail", (-11.8, -28.2), (-11.6, -25.4), 0.45)
    mb.add_circle("primary", -12.8, -26.8, 1.0, filled=True)

    # --- LEFT EAR (VISIBLE IN PROFILE) ---
    mb.add_arc_pts("primary", (8.4, -21.6), (13.4, -20.2), 1.1)
    mb.add_arc_pts("primary", (13.4, -20.2), (12.6, -14.6), 1.1)
    mb.add_arc_pts("primary", (12.6, -14.6), (8.2, -13.4), 0.9)
    mb.add_arc_pts("primary", (8.2, -13.4), (6.5, -15.6), 0.6)
    mb.add_arc_pts("detail", (9.2, -19.8), (11.4, -17.4), 0.8)
    mb.add_arc_pts("detail", (11.4, -17.4), (9.0, -15.2), 0.7)

    # --- LATE-18TH-CENTURY WAVY CRANIAL & NAPE HAIR ---
    # Smooth outer cranium silhouette curving down over back curls
    mb.add_arc_pts("primary", (-11.5, -46.5), (5.0, -54.2), 2.8)
    mb.add_arc_pts("primary", (5.0, -54.2), (24.5, -43.5), 3.6)
    mb.add_arc_pts("primary", (24.5, -43.5), (30.2, -25.5), 2.8)
    # Cascading curled locks resting cleanly atop the high coat collar
    mb.add_arc_pts("primary", (30.2, -25.5), (27.8, -18.0), 0.9)
    mb.add_arc_pts("primary", (27.8, -18.0), (30.6, -10.5), 1.6)
    mb.add_arc_pts("primary", (30.6, -10.5), (27.4, -3.6), 1.3)
    mb.add_arc_pts("primary", (27.4, -3.6), (21.5, -0.4), 1.2)
    mb.add_arc_pts("primary", (21.5, -0.4), (14.5, -0.6), 0.8)
    mb.add_arc_pts("primary", (14.5, -0.6), (11.2, -3.2), 0.6)

    # Temple hairline & tapered sideburn in front of ear
    mb.add_arc_pts("primary", (-11.5, -46.5), (-4.0, -40.8), 1.2)
    mb.add_arc_pts("primary", (-4.0, -40.8), (1.8, -33.2), -1.0)
    mb.add_arc_pts("primary", (1.8, -33.2), (4.5, -24.0), 0.9)
    mb.add_arc_pts("primary", (4.5, -24.0), (5.5, -16.2), -0.6)
    mb.add_arc_pts("primary", (5.5, -16.2), (3.8, -12.4), 0.6)
    mb.add_arc_pts("primary", (3.8, -12.4), (7.5, -12.8), -0.5)

    # Flowing Euclid III.12 tangent wave strands through the 18th-century hair
    mb.add_wave("detail", (-7.5, -47.5), (22.0, -39.5), 4, wave_angle_deg - 4.0, 1)
    mb.add_wave("detail", (-2.0, -48.5), (26.5, -31.5), 4, wave_angle_deg - 2.0, -1)
    mb.add_wave("detail", (1.5, -43.5), (26.0, -22.5), 4, wave_angle_deg, 1)
    mb.add_wave("detail", (4.5, -36.0), (26.5, -12.0), 4, wave_angle_deg + 4.0, -1)
    mb.add_wave("detail", (7.5, -28.0), (24.0, -4.5), 4, wave_angle_deg + 6.0, 1)
    mb.add_wave("detail", (14.5, -15.5), (19.0, -2.5), 3, wave_angle_deg + 8.0, -1)

    # --- WRAPPED WHITE CRAVAT / STOCK & TAILORED 18TH-CENTURY COAT ---
    # Neck back & wrapped cravat contours
    mb.add_arc_pts("primary", (9.5, -11.5), (11.2, -3.2), -0.7)
    mb.add_arc_pts("primary", (-7.2, 6.2), (-6.8, 12.2), 0.6)
    mb.add_arc_pts("primary", (-6.8, 12.2), (-14.5, 22.0), 1.0)
    # Layered horizontal cravat stock folds
    mb.add_arc_pts("detail", (-6.5, 4.8), (9.5, -3.2), -1.2)
    mb.add_arc_pts("detail", (-6.6, 8.6), (8.8, 0.8), -1.2)
    mb.add_arc_pts("detail", (-8.5, 13.5), (4.5, 6.2), -1.1)
    mb.add_arc_pts("detail", (-11.8, 18.2), (-2.5, 12.2), -0.8)

    # High folded Neoclassical coat collar starting cleanly beneath back curl
    mb.add_arc_pts("primary", (25.2, -1.2), (31.5, 13.8), 1.5)
    mb.add_arc_pts("primary", (31.5, 13.8), (18.2, 22.8), 1.2)
    mb.add_arc_pts("primary", (18.2, 22.8), (10.5, 5.5), -1.2)
    mb.add_arc_pts("primary", (10.5, 5.5), (-3.5, 10.5), -0.9)

    # Near-side (left) wide folded coat lapel descending down chest
    mb.add_arc_pts("primary", (10.5, 5.5), (-2.5, 21.5), 1.2)
    mb.add_arc_pts("primary", (-2.5, 21.5), (-18.0, 38.5), 1.4)
    mb.add_arc_pts("primary", (-18.0, 38.5), (-24.5, 76.5), 2.2)
    # Inner lapel crease & triangular turnback
    mb.add_arc_pts("primary", (-1.0, 19.5), (1.5, 31.5), 0.7)
    mb.add_arc_pts("primary", (1.5, 31.5), (-18.0, 38.5), -1.0)

    # Far-side (right) folded lapel seen in crisp profile on viewer's left
    mb.add_arc_pts("primary", (-14.5, 22.0), (-33.5, 31.0), 1.4)
    mb.add_arc_pts("primary", (-33.5, 31.0), (-24.5, 42.2), -1.2)
    mb.add_arc_pts("primary", (-24.5, 42.2), (-33.5, 78.5), 2.6)
    # Inner lapel fold line & double-breasted buttons nestled cleanly inside panel
    mb.add_arc_pts("detail", (-14.5, 22.0), (-22.5, 36.0), 1.0)
    mb.add_circle("detail", -22.2, 50.8, 1.75)
    mb.add_circle("detail", -25.2, 62.5, 1.75)

    # Tailored coat back, shoulder & sleeve grounded smoothly to MED_R
    mb.add_arc_pts("primary", (31.5, 13.8), (44.5, 74.5), 9.2)
    # Tailored sleeve seam & streamlined wool drapery folds
    mb.add_arc_pts("primary", (22.5, 20.5), (27.5, 81.5), 5.8)
    mb.add_arc_pts("detail", (33.5, 25.0), (38.0, 77.5), 4.6)
    mb.add_arc_pts("detail", (10.5, 32.0), (12.0, 83.5), 3.2)
    mb.add_arc_pts("detail", (-8.5, 44.0), (-11.5, 83.5), 1.6)
    # Subtle collar fold line
    mb.add_arc_pts("detail", (20.2, 2.2), (25.5, 14.5), 1.0)

    return mb.build()


def build_mascheroni_svg(theme: str = "dark", wave_angle_deg: float = 30.0) -> str:
    """Render the Lorenzo Mascheroni medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_mascheroni_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_mascheroni_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 30.0,
) -> tuple[Path, Path]:
    """Write ``mascheroni_dark.svg`` and ``mascheroni_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "mascheroni_dark.svg"
    light_path = target_dir / "mascheroni_light.svg"
    dark_path.write_text(
        build_mascheroni_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_mascheroni_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
