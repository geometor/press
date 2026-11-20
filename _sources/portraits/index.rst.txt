:navigation: header
:order: 35
:nav_title: Portraits

==================================
Compass-and-Straightedge Portraits
==================================

.. rubric:: Line-and-Circle Author Medallions for the GEOMETOR Digital Library

To give every author gallery, person card, and book title page a unified geometric signature, GEOMETOR Press constructs vector portraits **strictly from straight lines and circular arcs**—with **zero Bézier curves**—calibrated over verified public-domain masterworks.

- **Unified Portrait Gallery (Studies 01–48)**: `Open Fullscreen <../_static/studios/portraits_gallery.html>`__ (or ``demos/portraits_gallery.html``)
- **Live 48-Slot Pantheon Poster**: ``editions/posters/geometor_portraits_poster.png`` (`Open Full-Res Poster <../_static/portraits/geometor_portraits_poster.png>`__)

.. raw:: html

   <div style="margin: 1.25rem 0 1.5rem; border: 1px solid rgba(160,160,160,0.3); border-radius: 12px; overflow: hidden;">
     <iframe src="../_static/studios/portraits_gallery.html"
             title="GEOMETOR Press — Compass-and-Straightedge Portrait Gallery"
             style="width: 100%; height: 860px; border: 0; display: block;"
             loading="lazy"></iframe>
   </div>

   <figure style="margin: 0 0 2rem; text-align: center;">
     <a href="../_static/portraits/geometor_portraits_poster.png" target="_blank" rel="noopener">
       <img src="../_static/portraits/geometor_portraits_poster.png" alt="GEOMETOR Pantheon of Geometers — Complete 48-Slot Dark Poster" style="width: 100%; border-radius: 12px; border: 1px solid rgba(212,175,55,0.35);" />
     </a>
     <figcaption style="font-size: 0.85rem; margin-top: 0.5rem;">GEOMETOR Pantheon of Geometers (<code>48</code> Complete · <code>37</code> Portraits + <code>11</code> Sacred Geometric Emblem Seals · <code>0</code> Bézier Curves)</figcaption>
   </figure>

1. Canonical Medallion Specification
------------------------------------

- **Coordinate Frame**: ``viewBox="-102 -106 204 196"`` with inner medallion circle ``(0, -8)``, radius ``R = 92``, and outer gold rim ``r = 95.2``.
- **Uniform Eye-Line & Head Scale**: Every subject's eyes align near ``y = -27`` with cranial circle ``R ≈ 26`` so frontal and three-quarter portraits sit on one steady horizontal horizon across collection cards.
- **Permitted Primitives**: ``<line>``, ``<circle>``, and circular-arc ``<path d="M ... A ...">`` only (`Euclid III.12` externally tangent circular arcs for curls, beards, hoods, and drapery).
- **Four Visual Layers**:
  1. **Scaffold** (``0.44``): Medallion ring, bilateral axes, cranial circle ``R``, golden circle ``R·φ``, and Vesica eye circles.
  2. **Golden Signature** (``0.85``): Subject's signature geometric construction or monogram.
  3. **Detail** (``0.62``): Upper eyelid fold, delicate lower lid, iris ring, and interior curl/drapery strands.
  4. **Primary** (``1.15``): Connected cranial, brow, eye, nose, lip, beard, and collar contours.

2. Study 01 — Albrecht Dürer (1500)
-----------------------------------

Constructed over Dürer's *Self-Portrait at Twenty-Eight* (1500, Alte Pinakothek, Munich — Public Domain). Placing the cranial circle ``R = 26`` at ``(0, -27)`` hits the center hairline at ``-R``, both temples at ``±R``, the base of the nose at ``+R``, and both pupils at ``±R/2 = ±13``, while the cascading locks follow exact ``60°`` rays from apex ``(0, -84)`` via ``Euclid III.12`` tangent circular arcs.

- **Standalone Studio**: ``demos/durer_portrait_studio.html`` (`Open Fullscreen <../_static/studios/durer_portrait_studio.html>`__)
- **Vector Exports**: ``_static/portraits/durer_dark.svg`` & ``_static/portraits/durer_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/durer_dark.svg" alt="Albrecht Durer 1500 Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>durer_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/durer_light.svg" alt="Albrecht Durer 1500 Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>durer_light.svg</code>)</figcaption>
     </figure>
   </div>

   <div style="margin: 1.25rem 0 2.25rem; border: 1px solid rgba(160,160,160,0.3); border-radius: 12px; overflow: hidden;">
     <iframe src="../_static/studios/durer_portrait_studio.html"
             title="GEOMETOR Press — Albrecht Durer 1500 Portrait Studio"
             style="width: 100%; height: 740px; border: 0; display: block;"
             loading="lazy"></iframe>
   </div>

