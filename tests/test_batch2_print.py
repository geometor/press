"""Tests for Byrne Polychrome Quarto and Kepler Trilogy Trade PDF generators."""

from __future__ import annotations

from pathlib import Path

from geometor.press.byrne_print import build_byrne_quarto_html
from geometor.press.kepler_print import build_kepler_trilogy_html


def test_build_byrne_quarto_html_preview() -> None:
    """Byrne quarto HTML renders colored glyph spans and SVG plates."""
    html = build_byrne_quarto_html(Path("/home/phi/PROJECTS/geometor/byrne"), limit=2)
    assert "Proposition I.1" in html
    assert "byrne-sym" in html
    assert "#d62828" in html


def test_build_kepler_trilogy_html_preview() -> None:
    """Kepler trilogy HTML renders Mysterium, Strena, and Harmonices sections."""
    html = build_kepler_trilogy_html(Path("/home/phi/PROJECTS/geometor/kepler"))
    assert "Mysterium Cosmographicum" in html
    assert "Strena seu de Nive Sexangula" in html
    assert "Harmonices Mundi" in html
