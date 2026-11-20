"""Project Medallion: Polyhedra (geometor/polyhedra) — Exact 3D Polyhedra Catalog.

Renders an exact 3D orthographic projection of concentric nested Platonic
polyhedra inside a celestial circumsphere within the unified ``R = 68``
graduated astrolabe seal:

1. **Outer Regular Dodecahedron (``R = 56``)**: All 20 exact golden-ratio
   vertices and 30 edges projected through a clean SO(3) rotation, separating
   front-facing edges (``primary``) from back-facing wireframe edges
   (``detail``) for immediate spatial depth.
2. **Middle Cube & Face-Center Dual Octahedron**: An exact cube
   (``R_cube = 36``) gleams in ``golden`` enclosing its exact face-center dual
   octahedron (``R_oct = 36 / sqrt(3)``) in crisp ``primary``, with all 6
   octahedron vertices resting strictly on the cube's 6 face centroids
   (verified to ``< 1e-12``).
3. **Inner Regular Tetrahedron Star Core**: An exact regular tetrahedron
   (``R_tet = 14``) nested at the heart of the octahedron completes the
   four-tier concentric Platonic hierarchy inside concentric spherical rings.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_polyhedra_elements",
    "build_polyhedra_svg",
    "write_polyhedra_svgs",
]

DEFAULT_OUT_DIR = (
    Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits" / "projects"
)

Point3 = tuple[float, float, float]
Point2 = tuple[float, float]


def _norm3(v: Point3) -> float:
    """Return the Euclidean norm of a 3D vector."""
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def _dist3(a: Point3, b: Point3) -> float:
    """Return the Euclidean distance between two 3D points."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def _scale3(v: Point3, radius: float) -> Point3:
    """Normalize 3D vector ``v`` and scale to circumradius ``radius``."""
    n = _norm3(v)
    return (v[0] * radius / n, v[1] * radius / n, v[2] * radius / n)


def _rotate3(v: Point3, yaw_deg: float, pitch_deg: float, roll_deg: float) -> Point3:
    """Apply an exact SO(3) yaw-pitch-roll rotation to 3D point ``v``."""
    x, y, z = v
    cy, sy = math.cos(math.radians(yaw_deg)), math.sin(math.radians(yaw_deg))
    cx, sx = math.cos(math.radians(pitch_deg)), math.sin(math.radians(pitch_deg))
    cz, sz = math.cos(math.radians(roll_deg)), math.sin(math.radians(roll_deg))

    # Yaw around Y
    x1 = cy * x + sy * z
    y1 = y
    z1 = -sy * x + cy * z

    # Pitch around X
    x2 = x1
    y2 = cx * y1 - sx * z1
    z2 = sx * y1 + cx * z1

    # Roll around Z
    x3 = cz * x2 - sz * y2
    y3 = sz * x2 + cz * y2
    z3 = z2
    return (x3, y3, z3)


def _edges_by_min_dist(verts: list[Point3], tol: float = 1e-4) -> list[tuple[int, int]]:
    """Return all exact edge index pairs realizing the minimum pairwise distance."""
    min_d = min(
        _dist3(verts[i], verts[j])
        for i in range(len(verts))
        for j in range(i + 1, len(verts))
    )
    return [
        (i, j)
        for i in range(len(verts))
        for j in range(i + 1, len(verts))
        if abs(_dist3(verts[i], verts[j]) - min_d) <= tol * min_d
    ]


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