3. Study 02 — Euclid of Alexandria (fl. c. 300 BCE)
---------------------------------------------------

Constructed over the Urbino Baroque portrait holding an open folio of the *Elements* (J. Paul Getty Museum / Google Art Project — Public Domain), with three-quarter geometric symmetry reconstructing the shadowed half of the face, ``Euclid III.12`` tangent circular arcs for the philosopher beard and rustic tunic folds, and Book I Proposition 1 (*Vesica Piscis* + Equilateral Triangle ``<A B C>``) in the golden layer.

- **Vector Exports**: ``_static/portraits/euclid_dark.svg`` & ``_static/portraits/euclid_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/euclid_dark.svg" alt="Euclid of Alexandria Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>euclid_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/euclid_light.svg" alt="Euclid of Alexandria Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>euclid_light.svg</code>)</figcaption>
     </figure>
   </div>

4. Study 03 — Plato of Athens (c. 428 – c. 348 BCE)
----------------------------------------------------

Constructed over Raphael's *The School of Athens* (1509–1511, Apostolic Palace, Vatican — Public Domain), capturing Plato's upward-pointing hand, flowing beard in ``Euclid III.12`` tangent circular arcs, the Divided Line (*Republic* VI), and a dodecahedral projection.

- **Vector Exports**: ``_static/portraits/plato_dark.svg`` & ``_static/portraits/plato_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/plato_dark.svg" alt="Plato of Athens Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>plato_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/plato_light.svg" alt="Plato of Athens Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>plato_light.svg</code>)</figcaption>
     </figure>
   </div>

5. Study 04 — Aristotle of Stagira (384 – 322 BCE)
--------------------------------------------------

Paired across the gallery with Plato from Raphael's *The School of Athens* (1509–1511, Vatican — Public Domain), featuring Aristotle's three-quarter left profile, curled beard in ``Euclid III.12`` tangent arcs, and the Continuum Axis & Geometric Syllogism Triangle.

- **Vector Exports**: ``_static/portraits/aristotle_dark.svg`` & ``_static/portraits/aristotle_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/aristotle_dark.svg" alt="Aristotle of Stagira Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>aristotle_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/aristotle_light.svg" alt="Aristotle of Stagira Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>aristotle_light.svg</code>)</figcaption>
     </figure>
   </div>

6. Study 05 — Fra Luca Pacioli (c. 1447 – 1517)
-----------------------------------------------

Constructed over Jacopo de' Barbari's 1495 portrait (Museo di Capodimonte, Naples — Public Domain), framing the Franciscan cowl hood in concentric circular arcs alongside the suspended glass rhombicuboctahedron and Golden Ratio dividers.

- **Vector Exports**: ``_static/portraits/pacioli_dark.svg`` & ``_static/portraits/pacioli_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/pacioli_dark.svg" alt="Fra Luca Pacioli Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>pacioli_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/pacioli_light.svg" alt="Fra Luca Pacioli Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>pacioli_light.svg</code>)</figcaption>
     </figure>
   </div>

7. Study 06 — Johannes Kepler (1571 – 1630)
-------------------------------------------

Constructed over the authentic Linz/Strasbourg portrait (``JKepler.jpg`` — Public Domain), pairing Kepler's lace ruff collar in ``Euclid III.12`` tangent arcs with the Kepler Right Triangle :math:`(1, \sqrt{\phi}, \phi)` and nested Platonic orbits.

- **Vector Exports**: ``_static/portraits/kepler_dark.svg`` & ``_static/portraits/kepler_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/kepler_dark.svg" alt="Johannes Kepler Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>kepler_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/kepler_light.svg" alt="Johannes Kepler Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>kepler_light.svg</code>)</figcaption>
     </figure>
   </div>

8. Study 07 — Leonhard Euler (1707 – 1783)
------------------------------------------

Constructed over Jakob Emanuel Handmann's 1753 pastel (Kunstmuseum Basel — Public Domain), rendering Euler's silk cap in concentric circular arcs framed by the Euler Line (``O–G–H``) and Nine-Point Circle.

- **Vector Exports**: ``_static/portraits/euler_dark.svg`` & ``_static/portraits/euler_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/euler_dark.svg" alt="Leonhard Euler Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>euler_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/euler_light.svg" alt="Leonhard Euler Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>euler_light.svg</code>)</figcaption>
     </figure>
   </div>

9. Study 08 — Archimedes of Syracuse (c. 287 – c. 212 BCE)
-----------------------------------------------------------

Constructed over Domenico Fetti's *Archimedes Thoughtful* (1620, Gemäldegalerie Alte Meister, Dresden — Public Domain), pairing Archimedes' contemplative hand-on-beard pose with his tombstone **Circumscribed Cylinder & Inscribed Sphere (`2:3`)** theorem and **Inscribed/Circumscribed Hexagon `π` Bounds**.

