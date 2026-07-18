# DECISIONS — Vertex

Append-only record of ratified decisions. Newest at the bottom of each section
is fine; never rewrite a prior entry — correct it with a new one that cites it.
ROADMAP.md holds *direction*; this holds *what was settled and why*.

---

## D-001 — Retrofit ecosystem scaffolding onto the existing repo (2026-06-26)

**Decision.** Apply the canonical retrofit (ONBOARDING.md Part 2) non-
destructively: add CLAUDE.md, ./verify, ROADMAP, DECISIONS, README, manifest,
knowledge loop, traces, and the invariant `.claude/` harness layer. The product
files under `.claude/skills/vertex/` and the two source docs are left untouched.
**Why.** The repo had real content (a shipped v1 skill, a pending revision
brief, two generated maps) but zero harness — no charter, oracle, or roadmap.
**Trace.** traces/2026-06-26-retrofit.md.

## D-002 — Architecture rung 1 (single-threaded) (2026-06-26)

**Decision.** Rung 1. The `.claude/agents/` files are copied but inert by
default; a fresh-context `critic` may be used at review beats without
escalating the standing rung. **Why.** One skill = docs + a few scripts; no
parallelizable seams, no token budget that justifies a fleet. Escalation must
be earned (doctrine: burden of proof runs toward *not* escalating). Note: the
skill's Survey stage forks a subagent at *runtime* — that is the skill's
behavior, orthogonal to the project's development rung.

## D-003 — Oracle: Layer-0 now, Layer-E as a human-run gate (2026-06-26)

**Decision.** `./verify` enforces Layer-0 deterministically (structure, syntax,
and a good/bad-fixture self-test of `layer0_check.py`). Layer-E (the known-
domain confabulation audit) is tracked as ROADMAP Q-004 and run by the human;
`./verify full` names it but never auto-passes it. **Why.** Map *accuracy*
can't be checked without ground truth the human holds; scripting it would fake
the one check fluency most erodes (scaffolding-doc §10).

## D-004 — Persisted maps use timestamped filenames (this session)

**Decision.** `vertex/<domain>_<YYYY-MM-DD>.md`. **Why.** Gives the diffable
longitudinal corpus (scaffolding-doc §8) without relying on git for run
artifacts, and the `vertex/` dir is gitignored. **Status.** Still formally open
vs. overwrite-in-place for the *trinary* rework — carried as a Q-001 open
question and the Trinary brief §5; this decision governs current behavior.

## D-005 — Trinary revision is absorbed as a ROADMAP phase, not implemented now
(2026-06-26)

**Decision.** The field/artifact/system revision
([VERTEX_Skill_Trinary_Update.md](VERTEX_Skill_Trinary_Update.md)) becomes
ROADMAP Q-001 with the brief's §4 checklist as acceptance criteria; the
retrofit does not touch the skill's behavior. **Why.** Retrofit adds
scaffolding only — never feature work — and the brief carries unresolved §5
questions the human owns.

---

## Decisions inherited from before the harness (reconstructed, lower confidence)

These predate DECISIONS.md; recorded from session history and the source docs,
not from a contemporaneous log. Correct if memory differs.

- **DI-A — Single `/vertex` command with a profile flag**, defaulting to
  `concept`, rather than two skills. (Scaffolding-doc §2 recommendation,
  ratified when the skill was first built.) Superseded in *direction* by D-005
  / Q-001 (flag becomes `field|artifact|system`).
- **DI-B — Build the Layer-0 gate as part of v1** (scaffolding-doc §11 step 5),
  rather than deferring it. Realized as `scripts/layer0_check.py`.
