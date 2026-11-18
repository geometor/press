"""Collector Card Deck PDF generator for GEOMETOR Press.

Produces print-ready duplex Tarot-format (2.75in x 4.75in) 52-card decks,
starting with 'The Golden Deck' (45 exact golden-ratio constructions + 7
geometric family key cards from geometor/divine).
"""

from __future__ import annotations

from html import escape
from pathlib import Path

from .coffee_table import (
    ConstructionEntry,
    FamilyGroup,
    load_divine_book_data,
    rst_inline_to_html,
)

_CARDS_CSS = """
@page {
  size: 2.75in 4.75in;
  margin: 0;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  padding: 0;
  font-family: "Noto Serif", "Liberation Serif", "DejaVu Serif", serif;
}

.card {
  width: 2.75in;
  height: 4.75in;
  padding: 0.16in;
  break-after: page;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}

.card-parchment {
  background: #faf7f2;
  color: #1c1917;
}

.card-obsidian {
  background: #111216;
  color: #f2efe9;
}

.card-frame {
  width: 100%;
  height: 100%;
  border: 1.2pt solid #d4af37;
  padding: 0.14in;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-obsidian .card-frame {
  border-color: #e8b85a;
  background: #15171d;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: "Fira Mono", monospace;
  font-size: 7pt;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #9a6e1c;
  border-bottom: 0.6pt solid #e5dccb;
  padding-bottom: 0.05in;
}

.card-obsidian .card-top {
  color: #e8b85a;
  border-bottom-color: #2c303c;
}

.card-svg-box {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0.07in 0;
  background: #fdfbf7;
  border: 0.5pt solid #e5dccb;
  padding: 0.04in;
}

.card-svg-box svg {
  width: 2.15in;
  height: 2.15in;
}

.card-title-front {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 11pt;
  line-height: 1.18;
  font-weight: 700;
  margin: 0.04in 0 0.04in 0;
  color: #151311;
}

.card-sub-front {
  font-family: "Fira Sans", sans-serif;
  font-size: 6.8pt;
  color: #575046;
  display: flex;
  justify-content: space-between;
  border-top: 0.6pt solid #e5dccb;
  padding-top: 0.05in;
}

.card-back-title {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 9.2pt;
  line-height: 1.15;
  font-weight: 700;
  margin: 0.05in 0;
  color: #f8f5ef;
}

.card-enun {
  font-size: 6.7pt;
  line-height: 1.32;
  font-style: italic;
  color: #d6d0c4;
  border-left: 1.5pt solid #e8b85a;
  padding-left: 0.07in;
  margin: 0.04in 0 0.06in 0;
}

.card-section-label {
  font-family: "Fira Sans", sans-serif;
  font-size: 6.2pt;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #e8b85a;
  margin: 0.04in 0 0.03in 0;
}

.card-steps {
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 6.4pt;
  line-height: 1.28;
  color: #e7e2d8;
}

.card-steps li {
  margin-bottom: 0.025in;
}

.card-step-idx {
  font-family: "Fira Mono", monospace;
  color: #e8b85a;
  font-weight: 700;
  margin-right: 0.04in;
}

.card-cert {
  width: 100%;
  border-collapse: collapse;
  font-size: 6.1pt;
  margin-top: 0.04in;
  color: #e7e2d8;
}

.card-cert th, .card-cert td {
  border-top: 0.4pt solid #2c303c;
  padding: 0.02in 0.03in;
  text-align: left;
  vertical-align: top;
}

.card-cert th {
  width: 34%;
  color: #a8a092;
  font-family: "Fira Sans", sans-serif;
}

.card-footer {
  font-family: "Fira Sans", sans-serif;
  font-size: 6pt;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #8a7f6d;
  display: flex;
  justify-content: space-between;
  border-top: 0.5pt solid #2c303c;
  padding-top: 0.04in;
}

.card-parchment .card-footer {
  border-top-color: #e5dccb;
  color: #6b6356;
}

.family-key-title {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 13.5pt;
  line-height: 1.15;
  color: #f8f5ef;
  margin: 0.06in 0 0.04in 0;
}

.family-key-sub {
  font-size: 7.4pt;
  font-style: italic;
  color: #c5bdb0;
  margin: 0 0 0.08in 0;
}

.family-list {
  margin: 0.05in 0;
  padding: 0;
  list-style: none;
  font-size: 6.9pt;
  line-height: 1.42;
  color: #292524;
}

.family-list li {
  display: flex;
  justify-content: space-between;
  border-bottom: 0.4pt solid #e5dccb;
  padding: 0.025in 0;
}

.g-token {
  font-family: "Fira Mono", monospace;
  font-weight: 600;
  color: #f3c86b;
}

.card-parchment .g-token {
  color: #78350f;
}

.euclid-graphic .geom-label {
  stroke: none !important;
  fill: #1c1917 !important;
}

.frac sup, .frac sub { font-size: 0.72em; }
"""


