"""Project Medallion: Model (geometor/model) — Exact Symbolic Geometry Engine.

Visualizes the exact compass-and-straightedge Constructive DAG of
``geometor.model`` inside the unified ``R = 68`` graduated astrolabe seal:

1. **Three Mutually Intersecting Circles & Radical Center**: Three primary
   circles ``C_1, C_2, C_3`` anchored on genesis centers ``O_1, O_2, O_3``
   generate six exact analytical circle-circle intersection nodes
   ``A, B, C, D, E, F`` whose three pairwise radical axes concur at the exact
   Radical Center ``R`` (verified to ``< 1e-12``).
2. **Two Secant Lines & Exact Secant Intersections**: Two crisp secant lines
   sweeping from apex ``A`` through ``C`` and ``E`` pierce ``C_3`` at exact
   analytical nodes ``G`` and ``H``.
3. **Glowing Golden Ancestral Dependency DAG**: Directed golden dependency
   edges with crisp directional chevrons trace constructive ancestry from
   genesis centers ``O_1, O_2, O_3`` through radical intersections ``A..F`` to
   the Radical Center ``R`` and derived secant nodes ``G, H``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_model_elements",
    "build_model_svg",
    "write_model_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _circle_circle_intersections(
    c1: Point,
    r1: float,
    c2: Point,
    r2: float,
) -> tuple[Point, Point]:
    """Return the two exact intersection points of circles ``(c1, r1)`` and ``(c2, r2)``."""
    dx = c2[0] - c1[0]
    dy = c2[1] - c1[1]
    d = math.hypot(dx, dy)
    if d < 1e-12 or d >= r1 + r2 or d <= abs(r1 - r2):
        msg = f"Circles do not intersect cleanly: d={d:.6f}, r1={r1}, r2={r2}"
        raise ValueError(msg)
    a = (r1 * r1 - r2 * r2 + d * d) / (2.0 * d)
    h = math.sqrt(max(0.0, r1 * r1 - a * a))
    mx = c1[0] + a * dx / d
    my = c1[1] + a * dy / d
    rx = -dy * (h / d)
    ry = dx * (h / d)
    return ((mx + rx, my + ry), (mx - rx, my - ry))


def _line_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Point:
    """Return the exact intersection of lines ``p1-p2`` and ``p3-p4``."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-12:
        msg = "Parallel lines in _line_intersection"
        raise ValueError(msg)
    det1 = x1 * y2 - y1 * x2
    det2 = x3 * y4 - y3 * x4
    return (
        (det1 * (x3 - x4) - (x1 - x2) * det2) / denom,
        (det1 * (y3 - y4) - (y1 - y2) * det2) / denom,
    )


