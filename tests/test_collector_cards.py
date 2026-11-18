"""Tests for the GEOMETOR Press Collector Deck PDF generator."""

from __future__ import annotations

from pathlib import Path

from geometor.press.collector_cards import build_golden_deck_html


def test_build_golden_deck_html_contains_52_cards() -> None:
    """Full Golden Deck HTML contains 7 family keys + 45 constructions (104 faces)."""
    divine_repo = Path("/home/phi/PROJECTS/geometor/divine")
    html = build_golden_deck_html(divine_repo)
    assert html.count('<article class="card ') == 104
    assert "· KEY" in html
    assert "GC-01.01" in html
    assert "THE GOLDEN DECK" in html
