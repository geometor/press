"""Study 07: Leonhard Euler (1753 Handmann pastel) in lines and circular arcs."""

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
    render_medallion_svg,
    tangent_wave_arcs,
)

__all__ = ["build_euler_elements", "build_euler_svg", "write_euler_svgs"]

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def _triangle_euler_geometry(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
) -> dict[str, Any]:
    """Compute exact circumcenter O, centroid G, nine-point center N, orthocenter H, and R."""
    ax, ay = a
    bx, by = b
    cx, cy = c
    d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ox = (
        (ax * ax + ay * ay) * (by - cy)
        + (bx * bx + by * by) * (cy - ay)
        + (cx * cx + cy * cy) * (ay - by)
    ) / d
    oy = (
        (ax * ax + ay * ay) * (cx - bx)
        + (bx * bx + by * by) * (ax - cx)
        + (cx * cx + cy * cy) * (bx - ax)
    ) / d
    gx = (ax + bx + cx) / 3.0
    gy = (ay + by + cy) / 3.0
    hx = 3.0 * gx - 2.0 * ox
    hy = 3.0 * gy - 2.0 * oy
    nx = 0.5 * (ox + hx)
    ny = 0.5 * (oy + hy)
    r_circ = math.hypot(ax - ox, ay - oy)
    return {
        "O": (ox, oy),
        "G": (gx, gy),
        "N": (nx, ny),
        "H": (hx, hy),
        "R": r_circ,
        "R9": 0.5 * r_circ,
    }


