# GEOMETOR Press — Roadmap

## Phase 1: Foundation & Visual Lookbook (v0.1.0 — Completed)

- Establish **GEOMETOR Press** brand identity, colophon (*Vesica-to-$\phi$*), and five mineral-coded Spine Series (*Fontes Geometrici*, *Bibliotheca Noetica*, *Synthesis & Constructio*, *Morphogenesis & Natura*, *Instrumenta & Machina*).
- Conduct full 47-repository workspace census (`71,900+` SVGs, `2,377` archival folios, `44+` distinct book works) and encode canonical `resources/shelf.yaml` + `resources/shelf.json`.
- Build standalone zero-CDN parametric HTML/SVG workbenches (`demos/cover_studio.html` and `demos/cards_posters_studio.html`) with live vector SVG export.
- Curate 12 visual concept plates across framed Aldine/Nocturnal covers, four alternate cover philosophies (Full-Bleed Loci, $1:\phi$ Split-Band, Ratdolt 1482 Letterpress, Raw Linen Blind-Deboss), collector card decks, greeting cards, and museum broadsides.

## Phase 2: Book Master Agent (`press`) & `publish epub` Vetting

- **Book Master Agent (`press`) + Skill (`geometor-press`)**:
  - Author `agents/press.md` and `skills/geometor-press/SKILL.md` (either in `geometor/press` or `photon-platform/publish`) and register in `photon-platform/clerk` (`DEFAULT_TOOL_REPO_SPECS`) so `clerk agents sync` deploys the Book Master across workspaces.
- **EPUB 3.3 Pipeline Audit (`publish epub`)**:
  - Run and inspect `publish epub` on `geometor/hoenen` (*De Noetica Geometriae*) in Foliate, Calibre, and Apple Books.
  - Generalize `photon_platform/publish/directives/book.py` (replacing Hoenen-specific `(?:caput-\d+|appendix)` counterpart regex with generic `:layout: book` track discovery).
  - Persist compiled `.epub` releases into a dedicated non-gitignored release staging path (`releases/epub/`) so `publish clean` does not wipe vetted e-books.
  - Embed polytonic Greek (`grc`), classical Latin (`la`), mathematical serif fonts, and light-ground SVG rules in `epub.css`.

## Phase 3: Parametric Cover, Deck & Poster Compilers

- **`publish cover`**: Generate print-ready front/spine/back wraps (with dynamic spine width calculated from page count $\times$ paper caliper + `0.125"` bleed) directly from `shelf.yaml` + repository `.euclid-graphic` SVGs.
- **Card Deck Imposition (`publish deck`)**: Batch-compile 52/54/60-card print-ready PDF sheets (`2.75" × 4.75"` + `3mm` bleed) from `geometor/divine` (*The Golden Deck*), `geometor/etc` (*Classic 54 Triangle Centers*), and `geometor/pacioli` (*Leonardo's 60 Solids*).
- **Broadside & Greeting Folio Masters (`publish poster` / `publish card`)**: Export 300+ DPI vector PDF masters (`18"×24"`, `24"×36"`, and `5"×7"` A2 folded cards) for archival cotton giclée fulfillment.

## Phase 4: Print-Ready Book Interiors (`publish print`) & Storefront

- **Typst / LuaLaTeX Book Interior Compiler (`publish print`)**:
  - Compile `:layout: book` RST trees into press-ready PDF/X-1a interiors using $\phi$ / Van de Graaf page canons:
    - Trade Scholarly (`6" × 9"`),
    - Parallel Facing-Page Bilingual (`7" × 10"` verso source / recto English),
    - Illustrated Quarto (`8" × 10"` / `8.5" × 11"` for *Euclid*, *Byrne*, *Pacioli*, *Dürer*, *ETC*).
- **Two-Tier Sustainable Fulfillment**:
  - *Tier 1 (Always-In-Print Catalog)*: Zero-inventory print-on-demand via IngramSpark + direct storefront (LemonSqueezy / Gumroad / Lulu Direct + Prodigi/Printful giclée broadsides) on `geometor.com/press`—avoiding crowdfunding shipping bottlenecks while keeping every volume permanently available.
  - *Tier 2 (Numbered Collector Editions)*: Limited foil-stamped clothbound hardcovers and gilded card decks for flagship releases (*Hoenen Premiere*, *Polychrome Byrne*, *The Golden Deck*, *Kepler's Snowflake Gift Box*).
