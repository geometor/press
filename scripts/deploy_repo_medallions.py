"""Deploy compass-and-straightedge medallions as logos, favicons, heroes, and portal thumbnails."""

from __future__ import annotations

import argparse
from collections.abc import Callable
import importlib
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any

from PIL import Image, ImageDraw
import weasyprint

_SRC = str(Path(__file__).resolve().parents[1] / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from geometor.press.portraits import MED_R, RIM_R, render_medallion_coin_svg

GEO_ROOT = Path("/home/phi/PROJECTS/geometor")
COM_MEDALLIONS_DIR = GEO_ROOT / "geometor.com" / "docsrc" / "_static" / "medallions"

# Maps every GEOMETOR repo folder name to (subpackage, module_name, builder_func_name).
REPO_MEDALLION_MAP: dict[str, tuple[str, str, str]] = {
    # 43 repositories mapped to completed 48-person Pantheon medallions
    "altshiller-court": ("portrait_studies", "altshiller_court", "build_altshiller_court_elements"),
    "apollonius": ("portrait_studies", "apollonius", "build_apollonius_elements"),
    "aquinas": ("portrait_studies", "aquinas", "build_aquinas_elements"),
    "archimedes": ("portrait_studies", "archimedes", "build_archimedes_elements"),
    "aristotle": ("portrait_studies", "aristotle", "build_aristotle_elements"),
    "bertrand-russell": ("portrait_studies", "bertrand_russell", "build_bertrand_russell_elements"),
    "byrne": ("portrait_studies", "byrne", "build_byrne_elements"),
    "casey": ("portrait_studies", "casey", "build_casey_elements"),
    "ceva": ("portrait_studies", "ceva", "build_ceva_elements"),
    "cusa": ("portrait_studies", "cusa", "build_cusa_elements"),
    "durer": ("portrait_studies", "durer", "build_durer_elements"),
    "etc": ("portrait_studies", "kimberling", "build_kimberling_elements"),
    "euclid": ("portrait_studies", "euclid", "build_euclid_elements"),
    "euler": ("portrait_studies", "euler", "build_euler_elements"),
    "feuerbach": ("portrait_studies", "feuerbach", "build_feuerbach_elements"),
    "fibonacci": ("portrait_studies", "fibonacci", "build_fibonacci_elements"),
    "hambidge": ("portrait_studies", "hambidge", "build_hambidge_elements"),
    "heron": ("portrait_studies", "heron", "build_heron_elements"),
    "hilbert": ("portrait_studies", "hilbert", "build_hilbert_elements"),
    "hoenen": ("portrait_studies", "hoenen", "build_hoenen_elements"),
    "huntley": ("portrait_studies", "huntley", "build_huntley_elements"),
    "kepler": ("portrait_studies", "kepler", "build_kepler_elements"),
    "klein": ("portrait_studies", "klein", "build_klein_elements"),
    "lemoine": ("portrait_studies", "lemoine", "build_lemoine_elements"),
    "livio": ("portrait_studies", "livio", "build_livio_elements"),
    "mascheroni": ("portrait_studies", "mascheroni", "build_mascheroni_elements"),
    "menelaus": ("portrait_studies", "menelaus", "build_menelaus_elements"),
    "nicomachus": ("portrait_studies", "nicomachus", "build_nicomachus_elements"),
    "pacioli": ("portrait_studies", "pacioli", "build_pacioli_elements"),
    "pappus": ("portrait_studies", "pappus", "build_pappus_elements"),
    "pascal": ("portrait_studies", "pascal", "build_pascal_elements"),
    "pasch": ("portrait_studies", "pasch", "build_pasch_elements"),
    "petersen": ("portrait_studies", "petersen", "build_petersen_elements"),
    "piero": ("portrait_studies", "piero", "build_piero_elements"),
    "plato": ("portrait_studies", "plato", "build_plato_elements"),
    "poincare": ("portrait_studies", "poincare", "build_poincare_elements"),
    "proclus": ("portrait_studies", "proclus", "build_proclus_elements"),
    "ptolemy": ("portrait_studies", "ptolemy", "build_ptolemy_elements"),
    "staudt": ("portrait_studies", "staudt", "build_staudt_elements"),
    "steiner": ("portrait_studies", "steiner", "build_steiner_elements"),
    "thompson": ("portrait_studies", "thompson", "build_thompson_elements"),
    "walter-russell": ("portrait_studies", "walter_russell", "build_walter_russell_elements"),
    "wildberger": ("portrait_studies", "wildberger", "build_wildberger_elements"),
    # 21 bespoke non-human project & catalog graphic medallions
    "codes": ("project_medallions", "codes", "build_codes_elements"),
    "constructions": ("project_medallions", "constructions", "build_constructions_elements"),
    "divine": ("project_medallions", "divine", "build_divine_elements"),
    "elementarium": ("project_medallions", "elementarium", "build_elementarium_elements"),
    "elements": ("project_medallions", "elements", "build_elements_elements"),
    "explorer": ("project_medallions", "explorer", "build_explorer_elements"),
    "fundamentals": ("project_medallions", "fundamentals", "build_fundamentals_elements"),
    "geometor.com": ("project_medallions", "geometor", "build_geometor_elements"),
    "gibert": ("project_medallions", "gibert", "build_gibert_elements"),
    "heptadecagon": ("project_medallions", "heptadecagon", "build_heptadecagon_elements"),
    "knott": ("project_medallions", "knott", "build_knott_elements"),
    "levels": ("project_medallions", "levels", "build_levels_elements"),
    "model": ("project_medallions", "model", "build_model_elements"),
    "phyllotaxis": ("project_medallions", "phyllotaxis", "build_phyllotaxis_elements"),
    "polyhedra": ("project_medallions", "polyhedra", "build_polyhedra_elements"),
    "posamentier": ("project_medallions", "posamentier", "build_posamentier_elements"),
    "press": ("project_medallions", "press", "build_press_elements"),
    "seer": ("project_medallions", "seer", "build_seer_elements"),
    "seer_navigator": ("project_medallions", "seer_navigator", "build_seer_navigator_elements"),
    "seer_sessions": ("project_medallions", "seer_sessions", "build_seer_sessions_elements"),
    "trees": ("project_medallions", "trees", "build_trees_elements"),
}

# Additional Pantheon person medallions whose ID does not equal a repo folder name
EXTRA_PERSON_MEDALLIONS: dict[str, tuple[str, str, str]] = {
    "ernst-haeckel": ("portrait_studies", "ernst_haeckel", "build_ernst_haeckel_elements"),
    "hans-kayser": ("portrait_studies", "hans_kayser", "build_hans_kayser_elements"),
    "heath": ("portrait_studies", "heath", "build_heath_elements"),
    "kimberling": ("portrait_studies", "kimberling", "build_kimberling_elements"),
    "leonardo": ("portrait_studies", "leonardo", "build_leonardo_elements"),
    "odom": ("portrait_studies", "odom", "build_odom_elements"),
}

# Repos whose home page already has a custom interactive hero (keep logo/favicon, don't inject hero)
SKIP_HOME_HERO_REPOS = {"geometor.com"}


def _load_builder(subpkg: str, mod_name: str, fn_name: str) -> Callable[[], dict[str, list[dict[str, Any]]]]:
    mod = importlib.import_module(f"geometor.press.{subpkg}.{mod_name}")
    fn = getattr(mod, fn_name)
    return fn


def _render_coin_png_and_ico(
    layers: dict[str, list[dict[str, Any]]],
    logo_png: Path,
    favicon_ico: Path,
    size: int = 512,
) -> None:
    """Render a transparent-exterior circular medallion PNG logo and multi-size ICO favicon."""
    svg_dark = render_medallion_coin_svg(layers, theme="dark")
    # Render at 2x supersampling (1024x1024) on solid dark bg, then apply exact circular alpha mask
    hi_size = size * 2
    html = (
        "<!doctype html><html><head><style>"
        f"@page {{ size: {hi_size}px {hi_size}px; margin: 0; }}"
        "html, body { margin: 0; padding: 0; background: #0d1017; }"
        f"svg {{ display: block; width: {hi_size}px; height: {hi_size}px; }}"
        "</style></head><body>"
        f"{svg_dark}"
        "</body></html>"
    )
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pdf_path = tmp_path / "coin.pdf"
        png_prefix = tmp_path / "coin"
        weasyprint.HTML(string=html).write_pdf(str(pdf_path))
        subprocess.run(
            ["pdftoppm", "-png", "-r", "96", "-singlefile", str(pdf_path), str(png_prefix)],
            check=True,
            capture_output=True,
        )
        raw = Image.open(f"{png_prefix}.png").convert("RGBA")
        if raw.size != (hi_size, hi_size):
            raw = raw.resize((hi_size, hi_size), Image.Resampling.LANCZOS)

        # Build crisp 4x antialiased circular alpha mask matching RIM_R (95.2 + stroke/2 inside 200 viewBox)
        mask_scale = 2
        m_size = hi_size * mask_scale
        mask_hi = Image.new("L", (m_size, m_size), 0)
        draw = ImageDraw.Draw(mask_hi)
        # viewBox="-100 -108 200 200" centered on (0, -8); outer rim radius = RIM_R + 0.65
        radius_frac = min(0.992, (RIM_R + 0.8) / 100.0)
        pad = (1.0 - radius_frac) * 0.5 * m_size
        draw.ellipse((pad, pad, m_size - pad, m_size - pad), fill=255)
        mask = mask_hi.resize((hi_size, hi_size), Image.Resampling.LANCZOS)
        raw.putalpha(mask)

        final_logo = raw.resize((size, size), Image.Resampling.LANCZOS)
        logo_png.parent.mkdir(parents=True, exist_ok=True)
        final_logo.save(logo_png, format="PNG", optimize=True)

        # Save multi-resolution favicon.ico (16, 32, 48, 64)
        favicon_ico.parent.mkdir(parents=True, exist_ok=True)
        final_logo.save(
            favicon_ico,
            format="ICO",
            sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
        )


def _inject_home_hero(index_rst: Path, repo_name: str) -> bool:
    """Idempotently feature _static/medallion.svg right beneath the H1 title of docsrc/index.rst."""
    if not index_rst.is_file():
        return False
    text = index_rst.read_text(encoding="utf-8")
    if "_static/medallion.svg" in text or "repo-medallion-hero" in text:
        return False

    lines = text.splitlines()
    # Find the H1 heading (supports both overline+underline === and underline-only ===)
    insert_at: int | None = None
    alt_title = repo_name.replace("-", " ").title()
    for i in range(len(lines) - 1):
        curr = lines[i].strip()
        nxt = lines[i + 1].strip()
        if (
            curr
            and nxt
            and not curr.startswith(("=", "-", ":", ".."))
            and set(nxt) == {"="}
            and len(nxt) >= max(3, len(curr) - 2)
        ):
            alt_title = re.sub(r"[`*]", "", curr).strip()
            insert_at = i + 2
            break

    if insert_at is None:
        return False

    hero_block = [
        "",
        ".. image:: _static/medallion.svg",
        f"   :alt: {alt_title} Medallion",
        "   :class: repo-medallion-hero",
    ]
    new_lines = lines[:insert_at] + hero_block + lines[insert_at:]
    trailing = "\n" if text.endswith("\n") else ""
    index_rst.write_text("\n".join(new_lines) + trailing, encoding="utf-8")
    return True


def deploy_all(selected: list[str] | None = None, skip_hero: bool = False) -> None:
    """Deploy medallions to all selected GEOMETOR repos and export portal thumbnails."""
    COM_MEDALLIONS_DIR.mkdir(parents=True, exist_ok=True)
    targets = selected if selected else sorted(REPO_MEDALLION_MAP.keys())

    deployed = 0
    heroes_added = 0
    for repo in targets:
        if repo not in REPO_MEDALLION_MAP:
            print(f"SKIP unknown repo: {repo}")
            continue
        subpkg, mod_name, fn_name = REPO_MEDALLION_MAP[repo]
        repo_dir = GEO_ROOT / repo
        docsrc = repo_dir / "docsrc"
        if not docsrc.is_dir():
            print(f"SKIP missing docsrc: {repo}")
            continue

        builder = _load_builder(subpkg, mod_name, fn_name)
        layers = builder()

        static_dir = docsrc / "_static"
        static_dir.mkdir(parents=True, exist_ok=True)
        coin_svg = render_medallion_coin_svg(layers, theme="adaptive")

        # 1. Write repo adaptive coin SVG
        (static_dir / "medallion.svg").write_text(coin_svg, encoding="utf-8")
        # 2. Export portal thumbnail for geometor.com/projects/ and /people/
        (COM_MEDALLIONS_DIR / f"{repo}.svg").write_text(coin_svg, encoding="utf-8")
        if repo == "walter-russell":
            (COM_MEDALLIONS_DIR / "russell.svg").write_text(coin_svg, encoding="utf-8")
        elif repo == "constructions":
            (COM_MEDALLIONS_DIR / "animations.svg").write_text(coin_svg, encoding="utf-8")
        # 3. Render 512px transparent circular logo.png & multi-size favicon.ico
        _render_coin_png_and_ico(
            layers,
            static_dir / "logo.png",
            static_dir / "favicon.ico",
            size=512,
        )
        # 4. Feature medallion on home page
        if not skip_hero and repo not in SKIP_HOME_HERO_REPOS:
            if _inject_home_hero(docsrc / "index.rst", repo):
                heroes_added += 1

        deployed += 1
        print(f"[{deployed:02d}/{len(targets):02d}] Deployed medallion -> {repo}")

    # Also export extra Pantheon person medallions to geometor.com/_static/medallions/
    if not selected:
        for person_id, (subpkg, mod_name, fn_name) in sorted(EXTRA_PERSON_MEDALLIONS.items()):
            layers = _load_builder(subpkg, mod_name, fn_name)()
            coin_svg = render_medallion_coin_svg(layers, theme="adaptive")
            (COM_MEDALLIONS_DIR / f"{person_id}.svg").write_text(coin_svg, encoding="utf-8")
        print(f"Exported {len(EXTRA_PERSON_MEDALLIONS)} additional Pantheon person coins to {COM_MEDALLIONS_DIR}")

    print(f"Done: {deployed} repositories updated ({heroes_added} home heroes added); MED_R={MED_R}.")


def main() -> None:
    """CLI entry point for deploying medallions across GEOMETOR repos."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repos", nargs="*", help="Optional subset of repo names to deploy.")
    parser.add_argument("--skip-hero", action="store_true", help="Skip home page index.rst hero injection.")
    args = parser.parse_args()
    deploy_all(selected=args.repos, skip_hero=args.skip_hero)


if __name__ == "__main__":
    main()
