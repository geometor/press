"""Study 40: Proclus Lycius — Pure Sacred Geometric Emblem Medallion.

Celebrates Proclus Diadochus's *Commentary on the First Book of Euclid's
Elements* (412-485 CE) and his Neoplatonic philosophy of *Peras* (Limit),
*Apeiron* (Unlimited), and *Phantasia* (Imagination as the mirror projecting
pure intellectual forms into geometric space):

1. **Concentric Neoplatonic Triad Circles**: Three harmonically spaced rings
   centered at ``(0, -8)`` in exact geometric progression ``1 : sqrt(3) : 3``
   (*Monas* ``r_1 = a``, *Nous* ``r_2 = a * sqrt(3)``, *Psyche / Phantasia*
   ``r_3 = 3a``) with 6-fold radial symmetry rays.
2. **Elements Book I, Proposition 1 Vesica Piscis**: Twin congruent compass
   circles centered at horizontal foci ``A = (-a, -8)`` and ``B = (+a, -8)``
   (radius ``2a``), each passing through the other's center and tangent
   internally to the outer Triad ring ``r_3 = 3a``.
3. **Twin Reflected Golden Equilateral Triangles & Seed-of-Life Rosette**:
   Upper ``<A B C>`` and lower ``<A B D>`` rising from unobstructed golden
   shared base ``AB`` to the exact *Vesica* apexes ``C`` and ``D`` on
   ``r_2 = a * sqrt(3)``, linked by the unobstructed golden vertical ``sqrt(3)``
   axis ``C-D`` and cradling a luminous 6-petal Seed-of-Life rosette and
   inscribed golden hexagram inside ``r_1 = a``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ..portraits import MED_CX, MED_CY, MED_R, MedallionBuilder, polar, render_medallion_svg

__all__ = [
    "build_proclus_elements",
    "build_proclus_svg",
    "write_proclus_svgs",
]

DEFAULT_OUT_DIR = Path(__file__).resolve().parents[4] / "docsrc" / "_static" / "portraits"

Point = tuple[float, float]


def _dist(p1: Point, p2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _add_astrolabe_seal(mb: MedallionBuilder, r_seal: float) -> None:
    """Add the unified GEOMETOR Emblem Pantheon scaffold and graduated astrolabe seal."""
    ox, oy = MED_CX, MED_CY
    r_bezel = r_seal + 4.8

    # Subtle medallion-centered sacred scaffold rings & crosshairs
    mb.add_circle("scaffold", ox, oy, MED_R, clip=False)
    for r in (78.0, 52.0, 26.0):
        mb.add_circle("scaffold", ox, oy, r)
    mb.add_line("scaffold", ox, oy - MED_R, ox, oy + MED_R)
    mb.add_line("scaffold", ox - MED_R, oy, ox + MED_R, oy)
    for deg in (45.0, 135.0, 225.0, 315.0):
        p_in = polar(ox, oy, 78.0, deg)
        p_out = polar(ox, oy, MED_R, deg)
        mb.add_line("scaffold", p_in[0], p_in[1], p_out[0], p_out[1])

    # Bold outer seal ring & fine graduated astrolabe bezel
    mb.add_circle("primary", ox, oy, r_seal)
    mb.add_circle("detail", ox, oy, r_bezel)

    # 36 calibrated astrolabe degree ticks & 4 cardinal golden pins
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


def build_proclus_elements() -> dict[str, list[dict[str, Any]]]:
    """Build the 4-layer sacred emblem medallion for Proclus Lycius.

    Returns:
        Dictionary mapping canonical layers (``scaffold``, ``golden``,
        ``detail``, ``primary``) to lists of primitive geometry entries.
    """
    mb = MedallionBuilder()
    ox, oy = MED_CX, MED_CY
    r_seal = 68.0

    _add_astrolabe_seal(mb, r_seal)

    # ------------------------------------------------------------------
    # 1. Exact Neoplatonic Triad Radii (1 : sqrt(3) : 3) & Vesica Foci
    # ------------------------------------------------------------------
    sqrt3 = math.sqrt(3.0)
    a = 20.0  # Half-base of Euclid I.1; gives r_3 = 3a = 60.0 inside R_seal = 68.0
    r_monas = a  # Ring 1: passes through A and B
    r_nous = a * sqrt3  # Ring 2: passes through Vesica apexes C and D
    r_psyche = 3.0 * a  # Ring 3: externally tangent to both Vesica circles
    r_vesica = 2.0 * a  # Radius of twin Euclid I.1 compass circles

    # Verify exact geometric progression r_monas : r_nous : r_psyche = 1 : sqrt(3) : 3
    if abs((r_nous / r_monas) - sqrt3) > 1e-12 or abs((r_psyche / r_nous) - sqrt3) > 1e-12:
        msg = "Neoplatonic Triad geometric progression violated"
        raise ValueError(msg)

    pt_a: Point = (ox - a, oy)
    pt_b: Point = (ox + a, oy)
    pt_c: Point = (ox, oy - r_nous)
    pt_d: Point = (ox, oy + r_nous)

    # Verify exact Euclid I.1 equilateral triangles and sqrt(3) vesica proportion
    for side in (
        _dist(pt_a, pt_b),
        _dist(pt_a, pt_c),
        _dist(pt_b, pt_c),
        _dist(pt_a, pt_d),
        _dist(pt_b, pt_d),
    ):
        if abs(side - r_vesica) > 1e-12:
            msg = f"Equilateral side invariant violated: {side} != {r_vesica}"
            raise ValueError(msg)
    if abs((_dist(pt_c, pt_d) / _dist(pt_a, pt_b)) - sqrt3) > 1e-12:
        msg = "Vesica sqrt(3) axial ratio violated"
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # 2. Concentric Neoplatonic Triad Circles & 6-Fold Symmetry Rays
    # ------------------------------------------------------------------
    mb.add_circle("detail", ox, oy, r_psyche)
    mb.add_circle("detail", ox, oy, r_nous)
    mb.add_circle("primary", ox, oy, r_monas)

    # 6-fold radial symmetry rays: diagonals span Ring 1 -> Ring 3;
    # vertical extensions span ONLY outside C-D so golden axis C-D stays unobstructed.
    for deg in (30.0, 150.0, 210.0, 330.0):
        p1 = polar(ox, oy, r_monas, deg)
        p2 = polar(ox, oy, r_psyche, deg)
        mb.add_line("detail", p1[0], p1[1], p2[0], p2[1])
        p_n = polar(ox, oy, r_nous, deg)
        mb.add_circle("detail", p_n[0], p_n[1], 1.45)
        mb.add_circle("detail", p2[0], p2[1], 1.55)

    for deg in (90.0, 270.0):
        p_in = polar(ox, oy, r_nous, deg)
        p_out = polar(ox, oy, r_psyche, deg)
        mb.add_line("detail", p_in[0], p_in[1], p_out[0], p_out[1])
        mb.add_circle("detail", p_out[0], p_out[1], 1.55)

    # Horizontal wing extensions ONLY outside A-B so golden Euclid I.1 base AB glows purely
    mb.add_line("detail", ox - r_psyche, oy, pt_a[0], pt_a[1])
    mb.add_line("detail", pt_b[0], pt_b[1], ox + r_psyche, oy)
    mb.add_circle("golden", ox - r_psyche, oy, 1.65)
    mb.add_circle("golden", ox + r_psyche, oy, 1.65)

    # ------------------------------------------------------------------
    # 3. Heroic Elements I.1 Vesica Piscis (Twin Congruent Circles)
    # ------------------------------------------------------------------
    mb.add_circle("primary", pt_a[0], pt_a[1], r_vesica)
    mb.add_circle("primary", pt_b[0], pt_b[1], r_vesica)

    # ------------------------------------------------------------------
    # 4. Inscribed 6-Petal Seed-of-Life Rosette & Golden Hexagram inside Monas
    # ------------------------------------------------------------------
    r_seed = 0.5 * a  # 10.0: 6 tangent petal circles passing through O and kissing r_1 = 20.0
    for k in range(6):
        deg = float(k * 60)
        scx, scy = polar(ox, oy, r_seed, deg)
        mb.add_circle("detail", scx, scy, r_seed)

    # Inscribed inner golden hexagram (interlocking upward & downward triangles on r_1)
    tri_up = [polar(ox, oy, r_monas, deg) for deg in (-90.0, 30.0, 150.0)]
    tri_dn = [polar(ox, oy, r_monas, deg) for deg in (90.0, 210.0, 330.0)]
    for tri in (tri_up, tri_dn):
        for i in range(3):
            p1, p2 = tri[i], tri[(i + 1) % 3]
            mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # ------------------------------------------------------------------
    # 5. Twin Reflected Golden Equilateral Triangles <ABC> & <ABD> + Axis CD
    # ------------------------------------------------------------------
    # Unobstructed golden shared base AB and vertical sqrt(3) Vesica axis CD
    mb.add_line("golden", pt_a[0], pt_a[1], pt_b[0], pt_b[1])
    mb.add_line("golden", pt_c[0], pt_c[1], pt_d[0], pt_d[1])

    # Four radiant diamond edges of Limit (upper <ABC>) & Unlimited (lower <ABD>)
    for p1, p2 in ((pt_a, pt_c), (pt_b, pt_c), (pt_a, pt_d), (pt_b, pt_d)):
        mb.add_line("golden", p1[0], p1[1], p2[0], p2[1])

    # Bold double-ringed golden nodes at A, B, C, D
    for vx, vy in (pt_a, pt_b, pt_c, pt_d):
        mb.add_circle("golden", vx, vy, 4.3)
        mb.add_circle("golden", vx, vy, 2.35, filled=True)

    # Central Monas jewel at O = (0, -8)
    mb.add_circle("golden", ox, oy, 2.9)
    mb.add_circle("golden", ox, oy, 1.35, filled=True)

    return mb.build()


def build_proclus_svg(theme: str = "dark") -> str:
    """Render the Proclus Lycius medallion SVG for ``'dark'`` or ``'light'`` theme."""
    layers = build_proclus_elements()
    return render_medallion_svg(layers, theme=theme)


def write_proclus_svgs(out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write ``proclus_dark.svg`` and ``proclus_light.svg`` to ``out_dir``."""
    target_dir = out_dir or DEFAULT_OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    dark_path = target_dir / "proclus_dark.svg"
    light_path = target_dir / "proclus_light.svg"
    dark_path.write_text(build_proclus_svg(theme="dark"), encoding="utf-8")
    light_path.write_text(build_proclus_svg(theme="light"), encoding="utf-8")
    return dark_path, light_path
