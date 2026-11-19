"""Study 06: Johannes Kepler (c. 1620) in lines and circular arcs."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import (
    MED_CX,
    MED_CY,
    MED_R,
    arc_path,
    clip_line_to_medallion,
    normalize_short_span,
    polar,
    render_medallion_svg,
    tangent_wave_arcs,
)

__all__ = ["build_kepler_elements", "build_kepler_svg", "write_kepler_svgs"]

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def build_kepler_elements(wave_angle_deg: float = 36.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Johannes Kepler (c. 1620) medallion strictly from lines, circles, and circular arcs.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc lace ruff & beard curls.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``primary``, and ``detail`` primitive lists.
    """
    radius_head = 26.0
    phi = (1.0 + math.sqrt(5.0)) / 2.0

    scaffold: list[dict[str, Any]] = []
    primary: list[dict[str, Any]] = []
    detail: list[dict[str, Any]] = []
    golden: list[dict[str, Any]] = []

    def add_circle(
        layer: list[dict[str, Any]],
        cx: float,
        cy: float,
        r: float,
        *,
        filled: bool = False,
    ) -> None:
        layer.append({"kind": "circle", "cx": cx, "cy": cy, "r": r, "filled": filled})

    def add_line(
        layer: list[dict[str, Any]],
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        clip: bool = True,
    ) -> None:
        if clip:
            clipped = clip_line_to_medallion(x1, y1, x2, y2)
            if clipped is None:
                return
            x1, y1, x2, y2 = clipped
        layer.append({"kind": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2})

    def add_arc(
        layer: list[dict[str, Any]],
        cx: float,
        cy: float,
        r: float,
        a1: float,
        a2: float,
    ) -> None:
        a1_n, a2_n = normalize_short_span(a1, a2)
        layer.append(
            {
                "kind": "arc",
                "d": arc_path(cx, cy, r, a1_n, a2_n),
                "cx": cx,
                "cy": cy,
                "r": r,
                "a1": a1_n,
                "a2": a2_n,
            }
        )

    # =========================================================================
    # Layer 1: Geometric Construction Scaffold
    # =========================================================================
    add_circle(scaffold, MED_CX, MED_CY, MED_R)
    add_line(scaffold, 0.0, -110.0, 0.0, 95.0)
    add_line(scaffold, -100.0, -27.0, 100.0, -27.0)
    add_line(scaffold, -100.0, 0.0, 100.0, 0.0)
    add_circle(scaffold, 0.0, -27.0, radius_head)
    add_circle(scaffold, 0.0, -27.0, radius_head * phi)
    add_circle(scaffold, 0.0, -27.0, radius_head * 2.0)
    add_circle(scaffold, -10.5, -24.8, radius_head / 2.0)
    add_circle(scaffold, 9.5, -26.2, radius_head / 2.0)
    add_circle(scaffold, 0.0, 2.0, 44.0)

    # =========================================================================
    # Layer 4 (Gold Signature): Kepler Right Triangle (1 : sqrt(phi) : phi)
    #                           & Nested Platonic Orbits
    # =========================================================================
    # 1) Kepler Right Triangle in upper-right field (1 : sqrt(phi) : phi)
    kx, ky = 47.0, -34.0
    unit = 19.0
    leg_b = unit * math.sqrt(phi)
    hyp_c = unit * phi
    add_line(golden, kx, ky, kx + unit, ky)
    add_line(golden, kx, ky, kx, ky - leg_b)
    add_line(golden, kx + unit, ky, kx, ky - leg_b)
    # Right-angle square marker
    sq = 3.2
    add_line(golden, kx + sq, ky, kx + sq, ky - sq)
    add_line(golden, kx, ky - sq, kx + sq, ky - sq)
    # Thales semicircle on hypotenuse (passes through right-angle vertex by Thales's theorem)
    hx, hy = kx + 0.5 * unit, ky - 0.5 * leg_b
    hyp_ang = math.degrees(math.atan2(-leg_b, unit))
    add_arc(golden, hx, hy, 0.5 * hyp_c, hyp_ang, hyp_ang - 90.0)
    add_arc(golden, hx, hy, 0.5 * hyp_c, hyp_ang - 90.0, hyp_ang - 180.0)

    # 2) Nested Platonic Orbits in lower-left field (Circle -> Triangle -> Circle -> Square -> Circle)
    ox, oy = -52.0, 44.0
    r0 = 14.5
    add_circle(golden, ox, oy, r0)
    tri_pts = [polar(ox, oy, r0, -90.0 + 120.0 * i) for i in range(3)]
    for i in range(3):
        p1, p2 = tri_pts[i], tri_pts[(i + 1) % 3]
        add_line(golden, p1[0], p1[1], p2[0], p2[1])
    r1 = r0 * 0.5
    add_circle(golden, ox, oy, r1)
    sq_pts = [polar(ox, oy, r1, 45.0 + 90.0 * i) for i in range(4)]
    for i in range(4):
        p1, p2 = sq_pts[i], sq_pts[(i + 1) % 4]
        add_line(golden, p1[0], p1[1], p2[0], p2[1])
    r2 = r1 / math.sqrt(2.0)
    add_circle(golden, ox, oy, r2)

    # =========================================================================
    # Layer 2 & 3: Cranial, Facial, Hair, Beard & Lace Ruff Contours
    # =========================================================================
    # --- Eyes & Eyebrows (three-quarter right pose) ---
    # Left eye (viewer's left, closer)
    add_arc(primary, -10.5, -18.5, 8.2, -128.0, -52.0)
    add_arc(detail, -10.5, -17.3, 8.0, -122.0, -58.0)
    add_arc(detail, -10.5, -31.2, 8.2, 54.0, 126.0)
    add_circle(detail, -10.5, -24.8, 2.75)
    add_circle(primary, -10.5, -24.8, 1.15, filled=True)
    add_arc(primary, -11.0, -19.5, 13.8, -126.0, -54.0)
    add_arc(detail, -11.0, -18.4, 13.2, -120.0, -60.0)

    # Right eye (viewer's right, slightly narrower)
    add_arc(primary, 9.5, -20.0, 7.8, -126.0, -54.0)
    add_arc(detail, 9.5, -18.8, 7.6, -120.0, -60.0)
    add_arc(detail, 9.5, -32.2, 7.6, 56.0, 124.0)
    add_circle(detail, 9.5, -26.2, 2.55)
    add_circle(primary, 9.5, -26.2, 1.10, filled=True)
    add_arc(primary, 10.2, -20.8, 13.2, -124.0, -54.0)
    add_arc(detail, 10.2, -19.7, 12.6, -118.0, -60.0)

    # --- Nose (slightly turned right in three-quarter view) ---
    add_line(detail, -2.5, -26.5, -2.8, -12.5)
    add_line(primary, 1.5, -27.0, 4.2, -11.2)
    add_arc(primary, 2.2, -12.2, 3.2, 20.0, 145.0)
    add_arc(primary, -3.2, -10.8, 2.1, 45.0, 210.0)
    add_arc(primary, 6.2, -11.8, 1.9, -20.0, 135.0)

    # --- Mustache & Mouth ---
    # Sweeping handlebar mustache
    add_arc(primary, -5.5, -0.5, 9.2, -135.0, -45.0)
    add_arc(primary, -13.2, -4.2, 8.2, 60.0, 148.0)
    add_arc(primary, 7.0, -1.0, 8.5, -135.0, -45.0)
    add_arc(primary, 12.5, -3.8, 6.8, 45.0, 130.0)
    add_arc(detail, -5.5, 1.2, 8.2, -130.0, -55.0)
    add_arc(detail, 7.0, 0.8, 7.5, -125.0, -50.0)
    # Lower lip & soul patch beneath mustache
    add_line(primary, -1.8, 0.8, 5.2, 0.5)
    add_arc(detail, 1.7, -1.0, 4.0, 55.0, 125.0)
    add_line(detail, 1.7, 3.0, 1.7, 6.5)

    # --- Beard (broad tapered goatee with Euclid III.12 bottom wave) ---
    add_line(primary, -14.8, 4.5, -12.8, 29.0)
    add_line(primary, 17.2, 2.2, 16.0, 27.0)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-12.8, 29.0, 16.0, 27.0, 5, 34.0, 1):
        add_arc(primary, cx, cy, r, a1, a2)
    # Interior beard grain lines
    add_line(detail, -8.5, 6.5, -7.8, 27.5)
    add_line(detail, -2.5, 7.0, -2.2, 28.0)
    add_line(detail, 3.5, 6.8, 3.8, 27.8)
    add_line(detail, 9.8, 5.2, 9.5, 26.8)

    # --- Face Contour (Forehead, Cheek, Jaw, Ear) ---
    # Viewer's right (far cheek & jaw)
    add_arc(primary, 12.0, -39.0, 11.5, -55.0, 15.0)
    add_arc(primary, 13.5, -24.0, 9.5, -35.0, 35.0)
    add_line(primary, 21.8, -19.0, 17.5, -1.5)
    # Viewer's left (temple, cheekbone, jaw)
    add_line(primary, -31.8, -46.5, -33.8, -26.5)
    add_arc(primary, -18.0, -14.0, 16.5, 130.0, 195.0)
    add_line(primary, -29.0, -3.5, -19.5, 5.5)

    # Ear (viewer's left, prominent)
    add_arc(primary, -38.5, -18.5, 8.2, 115.0, 245.0)
    add_arc(primary, -37.2, -13.5, 4.5, 60.0, 175.0)
    add_arc(detail, -38.2, -18.2, 5.2, 125.0, 240.0)
    add_arc(detail, -36.8, -16.8, 2.6, 100.0, 230.0)

    # --- Hairline & Crown ---
    # Hairline with central widow's peak
    add_arc(primary, -14.0, -44.0, 16.0, -145.0, -65.0)
    add_arc(primary, -5.0, -46.0, 9.0, -105.0, -40.0)
    add_arc(primary, 8.0, -45.5, 10.5, -135.0, -55.0)
    # Outer hair silhouette (connected crown)
    add_arc(primary, -6.5, -42.5, 25.5, -148.0, -45.0)
    add_arc(primary, -25.5, -42.0, 15.5, 152.0, 238.0)
    add_arc(primary, 10.5, -44.5, 16.5, -72.0, 18.0)
    add_line(primary, 26.2, -39.5, 22.8, -32.0)
    # Interior hair wave detail
    add_arc(detail, -6.5, -44.5, 21.5, -142.0, -55.0)
    add_arc(detail, -27.5, -40.5, 11.5, 160.0, 235.0)

    # --- Iconic Lace Ruff Collar ---
    # Left collar wing: top edge, outer curved rim, lower straight fold
    lc_cx, lc_cy, lc_r, lc_a1, lc_a2 = -32.0, -8.5, 24.5, 152.0, 206.0
    lx1, ly1 = polar(lc_cx, lc_cy, lc_r, lc_a2)
    lx2, ly2 = polar(lc_cx, lc_cy, lc_r, lc_a1)
    add_line(primary, lx1, ly1, -35.5, -11.0)
    add_arc(primary, lc_cx, lc_cy, lc_r, lc_a1, lc_a2)
    add_line(primary, lx2, ly2, -13.5, 22.0)
    # Left collar radial pleat lines (detail)
    add_line(detail, -47.0, -14.0, -34.0, -6.5)
    add_line(detail, -51.5, -6.5, -30.5, 1.5)
    add_line(detail, -51.5, 0.5, -24.5, 11.5)

    # Right collar wing: top edge, outer curved rim, lower straight fold
    rc_cx, rc_cy, rc_r, rc_a1, rc_a2 = 18.5, -5.5, 20.5, -32.0, 32.0
    rx1, ry1 = polar(rc_cx, rc_cy, rc_r, rc_a1)
    rx2, ry2 = polar(rc_cx, rc_cy, rc_r, rc_a2)
    add_line(primary, 22.0, -13.0, rx1, ry1)
    add_arc(primary, rc_cx, rc_cy, rc_r, rc_a1, rc_a2)
    add_line(primary, rx2, ry2, 16.8, 16.8)
    # Right collar radial pleat lines (detail)
    add_line(detail, 34.0, -10.5, 22.0, -4.5)
    add_line(detail, 36.5, -2.5, 20.0, 4.5)

    # Euclid III.12 Lace Scallops along Left & Right Ruff Perimeters
    for cx, cy, r, a1, a2 in tangent_wave_arcs(lx1 - 3.5, ly1, lx2 - 3.5, ly2, 6, wave_angle_deg, -1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(lx2 - 0.8, ly2 + 1.4, -14.0, 23.4, 9, wave_angle_deg, 1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(rx1 + 3.5, ry1, rx2 + 3.5, ry2, 5, wave_angle_deg, 1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(rx2 + 0.8, ry2 + 1.2, 17.5, 18.0, 5, wave_angle_deg, 1):
        add_arc(detail, cx, cy, r, a1, a2)

    # --- Shoulders & Doublet ---
    add_line(primary, -41.5, 16.0, -90.0, 46.0)
    add_line(primary, 32.5, 11.5, 86.0, 42.0)
    add_line(detail, 1.5, 29.0, 2.5, 84.0)
    # Subtle shoulder lapel folds
    add_line(detail, -28.0, 21.0, -42.0, 76.0)
    add_line(detail, 26.0, 16.0, 38.0, 76.0)

    return {
        "scaffold": scaffold,
        "golden": golden,
        "primary": primary,
        "detail": detail,
    }


def build_kepler_svg(theme: str = "dark", wave_angle_deg: float = 36.0) -> str:
    """Build the complete Johannes Kepler medallion SVG string for ``theme`` ('dark' or 'light')."""
    layers = build_kepler_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_kepler_svgs(output_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``kepler_dark.svg`` and ``kepler_light.svg`` to ``output_dir``."""
    target = output_dir or DEFAULT_OUTPUT_DIR
    target.mkdir(parents=True, exist_ok=True)
    dark_path = target / "kepler_dark.svg"
    light_path = target / "kepler_light.svg"
    dark_path.write_text(build_kepler_svg("dark"), encoding="utf-8")
    light_path.write_text(build_kepler_svg("light"), encoding="utf-8")
    return dark_path, light_path
