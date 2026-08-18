# Agent Charter — Vertex

Everything above §Domain is the invariant harness layer. Do not edit it
per-project. Project-specific facts live in §Domain and in ROADMAP.md.

## Truth contract

- **ROADMAP.md is the single source of truth.** Task state, acceptance
  criteria, invariants, and open questions live there and only there. If the
  conversation and ROADMAP.md disagree, ROADMAP.md wins; if ROADMAP.md is
  wrong, fixing it is the first task.
- **Passing ≠ done.** Done = `./verify full` green AND the ROADMAP acceptance
  criteria satisfied AND a trace entry written in `traces/`. Never collapse
  these into each other.
- **Grounded refusal is a success class.** "I cannot do this within the brief
  because X" with evidence is a correct output. Guessing to appear productive
  is a failure.
- **Reduce, never invent.** Prefer deleting code, tightening a contract, or
  reusing an existing mechanism over adding a new one. Every new abstraction
  must displace at least as much complexity as it introduces.
- **Review beats are visual-first.** When presenting completed work at a
  gate (phase close, ratification request, PR), lead with a visual — a
  self-contained HTML report, render set, or live demo — sufficient to
  evaluate the change WITHOUT reading the diff, plus evidence it works and
  open questions. Code diving is the fallback, never the ask.

## Provenance

- Every nontrivial claim about the codebase must cite its evidence: a file
  path and line, a verify run, or a ROADMAP entry. No provenance → phrase it
  as a hypothesis, not a fact.
- Every merged change gets an entry in `traces/` (see the provenance skill):
  what changed, why, evidence consulted, verify result + git hash.

## Delegation policy (lead session)

- The lead plans, delegates, integrates, and is the **only** writer of
  ROADMAP.md. Subagents never touch it.
- Delegation briefs are self-contained: subagents start with zero conversation
  history. Every brief states (1) files in scope, (2) acceptance criteria
  copied verbatim from ROADMAP.md, (3) the verify target, (4) what is
  explicitly out of scope.
- Use built-in Explore for codebase reconnaissance. Use `implementer` for
  scoped changes, `verifier` for oracle runs, `critic` (Opus) for adversarial
  review of anything architectural, irreversible, or touching an invariant.
- One queue item per implementer dispatch. Parallel dispatches only for items
  with disjoint file scopes.
- Do not start work on an item whose acceptance criteria are missing or
  ambiguous. Surface the gap to the human; that is the deliverable.

## Oracle discipline

- Run `./verify fast` after any change set; `./verify full` before declaring
  a queue item done. Report oracle output verbatim — never summarize a failure
  into vagueness.
- A red oracle halts forward work. Fix or revert; do not stack changes on red.
- Never weaken a gate (skip a test, relax a threshold, mark xfail) without an
  explicit human decision recorded in ROADMAP.md.

## Human gates

Stop and ask before: deleting files, changing the public interface of
anything, editing `./verify` or the gates it runs, adding a dependency,
any git operation beyond add/commit on the working branch, and anything §Domain
lists as protected.

---

## §Domain — Vertex

**What this is.** Vertex is a **Claude Code skill** (`/vertex <domain>
[concept|system]`) that maps the topology of the user's ignorance in an
unfamiliar domain and routes toward competency. It is reconnaissance, not the
campaign: it produces a structured, calibrated *terrain map* — it does NOT
answer the domain question itself. Form factor: SKILL.md + bundled
`references/` (the Map contract and the protected Calibrate doctrine) +
`scripts/` (grounding + the Layer-0 validator). Primary consumer: the user,
interactively.

**Stack & entrypoints.** Markdown (the skill body + references), Bash
(`scripts/survey_repo.sh`), Python 3 stdlib (`scripts/survey_deps.py`,
`scripts/layer0_check.py`; PyYAML used if present, regex fallback otherwise).
No build step. Skill entry: `.claude/skills/vertex/SKILL.md`. Oracle entry:
`./verify`. The skill runs a five-stage pipeline — Frame → Survey → Map →
Route → Calibrate → Persist.

**Domain invariants.** (The critic checks against these.)
- **Cardinal rule: chart what is there; never confabulate terrain that isn't.**
  Every asserted feature traces to a source (concept) or a pulled artifact
  (system); unsupported terrain is flagged, not stated.
