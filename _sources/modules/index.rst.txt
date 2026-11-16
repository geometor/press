:navigation: header
:order: 95

=======
Modules
=======

``geometor.press`` provides typed data structures, workspace census scanners, and CLI tools over ``resources/shelf.yaml`` and ``resources/census.json``:

- :mod:`geometor.press` — Public package interface exporting :class:`~geometor.press.shelf.ShelfCatalog`, :func:`~geometor.press.shelf.load_shelf`, :class:`~geometor.press.census.RepoCensus`, :func:`~geometor.press.census.scan_workspace`, and :func:`~geometor.press.cli.run_cli`.
- :mod:`geometor.press.shelf` — Immutable Python 3.13 dataclasses (:class:`~geometor.press.shelf.ImprintProfile`, :class:`~geometor.press.shelf.SeriesSpec`, :class:`~geometor.press.shelf.CatalogEntry`, :class:`~geometor.press.shelf.WorkSpec`, :class:`~geometor.press.shelf.DerivedProduct`) and query filters across readiness stages, spine series, and derived tactile products.
- :mod:`geometor.press.census` — Read-only repository scanner inspecting ``pyproject.toml``, ``resources/`` folios and apparatus, ``docsrc/`` ``:layout: book`` subtrees, SVGs, and compiled ``docs/``.
- :mod:`geometor.press.cli` — Command-line explorer (``press summary``, ``press shelf``, ``press products``, ``press census``).
