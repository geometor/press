"""Coffee Table Book & Print PDF generator for GEOMETOR Press.

Produces facing-page spread PDFs (verso: enunciation, steps, proof, and
machine-verified symbolic certificate; recto: full-bleed vector SVG plate)
using WeasyPrint CSS Paged Media.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
import json
from pathlib import Path
import re
from typing import Any


_SUPERSCRIPTS = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "+": "⁺",
    "-": "⁻",
    "n": "ⁿ",
}


def latex_to_html(expr: str) -> str:
    """Convert inline LaTeX math expressions into clean typographic HTML."""
    s = expr.strip()
    replacements = [
        (r"\mathbb{Q}", "ℚ"),
        (r"\mathbb{R}", "ℝ"),
        (r"\mathbb{Z}", "ℤ"),
        (r"\mathbb{N}", "ℕ"),
        (r"\phi", "φ"),
        (r"\varphi", "φ"),
        (r"\pi", "π"),
        (r"\theta", "θ"),
        (r"\alpha", "α"),
        (r"\beta", "β"),
        (r"\gamma", "γ"),
        (r"\delta", "δ"),
        (r"\sigma", "σ"),
        (r"\triangle", "△"),
        (r"\angle", "∠"),
        (r"\perp", "⊥"),
        (r"\parallel", "∥"),
        (r"\cong", "≅"),
        (r"\sim", "∼"),
        (r"\approx", "≈"),
        (r"\neq", "≠"),
        (r"\leq", "≤"),
        (r"\geq", "≥"),
        (r"\le", "≤"),
        (r"\ge", "≥"),
        (r"\cdot", "·"),
        (r"\times", "×"),
        (r"\pm", "±"),
        (r"\mp", "∓"),
        (r"\infty", "∞"),
        (r"^\circ", "°"),
        (r"\circ", "°"),
        (r"\quad", " "),
        (r"\,", " "),
        (r"\;", " "),
        (r"\:", " "),
        (r"\!", ""),
    ]
    for old, new in replacements:
        s = s.replace(old, new)

    # \text{...} and \mathrm{...}
    s = re.sub(r"\\(?:text|mathrm|operatorname)\{([^{}]*)\}", r"\1", s)

    # \sqrt{x} -> √(x) or √x (use a marker or run after \frac; handle \frac/\tfrac first!)
    def _replace_fracs(text: str) -> str:
        pattern = re.compile(r"\\(?:t|d)?frac\b")
        out_parts: list[str] = []
        pos = 0
        while True:
            m = pattern.search(text, pos)
            if not m:
                out_parts.append(text[pos:])
                break
            out_parts.append(text[pos : m.start()])
            cur = m.end()
            while cur < len(text) and text[cur].isspace():
                cur += 1
            args: list[str] = []
            for _ in range(2):
                if cur < len(text) and text[cur] == "{":
                    depth = 1
                    start = cur + 1
                    cur += 1
                    while cur < len(text) and depth > 0:
                        if text[cur] == "{":
                            depth += 1
                        elif text[cur] == "}":
                            depth -= 1
                        cur += 1
                    args.append(text[start : cur - 1])
                elif cur < len(text):
                    args.append(text[cur])
                    cur += 1
            if len(args) == 2:
                out_parts.append(
                    f'<span class="frac"><sup>{args[0]}</sup>⁄<sub>{args[1]}</sub></span>'
                )
            else:
                out_parts.append(m.group(0))
            pos = cur
        return "".join(out_parts)

    for _ in range(3):
        s = _replace_fracs(s)

    # \sqrt{x} -> √(x) or √x
    s = re.sub(
        r"\\sqrt\{([^{}]+)\}",
        lambda m: f"√{m.group(1)}" if len(m.group(1)) <= 2 else f"√({m.group(1)})",
        s,
    )

    # \overline{AB} -> AB̄ (simple span with overline)
    s = re.sub(
        r"\\overline\{([^{}]+)\}",
        lambda m: f'<span class="overline">{m.group(1)}</span>',
        s,
    )

    # Exponents: ^{...} and ^2
    s = re.sub(r"\^\{([^{}]+)\}", lambda m: f"<sup>{m.group(1)}</sup>", s)
    s = re.sub(
        r"\^([0-9n])",
        lambda m: _SUPERSCRIPTS.get(m.group(1), f"<sup>{m.group(1)}</sup>"),
        s,
    )

    # Subscripts: _{...} and _i
    s = re.sub(r"_\{([^{}]+)\}", lambda m: f"<sub>{m.group(1)}</sub>", s)
    s = re.sub(r"_([A-Za-z0-9])", lambda m: f"<sub>{m.group(1)}</sub>", s)

    # Clean remaining simple braces
    s = s.replace(r"\{", "{").replace(r"\}", "}")
    s = re.sub(r"(?<!\\)[{}]", "", s)
    return s


def rst_inline_to_html(text: str) -> str:
    """Convert RST inline roles (:g:, :math:, :person:, :term:, etc.) to HTML."""
    out = escape(text.strip())

    # Restore :math:`...`
    def _repl_math(m: re.Match[str]) -> str:
        raw = m.group(1).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        return f'<span class="math-inline">{latex_to_html(raw)}</span>'

    out = re.sub(r":math:`([^`]+)`", _repl_math, out)
    out = re.sub(r":g:`([^`]+)`", r'<span class="g-token">\1</span>', out)
    out = re.sub(r":mod:`([^`]+)`", r"<code>\1</code>", out)

    for role in ("person", "term", "cite", "ref"):
        out = re.sub(
            rf":{role}:`([^`<]+?)\s*&lt;[^`]+&gt;`",
            r'<span class="scholar-ref">\1</span>',
            out,
        )
        out = re.sub(rf":{role}:`([^`]+)`", r'<span class="scholar-ref">\1</span>', out)

    # External RST links `Label <url>`_
    out = re.sub(r"`([^`<]+?)\s*&lt;https?://[^`]+&gt;`_+", r"\1", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", out)
    out = re.sub(r"``([^`]+)``", r"<code>\1</code>", out)
    return out


@dataclass
class ConstructionEntry:
    """Parsed construction record for the Coffee Table Book."""

    catalog_code: str
    slug: str
    family_slug: str
    title: str
    short_title: str
    discoverer_line: str
    enunciation: str
    given: str
    steps: list[str]
    proof: str
    certificate: list[tuple[str, str]]
    svg_markup: str
    number_field_text: str
    elementary_loci: int | None
    lemoine_simplicity: int | None
    year: str


@dataclass
class FamilyGroup:
    """Family chapter grouping constructions."""

    code: str
    slug: str
    title: str
    subtitle: str
    description: str
    entries: list[ConstructionEntry] = field(default_factory=list)


def _extract_directive_block(lines: list[str], start_idx: int) -> tuple[str, int]:
    """Extract an indented RST directive body starting after `.. directive::`."""
    body: list[str] = []
    i = start_idx + 1
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            if body:
                body.append("")
            i += 1
            continue
        if line.startswith(("   ", "\t")):
            stripped = line.strip()
            if not stripped.startswith(":"):
                body.append(stripped)
            i += 1
        else:
            break
    text = " ".join(part for part in body if part).strip()
    return text, i


def _parse_construction_rst(
    rst_path: Path,
    manifest_item: dict[str, Any],
    repo_root: Path,
) -> ConstructionEntry:
    """Parse a single divine construction index.rst and its SVG plate."""
    raw = rst_path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    discoverer_line = ""
    enunciation = ""
    given = ""
    steps: list[str] = []
    proof_lines: list[str] = []
    certificate: list[tuple[str, str]] = []

    section = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("**Discoverer(s)**"):
            discoverer_line = stripped
        elif stripped.startswith(".. enunciation::"):
            enunciation, i = _extract_directive_block(lines, i)
            continue
        elif stripped.startswith(".. step::"):
            step_txt, i = _extract_directive_block(lines, i)
            if step_txt:
                steps.append(step_txt)
            continue
        elif stripped.startswith("**Given**:"):
            given = stripped[len("**Given**:") :].strip()
        elif stripped == "Exact Symbolic Proof & Certificate":
            section = "proof"
            i += 2
            continue
        elif stripped in ("Automated Divine Scan", "Historical Commentary & Attribution"):
            section = ""
        elif stripped.startswith(".. list-table::"):
            section = "table"
            i += 1
            continue
        elif section == "proof" and stripped and not stripped.startswith("-"):
            proof_lines.append(stripped)
        elif section == "table":
            if stripped.startswith("* - "):
                key = stripped[4:].strip()
                val = ""
                if i + 1 < len(lines) and lines[i + 1].strip().startswith("- "):
                    val = lines[i + 1].strip()[2:].strip()
                    i += 1
                if key.lower() != "invariant":
                    certificate.append((key, val))
            elif stripped and not stripped.startswith((":", "* ", "- ")):
                section = ""

        i += 1

    svg_rel = str(manifest_item.get("svg_path") or "")
    svg_file = repo_root / svg_rel if svg_rel else rst_path.parent / f"{manifest_item['slug']}.svg"
    svg_markup = ""
    if svg_file.is_file():
        svg_markup = svg_file.read_text(encoding="utf-8")
        # Ensure responsive scaling inside print frame
        svg_markup = re.sub(r'\s+width="[^"]*"', "", svg_markup, count=1)
        svg_markup = re.sub(r'\s+height="[^"]*"', "", svg_markup, count=1)
        svg_markup = re.sub(
            r"(\.geom-label\s*\{[^}]*?)stroke:\s*[^;]+;",
            r"\1stroke: none;",
            svg_markup,
        )

    return ConstructionEntry(
        catalog_code=str(manifest_item.get("catalog_code") or ""),
        slug=str(manifest_item.get("slug") or ""),
        family_slug=str(manifest_item.get("family_slug") or ""),
        title=str(manifest_item.get("title") or ""),
        short_title=str(manifest_item.get("short_title") or ""),
        discoverer_line=discoverer_line,
        enunciation=enunciation,
        given=given,
        steps=steps,
        proof=" ".join(proof_lines),
        certificate=certificate,
        svg_markup=svg_markup,
        number_field_text=str(manifest_item.get("number_field_text") or "ℚ(φ)"),
        elementary_loci=manifest_item.get("elementary_loci"),
        lemoine_simplicity=manifest_item.get("lemoine_simplicity"),
        year=str(manifest_item.get("year") or ""),
    )


def load_divine_book_data(
    divine_repo: Path,
    limit: int | None = None,
) -> tuple[dict[str, Any], list[FamilyGroup]]:
    """Load families and parsed constructions from `geometor/divine`."""
    manifest_path = divine_repo / "resources" / "catalog_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    families_by_slug: dict[str, FamilyGroup] = {}
    families: list[FamilyGroup] = []
    for fam in manifest.get("families", []):
        fg = FamilyGroup(
            code=str(fam.get("code") or ""),
            slug=str(fam.get("slug") or ""),
            title=str(fam.get("title") or ""),
            subtitle=str(fam.get("subtitle") or ""),
            description=str(fam.get("description") or ""),
        )
        families_by_slug[fg.slug] = fg
        families.append(fg)

    items = manifest.get("constructions", [])
    if limit is not None:
        items = items[:limit]

    for item in items:
        fslug = str(item.get("family_slug") or "")
        slug = str(item.get("slug") or "")
        rst_path = divine_repo / "docsrc" / "constructions" / fslug / slug / "index.rst"
        if not rst_path.is_file():
            continue
        entry = _parse_construction_rst(rst_path, item, divine_repo)
        if fslug in families_by_slug:
            families_by_slug[fslug].entries.append(entry)

    families = [f for f in families if f.entries]
    return manifest, families


_COFFEE_TABLE_CSS = """
@page {
  size: 10in 10in;
  margin: 0.72in 0.78in 0.78in 0.78in;
  background: #faf7f2;
  @bottom-center {
    content: counter(page);
    font-family: "Fira Sans", sans-serif;
    font-size: 8.5pt;
    color: #6b6356;
    letter-spacing: 0.08em;
  }
}

