"""Initialize or update the 48-slot GEOMETOR Pantheon in resources/portraits.{json,yaml}."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]


def _yaml_scalar(val: Any) -> str:
    """Serialize a scalar value as valid YAML."""
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    return json.dumps(str(val), ensure_ascii=False)


def _dump_yaml(obj: Any, indent: int = 0) -> list[str]:
    """Minimal deterministic YAML dumper for portraits manifest dictionaries/lists."""
    pad = "  " * indent
    lines: list[str] = []
    if isinstance(obj, dict):
        if not obj:
            return [f"{pad}{{}}"]
        for k, v in obj.items():
            if isinstance(v, dict):
                if not v:
                    lines.append(f"{pad}{k}: {{}}")
                else:
                    lines.append(f"{pad}{k}:")
                    lines.extend(_dump_yaml(v, indent + 1))
            elif isinstance(v, list):
                if not v:
                    lines.append(f"{pad}{k}: []")
                elif all(not isinstance(item, (dict, list)) for item in v):
                    items = ", ".join(_yaml_scalar(item) for item in v)
                    lines.append(f"{pad}{k}: [{items}]")
                else:
                    lines.append(f"{pad}{k}:")
                    lines.extend(_dump_yaml(v, indent + 1))
            else:
                lines.append(f"{pad}{k}: {_yaml_scalar(v)}")
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    prefix = f"{pad}- " if first else f"{pad}  "
                    first = False
                    if isinstance(v, dict):
                        if not v:
                            lines.append(f"{prefix}{k}: {{}}")
                        else:
                            lines.append(f"{prefix}{k}:")
                            lines.extend(_dump_yaml(v, indent + 2))
                    elif isinstance(v, list):
                        if not v:
                            lines.append(f"{prefix}{k}: []")
                        elif all(not isinstance(sub, (dict, list)) for sub in v):
                            items = ", ".join(_yaml_scalar(sub) for sub in v)
                            lines.append(f"{prefix}{k}: [{items}]")
                        else:
                            lines.append(f"{prefix}{k}:")
                            lines.extend(_dump_yaml(v, indent + 2))
                    else:
                        lines.append(f"{prefix}{k}: {_yaml_scalar(v)}")
            else:
                lines.append(f"{pad}- {_yaml_scalar(item)}")
    return lines
JSON_PATH = REPO_ROOT / "resources" / "portraits.json"
YAML_PATH = REPO_ROOT / "resources" / "portraits.yaml"

BIRTH_YEARS_EXISTING: dict[str, int] = {
    "durer": 1471,
    "euclid": -325,
    "plato": -428,
    "aristotle": -384,
    "pacioli": 1447,
    "kepler": 1571,
    "euler": 1707,
}

NEW_ENTRIES: list[dict[str, Any]] = [
    # Batch 2 (Studies 08-15 — Researched & Staged)
    {
        "id": "archimedes",
        "name": "Archimedes of Syracuse",
        "dates": "c. 287 - c. 212 BCE",
        "birth_year": -287,
        "era": "Antiquity",
        "repo": "archimedes",
        "status": "researched",
        "queue_order": 7,
        "pose": "Three-quarter right scholar leaning over instruments",
        "reference": {
            "title": "Portrait of a Scholar (Archimedes)",
            "artist": "Domenico Fetti (c. 1620)",
            "holding": "Gemäldegalerie Alte Meister, Dresden",
            "rights": "Public Domain",
            "wikimedia_file": "File:Domenico-Fetti Archimedes 1620.jpg",
            "url": "https://commons.wikimedia.org/wiki/File:Domenico-Fetti_Archimedes_1620.jpg",
            "local_ref": "resources/portraits_ref/archimedes_ref.jpg",
        },
        "signature_motif": "Circumscribed Cylinder & Inscribed Sphere (2:3) + Hexagon pi Bounds",
        "outputs": {},
        "notes": "Focus on domed forehead, furrowed brow, and curled scholar beard.",
    },
    {
        "id": "aquinas",
        "name": "St. Thomas Aquinas",
        "dates": "1225 - 1274",
        "birth_year": 1225,
        "era": "Medieval",
        "repo": "aquinas",
        "status": "researched",
        "queue_order": 8,
        "pose": "Three-quarter left in Dominican tonsure and habit",
        "reference": {
            "title": "Saint Thomas Aquinas (1476, Demidoff Altarpiece)",
            "artist": "Carlo Crivelli",
            "holding": "National Gallery, London",
            "rights": "Public Domain",
            "wikimedia_file": "File:St-thomas-aquinas.jpg",
            "url": "https://commons.wikimedia.org/wiki/File:St-thomas-aquinas.jpg",
            "local_ref": "resources/portraits_ref/aquinas_ref.jpg",
        },
        "signature_motif": "Radiant Sun of Materia Intelligibilis & Three Degrees of Abstraction",
        "outputs": {},
        "notes": "Clean Dominican tonsure ring and hooded collar lend themselves directly to concentric arcs.",
    },
    {
        "id": "pascal",
        "name": "Blaise Pascal",
        "dates": "1623 - 1662",
        "birth_year": 1623,
        "era": "Early Modern",
        "repo": "pascal",
        "status": "researched",
        "queue_order": 9,
        "pose": "Three-quarter right with flowing waves and white cravat collar",
        "reference": {
            "title": "Portrait of Blaise Pascal (after François II Quesnel, 1691)",
            "holding": "Palace of Versailles",
            "rights": "Public Domain",
            "wikimedia_file": "File:Blaise_Pascal_Versailles.JPG",
            "url": "https://commons.wikimedia.org/wiki/File:Blaise_Pascal_Versailles.JPG",
            "local_ref": "resources/portraits_ref/pascal_ref.jpg",
        },
        "signature_motif": "Hexagrammum Mysticum (Circle, Inscribed Hexagon & Pascal Line)",
        "outputs": {},
        "notes": "Iconic flowing Baroque hair waves via Euclid III.12 tangent arcs.",
    },
    {
        "id": "steiner",
        "name": "Jakob Steiner",
        "dates": "1796 - 1863",
        "birth_year": 1796,
        "era": "19th Century",
        "repo": "steiner",
        "status": "researched",
        "queue_order": 10,
        "pose": "Three-quarter left engraving in 19th-century high collar",
        "reference": {
            "title": "Jakob Steiner portrait (1881 Gesammelte Werke frontispiece)",
            "artist": "August Weger",
            "holding": "ETH Zürich / Gesammelte Werke",
            "rights": "Public Domain",
            "wikimedia_file": "File:Jakob Steiner portrait 1881.jpg",
            "url": "https://commons.wikimedia.org/wiki/File:Jakob_Steiner_portrait_1881.jpg",
            "local_ref": "resources/portraits_ref/steiner_ref.jpg",
        },
        "signature_motif": "Steiner Porism (Ring of Tangent Circles) & Poncelet-Steiner Circle",
        "outputs": {},
        "notes": "Crisp steel-engraving planes ideal for synthetic line-and-arc portraiture.",
    },
    {
        "id": "byrne",
        "name": "Oliver Byrne",
        "dates": "1810 - 1880",
        "birth_year": 1810,
        "era": "19th Century",
        "repo": "byrne",
        "status": "researched",
        "queue_order": 11,
        "pose": "Three-quarter Victorian bust portrait",
        "reference": {
            "title": "Oliver Byrne Portrait (c. 1850)",
            "holding": "Public Domain archival portrait",
            "rights": "Public Domain",
            "wikimedia_file": "File:Oliver Byrne Portrait (ca 1850).jpg",
            "url": "https://commons.wikimedia.org/wiki/File:Oliver_Byrne_Portrait_(ca_1850).jpg",
            "local_ref": "resources/portraits_ref/byrne_ref.jpg",
        },
        "signature_motif": "Elements I.47 Pythagorean Square-Dissection Diagram",
        "outputs": {},
        "notes": "Author of the 1847 polychrome Elements of Euclid.",
    },
    {
        "id": "hilbert",
        "name": "David Hilbert",
        "dates": "1862 - 1943",
        "birth_year": 1862,
        "era": "Modern",
        "repo": "hilbert",
        "status": "researched",
        "queue_order": 12,
        "pose": "Frontal / slight three-quarter with felt hat, pince-nez, and goatee",
        "reference": {
            "title": "David Hilbert (1912 Göttingen portrait)",
            "holding": "University of Göttingen / Wikimedia Commons",
            "rights": "Public Domain",
            "wikimedia_file": "File:Hilbert.jpg",
            "url": "https://commons.wikimedia.org/wiki/File:Hilbert.jpg",
            "local_ref": "resources/portraits_ref/hilbert_ref.jpg",
        },
        "signature_motif": "Pappus-Hilbert Incidence Configuration & Parallel-Axiom Grid",
        "outputs": {},
        "notes": "Circular pince-nez spectacles and sweeping hat brim are native compass geometry.",
    },
    {
        "id": "bertrand-russell",
        "name": "Bertrand Russell",
        "dates": "1872 - 1970",
        "birth_year": 1872,
        "era": "Modern",
        "repo": "bertrand-russell",
        "status": "researched",
        "queue_order": 13,
        "pose": "Three-quarter right Edwardian portrait with mustache",
        "reference": {
            "title": "Bertrand Russell (1907)",
            "holding": "Wikimedia Commons (PD-1923)",
            "rights": "Public Domain",
            "wikimedia_file": "File:Bertrand Russell, 1907.jpg",
            "url": "https://commons.wikimedia.org/wiki/File:Bertrand_Russell,_1907.jpg",
            "local_ref": "resources/portraits_ref/bertrand_russell_ref.jpg",
        },
        "signature_motif": "Projective Cross-Ratio Pencil & Intersecting Logic Circles",
        "outputs": {},
        "notes": "Author of An Essay on the Foundations of Geometry (1897).",
    },
    {
        "id": "heath",
        "name": "Sir Thomas Little Heath",
        "dates": "1861 - 1940",
        "birth_year": 1861,
        "era": "Modern",
        "repo": "euclid",
        "status": "researched",
        "queue_order": 14,
        "pose": "Three-quarter left studio portrait with mustache and wing collar",
        "reference": {
            "title": "Sir Thomas Little Heath (c. 1910)",
            "holding": "MacTutor / Royal Society Obituary",
            "rights": "Public Domain",
            "wikimedia_file": "File:Thomas Little Heath.jpg",
            "url": "https://commons.wikimedia.org/wiki/File:Thomas_Little_Heath.jpg",
            "local_ref": "resources/portraits_ref/heath_ref.jpg",
        },
        "signature_motif": "Greek Elements Scroll & Book XIII Golden Section / Regular Solids",
        "outputs": {},
        "notes": "Translator and commentator of Euclid, Archimedes, and Apollonius.",
    },
    # Remaining 33 Pantheon Slots (Queued for Archival Researchers R1, R2, R3)
    {"id": "apollonius", "name": "Apollonius of Perga", "dates": "c. 240 - c. 190 BCE", "birth_year": -240, "era": "Antiquity", "repo": "apollonius"},
    {"id": "heron", "name": "Heron of Alexandria", "dates": "c. 10 - c. 70 CE", "birth_year": 10, "era": "Antiquity", "repo": "heron"},
    {"id": "nicomachus", "name": "Nicomachus of Gerasa", "dates": "c. 60 - c. 120 CE", "birth_year": 60, "era": "Antiquity", "repo": "nicomachus"},
    {"id": "menelaus", "name": "Menelaus of Alexandria", "dates": "c. 70 - c. 140 CE", "birth_year": 70, "era": "Antiquity", "repo": "menelaus"},
    {"id": "ptolemy", "name": "Claudius Ptolemy", "dates": "c. 100 - c. 170 CE", "birth_year": 100, "era": "Antiquity", "repo": "ptolemy"},
    {"id": "pappus", "name": "Pappus of Alexandria", "dates": "c. 290 - c. 350 CE", "birth_year": 290, "era": "Antiquity", "repo": "pappus"},
    {"id": "proclus", "name": "Proclus Lycius", "dates": "412 - 485 CE", "birth_year": 412, "era": "Antiquity", "repo": "proclus"},
    {"id": "fibonacci", "name": "Leonardo Pisano (Fibonacci)", "dates": "c. 1170 - c. 1250", "birth_year": 1170, "era": "Medieval", "repo": "fibonacci"},
    {"id": "cusa", "name": "Nicholas of Cusa", "dates": "1401 - 1464", "birth_year": 1401, "era": "Renaissance", "repo": "cusa"},
    {"id": "piero", "name": "Piero della Francesca", "dates": "c. 1415 - 1492", "birth_year": 1415, "era": "Renaissance", "repo": "piero"},
    {"id": "leonardo", "name": "Leonardo da Vinci", "dates": "1452 - 1519", "birth_year": 1452, "era": "Renaissance", "repo": "pacioli"},
    {"id": "ceva", "name": "Giovanni Ceva", "dates": "1647 - 1734", "birth_year": 1647, "era": "Early Modern", "repo": "ceva"},
    {"id": "mascheroni", "name": "Lorenzo Mascheroni", "dates": "1750 - 1800", "birth_year": 1750, "era": "Enlightenment", "repo": "mascheroni"},
    {"id": "staudt", "name": "Karl G. C. von Staudt", "dates": "1798 - 1867", "birth_year": 1798, "era": "19th Century", "repo": "staudt"},
    {"id": "feuerbach", "name": "Karl Wilhelm Feuerbach", "dates": "1800 - 1834", "birth_year": 1800, "era": "19th Century", "repo": "feuerbach"},
    {"id": "casey", "name": "John Casey", "dates": "1820 - 1891", "birth_year": 1820, "era": "19th Century", "repo": "casey"},
    {"id": "ernst-haeckel", "name": "Ernst Haeckel", "dates": "1834 - 1919", "birth_year": 1834, "era": "19th Century", "repo": "phyllotaxis"},
    {"id": "petersen", "name": "Julius Petersen", "dates": "1839 - 1910", "birth_year": 1839, "era": "19th Century", "repo": "petersen"},
    {"id": "lemoine", "name": "Émile Lemoine", "dates": "1840 - 1912", "birth_year": 1840, "era": "19th Century", "repo": "lemoine"},
    {"id": "pasch", "name": "Moritz Pasch", "dates": "1843 - 1930", "birth_year": 1843, "era": "19th Century", "repo": "pasch"},
    {"id": "klein", "name": "Felix Klein", "dates": "1849 - 1925", "birth_year": 1849, "era": "19th Century", "repo": "klein"},
    {"id": "poincare", "name": "Henri Poincaré", "dates": "1854 - 1912", "birth_year": 1854, "era": "19th Century", "repo": "poincare"},
    {"id": "thompson", "name": "D'Arcy Wentworth Thompson", "dates": "1860 - 1948", "birth_year": 1860, "era": "Modern", "repo": "thompson"},
    {"id": "hambidge", "name": "Jay Hambidge", "dates": "1867 - 1924", "birth_year": 1867, "era": "Modern", "repo": "hambidge"},
    {"id": "walter-russell", "name": "Walter Russell", "dates": "1871 - 1963", "birth_year": 1871, "era": "Modern", "repo": "walter-russell"},
    {"id": "hoenen", "name": "Petrus Hoenen, S.J.", "dates": "1880 - 1961", "birth_year": 1880, "era": "Modern", "repo": "hoenen"},
    {"id": "altshiller-court", "name": "Nathan Altshiller-Court", "dates": "1881 - 1968", "birth_year": 1881, "era": "Modern", "repo": "altshiller-court"},
    {"id": "hans-kayser", "name": "Hans Kayser", "dates": "1891 - 1964", "birth_year": 1891, "era": "Modern", "repo": "geometor.com"},
    {"id": "huntley", "name": "H. E. Huntley", "dates": "1892 - 1977", "birth_year": 1892, "era": "Modern", "repo": "huntley"},
    {"id": "odom", "name": "George Odom", "dates": "1941 - 2010", "birth_year": 1941, "era": "Contemporary", "repo": "divine"},
    {"id": "kimberling", "name": "Clark Kimberling", "dates": "b. 1942", "birth_year": 1942, "era": "Contemporary", "repo": "etc"},
    {"id": "livio", "name": "Mario Livio", "dates": "b. 1945", "birth_year": 1945, "era": "Contemporary", "repo": "livio"},
    {"id": "wildberger", "name": "Norman J. Wildberger", "dates": "b. 1957", "birth_year": 1957, "era": "Contemporary", "repo": "wildberger"},
]


def main() -> None:
    """Populate the full 48-slot Pantheon in resources/portraits.{json,yaml}."""
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    portraits: list[dict[str, Any]] = payload.get("portraits", [])
    by_id = {p["id"]: p for p in portraits}

    for pid, year in BIRTH_YEARS_EXISTING.items():
        if pid in by_id:
            by_id[pid]["birth_year"] = year

    next_order = len(portraits)
    for item in NEW_ENTRIES:
        pid = item["id"]
        if pid in by_id:
            by_id[pid].update(item)
            continue
        entry = {
            "id": pid,
            "name": item["name"],
            "dates": item["dates"],
            "birth_year": item["birth_year"],
            "era": item["era"],
            "repo": item["repo"],
            "status": item.get("status", "queued"),
            "queue_order": item.get("queue_order", next_order),
            "pose": item.get("pose", "TBD by archival researcher"),
            "reference": item.get("reference", {}),
            "signature_motif": item.get("signature_motif", ""),
            "outputs": item.get("outputs", {}),
            "notes": item.get("notes", ""),
        }
        portraits.append(entry)
        by_id[pid] = entry
        next_order += 1

    payload["portraits"] = portraits
    JSON_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    YAML_PATH.write_text("\n".join(_dump_yaml(payload)) + "\n", encoding="utf-8")
    print(f"Synced {len(portraits)} Pantheon portraits to portraits.json and portraits.yaml")


if __name__ == "__main__":
    main()
