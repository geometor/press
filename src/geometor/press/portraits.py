"""Compass-and-straightedge vector portrait medallion engine for :mod:`geometor.press`."""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any

DEFAULT_PORTRAITS_JSON = Path(__file__).resolve().parents[3] / "resources" / "portraits.json"

MED_CX: float = 0.0
MED_CY: float = -8.0
MED_R: float = 92.0
RIM_R: float = 95.2

MEDALLION_SPEC: dict[str, Any] = {
    "viewBox": "-102 -106 204 196",
    "medallion_center": (MED_CX, MED_CY),
    "medallion_radius": MED_R,
    "outer_rim_radius": RIM_R,
    "canonical_eye_line_y": -27.0,
    "canonical_head_radius": 26.0,
}

_FORBIDDEN_PATH_COMMANDS = ("C", "Q", "S", "T", "c", "q", "s", "t")


@dataclass(frozen=True)
class PortraitRecord:
    """Metadata and public-domain reference specification for one person portrait."""

    id: str
    name: str
    dates: str
    era: str
    repo: str
    status: str
    queue_order: int
    pose: str
    signature_motif: str
    reference: dict[str, Any]
    outputs: dict[str, str]
    notes: str = ""


def load_portraits(json_path: Path | None = None) -> list[PortraitRecord]:
    """Load the portrait catalog and Next-5 queue from ``resources/portraits.json``."""
    target = json_path or DEFAULT_PORTRAITS_JSON
    payload = json.loads(target.read_text(encoding="utf-8"))
    return [
        PortraitRecord(
            id=str(item["id"]),
            name=str(item["name"]),
            dates=str(item["dates"]),
            era=str(item["era"]),
            repo=str(item["repo"]),
            status=str(item["status"]),
            queue_order=int(item["queue_order"]),
            pose=str(item["pose"]),
            signature_motif=str(item["signature_motif"]),
            reference=dict(item.get("reference", {})),
            outputs=dict(item.get("outputs", {})),
            notes=str(item.get("notes", "")),
        )
        for item in payload.get("portraits", [])
    ]