@page :first {
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-center { content: none; }
}

@page front {
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-center { content: none; }
}

@page recto_plate {
  margin: 0.55in 0.65in 0.65in 0.55in;
  @top-right {
    content: "GOLDEN CONSTRUCTIONS · PLATES";
    font-family: "Fira Sans", sans-serif;
    font-size: 7.5pt;
    letter-spacing: 0.14em;
    color: #8a7f6d;
  }
  @bottom-center {
    content: counter(page);
    font-family: "Fira Sans", sans-serif;
    font-size: 8.5pt;
    color: #6b6356;
  }
}

@page verso_text {
  margin: 0.68in 0.68in 0.72in 0.78in;
  @top-left {
    content: "GEOMETOR PRESS · DIVINE PROPORTION";
    font-family: "Fira Sans", sans-serif;
    font-size: 7.5pt;
    letter-spacing: 0.14em;
    color: #8a7f6d;
  }
  @bottom-center {
    content: counter(page);
    font-family: "Fira Sans", sans-serif;
    font-size: 8.5pt;
    color: #6b6356;
  }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  padding: 0;
  font-family: "Noto Serif", "Liberation Serif", "DejaVu Serif", serif;
  font-size: 9.6pt;
  line-height: 1.48;
  color: #1c1917;
  background: #faf7f2;
}

