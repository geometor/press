"""Study 37: Mario Livio (after the NASA/STScI portrait)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MedallionBuilder, render_medallion_svg

__all__ = [
    "build_livio_elements",
    "build_livio_svg",
    "write_livio_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _add_pentagram_phi_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw the Regular Inscribed Pentagram & Golden Ratio ``phi`` Division in left margin.

    Constructs a circumcircle enclosing an exact regular pentagon and its
    ``{5/2}`` pentagram star, highlighting the nested inverted inner pentagon
    and the golden-ratio chord section ``a : b = phi`` along the diagonals.
    """
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    r_out = 12.2
    r_in = r_out / (phi * phi)

    # Circumcircle and inner circle framing the nested pentagon
    mb.add_circle("golden", cx, cy, r_out)
    mb.add_circle("golden", cx, cy, r_in * math.cos(math.radians(36.0)))

    outer: list[tuple[float, float]] = []
    inner: list[tuple[float, float]] = []
    for k in range(5):
        ang_o = math.radians(-90.0 + 72.0 * k)
        ang_i = math.radians(-54.0 + 72.0 * k)
        outer.append((cx + r_out * math.cos(ang_o), cy + r_out * math.sin(ang_o)))
        inner.append((cx + r_in * math.cos(ang_i), cy + r_in * math.sin(ang_i)))

    # Outer regular pentagon & exact {5/2} pentagram star diagonals
    for k in range(5):
        p1, p2 = outer[k], outer[(k + 1) % 5]
        d1, d2 = outer[k], outer[(k + 2) % 5]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
        mb.add_line("golden", d1[0], d1[1], d2[0], d2[1])
        mb.add_circle("golden", p1[0], p1[1], 0.56, filled=True)

    # Highlight the 5 golden-section chord intersection vertices of the inner pentagon
    for ix, iy in inner:
        mb.add_circle("golden", ix, iy, 0.62, filled=True)
    mb.add_circle("golden", cx, cy, 0.52, filled=True)


