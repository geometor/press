"""Project Medallion: Seer Sessions — Empirical Reasoning Archive.

Sacred geometric emblem for ``geometor/seer_sessions`` framed within the
unified ``R = 68`` graduated astrolabe seal:

1. **Four Concentric Quartile Telemetry Rings (``Q1..Q4``)**: Calibrated radial
   benchmark rings at ``25%, 50%, 75%, 100%`` (``r = 13, 26, 39, 52``) divided
   cleanly into 12 radial session epochs by precision sector dividers.
2. **Radially Plotted Golden Convergence Curve & Baseline Envelope**: Across
   all 12 benchmark epochs, a golden convergence trajectory climbs steadily
   from ``42%`` to ``96%`` with radial telemetry bars and double-ringed peak
   jewels, contrasted against an inner ``detail`` baseline benchmark polygon.
3. **Outer Cumulative Arc Gauge (``84%`` Solved Span)**: A double-rail outer
   circular gauge (``r = 58.0..62.4``) tracks cumulative archive convergence
   clockwise from North with radiant golden arc bands, calibrated ``10 deg``
   metric ticks, and a luminous end-cap needle.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_seer_sessions_elements",
    "build_seer_sessions_svg",
    "write_seer_sessions_svgs",
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


def _add_long_arc(
    mb: MedallionBuilder,
    layer: str,
    cx: float,
    cy: float,
    r: float,
    start_deg: float,
    sweep_deg: float,
) -> None:
    """Add a circular arc of arbitrary positive ``sweep_deg`` split into <= 120-deg spans."""
    remaining = sweep_deg
    cur = start_deg
    while remaining > 1e-6:
        step = min(120.0, remaining)
        mb.add_arc(layer, cx, cy, r, cur, cur + step)
        cur += step
        remaining -= step


def build_seer_sessions_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/seer_sessions``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Four Concentric Quartile Telemetry Rings (Q1..Q4) & 12 Sectors
    # ------------------------------------------------------------------
    r_core = 6.5
    r_q = (13.0, 26.0, 39.0, 52.0)  # Exact 25%, 50%, 75%, 100% quartile rings
    mb.add_circle("detail", ox, oy, r_core)
    for idx, rq in enumerate(r_q):
        layer = "primary" if idx in (1, 3) else "detail"
        mb.add_circle(layer, ox, oy, rq)

    # 12 radial telemetry sector dividers (every 30 deg from North -90 deg)
    for k in range(12):
        deg = -90.0 + 30.0 * k
        p_in = polar(ox, oy, r_core, deg)
        r_end = r_q[3] + (3.2 if k % 3 == 0 else 0.0)
        p_out = polar(ox, oy, r_end, deg)
        mb.add_line("primary" if k % 3 == 0 else "detail", p_in[0], p_in[1], p_out[0], p_out[1])

    # Crisp quartile notch ticks along cardinal axes
    for deg in (-90.0, 0.0, 90.0, 180.0):
        rad = math.radians(deg)
        nx, ny = -math.sin(rad), math.cos(rad)
        for rq in r_q[:3]:
            cx, cy = polar(ox, oy, rq, deg)
            mb.add_line("detail", cx - 1.6 * nx, cy - 1.6 * ny, cx + 1.6 * nx, cy + 1.6 * ny)

    # ------------------------------------------------------------------
    # 2. Baseline Envelope & Radially Plotted Golden Convergence Trajectory
    # ------------------------------------------------------------------
    baseline_scores = (0.28, 0.31, 0.35, 0.38, 0.42, 0.46, 0.48, 0.51, 0.54, 0.57, 0.60, 0.63)
    converged_scores = (0.42, 0.49, 0.54, 0.62, 0.67, 0.74, 0.78, 0.83, 0.87, 0.91, 0.94, 0.97)

    base_pts: list[Point] = []
    conv_pts: list[Point] = []
    for k in range(12):
        deg = -90.0 + 30.0 * k
        base_pts.append(polar(ox, oy, baseline_scores[k] * r_q[3], deg))
        conv_pts.append(polar(ox, oy, converged_scores[k] * r_q[3], deg))

    # Inner baseline benchmark polygon (detail)
    for k in range(11):
        p1, p2 = base_pts[k], base_pts[k + 1]
        mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])
    for bx, by in base_pts:
        mb.add_circle("detail", bx, by, 1.0, filled=True)

    # Golden radial improvement bars (from baseline score up to converged score)
    for k in range(12):
        bpt, cpt = base_pts[k], conv_pts[k]
        mb.add_line("golden", bpt[0], bpt[1], cpt[0], cpt[1])

    # Luminous golden convergence trajectory polyline connecting all 12 epoch nodes
    for k in range(11):
        p1, p2 = conv_pts[k], conv_pts[k + 1]
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Radially plotted golden convergence nodes (crowned at Q2/Q3/Q4 peaks)
    for k, (cx, cy) in enumerate(conv_pts):
        if k in (0, 5, 11):
            mb.add_circle("golden", cx, cy, 3.2)
            mb.add_circle("golden", cx, cy, 1.55, filled=True)
        elif k % 3 == 0:
            mb.add_circle("golden", cx, cy, 2.5)
            mb.add_circle("golden", cx, cy, 1.2, filled=True)
        else:
            mb.add_circle("golden", cx, cy, 1.8)
            mb.add_circle("golden", cx, cy, 0.95, filled=True)

    # ------------------------------------------------------------------
    # 3. Outer Cumulative Arc Gauge (84% Solved Telemetry Band)
    # ------------------------------------------------------------------
    r_gauge_in = 58.2
    r_gauge_out = 62.6
    r_gauge_mid1 = 59.6
    r_gauge_mid2 = 61.2

    # Clean outer track rails in detail
    mb.add_circle("detail", ox, oy, r_gauge_in)
    mb.add_circle("detail", ox, oy, r_gauge_out)

    # Active cumulative solved arc: 84% = 302.4 deg clockwise from North (-90 deg)
    cumulative_frac = 0.84
    sweep_deg = 360.0 * cumulative_frac
    start_deg = -90.0
    end_deg = start_deg + sweep_deg

    _add_long_arc(mb, "golden", ox, oy, r_gauge_mid1, start_deg, sweep_deg)
    _add_long_arc(mb, "golden", ox, oy, r_gauge_mid2, start_deg, sweep_deg)

    # Calibrated radial metric ticks every 12 deg along the active cumulative gauge
    n_ticks = int(sweep_deg // 12.0)
    for t in range(n_ticks + 1):
        deg = start_deg + 12.0 * t
        p1 = polar(ox, oy, r_gauge_in, deg)
        p2 = polar(ox, oy, r_gauge_out, deg)
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Crisp start cap at North and glowing end-cap indicator needle at 84%
    for deg in (start_deg, end_deg):
        p1 = polar(ox, oy, r_gauge_in - 2.2, deg)
        p2 = polar(ox, oy, r_gauge_out + 2.0, deg)
        mb.add_line("primary", p1[0], p1[1], p2[0], p2[1])
    end_jewel = polar(ox, oy, 0.5 * (r_gauge_in + r_gauge_out), end_deg)
    mb.add_circle("golden", end_jewel[0], end_jewel[1], 2.9)
    mb.add_circle("golden", end_jewel[0], end_jewel[1], 1.45, filled=True)

    # Central archive core jewel
    mb.add_circle("golden", ox, oy, 2.8)
    mb.add_circle("golden", ox, oy, 1.35, filled=True)

    return mb.build()


def build_seer_sessions_svg(theme: str = "dark") -> str:
    """Render the Seer Sessions project medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_seer_sessions_elements()
    return render_medallion_svg(layers, theme=theme)


def write_seer_sessions_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``seer_sessions_dark.svg`` and ``seer_sessions_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "seer_sessions_dark.svg"
    light_path = target_dir / "seer_sessions_light.svg"
    dark_path.write_text(build_seer_sessions_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_seer_sessions_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
