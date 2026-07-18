# traces/

Append-only decision log — one file per merged change set, named
`YYYY-MM-DD-<slug>.md`. Format is defined by the provenance skill
(`.claude/skills/provenance/SKILL.md`): what changed, why, evidence consulted,
alternatives rejected, verify result + git hash, open questions.

Never edit or delete a prior trace. Correct the record with a new entry that
cites the old one.
