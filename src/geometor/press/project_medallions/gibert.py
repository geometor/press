"""Author Medallion: Bernard Gibert — Catalogue of Triangle Cubics (CTC).

Sacred geometric emblem celebrating Bernard Gibert's *Catalogue of Triangle
Cubics* (``CTC``) and the iconic **Neuberg Cubic (``K001``)**, framed within
the unified ``R = 68`` graduated astrolabe seal:

1. **Acute Scalene Triangle ``ABC``, Circumcircle ``(O, R = 42)``, & Incircle
   ``(I, r)``**: An exact acute scalene reference triangle (angles ``76 deg,
   58 deg, 46 deg``) inscribed in its primary circumcircle centered at
   ``O = X(3) = (0, -8)``, accompanied by its exact incircle ``(I, r)``,
   altitudes meeting at orthocenter ``H = X(4)``, and Euler line ``O-H``.
2. **Exact Isogonal-Conjugate Pairs & Sideline Reflections**: Verifies exact
   triangle centers ``X(1) = I`` (self-isogonal), ``(X(3) = O, X(4) = H)``,
   and ``(X(13) = Fermat, X(15) = Isodynamic)``, along with the sideline
   reflections ``A', B', C'`` across ``BC, CA, AB`` — every one of which
   satisfies the exact Neuberg Cubic equation ``F(P) = 0`` to ``< 1e-10``.
3. **Exact Neuberg Cubic (``K001``) via Circular Osculating Arcs**: Traces the
   exact real algebraic locus ``(S* (P* - P)) x (H - O) = 0`` inside the
   ``R = 68`` seal via Newton-polished contour extraction and renders both
   branches as a smooth chain of exact 3-point circular osculating arcs
   (zero Beziers) threading precisely through ``A, B, C, I, O, H, X(13), X(15)``
   and sideline reflections.
"""

from __future__ import annotations

from collections.abc import Callable
import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_gibert_elements",
    "build_gibert_svg",
    "write_gibert_svgs",
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


def _reflect_point_across_line(pt: Point, l1: Point, l2: Point) -> Point:
    """Return exact reflection of ``pt`` across line ``l1-l2``."""
    dx, dy = l2[0] - l1[0], l2[1] - l1[1]
    denom = dx * dx + dy * dy
    t = ((pt[0] - l1[0]) * dx + (pt[1] - l1[1]) * dy) / denom
    fx, fy = l1[0] + t * dx, l1[1] + t * dy
    return (2.0 * fx - pt[0], 2.0 * fy - pt[1])


def _foot_on_line(pt: Point, l1: Point, l2: Point) -> Point:
    """Return orthogonal projection foot of ``pt`` onto line ``l1-l2``."""
    dx, dy = l2[0] - l1[0], l2[1] - l1[1]
    t = ((pt[0] - l1[0]) * dx + (pt[1] - l1[1]) * dy) / (dx * dx + dy * dy)
    return (l1[0] + t * dx, l1[1] + t * dy)


