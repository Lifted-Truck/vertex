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

## D-006 — Fix the Layer-0 regex fallback rather than pin PyYAML in CI (2026-08-18)

**Decision.** Patch the PyYAML-less fallback in `layer0_check.py` (a protected
path — human-gated and approved this session) on two counts: the `profile`
check was quote-blind and rejected every valid map, and the source check used
`\S+`, so `source: ""` counted as present — silently unenforcing the cardinal
"every `key_concept` carries a non-empty `source`" rule. CI then runs
**deliberately without PyYAML** so the fallback path is exercised on every push.
**Why.** Found while testing CI parity before writing the workflow: a bare
runner would have gone red on day one (bug A), and "fixing" only that would
have turned a loudly-broken gate into a quietly blind one (bug B) — the exact
green-and-blind failure kit 2.4.0 exists to end. Pinning PyYAML in CI would
have hidden both and left the fallback rotting unseen, since no developer runs
it locally. **Rejected alternative.** Pin PyYAML in CI (hides the defect);
defer as ROADMAP debt (leaves the cardinal rule unenforced for any PyYAML-less
environment). **Evidence.** Both fixtures now agree on both paths; a
valid-except-`source: ""` map fails the fallback with `1 terms but only 0
non-empty sources`. **Trace.** traces/2026-08-18-kit-2.4.1-retrofit.md.

## D-007 — Declare kit_version 2.4.1 (2026-08-18)

**Decision.** Record `"kit_version": "2.4.1"` in `project.manifest.json`, add
the kit CI workflow, and append the kit 2.1.0 `## Mailbox` scope section to
CLAUDE.md. **Why.** `currency.py` read `pre-2.0.0 / BEHIND by 5`; the only
mechanical gap was CI (2.2.0/2.3.0/2.4.0 were closed by the 2026-08-18 hand
migration to vendored gates). The declaration is written only because the
closing `currency.py` re-read of the tree says CURRENT — a repo never declares
a version it does not meet. **Trace.** traces/2026-08-18-kit-2.4.1-retrofit.md.

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
