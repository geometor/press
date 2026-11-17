:navigation: header
:order: 15
:nav_title: Standards
:breadcrumb_title: Standards

.. _press-standards:

Codex, SVG & Project Scaffolding Standards
==========================================

.. rubric:: Canonical Lessons & Specifications for New GEOMETOR Repositories

This specification captures the verified engineering and editorial standards established across the **61 GEOMETOR repositories**, ``photon-platform/clerk``, and ``photon-platform/publish``. Follow this checklist whenever scaffolding a new project with ``clerk init`` or curating a Book Codex.

----

1. Strict XML & Theme-Safe SVG Diagrams
---------------------------------------

Every ``.svg`` diagram—whether a construction hero or an inline ``.euclid-graphic``—must be **100% valid strict XML** so it renders cleanly in GitHub ``camo`` proxies, Antigravity previews, browsers, and EPUB 3.3 readers:

* **Escape XML Attribute Metacharacters**: Never place literal ``<``, ``>``, or ``&`` inside XML attribute values. Escape polygon/angle references such as ``data-ref="< A B C >"`` as ``data-ref="&lt; A B C &gt;"`` (browsers and ``getAttribute()`` decode entities back to ``< A B C >`` automatically).
* **Wrap Inline Scripts in CDATA**: If an SVG embeds interactive ``<script>`` logic containing ``<`` or ``&``, wrap the script body in ``//<![CDATA[ ... //]]>``.
* **Standalone Light & Dark Theme CSS**: Hero SVGs referenced in ``README.rst`` or external galleries must embed a ``<style>`` block defining ``--svg-bg``, ``@media (prefers-color-scheme: dark)`` (or light), and an opaque ``.svg-bg`` background ``<rect>`` so diagrams never disappear against dark or light canvases.
* **Verify XML Parsing**: Validate every generated SVG with Python's ``xml.etree.ElementTree.fromstring`` before committing.

----

2. Repository Storefront & ``README.rst``
-----------------------------------------

* **No Nested Bold Around RST Links**: Never wrap an RST hyperlink in ``**...**`` (bold around backtick links breaks in GitHub's RST parser). Always write `` `Title <url>`_ `` directly.
* **Masthead & Mission**: Open with ``GEOMETOR • <repo>``, ``**Visit the Online Archive:** <url>``, the clickable construction hero ``.. image::`` block (when visual assets exist), and the ``•``-delimited ``semantic digital archive`` summary line.
* **Validate Before Push**: Run ``docutils`` over ``README.rst`` to confirm zero warnings or syntax errors.

----

3. Elevating English & Multi-Track Book Title Pages
---------------------------------------------------

* **Pure English Primary Title Page (``index.rst``)**: Use clean English for ``<h1>``, ``:book_title:``, ``:nav_title:``, and ``:breadcrumb_title:`` (retaining accepted English loan-titles such as *Almagest*, *Metrica*, *Organon*, *Meno*, *Theaetetus*, *Republic*, *Timaeus*, and *Summa Theologiae*), with the native original title italicized in ``.. rubric::``.
* **Dedicated Native Title Pages (``title-<lang>.rst``)**: Instead of mixing bilingual double text on one page, create a companion native-language Title Page (``title-la.rst``, ``title-de.rst``, ``title-it.rst``, ``title-fr.rst``, ``title-el.rst``) with ``:type: book_title`` and ``:layout: book``, wired via ``:tracks: English: index | Latin: title-la`` and included in a hidden ``:caption: Title Pages`` toctree.
* **Zero Years in Menus**: Never put publication years inside ``:nav_title:``, ``:breadcrumb_title:``, or toctree ``:caption:`` labels. Years belong in the page body and subtitle ``.. rubric::``.
* **Canonical Track Menu Labels**: Always use full English words in ``:tracks:``, ``:track_label:``, and inline track tables: ``English``, ``Latin``, ``Greek``, ``German``, ``French``, ``Italian``, ``Danish``, ``Summary``, ``Notes``, ``Commentary``, ``Folio``, ``Pseudocode``, ``Proposition``, ``Video``, ``Code``, ``Heath``, ``Overview``. Never mix short codes (``EN``, ``FR``, ``EL``), native spellings (``Deutsch``, ``Français``), or edition dates inside track pills.

----

4. ``1280×640px`` Social & GitHub Banners
-----------------------------------------

* Run ``publish social-banner --force`` to generate ``1280×640px`` OpenGraph banners (``docsrc/_static/social/banner.png`` and ``<book>.png``) alongside the ``1280×640px`` GitHub repository social preview banner (``docsrc/_static/social/github.png``).