- **Vector Exports**: ``_static/portraits/archimedes_dark.svg`` & ``_static/portraits/archimedes_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/archimedes_dark.svg" alt="Archimedes of Syracuse Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>archimedes_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/archimedes_light.svg" alt="Archimedes of Syracuse Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>archimedes_light.svg</code>)</figcaption>
     </figure>
   </div>

10. Study 09 — St. Thomas Aquinas (1225 – 1274)
-----------------------------------------------

Constructed over Carlo Crivelli's 1476 altarpiece panel (National Gallery, London — Public Domain), uniting the Dominican tonsure and cowl arcs with the **Radiant Sun of *Materia Intelligibilis*** on his breastplate and the **Three Degrees of Abstraction Triangle** along his upward gaze.

- **Vector Exports**: ``_static/portraits/aquinas_dark.svg`` & ``_static/portraits/aquinas_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/aquinas_dark.svg" alt="St. Thomas Aquinas Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>aquinas_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/aquinas_light.svg" alt="St. Thomas Aquinas Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>aquinas_light.svg</code>)</figcaption>
     </figure>
   </div>

11. Study 10 — Blaise Pascal (1623 – 1662)
------------------------------------------

Constructed over the Palace of Versailles portrait after François II Quesnel (1691 — Public Domain), framing Pascal's pointed white *rabat* collar and Baroque hair waves with **Pascal's Triangle Lattice** and the mathematically exact ***Hexagrammum Mysticum* Pascal Line**.

- **Vector Exports**: ``_static/portraits/pascal_dark.svg`` & ``_static/portraits/pascal_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/pascal_dark.svg" alt="Blaise Pascal Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>pascal_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/pascal_light.svg" alt="Blaise Pascal Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>pascal_light.svg</code>)</figcaption>
     </figure>
   </div>

12. Study 11 — Jakob Steiner (1796 – 1863)
------------------------------------------

Constructed over August Weger's 1881 *Gesammelte Werke* engraving (Public Domain), pairing Steiner's folded arms and ``Euclid III.12`` beard waves with the **Steiner Porism (6-Circle Tangent Ring)** and the **Poncelet–Steiner Single-Circle Harmonic Construction**.

- **Vector Exports**: ``_static/portraits/steiner_dark.svg`` & ``_static/portraits/steiner_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/steiner_dark.svg" alt="Jakob Steiner Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>steiner_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/steiner_light.svg" alt="Jakob Steiner Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>steiner_light.svg</code>)</figcaption>
     </figure>
   </div>

13. Study 12 — Oliver Byrne (1810 – 1880)
-----------------------------------------

Constructed over the historic c. 1850 portrait (Public Domain), capturing Byrne's visionary upward gaze, billowing Victorian side-curls, and knotted cravat flanked by ***Elements* I.47 (Pythagorean Windmill)** and his **Visual-Proof Triad**.

- **Vector Exports**: ``_static/portraits/byrne_dark.svg`` & ``_static/portraits/byrne_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/byrne_dark.svg" alt="Oliver Byrne Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>byrne_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/byrne_light.svg" alt="Oliver Byrne Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>byrne_light.svg</code>)</figcaption>
     </figure>
   </div>

14. Study 13 — David Hilbert (1862 – 1943)
------------------------------------------

Constructed over the iconic 1912 Göttingen portrait (Public Domain), rendering Hilbert's Panama hat and circular-arc pince-nez spectacles alongside the **Pappus–Hilbert Incidence Configuration** and **Order-2 Hilbert Space-Filling Curve**.

- **Vector Exports**: ``_static/portraits/hilbert_dark.svg`` & ``_static/portraits/hilbert_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/hilbert_dark.svg" alt="David Hilbert Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>hilbert_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/hilbert_light.svg" alt="David Hilbert Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>hilbert_light.svg</code>)</figcaption>
     </figure>
   </div>

15. Study 14 — Bertrand Russell (1872 – 1970)
---------------------------------------------

Constructed over the 1907 Edwardian portrait (Public Domain), framing Russell's club collar and walrus mustache with the **Projective Cross-Ratio Pencil** and **Logic Triad Venn Circles**.

- **Vector Exports**: ``_static/portraits/bertrand_russell_dark.svg`` & ``_static/portraits/bertrand_russell_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/bertrand_russell_dark.svg" alt="Bertrand Russell Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>bertrand_russell_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/bertrand_russell_light.svg" alt="Bertrand Russell Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>bertrand_russell_light.svg</code>)</figcaption>
     </figure>
   </div>

16. Study 15 — Sir Thomas Little Heath (1861 – 1940)
----------------------------------------------------