.title-page {
  page: front;
  break-after: page;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 8.4in;
  border: 1.5pt solid #d4af37;
  padding: 0.55in;
  background: #fdfbf7;
}

.title-kicker {
  font-family: "Fira Sans", sans-serif;
  font-size: 8.5pt;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #9a6e1c;
}

.title-main {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 36pt;
  line-height: 1.1;
  font-weight: 700;
  margin: 0.15in 0 0.1in 0;
  color: #151311;
}

.title-sub {
  font-size: 13pt;
  font-style: italic;
  color: #575046;
  margin: 0 0 0.25in 0;
}

.title-emblem {
  width: 100%;
  height: 4.1in;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 0.75pt solid #e5dccb;
  border-bottom: 0.75pt solid #e5dccb;
  padding: 0.15in 0;
}

.title-emblem svg {
  width: 5.2in;
  height: 3.6in;
}

.euclid-graphic .geom-label {
  stroke: none !important;
  fill: #1c1917 !important;
}

.title-imprint {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  font-family: "Fira Sans", sans-serif;
  font-size: 8.5pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #575046;
}

.colophon-page, .toc-page, .index-page {
  page: front;
  break-after: page;
}

.colophon-box {
  margin-top: 2.2in;
  border-left: 2pt solid #d4af37;
  padding-left: 0.28in;
  max-width: 6.2in;
}

