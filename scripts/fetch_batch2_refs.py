"""Fetch verified public-domain Batch 2 reference portraits from Wikimedia Commons."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

REFS_DIR = Path(__file__).resolve().parents[1] / "resources" / "portraits_ref"
REFS_DIR.mkdir(parents=True, exist_ok=True)

BATCH2_FILES: dict[str, list[str]] = {
    "archimedes": [
        "File:Domenico-Fetti Archimedes 1620.jpg",
        "File:Domenico Fetti - Portrait of a Scholar - WGA07862.jpg",
    ],
    "aquinas": [
        "File:St-thomas-aquinas.jpg",
        "File:Saint Thomas Aquinas (Crivelli, 15th-century).jpg",
    ],
    "pascal": [
        "File:Blaise_Pascal_Versailles.JPG",
        "File:Blaise_pascal.jpg",
    ],
    "steiner": [
        "File:Jakob Steiner portrait 1881.jpg",
        "File:JakobSteiner.jpg",
    ],
    "byrne": [
        "File:Oliver Byrne Portrait (ca 1850).jpg",
    ],
    "hilbert": [
        "File:Hilbert.jpg",
    ],
    "bertrand_russell": [
        "File:Bertrand Russell, 1907.jpg",
        "File:Russell1907-2.jpg",
    ],
    "heath": [
        "File:Thomas Little Heath.jpg",
    ],
}

HEADERS = {
    "User-Agent": "GEOMETORPressAtelier/0.1 (https://geometor.com; educational geometric portrait study)",
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
    """Download URL to dest and normalize to RGB JPEG if needed."""
    req = urllib.request.Request(url, headers=HEADERS)
    tmp = dest.with_suffix(".tmp")
    with urllib.request.urlopen(req, timeout=30) as resp:
        tmp.write_bytes(resp.read())
    with Image.open(tmp) as img:
        rgb = img.convert("RGB")
        rgb.save(dest, format="JPEG", quality=92)
    tmp.unlink(missing_ok=True)


def main() -> None:
    """Download and verify all 8 Batch 2 portrait references."""
    for pid, candidates in BATCH2_FILES.items():
        dest = REFS_DIR / f"{pid}_ref.jpg"
        if dest.is_file() and dest.stat().st_size > 10_000:
            with Image.open(dest) as img:
                print(f"[SKIP] {pid}: {dest.name} ({img.size[0]}x{img.size[1]})")
            continue
        ok = False
        for title in candidates:
            try:
                url = resolve_commons_url(title)
                if not url:
                    continue
                download_file(url, dest)
                with Image.open(dest) as img:
                    print(f"[OK]   {pid}: {title} -> {dest.name} ({img.size[0]}x{img.size[1]})")
                ok = True
                break
            except Exception as exc:
                print(f"[WARN] {pid} ({title}): {exc}")
        if not ok:
            raise RuntimeError(f"Failed to download reference image for {pid}")


if __name__ == "__main__":
    main()
