# ROADMAP — Vertex

Single source of truth. Only the lead session (or the human) edits this file.
State lives here; conversations are ephemeral.

## Status

- **Phase:** v1 shipped (concept/system binary) → hardening + a pending major
  revision (the field/artifact/system trinary, not yet implemented).
- **Oracle:** `./verify fast` covers scaffolding + manifest JSON + SKILL.md
  frontmatter + script syntax + the Layer-0 self-test (good fixture passes /
  bad fixture fails). `full` = fast today. **Gap:** Layer-E (the known-domain
  confabulation audit, scaffolding-doc §9) is human-run and NOT scripted — it
  is Q-004 below, not a silent pass.
- **Last human ratification:** 2026-06-26 (retrofit plan + manifest approved).

## Invariants under active protection

See CLAUDE.md §Domain. The one most at risk from the queue below: the
**Calibrate hard gate** and the **universal comfort-convergence check** must
survive the trinary revision (Q-001) unweakened — the Trinary brief §2.5/§3
explicitly require this.

## Queue

### Q-001 — Implement the field/artifact/system trinary revision
- **Status:** open (design ratified in the brief; implementation not started)
- **Scope:** `.claude/skills/vertex/SKILL.md`, `references/terrain-schema.md`,
  `references/calibration.md`, `scripts/layer0_check.py`, `scripts/` retagging;
  source brief: [VERTEX_Skill_Trinary_Update.md](VERTEX_Skill_Trinary_Update.md).
- **Why:** the v1 `concept|system` binary is cut on the wrong axis (grounding
  instrument, not terrain ontology). Re-cut by "what would settle a dispute —
  the literature, the object itself, or watching it run?" yields three types.
- **Acceptance criteria** (verbatim from the brief's §4 self-verify checklist;
  each should become a Layer-0 branch or a fixture):
  1. Flag accepts `field|artifact|system`, defaults to `field`; old
     `concept`/`system` handled per §2.1 migration (no silent `system`→`system`).
  2. Frame routes via the diagnostic and detects composite delves.
  3. Survey forks three ways; the `system` path instruments behavior and never
     asserts structure from a static surface alone.
  4. Schema carries `terrain_type` + exactly one populated type block per
     (sub-)map; empties explicit.
  5. Calibrate forks per type AND retains the universal comfort-convergence pass.
  6. Layer-0 branches on `terrain_type` and validates composite sub-maps.
  7. Cardinal-rule sharpenings present in artifact/system stage prompts.
  8. A known-domain Layer-E run on each type produces a non-empty
     type-appropriate unknowns field.
- **Out of scope:** building real `system`-instrumentation tooling (log/trace
  parsers) — brief §2.8 says leave a stub. That is Q-005.
- **Open questions (surface to human — brief §5, do not decide unilaterally):**
  - The two existing persisted maps' migration (`concept`→`field`) — see Q-002.
  - Composite delves: persist one merged file (assumed) vs. one per constituent.
  - Overwrite-in-place vs. timestamped versioning (also scaffolding §12; this
    retrofit's map runs use **timestamped** — Decision D-004).

### Q-002 — Migrate the two existing persisted maps to the trinary
- **Status:** blocked (on Q-001)
- **Scope:** `vertex/fourier-transform_2026-06-26.md`,
  `vertex/logical-verification-nl-claims_2026-07-16.md` (both gitignored run
  artifacts).
- **Acceptance criteria:** both re-tagged `concept`→`field`; each confirmed
  `field` (not `artifact`/`system`) via the diagnostic, or flagged to the human
  if ambiguous.
- **Out of scope:** re-running the surveys; this is a re-tag, not a re-delve.

### Q-003 — Fix multi-word `$ARGUMENTS` parsing in the skill invocation
- **Status:** open
- **Scope:** `.claude/skills/vertex/SKILL.md` (argument-parsing note only).
- **Why:** on the first real run, `/vertex fourier transform` mis-split the
  domain (header showed `transform`, empty profile). Evidence:
  traces/2026-06-26-retrofit.md and the fourier map's own closing note.
- **Acceptance criteria:** SKILL.md instructs treating **all of `$ARGUMENTS`
  as the domain unless the last token is exactly the profile keyword**
  (`concept`/`system`, or `field`/`artifact`/`system` after Q-001).

### Q-004 — Wire the Layer-E confabulation audit as a checkable gate
- **Status:** open
- **Scope:** ROADMAP + a `tests/layer-e/` protocol doc; NOT `./verify` auto-pass.
- **Why:** scaffolding-doc §9/§10 — the highest-value check (run `/vertex` on a
  domain the human knows cold, check the map against ground truth they hold) is
  exactly the one fluency erodes. It cannot be scripted honestly.
- **Acceptance criteria:** a written, repeatable human-run protocol (which
  known domains, what "clean map with empty unknown-unknowns = failure" means),
  and a place to record each run's verdict. `./verify full` names it, never
  fakes it.

### Q-005 — (Deferred) Real `system`-profile instrumentation tooling
- **Status:** deferred (stub only, per brief §2.8)
- **Scope:** future `scripts/` for log/trace parsing.
- **Acceptance criteria:** TBD after Q-001 lands and a real `system` delve is
  attempted.

## Decision log

<!-- One line per ratified decision, newest first, linking to traces/. -->
- 2026-06-26 — Retrofit ecosystem scaffolding onto the repo; rung 1, Layer-0
  now + Layer-E as a gate, knowledge loop installed, Trinary absorbed as Q-001.
  (trace: traces/2026-06-26-retrofit.md)

## Graduation criteria

Vertex graduates from interactive prototyping to autonomous queue work when the
remaining open questions are infrastructure (parsing, schema branching, fixture
coverage) rather than **judgment** ones. Still in the judgment column: whether a
given entry is `field`/`artifact`/`system` (Q-001 diagnostic), and every
Layer-E accuracy call (Q-004) — those stay human-ratified. Q-003 and the Q-001
mechanical criteria are infrastructure and are queue-ready now.
