# ROADMAP — Vertex

Single source of truth. Only the lead session (or the human) edits this file.
State lives here; conversations are ephemeral.

## Status

- **Phase:** v1 shipped (concept/system binary) → hardening + a pending major
  revision (the field/artifact/system trinary, not yet implemented) + a new
  visual-output track (Q-006, prototype in progress).
- **Oracle:** `./verify fast` covers scaffolding + manifest JSON + SKILL.md
  frontmatter + script syntax + the Layer-0 self-test (good fixture passes /
  bad fixture fails). `full` = fast today. **Gap:** Layer-E (the known-domain
  confabulation audit, scaffolding-doc §9) is human-run and NOT scripted — it
  is Q-004 below, not a silent pass.
- **Last human ratification:** 2026-07-21 (Q-006 prototype accepted after
  visual review; Layer-0 renderer gate wired into `./verify` — an oracle edit,
  human-gated, ratified in conversation). Prior: 2026-07-20 (Q-006/Q-007
  roadmap + prototype), 2026-06-26 (retrofit plan + manifest).

## Invariants under active protection

See CLAUDE.md §Domain. The two most at risk from the queue below:
- The **Calibrate hard gate** and the **universal comfort-convergence check**
  must survive the trinary revision (Q-001) unweakened — Trinary brief §2.5/§3.
- The **visual renderer (Q-006) must not become a confabulation surface.** A
  rendered map launders conjecture into apparent fact; the renderer therefore
  adds **no visual channel for anything Calibrate did not already measure**, and
  uncertainty must be its most salient channel, not a footnote (Portolan's
  founding caution; "expressiveness paired with measurability").

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

### Q-006 — Deterministic visual renderer for terrain maps
- **Status:** prototype shipped + ratified (2026-07-21); Layer-0 gate wired
  (`./verify` check 6: fixture renders, non-empty, deterministic, no external
  refs — negative-tested). **Remaining before close:** Route trail on the chart
  (design constraint 5); band-matcher under-claiming on low-token-overlap
  labels (e.g. the Fourier convergence controversy renders unassessed though
  banded high — safe direction, still a gap); trinary tracking on Q-001 land.
  Trace: traces/2026-07-21-q006-renderer-prototype.md
- **Scope:** new `scripts/render_map.py` (Python 3; PyYAML if present, regex
  fallback — the project convention in CLAUDE.md §Domain / `layer0_check.py`);
  a Layer-0 branch that runs it on `tests/fixtures/good_map.md`; **no schema
  changes**
  (hard constraint). Prototype target: the **current binary schema** and the
  existing Fourier map (per the "visuals-first" call).
- **Why:** a terrain map is currently YAML + prose. A visual makes it evaluable
  at a glance for the human AND is the consultancy "Latent Space Navigation"
  demo artifact — identity is **deliberately both** (human ratification
  2026-07-20). But a rendered graph is dangerously persuasive (Portolan's
  founding caution: it launders conjecture into apparent fact), so the renderer
  must lead with uncertainty by construction.
- **Design constraints (load-bearing — a critic checks against these):**
  1. **Deterministic code renders; the model never hand-authors the page**
     (AI/deterministic boundary). Same map in → byte-identical render out, so
     renders are diffable across the timestamped corpus (watch the fog recede).
  2. **Self-contained, stdlib-only, offline.** One HTML file, no CDN / network /
     external refs — mirrors Portolan's pure-render client + server-side
     deterministic layout (`layout.py`).
  3. **Uncertainty is the most salient channel.** Confidence bands → visual
     weight (high = solid; low = faded/dashed, Portolan's dashed-until-earned
     grammar); suspected unknown-unknowns → literal edge-fog sized to the
     Calibrate list; the "single claim least entitled to" is pinned on the map.
  4. **No unmeasured channel.** The renderer reads only what Calibrate already
     produced; nothing gets a glow/weight it did not earn (invariant above).
  5. **Route as a marked trail** from "you are here" (Frame current standing) to
     the competency target.
- **Acceptance criteria:**
  1. `python3 scripts/render_map.py <map>.md > out.html` yields a self-contained
     file that opens offline with **zero** network requests (no external
     `src=`/`href`/`http`).
  2. Runs clean on `tests/fixtures/good_map.md`; a Layer-0 branch asserts exit 0
     + non-empty HTML + no external references.
  3. Every low-confidence node/edge from Calibrate is visually distinct from
     high-confidence; the mapping is legible without reading the source.
  4. A non-empty suspected-unknown-unknowns list renders as visible fog/blank at
     the edge; an **empty** list renders the red-flag warning, not clean edges.
  5. Deterministic: two runs on the same input are byte-identical.
- **Out of scope:** bridge-mode rendering (Q-007); any interactive/served GUI
  (this is a static file, not a web app); consuming the trinary schema.
- **Dependency / cross-ref:** prototype targets the **current binary** schema;
  when **Q-001** lands, the renderer must track the field/artifact/system schema
  (type-specific fog semantics). Flagged so it is not silently stale.
- **Open questions (surface, do not decide unilaterally):** whether to commit
  one example rendered HTML as a tracked reference artifact (vs. keeping renders
  gitignored like the maps); exact fog encoding (opacity gradient vs. hatching).

### Q-007 — (Design only) `/vertex bridge <A> <B>` — cross-silo analogical mapping
- **Status:** design only (recorded 2026-07-20; not scheduled)
- **Why:** the most differentiated Vertex mode — pierce a silo and chart the
  analogical structure between two domains; the deepest attractor-basin escape
  and the strongest demo artifact. Also the **highest-confabulation-risk mode**
  conceivable (a felt "resonance" *is* the El Dorado feeling), so it is recorded
  with its defenses attached, not as an open invitation.
- **Design constraints (must hold before it is scheduled):**
  - **Typed bridges**, mirroring Portolan provenance: `attested` (cross-domain
    literature exists — cite it, solid), `measured` (N blind judges endorse the
    isomorphism — tally rendered, splits escalate), `conjectured` (model
    assertion alone — dashed, and stays dashed).
  - **Every asserted bridge must emit a falsifiable transfer prediction**
    ("technique X from A should work on problem Y in B") or it is inadmissible —
    the ATTEST move applied to bridges (cf. Portolan's rule that an unnamed
    misleads-claim is inadmissible).
  - Multi-agent consensus (blind judges, tally, escalate on split) is the
    `measured` tier — mechanism validated by Portolan's edge-model-v2 swarm
    experiments; consensus is filed **below** evidenced (measured ≠ guaranteed).
- **Acceptance criteria:** TBD (design stage).
- **Dependency:** after Q-006 (shares the renderer) and ideally after Q-001.

## Decision log

<!-- One line per ratified decision, newest first, linking to traces/. -->
- 2026-07-21 — Q-006 prototype ratified after visual review; renderer gate
  added to `./verify` (oracle edit, human-approved; negative-tested red/green).
  (trace: traces/2026-07-21-q006-renderer-prototype.md)
- 2026-07-20 — Open the visual-output track: Q-006 deterministic renderer
  (uncertainty-first, no unmeasured channels, prototype vs. current binary
  schema) + Q-007 bridge-mode design; identity ratified as **both** personal
  instrument and consultancy demo. Lessons drawn from the Portolan sibling
  project (provenance-as-line-style, deterministic server-side layout, swarm
  consensus with split-escalation). (trace: pending prototype close)
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
