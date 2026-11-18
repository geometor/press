"""Command-line interface for inspecting the GEOMETOR Press shelf and census."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .census import DEFAULT_CENSUS_JSON, scan_workspace, write_census_json
from .shelf import ShelfCatalog, load_shelf


def _print_summary(catalog: ShelfCatalog) -> None:
    counts = catalog.summary_counts()
    print(f"{catalog.imprint.name} — {catalog.imprint.tagline}")
    print(f"Engine: {catalog.imprint.engine} | Portal: {catalog.imprint.portal}")
    print("-" * 76)
    print(
        f"Repositories: {counts['repositories']} | "
        f"Book Works: {counts['works']} | "
        f"RST Docs: {counts['docsrc_rst']:,} | "
        f"Folios: {counts['folios']:,} | "
        f"SVGs: {counts['svgs']:,}"
    )
    print("\nReadiness Stages:")
    for stage, num in counts["stages"].items():
        print(f"  - {stage:22s}: {num:2d} repos")
    print("\nSpine Series:")
    for key, num in counts["series"].items():
        spec = catalog.series.get(key)
        label = f"{spec.title} ({spec.accent})" if spec else key
        print(f"  - {key:16s}: {num:2d} repos  [{label}]")
    print("\nDerived Tactile & Digital Products:")
    for kind, num in counts["derived_products"].items():
        print(f"  - {kind:18s}: {num:2d} product lines")


def _print_shelf(
    catalog: ShelfCatalog,
    stage: str | None = None,
    series: str | None = None,
) -> None:
    entries = list(catalog.entries)
    if stage:
        entries = [e for e in entries if e.stage == stage]
    if series:
        entries = [e for e in entries if e.series == series]

    header = f"{'REPO':18s} | {'SERIES':12s} | {'STAGE':20s} | {'WORKS':5s} | {'TITLE'}"
    print(header)
    print("-" * len(header))
    for entry in entries:
        first_title = entry.works[0].title if entry.works else "(Infrastructure / App)"
        print(
            f"{entry.repo:18s} | {entry.series:12s} | {entry.stage:20s} | "
            f"{len(entry.works):5d} | {first_title[:56]}"
        )


def _print_products(catalog: ShelfCatalog, kind: str | None = None) -> None:
    items = catalog.all_derived_products(kind=kind)
    header = f"{'KIND':16s} | {'REPO':16s} | {'PRODUCT TITLE'}"
    print(header)
    print("-" * len(header))
    for entry, prod in items:
        print(f"{prod.kind:16s} | {entry.repo:16s} | {prod.title}")


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser for ``geometor-press``."""
    parser = argparse.ArgumentParser(
        prog="press",
        description="GEOMETOR Press — Shelf Manifest, Product Matrix & Workspace Census CLI.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("summary", help="Display imprint, stage, series, and product totals.")

    shelf_p = sub.add_parser("shelf", help="List cataloged repositories and book works.")
    shelf_p.add_argument("--stage", default=None, help="Filter by readiness stage.")
    shelf_p.add_argument("--series", default=None, help="Filter by spine series key.")

    prod_p = sub.add_parser(
        "products",
        help="List derived card decks, greeting cards, posters, and apps.",
    )
    prod_p.add_argument(
        "--kind",
        default=None,
        choices=["cards_collector", "cards_greeting", "poster", "app"],
        help="Filter by product kind.",
    )

    census_p = sub.add_parser(
        "census",
        help="Run live read-only repository census across the GEOMETOR workspace.",
    )
    census_p.add_argument(
        "--workspace",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor"),
        help="Path to the GEOMETOR workspace root.",
    )
    census_p.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_CENSUS_JSON,
        help="Output JSON path for census snapshot.",
    )

    ct_p = sub.add_parser(
        "coffee-table",
        help="Build a facing-page spread Coffee Table Book PDF (e.g., for divine).",
    )
    ct_p.add_argument(
        "--repo",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/divine"),
        help="Path to the source repository (default: geometor/divine).",
    )
    ct_p.add_argument(
        "--output",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/press/editions/divine/golden_constructions_coffee_table.pdf"),
        help="Output PDF file path.",
    )
    ct_p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on number of constructions to include (for quick previews).",
    )
    ct_p.add_argument(
        "--layout",
        choices=["spread", "phi-horz", "phi-vert"],
        default="spread",
        help="Page layout: 10x10 facing spread or 1:phi single-page horz/vert.",
    )

    cover_p = sub.add_parser(
        "coffee-table-cover",
        help="Build full-bleed hardcover wrap cover PDF for Golden Constructions.",
    )
    cover_p.add_argument(
        "--repo",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/divine"),
        help="Path to the divine repository.",
    )
    cover_p.add_argument(
        "--output",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/press/editions/divine/golden_constructions_wrap_cover.pdf"),
        help="Output PDF file path.",
    )
    cover_p.add_argument(
        "--spine-width",
        type=float,
        default=0.42,
        help="Spine width in inches (default: 0.42).",
    )

    cards_p = sub.add_parser(
        "collector-cards",
        help="Build a 52-card Tarot-format duplex Collector Deck PDF (The Golden Deck).",
    )
    cards_p.add_argument(
        "--repo",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/divine"),
        help="Path to the source repository (default: geometor/divine).",
    )
    cards_p.add_argument(
        "--output",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/press/editions/divine/the_golden_deck_52_cards.pdf"),
        help="Output PDF file path.",
    )
    cards_p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on number of constructions to include.",
    )

    euclid_p = sub.add_parser(
        "euclid-pdf",
        help="Build a 6in x 9in Scholarly Trade Codex PDF for Euclid's Elements.",
    )
    euclid_p.add_argument(
        "--repo",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/euclid"),
        help="Path to the euclid repository.",
    )
    euclid_p.add_argument(
        "--volume",
        default="volume_I",
        help="Volume directory (default: volume_I).",
    )
    euclid_p.add_argument(
        "--book",
        default="book_i",
        help="Book directory (default: book_i).",
    )
    euclid_p.add_argument(
        "--output",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/press/editions/euclid/euclid_book_i_trade.pdf"),
        help="Output PDF file path.",
    )
    euclid_p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on number of propositions.",
    )

    byrne_p = sub.add_parser(
        "byrne-pdf",
        help="Build an 8.5in x 11in Polychrome Fine-Color Quarto PDF for Byrne's Euclid.",
    )
    byrne_p.add_argument(
        "--repo",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/byrne"),
        help="Path to the byrne repository.",
    )
    byrne_p.add_argument(
        "--output",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/press/editions/byrne/byrne_polychrome_quarto.pdf"),
        help="Output PDF file path.",
    )
    byrne_p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on number of propositions.",
    )

    kepler_p = sub.add_parser(
        "kepler-pdf",
        help="Build a 6in x 9in Trade Monograph PDF for Kepler's Geometric Trilogy.",
    )
    kepler_p.add_argument(
        "--repo",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/kepler"),
        help="Path to the kepler repository.",
    )
    kepler_p.add_argument(
        "--output",
        type=Path,
        default=Path("/home/phi/PROJECTS/geometor/press/editions/kepler/kepler_trilogy_trade.pdf"),
        help="Output PDF file path.",
    )
    kepler_p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on number of sections.",
    )

    return parser


