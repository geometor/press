==============
GEOMETOR Press
==============

*Exploring the Architecture of All That Is — Exact Symbolic & Classical Editions.*

``geometor-press`` is the editorial, typographic, brand, and product-curation headquarters for **GEOMETOR Press**—organizing **48 cataloged repositories**, **44+ distinct book works**, **71,900+ parametric vector SVGs**, and **2,377 archival folios** into a cohesive family of:

- **Print Books & Fine Collector Quartos** (Trade Paperbacks, Facing Bilingual Greek/Latin/German/French/English Editions, and Clothbound Hardcovers)
- **EPUB 3.3 Electronic Editions** (Reflowable scholarly editions and fixed-layout polychrome plates compiled via ``photon-platform/publish``)
- **Collector, Study & Puzzle Card Decks** (*The Golden Deck*, *Centers of the Triangle: Series I*, *Leonardo's 60 Polyhedra*, *Euclid Book I*, *Seelig F.1–F.55*, *Archimedes' Stomachion*)
- **Folded Foil Greeting & Seasonal Note Cards** (*Kepler's De Nive Sexangula 1611*, *Feuerbach's Kiss 1822*, *Golden Meristem 137.5°*, *Dürer & Pacioli Majuscules*)
- **Museum-Grade Broadside Posters** (*The Deductive Spine G.1–G.601*, *Polychrome Euclid Grid*, *Four Reference Triangles*, *Hexagrammum Mysticum*, *Planisphaerium*)
- **Living Instrument Apps** (Interactive step-scrubbers, 3D polyhedra/meristem studios, and playable harmonic scales)

The Five Spine Series
---------------------

Every volume and tactile edition is organized into one of five mineral-pigment series sharing aligned spine medallions and the *Vesica-to-* :math:`\phi` colophon:

1. **Series I · Fontes Geometrici** (Warm Ochre / Gold ``#b8860b``) — Classical, Medieval & Renaissance geometric treatises (*Euclid*, *Archimedes*, *Apollonius*, *Pappus*, *Menelaus*, *Ptolemy*, *Fibonacci*, *Pacioli*, *Dürer*, *Kepler*, *Byrne*).
2. **Series II · Bibliotheca Noetica** (Venetian Rubric Red ``#8b3a3a``) — Philosophical, epistemological & axiomatic foundations (*Plato*, *Aristotle*, *Proclus*, *Aquinas*, *Hoenen*, *Hilbert*, *Poincaré*, *Bertrand Russell*, *von Staudt*, *Klein*).
3. **Series III · Synthesis & Constructio** (Prussian Blueprint Blue ``#2b5b84``) — Modern synthetic, projective & computable geometry (*Elements 2.0*, *Divine Constructions*, *ETC Triangle Centers*, *Altshiller-Court*, *Casey*, *Lemoine*, *Feuerbach*, *Wildberger*).
4. **Series IV · Morphogenesis & Natura** (Botanical Viridian ``#2e6f40``) — Living geometry, dynamic symmetry & wave-field cosmogony (*Phyllotaxis*, *D'Arcy Thompson*, *Walter Russell*).
5. **Series V · Instrumenta & Machina** (Spectral Violet ``#5a4fcf``) — Symbolic kernels, formal grammars & reasoning observatories (*GEOMETOR Model*, *GEOMETOR Codes*, *Explorer*, *Seer*).

Repository Layout
-----------------

- ``resources/shelf.yaml`` & ``resources/shelf.json`` — Canonical machine-readable Shelf & Multi-Format Product Manifest.
- ``resources/census.json`` — Empirical snapshot across all GEOMETOR repositories.
- ``demos/cover_studio.html`` — Standalone parametric SVG Cover & Spine Studio (3 binding finishes, :math:`\phi` canon grid, 8-book matched shelf, SVG export).
- ``demos/cards_posters_studio.html`` — Standalone interactive 3D-flip Collector Card Deck, Greeting Folio & ``24" × 36"`` Broadside Poster Studio with SVG export.
- ``docsrc/_static/lookbook/`` — 12 high-resolution concept plates across covers, spines, collector decks, greeting cards, and museum posters.
- ``src/geometor/press/`` — Typed Python 3.13 shelf loader, workspace census scanner, and ``press`` CLI.

CLI Usage
---------

.. code-block:: bash

   # Imprint overview, readiness stages, spine series & derived product totals
   python -m geometor.press summary

   # Filter the shelf by readiness stage or spine series
   python -m geometor.press shelf --stage stage_4_codex_live
   python -m geometor.press shelf --series fontes

   # Inspect non-book collector decks, greeting cards, posters & apps
   python -m geometor.press products --kind cards_collector
   python -m geometor.press products --kind poster

   # Refresh the workspace census snapshot
   python -m geometor.press census

Documentation
-------------

Compile the GEOMETOR Press codex and embedded interactive studios via ``photon-platform/publish``:

.. code-block:: bash

   publish build
