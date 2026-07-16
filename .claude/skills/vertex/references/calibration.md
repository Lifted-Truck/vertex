# Calibrate — mandatory final stage

You have just produced a map that probably **feels** complete. That feeling is
the signal this stage exists to distrust. A more fluent model produces a more
seductive map, so the sense of having mapped the terrain arrives faster and
better-dressed than the actual mapping warrants. The map's coherence is not
evidence of its accuracy.

Run all four checks. Do not abbreviate, summarize, or skip. The output of this
stage is part of the persisted artifact and is checked by Layer-0.

---

## A. Confidence bands

For **each** `subdomain` and **each** `live_controversy`, tag confidence:
`high` / `medium` / `low`.

- `high` — multiple independent Survey sources, or a directly pulled artifact.
- `medium` — one source, or sources that corroborate but don't independently
  confirm.
- `low` — supported mainly by your prior rather than a Survey source or pulled
  artifact. **Downgrade aggressively here.** When unsure between two bands,
  pick the lower one.

Then report the **count of low-confidence load-bearing nodes** — nodes the
Route stage depends on that are only `low`. That number is the headline honesty
metric of the run.

## B. Falsification

State plainly, in the form **"This map is wrong if ___."** Give **at least
three** concrete, checkable conditions — each a thing that, if true, would mean
the terrain is shaped differently than mapped (e.g., "wrong if the field treats
X and Y as one subdomain rather than two," "wrong if source Z is retracted or
fringe"). Vague conditions ("wrong if I missed something") do not count.

## C. Known-unknowns vs *suspected* unknown-unknowns

Two **separate** lists. Never merge them — the merge is exactly where false
confidence hides.

- **Known-unknowns** — gaps you can name: a specific subarea you saw referenced
  but did not survey, a term you logged without a gloss, a controversy you know
  exists but couldn't resolve the camps of.
- **Suspected unknown-unknowns** — regions where the field is probably *larger*
  than what Survey reached: a subarea every source gestured at but none
  explained, a discipline the bridges hint at but Survey never entered, a sense
  that the established framing is hiding a contested foundation.

If the suspected-unknown-unknowns list is empty, that is itself a red flag —
say so and re-examine. A genuinely unfamiliar domain almost never has an empty
list here.

## D. Comfort-convergence check

Answer in one line each. Be adversarial with yourself.

1. Does this map feel clean and authoritative? If yes — **where** might that
   polish be covering a gap?
2. Did Survey actually reach **disconfirming** sources, or only corroborating
   ones? Name one disconfirming source it reached, or admit it reached none.
3. Name the single map claim you are **least entitled to**. Is it flagged in A,
   B, or C above? If not, flag it now.

---

> Cardinal rule, restated: chart what is there; never confabulate terrain that
> isn't. This stage is the structural enforcement of that rule. Nothing in the
> environment will keep practicing this suspicion for you — that is precisely
> why it is hard-coded here rather than left to discretion.
