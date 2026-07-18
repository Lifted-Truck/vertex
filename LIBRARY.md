# LIBRARY — Vertex durable lessons

Long-term memory. Each entry is evidence-backed and carries a falsifier. New
lessons enter as `tier: candidate`; promote to `canonical` on a second
independent occurrence or human review. Prefer not writing over writing
unverified. See CLAUDE.md → Self-Improving Knowledge Loop for the write gate.

---

[L0001] Layer-0 stage-body parser must span subsections
| tier: candidate
| added: 2026-06-26
| tags: skill-authoring, calibration
| lesson: When `layer0_check.py` extracts a stage section (e.g. Calibrate) to
  check its contents, it must read from the stage heading until the next
  heading of EQUAL-OR-HIGHER level, not until the next heading of any level.
  The Calibrate stage has `###` subsections (A/B/C/D); a naive "until next
  heading" regex stops at the first `###` and reports the stage empty, which
  false-fails an otherwise valid map.
| evidence: First build of the gate did exactly this — the good fixture failed
  with "Calibrate section is empty" until `stage_body()` was changed to compute
  the heading level and scan for `^#{1,level}\s`. See
  `.claude/skills/vertex/scripts/layer0_check.py` `stage_body()`.
| falsifier: A Layer-0 run where a valid, fully-populated Calibrate section
  (with `###` subsections) is accepted by a parser that stops at the first
  deeper heading — would mean the level-aware scan is not actually needed.
| supersedes: none
