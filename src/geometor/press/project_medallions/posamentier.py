"""Author Medallion: Posamentier & Lehmann — The Glorious Golden Ratio.

Sacred geometric emblem celebrating Alfred S. Posamentier & Ingmar Lehmann's
*The Glorious Golden Ratio*, framed within the unified ``R = 68`` graduated
astrolabe seal:

1. **Regular Decagon (``{10/1}``) & Golden ``{10/3}`` Decagram**: Inscribed in
   circumcircle ``(O, R = 56)``, the decagon side ``s_10 = R / phi``, radius
   ``R``, and ``{10/3}`` star chord ``c_{10/3} = R * phi`` form the exact
   three-term golden progression ``phi^-1 : 1 : phi`` (verified to ``< 1e-12``).
2. **Nested Regular Pentagon on the Exact ``R / phi`` Star Ring**: The inner
   intersections of the ``{10/3}`` golden star polygon lie strictly on the
   concentric circle of radius ``R * cos(54 deg) / cos(18 deg) = R / phi = s_10``,
   inscribing a bold nested upright regular pentagon and inner pentagram.
3. **Ptolemy's Exact ``R : s_10 = phi`` Compass Construction**: Bisecting
   horizontal radius ``O-E`` at ``M = (R/2, 0)``, Ptolemy's golden compass arc
   of radius ``|M V_0| = (sqrt(5)/2) R`` swings from apex ``V_0`` directly onto
   point ``P = (-R/phi, 0)`` on the inner ``R / phi`` ring, paired with twin
   chord-transfer arcs proving ``|O P| = |V_0 V_1| = s_10``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_posamentier_elements",
    "build_posamentier_svg",
    "write_posamentier_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point = tuple[float, float]


def _add_astrolabe_seal(mb: MedallionBuilder, r_seal: float) -> None:
    """Add the unified GEOMETOR Emblem Pantheon scaffold and graduated astrolabe seal."""
    ox, oy = MED_CX, MED_CY
    r_bezel = r_seal + 4.8

    mb.add_circle("scaffold", ox, oy, MED_R, clip=False)
    for r in (78.0, 52.0, 26.0):
        mb.add_circle("scaffold", ox, oy, r)
    mb.add_line("scaffold", ox, oy - MED_R, ox, oy + MED_R)
    mb.add_line("scaffold", ox - MED_R, oy, ox + MED_R, oy)
    for deg in (45.0, 135.0, 225.0, 315.0):
        p_in = polar(ox, oy, 78.0, deg)
        p_out = polar(ox, oy, MED_R, deg)
        mb.add_line("scaffold", p_in[0], p_in[1], p_out[0], p_out[1])

    mb.add_circle("primary", ox, oy, r_seal)
    mb.add_circle("detail", ox, oy, r_bezel)

    for k in range(36):
        deg = float(k * 10)
        if k % 9 == 0:
            p1 = polar(ox, oy, r_seal, deg)
            p2 = polar(ox, oy, r_bezel + 3.2, deg)
            mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])
            tip = polar(ox, oy, r_bezel + 4.8, deg)
            mb.add_circle("golden", tip[0], tip[1], 1.15, filled=True)
        elif k % 3 == 0:
            p1 = polar(ox, oy, r_seal, deg)
            p2 = polar(ox, oy, r_bezel + 1.4, deg)
            mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])
        else:
            p1 = polar(ox, oy, r_seal + 1.1, deg)
            p2 = polar(ox, oy, r_bezel, deg)
            mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])


def _dist(p1: Point, p2: Point) -> float:
    """Return Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _angle_deg(cx: float, cy: float, pt: Point) -> float:
    """Return polar angle in degrees from ``(cx, cy)`` to ``pt``."""
    return math.degrees(math.atan2(pt[1] - cy, pt[0] - cx))


