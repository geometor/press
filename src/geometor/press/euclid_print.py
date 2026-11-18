"""Scholarly Trade Codex (6in x 9in) PDF generator for Euclid's Elements."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from pathlib import Path
import re

from .coffee_table import _extract_directive_block, latex_to_html


def _euclid_inline_to_html(text: str) -> str:
    """Convert Euclid Heath RST inline roles into clean scholarly print HTML."""
    out = escape(text.strip())
    # Strip escaped footnote markers `\ [#f1]_` -> superscript `[1]`
    out = re.sub(r"\\\s*\[#f(\d+)\]_", r'<sup class="fn-mark">[\1]</sup>', out)
    out = re.sub(r"\[#f(\d+)\]_", r'<sup class="fn-mark">[\1]</sup>', out)

    def _repl_math(m: re.Match[str]) -> str:
        raw = m.group(1).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        return f'<span class="math-inline">{latex_to_html(raw)}</span>'

    out = re.sub(r":math:`([^`]+)`", _repl_math, out)
    out = re.sub(r":g:`([^`<]+?)\s*&lt;[^`]+&gt;`", r'<span class="g-token">\1</span>', out)
    out = re.sub(r":g:`([^`]+)`", r'<span class="g-token">\1</span>', out)
    out = re.sub(r":eq:`([^`<]+?)\s*&lt;[^`]+&gt;`", r'<span class="eq-token">\1</span>', out)
    out = re.sub(r":just:`([^`<]+?)\s*&lt;[^`]+&gt;`", r'<span class="just-ref">\1</span>', out)
    for role in ("term", "person", "cite", "ref"):
        out = re.sub(rf":{role}:`([^`<]+?)\s*&lt;[^`]+&gt;`", r"\1", out)
        out = re.sub(rf":{role}:`([^`]+)`", r"\1", out)

    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", out)
    return out


@dataclass
class EuclidProposition:
    """Parsed Euclid proposition for 6x9 trade print."""

    canonical_id: str
    title: str
    pages: str
    enunciation: str
    svg_markups: list[str] = field(default_factory=list)
    paragraphs: list[tuple[str, str]] = field(default_factory=list)


def _parse_proposition_rst(rst_path: Path) -> EuclidProposition:
    """Parse a single Euclid proposition index.rst file."""
    lines = rst_path.read_text(encoding="utf-8").splitlines()
    canonical_id = ""
    title = ""
    pages = ""
    enunciation = ""
    svg_markups: list[str] = []
    paragraphs: list[tuple[str, str]] = []

    i = 0
    buf: list[str] = []

    def _flush_buf() -> None:
        nonlocal buf
        txt = " ".join(x.strip() for x in buf if x.strip()).strip()
        if txt:
            paragraphs.append(("body", txt))
        buf = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith(":canonical_id:"):
            canonical_id = stripped.split(":", 2)[2].strip()
        elif stripped.startswith(":title:"):
            title = stripped.split(":", 2)[2].strip()
        elif stripped.startswith(":pages:"):
            pages = stripped.split(":", 2)[2].strip()
        elif stripped.startswith((".. _", ".. folio::", ".. toctree::", ":")):
            if stripped.startswith(".. folio::"):
                i += 1
                while i < len(lines) and (not lines[i].strip() or lines[i].startswith(("   ", "\t"))):
                    i += 1
                continue
            if stripped.startswith(".. toctree::"):
                break
        elif stripped.startswith("PROPOSITION "):
            _flush_buf()
            i += 2
            continue
        elif stripped.startswith(".. enunciation::"):
            _flush_buf()
            enunciation, i = _extract_directive_block(lines, i)
            continue
        elif stripped.startswith(".. assertion::"):
            _flush_buf()
            assertion_txt, i = _extract_directive_block(lines, i)
            if assertion_txt:
                paragraphs.append(("assertion", assertion_txt))
            continue
        elif stripped.startswith(".. qed::"):
            _flush_buf()
            qed_txt, i = _extract_directive_block(lines, i)
            if qed_txt:
                paragraphs.append(("qed", qed_txt))
            continue
        elif stripped.startswith(".. picture::"):
            _flush_buf()
            svg_name = stripped[len(".. picture::") :].strip()
            svg_file = rst_path.parent / svg_name
            if svg_file.is_file():
                svg_txt = svg_file.read_text(encoding="utf-8")
                svg_txt = re.sub(r'\s+width="[^"]*"', "", svg_txt, count=1)
                svg_txt = re.sub(r'\s+height="[^"]*"', "", svg_txt, count=1)
                svg_txt = re.sub(
                    r"(\.geom-label\s*\{[^}]*?)stroke:\s*[^;]+;",
                    r"\1stroke: none;",
                    svg_txt,
                )
                svg_markups.append(svg_txt)
            i += 1
            while i < len(lines) and lines[i].startswith(("   ", "\t")):
                i += 1
            continue
        elif stripped.startswith(".. [#f"):
            _flush_buf()
            break
        elif not stripped:
            _flush_buf()
        elif not stripped.startswith("="):
            buf.append(stripped)

        i += 1

    _flush_buf()
    return EuclidProposition(
        canonical_id=canonical_id or rst_path.parent.name,
        title=title or f"Proposition {rst_path.parent.name}",
        pages=pages,
        enunciation=enunciation,
        svg_markups=svg_markups,
        paragraphs=paragraphs,
    )


_EUCLID_TRADE_CSS = """
@page {
  size: 6in 9in;
  margin: 0.72in 0.65in 0.75in 0.75in;
  @top-center {
    content: "EUCLID'S ELEMENTS · THE HEATH EDITION";
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

@page :first {
  @top-center { content: none; }
  @bottom-center { content: none; }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: "Noto Serif", "Liberation Serif", serif;
  font-size: 9.8pt;
  line-height: 1.5;
  color: #1c1917;
}

.trade-title {
  break-after: page;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 7.4in;
  border-top: 2pt solid #9a6e1c;
  border-bottom: 2pt solid #9a6e1c;
  padding: 0.5in 0;
}

.trade-kicker {
  font-family: "Fira Sans", sans-serif;
  font-size: 8pt;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #9a6e1c;
}

.trade-h1 {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 28pt;
  line-height: 1.12;
  margin: 0.2in 0 0.1in 0;
}

.trade-sub {
  font-size: 11pt;
  font-style: italic;
  color: #575046;
}

.prop-block {
  margin-bottom: 0.35in;
  padding-bottom: 0.22in;
  border-bottom: 0.6pt solid #d6cbb8;
}

.prop-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1pt solid #9a6e1c;
  padding-bottom: 0.04in;
  margin-bottom: 0.09in;
}

.prop-title {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 13pt;
  margin: 0;
}

.prop-pages {
  font-family: "Fira Mono", monospace;
  font-size: 7.5pt;
  color: #78716c;
}

.prop-enun {
  background: #f5f0e6;
  border-left: 2pt solid #9a6e1c;
  padding: 0.08in 0.12in;
  font-style: italic;
  margin: 0 0 0.1in 0;
}

.prop-figure {
  text-align: center;
  margin: 0.1in 0;
}

.prop-figure svg {
  max-width: 3.4in;
  max-height: 2.3in;
  width: auto;
  height: auto;
}

.prop-assertion {
  margin: 0.06in 0 0.06in 0.18in;
  font-weight: 500;
}

.g-token {
  font-family: "Fira Mono", monospace;
  font-size: 0.9em;
  color: #78350f;
  font-weight: 600;
}

.just-ref {
  font-family: "Fira Sans", sans-serif;
  font-size: 0.85em;
  color: #6b6356;
}

.fn-mark {
  font-size: 0.7em;
  color: #78716c;
}
"""


def build_euclid_trade_html(
    euclid_repo: Path,
    volume: str = "volume_I",
    book: str = "book_i",
    limit: int | None = None,
) -> str:
    """Render 6x9 Scholarly Trade Codex HTML for a Book of Euclid's Elements."""
    props_dir = euclid_repo / "docsrc" / "heath" / volume / book / "propositions"
    rst_files = sorted(props_dir.glob("*/index.rst"))
    if limit is not None:
        rst_files = rst_files[:limit]

    props = [_parse_proposition_rst(p) for p in rst_files]
    book_label = book.replace("_", " ").title()

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8" />',
        f"<title>Euclid's Elements — {escape(book_label)}</title>",
        f"<style>{_EUCLID_TRADE_CSS}</style></head><body>",
        '<section class="trade-title">',
        '<div><div class="trade-kicker">GEOMETOR PRESS · CLASSICAL CANON</div>',
        '<h1 class="trade-h1">The Thirteen Books of Euclid’s Elements</h1>',
        f'<p class="trade-sub">Sir Thomas L. Heath Edition · {escape(book_label)} ({len(props)} Propositions)</p></div>',
        '<div class="trade-kicker">6″ × 9″ TRADE CODEX · CALIBRATED VECTOR PLATES</div>',
        "</section>",
    ]

    for prop in props:
        figs = "".join(f'<div class="prop-figure">{svg}</div>' for svg in prop.svg_markups)
        body_html = "".join(
            f'<p class="prop-assertion">{_euclid_inline_to_html(txt)}</p>'
            if kind == "assertion"
            else f'<p style="font-style:italic;text-align:right;color:#575046;">{_euclid_inline_to_html(txt)}</p>'
            if kind == "qed"
            else f"<p>{_euclid_inline_to_html(txt)}</p>"
            for kind, txt in prop.paragraphs
        )
        pg_label = f"Heath pp. {prop.pages}" if prop.pages else prop.canonical_id
        parts.append(
            f'<article class="prop-block">'
            f'<div class="prop-head"><h2 class="prop-title">{escape(prop.title)}</h2>'
            f'<span class="prop-pages">{escape(pg_label)}</span></div>'
            f'<div class="prop-enun">{_euclid_inline_to_html(prop.enunciation)}</div>'
            f"{figs}{body_html}</article>"
        )

    parts.append("</body></html>")
    return "\n".join(parts)


def build_euclid_trade_pdf(
    euclid_repo: Path,
    output_pdf: Path,
    volume: str = "volume_I",
    book: str = "book_i",
    limit: int | None = None,
) -> Path:
    """Compile a 6x9 Scholarly Trade Codex PDF for Euclid's Elements."""
    import weasyprint

    html_str = build_euclid_trade_html(euclid_repo, volume=volume, book=book, limit=limit)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    weasyprint.HTML(string=html_str, base_url=str(euclid_repo)).write_pdf(str(output_pdf))
    return output_pdf