.colophon-box h2, .toc-page h2, .index-page h2 {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 20pt;
  margin: 0 0 0.18in 0;
  color: #151311;
}

.toc-family {
  margin-bottom: 0.16in;
  padding-bottom: 0.1in;
  border-bottom: 0.5pt solid #e5dccb;
}

.toc-family-head {
  font-family: "Fira Sans", sans-serif;
  font-weight: 700;
  font-size: 9.5pt;
  color: #9a6e1c;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.toc-items {
  font-size: 8.5pt;
  color: #44403c;
  margin-top: 0.04in;
  line-height: 1.45;
}

.family-opener {
  page: recto_plate;
  break-before: right;
  break-after: page;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 8.5in;
  padding: 0.5in;
  border: 1pt solid #e5dccb;
  background: #fdfbf7;
}

.family-code {
  font-family: "Fira Mono", monospace;
  font-size: 11pt;
  letter-spacing: 0.2em;
  color: #9a6e1c;
  margin-bottom: 0.12in;
}

.family-title {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 28pt;
  line-height: 1.15;
  margin: 0 0 0.14in 0;
  color: #151311;
}

.family-subtitle {
  font-size: 12pt;
  font-style: italic;
  color: #575046;
  margin: 0 0 0.24in 0;
}

.family-desc {
  font-size: 10.5pt;
  line-height: 1.6;
  color: #292524;
  max-width: 6.8in;
  border-top: 1pt solid #d4af37;
  padding-top: 0.2in;
}

.spread-verso {
  page: verso_text;
  break-before: left;
  break-after: page;
}

