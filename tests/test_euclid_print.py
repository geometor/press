"""Tests for the Euclid 6x9 Trade Codex PDF generator and wrap cover."""

from __future__ import annotations

from pathlib import Path

from geometor.press.coffee_table import build_divine_cover_html
from geometor.press.euclid_print import build_euclid_trade_html


def test_build_divine_cover_html() -> None:
    """Wrap cover HTML renders front, spine, and back panels."""
    html = build_divine_cover_html(Path("/home/phi/PROJECTS/geometor/divine"))
    assert "Golden Constructions" in html
    assert "panel-spine" in html
    assert "ISBN / BARCODE AREA" in html


def test_build_euclid_trade_html_book_i_preview() -> None:
    """Euclid Book I trade HTML renders propositions and SVGs cleanly."""
    html = build_euclid_trade_html(Path("/home/phi/PROJECTS/geometor/euclid"), limit=3)
    assert "Proposition I.1" in html
    assert "equilateral triangle" in html
    assert "stroke: none;" in html
