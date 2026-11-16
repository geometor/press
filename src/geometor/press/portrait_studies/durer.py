"""Study 01: Albrecht Durer (1500 Self-Portrait) in lines and circular arcs."""

from __future__ import annotations

import math
from typing import Any

from ..portraits import (
    MED_CX,
    MED_CY,
    MED_R,
    arc_path,
    clip_line_to_medallion,
    normalize_short_span,
    tangent_wave_arcs,
)

__all__ = ["build_durer_elements"]


def build_durer_elements(wave_angle_deg: float = 34.0) -> dict[str, list[dict[str, Any]]]:
    """Construct Albrecht Durer (1500) medallion strictly from lines, circles, and circular arcs.

    Args:
        wave_angle_deg: Half-angle (degrees) for Euclid III.12 tangent-arc hair curls.

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

    def mirror_line(layer: list[dict[str, Any]], x1: float, y1: float, x2: float, y2: float) -> None:
        add_line(layer, x1, y1, x2, y2)
        add_line(layer, -x1, y1, -x2, y2)

    def mirror_arc(
        layer: list[dict[str, Any]], cx: float, cy: float, r: float, a1: float, a2: float
    ) -> None:
        add_arc(layer, cx, cy, r, a1, a2)
        add_arc(layer, -cx, cy, r, 180.0 - a1, 180.0 - a2)

    def mirror_circle(
        layer: list[dict[str, Any]],
        cx: float,
        cy: float,
        r: float,
        *,
        filled: bool = False,
    ) -> None:
        add_circle(layer, cx, cy, r, filled=filled)
        if abs(cx) > 1e-6:
            add_circle(layer, -cx, cy, r, filled=filled)

    # Layer 1: Geometric Construction Scaffold
    add_circle(scaffold, MED_CX, MED_CY, MED_R)
    add_line(scaffold, 0.0, -110.0, 0.0, 95.0)
    add_line(scaffold, -100.0, -27.0, 100.0, -27.0)
    add_line(scaffold, -100.0, 0.0, 100.0, 0.0)
    add_circle(scaffold, 0.0, -27.0, radius_head)
    add_circle(scaffold, 0.0, -27.0, radius_head * phi)
    add_circle(scaffold, 0.0, -27.0, radius_head * 2.0)
    mirror_circle(scaffold, -13.0, -27.0, radius_head / 2.0)
    add_circle(scaffold, 0.0, 0.0, 28.5)

    # Layer 4 (Gold Signature): 60-degree Equilateral Cascade Triangle & 1500 AD Monogram
    tri_apex_y = -84.0
    tri_base_y = -27.0 + math.sqrt(27.0**2 + 4536.0)
    tri_half_w = (tri_base_y - tri_apex_y) / sqrt3
    add_line(golden, 0.0, tri_apex_y, -tri_half_w, tri_base_y, clip=False)
    add_line(golden, 0.0, tri_apex_y, tri_half_w, tri_base_y, clip=False)
    add_line(golden, -tri_half_w, tri_base_y, tri_half_w, tri_base_y, clip=False)

    mx, my = -71.5, -22.5
    add_line(golden, mx - 5.0, my - 5.2, mx + 5.0, my - 5.2)
    add_line(golden, mx - 3.4, my - 5.2, mx - 5.5, my + 5.3)
    add_line(golden, mx + 3.4, my - 5.2, mx + 5.5, my + 5.3)
    add_line(golden, mx - 4.1, my - 1.1, mx + 4.1, my - 1.1)
    add_line(golden, mx - 1.7, my + 0.3, mx - 1.7, my + 5.1)
    add_line(golden, mx - 1.7, my + 0.3, mx + 0.3, my + 0.3)
    add_line(golden, mx - 1.7, my + 5.1, mx + 0.3, my + 5.1)
    add_arc(golden, mx + 0.3, my + 2.7, 2.4, -89.0, 89.0)
    add_line(golden, mx - 4.5, my - 8.8, mx - 4.5, my - 6.9)
    add_line(golden, mx - 2.2, my - 8.8, mx - 1.0, my - 8.8)
    add_arc(golden, mx - 1.7, my - 7.6, 0.75, -90.0, 85.0)
    add_circle(golden, mx + 1.3, my - 7.85, 0.9)
    add_circle(golden, mx + 4.2, my - 7.85, 0.9)

    # Layer 2 & 3: Connected Facial, Hair & Robe Contours
    mirror_arc(primary, -10.5, -34.0, 21.8, -60.0, -152.0)
    add_arc(detail, 2.8, -51.2, 3.6, 145.0, 240.0)
    add_arc(detail, -2.5, -52.0, 3.2, -55.0, 35.0)

    mirror_arc(primary, -3.5, -27.5, 22.0, -138.0, -195.0)
    mirror_line(primary, -24.4, -21.8, -21.2, 6.0)
    mirror_arc(primary, -5.0, 5.5, 16.2, 178.0, 118.0)
    mirror_arc(primary, -6.2, 16.5, 12.6, 120.0, 60.0)

    mirror_arc(primary, -14.5, -19.5, 13.8, -126.0, -50.0)
    mirror_arc(detail, -14.5, -18.3, 13.2, -120.0, -58.0)

    mirror_arc(detail, -13.2, -21.2, 8.6, -134.0, -46.0)
    mirror_arc(primary, -13.2, -20.2, 8.0, -138.0, -42.0)
    mirror_arc(detail, -13.2, -31.4, 7.4, 54.0, 126.0)
    mirror_circle(detail, -13.0, -26.2, 2.75)
    mirror_circle(primary, -13.0, -26.3, 1.15, filled=True)

    add_line(primary, -4.3, -28.5, -3.4, -6.5)
    add_line(detail, 3.9, -27.5, 3.1, -6.5)
    add_arc(primary, 0.0, -4.8, 3.6, 28.0, 152.0)
    mirror_arc(primary, -4.5, -3.1, 2.35, 35.0, 205.0)

    mirror_arc(primary, -6.5, 16.2, 14.8, -74.0, -165.0)
    mirror_arc(detail, -7.0, 16.5, 12.4, -76.0, -158.0)
    mirror_arc(primary, -2.8, 7.6, 3.4, -128.0, -35.0)
    mirror_line(primary, -5.2, 5.6, -9.5, 6.8)
    mirror_line(detail, -0.5, 6.4, -9.5, 6.8)
    add_arc(primary, 0.0, 2.6, 8.2, 46.0, 134.0)

    add_arc(detail, 0.0, 17.2, 5.0, -135.0, -45.0)
    add_line(detail, 0.0, 15.2, 0.0, 27.2)
    mirror_line(detail, -4.2, 16.8, -5.2, 28.0)
    mirror_line(detail, -8.5, 16.2, -10.2, 26.8)

    mirror_arc(primary, -10.5, -42.5, 26.2, -66.0, -171.0)
    add_arc(detail, 2.0, -67.2, 4.2, 160.0, 255.0)

    for cx, cy, r, a1, a2 in tangent_wave_arcs(
        -29.2, -46.5, -73.0, 46.0, 7, wave_angle_deg, 1
    ):
        mirror_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(
        -24.8, -35.0, -35.0, 44.0, 7, wave_angle_deg + 1.0, -1
    ):
        mirror_arc(primary, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(
        -27.0, -41.5, -53.0, 47.5, 7, wave_angle_deg + 3.0, 1
    ):
        mirror_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(
        -28.0, -39.0, -63.0, 47.0, 6, wave_angle_deg + 1.0, -1
    ):
        mirror_arc(detail, cx, cy, r, a1, a2)

    for cx, cy, r, a1, a2 in [
        (-39.0, 46.5, 5.5, 12.0, 172.0),
        (-51.0, 48.5, 6.2, 8.0, 172.0),
        (-64.0, 47.5, 6.8, 5.0, 168.0),
    ]:
        mirror_arc(detail, cx, cy, r, a1, a2)

    mirror_line(detail, -12.5, 28.0, -14.0, 49.5)
    add_line(primary, -7.2, 56.5, 1.8, 56.5)
    add_line(detail, -6.4, 58.8, 1.0, 58.8)

    add_line(primary, -18.5, 35.0, -2.5, 67.5)
    add_line(primary, 18.5, 33.5, -9.8, 83.5)
    add_line(primary, -35.5, 52.0, -20.0, 82.0)
    add_line(primary, 36.5, 49.5, 19.5, 82.0)

    for cx, cy, r, a1, a2 in tangent_wave_arcs(35.0, 51.0, 19.8, 81.0, 5, 32.0, 1):
        add_arc(detail, cx, cy, r, a1, a2)
    for cx, cy, r, a1, a2 in tangent_wave_arcs(-34.2, 53.0, -19.8, 81.0, 5, 32.0, -1):
        add_arc(detail, cx, cy, r, a1, a2)

    add_arc(primary, -42.0, 104.0, 56.0, -118.5, -91.0)
    add_arc(primary, 42.0, 104.0, 56.0, -89.0, -61.5)

    return {
        "scaffold": scaffold,
        "golden": golden,
        "primary": primary,
        "detail": detail,
    }
