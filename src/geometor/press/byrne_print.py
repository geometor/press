"""Polychrome Fine-Color Quarto (8.5in x 11in) PDF generator for Oliver Byrne's Euclid."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from pathlib import Path
import re

from .coffee_table import latex_to_html

_BYRNE_COLORS = {
    "red": "#d62828",
    "blue": "#1d4ed8",
    "yellow": "#d97706",
    "black": "#111827",
}


def _render_byrne_line(spec: str) -> str:
    parts = spec.lower().split()
    color = _BYRNE_COLORS.get(parts[0] if parts else "black", "#111827")
    dashed = "dashed" in parts or "dotted" in parts
    glyph = "┄" if dashed else "━━"
    return f'<span class="byrne-sym" style="color:{color}">{glyph}</span>'


def _render_byrne_circle(spec: str) -> str:
    parts = spec.lower().split()
    color = _BYRNE_COLORS.get(parts[0] if parts else "black", "#111827")
    return f'<span class="byrne-sym" style="color:{color}">◯</span>'


def _render_byrne_tri(spec: str) -> str:
    colors = [_BYRNE_COLORS.get(c.strip(), "#111827") for c in spec.lower().split("/")]
    c0 = colors[0] if colors else "#111827"
    return f'<span class="byrne-sym" style="color:{c0}">△</span>'


def _byrne_inline_to_html(text: str) -> str:
    """Convert Byrne RST roles (:byrne-line:, :byrne-circle:, :byrne-tri:, :byrne-op:) to HTML."""
    out = escape(text.strip())

    def _repl_dollar(m: re.Match[str]) -> str:
        raw = m.group(1).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        return f'<span class="math-inline">{latex_to_html(raw)}</span>'

    out = re.sub(r"\$([^$]+)\$", _repl_dollar, out)
    out = re.sub(
        r":byrne-line:`([^`<]+?)\s*&lt;[^`]+&gt;`",
        lambda m: _render_byrne_line(m.group(1)),
        out,
    )
    out = re.sub(
        r":byrne-circle:`([^`<]+?)\s*&lt;[^`]+&gt;`",
        lambda m: _render_byrne_circle(m.group(1)),
        out,
    )
    out = re.sub(
        r":byrne-tri:`([^`<]+?)\s*&lt;[^`]+&gt;`",
        lambda m: _render_byrne_tri(m.group(1)),
        out,
    )
    out = re.sub(r":byrne-op:`therefore`", '<span class="byrne-op">∴</span>', out)
    out = re.sub(r":byrne-op:`([^`]+)`", r'<span class="byrne-op">\1</span>', out)
    out = re.sub(r":just:`([^`]+)`", r'<span class="just-ref">[\1]</span>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", out)
    out = re.sub(r"``([^`]+)``", r"<code>\1</code>", out)
    return out


@dataclass
class ByrneProp:
    """Parsed Byrne proposition."""

    title: str
    rubric: str
    svg_markup: str
    blocks: list[str] = field(default_factory=list)


def _parse_byrne_rst(rst_path: Path, docsrc_dir: Path) -> ByrneProp:
    lines = rst_path.read_text(encoding="utf-8").splitlines()
    title = ""
    rubric = ""
    svg_markup = ""
    blocks: list[str] = []

    for idx, line in enumerate(lines):
        s = line.strip()
        if s.startswith(".. toctree::"):
            break
        if not s or s.startswith((":", ".. _", ".. folio::", "----")):
            continue
        if idx + 1 < len(lines) and lines[idx + 1].strip().startswith("=" * 3):
            title = s
            continue
        if s.startswith("=" * 3):
            continue
        if s.startswith(".. rubric::"):
            rubric = s[len(".. rubric::") :].strip()
            continue
        if s.startswith(".. picture::"):
            rel = s[len(".. picture::") :].strip().lstrip("/")
            svg_file = docsrc_dir / rel
            if svg_file.is_file():
                svg_txt = svg_file.read_text(encoding="utf-8")
                svg_txt = re.sub(r'\s+width="[^"]*"', "", svg_txt, count=1)
                svg_txt = re.sub(r'\s+height="[^"]*"', "", svg_txt, count=1)
                svg_txt = re.sub(
                    r"(\.geom-label\s*\{[^}]*?)stroke:\s*[^;]+;",
                    r"\1stroke: none;",
                    svg_txt,
                )
                svg_markup = svg_txt
            continue
        if s.startswith((".. container::", ":alt:", ":caption:", ":page:")):
            continue
        if s.startswith("See :ref:"):
            continue
        if line.startswith("   ") and not line.strip().startswith(":"):
            blocks.append(s)
        elif not line.startswith(" "):
            blocks.append(s)

    return ByrneProp(title=title, rubric=rubric, svg_markup=svg_markup, blocks=blocks)


_BYRNE_CSS = """
@page {
  size: 8.5in 11in;
  margin: 0.72in 0.78in 0.78in 0.78in;
  background: #fdfaf3;
  @top-center {
    content: "OLIVER BYRNE · THE FIRST SIX BOOKS OF EUCLID (1847)";
    font-family: "Fira Sans", sans-serif;
    font-size: 7.5pt;
    letter-spacing: 0.14em;
    color: #575046;
  }
  @bottom-center {
    content: counter(page);
    font-family: "Fira Sans", sans-serif;
    font-size: 8.5pt;
    color: #575046;
  }
}
@page :first { @top-center { content: none; } @bottom-center { content: none; } }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Noto Serif", "Liberation Serif", serif;
  font-size: 10.5pt;
  line-height: 1.55;
  color: #111827;
  background: #fdfaf3;
}
.byrne-title-page {
  break-after: page;
  height: 9.4in;
  border: 2pt solid #111827;
  padding: 0.6in;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: #fdfaf3;
}
.byrne-bars {
  display: flex;
  gap: 0.12in;
  height: 0.16in;
}
.bar-r { flex: 1; background: #d62828; }
.bar-y { flex: 1; background: #eab308; }
.bar-b { flex: 1; background: #1d4ed8; }
.byrne-h1 {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 32pt;
  line-height: 1.12;
  margin: 0.25in 0 0.12in 0;
}
.byrne-prop {
  break-inside: avoid;
  margin-bottom: 0.45in;
  padding-bottom: 0.25in;
  border-bottom: 1pt solid #d6cbb8;
}
.byrne-prop h2 {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 16pt;
  margin: 0 0 0.04in 0;
}
.byrne-rubric {
  font-family: "Fira Sans", sans-serif;
  font-size: 8.2pt;
  color: #6b6356;
  margin-bottom: 0.14in;
}
.byrne-plate {
  text-align: center;
  margin: 0.14in 0 0.18in 0;
  padding: 0.16in;
  border: 0.75pt solid #e5dccb;
  background: #ffffff;
}
.byrne-plate svg {
  max-width: 4.8in;
  max-height: 3.1in;
  width: auto;
  height: auto;
}
.byrne-sym {
  font-family: "DejaVu Sans", sans-serif;
  font-weight: 700;
  font-size: 1.15em;
  padding: 0 0.04em;
}
.byrne-op { font-weight: 700; font-size: 1.1em; padding-right: 0.08em; }
.just-ref { font-family: "Fira Sans", sans-serif; font-size: 0.8em; color: #6b6356; }
"""


def build_byrne_quarto_html(byrne_repo: Path, limit: int | None = None) -> str:
    """Render 8.5x11 Polychrome Fine-Color Quarto HTML for Byrne's Coloured Euclid."""
    docsrc = byrne_repo / "docsrc"
    rst_files = sorted((docsrc / "coloured_euclid").glob("book-*/*/index.rst"))
    if limit is not None:
        rst_files = rst_files[:limit]

    props = [_parse_byrne_rst(p, docsrc) for p in rst_files]
    cover_svg = props[0].svg_markup if props else ""

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8" />',
        "<title>Oliver Byrne — Polychrome Euclid (1847)</title>",
        f"<style>{_BYRNE_CSS}</style></head><body>",
        '<section class="byrne-title-page">',
        '<div><div class="byrne-bars"><div class="bar-r"></div><div class="bar-y"></div><div class="bar-b"></div></div>'
        '<h1 class="byrne-h1">The First Six Books of the Elements of Euclid</h1>'
        '<p style="font-style:italic;font-size:13pt;color:#44403c;">In which Coloured Diagrams and Symbols are used instead of Letters for the greater ease of Learners — Oliver Byrne (1847)</p></div>',
        f'<div style="text-align:center;">{cover_svg}</div>',
        '<div style="font-family:Fira Sans,sans-serif;font-size:8.5pt;letter-spacing:0.14em;text-transform:uppercase;display:flex;justify-content:space-between;"><span>GEOMETOR PRESS · FINE COLOR QUARTO</span><span>'
        + f"{len(props)} POLYCHROME PLATES</span></div></section>",
    ]

    for prop in props:
        body = "".join(f"<p>{_byrne_inline_to_html(b)}</p>" for b in prop.blocks)
        parts.append(
            f'<article class="byrne-prop"><h2>{escape(prop.title)}</h2>'
            f'<div class="byrne-rubric">{_byrne_inline_to_html(prop.rubric)}</div>'
            f'<div class="byrne-plate">{prop.svg_markup}</div>'
            f"{body}</article>"
        )

    parts.append("</body></html>")
    return "\n".join(parts)


def build_byrne_quarto_pdf(
    byrne_repo: Path,
    output_pdf: Path,
    limit: int | None = None,
) -> Path:
    """Compile Byrne's Polychrome Fine-Color Quarto PDF using WeasyPrint."""
    import weasyprint

    html_str = build_byrne_quarto_html(byrne_repo, limit=limit)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    weasyprint.HTML(string=html_str, base_url=str(byrne_repo)).write_pdf(str(output_pdf))
    return output_pdf