def _line_circle_intersections(
    p1: Point,
    p2: Point,
    cx: float,
    cy: float,
    r: float,
) -> tuple[Point, Point]:
    """Return the two intersections of infinite line ``p1-p2`` with circle ``(cx, cy, r)``."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    fx, fy = p1[0] - cx, p1[1] - cy
    a = dx * dx + dy * dy
    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - r * r
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        msg = "Secant line does not intersect target circle"
        raise ValueError(msg)
    s = math.sqrt(disc)
    t1 = (-b - s) / (2.0 * a)
    t2 = (-b + s) / (2.0 * a)
    return ((p1[0] + t1 * dx, p1[1] + t1 * dy), (p1[0] + t2 * dx, p1[1] + t2 * dy))


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


def _add_dag_edge(
    mb: MedallionBuilder,
    src: Point,
    dst: Point,
    *,
    t_chevron: float = 0.58,
    chevron_size: float = 2.6,
) -> None:
    """Draw a glowing golden ancestral DAG edge from ``src`` to ``dst`` with a chevron."""
    mb.add_line("golden", src[0], src[1], dst[0], dst[1])
    dx, dy = dst[0] - src[0], dst[1] - src[1]
    seg_len = math.hypot(dx, dy)
    if seg_len < 6.0:
        return
    ux, uy = dx / seg_len, dy / seg_len
    nx, ny = -uy, ux
    tip_x = src[0] + t_chevron * dx
    tip_y = src[1] + t_chevron * dy
    back_x = tip_x - chevron_size * ux
    back_y = tip_y - chevron_size * uy
    wing = 0.62 * chevron_size
    mb.add_line("golden", tip_x, tip_y, back_x + wing * nx, back_y + wing * ny)
    mb.add_line("golden", tip_x, tip_y, back_x - wing * nx, back_y - wing * ny)


def build_model_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/model``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Three Genesis Circles & Exact Analytical Radical Intersections
    # ------------------------------------------------------------------
    o1: Point = (ox - 20.0, oy - 12.0)
    o2: Point = (ox + 20.0, oy - 12.0)
    o3: Point = (ox, oy + 19.0)
    r1, r2, r3 = 30.0, 30.0, 28.0

    # Pairwise circle-circle intersections
    p12_a, p12_b = _circle_circle_intersections(o1, r1, o2, r2)
    pt_a, pt_b = (p12_a, p12_b) if p12_a[1] < p12_b[1] else (p12_b, p12_a)

    p13_a, p13_b = _circle_circle_intersections(o1, r1, o3, r3)
    pt_c, pt_d = (p13_a, p13_b) if p13_a[0] < p13_b[0] else (p13_b, p13_a)

    p23_a, p23_b = _circle_circle_intersections(o2, r2, o3, r3)
    pt_e, pt_f = (p23_a, p23_b) if p23_a[0] > p23_b[0] else (p23_b, p23_a)

    # Verify exact radical center concurrency of (A-B), (C-D), (E-F)
    rad_r1 = _line_intersection(pt_a, pt_b, pt_c, pt_d)
    rad_r2 = _line_intersection(pt_a, pt_b, pt_e, pt_f)
    if _dist(rad_r1, rad_r2) > 1e-11:
        msg = f"Radical center concurrency violated: {_dist(rad_r1, rad_r2):.3e}"
        raise ValueError(msg)
    pt_rad = rad_r1

    # Two secant lines through A-C and A-E piercing circle C_3 at exact nodes G and H
    s1_lo, s1_hi = _line_circle_intersections(pt_a, pt_c, ox, oy, r_seal)
    s2_lo, s2_hi = _line_circle_intersections(pt_a, pt_e, ox, oy, r_seal)

    g_cands = _line_circle_intersections(pt_a, pt_c, o3[0], o3[1], r3)
    pt_g = g_cands[0] if _dist(g_cands[0], pt_c) > _dist(g_cands[1], pt_c) else g_cands[1]

    h_cands = _line_circle_intersections(pt_a, pt_e, o3[0], o3[1], r3)
    pt_h = h_cands[0] if _dist(h_cands[0], pt_e) > _dist(h_cands[1], pt_e) else h_cands[1]

    # Verify exact circle membership of derived secant nodes
    if abs(_dist(pt_g, o3) - r3) > 1e-11 or abs(_dist(pt_h, o3) - r3) > 1e-11:
        msg = "Secant intersection membership invariant violated"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Detail Layer: Radical Axes & Genesis Center Triangle
    # ------------------------------------------------------------------
    mb.add_line("detail", o1[0], o1[1], o2[0], o2[1])
    mb.add_line("detail", o2[0], o2[1], o3[0], o3[1])
    mb.add_line("detail", o3[0], o3[1], o1[0], o1[1])

    # Three radical axes meeting at Radical Center R
    for p_u, p_v in ((pt_a, pt_b), (pt_c, pt_d), (pt_e, pt_f)):
        ax1, ax2 = _line_circle_intersections(p_u, p_v, ox, oy, 58.0)
        mb.add_line("detail", ax1[0], ax1[1], ax2[0], ax2[1])

    # Subtle construction halo rings around genesis centers
    for oc in (o1, o2, o3):
        mb.add_circle("detail", oc[0], oc[1], 7.0)

    # ------------------------------------------------------------------
    # 3. Bold Primary Layer: Three Circles & Two Secant Lines
    # ------------------------------------------------------------------
    mb.add_circle("primary", o1[0], o1[1], r1)
    mb.add_circle("primary", o2[0], o2[1], r2)
    mb.add_circle("primary", o3[0], o3[1], r3)

    mb.add_line("primary", s1_lo[0], s1_lo[1], s1_hi[0], s1_hi[1])
    mb.add_line("primary", s2_lo[0], s2_lo[1], s2_hi[0], s2_hi[1])

    # ------------------------------------------------------------------
    # 4. Luminous Golden Ancestral Dependency DAG & Radical Nodes
    # ------------------------------------------------------------------
    # Genesis centers -> primary radical intersections
    _add_dag_edge(mb, o1, pt_a, t_chevron=0.56)
    _add_dag_edge(mb, o2, pt_a, t_chevron=0.56)
    _add_dag_edge(mb, o1, pt_c, t_chevron=0.56)
    _add_dag_edge(mb, o3, pt_c, t_chevron=0.56)
    _add_dag_edge(mb, o2, pt_e, t_chevron=0.56)
    _add_dag_edge(mb, o3, pt_e, t_chevron=0.56)

    # Inner intersections converging onto the Radical Center R
    _add_dag_edge(mb, pt_a, pt_rad, t_chevron=0.55)
    _add_dag_edge(mb, pt_d, pt_rad, t_chevron=0.60, chevron_size=2.0)
    _add_dag_edge(mb, pt_f, pt_rad, t_chevron=0.60, chevron_size=2.0)
    _add_dag_edge(mb, pt_rad, pt_b, t_chevron=0.62, chevron_size=2.2)

    # Secant dependency links C -> G, E -> H, and closing chord G -- H
    _add_dag_edge(mb, pt_c, pt_g, t_chevron=0.55)
    _add_dag_edge(mb, pt_e, pt_h, t_chevron=0.55)
    mb.add_line("golden", pt_g[0], pt_g[1], pt_h[0], pt_h[1])

    # Genesis center nodes O1, O2, O3
    for oc in (o1, o2, o3):
        mb.add_circle("golden", oc[0], oc[1], 3.3)
        mb.add_circle("golden", oc[0], oc[1], 1.6, filled=True)

    # Six radical intersection nodes A, B, C, D, E, F
    for node in (pt_a, pt_b, pt_c, pt_e):
        mb.add_circle("golden", node[0], node[1], 4.0)
        mb.add_circle("golden", node[0], node[1], 2.1, filled=True)
    for node in (pt_d, pt_f, pt_g, pt_h):
        mb.add_circle("golden", node[0], node[1], 3.1)
        mb.add_circle("golden", node[0], node[1], 1.55, filled=True)

    # Radiant Radical Center jewel R
    mb.add_circle("golden", pt_rad[0], pt_rad[1], 5.2)
    mb.add_circle("golden", pt_rad[0], pt_rad[1], 2.5, filled=True)

    return mb.build()


def build_model_svg(theme: str = "dark") -> str:
    """Render the ``geometor/model`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_model_elements()
    return render_medallion_svg(layers, theme=theme)


def write_model_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``model_dark.svg`` and ``model_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "model_dark.svg"
    light_path = target_dir / "model_light.svg"
    dark_path.write_text(build_model_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_model_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
