"""Study 04: Aristotle of Stagira (School of Athens) in lines and circular arcs."""

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
    inside_medallion,
    normalize_short_span,
    polar,
    render_medallion_svg,
    tangent_wave_arcs,
)

__all__ = [
    "build_aristotle_elements",
    "build_aristotle_svg",
    "write_aristotle_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"


def build_aristotle_elements(wave_angle_deg: float = 36.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Aristotle of Stagira medallion strictly from lines, circles, and circular arcs.

    Calibrated to Raphael's *School of Athens* (right figure, three-quarter left profile).

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc beard & hair curls.

    Returns:
        Dictionary of ``scaffold``, ``golden``, ``primary``, and ``detail`` primitive lists.
    """
    radius_head = 26.0
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    sqrt3 = math.sqrt(3.0)

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
        clip: bool = True,
    ) -> None:
        a1_n, a2_n = normalize_short_span(a1, a2)
        if clip:
            # Sample arc to ensure all points remain inside MED_R
            steps = 16
            kept: list[float] = []
            for i in range(steps + 1):
                ang = a1_n + (a2_n - a1_n) * (i / steps)
                px, py = polar(cx, cy, r, ang)
                if inside_medallion(px, py, margin=0.0):
                    kept.append(ang)
            if len(kept) < 2:
                return
            a1_n, a2_n = kept[0], kept[-1]
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
    add_line(scaffold, 0.0, -110.0, 0.0, 95.0)
    add_line(scaffold, -100.0, -27.0, 100.0, -27.0)
    add_line(scaffold, -100.0, 0.0, 100.0, 0.0)
    add_circle(scaffold, 0.0, -27.0, radius_head)
    add_circle(scaffold, 0.0, -27.0, radius_head * phi)
    add_circle(scaffold, 0.0, -27.0, radius_head * 2.0)
    # Three-quarter left eye construction circles
    add_circle(scaffold, -16.5, -27.0, radius_head / 2.0)
    add_circle(scaffold, -4.5, -27.0, radius_head / 2.0)

    # -------------------------------------------------------------------------
    # Layer 4 (Gold Signature): Continuum Axis & Geometric Syllogism Triangle
    # -------------------------------------------------------------------------
    tri_apex_y = -82.0
    tri_base_y = 46.0
    tri_half_w = (tri_base_y - tri_apex_y) / sqrt3  # ~73.90 (inside MED_R=92 at y=46)
    add_line(golden, 0.0, tri_apex_y, -tri_half_w, tri_base_y, clip=False)
    add_line(golden, 0.0, tri_apex_y, tri_half_w, tri_base_y, clip=False)
    add_line(golden, -tri_half_w, tri_base_y, tri_half_w, tri_base_y, clip=False)

    # Continuum Axis extending horizontally across the medallion at y = 46.0
    add_line(golden, -95.0, tri_base_y, 95.0, tri_base_y, clip=True)
    # Syllogism vertex nodes (Major, Minor, Middle) & golden-section divisions
    add_circle(golden, 0.0, tri_apex_y, 2.0)
    add_circle(golden, -tri_half_w, tri_base_y, 2.0)
    add_circle(golden, tri_half_w, tri_base_y, 2.0)
    for tick_x in (-radius_head * phi, -radius_head, 0.0, radius_head, radius_head * phi):
        add_line(golden, tick_x, tri_base_y - 2.2, tick_x, tri_base_y + 2.2, clip=True)

    # -------------------------------------------------------------------------
    # Layer 2 & 3: Cranial, Facial Profile, Eyes, Nose & Mouth (3/4 Left)
    # -------------------------------------------------------------------------
    # Forehead & brow ridge (left profile)
    add_arc(primary, -4.0, -36.0, 17.5, -172.0, -135.0)
    add_line(primary, -21.2, -37.5, -21.8, -31.0)
    add_arc(primary, -18.5, -29.0, 3.6, 155.0, 215.0)

    # Classical straight Greek nose
    add_line(primary, -20.0, -27.2, -24.2, -14.8)
    add_arc(primary, -21.5, -14.8, 2.7, 90.0, 185.0)
    add_line(primary, -21.5, -12.1, -17.8, -12.4)
    add_arc(detail, -16.8, -14.2, 2.1, -20.0, 110.0)

    # Cheekbone & temple (right side of face, viewer's right)
    add_arc(primary, 3.5, -24.0, 12.8, -32.0, 38.0)
    add_line(detail, -14.0, -21.0, -10.5, -14.5)

    # Right ear (partially framed by curls)
    add_arc(primary, 13.5, -22.5, 5.2, -70.0, 85.0)
    add_arc(detail, 13.8, -22.5, 2.8, -60.0, 75.0)

    # Left eye (further eye, viewer's left)
    add_arc(primary, -16.5, -24.2, 7.0, -128.0, -52.0)  # brow
    add_arc(primary, -16.5, -22.2, 5.8, -126.0, -54.0)  # upper lid
    add_arc(detail, -16.5, -30.5, 5.2, 52.0, 128.0)     # lower lid
    add_circle(detail, -16.6, -27.0, 2.1)               # iris
    add_circle(primary, -16.6, -27.0, 1.05, filled=True)  # pupil

    # Right eye (nearer eye, viewer's right)
    add_arc(primary, -4.2, -23.6, 8.4, -132.0, -48.0)   # brow
    add_arc(detail, -4.2, -23.0, 7.8, -125.0, -55.0)    # upper lid fold
    add_arc(primary, -4.2, -21.5, 6.8, -128.0, -52.0)   # upper lash
    add_arc(detail, -4.2, -31.8, 6.2, 50.0, 130.0)      # lower lid
    add_circle(detail, -4.5, -26.8, 2.3)                # iris
    add_circle(primary, -4.5, -26.8, 1.15, filled=True)  # pupil

    # Mustache & lips
    add_arc(primary, -20.8, -5.5, 7.0, -130.0, -55.0)
    add_arc(primary, -11.5, -4.0, 8.8, -125.0, -45.0)
    add_line(primary, -19.2, -8.8, -12.5, -8.5)
    add_arc(detail, -15.8, -10.2, 3.6, 48.0, 132.0)

    # -------------------------------------------------------------------------
    # Curly Hair (Euclid III.12 Tangent Circular Arcs)
    # -------------------------------------------------------------------------
    # Crown curls
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-26.0, -47.0, -4.0, -59.0, 5, wave_angle_deg, 1):
        add_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-4.0, -59.0, 26.0, -50.0, 6, wave_angle_deg, -1):
        add_arc(primary, cx, cy, r, a1, a2)

    # Left temple & brow-framing curls
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-22.5, -47.5, -9.0, -44.0, 4, wave_angle_deg - 2.0, -1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-26.0, -45.0, -23.5, -31.0, 3, wave_angle_deg, 1):
        add_arc(detail, cx, cy, r, a1, a2)

    # Back-of-head curls (viewer's right, framing ear to nape)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(26.0, -50.0, 35.0, -12.0, 6, wave_angle_deg + 2.0, 1):
        add_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(35.0, -12.0, 21.0, 2.0, 4, wave_angle_deg, -1):
        add_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(20.0, -45.0, 28.0, -10.0, 5, wave_angle_deg, -1):
        add_arc(detail, cx, cy, r, a1, a2)

    # -------------------------------------------------------------------------
    # Curly Philosopher Beard (Euclid III.12 Tangent Circular Arcs)
    # -------------------------------------------------------------------------
    # Outer beard contour: left cheek -> chin -> right jaw
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-23.0, -8.5, -16.0, 12.5, 4, wave_angle_deg + 2.0, 1):
        add_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-16.0, 12.5, 13.5, 4.0, 6, wave_angle_deg + 2.0, 1):
        add_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(13.5, 4.0, 14.0, -13.0, 4, wave_angle_deg, -1):
        add_arc(primary, cx, cy, r, a1, a2)

    # Interior beard curl layers
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-19.5, -4.0, 10.5, -2.5, 6, wave_angle_deg, -1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-18.0, 3.5, 9.5, 2.0, 5, wave_angle_deg, 1):
        add_arc(detail, cx, cy, r, a1, a2)

    # -------------------------------------------------------------------------
    # Neck, Tunic & Draped Blue/Gold Cloak (Strictly Clipped Inside MED_R=92)
    # -------------------------------------------------------------------------
    # Neck & nape
    add_line(primary, -10.5, 11.5, -8.5, 19.0)
    add_arc(primary, 10.0, 10.0, 14.5, -38.0, 22.0)

    # Left shoulder & cloak outer sweep (clipped inside MED_R=92)
    add_arc(primary, -18.0, 58.0, 47.0, -135.0, -98.0)
    add_arc(primary, -10.0, 82.0, 68.0, -165.0, -132.0)

    # Right shoulder & cloak outer sweep (single clean sweep clipped inside MED_R=92)
    add_arc(primary, 10.0, 76.0, 70.0, -76.0, -10.0)

    # Iconic gold-trimmed U-fold across chest
    add_arc(primary, -10.0, 34.0, 26.0, -145.0, -210.0)
    add_arc(primary, 6.0, 12.0, 38.0, 25.0, 138.0)
    add_arc(detail, 6.0, 12.0, 34.8, 28.0, 135.0)

    # Tunic V-neck opening
    add_line(primary, 13.0, 18.0, 32.0, 36.5)
    add_line(primary, 32.0, 36.5, 42.0, 24.5)
    add_line(detail, 14.0, 15.0, 31.5, 32.5)

    # Sweeping chest & shoulder drapery folds (bounded inside shoulders)
    add_arc(detail, -8.0, -22.0, 52.0, 32.0, 96.0)
    add_arc(detail, -4.0, -14.0, 62.0, 26.0, 88.0)
    add_arc(primary, -2.0, 115.0, 62.0, -118.0, -60.0)

    # Euclid III.12 tangent drapery folds on right cloak & lower-left bust
    for cx, cy, r, a1, a2 in tangent_wave_arcs(38.0, 34.0, 70.0, 64.0, 5, 28.0, 1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-58.0, 44.0, -34.0, 70.0, 4, 28.0, -1):
        add_arc(detail, cx, cy, r, a1, a2)

    return {
        "scaffold": scaffold,
        "golden": golden,
        "primary": primary,
        "detail": detail,
    }


def build_aristotle_svg(theme: str = "dark", wave_angle_deg: float = 36.0) -> str:
    """Render the Aristotle medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_aristotle_elements(wave_angle_deg=wave_angle_deg)
    return render_medallion_svg(layers, theme=theme)


def write_aristotle_svgs(
    out_dir: Path | None = None,
    wave_angle_deg: float = 36.0,
) -> tuple[Path, Path]:
    """Write ``aristotle_dark.svg`` and ``aristotle_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "aristotle_dark.svg"
    light_path = target_dir / "aristotle_light.svg"
    dark_path.write_text(build_aristotle_svg(theme="dark", wave_angle_deg=wave_angle_deg), encoding="utf-8")
    light_path.write_text(build_aristotle_svg(theme="light", wave_angle_deg=wave_angle_deg), encoding="utf-8")
    return dark_path, light_path