def build_posamentier_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Posamentier & Lehmann.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    sqrt5 = math.sqrt(5.0)
    phi = 0.5 * (1.0 + sqrt5)

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Regular Decagon ({10/1}), {10/3} Star, & Nested Pentagon
    # ------------------------------------------------------------------
    r_outer = 56.0
    dec_pts = [polar(ox, oy, r_outer, -90.0 + 36.0 * k) for k in range(10)]

    s10 = _dist(dec_pts[0], dec_pts[1])
    c10_3 = _dist(dec_pts[0], dec_pts[3])
    r_inner = r_outer / phi  # Exact inner {10/3} star intersection ring == s10!

    # Analytical verification of Ptolemy's golden progression s_10 : R : c_{10/3} = 1/phi : 1 : phi
    if abs((r_outer / s10) - phi) > 1e-12:
        msg = f"Ptolemy decagon golden ratio R/s_10 violated: {r_outer / s10:.15f}"
        raise ValueError(msg)
    if abs((c10_3 / r_outer) - phi) > 1e-12:
        msg = f"Decagram golden ratio c_(10/3)/R violated: {c10_3 / r_outer:.15f}"
        raise ValueError(msg)

    # Nested regular pentagon inscribed on the exact r_inner = R / phi ring
    pent_pts = [polar(ox, oy, r_inner, -90.0 + 72.0 * k) for k in range(5)]

    # ------------------------------------------------------------------
    # 2. Detail Geometry: Inner Rings, Pentagram, & Ptolemy Diameter
    # ------------------------------------------------------------------
    mb.add_circle("detail", ox, oy, r_inner)
    mb.add_circle("detail", ox, oy, r_inner / phi)  # Secondary phi^-2 heart ring

    # Horizontal Ptolemy diameter W -- O -- E and vertical radius O -- V_0
    pt_w: Point = (ox - r_outer, oy)
    pt_e: Point = (ox + r_outer, oy)
    pt_v0 = dec_pts[0]
    mb.add_line("detail", pt_w[0], pt_w[1], pt_e[0], pt_e[1])
    mb.add_line("detail", ox, oy, pt_v0[0], pt_v0[1])

    # Subtle inner pentagram chords inside the nested pentagon
    for k in range(5):
        p1, p2 = pent_pts[k], pent_pts[(k + 2) % 5]
        mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])

    # ------------------------------------------------------------------
    # 3. Bold Primary Circumcircle, Regular Decagon, & Nested Pentagon
    # ------------------------------------------------------------------
    mb.add_circle("primary", ox, oy, r_outer)
    for k in range(10):
        p1, p2 = dec_pts[k], dec_pts[(k + 1) % 10]
        mb.add_line("primary", p1[0], p1[1], p2[0], p2[1])

    for k in range(5):
        p1, p2 = pent_pts[k], pent_pts[(k + 1) % 5]
        mb.add_line("primary", p1[0], p1[1], p2[0], p2[1])

    # ------------------------------------------------------------------
    # 4. Luminous Golden {10/3} Star Polygon & Ptolemy Compass Transfer Arcs
    # ------------------------------------------------------------------
    for k in range(10):
        p1, p2 = dec_pts[k], dec_pts[(k + 3) % 10]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Ptolemy's Exact Compass Construction of s_10 = R / phi:
    # Midpoint M = (ox + R/2, oy); compass radius r_ptol = |M V_0| = (sqrt(5)/2) * R
    pt_m: Point = (ox + 0.5 * r_outer, oy)
    r_ptol = _dist(pt_m, pt_v0)
    pt_p: Point = (pt_m[0] - r_ptol, oy)  # Exact Ptolemy cut at (ox - R/phi, oy)

    # Verify |O P| == s_10 == R / phi to < 1e-12
    op_len = abs(pt_p[0] - ox)
    if abs(op_len - s10) > 1e-12:
        msg = f"Ptolemy construction |OP| == s_10 violated: {op_len:.15f} != {s10:.15f}"
        raise ValueError(msg)

    # Ptolemy's golden hypotenuse M -- V_0 and golden segment O -- P (= s_10)
    mb.add_line("golden", pt_m[0], pt_m[1], pt_v0[0], pt_v0[1])
    mb.add_line("golden", ox, oy, pt_p[0], pt_p[1])

    # Ptolemy's hero compass swing arc centered at M sweeping V_0 -> P
    ang_v0 = _angle_deg(pt_m[0], pt_m[1], pt_v0)
    ang_p = _angle_deg(pt_m[0], pt_m[1], pt_p)
    mb.add_arc("golden", pt_m[0], pt_m[1], r_ptol, ang_v0, ang_p)

    # Twin golden compass transfer arcs from V_0 with radius s_10 landing on V_1 and V_9
    a_v1 = _angle_deg(pt_v0[0], pt_v0[1], dec_pts[1])
    a_v9 = _angle_deg(pt_v0[0], pt_v0[1], dec_pts[9])
    mb.add_arc("golden", pt_v0[0], pt_v0[1], s10, a_v1 - 16.0, a_v1 + 26.0)
    mb.add_arc("golden", pt_v0[0], pt_v0[1], s10, a_v9 - 26.0, a_v9 + 16.0)

    # Golden decagon vertex jewels & nested pentagon jewels
    for idx, (vx, vy) in enumerate(dec_pts):
        if idx in (0, 1, 9):
            mb.add_circle("golden", vx, vy, 3.6)
            mb.add_circle("golden", vx, vy, 1.8, filled=True)
        else:
            mb.add_circle("golden", vx, vy, 2.2)
            mb.add_circle("golden", vx, vy, 1.05, filled=True)

    for px, py in pent_pts:
        mb.add_circle("golden", px, py, 2.3)
        mb.add_circle("golden", px, py, 1.15, filled=True)

    # Hero Ptolemy jewels at M (midpoint), P (golden cut), and O (center)
    for hx, hy in (pt_m, pt_p, (ox, oy)):
        mb.add_circle("golden", hx, hy, 3.4)
        mb.add_circle("golden", hx, hy, 1.65, filled=True)

    return mb.build()


def build_posamentier_svg(theme: str = "dark") -> str:
    """Render the Posamentier & Lehmann medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_posamentier_elements()
    return render_medallion_svg(layers, theme=theme)


def write_posamentier_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``posamentier_dark.svg`` and ``posamentier_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "posamentier_dark.svg"
    light_path = target_dir / "posamentier_light.svg"
    dark_path.write_text(build_posamentier_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_posamentier_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
