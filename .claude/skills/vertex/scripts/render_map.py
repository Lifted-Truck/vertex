#!/usr/bin/env python3
"""render_map.py — deterministic visual renderer for a persisted Vertex map.

Reads a vertex/<domain>_<date>.md artifact and emits ONE self-contained HTML
chart on stdout. Design constraints (ROADMAP Q-006 — a critic checks these):

  1. Deterministic: output is a pure function of the input file. Same map in,
     byte-identical HTML out — renders are diffable across the corpus.
  2. Self-contained/offline: no network refs, no CDN, no JS. Inline CSS/SVG.
  3. Uncertainty is the most salient channel: low/medium confidence renders
     faded+dashed (Portolan's dashed-until-earned grammar); nodes Calibrate
     never banded render as explicitly "unassessed", NOT as confident;
     suspected unknown-unknowns render as literal fog at the chart edge, and
     an EMPTY suspected list renders a red-flag warning, never clean edges.
  4. No unmeasured channel: every visual weight traces to a schema field or a
     Calibrate output. Nothing is beautified.

PyYAML parses the Map block when available (present on this machine); without
it a regex fallback extracts what it can and the page carries a visible
"degraded parse" banner — degradation is shown, never hidden.

Usage: python3 scripts/render_map.py vertex/<map>.md > out.html
Exit:  0 = rendered; 2 = usage/parse failure (no partial HTML on stdout).
"""
from __future__ import annotations

import html
import re
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------- parsing