def polar(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    """Return ``(x, y)`` on circle ``(cx, cy, r)`` at angle ``deg`` (0=right, 90=down)."""
    rad = math.radians(deg)
    return (cx + r * math.cos(rad), cy + r * math.sin(rad))


def inside_medallion(x: float, y: float, margin: float = 0.2) -> bool:
    """Return ``True`` if ``(x, y)`` lies within the canonical medallion circle."""
    return math.hypot(x - MED_CX, y - MED_CY) <= (MED_R + margin)


def clip_line_to_medallion(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> tuple[float, float, float, float] | None:
    """Clip straight segment ``(x1, y1)-(x2, y2)`` to exact intersection with medallion."""
    dx, dy = x2 - x1, y2 - y1
    fx, fy = x1 - MED_CX, y1 - MED_CY
    a = dx * dx + dy * dy
    if a < 1e-12:
        return None
    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - MED_R * MED_R
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        return None
    s = math.sqrt(disc)
    t_lo = max(0.0, (-b - s) / (2.0 * a))
    t_hi = min(1.0, (-b + s) / (2.0 * a))
    if t_lo >= t_hi:
        return None
    return (x1 + t_lo * dx, y1 + t_lo * dy, x1 + t_hi * dx, y1 + t_hi * dy)


def normalize_short_span(a1: float, a2: float) -> tuple[float, float]:
    """Normalize ``(a1, a2)`` so ``abs(a2 - a1) <= 180`` (preserving short circular arc)."""
    diff = (a2 - a1 + 180.0) % 360.0 - 180.0
    return a1, a1 + diff


def arc_path(cx: float, cy: float, r: float, deg1: float, deg2: float) -> str:
    """Return exact SVG circular arc path (``M ... A ...`` only — zero Beziers)."""
    x1, y1 = polar(cx, cy, r, deg1)
    x2, y2 = polar(cx, cy, r, deg2)
    delta = deg2 - deg1
    sweep = 1 if delta >= 0.0 else 0
    large = 1 if abs(delta) > 180.0 else 0
    return f"M {x1:.2f} {y1:.2f} A {r:.2f} {r:.2f} 0 {large} {sweep} {x2:.2f} {y2:.2f}"


def tangent_wave_arcs(
    x_start: float,
    y_start: float,
    x_end: float,
    y_end: float,
    half_waves: int,
    half_angle_deg: float,
    initial_sign: int = 1,
) -> list[tuple[float, float, float, float, float]]:
    """Construct a G1-smooth chain of externally tangent circular arcs (Euclid III.12)."""
    dx = x_end - x_start
    dy = y_end - y_start
    total_len = math.hypot(dx, dy)
    chord = total_len / half_waves
    ux, uy = dx / total_len, dy / total_len
    nx, ny = -uy, ux
    alpha = math.radians(half_angle_deg)
    radius = chord / (2.0 * math.sin(alpha))
    offset = radius * math.cos(alpha)

    arcs: list[tuple[float, float, float, float, float]] = []
    for k in range(half_waves):
        p1x = x_start + k * chord * ux
        p1y = y_start + k * chord * uy
        p2x = x_start + (k + 1) * chord * ux
        p2y = y_start + (k + 1) * chord * uy
        mx, my = 0.5 * (p1x + p2x), 0.5 * (p1y + p2y)
        sign = initial_sign if (k % 2 == 0) else -initial_sign
        cx = mx + sign * offset * nx
        cy = my + sign * offset * ny
        raw_a1 = math.degrees(math.atan2(p1y - cy, p1x - cx))
        raw_a2 = math.degrees(math.atan2(p2y - cy, p2x - cx))
        a1, a2 = normalize_short_span(raw_a1, raw_a2)
        mid_x, mid_y = polar(cx, cy, radius, 0.5 * (a1 + a2))
        if (
            inside_medallion(p1x, p1y, 1.0)
            and inside_medallion(p2x, p2y, 1.0)
            and inside_medallion(mid_x, mid_y, 1.0)
        ):
            arcs.append((cx, cy, radius, a1, a2))
    return arcs


def render_medallion_svg(layers: dict[str, list[dict[str, Any]]], theme: str = "dark") -> str:
    """Render a 4-layer portrait medallion SVG and assert zero Bezier commands."""
    if theme == "dark":
        bg, fg, det, scaf, gold = "#0d1017", "#eef2f7", "#8e9db2", "#46566c", "#d4af37"
    elif theme == "light":
        bg, fg, det, scaf, gold = "#f8f5ee", "#181c24", "#556173", "#9da8b8", "#b07f10"
    else:
        msg = f"Unsupported portrait theme {theme!r}; expected 'dark' or 'light'"
        raise ValueError(msg)

    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-102 -106 204 196" '
        'width="680" height="653" class="euclid-graphic">',
        f'  <rect x="-102" y="-106" width="204" height="196" fill="{bg}"/>',
    ]

    def emit(items: list[dict[str, Any]], stroke: str, width: float, opacity: float, cls: str) -> None:
        out.append(
            f'  <g class="{cls}" stroke="{stroke}" stroke-width="{width}" '
            f'stroke-linecap="round" fill="none" opacity="{opacity}">'
        )
        for el in items:
            kind = el["kind"]
            if kind == "circle":
                fill = stroke if el.get("filled") else "none"
                out.append(
                    f'    <circle cx="{el["cx"]:.2f}" cy="{el["cy"]:.2f}" '
                    f'r="{el["r"]:.2f}" fill="{fill}"/>'
                )
            elif kind == "line":
                out.append(
                    f'    <line x1="{el["x1"]:.2f}" y1="{el["y1"]:.2f}" '
                    f'x2="{el["x2"]:.2f}" y2="{el["y2"]:.2f}"/>'
                )
            elif kind == "arc":
                d = str(el["d"])
                for forbidden in _FORBIDDEN_PATH_COMMANDS:
                    if forbidden in d:
                        msg = f"Forbidden Bezier command {forbidden!r} in arc path: {d}"
                        raise ValueError(msg)
                out.append(f'    <path d="{d}"/>')
            else:
                msg = f"Unsupported portrait primitive kind: {kind!r}"
                raise ValueError(msg)
        out.append("  </g>")

    emit(layers.get("scaffold", []), scaf, 0.44, 0.45, "layer-scaffold")
    emit(layers.get("golden", []), gold, 0.85, 0.92, "layer-golden")
    emit(layers.get("detail", []), det, 0.62, 0.84, "layer-detail")
    emit(layers.get("primary", []), fg, 1.15, 1.0, "layer-primary")
    out.append(
        f'  <circle cx="{MED_CX}" cy="{MED_CY}" r="{RIM_R}" stroke="{gold}" '
        'stroke-width="0.65" fill="none" opacity="0.65" class="layer-rim"/>'
    )
    out.append("</svg>")
    return "\n".join(out)
