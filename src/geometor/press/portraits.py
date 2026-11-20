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


def render_medallion_coin_svg(
    layers: dict[str, list[dict[str, Any]]],
    theme: str = "adaptive",
) -> str:
    """Render a square transparent-exterior circular medallion coin SVG.

    Centers the canonical medallion ``(MED_CX=0, MED_CY=-8, RIM_R=95.2)`` inside a
    ``1:1`` ``viewBox="-100 -108 200 200"`` with transparent exterior corners so it
    displays cleanly as a site logo, hero emblem, or collection thumbnail.
    """
    if theme not in ("dark", "light", "adaptive"):
        msg = f"Unsupported coin theme {theme!r}; expected 'dark', 'light', or 'adaptive'"
        raise ValueError(msg)

    if theme == "adaptive":
        bg = "var(--med-bg, #0d1017)"
        fg = "var(--med-fg, #eef2f7)"
        det = "var(--med-det, #8e9db2)"
        scaf = "var(--med-scaf, #46566c)"
        gold = "var(--med-gold, #d4af37)"
        style_block = (
            "  <style>\n"
            "    .medallion-coin {\n"
            "      --med-bg: #0d1017;\n"
            "      --med-fg: #eef2f7;\n"
            "      --med-det: #8e9db2;\n"
            "      --med-scaf: #46566c;\n"
            "      --med-gold: #d4af37;\n"
            "    }\n"
            "    @media (prefers-color-scheme: light) {\n"
            "      .medallion-coin {\n"
            "        --med-bg: #f8f5ee;\n"
            "        --med-fg: #181c24;\n"
            "        --med-det: #556173;\n"
            "        --med-scaf: #9da8b8;\n"
            "        --med-gold: #b07f10;\n"
            "      }\n"
            "    }\n"
            "    body.light-mode .medallion-coin {\n"
            "      --med-bg: #f8f5ee;\n"
            "      --med-fg: #181c24;\n"
            "      --med-det: #556173;\n"
            "      --med-scaf: #9da8b8;\n"
            "      --med-gold: #b07f10;\n"
            "    }\n"
            "  </style>"
        )
    elif theme == "dark":
        bg, fg, det, scaf, gold = "#0d1017", "#eef2f7", "#8e9db2", "#46566c", "#d4af37"
        style_block = ""
    else:
        bg, fg, det, scaf, gold = "#f8f5ee", "#181c24", "#556173", "#9da8b8", "#b07f10"
        style_block = ""

    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-100 -108 200 200" '
        'width="512" height="512" class="euclid-graphic medallion-coin">',
    ]
    if style_block:
        out.append(style_block)
    out.append(
        f'  <circle cx="{MED_CX:.2f}" cy="{MED_CY:.2f}" r="{RIM_R:.2f}" '
        f'fill="{bg}" class="layer-disc"/>'
    )

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
        f'  <circle cx="{MED_CX:.2f}" cy="{MED_CY:.2f}" r="{RIM_R:.2f}" stroke="{gold}" '
        'stroke-width="1.05" fill="none" opacity="0.88" class="layer-rim"/>'
    )
    out.append("</svg>")
    return "\n".join(out)



def arc_through(
    p1: tuple[float, float],
    p2: tuple[float, float],
    sagitta: float,
) -> tuple[float, float, float, float, float]:
    """Compute circular arc ``(cx, cy, r, a1, a2)`` from ``p1`` to ``p2`` with signed sagitta.

    Positive ``sagitta`` bows to the left of directed segment ``p1 -> p2`` in SVG
    coordinates (x right, y down); negative ``sagitta`` bows to the right.
    """
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    chord = math.hypot(dx, dy)
    if chord < 1e-6 or abs(sagitta) < 1e-4:
        msg = f"Degenerate arc_through({p1}, {p2}, sagitta={sagitta})"
        raise ValueError(msg)
    s = abs(sagitta)
    r = (chord * chord) / (8.0 * s) + 0.5 * s
    mx, my = 0.5 * (x1 + x2), 0.5 * (y1 + y2)
    # Left unit normal in SVG coords (x right, y down): (dy/chord, -dx/chord)
    nx, ny = dy / chord, -dx / chord
    sign = 1.0 if sagitta > 0.0 else -1.0
    # Center lies opposite the bulge by (r - s)
    cx = mx - sign * (r - s) * nx
    cy = my - sign * (r - s) * ny
    a1 = math.degrees(math.atan2(y1 - cy, x1 - cx))
    a2 = math.degrees(math.atan2(y2 - cy, x2 - cx))
    a1_n, a2_n = normalize_short_span(a1, a2)
    return (cx, cy, r, a1_n, a2_n)


