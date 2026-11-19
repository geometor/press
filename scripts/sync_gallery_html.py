"""Generate demos/portraits_gallery.html and docsrc/_static/studios/portraits_gallery.html from portraits.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = REPO_ROOT / "resources" / "portraits.json"
TARGETS = [
    REPO_ROOT / "demos" / "portraits_gallery.html",
    REPO_ROOT / "docsrc" / "_static" / "studios" / "portraits_gallery.html",
]


def build_gallery_html(portraits: list[dict[str, Any]]) -> str:
    """Build the self-contained interactive HTML gallery for all completed portrait studies."""
    completed = [p for p in portraits if p.get("status") == "complete"]
    completed.sort(key=lambda p: int(p.get("queue_order", 999)))

    js_items = []
    for idx, p in enumerate(completed, start=1):
        ref = p.get("reference") or {}
        ref_parts = [ref.get("artist"), ref.get("title"), ref.get("holding")]
        ref_str = ", ".join(str(x) for x in ref_parts if x) or "Verified Public Domain"
        js_items.append(
            {
                "id": str(p["id"]).replace("-", "_"),
                "slug": str(p["id"]),
                "study": f"Study {idx:02d}",
                "name": str(p["name"]),
                "dates": str(p.get("dates", "")),
                "era": str(p.get("era", "")),
                "motif": str(p.get("signature_motif", "")),
                "ref": ref_str,
            }
        )

    eras = []
    for item in js_items:
        if item["era"] and item["era"] not in eras:
            eras.append(item["era"])

    n_done = len(js_items)
    n_total = len(portraits)
    js_data = json.dumps(js_items, indent=2, ensure_ascii=False)
    era_buttons = "\n          ".join(
        f'<button type="button" data-set-era="{era}">{era}</button>' for era in eras
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark" data-scale="gallery" data-mode="single">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>GEOMETOR Press — Compass-and-Straightedge Portrait Gallery</title>
  <style>
    :root {{
      --bg: #080c12;
      --surface: #0f1621;
      --surface-2: #151f2e;
      --border: rgba(212, 175, 55, 0.24);
      --border-subtle: rgba(142, 157, 178, 0.18);
      --text: #eef2f7;
      --muted: #8e9db2;
      --gold: #d4af37;
      --chip-bg: rgba(212, 175, 55, 0.12);
    }}

    html[data-theme="light"] {{
      --bg: #fbf8f1;
      --surface: #f4efe3;
      --surface-2: #ebe4d4;
      --border: rgba(176, 127, 16, 0.30);
      --border-subtle: rgba(85, 97, 115, 0.18);
      --text: #181c24;
      --muted: #556173;
      --gold: #b07f10;
      --chip-bg: rgba(176, 127, 16, 0.12);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
      line-height: 1.45;
      transition: background 0.2s ease, color 0.2s ease;
    }}

    .shell {{
      max-width: 1420px;
      margin: 0 auto;
      padding: 1.5rem 1.5rem 2.5rem;
    }}

    header.topbar {{
      display: flex;
      flex-wrap: wrap;
      align-items: flex-end;
      justify-content: space-between;
      gap: 1rem 1.5rem;
      padding-bottom: 1.15rem;
      margin-bottom: 1rem;
      border-bottom: 1px solid var(--border);
    }}

    .title-block h1 {{
      margin: 0;
      font-size: 1.35rem;
      font-weight: 600;
      letter-spacing: 0.02em;
    }}

    .title-block p {{
      margin: 0.25rem 0 0;
      font-size: 0.88rem;
      color: var(--muted);
    }}

    .controls, .era-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      align-items: center;
    }}

    .era-bar {{
      margin-bottom: 1.25rem;
    }}

    .segmented {{
      display: inline-flex;
      flex-wrap: wrap;
      background: var(--surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 2px;
      gap: 2px;
    }}

    .segmented button,
    .toggle-btn {{
      appearance: none;
      border: 0;
      background: transparent;
      color: var(--muted);
      font-size: 0.8rem;
      font-weight: 500;
      padding: 0.38rem 0.7rem;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.15s ease, color 0.15s ease;
    }}

    .segmented button.active,
    .toggle-btn.active {{
      background: var(--chip-bg);
      color: var(--gold);
    }}

    .toggle-btn {{
      background: var(--surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.42rem 0.75rem;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 1.15rem;
    }}

    html[data-scale="card"] .grid {{
      grid-template-columns: repeat(auto-fill, minmax(175px, 1fr));
    }}

    html[data-scale="badge"] .grid {{
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    }}

    html[data-mode="both"] .grid {{
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    }}

    .card {{
      background: var(--surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      cursor: pointer;
      transition: transform 0.15s ease, border-color 0.15s ease;
    }}

    .card:hover {{
      transform: translateY(-2px);
      border-color: var(--gold);
    }}

    .card-head {{
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.74rem;
      color: var(--muted);
      margin-bottom: 0.65rem;
    }}

    .study-num {{
      color: var(--gold);
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}

    .medallion-pair {{
      display: flex;
      gap: 0.75rem;
      align-items: center;
      justify-content: center;
      width: 100%;
    }}

    .medallion-wrap {{
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 10px;
      overflow: hidden;
    }}

    .medallion-wrap img {{
      display: block;
      width: 210px;
      height: auto;
      transition: width 0.18s ease;
    }}

    html[data-mode="both"] .medallion-wrap img {{
      width: 150px;
    }}

    html[data-scale="card"] .medallion-wrap img {{
      width: 116px;
    }}

    html[data-scale="badge"] .medallion-wrap img {{
      width: 48px;
    }}

    .horizon-line {{
      display: none;
      position: absolute;
      left: 0;
      right: 0;
      top: 40.306%;
      height: 1px;
      border-top: 1px dashed var(--gold);
      opacity: 0.75;
      pointer-events: none;
    }}

    html[data-horizon="on"] .horizon-line {{
      display: block;
    }}

    .card-meta {{ margin-top: 0.8rem; }}
    .card-name {{ font-size: 1rem; font-weight: 600; margin: 0; }}
    .card-dates {{ font-size: 0.78rem; color: var(--muted); margin: 0.15rem 0 0.35rem; }}
    .card-motif {{ font-size: 0.76rem; color: var(--gold); margin: 0; }}
    html[data-scale="badge"] .card-motif {{ display: none; }}

    dialog#inspector {{
      background: var(--surface);
      color: var(--text);
      border: 1px solid var(--gold);
      border-radius: 14px;
      padding: 1.35rem;
      max-width: 740px;
      width: calc(100vw - 2rem);
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.55);
    }}

    dialog#inspector::backdrop {{
      background: rgba(4, 7, 12, 0.75);
      backdrop-filter: blur(4px);
    }}

    .modal-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1rem;
      margin-bottom: 1rem;
    }}

    .modal-top h2 {{ margin: 0; font-size: 1.25rem; }}
    .modal-top p {{ margin: 0.2rem 0 0; font-size: 0.85rem; color: var(--muted); }}

    .close-btn {{
      appearance: none;
      background: var(--surface-2);
      color: var(--text);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.35rem 0.65rem;
      cursor: pointer;
      font-size: 0.85rem;
    }}

    .modal-svgs {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1rem;
      margin: 1rem 0;
    }}

    .modal-pane {{
      border-radius: 10px;
      padding: 0.75rem;
      text-align: center;
      border: 1px solid var(--border-subtle);
    }}

    .modal-pane.dark-pane {{ background: #080c12; color: #eef2f7; }}
    .modal-pane.light-pane {{ background: #fbf8f1; color: #181c24; }}

    .modal-pane img {{
      width: 100%;
      max-width: 260px;
      height: auto;
      display: block;
      margin: 0 auto 0.5rem;
    }}

    .modal-pane a {{ color: var(--gold); font-size: 0.78rem; text-decoration: none; }}
    .modal-details {{ font-size: 0.85rem; color: var(--muted); border-top: 1px solid var(--border-subtle); padding-top: 0.85rem; }}
    .modal-details strong {{ color: var(--text); }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <div class="title-block">
        <h1>GEOMETOR Compass-and-Straightedge Portraits</h1>
        <p>Studies 01–{n_done:02d} ({n_done} of {n_total} Pantheon slots complete) · Strictly lines, circles, and circular arcs (0 Bézier curves) · Eye-line y = −27</p>
      </div>
      <div class="controls">
        <div class="segmented" role="group" aria-label="Theme">
          <button type="button" data-set-mode="dark" class="active">Obsidian Ink</button>
          <button type="button" data-set-mode="light">Warm Paper</button>
          <button type="button" data-set-mode="both">Side-by-Side</button>
        </div>
        <div class="segmented" role="group" aria-label="Scale">
          <button type="button" data-set-scale="gallery" class="active">Gallery</button>
          <button type="button" data-set-scale="card">Card (116px)</button>
          <button type="button" data-set-scale="badge">Badge (48px)</button>
        </div>
        <button type="button" class="toggle-btn" id="horizon-toggle">Eye-Line (y = −27)</button>
      </div>
    </header>

    <div class="era-bar">
      <div class="segmented" role="group" aria-label="Era Filter">
        <button type="button" data-set-era="All" class="active">All ({n_done})</button>
        {era_buttons}
      </div>
    </div>

    <main class="grid" id="gallery-grid"></main>
  </div>

  <dialog id="inspector">
    <div class="modal-top">
      <div>
        <h2 id="m-title"></h2>
        <p id="m-sub"></p>
      </div>
      <button type="button" class="close-btn" id="m-close">Close</button>
    </div>
    <div class="modal-svgs">
      <div class="modal-pane dark-pane">
        <img id="m-dark-img" alt="" />
        <a id="m-dark-link" target="_blank" rel="noopener">Open Dark SVG</a>
      </div>
      <div class="modal-pane light-pane">
        <img id="m-light-img" alt="" />
        <a id="m-light-link" target="_blank" rel="noopener">Open Light SVG</a>
      </div>
    </div>
    <div class="modal-details">
      <p><strong>Signature Motif:</strong> <span id="m-motif"></span></p>
      <p><strong>Reference Source:</strong> <span id="m-ref"></span></p>
    </div>
  </dialog>

  <script>
    const PORTRAITS = {js_data};
    let activeEra = "All";

    function svgUrl(id, theme) {{
      return `../portraits/${{id}}_${{theme}}.svg`;
    }}

    function attachFallback(img, id, theme) {{
      img.onerror = function () {{
        if (!this.dataset.triedFallback) {{
          this.dataset.triedFallback = "1";
          this.src = `../docsrc/_static/portraits/${{id}}_${{theme}}.svg`;
        }}
      }};
    }}

    const grid = document.getElementById("gallery-grid");

    function renderGrid() {{
      const mode = document.documentElement.dataset.mode;
      const theme = document.documentElement.dataset.theme;
      grid.innerHTML = "";

      const filtered = activeEra === "All"
        ? PORTRAITS
        : PORTRAITS.filter((p) => p.era === activeEra);

      for (const p of filtered) {{
        const card = document.createElement("article");
        card.className = "card";
        card.tabIndex = 0;
        card.setAttribute("role", "button");
        card.setAttribute("aria-label", `Inspect ${{p.name}}`);

        const head = document.createElement("div");
        head.className = "card-head";
        head.innerHTML = `<span class="study-num">${{p.study}}</span><span>${{p.era}}</span>`;
        card.appendChild(head);

        const pair = document.createElement("div");
        pair.className = "medallion-pair";

        const themesToShow = mode === "both" ? ["dark", "light"] : [theme];
        for (const t of themesToShow) {{
          const wrap = document.createElement("div");
          wrap.className = "medallion-wrap";
          const img = document.createElement("img");
          img.src = svgUrl(p.id, t);
          img.alt = `${{p.name}} (${{t}})`;
          attachFallback(img, p.id, t);
          const horizon = document.createElement("div");
          horizon.className = "horizon-line";
          wrap.appendChild(img);
          wrap.appendChild(horizon);
          pair.appendChild(wrap);
        }}
        card.appendChild(pair);

        const meta = document.createElement("div");
        meta.className = "card-meta";
        meta.innerHTML = `
          <h2 class="card-name">${{p.name}}</h2>
          <div class="card-dates">${{p.dates}}</div>
          <p class="card-motif">${{p.motif}}</p>
        `;
        card.appendChild(meta);

        card.addEventListener("click", () => openModal(p));
        card.addEventListener("keydown", (e) => {{
          if (e.key === "Enter" || e.key === " ") {{
            e.preventDefault();
            openModal(p);
          }}
        }});

        grid.appendChild(card);
      }}
    }}

    const modal = document.getElementById("inspector");
    function openModal(p) {{
      document.getElementById("m-title").textContent = `${{p.study}} — ${{p.name}}`;
      document.getElementById("m-sub").textContent = `${{p.dates}} · ${{p.era}}`;
      document.getElementById("m-motif").textContent = p.motif;
      document.getElementById("m-ref").textContent = p.ref;

      const dImg = document.getElementById("m-dark-img");
      const lImg = document.getElementById("m-light-img");
      delete dImg.dataset.triedFallback;
      delete lImg.dataset.triedFallback;
      dImg.src = svgUrl(p.id, "dark");
      lImg.src = svgUrl(p.id, "light");
      attachFallback(dImg, p.id, "dark");
      attachFallback(lImg, p.id, "light");

      document.getElementById("m-dark-link").href = svgUrl(p.id, "dark");
      document.getElementById("m-light-link").href = svgUrl(p.id, "light");
      modal.showModal();
    }}

    document.getElementById("m-close").addEventListener("click", () => modal.close());
    modal.addEventListener("click", (e) => {{
      if (e.target === modal) modal.close();
    }});

    document.querySelectorAll("[data-set-mode]").forEach((btn) => {{
      btn.addEventListener("click", () => {{
        document.querySelectorAll("[data-set-mode]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const val = btn.dataset.setMode;
        if (val === "both") {{
          document.documentElement.dataset.mode = "both";
        }} else {{
          document.documentElement.dataset.mode = "single";
          document.documentElement.dataset.theme = val;
        }}
        renderGrid();
      }});
    }});

    document.querySelectorAll("[data-set-scale]").forEach((btn) => {{
      btn.addEventListener("click", () => {{
        document.querySelectorAll("[data-set-scale]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        document.documentElement.dataset.scale = btn.dataset.setScale;
      }});
    }});

    document.querySelectorAll("[data-set-era]").forEach((btn) => {{
      btn.addEventListener("click", () => {{
        document.querySelectorAll("[data-set-era]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        activeEra = btn.dataset.setEra;
        renderGrid();
      }});
    }});

    const horizonBtn = document.getElementById("horizon-toggle");
    horizonBtn.addEventListener("click", () => {{
      const active = document.documentElement.dataset.horizon === "on";
      document.documentElement.dataset.horizon = active ? "off" : "on";
      horizonBtn.classList.toggle("active", !active);
    }});

    renderGrid();
  </script>
</body>
</html>
"""


def main() -> None:
    """Sync unified interactive gallery HTML from resources/portraits.json."""
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    html = build_gallery_html(payload.get("portraits", []))
    for target in TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
    print(f"Synced interactive gallery HTML to {len(TARGETS)} locations.")


if __name__ == "__main__":
    main()
