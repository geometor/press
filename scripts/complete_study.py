"""Mark a portrait study complete in portraits.{json,yaml} and refresh gallery + live poster."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from build_portraits_poster import build_poster  # noqa: E402
from sync_gallery_html import main as sync_gallery  # noqa: E402
from update_pantheon_manifest import JSON_PATH, YAML_PATH, _dump_yaml  # noqa: E402


def mark_complete(study_id: str) -> None:
    """Set study_id status to complete with SVG output paths and refresh gallery & live poster."""
    mod_name = study_id.replace("-", "_")
    dark_rel = f"docsrc/_static/portraits/{mod_name}_dark.svg"
    light_rel = f"docsrc/_static/portraits/{mod_name}_light.svg"
    for rel in (dark_rel, light_rel):
        if not (REPO_ROOT / rel).is_file():
            raise FileNotFoundError(f"Missing exported SVG: {REPO_ROOT / rel}")

    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    found = False
    for entry in payload["portraits"]:
        if entry["id"] == study_id:
            entry["status"] = "complete"
            entry["outputs"] = {"dark_svg": dark_rel, "light_svg": light_rel}
            found = True
            break
    if not found:
        raise KeyError(f"Unknown portrait id: {study_id}")

    JSON_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    YAML_PATH.write_text("\n".join(_dump_yaml(payload)) + "\n", encoding="utf-8")
    sync_gallery()
    build_poster()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: complete_study.py <study_id>")
    mark_complete(sys.argv[1])
