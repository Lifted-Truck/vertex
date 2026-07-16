# VERTEX — Skill Scaffolding Document

*Turning the Vertex Protocol from an invoked lens into a robust, repeatable Claude Code Skill.*

---

## 0. Purpose & Contract

Vertex formalizes the one residue of the protocol stack you still reach for: **mapping the topology of your own ignorance in an unfamiliar domain and charting a route to competency.** You vault onto Mount Stupid deliberately, survey the valley of what you don't yet understand, and leave with a structured, calibrated terrain map.

The skill has exactly one job and one hard boundary:

- **Does:** locate the subdomains, prerequisites, live controversies, canonical sources, cross-silo bridges, and known/unknown gaps of a domain you're entering — and orders them into a competency route.
- **Does not:** answer the domain question itself. Vertex is reconnaissance, not the campaign. If the user asks "explain transformer attention," that is not a Vertex invocation; "what's the shape of what I don't know about mechanistic interpretability" is.

The cardinal rule — the epistemic-honesty boundary that makes this analogous to your other tools (ATTEST's *locate and evidence, never adjudicate*; Tonality's *reduce, never invent*):

> **Chart what is there. Never confabulate terrain that isn't.**

The native failure mode (§10) is a fluent, confident map that masks what the model actually doesn't know. Every design decision below is in service of defeating that.

---

## 1. What "more robust" actually buys

The old Vertex was a prompt-lens: load the framing, run it by hand, get prose back. "Robust" means six concrete mechanisms that convert a vibe into a pipeline:

1. **Schema-enforced output** — the Map stage emits a typed terrain map against a fixed schema, so output is validatable and diffable rather than free prose.
2. **Hard-gated Calibrate** — the calibration stage is non-skippable and lives in its own bundled reference file so it can't be smoothed away by fluency.
3. **Grounded Survey** — Survey must cite. Conceptual domains ground via web search; technical domains pull real artifacts (file trees, dep graphs, grep) via dynamic injection.
4. **Persistence** — each run writes `vertex/<domain>.md`, accreting a diffable corpus you can re-run as competency grows (the terrain map updated against the territory).
5. **Deterministic Layer-0 eval** — a structural gate that mechanically checks every output has all five stages, validates against schema, and contains non-empty calibration fields. CI-blockable.
6. **Forked Survey** — the wide, low-signal sweep runs in a subagent so it doesn't pollute the main context.

---

## 2. The decision you have to record first

Everything downstream of the scripting layer forks on one question, the one we left open last time:

**Is Vertex aimed at technical/system domains, conceptual/intellectual domains, or both?**