.spread-recto {
  page: recto_plate;
  break-before: right;
  break-after: page;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 8.65in;
}

.entry-header {
  border-bottom: 1.2pt solid #d4af37;
  padding-bottom: 0.1in;
  margin-bottom: 0.12in;
}

.entry-code-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: "Fira Sans", sans-serif;
  font-size: 8pt;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #9a6e1c;
  margin-bottom: 0.04in;
}

.entry-title {
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 16.5pt;
  line-height: 1.18;
  margin: 0 0 0.06in 0;
  color: #151311;
}

.entry-meta {
  font-family: "Fira Sans", sans-serif;
  font-size: 8pt;
  color: #575046;
}

.enunciation-box {
  background: #f3ede2;
  border-left: 2.5pt solid #d4af37;
  padding: 0.1in 0.14in;
  margin: 0 0 0.12in 0;
  font-style: italic;
  font-size: 9.2pt;
  line-height: 1.42;
}

.subhead {
  font-family: "Fira Sans", sans-serif;
  font-size: 8pt;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #78350f;
  margin: 0.1in 0 0.05in 0;
}

.given-line {
  font-size: 8.9pt;
  margin: 0 0 0.07in 0;
}

.steps-list {
  margin: 0 0 0.1in 0;
  padding-left: 0;
  list-style: none;
}

.steps-list li {
  display: flex;
  gap: 0.09in;
  font-size: 8.8pt;
  line-height: 1.38;
  margin-bottom: 0.045in;
}

.step-num {
  font-family: "Fira Mono", monospace;
  font-size: 7.8pt;
  font-weight: 700;
  color: #9a6e1c;
  min-width: 0.22in;
  padding-top: 0.01in;
}

.proof-text {
  font-size: 8.7pt;
  line-height: 1.4;
  margin: 0 0 0.1in 0;
  color: #292524;
}

.cert-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 8pt;
  margin-top: 0.04in;
}

.cert-table th, .cert-table td {
  border-top: 0.5pt solid #d6cbb8;
  border-bottom: 0.5pt solid #d6cbb8;
  padding: 0.035in 0.06in;
  text-align: left;
  vertical-align: top;
}

.cert-table th {
  width: 28%;
  font-family: "Fira Sans", sans-serif;
  font-weight: 600;
  color: #575046;
}

.plate-frame {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 0.75pt solid #e5dccb;
  background: #fdfbf7;
  padding: 0.22in;
  margin-bottom: 0.14in;
}

.plate-frame svg {
  width: 100%;
  height: auto;
  max-height: 7.3in;
}

.plate-footer {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-top: 0.75pt solid #d4af37;
  padding-top: 0.08in;
  font-family: "Fira Sans", sans-serif;
  font-size: 8.2pt;
  color: #44403c;
}

.plate-num {
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #9a6e1c;
}

.g-token {
  font-family: "Fira Mono", monospace;
  font-weight: 600;
  font-size: 0.92em;
  color: #78350f;
}

.math-inline {
  font-family: "DejaVu Math TeX Gyre", "Noto Serif", serif;
}

.frac sup, .frac sub {
  font-size: 0.72em;
}

.overline {
  text-decoration: overline;
}

.index-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 7.8pt;
}

.index-table th, .index-table td {
  border-bottom: 0.4pt solid #e5dccb;
  padding: 0.03in 0.05in;
  text-align: left;
}