def run_cli(argv: Sequence[str] | None = None) -> int:
    """Execute the ``press`` CLI and return a POSIX exit status.

    Args:
        argv: Optional command-line argument sequence; defaults to ``sys.argv[1:]``.

    Returns:
        Zero on clean completion.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "summary"

    if command == "census":
        records = scan_workspace(args.workspace)
        write_census_json(records, args.output)
        print(f"Scanned {len(records)} repositories -> {args.output}")
        return 0

    if command == "coffee-table":
        from .coffee_table import build_divine_coffee_table_pdf, build_divine_phi_page_pdf

        if args.layout == "spread":
            out = build_divine_coffee_table_pdf(args.repo, args.output, limit=args.limit)
        else:
            orient = "horz" if args.layout == "phi-horz" else "vert"
            out = build_divine_phi_page_pdf(
                args.repo, args.output, orientation=orient, limit=args.limit
            )
        print(f"Coffee Table Book PDF created -> {out}")
        return 0

    if command == "coffee-table-cover":
        from .coffee_table import build_divine_cover_pdf

        out = build_divine_cover_pdf(args.repo, args.output, spine_width_in=args.spine_width)
        print(f"Wrap Cover PDF created -> {out}")
        return 0

    if command == "collector-cards":
        from .collector_cards import build_golden_deck_pdf

        out = build_golden_deck_pdf(args.repo, args.output, limit=args.limit)
        print(f"Collector Deck PDF created -> {out}")
        return 0

    if command == "euclid-pdf":
        from .euclid_print import build_euclid_trade_pdf

        out = build_euclid_trade_pdf(
            args.repo,
            args.output,
            volume=args.volume,
            book=args.book,
            limit=args.limit,
        )
        print(f"Euclid Trade PDF created -> {out}")
        return 0

    if command == "byrne-pdf":
        from .byrne_print import build_byrne_quarto_pdf

        out = build_byrne_quarto_pdf(args.repo, args.output, limit=args.limit)
        print(f"Byrne Quarto PDF created -> {out}")
        return 0

    if command == "kepler-pdf":
        from .kepler_print import build_kepler_trilogy_pdf

        out = build_kepler_trilogy_pdf(args.repo, args.output, limit=args.limit)
        print(f"Kepler Trade PDF created -> {out}")
        return 0

    catalog = load_shelf()
    if command == "summary":
        _print_summary(catalog)
    elif command == "shelf":
        _print_shelf(catalog, stage=args.stage, series=args.series)
    elif command == "products":
        _print_products(catalog, kind=args.kind)
    return 0


def main() -> None:
    """Console script entry point."""
    raise SystemExit(run_cli())
