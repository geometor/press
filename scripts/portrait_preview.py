"""Single-command grid, dark/light render, and reference-overlay helper for portrait studies."""

from __future__ import annotations

import argparse
import importlib
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw
from weasyprint import HTML

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from geometor.press.portraits import MED_CX, MED_CY, MED_R, RIM_R, render_medallion_svg  # noqa: E402

VB_X, VB_Y, VB_W, VB_H = -102.0, -106.0, 204.0, 196.0
CANVAS_W = 816  # 4 px per SVG unit
CANVAS_H = 784


def svg_to_px(x: float, y: float) -> tuple[float, float]:
    """Convert SVG viewBox coordinate to pixel coordinate on ``CANVAS_W x CANVAS_H``."""
    return ((x - VB_X) * (CANVAS_W / VB_W), (y - VB_Y) * (CANVAS_H / VB_H))


def build_calibrated_crop(
    ref_path: Path,
    *,
    cx_frac: float = 0.5,
    eye_frac: float = 0.40,
    head_w_frac: float = 0.30,
) -> Image.Image:
    """Scale and position ``ref_path`` so eyes land at ``(0, -27)`` and head width is ``~52`` units."""
    with Image.open(ref_path) as raw:
        img = raw.convert("RGB")
    iw, ih = img.size
    # Target head width = 52 SVG units = 208 px
    target_head_px = 52.0 * (CANVAS_W / VB_W)
    scale = target_head_px / max(1.0, iw * head_w_frac)
    nw = max(1, int(round(iw * scale)))
    nh = max(1, int(round(ih * scale)))
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), (13, 16, 23))
    target_cx, target_cy = svg_to_px(0.0, -27.0)
    ox = int(round(target_cx - cx_frac * nw))
    oy = int(round(target_cy - eye_frac * nh))
    canvas.paste(resized, (ox, oy))
    return canvas


def draw_grid_overlay(base: Image.Image) -> Image.Image:
    """Draw canonical 10/20 SVG coordinate grid, medallion circle, and cranial circle."""
    out = base.copy().convert("RGBA")
    overlay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Grid lines every 10 units
    for gx in range(-100, 101, 10):
        px, _ = svg_to_px(gx, 0)
        color = (212, 175, 55, 130) if gx == 0 else (120, 180, 255, 95 if gx % 20 == 0 else 45)
        draw.line([(px, 0), (px, CANVAS_H)], fill=color, width=1)
        if gx % 20 == 0:
            draw.text((px + 2, 4), f"{gx}", fill=(255, 220, 120, 220))
    for gy in range(-100, 91, 10):
        _, py = svg_to_px(0, gy)
        color = (120, 180, 255, 95 if gy % 20 == 0 else 45)
        draw.line([(0, py), (CANVAS_W, py)], fill=color, width=1)
        if gy % 20 == 0:
            draw.text((4, py + 2), f"{gy}", fill=(255, 220, 120, 220))

    # Canonical eye line y = -27
    _, eye_py = svg_to_px(0, -27.0)
    draw.line([(0, eye_py), (CANVAS_W, eye_py)], fill=(255, 100, 100, 190), width=2)
    draw.text((4, eye_py - 14), "y=-27", fill=(255, 130, 130, 240))

    # Medallion circle MED_R = 92 & outer rim 95.2
    for rad, col, w in ((MED_R, (212, 175, 55, 220), 2), (RIM_R, (212, 175, 55, 120), 1)):
        x0, y0 = svg_to_px(MED_CX - rad, MED_CY - rad)
        x1, y1 = svg_to_px(MED_CX + rad, MED_CY + rad)
        draw.ellipse([x0, y0, x1, y1], outline=col, width=w)

    # Cranial circle (0, -27), R=26 & golden circle R*phi
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    for rad, col in ((26.0, (0, 255, 180, 200)), (26.0 * phi, (212, 175, 55, 130))):
        x0, y0 = svg_to_px(-rad, -27.0 - rad)
        x1, y1 = svg_to_px(rad, -27.0 + rad)
        draw.ellipse([x0, y0, x1, y1], outline=col, width=2)

    return Image.alpha_composite(out, overlay).convert("RGB")