def build_euler_elements(fold_angle_deg: float = 30.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Leonhard Euler (1753) medallion strictly from lines, circles, and circular arcs.

    Args:
        fold_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc silk cap folds.

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

    def arc_from_points(
        layer: list[dict[str, Any]],
        p1: tuple[float, float],
        p2: tuple[float, float],
        sagitta: float,
    ) -> None:
        """Construct exact circular arc through p1 and p2 with signed sagitta (+ = left of p1->p2)."""
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        chord = math.hypot(dx, dy)
        if chord < 1e-6 or abs(sagitta) < 1e-4:
            add_line(layer, x1, y1, x2, y2)
            return
        h = abs(sagitta)
        r = (chord * chord) / (8.0 * h) + h / 2.0
        mx, my = 0.5 * (x1 + x2), 0.5 * (y1 + y2)
        nx, ny = -dy / chord, dx / chord
        sign = 1.0 if sagitta > 0.0 else -1.0
        # Center lies opposite the bulge direction at distance (r - h)
        cx = mx - sign * (r - h) * nx
        cy = my - sign * (r - h) * ny
        a1 = math.degrees(math.atan2(y1 - cy, x1 - cx))
        a2 = math.degrees(math.atan2(y2 - cy, x2 - cx))
        add_arc(layer, cx, cy, r, a1, a2)

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    add_circle(scaffold, MED_CX, MED_CY, MED_R)
    add_line(scaffold, 0.0, -110.0, 0.0, 95.0)
    add_line(scaffold, -100.0, -27.0, 100.0, -27.0)
    add_line(scaffold, -100.0, 0.0, 100.0, 0.0)
    add_circle(scaffold, 0.0, -27.0, radius_head)
    add_circle(scaffold, -4.0, -27.0, radius_head)
    add_circle(scaffold, 0.0, -27.0, radius_head * phi)
    add_circle(scaffold, -4.5, -25.5, 11.5)
    add_circle(scaffold, -26.5, -27.0, 10.0)

    # -------------------------------------------------------------------------
    # Layer 4 (Gold Signature): The Euler Line (O - G - H) & Nine-Point Circle
    # -------------------------------------------------------------------------
    tri_a = (-32.0, -82.0)
    tri_b = (-74.0, 24.0)
    tri_c = (72.0, -16.0)
    eg = _triangle_euler_geometry(tri_a, tri_b, tri_c)
    ox, oy = eg["O"]
    gx, gy = eg["G"]
    nx, ny = eg["N"]
    hx, hy = eg["H"]

    # Circumcircle in scaffold
    add_circle(scaffold, ox, oy, eg["R"])

    # Triangle ABC
    add_line(golden, *tri_a, *tri_b)
    add_line(golden, *tri_b, *tri_c)
    add_line(golden, *tri_c, *tri_a)
    for vx, vy in (tri_a, tri_b, tri_c):
        add_circle(golden, vx, vy, 1.35)

    # Nine-Point Circle (center N, radius R/2)
    add_circle(golden, nx, ny, eg["R9"])

    # Side midpoints on the Nine-Point Circle
    for p1, p2 in ((tri_a, tri_b), (tri_b, tri_c), (tri_c, tri_a)):
        add_circle(golden, 0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1]), 1.05)

    # Euler Line O - G - N - H (extended 10 units beyond O and H)
    ux = hx - ox
    uy = hy - oy
    ulen = math.hypot(ux, uy)
    ux, uy = ux / ulen, uy / ulen
    add_line(golden, ox - 10.0 * ux, oy - 10.0 * uy, hx + 10.0 * ux, hy + 10.0 * uy)

    # Collinear Euler Line centers: O, G, N, H
    for px, py in (eg["O"], eg["G"], eg["H"]):
        add_circle(golden, px, py, 1.35, filled=True)
    add_circle(golden, nx, ny, 1.55)
    add_circle(golden, nx, ny, 0.65, filled=True)

    # -------------------------------------------------------------------------
    # Layer 2 & 3: Cranial, Facial, Ear & Expression Contours
    # -------------------------------------------------------------------------
    # Forehead & left face silhouette (viewer's left, 3/4 view)
    arc_from_points(primary, (-34.5, -36.5), (-35.5, -28.0), 0.8)
    arc_from_points(primary, (-35.5, -28.0), (-32.5, -21.5), -0.8)
    arc_from_points(primary, (-32.5, -21.5), (-30.5, -9.0), 1.0)
    arc_from_points(primary, (-30.5, -9.0), (-26.5, 2.5), 0.8)
    arc_from_points(primary, (-26.5, 2.5), (-22.0, 12.5), 1.2)
    arc_from_points(primary, (-22.0, 12.5), (-11.0, 19.8), 2.0)

    # Chin & right jawline (viewer's right) up to ear
    arc_from_points(primary, (-11.0, 19.8), (4.0, 20.5), 2.2)
    arc_from_points(primary, (4.0, 20.5), (21.0, 12.5), 2.5)
    arc_from_points(primary, (21.0, 12.5), (29.5, -3.0), 1.8)
    arc_from_points(detail, (-10.0, 24.5), (7.5, 23.0), 1.6)

    # Ear (viewer's right)
    arc_from_points(primary, (30.5, -21.5), (39.5, -18.5), -3.0)
    arc_from_points(primary, (39.5, -18.5), (37.0, -5.0), -2.4)
    arc_from_points(primary, (37.0, -5.0), (29.5, -3.0), -1.8)
    arc_from_points(detail, (32.5, -17.5), (35.0, -8.5), -1.8)
    arc_from_points(detail, (31.5, -12.5), (33.5, -7.5), 1.0)

    # His Left Eye (viewer's right, open & clear)
    arc_from_points(primary, (-12.0, -25.2), (3.0, -24.2), -2.6)
    arc_from_points(detail, (-13.0, -27.4), (4.0, -26.2), -2.4)
    arc_from_points(detail, (-11.5, -24.8), (2.5, -24.2), 1.6)
    add_circle(detail, -4.5, -25.5, 2.65)
    add_circle(primary, -4.5, -25.5, 1.15, filled=True)
    # Left eyebrow
    arc_from_points(primary, (-15.5, -32.2), (6.5, -30.5), -3.0)
    arc_from_points(detail, (-14.5, -33.6), (5.0, -32.2), -2.4)

    # His Right Eye (viewer's left, squinting / drooping)
    arc_from_points(primary, (-31.5, -27.5), (-21.8, -26.5), -1.3)
    arc_from_points(detail, (-32.0, -29.2), (-21.5, -28.2), -1.5)
    arc_from_points(detail, (-30.5, -26.2), (-22.2, -26.2), 0.8)
    add_circle(primary, -26.5, -27.0, 0.95, filled=True)
    # Right eyebrow
    arc_from_points(primary, (-34.2, -33.2), (-21.5, -33.5), -1.8)
    arc_from_points(detail, (-33.5, -34.6), (-22.2, -34.6), -1.5)

    # Glabella frown furrow
    add_line(detail, -18.2, -39.5, -19.2, -30.5)
    add_line(detail, -20.8, -37.0, -21.2, -31.5)

    # Nose bridge, tip & nostril wing
    arc_from_points(primary, (-21.2, -30.5), (-24.5, -13.0), -0.6)
    arc_from_points(primary, (-24.5, -13.0), (-21.0, -8.5), 2.0)
    arc_from_points(primary, (-21.0, -8.5), (-15.0, -9.0), 1.0)
    arc_from_points(detail, (-16.2, -12.0), (-14.5, -9.2), -1.2)

    # Nasolabial folds
    arc_from_points(detail, (-22.5, -7.0), (-27.0, 1.5), 1.0)
    arc_from_points(detail, (-13.5, -7.5), (-4.0, 5.5), -2.0)

    # Mouth & lips
    arc_from_points(primary, (-26.5, 2.5), (-17.5, 3.6), 0.5)
    arc_from_points(primary, (-17.5, 3.6), (-6.8, 1.8), 0.7)
    arc_from_points(detail, (-24.5, 1.2), (-10.0, 1.2), -0.9)
    arc_from_points(detail, (-22.0, 6.2), (-10.5, 6.0), 1.2)

    # -------------------------------------------------------------------------
    # Silk Cap / Turban (Euclid III.12 Concentric & Tangent Circular Arcs)
    # -------------------------------------------------------------------------
    # Forehead wrap bands (3 concentric arcs sweeping across the brow)
    arc_from_points(primary, (-35.0, -36.5), (27.5, -34.5), -21.0)
    arc_from_points(primary, (27.5, -34.5), (37.5, -22.5), -2.2)
    arc_from_points(detail, (-35.5, -42.5), (38.0, -27.5), -22.0)
    arc_from_points(primary, (-34.5, -49.5), (44.5, -24.5), -24.0)

    # Left blue-grey tufted fold
    arc_from_points(primary, (-35.5, -49.5), (-35.0, -64.5), -3.2)
    arc_from_points(primary, (-35.0, -64.5), (-25.5, -75.5), -2.6)
    arc_from_points(primary, (-25.5, -75.5), (-14.5, -67.5), -2.4)
    arc_from_points(detail, (-31.5, -68.0), (-21.0, -56.5), -2.0)

    # Upper crown & billowing right wing
    arc_from_points(primary, (-19.5, -70.5), (-4.0, -91.5), -4.2)
    arc_from_points(primary, (-4.0, -91.5), (14.5, -90.5), -3.5)
    arc_from_points(primary, (14.5, -90.5), (46.0, -78.5), -4.5)
    arc_from_points(primary, (46.0, -78.5), (72.5, -58.5), -3.8)
    arc_from_points(primary, (72.5, -58.5), (69.5, -48.5), -2.5)
    arc_from_points(primary, (69.5, -48.5), (49.5, -44.5), -2.5)

    # Euclid III.12 tangent wave folds along turban crown
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-26.0, -56.0, 48.0, -56.0, 4, fold_angle_deg, 1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-10.0, -78.0, 56.0, -62.0, 4, fold_angle_deg - 2.0, -1):
        add_arc(detail, cx, cy, r, a1, a2)
    arc_from_points(detail, (-8.0, -86.5), (26.0, -63.5), -5.0)
    arc_from_points(detail, (14.0, -84.0), (54.0, -55.0), -4.5)

    # Hanging silk tail behind ear
    arc_from_points(primary, (44.5, -24.5), (56.5, 4.5), -3.5)
    arc_from_points(primary, (56.5, 4.5), (42.5, 11.5), -2.0)
    arc_from_points(primary, (42.5, 11.5), (39.5, -3.5), -1.5)
    arc_from_points(detail, (46.0, -16.5), (49.0, 8.5), -2.0)

    # -------------------------------------------------------------------------
    # Neck, Collar, Ruffled Cravat & Striped Coat
    # -------------------------------------------------------------------------
    # Neck & white shirt collar
    add_line(primary, -23.0, 15.0, -23.5, 29.0)
    add_line(primary, 31.5, 10.5, 34.5, 24.5)
    arc_from_points(primary, (34.5, 24.5), (8.0, 34.0), -3.2)
    arc_from_points(primary, (-22.0, 25.0), (-2.0, 35.0), 2.5)
    arc_from_points(detail, (29.5, 18.0), (11.0, 29.5), -2.2)

    # Coat collar & lapels
    add_line(primary, -27.5, 26.5, -10.0, 40.5)
    add_line(primary, -10.0, 40.5, -2.0, 45.5)
    add_circle(primary, -4.5, 41.2, 3.6)
    add_circle(detail, -4.5, 41.2, 2.2)

    add_line(primary, 35.0, 23.0, 42.0, 38.0)
    add_line(primary, 42.0, 38.0, 28.0, 46.5)
    add_line(primary, 28.0, 46.5, 18.5, 62.5)
    add_line(primary, 18.5, 62.5, 5.0, 83.5)
    add_circle(primary, 11.5, 73.5, 4.2)
    add_circle(detail, 11.5, 73.5, 2.6)

    # Ruffled white cravat (Euclid III.12 tangent wave arcs)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(6.0, 32.5, 21.5, 62.0, 5, 36.0, 1):
        add_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-1.0, 36.0, 14.0, 65.5, 5, 34.0, -1):
        add_arc(detail, cx, cy, r, a1, a2)

    # Coat shoulders (clipped cleanly inside MED_R = 92)
    arc_from_points(primary, (-27.5, 26.5), (-76.0, 44.0), 5.5)
    arc_from_points(primary, (35.0, 23.0), (80.0, 40.0), -5.5)

    # Characteristic diagonal stripes on blue coat
    add_line(detail, -72.0, 46.0, -50.0, 82.0)
    add_line(detail, -61.0, 40.0, -37.0, 84.0)
    add_line(detail, -48.0, 34.0, -20.0, 86.0)
    add_line(detail, -36.0, 30.0, -7.0, 86.0)
    add_line(detail, -10.0, 40.5, 5.0, 83.5)

    add_line(detail, 42.0, 38.0, 39.0, 84.0)
    add_line(detail, 53.0, 34.0, 52.0, 80.0)
    add_line(detail, 64.0, 36.0, 68.0, 72.0)
    add_line(detail, 75.0, 42.0, 82.0, 58.0)

    return {
        "scaffold": scaffold,
        "golden": golden,
        "primary": primary,
        "detail": detail,
    }


def build_euler_svg(theme: str = "dark") -> str:
    """Render Leonhard Euler portrait medallion SVG for ``'dark'`` or ``'light'`` theme."""
    return render_medallion_svg(build_euler_elements(), theme=theme)


def write_euler_svgs(output_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``euler_dark.svg`` and ``euler_light.svg`` to ``docsrc/_static/portraits/``."""
    target_dir = output_dir or DEFAULT_OUTPUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "euler_dark.svg"
    light_path = target_dir / "euler_light.svg"
    dark_path.write_text(build_euler_svg("dark"), encoding="utf-8")
    light_path.write_text(build_euler_svg("light"), encoding="utf-8")
    return dark_path, light_path
