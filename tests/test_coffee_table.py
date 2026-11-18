"""Tests for the GEOMETOR Press Coffee Table Book PDF generator."""

from __future__ import annotations

from pathlib import Path

from geometor.press.coffee_table import (
    build_divine_coffee_table_html,
    latex_to_html,
    rst_inline_to_html,
)


def test_latex_to_html_handles_nested_frac_and_sqrt() -> None:
    """Nested fractions and square roots convert cleanly without stray commands."""
    rendered = latex_to_html(r"\frac{\sqrt{5}}{2} + \tfrac{3}{2} = \phi^2")
    assert r"\frac" not in rendered
    assert r"\tfrac" not in rendered
    assert "√5" in rendered
    assert "φ²" in rendered


def test_rst_inline_to_html_formats_roles() -> None:
    """RST roles (:g:, :person:, :math:) render as styled HTML spans."""
    rendered = rst_inline_to_html(
        "By :person:`Euclid <euclid>`, segment :g:`AB` satisfies :math:`|AG|/|GB| = \\phi`."
    )
    assert "Euclid" in rendered
    assert '<span class="g-token">AB</span>' in rendered
    assert "φ" in rendered


def test_build_divine_coffee_table_html_preview() -> None:
    """Building HTML for divine constructs valid facing-page spread markup."""
    divine_repo = Path("/home/phi/PROJECTS/geometor/divine")
    html = build_divine_coffee_table_html(divine_repo, limit=2)
    assert "Golden Constructions" in html
    assert "GC-01.01" in html
    assert "Plate 01" in html
    assert "stroke: none;" in html
