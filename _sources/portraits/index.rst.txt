:navigation: header
:order: 35
:nav_title: Portraits

==================================
Compass-and-Straightedge Portraits
==================================

.. rubric:: Line-and-Circle Author Medallions for the GEOMETOR Digital Library

To give every author gallery, person card, and book title page a unified geometric signature, GEOMETOR Press constructs vector portraits **strictly from straight lines and circular arcs**—with **zero Bézier curves**—calibrated over verified public-domain masterworks.

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

3. Verified Public-Domain Reference Queue
-----------------------------------------

All portrait metadata, Wikimedia Commons identifiers, and museum holdings are tracked in ``resources/portraits.yaml`` and ``resources/portraits.json``:

.. list-table::
   :header-rows: 1
   :widths: 14 20 34 32

   * - Queue
     - Subject
     - Verified Public-Domain Source
     - Signature Geometric Motif
   * - **Next 1**
     - **Euclid** (``euclid``)
     - Urbino Baroque portrait holding *Elements* (Getty / Google Art Project; local ref staged)
     - Book I Prop. 1 *Vesica Piscis* & Equilateral Triangle
   * - **Next 2**
     - **Plato** (``plato``)
     - Raphael, *The School of Athens* (1509–1511, Vatican — ``Sanzio_01_Plato_Aristotle.jpg``)
     - Divided Line (*Republic* VI) & dodecahedral projection
   * - **Next 3**
     - **Aristotle** (``aristotle``)
     - Raphael, *The School of Athens* (1509–1511, Vatican — ``Sanzio_01_Plato_Aristotle.jpg``)
     - Continuum axis & syllogism triangle
   * - **Next 4**
     - **Fra Luca Pacioli** (``pacioli``)
     - Jacopo de' Barbari (1495, Capodimonte, Naples — ``Pacioli.jpg``)
     - Suspended rhombicuboctahedron & Golden Ratio dividers
   * - **Next 5**
     - **Johannes Kepler** (``kepler``)
     - Authentic Linz portrait (``JKepler.jpg`` — avoiding the spurious 1610 copy)
     - Kepler Right Triangle :math:`(1, \sqrt{\phi}, \phi)` & nested spheres
   * - **Queued**
     - **Leonhard Euler** (``euler``)
     - Jakob Emanuel Handmann pastel (1753, Kunstmuseum Basel — ``Leonhard_Euler.jpg``)
     - Euler Line (``O–G–H``) & Nine-Point Circle
