---
name: vertex
description: >-
  Maps the topology of the user's ignorance in an unfamiliar domain and routes
  toward competency. This skill should be used when the user is entering a field
  they don't yet understand, asks "what don't I know about X", wants to scope or
  reconnoiter unfamiliar terrain before diving in, or invokes /vertex. It
  produces a structured, calibrated terrain map — it does NOT answer the domain
  question itself.
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, WebSearch, Write, Bash, Task
---

# Vertex — Domain Reconnaissance

Invoked as `/vertex <domain> [concept|system]`.

- `$1` = the **domain** to map (required).
- `$2` = the **profile**: `concept` | `system`. Default to `concept` if absent —
  going wide into unfamiliar intellectual terrain is the dominant use.

**Cardinal rule:** chart what is there; never confabulate terrain that isn't.
You are mapping the user's ignorance, not displaying your own fluency. Every
asserted feature of the terrain must trace to a source (`concept`) or a pulled
artifact (`system`). **Unsupported terrain is flagged, not stated** — at Survey
you refuse to assert unsourced structure, and at Calibrate you stress-test what
survived.

This skill is reconnaissance, not the campaign. If the user asks you to *explain*
the domain ("explain transformer attention"), that is not a Vertex invocation.
"What's the shape of what I don't know about mechanistic interpretability" is.

Run the five stages in order. Name each output so later stages can reference it.
Get today's date for `surveyed_at` and the persisted filename with `!`date +%F``.

---

## 1. Frame
Fix the boundary before surveying. Produce:
- **Domain edges** — what is in / adjacent / out of scope.
- **Competency target** — what "competent enough" means *for the user's stated
  purpose* (read the literature? ship a thing? hold a conversation at a dinner?).
- **Declared current standing** — where the user says they are now.

This is the **only** stage that may ask the user **one** clarifying question, and
only if the competency target is genuinely ambiguous. Otherwise proceed on a
best-guess target and state the assumption explicitly.

## 2. Survey — delegate to a subagent
Reconnoiter the whole terrain at low resolution, leaning on cross-silo
pattern-piercing. This sweep is high-volume and low-signal-per-token, so **run it
in a forked subagent** (use the `Task` tool) and bring back only its
*conclusions* — not its raw foraging — to keep the main context clean.

**Grounding is mandatory. No terrain asserted without a source or a pulled
artifact.**

- `concept`: have the subagent `WebSearch` across the field's subareas, schools,
  key figures, canonical texts, and open disputes. Triangulate — seek
  disconfirming sources, not just corroborating ones.
- `system`: pull ground truth before asserting structure —
  - `!`bash .claude/skills/vertex/scripts/survey_repo.sh``
  - `!`python3 .claude/skills/vertex/scripts/survey_deps.py``
  Map against the artifact, not against your prior.

Each surveyed concept must carry the source/artifact it traces to, ready for the
schema's required `source` field.

## 3. Map
Read `references/terrain-schema.md` now and emit the terrain map as a single
fenced `yaml` block matching it exactly. Populate **every** required field.
Where a field is empty because the terrain is genuinely unknown, say so
explicitly (`"none found"` / `"unknown"` / `[]`) — **an empty field is data**,
and silent omission is a Layer-0 failure.

## 4. Route
From the map, produce an **ordered** competency path to the Frame target:
prerequisites first, then **leverage points** (the few concepts that unlock the
most), then the **minimal spanning set**. Each step cites the Map node it covers,
so Route is checkable against Map.

## 5. Calibrate — HARD GATE, never skip, never abbreviate
Read `references/calibration.md` and execute it **in full**. Do not summarize it
away. The output must contain, as labeled subsections:
- **A. Confidence bands** per subdomain and controversy, with the low-confidence
  load-bearing count.
- **B. Falsification** — at least three concrete "this map is wrong if ___"
  conditions.
- **C. Known-unknowns vs suspected unknown-unknowns** — two separate lists,
  never merged.
- **D. Comfort-convergence check** — the four adversarial one-liners.

---

## Persist
Write the **full** result — all five stage sections, including the `yaml` Map
block and the complete Calibrate output — to:

```
vertex/<domain>_<YYYY-MM-DD>.md
```

in the **working project** (not the skill directory), using the date from
`!`date +%F`` and a filesystem-safe slug of `$1` for `<domain>`. Timestamped
filenames accrete a diffable corpus: re-running `/vertex <domain>` months later
produces a side-by-side record of competency growing and the terrain turning out
to be shaped differently than first mapped.

After writing, optionally validate the artifact:
`!`python3 .claude/skills/vertex/scripts/layer0_check.py vertex/<file>.md``

---

> **Mechanism note:** `$1`/`$2`/`$ARGUMENTS` substitution, `!`command``
> injection, `allowed-tools`, and `disable-model-invocation` are honored by the
> Claude Code CLI (and `allowed-tools` is ignored by the SDK — there, gate tools
> at the query level). The Survey subagent is launched with the `Task` tool; if
> your runtime lacks it, run Survey inline but still report only conclusions.