.index-table th {
  font-family: "Fira Sans", sans-serif;
  font-weight: 700;
  color: #78350f;
  border-bottom: 1pt solid #d4af37;
}
"""


def build_divine_coffee_table_html(
    divine_repo: Path,
    limit: int | None = None,
) -> str:
    """Render complete HTML document for the Divine Coffee Table Book."""
    _, families = load_divine_book_data(divine_repo, limit=limit)
    all_entries = [e for f in families for e in f.entries]
    cover_svg = all_entries[0].svg_markup if all_entries else ""

    parts: list[str] = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8" />',
        "<title>Golden Constructions — 45 Exact Pathways to φ</title>",
        f"<style>{_COFFEE_TABLE_CSS}</style>",
        "</head>",
        "<body>",
        '<section class="title-page">',
        '<div><div class="title-kicker">GEOMETOR PRESS · MONOGRAPH SERIES</div>',
        '<h1 class="title-main">Golden Constructions</h1>',
        '<p class="title-sub">Exact Symbolic Pathways to the Divine Proportion φ = (1 + √5) / 2</p></div>',
        f'<div class="title-emblem">{cover_svg}</div>',
        '<div class="title-imprint"><span>45 Machine-Verified Plates</span><span>GEOMETOR · SymPy Exact Algebra</span></div>',
        "</section>",
        '<section class="colophon-page"><div class="colophon-box">',
        "<h2>Colophon &amp; Exact Precision</h2>",
        "<p>Every geometric locus in this volume is modeled in exact symbolic algebra over ℚ(φ) and closed-form radical extensions via <code>geometor.model</code> and verified by <code>geometor.divine</code>. No floating-point approximations enter any construction or plate.</p>",
        "<p><strong>Imprint:</strong> GEOMETOR Press<br/><strong>Edition:</strong> Collector Coffee Table Edition (10″ × 10″ Facing-Page Spreads)<br/><strong>Complexity Metric:</strong> Émile Lemoine’s <em>Géométrographie</em> Simplicity <em>S</em></p>",
        "</div></section>",
        '<section class="toc-page"><h2>Catalog of Seven Families</h2>',
    ]

    for fam in families:
        codes = ", ".join(f"{e.catalog_code} {e.short_title}" for e in fam.entries)
        parts.append(
            f'<div class="toc-family"><div class="toc-family-head">{escape(fam.code)} · {escape(fam.title)} ({len(fam.entries)})</div>'
            f'<div class="toc-items">{escape(codes)}</div></div>'
        )
    parts.append("</section>")

    plate_idx = 0
    for fam in families:
        parts.append(
            f'<section class="family-opener">'
            f'<div class="family-code">{escape(fam.code)} · {len(fam.entries)} CONSTRUCTIONS</div>'
            f'<h2 class="family-title">{escape(fam.title)}</h2>'
            f'<p class="family-subtitle">{escape(fam.subtitle)}</p>'
            f'<p class="family-desc">{escape(fam.description)}</p>'
            f"</section>"
        )

        for entry in fam.entries:
            plate_idx += 1
            loci_str = (
                f"Loci: {entry.elementary_loci} · Lemoine S = {entry.lemoine_simplicity}"
                if entry.lemoine_simplicity is not None
                else ""
            )
            steps_html = "".join(
                f'<li><span class="step-num">{idx:02d}</span><span>{rst_inline_to_html(st)}</span></li>'
                for idx, st in enumerate(entry.steps, start=1)
            )
            cert_html = "".join(
                f"<tr><th>{rst_inline_to_html(k)}</th><td>{rst_inline_to_html(v)}</td></tr>"
                for k, v in entry.certificate[:5]
            )
            parts.append(
                f'<article class="spread-verso">'
                f'<div class="entry-header">'
                f'<div class="entry-code-row"><span>{escape(entry.catalog_code)} · {escape(fam.title)}</span><span>{escape(entry.number_field_text)} · {escape(loci_str)}</span></div>'
                f'<h3 class="entry-title">{escape(entry.title)}</h3>'
                f'<div class="entry-meta">{rst_inline_to_html(entry.discoverer_line)}</div>'
                f"</div>"
                f'<div class="enunciation-box">{rst_inline_to_html(entry.enunciation)}</div>'
                f'<div class="subhead">Given &amp; Constructive Steps</div>'
                f'<p class="given-line"><strong>Given:</strong> {rst_inline_to_html(entry.given)}</p>'
                f'<ol class="steps-list">{steps_html}</ol>'
                f'<div class="subhead">Exact Symbolic Proof &amp; Certificate</div>'
                f'<p class="proof-text">{rst_inline_to_html(entry.proof)}</p>'
                f'<table class="cert-table">{cert_html}</table>'
                f"</article>"
            )
            parts.append(
                f'<section class="spread-recto">'
                f'<div class="plate-frame">{entry.svg_markup}</div>'
                f'<div class="plate-footer">'
                f'<span class="plate-num">Plate {plate_idx:02d} · {escape(entry.catalog_code)}</span>'
                f'<span>{escape(entry.short_title)} · {escape(entry.year)}</span>'
                f"</div>"
                f"</section>"
            )

    parts.append('<section class="index-page"><h2>Comparative Lemoine Index</h2><table class="index-table">')
    parts.append("<tr><th>Code</th><th>Construction</th><th>Field</th><th>Loci</th><th>Lemoine S</th></tr>")
    for entry in sorted(all_entries, key=lambda x: (x.lemoine_simplicity or 999, x.catalog_code)):
        parts.append(
            f"<tr><td>{escape(entry.catalog_code)}</td><td>{escape(entry.short_title)}</td>"
            f"<td>{escape(entry.number_field_text)}</td>"
            f"<td>{entry.elementary_loci if entry.elementary_loci is not None else '—'}</td>"
            f"<td>{entry.lemoine_simplicity if entry.lemoine_simplicity is not None else '—'}</td></tr>"
        )
    parts.append("</table></section></body></html>")
    return "\n".join(parts)


def build_divine_coffee_table_pdf(
    divine_repo: Path,
    output_pdf: Path,
    limit: int | None = None,
) -> Path:
    """Compile the Divine Coffee Table Book PDF using WeasyPrint."""
    import weasyprint

    html_str = build_divine_coffee_table_html(divine_repo, limit=limit)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    weasyprint.HTML(string=html_str, base_url=str(divine_repo)).write_pdf(str(output_pdf))
    return output_pdf


def build_divine_cover_html(
    divine_repo: Path,
    spine_width_in: float = 0.42,
    wrap_margin_in: float = 0.625,
) -> str:
    """Render full-bleed hardcover wrap cover HTML for Golden Constructions."""
    _, families = load_divine_book_data(divine_repo, limit=1)
    emblem_svg = families[0].entries[0].svg_markup if families and families[0].entries else ""
    # Adapt SVG strokes/labels for dark obsidian wrap cover
    emblem_svg = emblem_svg.replace("fill: #1c1917", "fill: #f2efe9")
    emblem_svg = emblem_svg.replace("stroke: #334155", "stroke: #94a3b8")
    emblem_svg = emblem_svg.replace("stroke: #475569", "stroke: #94a3b8")
    emblem_svg = emblem_svg.replace("fill: #0f172a", "fill: #f8fafc")

    total_w = 20.0 + spine_width_in + 2.0 * wrap_margin_in
    total_h = 10.0 + 2.0 * wrap_margin_in

    cover_css = f"""