def find_yaml_block(text: str) -> str | None:
    m = re.search(r"```ya?ml\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else None


def load_map(block: str) -> tuple[dict, bool]:
    """Return (map_data, degraded). Degraded = regex fallback was used."""
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(block)
        if isinstance(data, dict):
            return data, False
    except ImportError:
        pass
    # Lossy fallback: scalars + the two list shapes the chart needs most.
    data: dict = {}
    for key in ("domain", "competency_target", "profile", "surveyed_at"):
        m = re.search(rf'^{key}\s*:\s*"?([^"\n]+)"?\s*$', block, re.MULTILINE)
        data[key] = m.group(1).strip() if m else "unknown"
    data["subdomains"] = [
        {"name": n, "one_line": "", "maturity": m2}
        for n, m2 in re.findall(
            r'-\s*name:\s*"?([^"\n]+?)"?\s*\n\s*one_line:.*?\n\s*maturity:\s*"?(\w+)', block)
    ]
    data["prerequisite_dag"] = [
        {"node": n, "depends_on": re.findall(r'"([^"]+)"', d)}
        for n, d in re.findall(
            r'-\s*node:\s*"?([^"\n]+?)"?\s*\n\s*depends_on:\s*\[(.*?)\]', block)
    ]
    data["key_concepts"] = [
        {"term": t, "gloss": "", "source": s}
        for t, s in re.findall(
            r'-\s*term:\s*"?([^"\n]+?)"?\s*\n\s*gloss:.*?\n\s*source:\s*"?([^"\n]+)', block)
    ]
    data["live_controversies"] = [
        {"question": q, "camps": [], "why_unsettled": ""}
        for q in re.findall(r'-\s*question:\s*"?([^"\n]+)', block)
    ]
    data["canonical_sources"] = []
    data["silos_and_bridges"] = []
    cov = re.search(r"^coverage\s*:(.*)\Z", block, re.MULTILINE | re.DOTALL)
    data["coverage"] = {"surveyed": re.findall(r'"([^"]+)"', cov.group(1)) if cov else [],
                        "deliberately_out_of_scope": []}
    return data, True


def section(text: str, heading: str) -> str:
    """Markdown under a heading matching `heading`, incl. deeper subsections."""
    m = re.search(rf"^(#{{1,6}})\s*(?:\d+\.\s*)?{heading}\b.*?$",
                  text, re.MULTILINE | re.IGNORECASE)
    if not m:
        return ""
    level = len(m.group(1))
    rest = text[m.end():]
    nxt = re.search(rf"^#{{1,{level}}}\s", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def parse_calibrate(text: str) -> dict:
    cal = section(text, "Calibrate")
    out: dict = {"bands": {}, "low_load_bearing": None, "falsifications": [],
                 "known_unknowns": [], "suspected": [], "least_entitled": ""}
    # Bands: markdown-table rows (| label | **band** |) and inline "label: band".
    for label, band in re.findall(
            r"^\|\s*([^|\n]+?)\s*\|\s*\**(high|medium|low)\b", cal,
            re.MULTILINE | re.IGNORECASE):
        for part in label.split(","):
            out["bands"][_norm(part)] = band.lower()
    for label, band in re.findall(
            r"^\s*([A-Za-z][^:|\n]{0,80}?)\s*:\s*\**(high|medium|low)\b", cal,
            re.MULTILINE):
        out["bands"][_norm(label)] = band.lower()
    m = re.search(r"[Ll]ow-confidence load-bearing[^0-9]*(\d+)", cal)
    out["low_load_bearing"] = int(m.group(1)) if m else None
    fals = section(cal, r"B\.\s*Falsification") or cal
    out["falsifications"] = [
        s.strip().rstrip(".") for s in
        re.findall(r"[Ww]rong if\**\s*([^.\n]+)", fals)]
    unk = section(cal, r"C\.\s*Known")
    if unk:
        split = re.split(r"\**[Ss]uspected unknown[- ]unknowns[^:\n]*:?\**", unk, maxsplit=1)
        out["known_unknowns"] = _items(re.sub(
            r"\**[Kk]nown[- ]unknowns[^:\n]*:?\**", "", split[0], count=1))
        out["suspected"] = _items(split[1]) if len(split) > 1 else []
    m = re.search(r"least entitled[^:]*:\**\s*(.+?)(?:\n\n|\Z)", cal, re.DOTALL)
    out["least_entitled"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    return out


def _norm(s: str) -> str:
    # Hyphens and slashes become spaces so "DFT-vs-CFT" tokenizes as dft vs cft.
    return re.sub(r"[^a-z0-9 ]+", "", re.sub(r"[-/]", " ", s.lower())).strip()


_STOP = {"the", "and", "for", "with", "from", "of", "in", "a", "an", "is", "are"}


def _tokens(s: str) -> set[str]:
    # Light stemming (trailing 's') so convention/conventions match.
    return {w.rstrip("s") for w in _norm(s).split()
            if len(w) >= 3 and w not in _STOP}


def _items(chunk: str) -> list[str]:
    """Bulleted items if present, else non-trivial sentences."""
    bullets = [re.sub(r"\s+", " ", b).strip(" .")
               for b in re.findall(r"^\s*[-*]\s+(.+)$", chunk, re.MULTILINE)]
    if bullets:
        return bullets
    sents = [s.strip() for s in re.split(r"(?<=[.;])\s+", chunk.strip()) if s.strip()]
    return [re.sub(r"\s+", " ", s).strip(" .") for s in sents
            if s and not re.match(r"^\**\(?[A-D]\)?[.:]", s)][:6] if sents else []


def band_for(name: str, bands: dict[str, str]) -> str:
    """Match a node/question to its Calibrate band, else 'unassessed'.

    Exact norm match, then containment, then best stemmed-token overlap
    (>=2 shared significant tokens). An unmatched name renders 'unassessed' —
    the error direction is deliberate: the chart may under-claim confidence,
    never over-claim it.
    """
    n = _norm(name)
    if n in bands:
        return bands[n]
    # Token overlap FIRST: containment is unreliable for long labels (the short
    # subdomain key "fft" would steal the FFT-stability controversy into its
    # band), while >=2 shared tokens is a strong signal for them.
    nt = _tokens(name)
    best_band, best_score = "", 1  # need >=2 to beat this
    for key, band in sorted(bands.items()):
        score = len(nt & _tokens(key))
        if score > best_score:
            best_band, best_score = band, score
    if best_band:
        return best_band
    for key, band in bands.items():
        if key and (key in n or n in key):
            return band
    return "unassessed"

# ---------------------------------------------------------------- layout
# Portolan's move (layout.py): deterministic layered DAG layout, longest-path
# layers + barycenter sweeps. Positions are a function of structure alone.

def layered_layout(dag: list[dict]) -> tuple[dict[str, tuple[int, int]], int, int]:
    nodes = [d["node"] for d in dag]
    deps = {d["node"]: [p for p in d.get("depends_on") or [] if p in nodes] for d in dag}
    succ: dict[str, list[str]] = {n: [] for n in nodes}
    for n, ps in deps.items():
        for p in ps:
            succ[p].append(n)
    indeg = {n: len(deps[n]) for n in nodes}
    ready = sorted(n for n, d in indeg.items() if d == 0)
    layer = dict.fromkeys(nodes, 0)
    while ready:
        n = ready.pop(0)
        for s in sorted(succ[n]):
            layer[s] = max(layer[s], layer[n] + 1)
            indeg[s] -= 1
            if indeg[s] == 0:
                ready.append(s)
                ready.sort()
    by_layer: dict[int, list[str]] = {}
    for n in nodes:
        by_layer.setdefault(layer[n], []).append(n)
    for lst in by_layer.values():
        lst.sort()
    for sweep in range(4):  # barycenter passes, deterministic
        down = sweep % 2 == 0
        seq = sorted(by_layer) if down else sorted(by_layer, reverse=True)
        for lyr in seq:
            ref_layer = by_layer.get(lyr - 1 if down else lyr + 1, [])
            ref = {n: i for i, n in enumerate(ref_layer)}
            neigh = deps if down else succ
            by_layer[lyr] = sorted(
                by_layer[lyr],
                key=lambda n: (sum(ref[x] for x in neigh[n] if x in ref)
                               / max(1, len([x for x in neigh[n] if x in ref])), n))
    pos = {}
    for lyr, lst in by_layer.items():
        for col, n in enumerate(lst):
            pos[n] = (lyr, col)
    n_layers = max(by_layer, default=0) + 1
    max_rows = max((len(v) for v in by_layer.values()), default=1)
    return pos, n_layers, max_rows

# ---------------------------------------------------------------- render

E = html.escape
STYLE = {  # confidence -> (stroke, fill, dash, opacity, label)
    "high":       ("#2c4a3b", "#eef3ec", "0",   "1.0", "high — multiply sourced"),
    "medium":     ("#8a6d1f", "#f7f2e0", "7 4", "0.85", "medium — thinly sourced"),
    "low":        ("#a04434", "#f8ece8", "3 4", "0.6",  "low — prior only, distrust"),
    "unassessed": ("#7a766c", "#f1efe8", "1 4", "0.5",  "unassessed by Calibrate"),
}
NODE_W, NODE_H, LAYER_GAP, ROW_GAP, MARGIN, FOG_W = 176, 52, 226, 78, 40, 250


def node_svg(name: str, x: int, y: int, band: str) -> str:
    stroke, fill, dash, op, _ = STYLE[band]
    lines = textwrap.wrap(name, 24)[:3]
    tspans = "".join(
        f'<tspan x="{x + NODE_W // 2}" dy="{"1.1em" if i else 0}">{E(ln)}</tspan>'
        for i, ln in enumerate(lines))
    ty = y + NODE_H // 2 - (len(lines) - 1) * 7 + 4
    return (
        f'<g opacity="{op}"><rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" '
        f'rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6" '
        f'stroke-dasharray="{dash}"/>'
        f'<text x="{x + NODE_W // 2}" y="{ty}" text-anchor="middle" '
        f'font-size="11.5" fill="#2b2b26">{tspans}</text></g>')


def render(map_data: dict, cal: dict, degraded: bool, src_name: str) -> str:
    dag = map_data.get("prerequisite_dag") or []
    pos, n_layers, max_rows = layered_layout(dag)
    width = MARGIN * 2 + max(1, n_layers - 1) * LAYER_GAP + NODE_W + FOG_W
    height = MARGIN * 2 + max(max_rows, 1) * ROW_GAP + 30

    px = {n: (MARGIN + l * LAYER_GAP, MARGIN + c * ROW_GAP) for n, (l, c) in pos.items()}
    edges, nodes_s = [], []
    deps_ok = {d["node"] for d in dag}
    for d in dag:
        for p in d.get("depends_on") or []:
            if p in deps_ok and d["node"] in px:
                (x1, y1), (x2, y2) = px[p], px[d["node"]]
                ax, ay = x1 + NODE_W, y1 + NODE_H // 2
                bx, by = x2, y2 + NODE_H // 2
                mx = (ax + bx) / 2
                edges.append(f'<path d="M{ax},{ay} C{mx},{ay} {mx},{by} {bx},{by}" '
                             f'fill="none" stroke="#a89f8d" stroke-width="1.1"/>')
    for n, (x, y) in px.items():
        nodes_s.append(node_svg(n, x, y, band_for(n, cal["bands"])))

    fog_x = width - FOG_W - 10
    suspected = cal["suspected"]
    fog_labels = ""
    for i, s in enumerate(suspected[:5]):
        wrapped = textwrap.wrap(s, 30)[:3]
        ts = "".join(f'<tspan x="{fog_x + 34}" dy="{"1.25em" if j else 0}">{E(w)}</tspan>'
                     for j, w in enumerate(wrapped))
        fog_labels += (f'<text x="{fog_x + 34}" y="{50 + i * (height - 90) // max(1, min(len(suspected), 5))}" '
                       f'font-size="11" font-style="italic" fill="#5c564a">{ts}</text>')
    fog = (f'<rect x="{fog_x}" y="0" width="{FOG_W + 10}" height="{height}" fill="url(#fog)"/>'
           f'<text x="{fog_x + 34}" y="26" font-size="12" letter-spacing="3" '
           f'fill="#6b6557">TERRA INCOGNITA</text>{fog_labels}') if suspected else ""

    legend = "".join(
        f'<div class="lg"><svg width="34" height="12"><line x1="1" y1="6" x2="33" y2="6" '
        f'stroke="{s}" stroke-width="2.4" stroke-dasharray="{d}" opacity="{o}"/></svg>{E(lbl)}</div>'
        for s, _, d, o, lbl in (STYLE[b] for b in ("high", "medium", "low", "unassessed")))

    def panel_list(items: list[str]) -> str:
        return "".join(f"<li>{E(i)}</li>" for i in items) or "<li class='mut'>none recorded</li>"

    controversies = "".join(
        f'<div class="contested"><b>{E(c.get("question", ""))}</b>'
        f'<span class="band b-{band_for(c.get("question", ""), cal["bands"])}">'
        f'{band_for(c.get("question", ""), cal["bands"])}</span>'
        + (f'<div class="mut">camps: {E(" · ".join(map(str, c.get("camps") or [])))}</div>'
           if c.get("camps") else "")
        + f'</div>'
        for c in map_data.get("live_controversies") or [])

    concepts = "".join(
        f'<li><b>{E(str(k.get("term", "")))}</b> — {E(str(k.get("gloss", "")))}'
        f'<div class="src">source: {E(str(k.get("source", "")))}</div></li>'
        for k in map_data.get("key_concepts") or [])

    cov = map_data.get("coverage") or {}
    llb = cal["low_load_bearing"]
    banners = ""
    if degraded:
        banners += ('<div class="warnbox">DEGRADED PARSE — PyYAML unavailable; '
                    'regex fallback used. Fields may be missing. The gaps are in '
                    'the parse, not the terrain.</div>')
    if not suspected:
        banners += ('<div class="warnbox">⚠ EMPTY SUSPECTED-UNKNOWN-UNKNOWNS LIST '
                    '— a genuinely unfamiliar domain almost never has an empty list '
                    '(calibration.md §C). Treat the clean edges of this chart as a '
                    'defect of the survey, not a property of the terrain.</div>')
    if cal["least_entitled"]:
        banners += (f'<div class="pin">📌 <b>Claim least entitled to:</b> '
                    f'{E(cal["least_entitled"])}</div>')
    return f"""<!-- rendered by scripts/render_map.py — deterministic; do not hand-edit -->
<meta charset="utf-8">
<title>Vertex chart — {E(str(map_data.get("domain", "?")))}</title>
<style>
 body{{margin:0;background:#efe9da;color:#2b2b26;font:14px/1.5 Georgia,serif}}
 main{{max-width:1200px;margin:0 auto;padding:28px 20px 60px}}
 h1{{font-size:26px;letter-spacing:1px;margin:0}}
 h2{{font-size:15px;letter-spacing:2px;text-transform:uppercase;color:#6b6557;
    border-bottom:1px solid #c9c0ac;padding-bottom:4px;margin-top:34px}}
 .meta{{color:#6b6557;margin:6px 0 0}}
 .cartouche{{border:2px solid #6b6557;padding:14px 18px;background:#f5efe0;
    box-shadow:3px 3px 0 #d8d0bc;margin-bottom:18px}}
 .stat{{display:inline-block;border:1px solid #c9c0ac;background:#f5efe0;
    padding:4px 12px;margin:10px 8px 0 0;font-size:13px}}
 .stat b{{font-size:16px}}
 .warnbox{{border:2px solid #a04434;background:#f8ece8;color:#7c3122;
    padding:12px 16px;margin:14px 0;font-weight:bold}}
 .pin{{border-left:4px solid #a04434;background:#f8ece8;padding:10px 14px;margin:14px 0}}
 .chartwrap{{overflow-x:auto;border:1px solid #c9c0ac;background:#f5efe0;margin-top:12px}}
 .legend{{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;color:#4a463d;
    padding:10px 6px 2px}}
 .lg{{display:flex;align-items:center;gap:7px}}
 .contested{{border:1.5px dashed #8a6d1f;background:#f7f2e0;padding:10px 14px;margin:10px 0}}
 .band{{font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-left:10px;
    padding:1px 8px;border:1px solid}}
 .b-high{{color:#2c4a3b;border-color:#2c4a3b}} .b-medium{{color:#8a6d1f;border-color:#8a6d1f}}
 .b-low{{color:#a04434;border-color:#a04434}} .b-unassessed{{color:#7a766c;border-color:#7a766c}}
 .mut{{color:#6b6557;font-size:12.5px}}
 .src{{color:#6b6557;font-size:11.5px}}
 ul{{padding-left:22px}} li{{margin:4px 0}}
 .cols{{display:grid;grid-template-columns:1fr 1fr;gap:0 34px}}
 @media(max-width:800px){{.cols{{grid-template-columns:1fr}}}}
 details summary{{cursor:pointer;color:#4a463d}}
</style>
<main>
<div class="cartouche">
 <h1>VERTEX CHART · {E(str(map_data.get("domain", "?")))}</h1>
 <div class="meta">profile <b>{E(str(map_data.get("profile", "?")))}</b> ·
  surveyed {E(str(map_data.get("surveyed_at", "?")))} ·
  source <code>{E(src_name)}</code></div>
 <div class="meta">target: {E(str(map_data.get("competency_target", "?")))}</div>
 <span class="stat">low-confidence load-bearing nodes:
   <b>{llb if llb is not None else "not reported"}</b></span>
 <span class="stat">falsification conditions: <b>{len(cal["falsifications"])}</b></span>
 <span class="stat">suspected unknown-unknowns: <b>{len(suspected)}</b></span>
</div>
{banners}
<h2>Prerequisite chart <span style="text-transform:none;letter-spacing:0">— foundations left, targets right; the fog is measured, not decorative</span></h2>
<div class="legend">{legend}</div>
<div class="chartwrap"><svg viewBox="0 0 {width} {height}" width="{width}" height="{height}"
  xmlns="http://www.w3.org/2000/svg">
 <defs><linearGradient id="fog" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#d8d0bc" stop-opacity="0"/>
  <stop offset="0.45" stop-color="#d8d0bc" stop-opacity="0.85"/>
  <stop offset="1" stop-color="#cfc6ae" stop-opacity="1"/></linearGradient></defs>
 {''.join(edges)}
 {''.join(nodes_s)}
 {fog}
</svg></div>
<div class="cols">
<div>
<h2>Contested waters</h2>
{controversies or "<p class='mut'>none recorded</p>"}
<h2>This map is wrong if…</h2>
<ul>{panel_list(cal["falsifications"])}</ul>
</div>
<div>
<h2>Known-unknowns (named gaps)</h2>
<ul>{panel_list(cal["known_unknowns"])}</ul>
<h2>Beyond the chart edge (deliberately out of scope)</h2>
<ul>{panel_list([str(x) for x in cov.get("deliberately_out_of_scope") or []])}</ul>
</div>
</div>
<h2>Grounding</h2>
<details><summary>{len(map_data.get("key_concepts") or [])} key concepts, each with its source</summary>
<ul>{concepts}</ul></details>
<p class="mut" style="margin-top:30px">Chart drawn deterministically from the map artifact.
Coherence is not evidence of accuracy — the dashes and the fog are the honest parts.</p>
</main>
"""


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 render_map.py vertex/<map>.md > out.html", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"error: not a file: {path}", file=sys.stderr)
        return 2
    text = path.read_text()
    block = find_yaml_block(text)
    if block is None:
        print("error: no fenced yaml Map block found", file=sys.stderr)
        return 2
    map_data, degraded = load_map(block)
    cal = parse_calibrate(text)
    sys.stdout.write(render(map_data, cal, degraded, path.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