def clip_arc_to_medallion(
    cx: float,
    cy: float,
    r: float,
    a1: float,
    a2: float,
    margin: float = 0.0,
) -> list[tuple[float, float]]:
    """Clip a circular arc ``(cx, cy, r, a1..a2)`` to stay strictly inside the medallion.

    Returns a list of ``(start_deg, end_deg)`` sub-arc intervals whose points all lie
    within radius ``MED_R + margin`` of ``(MED_CX, MED_CY)``.
    """
    a1_n, a2_n = normalize_short_span(a1, a2)
    rad_limit = MED_R + margin
    d_centers = math.hypot(cx - MED_CX, cy - MED_CY)
    # Entire circle inside medallion
    if d_centers + r <= rad_limit:
        return [(a1_n, a2_n)]
    # Entire circle outside medallion
    if d_centers >= r + rad_limit or r >= d_centers + rad_limit:
        return []

    # Exact circle-circle intersection angles on circle (cx, cy, r)
    cos_val = (r * r + d_centers * d_centers - rad_limit * rad_limit) / (2.0 * r * d_centers)
    cos_val = max(-1.0, min(1.0, cos_val))
    base_angle = math.degrees(math.atan2(MED_CY - cy, MED_CX - cx))
    delta_deg = math.degrees(math.acos(cos_val))

    # Candidate split angles aligned to [min_a, max_a]
    lo, hi = (a1_n, a2_n) if a1_n <= a2_n else (a2_n, a1_n)
    cuts: list[float] = [lo, hi]
    for raw_ang in (base_angle - delta_deg, base_angle + delta_deg):
        for k in (-2, -1, 0, 1, 2):
            cand = raw_ang + 360.0 * k
            if lo + 1e-4 < cand < hi - 1e-4:
                cuts.append(cand)
    cuts.sort()

    intervals: list[tuple[float, float]] = []
    for s_ang, e_ang in zip(cuts[:-1], cuts[1:], strict=False):
        mid = 0.5 * (s_ang + e_ang)
        mx, my = polar(cx, cy, r, mid)
        if math.hypot(mx - MED_CX, my - MED_CY) <= rad_limit + 1e-3:
            if a1_n <= a2_n:
                intervals.append((s_ang, e_ang))
            else:
                intervals.append((e_ang, s_ang))
    if a1_n > a2_n:
        intervals.reverse()
    return intervals