Constructed over the c. 1910 Royal Society / MacTutor studio portrait (Public Domain), uniting Heath's classical scholarship with an ***Elements* Scroll & Golden Section (`1 : φ`)** and **Book XIII Inscribed Pentagon & Decagram Star**.

- **Vector Exports**: ``_static/portraits/heath_dark.svg`` & ``_static/portraits/heath_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/heath_dark.svg" alt="Sir Thomas Little Heath Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>heath_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/heath_light.svg" alt="Sir Thomas Little Heath Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>heath_light.svg</code>)</figcaption>
     </figure>
   </div>

17. Study 16 — Leonardo da Vinci (1452 – 1519)
----------------------------------------------

Constructed over the red-chalk *Portrait of a Man* (c. 1510–1515, Biblioteca Reale, Turin — Public Domain), balancing Leonardo's flowing sage beard with the **Vitruvian Circle-and-Square Canon** and **Geometric Compass Rosette**.

- **Vector Exports**: ``_static/portraits/leonardo_dark.svg`` & ``_static/portraits/leonardo_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/leonardo_dark.svg" alt="Leonardo da Vinci Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>leonardo_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/leonardo_light.svg" alt="Leonardo da Vinci Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>leonardo_light.svg</code>)</figcaption>
     </figure>
   </div>

18. Study 17 — Piero della Francesca (c. 1415 – 1492)
-----------------------------------------------------

Constructed over Santi di Tito's c. 1590 Sansepolcro portrait (Public Domain), pairing Piero's dignified Quattrocento silhouette with a **One-Point Perspective Vanishing Grid** and **Wireframe Truncated Polyhedron**.

- **Vector Exports**: ``_static/portraits/piero_dark.svg`` & ``_static/portraits/piero_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/piero_dark.svg" alt="Piero della Francesca Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>piero_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/piero_light.svg" alt="Piero della Francesca Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>piero_light.svg</code>)</figcaption>
     </figure>
   </div>

19. Study 18 — Nicholas of Cusa (1401 – 1464)
---------------------------------------------

Constructed over the Cusanusstift altar triptych donor portrait (c. 1460–1480, Bernkastel-Kues — Public Domain), framing Cusanus's cardinal biretta with **Coincidentia Oppositorum Infinite Polygons** and **Expanding Tangent Circles**.

- **Vector Exports**: ``_static/portraits/cusa_dark.svg`` & ``_static/portraits/cusa_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/cusa_dark.svg" alt="Nicholas of Cusa Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>cusa_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/cusa_light.svg" alt="Nicholas of Cusa Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>cusa_light.svg</code>)</figcaption>
     </figure>
   </div>

20. Study 19 — Leonardo Pisano / Fibonacci (c. 1170 – c. 1250)
--------------------------------------------------------------

Constructed over the c. 1850 Tuscan engraved portrait (Public Domain), uniting Fibonacci's medieval chaperon hood with **Fibonacci Whirling Squares**, a **Quarter-Circle Golden Spiral**, and an **Inscribed Pentagram**.

- **Vector Exports**: ``_static/portraits/fibonacci_dark.svg`` & ``_static/portraits/fibonacci_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/fibonacci_dark.svg" alt="Leonardo Pisano Fibonacci Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>fibonacci_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/fibonacci_light.svg" alt="Leonardo Pisano Fibonacci Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>fibonacci_light.svg</code>)</figcaption>
     </figure>
   </div>

21. Study 20 — Claudius Ptolemy (c. 100 – c. 170 CE)
----------------------------------------------------

Constructed over the Urbino Studiolo panel by Justus of Ghent & Pedro Berruguete (c. 1473–1476, Musée du Louvre — Public Domain), pairing Ptolemy's crowned scholar profile with **Ptolemy's Cyclic Quadrilateral** and **Epicycle-on-Deferent Orbits**.

- **Vector Exports**: ``_static/portraits/ptolemy_dark.svg`` & ``_static/portraits/ptolemy_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/ptolemy_dark.svg" alt="Claudius Ptolemy Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>ptolemy_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/ptolemy_light.svg" alt="Claudius Ptolemy Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>ptolemy_light.svg</code>)</figcaption>
     </figure>
   </div>

22. Study 21 — Felix Klein (1849 – 1925)
----------------------------------------

Constructed over the pre-1897 Gebrüder Noelle Göttingen studio portrait (Accademia delle Scienze di Torino — Public Domain), framing Klein's sweeping beard with the **Beltrami–Klein Hyperbolic Disk Model** and **Erlangen Symmetry Triad**.

- **Vector Exports**: ``_static/portraits/klein_dark.svg`` & ``_static/portraits/klein_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/klein_dark.svg" alt="Felix Klein Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>klein_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/klein_light.svg" alt="Felix Klein Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>klein_light.svg</code>)</figcaption>
     </figure>
   </div>

23. Study 22 — Henri Poincaré (1854 – 1912)
-------------------------------------------