@page {{
  size: {total_w:.3f}in {total_h:.3f}in;
  margin: 0;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  padding: 0;
  width: {total_w:.3f}in;
  height: {total_h:.3f}in;
  background: #0c0d10;
  color: #f2efe9;
  font-family: "Noto Serif", "Liberation Serif", serif;
}}
.wrap-canvas {{
  display: flex;
  width: {total_w:.3f}in;
  height: {total_h:.3f}in;
  padding: {wrap_margin_in:.3f}in;
}}
.panel-back, .panel-front {{
  width: 10in;
  height: 10in;
  padding: 0.72in;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.panel-frame {{
  width: 100%;
  height: 100%;
  border: 1.5pt solid #e8b85a;
  padding: 0.55in;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: #111318;
}}
.panel-spine {{
  width: {spine_width_in:.3f}in;
  height: 10in;
  display: flex;
  align-items: center;
  justify-content: center;
  border-left: 0.4pt dashed #2c313d;
  border-right: 0.4pt dashed #2c313d;
}}
.spine-text {{
  transform: rotate(-90deg);
  font-family: "Fira Sans", sans-serif;
  font-size: 8.5pt;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #e8b85a;
  white-space: nowrap;
}}
.kicker {{
  font-family: "Fira Sans", sans-serif;
  font-size: 8.5pt;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #e8b85a;
}}
.cover-title {{
  font-family: "Noto Serif Display", "Noto Serif", serif;
  font-size: 38pt;
  line-height: 1.08;
  margin: 0.14in 0 0.1in 0;
  color: #faf7f2;
}}
.cover-sub {{
  font-size: 13pt;
  font-style: italic;
  color: #c5bdb0;
  margin: 0;
}}
.cover-emblem {{
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 0.6pt solid #2c313d;
  border-bottom: 0.6pt solid #2c313d;
  padding: 0.2in 0;
}}
.cover-emblem svg {{
  width: 5.2in;
  height: 3.6in;
}}
.cover-foot {{
  display: flex;
  justify-content: space-between;
  font-family: "Fira Sans", sans-serif;
  font-size: 8.5pt;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #c5bdb0;
}}
.back-blurb {{
  font-size: 10.5pt;
  line-height: 1.62;
  color: #e7e2d8;
}}
.back-families {{
  font-family: "Fira Sans", sans-serif;
  font-size: 8.5pt;
  line-height: 1.75;
  color: #c5bdb0;
  border-left: 2pt solid #e8b85a;
  padding-left: 0.2in;
}}
.barcode-box {{
  width: 2in;
  height: 1.15in;
  border: 0.75pt solid #4b5563;
  background: #faf7f2;
  color: #1c1917;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Fira Mono", monospace;
  font-size: 7.5pt;
}}
"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8" /><title>Golden Constructions — Wrap Cover</title><style>{cover_css}</style></head>
<body>
<div class="wrap-canvas">
  <section class="panel-back"><div class="panel-frame">
    <div>
      <div class="kicker">GEOMETOR PRESS · MONOGRAPH SERIES</div>
      <p class="back-blurb"><strong>Golden Constructions</strong> gathers 45 classical and modern compass-and-straightedge constructions of the divine proportion φ = (1 + √5)/2—each modeled in exact symbolic algebra over ℚ(φ), scored by Émile Lemoine’s <em>Géométrographie</em>, and paired with a full-bleed vector plate.</p>
    </div>
    <div class="back-families">
      GC-01 · Classical &amp; Minimal-Step Compass (7)<br/>
      GC-02 · Equilateral Triangles &amp; Regular Hexagons (7)<br/>
      GC-03 · Squares, Lattice Grids &amp; Golden Crosses (8)<br/>
      GC-04 · Right Triangles, Egyptian 3–4–5 &amp; Kepler (4)<br/>
      GC-05 · Pentagons, Pentagrams &amp; Stars (6)<br/>
      GC-06 · Circles, Apollonian Windows &amp; Sangaku (7)<br/>
      GC-07 · Rhombi, Trapezoids &amp; Dissections (6)
    </div>
    <div style="display:flex;justify-content:space-between;align-items:flex-end;">
      <div class="cover-foot"><span>MATHEMATICS · GEOMETRY</span></div>
      <div class="barcode-box">ISBN / BARCODE AREA</div>
    </div>
  </div></section>
  <section class="panel-spine"><div class="spine-text">GOLDEN CONSTRUCTIONS &nbsp;·&nbsp; GEOMETOR PRESS</div></section>
  <section class="panel-front"><div class="panel-frame">
    <div>
      <div class="kicker">GEOMETOR PRESS · COLLECTOR EDITION</div>
      <h1 class="cover-title">Golden Constructions</h1>
      <p class="cover-sub">45 Exact Symbolic Pathways to the Divine Proportion φ</p>
    </div>
    <div class="cover-emblem">{emblem_svg}</div>
    <div class="cover-foot"><span>45 MACHINE-VERIFIED PLATES</span><span>SYMPY EXACT ALGEBRA · ℚ(φ)</span></div>
  </div></section>
</div>
</body></html>"""


def build_divine_cover_pdf(
    divine_repo: Path,
    output_pdf: Path,
    spine_width_in: float = 0.42,
) -> Path:
    """Compile the hardcover wrap cover PDF for Golden Constructions."""
    import weasyprint

    html_str = build_divine_cover_html(divine_repo, spine_width_in=spine_width_in)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    weasyprint.HTML(string=html_str, base_url=str(divine_repo)).write_pdf(str(output_pdf))
    return output_pdf