def svg_text_to_png(svg_text: str, out_png: Path, *, bg: str | None = None, dpi: int = 150) -> None:
    """Render an SVG string to a crisp PNG via WeasyPrint + pdftoppm."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    # Match exact 204:196 page aspect ratio (in pt: 306pt x 294pt)
    bg_css = f"background:{bg};" if bg else "background:transparent;"
    html = (
        f"<html><head><style>"
        f"@page {{ size: 306pt 294pt; margin: 0; }}"
        f"html, body {{ margin:0; padding:0; width:306pt; height:294pt; {bg_css} overflow:hidden; }}"
        f"svg {{ width:306pt; height:294pt; display:block; }}"
        f"</style></head><body>{svg_text}</body></html>"
    )
    pdf_path = out_png.with_suffix(".tmp.pdf")
    HTML(string=html).write_pdf(str(pdf_path))
    prefix = out_png.with_suffix("")
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), "-singlefile", str(pdf_path), str(prefix)],
        check=True,
    )
    pdf_path.unlink(missing_ok=True)


def render_study_previews(
    study_id: str,
    out_dir: Path,
    *,
    ref_path: Path | None = None,
    cx_frac: float = 0.5,
    eye_frac: float = 0.40,
    head_w_frac: float = 0.30,
) -> None:
    """Render ``<id>_dark.png``, ``<id>_light.png``, and optional ``<id>_overlay.png``."""
    out_dir.mkdir(parents=True, exist_ok=True)
    mod_name = study_id.replace("-", "_")
    mod = importlib.import_module(f"geometor.press.portrait_studies.{mod_name}")
    builder = getattr(mod, f"build_{mod_name}_elements")
    layers = builder()

    dark_svg = render_medallion_svg(layers, theme="dark")
    light_svg = render_medallion_svg(layers, theme="light")
    svg_text_to_png(dark_svg, out_dir / f"{mod_name}_dark.png", bg="#0d1017", dpi=160)
    svg_text_to_png(light_svg, out_dir / f"{mod_name}_light.png", bg="#f8f5ee", dpi=160)

    if ref_path is not None and ref_path.is_file():
        crop = build_calibrated_crop(
            ref_path, cx_frac=cx_frac, eye_frac=eye_frac, head_w_frac=head_w_frac
        )
        # Render dark SVG with darkened crop blended underneath
        dark_img = Image.open(out_dir / f"{mod_name}_dark.png").convert("RGB").resize(
            crop.size, Image.Resampling.LANCZOS
        )
        # Highlight bright strokes over dimmed reference photo
        blended = Image.blend(crop, dark_img, 0.58)
        blended.save(out_dir / f"{mod_name}_overlay.png")
    print(f"Rendered previews for {study_id} in {out_dir}")


def main() -> None:
    """CLI entrypoint for grid generation and study preview rendering."""
    parser = argparse.ArgumentParser(description="GEOMETOR Portrait Atelier Preview Tool")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_grid = sub.add_parser("grid", help="Generate calibrated coordinate grid over reference image")
    p_grid.add_argument("ref_jpg", type=Path)
    p_grid.add_argument("out_png", type=Path)
    p_grid.add_argument("--cx-frac", type=float, default=0.50)
    p_grid.add_argument("--eye-frac", type=float, default=0.40)
    p_grid.add_argument("--head-w-frac", type=float, default=0.30)

    p_ren = sub.add_parser("render", help="Render dark, light, and overlay PNGs for a portrait study")
    p_ren.add_argument("study_id", type=str)
    p_ren.add_argument("out_dir", type=Path)
    p_ren.add_argument("--ref", type=Path, default=None)
    p_ren.add_argument("--cx-frac", type=float, default=0.50)
    p_ren.add_argument("--eye-frac", type=float, default=0.40)
    p_ren.add_argument("--head-w-frac", type=float, default=0.30)

    args = parser.parse_args()
    if args.cmd == "grid":
        crop = build_calibrated_crop(
            args.ref_jpg,
            cx_frac=args.cx_frac,
            eye_frac=args.eye_frac,
            head_w_frac=args.head_w_frac,
        )
        gridded = draw_grid_overlay(crop)
        args.out_png.parent.mkdir(parents=True, exist_ok=True)
        gridded.save(args.out_png)
        print(f"Wrote grid: {args.out_png}")
    elif args.cmd == "render":
        render_study_previews(
            args.study_id,
            args.out_dir,
            ref_path=args.ref,
            cx_frac=args.cx_frac,
            eye_frac=args.eye_frac,
            head_w_frac=args.head_w_frac,
        )


if __name__ == "__main__":
    main()
