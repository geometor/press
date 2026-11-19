"""Study 03: Plato of Athens (School of Athens) in lines and circular arcs."""

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

__all__ = ["build_plato_elements", "build_plato_svg", "write_plato_svgs"]


def _clip_arc_to_medallion(
    cx: float,
    cy: float,
    r: float,
    a1: float,
    a2: float,
    steps: int = 24,
) -> list[tuple[float, float]]:
    """Return sub-spans of ``(a1, a2)`` that lie inside ``MED_R``."""
    a1_n, a2_n = normalize_short_span(a1, a2)
    spans: list[tuple[float, float]] = []
    in_span = False
    span_start = a1_n
    prev_a = a1_n
    for i in range(steps + 1):
        t = i / steps
        ang = a1_n + t * (a2_n - a1_n)
        px, py = polar(cx, cy, r, ang)
        inside = math.hypot(px - MED_CX, py - MED_CY) <= (MED_R - 0.15)
        if inside and not in_span:
            span_start = ang
            in_span = True
        elif not inside and in_span:
            spans.append((span_start, prev_a))
            in_span = False
        prev_a = ang
    if in_span:
        spans.append((span_start, a2_n))
    return [(s, e) for s, e in spans if abs(e - s) > 1.5]


def build_plato_elements(wave_angle_deg: float = 33.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Plato of Athens medallion strictly from lines, circles, and circular arcs.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc beard and hair locks.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``primary``, and ``detail`` primitive lists.
    """
    radius_head = 25.5
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    head_cx = 2.0
    eye_y = -27.0

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
        *,
        clip: bool = True,
    ) -> None:
        if clip:
            for sa, ea in _clip_arc_to_medallion(cx, cy, r, a1, a2):
                a1_n, a2_n = normalize_short_span(sa, ea)
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
        else:
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

    # -------------------------------------------------------------------------
    # Layer 1: Geometric Construction Scaffold
    # -------------------------------------------------------------------------
    add_circle(scaffold, MED_CX, MED_CY, MED_R)
    add_line(scaffold, 0.0, -102.0, 0.0, 86.0)
    add_line(scaffold, 10.5, -102.0, 10.5, 86.0)
    add_line(scaffold, -95.0, eye_y, 95.0, eye_y)
    add_line(scaffold, -95.0, 0.0, 95.0, 0.0)
    add_circle(scaffold, head_cx, eye_y, radius_head)
    add_circle(scaffold, head_cx, eye_y, radius_head * phi)
    add_circle(scaffold, head_cx, eye_y, radius_head * 2.0)
    add_circle(scaffold, 3.5, -26.5, 11.5)
    add_circle(scaffold, 17.5, -26.5, 11.5)
    add_circle(scaffold, 0.0, 12.0, 42.0)

    # -------------------------------------------------------------------------
    # Layer 4 (Golden Signature): Divided Line (Republic VI) & Dodecahedron
    # -------------------------------------------------------------------------
    # 1) The Divided Line (Republic VI, 509d-511e): AE divided at C in phi : 1,
    #    with AB : BC = phi : 1 (Intelligible) and CD : DE = phi : 1 (Visible).
    dl_x = -52.0
    dl_top = -76.0
    dl_bot = -22.0
    dl_len = dl_bot - dl_top  # 54.0
    ac_len = dl_len / phi
    y_c = dl_top + ac_len
    y_b = dl_top + ac_len / phi
    y_d = y_c + (dl_bot - y_c) / phi

    add_line(golden, dl_x, dl_top, dl_x, dl_bot)
    for y_tick, half_w in [
        (dl_top, 2.6),
        (y_b, 2.4),
        (y_c, 4.6),
        (y_d, 2.4),
        (dl_bot, 2.6),
    ]:
        add_line(golden, dl_x - half_w, y_tick, dl_x + half_w, y_tick)
    add_circle(golden, dl_x, y_c, 1.7)
    add_circle(golden, dl_x, dl_top, 1.0)
    add_circle(golden, dl_x, dl_bot, 1.0)

    # 2) Orthographic Dodecahedral Projection (Timaeus 55c) in upper right
    dod_cx, dod_cy = 55.0, -49.0
    r_out = 16.5
    # Exact 5-fold orthographic ratios of a regular dodecahedron:
    # outer decagon radius = R_out, mid-ring = R_out * cos(pi/5) / cos(0)?
    # Using exact golden ratios: r_inner = R_out / (phi^2), r_mid = R_out / phi
    r_inner = r_out / (phi * phi)
    r_mid = r_out / phi

    outer_pts = [polar(dod_cx, dod_cy, r_out, -90.0 + k * 36.0) for k in range(10)]
    mid_pts = [polar(dod_cx, dod_cy, r_mid, -90.0 + k * 72.0) for k in range(5)]
    inner_pts = [polar(dod_cx, dod_cy, r_inner, -90.0 + k * 72.0) for k in range(5)]

    add_circle(golden, dod_cx, dod_cy, r_out)
    for k in range(10):
        x1, y1 = outer_pts[k]
        x2, y2 = outer_pts[(k + 1) % 10]
        add_line(golden, x1, y1, x2, y2)
    for k in range(5):
        ix1, iy1 = inner_pts[k]
        ix2, iy2 = inner_pts[(k + 1) % 5]
        add_line(golden, ix1, iy1, ix2, iy2)
        mx, my = mid_pts[k]
        add_line(golden, ix1, iy1, mx, my)
        ox_prev, oy_prev = outer_pts[(2 * k - 1) % 10]
        ox_next, oy_next = outer_pts[(2 * k + 1) % 10]
        add_line(golden, mx, my, ox_prev, oy_prev)
        add_line(golden, mx, my, ox_next, oy_next)

    # -------------------------------------------------------------------------
    # Layer 2 & 3: Cranium, Face, Beard, Pointing Hand & Mantle Contours
    # -------------------------------------------------------------------------
    # Cranial dome & temple/cheek contour (three-quarter right profile)
    add_arc(primary, 1.5, -26.5, 25.5, -138.0, -18.0)
    add_arc(primary, 2.0, -25.0, 23.0, -22.0, 22.0)
    add_arc(primary, 10.0, -14.0, 14.5, -25.0, 32.0)
    # Left-side ear & cheek shadow contour
    add_arc(detail, -12.0, -22.0, 6.2, 120.0, 245.0)
    add_arc(detail, -13.5, -21.5, 3.4, 130.0, 240.0)

    # Furrowed brow lines (iconic Plato/Leonardo forehead)
    add_arc(detail, 8.0, -18.0, 20.0, -118.0, -68.0)
    add_arc(detail, 8.5, -14.5, 19.5, -115.0, -66.0)
    add_arc(detail, 9.0, -11.0, 19.0, -110.0, -64.0)

    # Brows & Eyes (3/4 right: right eye at x~3.5, left eye at x~17.5, y~-26.5)
    # Right eye (viewer's left)
    add_arc(primary, 3.5, -21.0, 10.5, -126.0, -62.0)
    add_arc(detail, 3.5, -20.2, 9.8, -122.0, -65.0)
    add_arc(primary, 3.5, -21.8, 6.4, -135.0, -48.0)
    add_arc(detail, 3.5, -31.8, 6.2, 52.0, 128.0)
    add_circle(detail, 3.5, -26.4, 2.2)
    add_circle(primary, 3.8, -26.4, 1.0, filled=True)

    # Left eye (viewer's right, slightly foreshortened)
    add_arc(primary, 17.0, -21.5, 9.6, -118.0, -56.0)
    add_arc(detail, 17.0, -20.7, 9.0, -114.0, -58.0)
    add_arc(primary, 17.5, -22.2, 5.8, -132.0, -48.0)
    add_arc(detail, 17.5, -31.2, 5.6, 52.0, 128.0)
    add_circle(detail, 17.8, -26.3, 2.0)
    add_circle(primary, 18.1, -26.3, 0.95, filled=True)

    # Nose bridge, tip & nostrils (3/4 right)
    add_line(primary, 10.6, -27.5, 14.8, -12.5)
    add_line(detail, 7.6, -25.0, 9.4, -12.5)
    add_arc(primary, 13.6, -12.2, 2.6, -15.0, 155.0)
    add_arc(primary, 10.2, -11.4, 2.0, 110.0, 245.0)
    add_arc(detail, 16.0, -12.0, 1.8, -40.0, 95.0)

    # Parted moustache & solemn mouth
    add_arc(primary, 3.5, -1.5, 10.2, -150.0, -58.0)
    add_arc(detail, 4.5, 0.5, 10.5, -148.0, -62.0)
    add_arc(primary, 17.5, -2.0, 8.2, -120.0, -28.0)
    add_arc(detail, 16.8, -0.2, 8.4, -118.0, -32.0)
    add_arc(primary, 12.4, 2.5, 7.2, -114.0, -66.0)
    add_arc(detail, 12.4, 4.2, 7.0, -110.0, -70.0)

    # -------------------------------------------------------------------------
    # Flowing Hair Locks & Philosopher Beard (Euclid III.12 tangent circular arcs)
    # -------------------------------------------------------------------------
    # Back hair cascade (viewer's left)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(
        -19.5, -40.0, -37.0, 14.0, 6, wave_angle_deg, 1
    ):
        add_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(
        -16.0, -34.0, -29.0, 18.0, 6, wave_angle_deg + 2.0, -1
    ):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(
        -22.5, -30.0, -42.0, 10.0, 5, wave_angle_deg, -1
    ):
        add_arc(detail, cx, cy, r, a1, a2)

    # Right temple lock
    for cx, cy, r, a1, a2 in tangent_wave_arcs(
        23.5, -34.0, 29.0, -6.0, 4, wave_angle_deg - 2.0, 1
    ):
        add_arc(primary, cx, cy, r, a1, a2)

    # Flowing white beard cascades (ending cleanly above collar strap)
    beard_strands = [
        (-15.5, -4.0, -24.5, 25.0, 5, wave_angle_deg, -1, primary),
        (-10.5, -3.0, -17.5, 29.0, 5, wave_angle_deg + 1.5, 1, detail),
        (-5.5, -2.0, -10.5, 32.5, 5, wave_angle_deg + 1.0, -1, detail),
        (3.5, -1.0, 1.5, 34.5, 6, wave_angle_deg, -1, primary),
        (11.0, -2.5, 10.5, 32.5, 5, wave_angle_deg + 1.0, 1, detail),
        (16.0, -4.0, 15.5, 28.0, 4, wave_angle_deg + 1.0, -1, detail),
        (20.5, -5.5, 21.0, 22.0, 4, wave_angle_deg - 1.0, 1, primary),
    ]
    for x1, y1, x2, y2, n_waves, w_deg, init_s, layer in beard_strands:
        for cx, cy, r, a1, a2 in tangent_wave_arcs(x1, y1, x2, y2, n_waves, w_deg, init_s):
            add_arc(layer, cx, cy, r, a1, a2)

    # Beard tip closure arcs
    add_arc(detail, -8.5, 25.5, 8.5, 48.0, 132.0)
    add_arc(primary, 3.0, 27.5, 8.5, 40.0, 140.0)

    # -------------------------------------------------------------------------
    # Raised Pointing Hand (Left side, pointing upward)
    # -------------------------------------------------------------------------
    # Index finger pointing up
    add_line(primary, -79.2, -37.0, -80.8, -21.0)
    add_line(primary, -77.6, -37.0, -76.2, -21.5)
    add_arc(primary, -78.4, -37.0, 0.8, 180.0, 360.0)
    # Curled fingers & thumb
    add_arc(primary, -74.2, -18.5, 2.3, -75.0, 115.0)
    add_arc(primary, -71.4, -15.5, 2.1, -65.0, 120.0)
    add_arc(detail, -73.8, -13.0, 2.3, 20.0, 180.0)
    add_arc(primary, -69.5, -19.2, 4.0, -100.0, 45.0)
    # Forearm & wrist descending cleanly into sleeve cuff
    add_line(primary, -80.8, -21.0, -83.5, 16.0)
    add_line(primary, -69.0, -15.2, -66.5, 16.0)
    add_arc(detail, -75.0, -9.0, 4.4, 10.0, 150.0)
    add_arc(primary, -75.0, 12.0, 9.5, 25.0, 155.0)

    # Right sleeve & tunic shoulder (viewer's left)
    add_arc(primary, -45.0, 48.0, 38.0, -142.0, -94.0)
    add_arc(primary, -42.0, 38.0, 26.0, -128.0, -78.0)
    add_arc(detail, -58.0, 45.0, 22.0, -135.0, -60.0)
    add_arc(primary, -34.0, 56.0, 34.0, 155.0, 198.0)
    add_arc(detail, -56.0, 52.0, 18.0, 95.0, 165.0)

    # -------------------------------------------------------------------------
    # Dark Collar Strap with Knot & Rose/Violet Mantle Drapery
    # -------------------------------------------------------------------------
    # Sweeping collar strap across chest (tucking behind rose mantle at x~20)
    add_arc(primary, -4.0, -16.0, 59.0, 62.0, 134.0)
    add_arc(primary, -4.0, -15.5, 53.5, 60.0, 133.0)
    add_arc(detail, -4.0, -15.8, 56.2, 62.0, 132.0)
    # Central knot & vertical hanging ribbon ends
    add_circle(primary, -4.2, 43.2, 2.6)
    add_line(primary, -5.8, 45.5, -7.2, 62.5)
    add_line(primary, -3.2, 45.8, -3.2, 63.0)
    add_arc(primary, -5.2, 62.5, 2.0, 5.0, 175.0)
    add_line(detail, -1.6, 45.0, -0.6, 60.0)
    add_line(detail, 0.2, 44.6, 1.4, 59.0)

    # Tunic vertical folds on chest (detail)
    add_arc(detail, 14.0, 48.0, 44.0, 135.0, 192.0)
    add_arc(detail, 26.0, 52.0, 44.0, 142.0, 196.0)
    add_arc(detail, -40.0, 58.0, 28.0, -25.0, 38.0)

    # Rose/violet mantle over left shoulder (viewer's right)
    add_arc(primary, 32.0, 68.0, 63.0, -102.0, -32.0)
    add_arc(primary, 74.0, 48.0, 57.0, 142.0, 206.0)
    add_arc(primary, 82.0, 50.0, 53.0, 138.0, 202.0)
    add_arc(detail, 88.0, 52.0, 48.0, 135.0, 198.0)
    add_arc(detail, 94.0, 55.0, 44.0, 142.0, 195.0)
    add_arc(primary, 42.0, 54.0, 36.0, -32.0, 14.0)
    add_arc(detail, 44.0, 64.0, 34.0, -35.0, 16.0)

    return {
        "scaffold": scaffold,
        "golden": golden,
        "primary": primary,
        "detail": detail,
    }


def build_plato_svg(theme: str = "dark", wave_angle_deg: float = 33.0) -> str:
    """Render the Plato of Athens portrait medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_plato_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_plato_svgs(
    output_dir: Path | None = None,
    wave_angle_deg: float = 33.0,
) -> tuple[Path, Path]:
    """Write ``plato_dark.svg`` and ``plato_light.svg`` to ``docsrc/_static/portraits``."""
    target_dir = output_dir or (
        Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"
    )
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "plato_dark.svg"
    light_path = target_dir / "plato_light.svg"
    dark_path.write_text(build_plato_svg("dark", wave_angle_deg=wave_angle_deg), encoding="utf-8")
    light_path.write_text(build_plato_svg("light", wave_angle_deg=wave_angle_deg), encoding="utf-8")
    return dark_path, light_path