- **Calibrate is a hard, non-skippable gate.** Its doctrine lives in
  `references/calibration.md` and must not be summarized away; the universal
  comfort-convergence check is never weakened.
- **Every `key_concept` carries a non-empty `source`.** Enforced by Layer-0.
- **Empty schema fields are explicit** (`"none found"` / `"unknown"` / `[]`),
  never silently omitted — an empty field is data.
- **The Layer-0 gate is mechanical and cannot be weakened to pass** — it must
  accept the good fixture and reject the bad one.

**Protected paths** (human gate before modifying):
- `.claude/skills/vertex/references/calibration.md` — the protected doctrine.
- `.claude/skills/vertex/references/terrain-schema.md` — the Map contract.
- `.claude/skills/vertex/scripts/layer0_check.py` — the deterministic gate.
- `tests/fixtures/{good,bad}_map.md` — the oracle's own truth set.

**Verify targets.** `./verify fast` (~seconds): scaffolding + manifest JSON +
SKILL.md frontmatter + script syntax (py `ast` + `bash -n`) + the Layer-0
self-test (good fixture passes / bad fixture fails). `full` = fast today;
**Layer-E** (the known-domain confabulation audit) is a human-run gate tracked
in ROADMAP (Q-004), never silently claimed as passing.

<!-- KNOWLEDGE-LOOP:START -->
## Self-Improving Knowledge Loop

Each session: read accumulated knowledge before acting, write distilled knowledge
after. This meta-layer sits on top of my primary role and never overrides it.

### Every session
1. **ORIENT** — Read INDEX.md in full (kept small on purpose). Pull ONLY the matching
   entries from LIBRARY.md into context. Never load all of LIBRARY by default.
2. **ACT** — Do the work, applying retrieved lessons. If a lesson proves wrong,
   correcting it outranks adding a new one.
3. **REFLECT** — Ask: "What did I learn that a future session needs and could not
   cheaply re-derive?" A lesson qualifies only if durable, evidenced (tied to a
   concrete trigger), and non-obvious. If nothing qualifies, write nothing.
4. **WRITE (atomic)** — Append the lesson to LIBRARY.md and a one-line pointer to
   INDEX.md in the same change. New lessons enter as `tier: candidate`; promote to
   `canonical` only on a second independent occurrence or human review.

### Write gate (anti-poisoning)
This loop feeds its own output back as input, so a wrong lesson, written once, is
retrieved and reinforced forever. Therefore: prefer not writing over writing
unverified; every lesson states what would falsify it; if a retrieved lesson
contradicts present evidence, trust the evidence and demote the lesson.

### Consolidation (periodic)
When LIBRARY exceeds ~30 entries, merge duplicates, delete superseded entries,
promote recurring candidates, tighten tags. Refactor it like code; don't grow it
like a log.

### LIBRARY entry template
`[Lxxxx] <title> | tier | added: YYYY-MM-DD | tags: … | lesson: … | evidence: … | falsifier: … | supersedes: …`
<!-- KNOWLEDGE-LOOP:END -->

<!-- KIT-MAILBOX:START (kit 2.1.0, applied 2026-08-18) -->
## Mailbox

Scope discipline for cross-repo exchanges (INTEGRATIONS §3). Three questions,
three answers:

- **Who owes me / what is addressed to us?** `integrations/` **in this repo**
  is the only place briefs to Vertex land. If it is not in our tree, it is not
  addressed to us.
- **Did anyone answer my brief?** Responses to briefs *we* filed live in the
  **provider's** tree (e.g. `autonomous/integrations/vertex/`), not ours. They
  must be **pulled and read** — nothing delivers them here.
- **Should I act on an exchange between two other repos?** No. Other repos'
  exchanges may be **read freely** — they are not secret, and reading them is
  often how you learn the ecosystem — but they are never **acted on**, and
  never **raised to the human as ours**. If one genuinely concerns Vertex, the
  correct move is to file our own brief, not to answer someone else's.

Why this is written down: on 2026-08-17 agents in several unrelated projects
each warned the human about the same single brief sitting in autonomous's
mailbox. Tooling caused it; the rule had never been stated either way.
<!-- KIT-MAILBOX:END -->
