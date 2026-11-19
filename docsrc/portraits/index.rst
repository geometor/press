:navigation: header
:order: 35
:nav_title: Portraits

==================================
Compass-and-Straightedge Portraits
==================================

.. rubric:: Line-and-Circle Author Medallions for the GEOMETOR Digital Library

To give every author gallery, person card, and book title page a unified geometric signature, GEOMETOR Press constructs vector portraits **strictly from straight lines and circular arcs**—with **zero Bézier curves**—calibrated over verified public-domain masterworks.

- **Unified Portrait Gallery (Studies 01–07)**: `Open Fullscreen <../_static/studios/portraits_gallery.html>`__ (or ``demos/portraits_gallery.html``)

.. raw:: html

   <div style="margin: 1.25rem 0 2rem; border: 1px solid rgba(160,160,160,0.3); border-radius: 12px; overflow: hidden;">
     <iframe src="../_static/studios/portraits_gallery.html"
             title="GEOMETOR Press — Compass-and-Straightedge Portrait Gallery"
             style="width: 100%; height: 820px; border: 0; display: block;"
             loading="lazy"></iframe>
   </div>

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

9. Completed Portrait Medallion Catalog
---------------------------------------

All portrait metadata, Wikimedia Commons identifiers, and museum holdings are tracked in ``resources/portraits.yaml`` and ``resources/portraits.json``:

.. list-table::
   :header-rows: 1
   :widths: 14 20 34 32

   * - Study
     - Subject
     - Verified Public-Domain Source
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