| | Technical / system | Conceptual / intellectual |
|---|---|---|
| Survey grounding | `!`command`` injection of real artifacts (file trees, dependency graphs, grep, API surfaces) | web search + source triangulation |
| Scripts | earn their place (`scripts/survey_repo.sh`, etc.) | mostly absent; schema enforcement does the work |
| Map content | mechanical coverage of the real surface + gaps | concept graph, prerequisite DAG, live debates, canonical sources |
| Calibrate target | coverage gaps in a *known* artifact (what's unmapped) | confabulated consensus, the El Dorado feeling, false synthesis |

**Recommendation (yours to ratify):** build a single `/vertex` entry point with a **domain-type flag** (`$1` = `concept` \| `system`, defaulting to `concept`, since going wide into unfamiliar intellectual terrain is your dominant use). One command, one diffable corpus, two activation profiles — the scripted technical path only fires when `system` is selected. This avoids splitting into two skills that drift apart (a single-source-of-truth concern you'll recognize).

Per your own maxim — *decisions not recorded are not decided* — §13 has this as a checkbox. Nothing below is load-bearing until you pick.

---

## 3. The pipeline: five stages

Each stage is a labeled section in the SKILL.md body. Stages are sequential and the output of each is named so later stages can reference it.

### Frame
Establish the boundary before surveying. Outputs: the domain's edges (what's in / adjacent / out), the user's **competency target** (what "competent enough" means *for this purpose* — read the literature? ship a thing? hold a conversation?), and the user's declared current standing. Frame is short and is the only stage that may ask the user a clarifying question.

### Survey
Go wide. Reconnoiter the whole terrain at low resolution, leaning on the cross-silo pattern-piercing that Vertex exists to exploit. **Grounding is mandatory** — no terrain asserted without a source or a pulled artifact. This stage is the one to **delegate to a subagent / forked context**, because the wide sweep is high-volume and low-signal-per-token; you want its *conclusions* in the main thread, not its raw foraging.

- `concept`: web search across the field's subareas, schools, key figures, canonical texts, and open disputes.
- `system`: inject ground truth — `!`find/tree``, dependency manifests, `!`grep`` for the real API surface — so the map is built against the artifact, not against the model's prior.

### Map
Structure the surveyed terrain into the **typed terrain-map schema** (§6). This is the stage that converts reconnaissance into a diffable artifact: subdomains, the prerequisite DAG, concepts with one-line definitions, live controversies, canonical sources, the silos and the bridges between them.

### Route
From the map, produce an **ordered competency path** to the Frame-stage target: prerequisites first, then leverage points (the few concepts that unlock the most), then the minimal spanning set. Each step cites the map node it covers, so Route is checkable against Map.

### Calibrate — *the protected stage*
The hard gate. Cannot be skipped, cannot be abbreviated. Lives in `references/calibration.md` so it's detailed and non-negotiable without bloating the body. Produces:

- **Confidence bands** per major map claim (and the map is downgraded where the only support was the model's prior, not a source).
- **Falsification conditions** — explicit "what would make this map wrong."
- **Known-unknowns vs *suspected* unknown-unknowns** — separated, never merged.
- **The comfort-convergence check** — an explicit pass that asks whether the map *feels* clean and authoritative, and treats that feeling as a warning rather than a confirmation. This is the residue you flagged as getting *harder* to maintain as models improve, because fluency makes the El Dorado feeling arrive faster and better-dressed. It is hard-coded here precisely because nothing in the environment will keep practicing it for you.

---

## 4. Directory structure

```
.claude/skills/vertex/
├── SKILL.md                  # frontmatter + the five-stage body
├── references/
│   ├── terrain-schema.md     # the typed Map output contract
│   └── calibration.md        # the protected Calibrate procedure + failure-mode doctrine
└── scripts/                  # system-profile only; omit if concept-only
    ├── survey_repo.sh        # file tree + LoC + entry points
    └── survey_deps.py        # dependency graph extraction

# Output (written into the working project, NOT the skill dir):
vertex/<domain>.md            # the persisted, diffable terrain map
```

Three-level progressive disclosure: metadata (always loaded) → SKILL.md body (loaded on trigger) → `references/` and `scripts/` (read only when the relevant stage needs them). Keep the body well under 500 lines; push depth into `references/`.

---

## 5. `SKILL.md` skeleton

```markdown
---
name: vertex
description: >-
  Maps the topology of the user's ignorance in an unfamiliar domain and
  routes toward competency. This skill should be used when the user is
  entering a field they don't yet understand, asks "what don't I know
  about X", wants to scope unfamiliar terrain, or invokes /vertex. It
  produces a structured, calibrated terrain map — it does NOT answer the
  domain question itself.
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, WebSearch, Write, Bash
---

# Vertex — Domain Reconnaissance

Invoked as `/vertex <domain> [concept|system]`. Argument `$1` selects the
profile; default to `concept` if absent.

**Cardinal rule:** chart what is there; never confabulate terrain that isn't.
You are mapping the user's ignorance, not displaying your own fluency. Every
asserted feature of the terrain must trace to a source (concept) or a pulled
artifact (system). Unsupported terrain is flagged, not stated.

Run the five stages in order. Name each output so later stages reference it.

## 1. Frame
Fix the boundary before surveying. Produce: domain edges (in / adjacent /
out); the user's competency TARGET (what "competent enough" means for their
stated purpose); their declared current standing. This is the only stage that
may ask one clarifying question.

## 2. Survey  (delegate to a subagent — see note below)
Reconnoiter the whole terrain at low resolution. Grounding is mandatory.
- concept: WebSearch across subareas, schools, key figures, canonical texts,
  and open disputes.
- system: pull ground truth before asserting structure —
  !`bash scripts/survey_repo.sh`
  and read scripts/survey_deps.py output. Map against the artifact.
Return conclusions, not raw foraging.

## 3. Map
Emit the terrain map against references/terrain-schema.md. Read that file now.
Populate every required field. Where a field is empty because the terrain is
genuinely unknown, say so explicitly — an empty field is data.

## 4. Route
From the map, produce an ordered competency path to the Frame target:
prerequisites first, then leverage points, then the minimal spanning set.
Each step cites the map node it covers.

## 5. Calibrate  (HARD GATE — never skip, never abbreviate)
Read references/calibration.md and execute it in full. Do not summarize it
away. Output must contain: confidence bands, falsification conditions,
known-unknowns separated from suspected unknown-unknowns, and the
comfort-convergence check.

## Persist
Write the full result to vertex/$1.md in the working project, against the
schema, so the corpus is diffable across re-runs.
```

> **Verify before relying on it:** the exact mechanism for forcing the Survey stage into a subagent (vs. inline) is the one frontmatter detail I'd confirm against the current Claude Code skills docs, since the subagent/`fork` surface has been moving. The `!`command`` dynamic injection, `$1`/`$ARGUMENTS` substitution, `allowed-tools`, and `disable-model-invocation` fields are current. (`allowed-tools` is honored by the Claude Code CLI but ignored by the SDK — there you gate tools at the query level.)

---

## 6. `references/terrain-schema.md` skeleton

The contract that makes Map output diffable and Layer-0-checkable. Keep it strict.

```markdown
# Terrain Map Schema

Every Vertex map emits these fields. Empty is allowed but must be explicit
("none found" / "unknown"), never silently omitted.

- domain:            <string>
- competency_target: <string, from Frame>
- profile:           concept | system
- surveyed_at:       <ISO date>
- subdomains:        [ {name, one_line, maturity: established|active|contested} ]
- prerequisite_dag:  [ {node, depends_on: [..]} ]
- key_concepts:      [ {term, gloss (<=1 line), source} ]
- live_controversies:[ {question, camps: [..], why_unsettled} ]
- canonical_sources: [ {title, author, why_it_matters} ]
- silos_and_bridges: [ {silo_a, silo_b, the_bridge} ]
- coverage:          {surveyed: [..], deliberately_out_of_scope: [..]}
```

`source` on every concept and a non-empty `coverage` block are what let the
Layer-0 oracle mechanically reject a confabulated map.

---

## 7. `references/calibration.md` skeleton — the part you protect

```markdown
# Calibrate — mandatory final stage

You have just produced a map that probably FEELS complete. That feeling is the
signal this stage exists to distrust. A fluent model produces a more seductive
map, so the sense of having mapped the terrain arrives faster and better-dressed
than the actual mapping warrants. Run all four checks. Do not abbreviate.

## A. Confidence bands
For each subdomain and each live_controversy, tag: high / medium / low.
Downgrade any claim whose only support was your prior rather than a Survey
source or pulled artifact. Report the count of low-confidence load-bearing nodes.

## B. Falsification
State plainly: "This map is wrong if ___." At least three concrete conditions —
a thing that, if true, would mean the terrain is shaped differently than mapped.

## C. Known vs suspected unknown-unknowns
Two separate lists. Known-unknowns: gaps you can name. Suspected
unknown-unknowns: regions where the field is probably larger than what Survey
reached (e.g., a subarea every source gestured at but none explained). Never
merge these — the merge is where false confidence hides.

## D. Comfort-convergence check
Answer in one line each:
- Does this map feel clean and authoritative? If yes, where might that polish be
  covering a gap?
- Did Survey actually reach disconfirming sources, or only corroborating ones?
- Name the single map claim you are least entitled to. Is it flagged above?
```

---

## 8. Persistence & the diffable corpus

Writing `vertex/<domain>.md` per run is the move that makes this a pipeline and not a one-off. Because Map emits against a fixed schema, two runs of `/vertex <domain>` separated by months produce diffable artifacts: you see exactly where your competency grew, where the terrain turned out to be shaped differently than first mapped, and which suspected unknown-unknowns resolved into known structure. The corpus *is* the longitudinal record of you climbing down the back of Mount Stupid.

---

## 9. Eval / audition — oracle-gated, in your usual two-layer shape

This maps cleanly onto the architecture you already run in ATTEST and wtfoundry.

**Layer-0 — deterministic, CI-blocking.** A script that parses `vertex/<domain>.md` and fails the build unless:
- all five stage sections are present;
- the Map block validates against `terrain-schema.md`;
- every `key_concept` has a non-empty `source`;
- the Calibrate block contains non-empty confidence bands, ≥3 falsification conditions, and *both* unknown lists.

This gate is mechanical and cannot be charmed. It catches the structural ways a run degrades.

**Layer-E — periodic, qualitative, the confabulation audit.** Run `/vertex` on **a domain you already know cold** (DSP, set-class theory, your own consultancy methodology) and check the map against ground truth you hold personally. Does it surface the *real* controversies? Does Calibrate honestly flag the places it's thin? A map of a known domain that comes back clean and confident *with nothing in its unknown-unknowns list* is the tool failing exactly as predicted in §10 — that's the audition checkpoint that matters most.

---

## 10. Native failure mode: confabulated terrain

The one risk worth naming loudly. Vertex's whole value proposition — a fluent model rapidly scaffolding unfamiliar terrain — is also its hazard: the same fluency that lets it pierce silos lets it *invent* a plausible, well-organized map of a field, complete with confident-sounding controversies and canonical sources that may be subtly wrong or hallucinated. The map's coherence is not evidence of its accuracy.

Each design choice above is a specific defense:

- **Grounded Survey + `source` on every concept** → terrain must trace to something external.
- **Schema with explicit-empty fields** → the model can't paper over a gap by omission; "unknown" is a required, visible value.
- **Calibrate as a protected, bundled, non-skippable stage** → the comfort-convergence check is structurally forced rather than left to discretion, because discretion is exactly what fluency erodes.
- **Layer-E known-domain audit** → you periodically catch confabulation against ground truth you personally hold.

You flagged this asymmetry yourself: decomposition and dialectic now have an external trainer in the model, but the suspicion does not. Vertex-as-skill is, in part, an attempt to give the suspicion a mechanical trainer it otherwise lacks.

---

## 11. Build sequence (audition-rig-first)

In your usual order — prove the contract on something real before scaling the machinery:

1. **Ratify §2.** Pick `concept` / `system` / both-via-flag. Record it. (Nothing else is decided until this is.)
2. **Write `terrain-schema.md` and `calibration.md` first.** These are the contract and the protected core; the body is comparatively cheap. This is the equivalent of writing the oracle before the generator.
3. **Hand-run the pipeline once, no skill** — `/vertex`-shaped prompt against a domain you know cold (Layer-E by hand). Confirm the schema is expressive enough and Calibrate actually bites.
4. **Wrap it as `SKILL.md`.** Confirm `/vertex` fires and the stage sections come through.
5. **Add the Layer-0 script.** Make a malformed map fail the gate.
6. **Only then** add `scripts/` for the `system` profile, if §2 selected it.
7. **Persist + diff.** Run twice on a moving domain; confirm the corpus diffs meaningfully.

---

## 12. Open decisions to record

- [ ] **Profile fork (§2):** `concept` only / `system` only / single command with `$1` flag (recommended).
- [ ] **Survey isolation:** subagent/forked vs inline — and confirm the current frontmatter mechanism for it.
- [ ] **Frame interactivity:** may Frame ask a clarifying question, or must it proceed on best-guess and flag assumptions? (Trade-off: friction vs. mis-scoped surveys.)
- [ ] **Persistence location & overwrite policy:** `vertex/<domain>.md` overwrite-in-place vs. timestamped versions (mirrors your `.als` `STAGE_YYYYMMDD` convention — versioned would give you the longitudinal diff for free).
- [ ] **Layer-0 strictness:** which schema fields are *hard* required vs. warn-only.
- [ ] **Scope of the cardinal rule:** is "never confabulate terrain" enforced purely by Calibrate, or also by a Survey-stage refusal to assert unsourced structure?

---

*Companion artifact intent: this document is formatted to drop into your decisions corpus the way `terrane-tonality-relay.md` was — the §12 checklist is the part that becomes "decided" once you fill it in.*