def _render_family_card_pair(fam: FamilyGroup, fam_idx: int) -> str:
    """Render front (obsidian) and back (parchment) for a Family Key Card."""
    fam_label = fam.code or f"GC-{fam_idx:02d}"
    emblem_svg = fam.entries[0].svg_markup if fam.entries else ""
    items_html = "".join(
        f"<li><span><strong>{escape(e.catalog_code)}</strong> {escape(e.short_title)}</span>"
        f"<span>S={e.lemoine_simplicity if e.lemoine_simplicity is not None else '—'}</span></li>"
        for e in fam.entries
    )
    front = (
        '<article class="card card-obsidian"><div class="card-frame">'
        f'<div class="card-top"><span>{escape(fam_label)} · KEY</span><span>{len(fam.entries)} PLATES</span></div>'
        '<div>'
        f'<h2 class="family-key-title">{escape(fam.title)}</h2>'
        f'<p class="family-key-sub">{escape(fam.subtitle)}</p>'
        '</div>'
        f'<div class="card-svg-box">{emblem_svg}</div>'
        '<div class="card-footer"><span>THE GOLDEN DECK</span><span>GEOMETOR PRESS</span></div>'
        '</div></article>'
    )
    back = (
        '<article class="card card-parchment"><div class="card-frame">'
        f'<div class="card-top"><span>{escape(fam_label)} · INDEX</span><span>FAMILY CARD</span></div>'
        f'<p style="font-size:6.8pt;line-height:1.35;margin:0.05in 0;">{escape(fam.description[:220])}</p>'
        f'<ul class="family-list">{items_html}</ul>'
        '<div class="card-footer"><span>45 CONSTRUCTIONS + 7 KEYS</span><span>ℚ(φ)</span></div>'
        '</div></article>'
    )
    return front + back


def _render_construction_card_pair(entry: ConstructionEntry, fam_label: str) -> str:
    """Render front (parchment plate) and back (obsidian study reverse) for a Construction Card."""
    s_badge = f"S={entry.lemoine_simplicity}" if entry.lemoine_simplicity is not None else "S=—"
    loci_badge = f"LOCI {entry.elementary_loci}" if entry.elementary_loci is not None else ""

    steps_html = "".join(
        f'<li><span class="card-step-idx">{idx:02d}</span>{rst_inline_to_html(st)}</li>'
        for idx, st in enumerate(entry.steps[:5], start=1)
    )
    cert_html = "".join(
        f"<tr><th>{rst_inline_to_html(k)}</th><td>{rst_inline_to_html(v)}</td></tr>"
        for k, v in entry.certificate[:3]
    )

    front = (
        '<article class="card card-parchment"><div class="card-frame">'
        f'<div class="card-top"><span>{escape(entry.catalog_code)}</span><span>{escape(s_badge)} · {escape(entry.number_field_text)}</span></div>'
        f'<div class="card-svg-box">{entry.svg_markup}</div>'
        '<div>'
        f'<h3 class="card-title-front">{escape(entry.short_title)}</h3>'
        f'<div class="card-sub-front"><span>{escape(fam_label)} · {escape(entry.year)}</span><span>{escape(loci_badge)}</span></div>'
        '</div>'
        '</div></article>'
    )
    back = (
        '<article class="card card-obsidian"><div class="card-frame">'
        f'<div class="card-top"><span>{escape(entry.catalog_code)} · PROOF</span><span>{escape(s_badge)}</span></div>'
        '<div>'
        f'<h4 class="card-back-title">{escape(entry.title)}</h4>'
        f'<div class="card-enun">{rst_inline_to_html(entry.enunciation)}</div>'
        '<div class="card-section-label">Steps</div>'
        f'<ol class="card-steps">{steps_html}</ol>'
        '<div class="card-section-label">Symbolic Certificate</div>'
        f'<table class="card-cert">{cert_html}</table>'
        '</div>'
        '<div class="card-footer"><span>THE GOLDEN DECK</span><span>GEOMETOR</span></div>'
        '</div></article>'
    )
    return front + back


def build_golden_deck_html(
    divine_repo: Path,
    limit: int | None = None,
) -> str:
    """Render HTML for the 52-card Golden Deck (7 family keys + 45 constructions)."""
    _, families = load_divine_book_data(divine_repo, limit=limit)

    cards_html: list[str] = []
    for fam_idx, fam in enumerate(families, start=1):
        fam_label = fam.code or f"GC-{fam_idx:02d}"
        cards_html.append(_render_family_card_pair(fam, fam_idx))
        for entry in fam.entries:
            cards_html.append(_render_construction_card_pair(entry, fam_label))

    return "\n".join(
        [
            "<!DOCTYPE html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8" />',
            "<title>The Golden Deck — 52-Card Collector &amp; Study Deck</title>",
            f"<style>{_CARDS_CSS}</style>",
            "</head>",
            "<body>",
            *cards_html,
            "</body>",
            "</html>",
        ]
    )


def build_golden_deck_pdf(
    divine_repo: Path,
    output_pdf: Path,
    limit: int | None = None,
) -> Path:
    """Compile The Golden Deck 52-card duplex PDF using WeasyPrint."""
    import weasyprint

    html_str = build_golden_deck_html(divine_repo, limit=limit)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    weasyprint.HTML(string=html_str, base_url=str(divine_repo)).write_pdf(str(output_pdf))
    return output_pdf
