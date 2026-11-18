"""Scholarly Trade Monograph (6in x 9in) PDF generator for Johannes Kepler's Geometric Works."""

from __future__ import annotations

from html import escape
from pathlib import Path
import re

from .coffee_table import latex_to_html


def _kepler_inline_to_html(text: str) -> str:
    """Convert Kepler RST prose and $...$ math into clean print HTML."""
    out = escape(text.strip())

    def _repl_dollar(m: re.Match[str]) -> str:
        raw = m.group(1).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        return f'<span class="math-inline">{latex_to_html(raw)}</span>'

    out = re.sub(r"\$([^$]+)\$", _repl_dollar, out)
    for role in ("person", "cite", "term", "ref", "doc"):
        out = re.sub(rf":{role}:`([^`<]+?)\s*&lt;[^`]+&gt;`", r"\1", out)
        out = re.sub(rf":{role}:`([^`]+)`", r"\1", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", out)
    return out


_KEPLER_CSS = """
@page {
  size: 6in 9in;
  margin: 0.72in 0.68in 0.75in 0.72in;
  @top-center {
    content: "JOHANNES KEPLER · GEOMETOR PRESS";
    font-family: "Fira Sans", sans-serif;
    font-size: 7pt;
    letter-spacing: 0.14em;
    color: #6b6356;
  }
  @bottom-center {
    content: counter(page);
    font-family: "Fira Sans", sans-serif;
    font-size: 8pt;
    color: #575046;
  }
}
@page :first { @top-center { content: none; } @bottom-center { content: none; } }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Noto Serif", "Liberation Serif", serif;
  font-size: 9.8pt;
  line-height: 1.52;
  color: #1c1917;
}
.kepler-title {
  break-after: page;
  height: 7.4in;
  border-top: 2pt solid #9a6e1c;
  border-bottom: 2pt solid #9a6e1c;
  padding: 0.5in 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.kepler-h1 {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 28pt;
  line-height: 1.12;
  margin: 0.15in 0 0.1in 0;
}
.kepler-work-head {
  font-family: "Fira Sans", sans-serif;
  font-size: 8.5pt;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #9a6e1c;
  margin-top: 0.3in;
  border-bottom: 1pt solid #9a6e1c;
  padding-bottom: 0.04in;
}
.kepler-sec h2 {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 13.5pt;
  margin: 0.12in 0 0.08in 0;
}
.kepler-fig {
  text-align: center;
  margin: 0.14in 0;
}
.kepler-fig svg {
  max-width: 3.8in;
  max-height: 2.5in;
  width: auto;
  height: auto;
}
"""


def build_kepler_trilogy_html(kepler_repo: Path, limit: int | None = None) -> str:
    """Render 6x9 Trade Monograph HTML for Kepler's three geometric works."""
    docsrc = kepler_repo / "docsrc"
    works = [
        ("Mysterium Cosmographicum (1596)", docsrc / "mysterium_cosmographicum"),
        ("Strena seu de Nive Sexangula (1611)", docsrc / "strena_sexangula"),
        ("Harmonices Mundi Libri V (1619)", docsrc / "harmonices_mundi"),
    ]

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8" />',
        "<title>Johannes Kepler — Geometric Trilogy</title>",
        f"<style>{_KEPLER_CSS}</style></head><body>",
        '<section class="kepler-title">',
        '<div><div style="font-family:Fira Sans,sans-serif;font-size:8pt;letter-spacing:0.18em;text-transform:uppercase;color:#9a6e1c;">GEOMETOR PRESS · RENAISSANCE COSMOGRAPHY</div>',
        '<h1 class="kepler-h1">The Geometric Trilogy of Johannes Kepler</h1>',
        '<p style="font-style:italic;color:#575046;">Mysterium Cosmographicum (1596) · Strena seu de Nive Sexangula (1611) · Harmonices Mundi (1619)</p></div>',
        '<div style="font-family:Fira Sans,sans-serif;font-size:8pt;letter-spacing:0.14em;text-transform:uppercase;color:#6b6356;">6″ × 9″ SCHOLARLY TRADE EDITION · ORIGINAL GEOMETOR TRANSLATION</div>',
        "</section>",
    ]

    count = 0
    for work_title, work_dir in works:
        if not work_dir.is_dir():
            continue
        en_files = sorted(work_dir.rglob("*-en.rst"))
        if not en_files:
            continue
        parts.append(f'<div class="kepler-work-head">{escape(work_title)}</div>')
        for rst in en_files:
            if limit is not None and count >= limit:
                break
            count += 1
            lines = rst.read_text(encoding="utf-8").splitlines()
            sec_title = rst.stem
            body_html: list[str] = []
            for idx, line in enumerate(lines):
                s = line.strip()
                if not s or s.startswith((":", ".. _", "=" * 3)):
                    continue
                if idx + 1 < len(lines) and lines[idx + 1].strip().startswith("=" * 3):
                    sec_title = s
                    continue
                if s.startswith(".. picture::"):
                    rel = s[len(".. picture::") :].strip().lstrip("/")
                    svg_file = docsrc / rel
                    if svg_file.is_file():
                        svg_txt = svg_file.read_text(encoding="utf-8")
                        svg_txt = re.sub(r'\s+width="[^"]*"', "", svg_txt, count=1)
                        svg_txt = re.sub(r'\s+height="[^"]*"', "", svg_txt, count=1)
                        svg_txt = re.sub(
                            r"(\.geom-label\s*\{[^}]*?)stroke:\s*[^;]+;",
                            r"\1stroke: none;",
                            svg_txt,
                        )
                        body_html.append(f'<div class="kepler-fig">{svg_txt}</div>')
                    continue
                if s.startswith((".. ", ":alt:", ":caption:")):
                    continue
                body_html.append(f"<p>{_kepler_inline_to_html(s)}</p>")
            parts.append(
                f'<article class="kepler-sec"><h2>{escape(sec_title)}</h2>{"".join(body_html)}</article>'
            )

    parts.append("</body></html>")
    return "\n".join(parts)


def build_kepler_trilogy_pdf(
    kepler_repo: Path,
    output_pdf: Path,
    limit: int | None = None,
) -> Path:
    """Compile Kepler's Geometric Trilogy 6x9 Trade PDF using WeasyPrint."""
    import weasyprint

    html_str = build_kepler_trilogy_html(kepler_repo, limit=limit)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    weasyprint.HTML(string=html_str, base_url=str(kepler_repo)).write_pdf(str(output_pdf))
    return output_pdf
