"""Sphinx configuration for GEOMETOR Press."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import sys

_REPO_ROOT = Path(__file__).resolve().parents[1]
_WORKSPACE_ROOT = _REPO_ROOT.parent
for _extra_path in (
    _REPO_ROOT / "src",
    _WORKSPACE_ROOT / ".venv" / "lib" / "python3.13" / "site-packages",
):
    if _extra_path.exists() and str(_extra_path) not in sys.path:
        sys.path.insert(0, str(_extra_path))

# Keep docsrc/_static/studios synchronized with canonical demos/*.html
_STUDIOS_DIR = _REPO_ROOT / "docsrc" / "_static" / "studios"
_STUDIOS_DIR.mkdir(parents=True, exist_ok=True)
for _demo_html in (_REPO_ROOT / "demos").glob("*.html"):
    shutil.copy2(_demo_html, _STUDIOS_DIR / _demo_html.name)

from photon_platform.publish.global_conf import *  # noqa: E402, F403

import geometor.press as module  # noqa: E402

version = module.__version__

org = "geometor"
org_name = "GEOMETOR"

repo = "press"
repo_name = "press"

setup_globals(org, org_name, repo, repo_name)  # noqa: F405
site_title = "Digital Scriptorium Press"
project = site_title
html_title = f"{site_title} • {org_name}"

# Configure offline-safe local intersphinx inventories across the GEOMETOR workspace
for _remote_key in list(intersphinx_mapping.keys()):  # noqa: F405
    _entry = intersphinx_mapping[_remote_key]  # noqa: F405
    if _entry[1] is None:
        intersphinx_mapping.pop(_remote_key, None)  # noqa: F405

for _sister in (
    "euclid",
    "elements",
    "divine",
    "etc",
    "pacioli",
    "hoenen",
    "plato",
    "codes",
):
    _inv = _WORKSPACE_ROOT / _sister / "docs" / "objects.inv"
    if _inv.is_file():
        intersphinx_mapping[_sister] = (  # noqa: F405
            f"https://geometor.github.io/{_sister}",
            (os.fspath(_inv), None),
        )

html_theme = "foundation"
html_title = "GEOMETOR Press"
blog_title = "GEOMETOR Press"
project = "GEOMETOR Press"
html_static_path: list[str] = ["_static"]
autoapi_add_toctree_entry = False
if "intro.rst" not in exclude_patterns:  # noqa: F405
    exclude_patterns.append("intro.rst")  # noqa: F405
suppress_warnings = ["autoapi.python_import_resolution", "toc.not_included"]
