"""Render the live 48-slot GEOMETOR Pantheon Dark Poster (8x6 chronological grid).

Slot states:
- ``queued``: faint dashed blueprint circle + muted name & dates below
- ``researched``: empty canonical medallion scaffold (gold rim, axes, R, R*phi, eyes)
- ``complete``: finished dark-theme portrait medallion SVG

Writes atomically via temp file + ``os.replace`` so an open image viewer refreshes cleanly.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from weasyprint import HTML

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from geometor.press.portraits import build_empty_medallion_svg  # noqa: E402

PORTRAITS_JSON = REPO_ROOT / "resources" / "portraits.json"
POSTER_DIR = REPO_ROOT / "editions" / "posters"
CACHE_DIR = POSTER_DIR / ".medallion_cache"
POSTER_PNG = POSTER_DIR / "geometor_portraits_poster.png"
POSTER_DOC_PNG = REPO_ROOT / "docsrc" / "_static" / "portraits" / "geometor_portraits_poster.png"

BG_COLOR = (8, 12, 18)
CARD_BG = (13, 16, 23)
GOLD = (212, 175, 55)
GOLD_DIM = (158, 132, 56)
IVORY = (238, 242, 247)
SLATE_LIGHT = (176, 190, 209)
SLATE_MUTED = (96, 114, 138)
DASH_RING = (46, 60, 80)

COLS = 8
ROWS = 6
CELL_W = 360
CELL_H = 408
MED_W = 310
MED_H = int(round(MED_W * 196 / 204))  # ~298 px preserving 204:196 aspect ratio
MARGIN_X = 110
HEADER_H = 190
FOOTER_H = 90
POSTER_W = MARGIN_X * 2 + COLS * CELL_W
POSTER_H = HEADER_H + ROWS * CELL_H + FOOTER_H


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a crisp serif/sans system font with graceful fallback."""
    candidates = (
        [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
    )
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def render_svg_to_png_cached(svg_text: str, cache_key: str, mtime_ns: int) -> Image.Image:
    """Render an SVG string to a cached ``MED_W x MED_H`` RGB PIL image."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached_png = CACHE_DIR / f"{cache_key}_{mtime_ns}.png"
    if not cached_png.is_file():
        # Clean older cached versions for this key
        for old in CACHE_DIR.glob(f"{cache_key}_*.png"):
            old.unlink(missing_ok=True)
        html = (
            "<html><head><style>"
            "@page { size: 306pt 294pt; margin: 0; }"
            "html, body { margin:0; padding:0; width:306pt; height:294pt; background:#0d1017; overflow:hidden; }"
            "svg { width:306pt; height:294pt; display:block; }"
            "</style></head><body>"
            f"{svg_text}"
            "</body></html>"
        )
        pdf_tmp = CACHE_DIR / f"{cache_key}.tmp.pdf"
        raw_prefix = CACHE_DIR / f"{cache_key}_raw"
        HTML(string=html).write_pdf(str(pdf_tmp))
        subprocess.run(
            ["pdftoppm", "-png", "-r", "120", "-singlefile", str(pdf_tmp), str(raw_prefix)],
            check=True,
        )
        pdf_tmp.unlink(missing_ok=True)
        raw_png = CACHE_DIR / f"{cache_key}_raw.png"
        with Image.open(raw_png) as img:
            resized = img.convert("RGB").resize((MED_W, MED_H), Image.Resampling.LANCZOS)
            resized.save(cached_png, format="PNG")
        raw_png.unlink(missing_ok=True)
    with Image.open(cached_png) as im:
        return im.copy()


def draw_dashed_circle(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    r: float,
    color: tuple[int, int, int],
    *,
    width: int = 2,
    dashes: int = 44,
) -> None:
    """Draw a clean dashed blueprint circle for queued slots."""
    step = 360.0 / dashes
    bbox = [cx - r, cy - r, cx + r, cy + r]
    for i in range(dashes):
        a0 = i * step
        a1 = a0 + step * 0.52
        draw.arc(bbox, start=a0, end=a1, fill=color, width=width)


def make_queued_tile() -> Image.Image:
    """Create the queued-state dashed blueprint tile."""
    tile = Image.new("RGB", (MED_W, MED_H), BG_COLOR)
    draw = ImageDraw.Draw(tile)
    # Medallion center (0, -8) in viewBox(-102, -106, 204, 196)
    cx = (0.0 - (-102.0)) / 204.0 * MED_W
    cy = (-8.0 - (-106.0)) / 196.0 * MED_H
    r_inner = 92.0 / 204.0 * MED_W
    r_outer = 95.2 / 204.0 * MED_W
    draw_dashed_circle(draw, cx, cy, r_outer, (38, 50, 68), width=2, dashes=48)
    draw_dashed_circle(draw, cx, cy, r_inner, DASH_RING, width=1, dashes=32)
    # Subtle crosshair at canonical eye center (0, -27)
    ey = (-27.0 - (-106.0)) / 196.0 * MED_H
    draw.line([(cx - 10, ey), (cx + 10, ey)], fill=(46, 60, 80), width=1)
    draw.line([(cx, ey - 10), (cx, ey + 10)], fill=(46, 60, 80), width=1)
    return tile


def draw_centered(
    draw: ImageDraw.ImageDraw,
    cx: float,
    y: float,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, int, int],
) -> None:
    """Draw horizontally centered text at ``(cx, y)``."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2.0, y), text, font=font, fill=fill)


def shorten(text: str, max_chars: int = 34) -> str:
    """Truncate label cleanly with ellipsis if wider than slot."""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def build_poster() -> Path:
    """Render and atomically save the 48-slot GEOMETOR Pantheon Dark Poster."""
    payload = json.loads(PORTRAITS_JSON.read_text(encoding="utf-8"))
    portraits: list[dict[str, Any]] = list(payload.get("portraits", []))
    # Sort chronologically by birth_year (fallback queue_order)
    portraits.sort(key=lambda p: (int(p.get("birth_year", 9999)), int(p.get("queue_order", 999))))

    n_complete = sum(1 for p in portraits if p.get("status") == "complete")
    n_researched = sum(1 for p in portraits if p.get("status") == "researched")
    n_queued = sum(1 for p in portraits if p.get("status") == "queued")
    n_total = len(portraits)

    canvas = Image.new("RGB", (POSTER_W, POSTER_H), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # Outer double gold museum border
    draw.rectangle([28, 28, POSTER_W - 29, POSTER_H - 29], outline=GOLD_DIM, width=2)
    draw.rectangle([38, 38, POSTER_W - 39, POSTER_H - 39], outline=(48, 62, 82), width=1)

    font_title = load_font(54, bold=True)
    font_sub = load_font(22, bold=False)
    font_name = load_font(22, bold=True)
    font_dates = load_font(16, bold=False)
    font_motif = load_font(14, bold=False)
    font_footer = load_font(18, bold=False)

    draw_centered(draw, POSTER_W / 2.0, 56, "GEOMETOR  ·  PANTHEON OF GEOMETERS", font_title, IVORY)
    subtitle = (
        f"Compass-and-Straightedge Portrait Medallions  (Lines & Circular Arcs Only · 0 Béziers)   |   "
        f"{n_complete} Complete · {n_researched} Researched · {n_queued} Queued  ({n_total} Total)"
    )
    draw_centered(draw, POSTER_W / 2.0, 128, subtitle, font_sub, GOLD)
    draw.line([(MARGIN_X, 168), (POSTER_W - MARGIN_X, 168)], fill=(48, 62, 82), width=1)

    empty_svg = build_empty_medallion_svg(theme="dark")
    empty_tile = render_svg_to_png_cached(empty_svg, "_empty_medallion", 1)
    queued_tile = make_queued_tile()

    # Soft circular mask so square SVG background blends seamlessly with poster background
    mask = Image.new("L", (MED_W, MED_H), 0)
    mask_draw = ImageDraw.Draw(mask)
    mcx = (0.0 - (-102.0)) / 204.0 * MED_W
    mcy = (-8.0 - (-106.0)) / 196.0 * MED_H
    mr = 97.5 / 204.0 * MED_W
    mask_draw.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=255)

    for idx, p in enumerate(portraits[: COLS * ROWS]):
        row = idx // COLS
        col = idx % COLS
        cell_x = MARGIN_X + col * CELL_W
        cell_y = HEADER_H + row * CELL_H
        cx = cell_x + CELL_W / 2.0
        tile_x = int(round(cx - MED_W / 2.0))
        tile_y = cell_y + 8

        status = str(p.get("status", "queued"))
        pid = str(p["id"])
        name = str(p["name"])
        dates = str(p.get("dates", ""))
        motif = str(p.get("signature_motif", ""))

        if status == "complete":
            dark_rel = p.get("outputs", {}).get("dark_svg", f"docsrc/_static/portraits/{pid.replace('-', '_')}_dark.svg")
            dark_path = REPO_ROOT / dark_rel
            if dark_path.is_file():
                tile = render_svg_to_png_cached(
                    dark_path.read_text(encoding="utf-8"),
                    pid,
                    dark_path.stat().st_mtime_ns,
                )
                canvas.paste(tile, (tile_x, tile_y), mask)
            else:
                canvas.paste(empty_tile, (tile_x, tile_y), mask)
            name_col = IVORY
            dates_col = GOLD
            motif_col = SLATE_LIGHT
        elif status == "researched":
            canvas.paste(empty_tile, (tile_x, tile_y), mask)
            name_col = SLATE_LIGHT
            dates_col = GOLD_DIM
            motif_col = SLATE_MUTED
        else:
            canvas.paste(queued_tile, (tile_x, tile_y))
            name_col = SLATE_MUTED
            dates_col = (72, 86, 106)
            motif_col = (58, 70, 88)

        label_y = tile_y + MED_H + 6
        draw_centered(draw, cx, label_y, shorten(name, 26), font_name, name_col)
        draw_centered(draw, cx, label_y + 28, dates, font_dates, dates_col)
        if status in ("complete", "researched") and motif:
            draw_centered(draw, cx, label_y + 50, shorten(motif, 38), font_motif, motif_col)

    draw.line(
        [(MARGIN_X, POSTER_H - FOOTER_H + 10), (POSTER_W - MARGIN_X, POSTER_H - FOOTER_H + 10)],
        fill=(48, 62, 82),
        width=1,
    )
    draw_centered(
        draw,
        POSTER_W / 2.0,
        POSTER_H - FOOTER_H + 30,
        "GEOMETOR Press · Canonical Medallion R = 92 · Eye-Line Horizon y = −27 · Chronological Pantheon (c. 428 BCE – Present)",
        font_footer,
        SLATE_MUTED,
    )

    POSTER_DIR.mkdir(parents=True, exist_ok=True)
    tmp_png = POSTER_PNG.with_suffix(".tmp.png")
    canvas.save(tmp_png, format="PNG", optimize=True)
    os.replace(tmp_png, POSTER_PNG)

    POSTER_DOC_PNG.parent.mkdir(parents=True, exist_ok=True)
    tmp_doc = POSTER_DOC_PNG.with_suffix(".tmp.png")
    canvas.save(tmp_doc, format="PNG", optimize=True)
    os.replace(tmp_doc, POSTER_DOC_PNG)

    print(
        f"Updated live poster: {POSTER_PNG} "
        f"({n_complete} complete, {n_researched} researched, {n_queued} queued)"
    )
    return POSTER_PNG


if __name__ == "__main__":
    build_poster()
