"""Fetch all remaining verified Wikimedia Commons reference portraits listed in portraits.json."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = REPO_ROOT / "resources" / "portraits.json"
REFS_DIR = REPO_ROOT / "resources" / "portraits_ref"
REFS_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "GEOMETORPressAtelier/0.1 (https://geometor.com; educational geometric portrait study)",
}

FALLBACKS: dict[str, list[str]] = {
    "ptolemy": ["File:Giusto di gand e pedro berruguete, tolomeo.jpg"],
    "ernst-haeckel": ["File:Ernst Haeckel 5.jpg"],
    "petersen": ["File:Petersen Julius.jpg"],
    "pasch": ["File:Moritz Pasch (mathematician).jpg"],
    "klein": ["File:Felix Klein.jpeg"],
    "poincare": ["File:Henri Poincaré, PA03199.jpg"],
    "thompson": ["File:D'arcy Wentworth Thompson, ca. 1906.jpg", "File:D'Arcy Wenthworth Thompson.jpg"],
    "leonardo": ["File:Attributed to Francesco Melzi - RCIN 912726, A portrait of Leonardo c.1515-18.jpg"],
    "livio": ["File:Mario Livio, 2017.jpg"],
}


def resolve_commons_url(file_title: str) -> str | None:
    """Resolve direct image URL via Wikimedia Commons API (preferring ~1200px thumb or original)."""
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": file_title,
            "prop": "imageinfo",
            "iiprop": "url|size",
            "iiurlwidth": "1200",
            "format": "json",
        }
    )
    api_url = f"https://commons.wikimedia.org/w/api.php?{params}"
    req = urllib.request.Request(api_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if infos:
            info = infos[0]
            return str(info.get("thumburl") or info.get("url") or "")
    return None


def download_file(url: str, dest: Path) -> None:
    """Download URL to dest and normalize to RGB JPEG."""
    req = urllib.request.Request(url, headers=HEADERS)
    tmp = dest.with_suffix(".tmp")
    with urllib.request.urlopen(req, timeout=30) as resp:
        tmp.write_bytes(resp.read())
    with Image.open(tmp) as img:
        rgb = img.convert("RGB")
        rgb.save(dest, format="JPEG", quality=92)
    tmp.unlink(missing_ok=True)


def main() -> None:
    """Download and verify all remaining Wikimedia portrait references from portraits.json."""
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    ok_count = 0
    fail_list: list[str] = []

    for entry in payload.get("portraits", []):
        if entry.get("status") == "complete":
            continue
        ref = entry.get("reference") or {}
        primary_file = str(ref.get("wikimedia_file") or "").strip()
        if not primary_file:
            continue

        pid = str(entry["id"])
        slug = pid.replace("-", "_")
        dest = REFS_DIR / f"{slug}_ref.jpg"
        if dest.is_file() and dest.stat().st_size > 4_000:
            with Image.open(dest) as img:
                print(f"[SKIP] {pid}: {dest.name} ({img.size[0]}x{img.size[1]})")
            ok_count += 1
            continue

        candidates = [primary_file, *FALLBACKS.get(pid, [])]
        downloaded = False
        for title in candidates:
            try:
                url = resolve_commons_url(title)
                if not url:
                    print(f"[MISS] {pid}: no imageinfo for {title}")
                    continue
                download_file(url, dest)
                with Image.open(dest) as img:
                    print(f"[OK]   {pid}: {title} -> {dest.name} ({img.size[0]}x{img.size[1]})")
                entry["reference"]["local_ref"] = f"resources/portraits_ref/{slug}_ref.jpg"
                downloaded = True
                ok_count += 1
                time.sleep(0.35)
                break
            except Exception as exc:
                print(f"[WARN] {pid} ({title}): {exc}")
                time.sleep(0.5)
        if not downloaded:
            fail_list.append(pid)

    JSON_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Summary: {ok_count} references ready; {len(fail_list)} failed: {fail_list}")


if __name__ == "__main__":
    main()
