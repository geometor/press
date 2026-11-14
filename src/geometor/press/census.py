"""Read-only workspace census scanner for GEOMETOR repositories."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import tomllib
from typing import Any

DEFAULT_CENSUS_JSON = Path(__file__).resolve().parents[3] / "resources" / "census.json"

SKIP_DIRS = frozenset(
    {
        ".agents",
        ".config",
        ".github",
        ".venv",
        "_demos",
        "_refs",
        "dist",
        "pypi_test_env",
        "todos",
        "uv_test_env",
    }
)


@dataclass(frozen=True)
class RepoCensus:
    """Empirical file and codex snapshot for a single GEOMETOR repository."""

    name: str
    has_git: bool
    version: str
    pkg_desc: str
    readme_title: str
    readme_blurb: str
    pdfs: int
    folio_pngs: int
    folio_rsts: int
    res_svgs: int
    has_apparatus: bool
    has_docsrc: bool
    docsrc_rsts: int
    docsrc_svgs: int
    book_subtrees: tuple[dict[str, str], ...]
    has_docs: bool
    py_files: int
    has_videos: bool
    has_demos: bool


def _peek_rst_meta(rst_path: Path) -> dict[str, str]:
    meta: dict[str, str] = {}
    try:
        text = rst_path.read_text(encoding="utf-8", errors="ignore")[:3000]
        for line in text.splitlines()[:30]:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(":") and ":" in stripped[1:]:
                parts = stripped[1:].split(":", 1)
                if len(parts) == 2:
                    meta[parts[0].strip()] = parts[1].strip()
            elif not stripped.startswith(".."):
                break
    except OSError:
        pass
    return meta


def _first_heading_or_summary(readme_path: Path) -> tuple[str, str]:
    if not readme_path.is_file():
        return ("", "")
    text = readme_path.read_text(encoding="utf-8", errors="ignore")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    cleaned = [
        ln.lstrip("# ").strip()
        for ln in lines
        if not re.fullmatch(r"[=\-~#*`^\"']+", ln)
    ]
    title = cleaned[0] if cleaned else ""
    blurb = ""
    for ln in cleaned[1:8]:
        if ln.lower() not in {"overview", "introduction", "description"} and len(ln) > 25:
            blurb = ln[:220]
            break
    return (title, blurb)


def scan_repo(repo_dir: Path) -> RepoCensus:
    """Inspect a single repository directory without modifying any files.

    Args:
        repo_dir: Path to the repository directory.

    Returns:
        Populated :class:`RepoCensus` snapshot.
    """
    name = repo_dir.name
    has_git = (repo_dir / ".git").exists()
    pyproject = repo_dir / "pyproject.toml"
    version = ""
    pkg_desc = ""
    if pyproject.is_file():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            proj = data.get("project", {})
            version = str(proj.get("version", ""))
            pkg_desc = str(proj.get("description", ""))
        except (OSError, tomllib.TOMLDecodeError):
            pass

    if not version and (repo_dir / "src").is_dir():
        for init_py in (repo_dir / "src").rglob("__init__.py"):
            txt = init_py.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', txt)
            if match:
                version = match.group(1)
                break

    readme_rst = repo_dir / "README.rst"
    readme_md = repo_dir / "README.md"
    readme_title, readme_blurb = _first_heading_or_summary(
        readme_rst if readme_rst.is_file() else readme_md
    )

    res_dir = repo_dir / "resources"
    pdfs = 0
    folio_pngs = 0
    folio_rsts = 0
    res_svgs = 0
    has_apparatus = False
    if res_dir.is_dir():
        edition_dirs = [
            sub.name
            for sub in sorted(res_dir.iterdir())
            if sub.is_dir() and not sub.name.startswith(".")
        ]
        pdfs = sum(1 for _ in res_dir.rglob("*.pdf"))
        folio_pngs = sum(
            1 for p in res_dir.rglob("*.png") if re.match(r"^\d{3,4}\.png$", p.name)
        )
        folio_rsts = sum(
            1 for p in res_dir.rglob("*.rst") if re.match(r"^\d{3,4}\.rst$", p.name)
        )
        res_svgs = sum(1 for _ in res_dir.rglob("*.svg"))
        has_apparatus = any(
            (res_dir / ed / fn).is_file()
            for ed in edition_dirs
            for fn in ("persons.json", "citations.json", "glossary.json")
        ) or any(
            (res_dir / fn).is_file()
            for fn in ("persons.json", "citations.json", "glossary.json")
        )

    docsrc_dir = repo_dir / "docsrc"
    has_docsrc = docsrc_dir.is_dir()
    docsrc_rsts = 0
    docsrc_svgs = 0
    book_subtrees: list[dict[str, str]] = []
    if has_docsrc:
        docsrc_rsts = sum(
            1
            for p in docsrc_dir.rglob("*.rst")
            if "modules/api" not in str(p) and ".archive" not in str(p)
        )
        docsrc_svgs = sum(1 for _ in docsrc_dir.rglob("*.svg"))
        for sub in sorted(docsrc_dir.iterdir()):
            idx = sub / "index.rst"
            if sub.is_dir() and not sub.name.startswith((".", "_")) and idx.is_file():
                meta = _peek_rst_meta(idx)
                if meta.get("layout") == "book" or "book_title" in meta:
                    book_subtrees.append(
                        {
                            "slug": sub.name,
                            "book_title": meta.get("book_title")
                            or meta.get("title")
                            or sub.name,
                            "subtitle": meta.get("book_subtitle")
                            or meta.get("subtitle")
                            or "",
                            "author": meta.get("author", ""),
                            "year": meta.get("year", ""),
                        }
                    )
        if not book_subtrees and (docsrc_dir / "index.rst").is_file():
            meta = _peek_rst_meta(docsrc_dir / "index.rst")
            if meta.get("layout") == "book" or "book_title" in meta:
                book_subtrees.append(
                    {
                        "slug": ".",
                        "book_title": meta.get("book_title")
                        or meta.get("title")
                        or name,
                        "subtitle": meta.get("book_subtitle")
                        or meta.get("subtitle")
                        or "",
                        "author": meta.get("author", ""),
                        "year": meta.get("year", ""),
                    }
                )

    has_docs = (repo_dir / "docs" / "index.html").is_file()
    py_files = (
        sum(1 for _ in (repo_dir / "src").rglob("*.py"))
        if (repo_dir / "src").is_dir()
        else 0
    )
    has_videos = (repo_dir / "videos").is_dir() or (repo_dir / "episodes").is_dir()
    has_demos = (repo_dir / "demos").is_dir()

    return RepoCensus(
        name=name,
        has_git=has_git,
        version=version,
        pkg_desc=pkg_desc,
        readme_title=readme_title,
        readme_blurb=readme_blurb,
        pdfs=pdfs,
        folio_pngs=folio_pngs,
        folio_rsts=folio_rsts,
        res_svgs=res_svgs,
        has_apparatus=has_apparatus,
        has_docsrc=has_docsrc,
        docsrc_rsts=docsrc_rsts,
        docsrc_svgs=docsrc_svgs,
        book_subtrees=tuple(book_subtrees),
        has_docs=has_docs,
        py_files=py_files,
        has_videos=has_videos,
        has_demos=has_demos,
    )


def scan_workspace(workspace_root: Path) -> list[RepoCensus]:
    """Scan all repositories under ``workspace_root`` in sorted order."""
    records: list[RepoCensus] = []
    for entry in sorted(workspace_root.iterdir()):
        if not entry.is_dir() or entry.name in SKIP_DIRS or entry.name.startswith("."):
            continue
        records.append(scan_repo(entry))
    return records


def load_census_snapshot(path: Path | None = None) -> list[RepoCensus]:
    """Load cached census records from ``resources/census.json``."""
    target = path if path is not None else DEFAULT_CENSUS_JSON
    raw_list: list[dict[str, Any]] = json.loads(target.read_text(encoding="utf-8"))
    records: list[RepoCensus] = []
    for item in raw_list:
        records.append(
            RepoCensus(
                name=str(item["name"]),
                has_git=bool(item["has_git"]),
                version=str(item.get("version", "")),
                pkg_desc=str(item.get("pkg_desc", "")),
                readme_title=str(item.get("readme_title", "")),
                readme_blurb=str(item.get("readme_blurb", "")),
                pdfs=int(item.get("pdfs", 0)),
                folio_pngs=int(item.get("folio_pngs", 0)),
                folio_rsts=int(item.get("folio_rsts", 0)),
                res_svgs=int(item.get("res_svgs", 0)),
                has_apparatus=bool(item.get("has_apparatus", False)),
                has_docsrc=bool(item.get("has_docsrc", False)),
                docsrc_rsts=int(item.get("docsrc_rsts", 0)),
                docsrc_svgs=int(item.get("docsrc_svgs", 0)),
                book_subtrees=tuple(item.get("book_subtrees", [])),
                has_docs=bool(item.get("has_docs", False)),
                py_files=int(item.get("py_files", 0)),
                has_videos=bool(item.get("has_videos", False)),
                has_demos=bool(item.get("has_demos", False)),
            )
        )
    return records


def write_census_json(records: list[RepoCensus], output_path: Path) -> None:
    """Serialize census records to formatted JSON."""
    payload = [
        {**asdict(rec), "book_subtrees": list(rec.book_subtrees)}
        for rec in records
    ]
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