class MedallionBuilder:
    """Shared compass-and-straightedge portrait builder with automatic medallion clipping."""

    def __init__(self) -> None:
        """Initialize the four canonical visual layers."""
        self.layers: dict[str, list[dict[str, Any]]] = {
            "scaffold": [],
            "golden": [],
            "detail": [],
            "primary": [],
        }

    def add_circle(
        self,
        layer: str,
        cx: float,
        cy: float,
        r: float,
        *,
        filled: bool = False,
        clip: bool = True,
    ) -> None:
        """Add a circle (skipping if it would protrude outside ``MED_R`` when ``clip=True``)."""
        if clip and math.hypot(cx - MED_CX, cy - MED_CY) + r > MED_R + 0.5:
            return
        entry: dict[str, Any] = {"kind": "circle", "cx": cx, "cy": cy, "r": r}
        if filled:
            entry["filled"] = True
        self.layers[layer].append(entry)

    def add_line(
        self,
        layer: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        clip: bool = True,
    ) -> None:
        """Add a straight segment, auto-clipped to ``MED_R`` by default."""
        if clip:
            clipped = clip_line_to_medallion(x1, y1, x2, y2)
            if clipped is None:
                return
            x1, y1, x2, y2 = clipped
        self.layers[layer].append({"kind": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2})

    def add_arc(
        self,
        layer: str,
        cx: float,
        cy: float,
        r: float,
        a1: float,
        a2: float,
        *,
        clip: bool = True,
    ) -> None:
        """Add a circular arc (``M ... A ...``), auto-clipped to ``MED_R`` by default."""
        spans = (
            clip_arc_to_medallion(cx, cy, r, a1, a2)
            if clip
            else [normalize_short_span(a1, a2)]
        )
        for sa, ea in spans:
            if abs(ea - sa) < 0.2:
                continue
            self.layers[layer].append(
                {
                    "kind": "arc",
                    "d": arc_path(cx, cy, r, sa, ea),
                    "cx": cx,
                    "cy": cy,
                    "r": r,
                    "a1": sa,
                    "a2": ea,
                }
            )

    def add_arc_pts(
        self,
        layer: str,
        p1: tuple[float, float],
        p2: tuple[float, float],
        sagitta: float,
        *,
        clip: bool = True,
    ) -> None:
        """Add a circular arc from ``p1`` to ``p2`` with signed ``sagitta``."""
        if abs(sagitta) < 0.08:
            self.add_line(layer, p1[0], p1[1], p2[0], p2[1], clip=clip)
            return
        cx, cy, r, a1, a2 = arc_through(p1, p2, sagitta)
        self.add_arc(layer, cx, cy, r, a1, a2, clip=clip)

    def add_wave(
        self,
        layer: str,
        p1: tuple[float, float],
        p2: tuple[float, float],
        half_waves: int,
        half_angle_deg: float = 32.0,
        initial_sign: int = 1,
    ) -> None:
        """Add a G1-smooth chain of externally tangent circular arcs (Euclid III.12)."""
        for cx, cy, r, a1, a2 in tangent_wave_arcs(
            p1[0], p1[1], p2[0], p2[1], half_waves, half_angle_deg, initial_sign
        ):
            self.add_arc(layer, cx, cy, r, a1, a2, clip=True)

    def add_scaffold_base(
        self,
        *,
        eye_lx: float = -13.0,
        eye_rx: float = 13.0,
        head_cx: float = 0.0,
        head_cy: float = -27.0,
        head_r: float = 26.0,
    ) -> None:
        """Add the canonical medallion scaffold (ring, axes, R, R*phi, Vesica eye circles)."""
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        self.add_circle("scaffold", MED_CX, MED_CY, MED_R, clip=False)
        self.add_line("scaffold", head_cx, MED_CY - MED_R, head_cx, MED_CY + MED_R)
        self.add_line("scaffold", -MED_R, head_cy, MED_R, head_cy)
        self.add_line("scaffold", -MED_R, head_cy + head_r, MED_R, head_cy + head_r)
        self.add_circle("scaffold", head_cx, head_cy, head_r)
        self.add_circle("scaffold", head_cx, head_cy, head_r * phi)
        self.add_circle("scaffold", head_cx, head_cy, head_r * phi * 1.25)
        eye_r = max(10.0, 0.5 * abs(eye_rx - eye_lx))
        self.add_circle("scaffold", eye_lx, head_cy, eye_r)
        self.add_circle("scaffold", eye_rx, head_cy, eye_r)

    def add_canonical_eye(
        self,
        cx: float,
        cy: float,
        *,
        width: float = 10.0,
        upper_sag: float = 2.6,
        lower_sag: float = -1.3,
        iris_r: float = 2.2,
        pupil_r: float = 1.05,
        gaze_dx: float = 0.0,
    ) -> None:
        """Draw an eye in the canonical GEOMETOR House Style (lines & circular arcs only)."""
        hw = 0.5 * width
        p_in = (cx - hw, cy)
        p_out = (cx + hw, cy)
        self.add_arc_pts("primary", p_in, p_out, upper_sag)
        self.add_arc_pts("detail", (cx - hw * 0.92, cy - 1.4), (cx + hw * 0.92, cy - 1.4), upper_sag * 0.85)
        self.add_arc_pts("detail", p_in, p_out, lower_sag)
        self.add_circle("detail", cx + gaze_dx, cy - 0.1, iris_r)
        self.add_circle("primary", cx + gaze_dx, cy - 0.1, pupil_r, filled=True)

    def build(self) -> dict[str, list[dict[str, Any]]]:
        """Return the completed 4-layer dictionary for :func:`render_medallion_svg`."""
        return self.layers


def build_empty_medallion_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the canonical empty medallion scaffold (Researched / Ready-for-Artist state)."""
    mb = MedallionBuilder()
    mb.add_scaffold_base()
    # Subtle golden tick marks at canonical eye-line & apex
    mb.add_line("golden", -91.5, -27.0, -85.0, -27.0)
    mb.add_line("golden", 85.0, -27.0, 91.5, -27.0)
    mb.add_line("golden", 0.0, -99.5, 0.0, -93.0)
    mb.add_circle("golden", 0.0, -27.0, 1.4)
    return mb.build()


def build_empty_medallion_svg(theme: str = "dark") -> str:
    """Render the empty canonical medallion SVG for researched-but-undrawn Pantheon slots."""
    return render_medallion_svg(build_empty_medallion_elements(), theme=theme)