def _line_circle_intersections(
    p1: Point,
    p2: Point,
    cx: float,
    cy: float,
    r: float,
) -> tuple[Point, Point]:
    """Return both intersections of line ``p1-p2`` with circle ``(cx, cy, r)``."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    fx, fy = p1[0] - cx, p1[1] - cy
    a = dx * dx + dy * dy
    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - r * r
    s = math.sqrt(max(0.0, b * b - 4.0 * a * c))
    t1 = (-b - s) / (2.0 * a)
    t2 = (-b + s) / (2.0 * a)
    return ((p1[0] + t1 * dx, p1[1] + t1 * dy), (p1[0] + t2 * dx, p1[1] + t2 * dy))


def _bary_to_point(
    u: float,
    v: float,
    w: float,
    pt_a: Point,
    pt_b: Point,
    pt_c: Point,
) -> Point:
    """Convert unnormalized barycentric coordinates ``(u, v, w)`` to Cartesian point."""
    s = u + v + w
    return (
        (u * pt_a[0] + v * pt_b[0] + w * pt_c[0]) / s,
        (u * pt_a[1] + v * pt_b[1] + w * pt_c[1]) / s,
    )


def _add_arc_3pt(
    mb: MedallionBuilder,
    layer: str,
    p1: Point,
    pm: Point,
    p2: Point,
) -> None:
    """Add an exact circular osculating arc passing through ``p1 -> pm -> p2``."""
    x1, y1 = p1
    x2, y2 = pm
    x3, y3 = p2
    det = 2.0 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(det) < 1e-4:
        mb.add_line(layer, x1, y1, x3, y3)
        return
    a1_sq = x1 * x1 + y1 * y1
    a2_sq = x2 * x2 + y2 * y2
    a3_sq = x3 * x3 + y3 * y3
    cx = (a1_sq * (y2 - y3) + a2_sq * (y3 - y1) + a3_sq * (y1 - y2)) / det
    cy = (a1_sq * (x3 - x2) + a2_sq * (x1 - x3) + a3_sq * (x2 - x1)) / det
    r = math.hypot(x1 - cx, y1 - cy)
    if r > 900.0 or r < 1.5:
        mb.add_line(layer, x1, y1, x3, y3)
        return
    ang1 = math.degrees(math.atan2(y1 - cy, x1 - cx))
    angm = math.degrees(math.atan2(y2 - cy, x2 - cx))
    ang2 = math.degrees(math.atan2(y3 - cy, x3 - cx))
    d12 = (ang2 - ang1 + 180.0) % 360.0 - 180.0
    d1m = (angm - ang1 + 180.0) % 360.0 - 180.0
    if (d12 > 0.0 and not (0.0 < d1m < d12)) or (d12 < 0.0 and not (d12 < d1m < 0.0)):
        mb.add_line(layer, x1, y1, x3, y3)
        return
    mb.add_arc(layer, cx, cy, r, ang1, ang1 + d12)


def _trace_cubic_contours(
    f_eval: Callable[[float, float], float],
    ox: float,
    oy: float,
    r_clip: float,
    grid_n: int = 72,
) -> list[list[Point]]:
    """Extract Newton-polished zero-contour polylines of ``f_eval(x, y) = 0`` inside ``r_clip``."""
    step = (2.0 * r_clip) / grid_n
    xs = [ox - r_clip + i * step for i in range(grid_n + 1)]
    ys = [oy - r_clip + j * step for j in range(grid_n + 1)]
    vals = [[f_eval(xs[i], ys[j]) for j in range(grid_n + 1)] for i in range(grid_n + 1)]

    def _polish(px: float, py: float) -> Point:
        eps = 1e-4
        for _ in range(4):
            f0 = f_eval(px, py)
            if abs(f0) < 1e-11:
                break
            fx = (f_eval(px + eps, py) - f_eval(px - eps, py)) / (2.0 * eps)
            fy = (f_eval(px, py + eps) - f_eval(px, py - eps)) / (2.0 * eps)
            g2 = fx * fx + fy * fy
            if g2 < 1e-16:
                break
            px -= f0 * fx / g2
            py -= f0 * fy / g2
        return (px, py)

    EdgeKey = tuple[str, int, int]
    edge_pt: dict[EdgeKey, Point] = {}
    adj: dict[EdgeKey, list[EdgeKey]] = {}

    def _get_h(i: int, j: int) -> EdgeKey:
        key: EdgeKey = ("h", i, j)
        if key not in edge_pt:
            v0, v1 = vals[i][j], vals[i + 1][j]
            t = v0 / (v0 - v1) if abs(v0 - v1) > 1e-15 else 0.5
            edge_pt[key] = _polish(xs[i] + t * step, ys[j])
        return key

    def _get_v(i: int, j: int) -> EdgeKey:
        key: EdgeKey = ("v", i, j)
        if key not in edge_pt:
            v0, v1 = vals[i][j], vals[i][j + 1]
            t = v0 / (v0 - v1) if abs(v0 - v1) > 1e-15 else 0.5
            edge_pt[key] = _polish(xs[i], ys[j] + t * step)
        return key

    for i in range(grid_n):
        for j in range(grid_n):
            cx_cell = 0.5 * (xs[i] + xs[i + 1])
            cy_cell = 0.5 * (ys[j] + ys[j + 1])
            if math.hypot(cx_cell - ox, cy_cell - oy) > r_clip + step:
                continue
            v00 = vals[i][j]
            v10 = vals[i + 1][j]
            v11 = vals[i + 1][j + 1]
            v01 = vals[i][j + 1]
            crossings: list[EdgeKey] = []
            if (v00 >= 0.0) != (v10 >= 0.0):
                crossings.append(_get_h(i, j))
            if (v10 >= 0.0) != (v11 >= 0.0):
                crossings.append(_get_v(i + 1, j))
            if (v01 >= 0.0) != (v11 >= 0.0):
                crossings.append(_get_h(i, j + 1))
            if (v00 >= 0.0) != (v01 >= 0.0):
                crossings.append(_get_v(i, j))
            if len(crossings) == 2:
                k1, k2 = crossings
                adj.setdefault(k1, []).append(k2)
                adj.setdefault(k2, []).append(k1)
            elif len(crossings) == 4:
                vmid = f_eval(cx_cell, cy_cell)
                pairs = (
                    ((crossings[0], crossings[1]), (crossings[2], crossings[3]))
                    if (vmid >= 0.0) == (v10 >= 0.0)
                    else ((crossings[0], crossings[3]), (crossings[1], crossings[2]))
                )
                for k1, k2 in pairs:
                    adj.setdefault(k1, []).append(k2)
                    adj.setdefault(k2, []).append(k1)

    visited: set[tuple[EdgeKey, EdgeKey]] = set()
    chains: list[list[Point]] = []

    def _edge_id(a: EdgeKey, b: EdgeKey) -> tuple[EdgeKey, EdgeKey]:
        return (a, b) if a < b else (b, a)

    starts = [k for k, nbrs in adj.items() if len(nbrs) == 1]
    for start in starts + list(adj.keys()):
        for nxt in adj.get(start, []):
            eid = _edge_id(start, nxt)
            if eid in visited:
                continue
            visited.add(eid)
            chain: list[Point] = [edge_pt[start], edge_pt[nxt]]
            cur = nxt
            while True:
                found = False
                for cand in adj.get(cur, []):
                    cid = _edge_id(cur, cand)
                    if cid not in visited:
                        visited.add(cid)
                        chain.append(edge_pt[cand])
                        cur = cand
                        found = True
                        break
                if not found:
                    break
            sub: list[Point] = []
            for pt in chain:
                if math.hypot(pt[0] - ox, pt[1] - oy) <= r_clip - 0.3:
                    sub.append(pt)
                else:
                    if len(sub) >= 3:
                        chains.append(sub)
                    sub = []
            if len(sub) >= 3:
                chains.append(sub)
    return chains


def build_gibert_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Bernard Gibert (``CTC``).

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Acute Scalene Triangle ABC (76, 58, 46 deg) & Classical Centers
    # ------------------------------------------------------------------
    r_circ = 42.0
    pt_a = polar(ox, oy, r_circ, -108.0)
    pt_b = polar(ox, oy, r_circ, 160.0)
    pt_c = polar(ox, oy, r_circ, 8.0)
    pt_o: Point = (ox, oy)  # X(3) circumcenter

    side_a = _dist(pt_b, pt_c)
    side_b = _dist(pt_c, pt_a)
    side_c = _dist(pt_a, pt_b)
    perim = side_a + side_b + side_c

    ang_a = math.acos((side_b * side_b + side_c * side_c - side_a * side_a) / (2.0 * side_b * side_c))
    ang_b = math.acos((side_c * side_c + side_a * side_a - side_b * side_b) / (2.0 * side_c * side_a))
    ang_c = math.pi - ang_a - ang_b

    # Exact X(1) Incenter & Inradius
    pt_i = _bary_to_point(side_a, side_b, side_c, pt_a, pt_b, pt_c)
    area2 = abs(
        (pt_b[0] - pt_a[0]) * (pt_c[1] - pt_a[1])
        - (pt_b[1] - pt_a[1]) * (pt_c[0] - pt_a[0])
    )
    r_in = area2 / perim

    # Exact X(4) Orthocenter H = A + B + C - 2*O (isogonal conjugate of O)
    pt_h: Point = (
        pt_a[0] + pt_b[0] + pt_c[0] - 2.0 * ox,
        pt_a[1] + pt_b[1] + pt_c[1] - 2.0 * oy,
    )

    # Second isogonal-conjugate pair on K001: X(13) Fermat & X(15) Isodynamic
    pi_3 = math.pi / 3.0
    pt_x13 = _bary_to_point(
        side_a / math.sin(ang_a + pi_3),
        side_b / math.sin(ang_b + pi_3),
        side_c / math.sin(ang_c + pi_3),
        pt_a,
        pt_b,
        pt_c,
    )
    pt_x15 = _bary_to_point(
        side_a * math.sin(ang_a + pi_3),
        side_b * math.sin(ang_b + pi_3),
        side_c * math.sin(ang_c + pi_3),
        pt_a,
        pt_b,
        pt_c,
    )

    # Exact sideline reflections A', B', C' of A, B, C across BC, CA, AB (all lie on K001!)
    pt_a_ref = _reflect_point_across_line(pt_a, pt_b, pt_c)
    pt_b_ref = _reflect_point_across_line(pt_b, pt_c, pt_a)
    pt_c_ref = _reflect_point_across_line(pt_c, pt_a, pt_b)

    # ------------------------------------------------------------------
    # 2. Exact Neuberg Cubic (K001) Implicit Equation & Invariant Verification
    # ------------------------------------------------------------------
    ex, ey = pt_h[0] - pt_o[0], pt_h[1] - pt_o[1]
    a2, b2, c2 = side_a * side_a, side_b * side_b, side_c * side_c
    signed_area2 = (pt_b[0] - pt_a[0]) * (pt_c[1] - pt_a[1]) - (pt_b[1] - pt_a[1]) * (
        pt_c[0] - pt_a[0]
    )

    def _neuberg_f(px: float, py: float) -> float:
        u = ((pt_b[0] - px) * (pt_c[1] - py) - (pt_b[1] - py) * (pt_c[0] - px)) / signed_area2
        v = ((pt_c[0] - px) * (pt_a[1] - py) - (pt_c[1] - py) * (pt_a[0] - px)) / signed_area2
        w = 1.0 - u - v
        vx = a2 * v * w * (pt_a[0] - px) + b2 * w * u * (pt_b[0] - px) + c2 * u * v * (pt_c[0] - px)
        vy = a2 * v * w * (pt_a[1] - py) + b2 * w * u * (pt_b[1] - py) + c2 * u * v * (pt_c[1] - py)
        return vx * ey - vy * ex

    # Verify exact Neuberg cubic incidence on A, B, C, I, O, H, X(13), X(15), A', B', C'
    scale_norm = a2 * r_circ * math.hypot(ex, ey)
    for label, pt in (
        ("A", pt_a),
        ("B", pt_b),
        ("C", pt_c),
        ("I", pt_i),
        ("O", pt_o),
        ("H", pt_h),
        ("X(13)", pt_x13),
        ("X(15)", pt_x15),
        ("A'", pt_a_ref),
        ("B'", pt_b_ref),
        ("C'", pt_c_ref),
    ):
        err = abs(_neuberg_f(pt[0], pt[1])) / scale_norm
        if err > 1e-10:
            msg = f"Neuberg cubic K001 incidence violated at {label}: err={err:.3e}"
            raise ValueError(msg)

    # ------------------------------------------------------------------
    # 3. Detail Construction: Incircle, Altitudes, Euler Line, Reflections
    # ------------------------------------------------------------------
    mb.add_circle("detail", pt_i[0], pt_i[1], r_in)

    # Altitudes meeting at H = X(4)
    for v_pt, s1, s2 in ((pt_a, pt_b, pt_c), (pt_b, pt_c, pt_a), (pt_c, pt_a, pt_b)):
        foot = _foot_on_line(v_pt, s1, s2)
        mb.add_line("detail", v_pt[0], v_pt[1], foot[0], foot[1])

    # Reflection rays A -> A', B -> B' for reflections visible inside the seal
    for orig, ref in ((pt_a, pt_a_ref), (pt_b, pt_b_ref), (pt_c, pt_c_ref)):
        if math.hypot(ref[0] - ox, ref[1] - oy) <= r_seal - 1.5:
            mb.add_line("detail", orig[0], orig[1], ref[0], ref[1])

    # Extended Euler line O-H clipped to the astrolabe seal
    e1, e2 = _line_circle_intersections(pt_o, pt_h, ox, oy, r_seal - 1.0)
    mb.add_line("detail", e1[0], e1[1], e2[0], e2[1])

    # ------------------------------------------------------------------
    # 4. Bold Primary Circumcircle & Acute Scalene Triangle ABC
    # ------------------------------------------------------------------
    mb.add_circle("primary", ox, oy, r_circ)
    mb.add_line("primary", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("primary", pt_b[0], pt_b[1], pt_c[0], pt_c[1])
    mb.add_line("primary", pt_c[0], pt_c[1], pt_a[0], pt_a[1])

    # ------------------------------------------------------------------
    # 5. Luminous Golden Neuberg Cubic (K001) via Exact Osculating Arcs
    # ------------------------------------------------------------------
    contours = _trace_cubic_contours(_neuberg_f, ox, oy, r_seal - 0.5, grid_n=84)
    arc_stride = 4
    for chain in contours:
        n_pts = len(chain)
        idx = 0
        while idx < n_pts - 1:
            nxt = min(n_pts - 1, idx + arc_stride)
            if nxt - idx >= 2:
                mid = (idx + nxt) // 2
                _add_arc_3pt(mb, "golden", chain[idx], chain[mid], chain[nxt])
            else:
                mb.add_line("golden", chain[idx][0], chain[idx][1], chain[nxt][0], chain[nxt][1])
            idx = nxt

    # Parallel golden isogonal-conjugate chords: O--H and X(13)--X(15)
    mb.add_line("golden", pt_o[0], pt_o[1], pt_h[0], pt_h[1])
    mb.add_line("golden", pt_x13[0], pt_x13[1], pt_x15[0], pt_x15[1])

    # Radiant golden double-ringed stars at X(1)=I, X(3)=O, X(4)=H
    for cx, cy in (pt_i, pt_o, pt_h):
        mb.add_circle("golden", cx, cy, 3.3)
        mb.add_circle("golden", cx, cy, 1.6, filled=True)

    # Crisp golden isogonal-conjugate pair jewels at X(13) & X(15)
    for cx, cy in (pt_x13, pt_x15):
        mb.add_circle("golden", cx, cy, 2.3)
        mb.add_circle("golden", cx, cy, 1.1, filled=True)

    # Golden jewels at triangle vertices A, B, C
    for vx, vy in (pt_a, pt_b, pt_c):
        mb.add_circle("golden", vx, vy, 3.1)
        mb.add_circle("golden", vx, vy, 1.5, filled=True)

    # Golden reflection jewels on K001 for sideline reflections inside seal
    for rx, ry in (pt_a_ref, pt_b_ref, pt_c_ref):
        if math.hypot(rx - ox, ry - oy) <= r_seal - 2.0:
            mb.add_circle("golden", rx, ry, 2.6)
            mb.add_circle("golden", rx, ry, 1.25, filled=True)

    return mb.build()


def build_gibert_svg(theme: str = "dark") -> str:
    """Render the Bernard Gibert (CTC) medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_gibert_elements()
    return render_medallion_svg(layers, theme=theme)


def write_gibert_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``gibert_dark.svg`` and ``gibert_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "gibert_dark.svg"
    light_path = target_dir / "gibert_light.svg"
    dark_path.write_text(build_gibert_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_gibert_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