def _add_golden_triangle_spiral_motif(
    mb: MedallionBuilder,
    cx: float,
    cy: float,
) -> None:
    """Draw the Golden Triangle (72-36-72) Penrose Subdivision & Golden Spiral in right margin.

    Recursively decomposes an exact ``72°-36°-72°`` Golden Triangle into
    alternating smaller Golden Triangles and obtuse Golden Gnomons (the Penrose
    kite-and-dart building blocks), then threads exact ``G1``-tangent ``108°``
    circular spiral arcs through the golden vertices.
    """
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    base = 13.8
    leg = phi * base
    height = math.sqrt(leg * leg - (0.5 * base) ** 2)

    pt_a = (cx + 1.2, cy - 0.52 * height)
    pt_b = (cx + 1.2 - 0.5 * base, cy + 0.48 * height)
    pt_c = (cx + 1.2 + 0.5 * base, cy + 0.48 * height)

    def _golden_subdivide(
        p_apex: tuple[float, float],
        p_right: tuple[float, float],
    ) -> tuple[float, float]:
        t = 1.0 / phi
        return (
            p_apex[0] + t * (p_right[0] - p_apex[0]),
            p_apex[1] + t * (p_right[1] - p_apex[1]),
        )

    # Recursive exact golden triangle & golden gnomon subdivision vertices
    pt_d = _golden_subdivide(pt_a, pt_c)
    pt_e = _golden_subdivide(pt_b, pt_d)
    pt_f = _golden_subdivide(pt_c, pt_e)
    pt_g = _golden_subdivide(pt_d, pt_f)
    pt_h = _golden_subdivide(pt_e, pt_g)

    # Outer Golden Triangle ABC & internal Penrose subdivision chords
    mb.add_line("golden", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_a[0], pt_a[1])
    mb.add_line("golden", pt_b[0], pt_b[1], pt_d[0], pt_d[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_e[0], pt_e[1])
    mb.add_line("golden", pt_d[0], pt_d[1], pt_f[0], pt_f[1])
    mb.add_line("golden", pt_e[0], pt_e[1], pt_g[0], pt_g[1])

    # Exact G1-smooth 108-degree circular golden spiral arcs (A -> B -> C -> D -> E -> F)
    arc_steps = (
        (pt_d, pt_a, pt_b),
        (pt_e, pt_b, pt_c),
        (pt_f, pt_c, pt_d),
        (pt_g, pt_d, pt_e),
        (pt_h, pt_e, pt_f),
    )
    for center, p_start, p_end in arc_steps:
        rad = math.hypot(p_start[0] - center[0], p_start[1] - center[1])
        a1 = math.degrees(math.atan2(p_start[1] - center[1], p_start[0] - center[0]))
        a2 = math.degrees(math.atan2(p_end[1] - center[1], p_end[0] - center[0]))
        mb.add_arc("golden", center[0], center[1], rad, a1, a2)

    # Crisp golden nodes at primary vertices & spiral convergence eye
    for vx, vy in (pt_a, pt_b, pt_c, pt_d, pt_e):
        mb.add_circle("golden", vx, vy, 0.56, filled=True)
    mb.add_circle("golden", pt_h[0], pt_h[1], 0.62)


def build_livio_elements(wave_angle_deg: float = 28.0) -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer geometric portrait of Mario Livio.

    Calibrated to the NASA/STScI portrait: clean-shaven approachable frontal-
    slightly-left gaze with bright friendly eyes locked on ``y = -27``, neatly
    side-swept graying hair above a clear rounded forehead, warm gentle smile
    with subtle nasolabial dimples and clean tapered jaw/chin, open-collar
    tailored button-down dress shirt with vertical placket and three small
    circular buttons, and natural broad shoulders extending smoothly to
    ``MED_R = 92.0``. Margin motifs display the Inscribed Pentagram ``phi``
    Chord Division (left) and the Golden Triangle Penrose Subdivision & Spiral
    (right).
    """
    mb = MedallionBuilder()
    mb.add_scaffold_base(
        eye_lx=-10.4,
        eye_rx=8.8,
        head_cx=0.0,
        head_cy=-27.0,
        head_r=26.0,
    )

    # --- GOLDEN RATIO MARGIN MOTIFS (open margins, zero face crossing) ---
    _add_pentagram_phi_motif(mb, cx=-63.5, cy=-26.0)
    _add_golden_triangle_spiral_motif(mb, cx=63.5, cy=-26.0)

    # --- NEATLY SIDE-SWEPT GRAYING HAIR & CLEAR ROUNDED FOREHEAD ---
    mb.add_arc_pts("primary", (-21.8, -28.0), (-25.0, -39.5), 1.4)
    mb.add_arc_pts("primary", (-25.0, -39.5), (-22.2, -50.8), 1.7)
    mb.add_arc_pts("primary", (-22.2, -50.8), (-12.5, -59.2), 2.0)
    mb.add_arc_pts("primary", (-12.5, -59.2), (7.5, -62.2), 2.4)
    mb.add_arc_pts("primary", (7.5, -62.2), (22.0, -57.8), 2.0)
    mb.add_arc_pts("primary", (22.0, -57.8), (26.2, -49.5), 1.4)
    mb.add_arc_pts("primary", (26.2, -49.5), (28.8, -38.8), 1.6)
    mb.add_arc_pts("primary", (28.8, -38.8), (26.8, -26.5), 1.2)
    mb.add_arc_pts("primary", (26.8, -26.5), (24.5, -18.0), 0.8)

    # Clear rounded forehead hairline
    mb.add_arc_pts("primary", (-20.2, -28.5), (-19.6, -40.2), 0.9)
    mb.add_arc_pts("primary", (-19.6, -40.2), (-14.2, -50.0), 1.3)
    mb.add_arc_pts("primary", (-14.2, -50.0), (-1.5, -54.2), 1.6)
    mb.add_arc_pts("primary", (-1.5, -54.2), (13.2, -50.8), 1.5)
    mb.add_arc_pts("primary", (13.2, -50.8), (21.2, -41.8), 1.3)
    mb.add_arc_pts("primary", (21.2, -41.8), (23.2, -29.5), 0.9)

    # Neatly combed side-swept graying hair texture strictly inside crown (zero crossings)
    mb.add_wave("detail", (-14.5, -55.8), (15.5, -58.8), 4, wave_angle_deg - 6.0, -1)
    mb.add_wave("detail", (4.0, -55.8), (22.0, -53.2), 3, wave_angle_deg - 4.0, 1)
    mb.add_wave("detail", (22.8, -46.5), (26.2, -31.0), 3, wave_angle_deg + 2.0, -1)
    mb.add_wave("detail", (-22.6, -34.0), (-20.8, -46.5), 3, wave_angle_deg + 2.0, 1)

    # --- CLEAN-SHAVEN APPROACHABLE FACE CONTOUR & RIGHT EAR ---
    mb.add_arc_pts("primary", (-20.2, -28.5), (-21.0, -19.5), -0.8)
    mb.add_arc_pts("primary", (-21.0, -19.5), (-19.2, -9.5), -1.0)
    mb.add_arc_pts("primary", (-19.2, -9.5), (-13.6, -0.5), -1.2)
    mb.add_arc_pts("primary", (-13.6, -0.5), (-4.5, 5.0), -1.3)
    mb.add_arc_pts("primary", (-4.5, 5.0), (4.5, 5.2), -1.4)
    mb.add_arc_pts("primary", (4.5, 5.2), (14.2, -0.5), -1.4)
    mb.add_arc_pts("primary", (14.2, -0.5), (21.2, -10.5), -1.2)
    mb.add_arc_pts("primary", (21.2, -10.5), (23.8, -21.5), -0.9)
    mb.add_arc_pts("primary", (23.8, -21.5), (23.2, -29.5), -0.6)

    # Right ear (viewer's right)
    mb.add_arc_pts("primary", (24.0, -29.2), (28.0, -27.2), 1.0)
    mb.add_arc_pts("primary", (28.0, -27.2), (26.6, -17.8), 1.1)
    mb.add_arc_pts("primary", (26.6, -17.8), (22.8, -15.2), 0.9)
    mb.add_arc_pts("detail", (24.6, -26.2), (25.4, -19.2), 0.8)

    # --- EXPRESSIVE SILVER BROWS & BRIGHT FRIENDLY EYES ON y = -27 ---
    mb.add_arc_pts("primary", (-17.6, -31.8), (-11.0, -33.2), 0.7)
    mb.add_arc_pts("primary", (-11.0, -33.2), (-4.2, -30.8), 0.55)
    mb.add_arc_pts("detail", (-16.6, -30.8), (-5.2, -30.0), 0.7)

    mb.add_arc_pts("primary", (1.6, -30.8), (9.0, -33.5), 0.75)
    mb.add_arc_pts("primary", (9.0, -33.5), (17.0, -31.2), 0.6)
    mb.add_arc_pts("detail", (2.6, -30.0), (16.0, -30.4), 0.75)

    mb.add_canonical_eye(
        -10.4,
        -26.8,
        width=9.5,
        upper_sag=1.80,
        lower_sag=-0.85,
        iris_r=1.92,
        pupil_r=1.02,
        gaze_dx=-0.15,
    )
    mb.add_canonical_eye(
        8.8,
        -26.8,
        width=9.8,
        upper_sag=1.80,
        lower_sag=-0.85,
        iris_r=1.95,
        pupil_r=1.04,
        gaze_dx=-0.20,
    )

    # Subtle warm smile dimples (clean, approachable facial plane)
    mb.add_arc_pts("detail", (-9.8, -12.5), (-12.5, -6.2), 0.5)
    mb.add_arc_pts("detail", (10.0, -12.2), (12.2, -6.0), -0.5)

    # --- NATURAL STRAIGHT NOSE & WARM GENTLE SMILE ---
    mb.add_arc_pts("primary", (-1.8, -29.8), (-3.2, -21.5), 0.25)
    mb.add_arc_pts("primary", (-3.2, -21.5), (-4.6, -15.8), 0.25)
    mb.add_arc_pts("primary", (-4.6, -15.8), (-3.6, -13.2), -0.45)
    mb.add_arc_pts("primary", (-3.6, -13.2), (0.8, -12.8), -0.35)
    mb.add_arc_pts("primary", (0.8, -12.8), (4.4, -14.2), -0.38)
    mb.add_arc_pts("primary", (4.4, -14.2), (4.7, -16.2), -0.48)
    mb.add_arc_pts("primary", (4.7, -16.2), (2.6, -16.8), -0.32)
    mb.add_arc_pts("detail", (-4.8, -15.6), (-6.2, -16.2), -0.32)

    # Gentle warm approachable smile & clean tapered chin
    mb.add_arc_pts("detail", (-7.2, -6.4), (-1.2, -6.2), 0.25)
    mb.add_arc_pts("detail", (-1.2, -6.2), (5.8, -6.1), 0.25)
    mb.add_arc_pts("primary", (-10.0, -5.8), (-1.2, -4.3), -0.6)
    mb.add_arc_pts("primary", (-1.2, -4.3), (8.8, -5.6), -0.6)
    mb.add_arc_pts("primary", (-6.0, -1.8), (-1.2, -1.2), -0.42)
    mb.add_arc_pts("primary", (-1.2, -1.2), (4.2, -1.8), -0.42)

    # --- OPEN-COLLAR BUTTON-DOWN DRESS SHIRT & NATURAL SHOULDERS TO MED_R ---
    # Neck & open-collar button-down shirt points
    mb.add_arc_pts("primary", (-10.2, 4.5), (-11.0, 13.8), 0.6)
    mb.add_arc_pts("primary", (-11.0, 13.8), (-13.8, 17.8), 0.5)
    mb.add_arc_pts("primary", (-13.8, 17.8), (-10.4, 27.8), -0.8)
    mb.add_arc_pts("primary", (-10.4, 27.8), (-3.2, 26.2), -0.6)
    mb.add_arc_pts("primary", (-8.8, 12.8), (-3.2, 26.2), -0.9)

    mb.add_arc_pts("primary", (20.2, -2.5), (26.2, 5.5), -0.8)
    mb.add_arc_pts("primary", (26.2, 5.5), (10.5, 29.2), 1.6)
    mb.add_arc_pts("primary", (10.5, 29.2), (3.2, 22.8), -0.7)
    mb.add_arc_pts("primary", (3.2, 22.8), (-3.2, 26.2), -0.4)
    mb.add_arc_pts("detail", (19.6, 3.8), (3.2, 22.8), -1.2)

    # Vertical button-down shirt placket flanking 3 small circular shirt buttons
    mb.add_arc_pts("primary", (-5.8, 26.8), (-12.8, 86.0), 1.6)
    mb.add_arc_pts("primary", (-0.2, 26.2), (-7.0, 86.0), 1.6)
    for bx, by in ((-2.8, 37.5), (-5.6, 58.2), (-8.2, 78.2)):
        mb.add_circle("primary", bx, by, 1.42)
        mb.add_circle("primary", bx, by, 0.56, filled=True)

    # Smooth single-sweep natural broad shoulders to MED_R = 92.0 (globe omitted)
    mb.add_arc_pts("primary", (-13.8, 17.8), (-72.0, 62.0), -11.5)
    mb.add_arc_pts("primary", (26.2, 5.5), (72.5, 58.0), 11.8)

    # Tailored dress-shirt sleeve folds & crisp breast pocket outline in detail
    mb.add_arc_pts("detail", (-36.5, 38.0), (-46.5, 80.0), -2.4)
    mb.add_arc_pts("detail", (-24.5, 52.0), (-28.5, 84.0), -1.4)
    mb.add_arc_pts("detail", (39.0, 24.0), (54.0, 76.0), 4.0)
    mb.add_arc_pts("detail", (22.0, 42.0), (34.5, 84.0), 2.8)
    # Shirt breast pocket on viewer's right
    mb.add_line("detail", 10.5, 58.5, 25.5, 58.5)
    mb.add_line("detail", 10.5, 58.5, 9.2, 76.5)
    mb.add_line("detail", 25.5, 58.5, 24.2, 76.5)
    mb.add_arc_pts("detail", (9.2, 76.5), (24.2, 76.5), -2.2)

    return mb.build()


def build_livio_svg(theme: str = "dark", wave_angle_deg: float = 28.0) -> str:
    """Render the Mario Livio medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_livio_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_livio_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 28.0,
) -> tuple[Path, Path]:
    """Write ``livio_dark.svg`` and ``livio_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "livio_dark.svg"
    light_path = target_dir / "livio_light.svg"
    dark_path.write_text(
        build_livio_svg(theme="dark", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    light_path.write_text(
        build_livio_svg(theme="light", wave_angle_deg=wave_angle_deg),
        encoding="utf-8",
    )
    return dark_path, light_path