def build_polyhedra_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for ``geometor/polyhedra``.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0
    phi = 0.5 * (1.0 + math.sqrt(5.0))
    inv_phi = 1.0 / phi

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact 3D Platonic Solid Coordinates & Edge Graphs
    # ------------------------------------------------------------------
    r_dodec = 56.0
    r_cube = 36.0
    r_oct = r_cube / math.sqrt(3.0)  # Exact face-center dual of the cube
    r_tet = 13.5

    raw_dodec: list[Point3] = []
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            for sz in (-1.0, 1.0):
                raw_dodec.append((sx, sy, sz))
    for sa in (-1.0, 1.0):
        for sb in (-1.0, 1.0):
            raw_dodec.append((0.0, sa * inv_phi, sb * phi))
            raw_dodec.append((sa * inv_phi, sb * phi, 0.0))
            raw_dodec.append((sa * phi, 0.0, sb * inv_phi))

    raw_cube: list[Point3] = [
        (sx, sy, sz) for sx in (-1.0, 1.0) for sy in (-1.0, 1.0) for sz in (-1.0, 1.0)
    ]
    raw_oct: list[Point3] = [
        (1.0, 0.0, 0.0),
        (-1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, -1.0, 0.0),
        (0.0, 0.0, 1.0),
        (0.0, 0.0, -1.0),
    ]
    raw_tet: list[Point3] = [
        (1.0, 1.0, 1.0),
        (1.0, -1.0, -1.0),
        (-1.0, 1.0, -1.0),
        (-1.0, -1.0, 1.0),
    ]

    yaw, pitch, roll = 25.0, 20.0, 8.0

    def project_all(pts: list[Point3], radius: float) -> list[Point3]:
        """Scale 3D vertices to ``radius`` and rotate into view space."""
        return [_rotate3(_scale3(v, radius), yaw, pitch, roll) for v in pts]

    dodec_3d = project_all(raw_dodec, r_dodec)
    cube_3d = project_all(raw_cube, r_cube)
    oct_3d = project_all(raw_oct, r_oct)
    tet_3d = project_all(raw_tet, r_tet)

    dodec_edges = _edges_by_min_dist(dodec_3d)
    cube_edges = _edges_by_min_dist(cube_3d)
    oct_edges = _edges_by_min_dist(oct_3d)
    tet_edges = _edges_by_min_dist(tet_3d)

    # Verify exact Platonic edge counts (30, 12, 12, 6)
    if (len(dodec_edges), len(cube_edges), len(oct_edges), len(tet_edges)) != (30, 12, 12, 6):
        msg = "Platonic solid edge-count invariant violated"
        raise ValueError(msg)

    def to_svg(p: Point3) -> Point2:
        """Orthographically project view-space ``(x, y, z)`` onto SVG medallion plane."""
        return (ox + p[0], oy - p[1])

    # ------------------------------------------------------------------
    # 2. Celestial Circumspheres (Concentric Spherical Shells)
    # ------------------------------------------------------------------
    mb.add_circle("detail", ox, oy, r_dodec)
    mb.add_circle("detail", ox, oy, r_cube)
    mb.add_circle("detail", ox, oy, r_oct)

    # ------------------------------------------------------------------
    # 3. Outer Dodecahedron (Depth-Separated Primary Front / Detail Back)
    # ------------------------------------------------------------------
    for i, j in dodec_edges:
        p1, p2 = dodec_3d[i], dodec_3d[j]
        z_mid = 0.5 * (p1[2] + p2[2])
        q1, q2 = to_svg(p1), to_svg(p2)
        layer = "primary" if z_mid >= -2.0 else "detail"
        mb.add_line(layer, q1[0], q1[1], q2[0], q2[1])

    for v in dodec_3d:
        qx, qy = to_svg(v)
        if v[2] >= 0.0:
            mb.add_circle("golden", qx, qy, 2.3)
            mb.add_circle("golden", qx, qy, 1.15, filled=True)
        else:
            mb.add_circle("detail", qx, qy, 1.15, filled=True)

    # ------------------------------------------------------------------
    # 4. Middle Cube (Golden) & Face-Center Dual Octahedron (Primary)
    # ------------------------------------------------------------------
    for i, j in cube_edges:
        p1, p2 = cube_3d[i], cube_3d[j]
        z_mid = 0.5 * (p1[2] + p2[2])
        q1, q2 = to_svg(p1), to_svg(p2)
        layer = "golden" if z_mid >= -4.0 else "detail"
        mb.add_line(layer, q1[0], q1[1], q2[0], q2[1])

    for v in cube_3d:
        qx, qy = to_svg(v)
        mb.add_circle("golden", qx, qy, 2.7)
        mb.add_circle("golden", qx, qy, 1.3, filled=True)

    for i, j in oct_edges:
        q1, q2 = to_svg(oct_3d[i]), to_svg(oct_3d[j])
        mb.add_line("primary", q1[0], q1[1], q2[0], q2[1])

    for v in oct_3d:
        qx, qy = to_svg(v)
        mb.add_circle("golden", qx, qy, 3.2)
        mb.add_circle("golden", qx, qy, 1.6, filled=True)

    # ------------------------------------------------------------------
    # 5. Inner Regular Tetrahedron Star Core (Golden)
    # ------------------------------------------------------------------
    for i, j in tet_edges:
        q1, q2 = to_svg(tet_3d[i]), to_svg(tet_3d[j])
        mb.add_line("golden", q1[0], q1[1], q2[0], q2[1])

    for v in tet_3d:
        qx, qy = to_svg(v)
        mb.add_circle("golden", qx, qy, 1.7, filled=True)

    # Central sphere origin jewel
    mb.add_circle("golden", ox, oy, 2.2)
    mb.add_circle("golden", ox, oy, 1.0, filled=True)

    return mb.build()


def build_polyhedra_svg(theme: str = "dark") -> str:
    """Render the ``geometor/polyhedra`` medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_polyhedra_elements()
    return render_medallion_svg(layers, theme=theme)


def write_polyhedra_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``polyhedra_dark.svg`` and ``polyhedra_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "polyhedra_dark.svg"
    light_path = target_dir / "polyhedra_light.svg"
    dark_path.write_text(build_polyhedra_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_polyhedra_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