Constructed over Eugène Pirou's 1887 Paris portrait (Public Domain), uniting Poincaré's pince-nez and pointed beard with the **Poincaré Hyperbolic Disk** (exact orthogonal geodesic arcs & ideal triangle) and **3-Body Phase Orbits**.

- **Vector Exports**: ``_static/portraits/poincare_dark.svg`` & ``_static/portraits/poincare_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/poincare_dark.svg" alt="Henri Poincare Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>poincare_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/poincare_light.svg" alt="Henri Poincare Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>poincare_light.svg</code>)</figcaption>
     </figure>
   </div>

24. Study 23 — Sir D'Arcy Wentworth Thompson (1860 – 1948)
----------------------------------------------------------

Constructed over Robertson's 1886 Dundee portrait (University of St Andrews — CC0 1.0), pairing Thompson's naturalistic poise with a **Logarithmic Gnomon Spiral** and **Cartesian-to-Polar Morphogenetic Transformation Grid**.

- **Vector Exports**: ``_static/portraits/thompson_dark.svg`` & ``_static/portraits/thompson_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/thompson_dark.svg" alt="D'Arcy Wentworth Thompson Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>thompson_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/thompson_light.svg" alt="D'Arcy Wentworth Thompson Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>thompson_light.svg</code>)</figcaption>
     </figure>
   </div>

25. Study 24 — Petrus Hoenen, S.J. (1880 – 1961)
------------------------------------------------

Constructed over the 1930s archival portrait (Public Domain Mark 1.0), framing Hoenen's Jesuit Roman collar and spectacles with the **Noetic Abstraction Triangle** (*Phantasm → Intelligible Matter → Judicium*) and **Constructive Compass Arc**.

- **Vector Exports**: ``_static/portraits/hoenen_dark.svg`` & ``_static/portraits/hoenen_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/hoenen_dark.svg" alt="Petrus Hoenen Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>hoenen_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/hoenen_light.svg" alt="Petrus Hoenen Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>hoenen_light.svg</code>)</figcaption>
     </figure>
   </div>

26. Study 25 — Walter Russell (1871 – 1963)
-------------------------------------------

Constructed over the archival circular portrait (Public Domain), uniting Russell's sculpted studio portrait with **Concentric Wave-Field Octave Circles** and the **Cubic-Sphere Dual Projection**.

- **Vector Exports**: ``_static/portraits/walter_russell_dark.svg`` & ``_static/portraits/walter_russell_light.svg``

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/walter_russell_dark.svg" alt="Walter Russell Medallion — Obsidian Ink" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Obsidian Ink (<code>walter_russell_dark.svg</code>)</figcaption>
     </figure>
     <figure style="margin: 0; text-align: center;">
       <img src="../_static/portraits/walter_russell_light.svg" alt="Walter Russell Medallion — Warm Paper" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" />
       <figcaption style="font-size: 0.85rem; margin-top: 0.4rem;">Warm Paper (<code>walter_russell_light.svg</code>)</figcaption>
     </figure>
   </div>

27. Batch 4 — Final 12 Portraits (Studies 26–37)
------------------------------------------------

Completing all **37 human portraits** across the 48-person GEOMETOR Pantheon—spanning Hellenistic woodcuts, medieval miniatures, Neoclassical profiles, 19th-century European studio portraits, and contemporary astrophysics—strictly via ``MedallionBuilder`` (zero Bézier curves, clipped within ``MED_R = 92``):

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.9rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/apollonius_dark.svg" alt="Apollonius of Perga" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">26 · Apollonius of Perga</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/heron_dark.svg" alt="Heron of Alexandria" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">27 · Heron of Alexandria</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/nicomachus_dark.svg" alt="Nicomachus of Gerasa" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">28 · Nicomachus of Gerasa</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/mascheroni_dark.svg" alt="Lorenzo Mascheroni" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">29 · Lorenzo Mascheroni</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/staudt_dark.svg" alt="Karl G. C. von Staudt" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">30 · Karl G. C. von Staudt</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/feuerbach_dark.svg" alt="Karl Wilhelm Feuerbach" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">31 · Karl Wilhelm Feuerbach</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/casey_dark.svg" alt="John Casey" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">32 · John Casey</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/ernst_haeckel_dark.svg" alt="Ernst Haeckel" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">33 · Ernst Haeckel</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/petersen_dark.svg" alt="Julius Petersen" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">34 · Julius Petersen</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/lemoine_dark.svg" alt="Emile Lemoine" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">35 · Émile Lemoine</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/pasch_dark.svg" alt="Moritz Pasch" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">36 · Moritz Pasch</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/livio_dark.svg" alt="Mario Livio" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">37 · Mario Livio</figcaption></figure>
   </div>

