# Vertex

**A Claude Code skill for domain reconnaissance.** Vertex maps the *topology of
your ignorance* in an unfamiliar domain and charts a route to competency. You
vault onto Mount Stupid deliberately, survey the valley of what you don't yet
understand, and leave with a structured, calibrated terrain map.

It has one job and one hard boundary:

- **Does:** locate the subdomains, prerequisites, live controversies, canonical
  sources, cross-silo bridges, and known/unknown gaps of a domain you're
  entering — and order them into a competency route.
- **Does NOT:** answer the domain question itself. Vertex is reconnaissance,
  not the campaign. "Explain transformer attention" is not a Vertex call;
  "what's the shape of what I don't know about mechanistic interpretability" is.

> **Cardinal rule: chart what is there; never confabulate terrain that isn't.**

*Last verified current: 2026-07-20.*

## Why it's built this way

A fluent model is dangerously good at *inventing* a plausible, well-organized
map of a field — confident controversies, canonical-sounding sources, a clean
prerequisite tree — that is subtly or entirely wrong. The map's coherence is
not evidence of its accuracy, and the better the model gets, the more seductive
the confabulation becomes. That single failure mode is what every design choice
here fights:

- **Grounding is mandatory.** Every asserted concept traces to a source (in a
  `concept` run) or a pulled artifact (in a `system` run) — or it is flagged,
  not stated.
- **Empty fields are explicit.** `"unknown"` / `"none found"` is a required,
  visible value, so a genuine gap can never hide as a silent omission.
- **Calibrate is a protected, non-skippable gate.** It forces confidence bands,
  falsification conditions, separated known-vs-*suspected* unknowns, and a
  *comfort-convergence check* that treats "this map feels complete" as a warning
  to investigate rather than a signal to stop.

If you only remember one thing: a Vertex map is designed to show you the shape
and the *edges* of your ignorance — including the parts it is not sure it
charted correctly — not to hand you a confident answer.

## Use it

```
/vertex <domain> [concept|system]
```

`$1` is the domain (required). `$2` is the profile — `concept` (web-grounded,
the default) or `system` (pulls real artifacts: file trees, deps, grep). The
skill runs five stages and writes a persisted map.

## The pipeline (five stages)

| Stage | What it does |
|---|---|
| **Frame** | Fix the boundary and the competency target before surveying. |
| **Survey** | Go wide at low resolution, in a forked subagent. **Grounding is mandatory** — no terrain asserted without a source or a pulled artifact. |
| **Map** | Structure the terrain into the typed schema (`references/terrain-schema.md`): subdomains, prerequisite DAG, concepts (each sourced), controversies, canonical sources, silos & bridges. |
| **Route** | Order a competency path to the Frame target: prerequisites → leverage points → minimal spanning set. |
| **Calibrate** | **The protected hard gate** (`references/calibration.md`): confidence bands, falsification conditions, known vs. *suspected* unknown-unknowns, and the comfort-convergence check. Never skipped, never abbreviated. |

Output is persisted to `vertex/<domain>_<YYYY-MM-DD>.md` (gitignored run
artifacts) so re-runs produce a diffable, longitudinal record of competency
growing.

## What a run produces

One markdown file carrying all five stages: the four narrative stages plus a
schema-typed **Map** (a fenced `yaml` block the Layer-0 gate validates against
`terrain-schema.md`) and the full **Calibrate** output. The tool's character is
clearest in Calibrate — for example, the tail of a real `concept` run on the
Fourier transform:

> **Low-confidence load-bearing nodes: 1.** The FFT-stability research-edge
> claim is the only low-confidence node, and the Route does *not* depend on it.
> The Route's spine — orthogonality → series → CFT → convolution/Parseval →
> DFT/FFT — is entirely high-confidence.
>
> **Single claim least entitled to:** the "2025 permutation-free FFT variant" —
> already flagged low in the confidence bands and as falsification condition #3.

The map names its own weakest point and where it is thin *by construction*, not
as an afterthought. Two runs of the same domain months apart are directly
diffable — you see where the terrain turned out differently shaped and which
*suspected* unknowns resolved into known structure.

## Repository layout

```
.claude/skills/vertex/
├── SKILL.md                  # the five-stage body + frontmatter
├── references/
│   ├── terrain-schema.md     # the typed Map contract (Layer-0 validates against this)
│   └── calibration.md        # the protected, non-skippable Calibrate doctrine
└── scripts/
    ├── survey_repo.sh        # system profile: file tree + LoC + entry points
    ├── survey_deps.py        # system profile: dependency-graph extraction
    └── layer0_check.py       # the deterministic gate (good map passes / bad map fails)

CLAUDE.md · ROADMAP.md · DECISIONS.md   # the harness: charter, direction, record
verify                                   # oracle: ./verify fast | full | report
tests/fixtures/{good,bad}_map.md         # the oracle's own truth set
traces/                                  # append-only decision traces
INDEX.md · LIBRARY.md                    # the self-improving knowledge loop
```

## Status

- **v1 shipped** — the `concept`/`system` binary skill, with the Layer-0 gate.
- **Pending (ROADMAP Q-001):** a major revision replacing the binary with a
  **field / artifact / system** trinary, cut by terrain ontology rather than
  grounding instrument. Design ratified in
  [VERTEX_Skill_Trinary_Update.md](VERTEX_Skill_Trinary_Update.md); **not yet
  implemented** — the skill still ships the binary.
- **Known gap:** Layer-E (the known-domain confabulation audit) is human-run
  (ROADMAP Q-004), not scripted.

Direction lives in [ROADMAP.md](ROADMAP.md); settled calls in
[DECISIONS.md](DECISIONS.md). Run `./verify report` for the oracle's last state.

## Verify

```
./verify fast     # structure + manifest + SKILL frontmatter + script syntax + layer0 self-test
./verify full     # = fast today; Layer-E is a human-run gate (Q-004)
./verify report    # prints the last run's target/exit/git hash
```
