# Trace — Q-006 renderer prototype (2026-07-21)

**What changed.** New `.claude/skills/vertex/scripts/render_map.py`: the
deterministic visual renderer (ROADMAP Q-006), prototype scope — current binary
schema, no schema changes, not yet wired into `./verify` (human gate pending).
Plus the ROADMAP edits opening Q-006/Q-007 and the 2026-07-20 decision-log
entry (ratified in conversation 2026-07-20: identity = both personal + demo;
visuals-first sequencing; uncertainty-first rendering).

**Why.** Visual-first review beats need the map evaluable at a glance; the
consultancy identity needs the demo artifact. Design constraints and their
provenance (Portolan lessons) are recorded in ROADMAP Q-006 — chiefly:
deterministic render (AI/deterministic boundary), no unmeasured visual channel,
uncertainty as the most salient channel.

**Evidence consulted.** `vertex/fourier-transform_2026-06-26.md` +
`tests/fixtures/good_map.md` (input shapes); Portolan `layout.py` (layered
layout approach, reimplemented not copied), `graph.js` (provenance line-style
grammar), README founding caution.

**Acceptance status (Q-006 criteria, prototype pass):**
1. Self-contained offline HTML, zero external refs — checked (grep). ✓
2. Renders clean on the good fixture — ✓. Layer-0 wiring NOT done (editing
   `./verify` is a human gate — pending ask).
3. Low-confidence visually distinct (dash/opacity grammar + legend); band
   matcher tested against 9 expected assignments incl. the load-bearing case
   (FFT-stability controversy → low). ✓
4. Empty suspected-unknowns renders the red-flag banner (tested on a stripped
   fixture). ✓
5. Deterministic — byte-identical across runs (cmp). ✓

**Known prototype limitations (honest list).**
- Fuzzy band matching can under-claim: a label sharing <2 significant tokens
  with its Calibrate band renders "unassessed" (e.g. the Fourier convergence
  controversy, banded high, may show unassessed). Error direction is deliberate
  (never over-claim) but re-run maps should prefer exact labels.
- Route trail not yet drawn (constraint 5) — the DAG is charted; the marked
  trail from current standing to target is not. Next iteration.
- Visual inspection was structural (geometry audit: no overlaps/out-of-bounds/
  fog collisions) — browser screenshot unavailable in-session; human review of
  the rendered charts IS the review beat.

**Verify:** `./verify fast` green (renderer not yet a gate). Git hash: see
commit carrying this trace.