28. Batch 5 — 11 Sacred Geometric Emblem Seals (Studies 38–48)
--------------------------------------------------------------

For the **11 Pantheon geometers** without verified public-domain portraits (honoring historical provenance and modern copyright strictly), GEOMETOR Press renders **centered astrolabe-seal sacred geometric emblems**—each analytically verified to machine or exact rational precision inside the unified 36-tick graduated bezel and 4 cardinal pins:

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.9rem; margin: 1.25rem 0;">
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/menelaus_dark.svg" alt="Menelaus of Alexandria" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">38 · Menelaus of Alexandria</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/pappus_dark.svg" alt="Pappus of Alexandria" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">39 · Pappus of Alexandria</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/proclus_dark.svg" alt="Proclus Lycius" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">40 · Proclus Lycius</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/ceva_dark.svg" alt="Giovanni Ceva" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">41 · Giovanni Ceva</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/hambidge_dark.svg" alt="Jay Hambidge" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">42 · Jay Hambidge</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/altshiller_court_dark.svg" alt="Nathan Altshiller-Court" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">43 · Nathan Altshiller-Court</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/hans_kayser_dark.svg" alt="Hans Kayser" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">44 · Hans Kayser</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/huntley_dark.svg" alt="H. E. Huntley" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">45 · H. E. Huntley</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/odom_dark.svg" alt="George Odom" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">46 · George Odom</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/kimberling_dark.svg" alt="Clark Kimberling" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">47 · Clark Kimberling</figcaption></figure>
     <figure style="margin: 0; text-align: center;"><img src="../_static/portraits/wildberger_dark.svg" alt="Norman J. Wildberger" style="width: 100%; border-radius: 10px; border: 1px solid rgba(160,160,160,0.25);" /><figcaption style="font-size: 0.8rem; margin-top: 0.35rem;">48 · Norman J. Wildberger</figcaption></figure>
   </div>

29. Complete Pantheon Medallion Catalog (48 of 48 Pantheon Slots)
-----------------------------------------------------------------

All **48 Pantheon medallion records** (37 verified public-domain portraits + 11 sacred geometric emblem seals; 96 exported dark/light SVGs with zero Bézier curves) are tracked in ``resources/portraits.yaml`` and ``resources/portraits.json``:

.. list-table::
   :header-rows: 1
   :widths: 14 20 34 32

   * - Study
     - Subject
     - Verified Source / Seal Type
     - Signature Geometric Motif
   * - **Study 01**
     - **Albrecht Dürer** (``durer``)
     - *Self-Portrait at Twenty-Eight* (1500, Alte Pinakothek)
     - 60° hair-cascade triangle & ``1500 AD`` monogram
   * - **Study 02**
     - **Euclid** (``euclid``)
     - Urbino Baroque portrait holding *Elements* (Getty / Google Art Project)
     - Book I Prop. 1 *Vesica Piscis* & Equilateral Triangle
   * - **Study 03**
     - **Plato** (``plato``)
     - Raphael, *The School of Athens* (1509–1511, Vatican — ``Sanzio_01_Plato_Aristotle.jpg``)
     - Divided Line (*Republic* VI) & dodecahedral projection
   * - **Study 04**
     - **Aristotle** (``aristotle``)
     - Raphael, *The School of Athens* (1509–1511, Vatican — ``Sanzio_01_Plato_Aristotle.jpg``)
     - Continuum axis & syllogism triangle
   * - **Study 05**
     - **Fra Luca Pacioli** (``pacioli``)
     - Jacopo de' Barbari (1495, Capodimonte, Naples — ``Pacioli.jpg``)
     - Suspended rhombicuboctahedron & Golden Ratio dividers
   * - **Study 06**
     - **Johannes Kepler** (``kepler``)
     - Authentic Linz portrait (``JKepler.jpg`` — avoiding the spurious 1610 copy)
     - Kepler Right Triangle :math:`(1, \sqrt{\phi}, \phi)` & nested spheres
   * - **Study 07**
     - **Leonhard Euler** (``euler``)
     - Jakob Emanuel Handmann pastel (1753, Kunstmuseum Basel — ``Leonhard_Euler.jpg``)
     - Euler Line (``O–G–H``) & Nine-Point Circle
   * - **Study 08**
     - **Archimedes of Syracuse** (``archimedes``)
     - Domenico Fetti (1620, Dresden — ``Domenico-Fetti Archimedes 1620.jpg``)
     - Circumscribed Cylinder & Inscribed Sphere (``2:3``) + Hexagon :math:`\pi` bounds
   * - **Study 09**
     - **St. Thomas Aquinas** (``aquinas``)
     - Carlo Crivelli (1476, National Gallery, London — ``St-thomas-aquinas.jpg``)
     - Radiant Sun of *Materia Intelligibilis* & Three Degrees of Abstraction
   * - **Study 10**
     - **Blaise Pascal** (``pascal``)
     - After François II Quesnel (Palace of Versailles — ``Blaise_Pascal_Versailles.JPG``)
     - *Hexagrammum Mysticum* Pascal Line & Pascal's Triangle lattice
   * - **Study 11**
     - **Jakob Steiner** (``steiner``)
     - August Weger engraving (1881 — ``Jakob Steiner portrait 1881.jpg``)
     - Steiner Porism (6-circle ring) & Poncelet–Steiner circle
   * - **Study 12**
     - **Oliver Byrne** (``byrne``)
     - Historic portrait (c. 1850 — ``Oliver Byrne Portrait (ca 1850).jpg``)
     - *Elements* I.47 Pythagorean Windmill & Visual-Proof Triad
   * - **Study 13**
     - **David Hilbert** (``hilbert``)
     - 1912 Göttingen portrait (``Hilbert.jpg``)
     - Pappus–Hilbert Incidence Configuration & Order-2 Hilbert Curve
   * - **Study 14**
     - **Bertrand Russell** (``bertrand-russell``)
     - 1907 Edwardian portrait (``Bertrand Russell, 1907.jpg``)
     - Projective Cross-Ratio Pencil & Logic Triad Venn Circles
   * - **Study 15**
     - **Sir Thomas Little Heath** (``heath``)
     - c. 1910 studio portrait (MacTutor / Royal Society — ``Thomas Little Heath.jpg``)
     - *Elements* Scroll Golden Section & Book XIII Pentagon / Decagram
   * - **Study 16**
     - **Leonardo da Vinci** (``leonardo``)
     - Red-chalk self-portrait (c. 1510–1515, Biblioteca Reale, Turin)
     - Vitruvian Circle-and-Square Canon & Geometric Compass Rosette
   * - **Study 17**
     - **Piero della Francesca** (``piero``)
     - Santi di Tito (c. 1590, Museo Civico di Sansepolcro)
     - One-Point Perspective Vanishing Grid & Truncated Polyhedron
   * - **Study 18**
     - **Nicholas of Cusa** (``cusa``)
     - Master of the Life of the Virgin (c. 1460–1480, Cusanusstift)
     - *Coincidentia Oppositorum* Infinite Polygons & Expanding Tangent Circles
   * - **Study 19**
     - **Leonardo Pisano (Fibonacci)** (``fibonacci``)
     - 19th-century Italian engraving (c. 1850 — ``Fibonacci.jpg``)
     - Fibonacci Whirling Squares & Quarter-Circle Golden Spiral
   * - **Study 20**
     - **Claudius Ptolemy** (``ptolemy``)
     - Justus of Ghent & Pedro Berruguete (c. 1473–1476, Louvre)
     - Ptolemy Cyclic Quadrilateral & Epicycle-on-Deferent Orbits
   * - **Study 21**
     - **Felix Klein** (``klein``)
     - Gebrüder Noelle (ante 1897, Accademia delle Scienze di Torino)
     - Beltrami–Klein Hyperbolic Disk Model & Erlangen Symmetry Triad
   * - **Study 22**
     - **Henri Poincaré** (``poincare``)
     - Eugène Pirou (1887, Paris — ``Poincare.jpg``)
     - Poincaré Hyperbolic Disk Orthogonal Geodesics & 3-Body Orbits
   * - **Study 23**
     - **D'Arcy Wentworth Thompson** (``thompson``)
     - Robertson, Dundee (1886, St Andrews — CC0 1.0)
     - Logarithmic Gnomon Spiral & Morphogenetic Transformation Grid
   * - **Study 24**
     - **Petrus Hoenen, S.J.** (``hoenen``)
     - Archival 1930s portrait (PD Mark 1.0 — ``PHJHoenen.jpg``)
     - Noetic Abstraction Triangle & Constructive Compass Arc
   * - **Study 25**
     - **Walter Russell** (``walter-russell``)
     - Archival circular portrait (Public Domain — ``Walter_Russell_circular_portrait.jpg``)
     - Concentric Wave-Field Octave Circles & Cubic-Sphere Dual Projection
   * - **Study 26**
     - **Apollonius of Perga** (``apollonius``)
     - 1537 Venice woodcut (Public Domain)
     - Descartes Apollonian Gasket & Orthogonal Coaxal Circles
   * - **Study 27**
     - **Heron of Alexandria** (``heron``)
     - Classical Hellenic bust engraving (Public Domain)
     - Heron Incircle (:math:`A = r s`) & *Catoptrica* Reflection Proof
   * - **Study 28**
     - **Nicomachus of Gerasa** (``nicomachus``)
     - 12th-century Cambridge MS illuminated miniature (Public Domain)
     - Pythagorean Tetractys & Odd Square Gnomon Lattice
   * - **Study 29**
     - **Lorenzo Mascheroni** (``mascheroni``)
     - F. Redenti Neoclassical profile engraving (Public Domain)
     - Napoleon's Compass-Only Circle Quartering & Seed of Life
   * - **Study 30**
     - **Karl G. C. von Staudt** (``staudt``)
     - 19th-century Erlangen archival portrait (Public Domain)
     - Complete Quadrangle Harmonic Throw :math:`H(A,B;C,D)` & Polarity Circle
   * - **Study 31**
     - **Karl Wilhelm Feuerbach** (``feuerbach``)
     - Romantic pencil portrait (Public Domain)
     - Feuerbach Nine-Point / Incircle / Excircle Tangencies (:math:`X(11)`)
   * - **Study 32**
     - **John Casey** (``casey``)
     - 19th-century Irish archival portrait (Public Domain)
     - Casey's Theorem (4 Circles Tangent to a 5th) & Radical Axis
   * - **Study 33**
     - **Ernst Haeckel** (``ernst-haeckel``)
     - Archival left-profile naturalist portrait (Public Domain)
     - *Circogonia icosahedra* Radiolarian & *Actinoptychus* Diatom Star
   * - **Study 34**
     - **Julius Petersen** (``petersen``)
     - 19th-century Danish cabinet portrait (Public Domain)
     - Petersen Graph (10 Vertices, 15 Edges) & Center of Similitude
   * - **Study 35**
     - **Émile Lemoine** (``lemoine``)
     - 19th-century French studio portrait (Public Domain)
     - First Lemoine Circle & Symmedians (:math:`X(6)`) + *Géométrographie* Compass
   * - **Study 36**
     - **Moritz Pasch** (``pasch``)
     - Giessen G. Backofen cabinet portrait (Public Domain)
     - Pasch's Axiom Transversal (1882) & Linear Betweenness Triad
   * - **Study 37**
     - **Mario Livio** (``livio``)
     - NASA / STScI portrait (Public Domain)
     - Inscribed Pentagram & Recursive Penrose Golden Triangle Spiral
   * - **Study 38**
     - **Menelaus of Alexandria** (``menelaus``)
     - Sacred Geometric Astrolabe Seal
     - *Sphaerica* Great-Circle Triangle & Planar/Spherical Menelaus Transversal
   * - **Study 39**
     - **Pappus of Alexandria** (``pappus``)
     - Sacred Geometric Astrolabe Seal
     - Pappus Hexagon Theorem (``P–Q–R``) & 9-Circle Inversion Arbelos Chain
   * - **Study 40**
     - **Proclus Lycius** (``proclus``)
     - Sacred Geometric Astrolabe Seal
     - :math:`1 : \sqrt{3} : 3` Neoplatonic Triad & *Elements* I.1 *Vesica Piscis*
   * - **Study 41**
     - **Giovanni Ceva** (``ceva``)
     - Sacred Geometric Astrolabe Seal
     - Concurrent Cevians (``3:2:5``), Cevian Triangle & Trilinear Polar
   * - **Study 42**
     - **Jay Hambidge** (``hambidge``)
     - Sacred Geometric Astrolabe Seal
     - Dynamic Symmetry :math:`1 : \sqrt{5}` Unfolding & 7-Turn Whirling-Square Spiral
   * - **Study 43**
     - **Nathan Altshiller-Court** (``altshiller-court``)
     - Sacred Geometric Astrolabe Seal
     - Four Congruent Orthocentric Circumcircles & Shared Nine-Point Circle
   * - **Study 44**
     - **Hans Kayser** (``hans-kayser``)
     - Sacred Geometric Astrolabe Seal
     - ``6 × 6`` Pythagorean–Kayser Lambdoma Lattice & Monochord Wave Arcs
   * - **Study 45**
     - **H. E. Huntley** (``huntley``)
     - Sacred Geometric Astrolabe Seal
     - ``3–4–5`` Angle-Bisector Golden Section & Golden Gnomon *Spira Mirabilis*
   * - **Study 46**
     - **George Odom** (``odom``)
     - Sacred Geometric Astrolabe Seal
     - Equilateral Triangle Midpoint-Chord Golden Section (:math:`AB:BC = \phi`)
   * - **Study 47**
     - **Clark Kimberling** (``kimberling``)
     - Sacred Geometric Astrolabe Seal
     - ETC Quartet :math:`X(1)\text{–}X(4)` Constellation, Euler Line & :math:`X(11)`
   * - **Study 48**
     - **Norman J. Wildberger** (``wildberger``)
     - Sacred Geometric Astrolabe Seal
     - ``13–14–15`` Quadrance Squares, Vertex Spread Circles & Exact Cross-Law
