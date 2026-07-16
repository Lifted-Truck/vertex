# Terrain Map Schema

The contract that makes the Map stage diffable and Layer-0-checkable. It is
strict on purpose. When you reach the Map stage, emit the map as a single
fenced **`yaml`** block matching the structure below, so the Layer-0 oracle
(`scripts/layer0_check.py`) can parse and validate it mechanically.

Every field is required. **Empty is allowed but must be explicit** — write
`"none found"`, `"unknown"`, or an empty list `[]` with a one-line note in the
adjacent prose. Silent omission is the failure this schema exists to prevent:
an absent field reads as "covered," when in reality it was never surveyed.

## Required fields

```yaml
domain:            "<string>"            # the field being mapped
competency_target: "<string>"            # verbatim from the Frame stage
profile:           "concept"             # concept | system
surveyed_at:       "<ISO date, YYYY-MM-DD>"

subdomains:
  - name:     "<string>"
    one_line: "<<=1 line>"
    maturity:  "established"             # established | active | contested

prerequisite_dag:
  - node:       "<subdomain or concept>"
    depends_on: ["<node>", "..."]        # [] if a root

key_concepts:
  - term:   "<string>"
    gloss:  "<<=1 line>"
    source: "<citation / URL / pulled artifact>"   # MUST be non-empty

live_controversies:
  - question:      "<the open question>"
    camps:         ["<position A>", "<position B>"]
    why_unsettled: "<<=1 line>"

canonical_sources:
  - title:         "<string>"
    author:        "<string>"
    why_it_matters: "<<=1 line>"

silos_and_bridges:
  - silo_a:     "<string>"
    silo_b:     "<string>"
    the_bridge: "<the concept/method that connects them>"

coverage:
  surveyed:                  ["<area>", "..."]   # what Survey actually reached
  deliberately_out_of_scope: ["<area>", "..."]   # excluded by the Frame boundary
```

## What the oracle enforces

- All ten top-level keys present.
- `profile` ∈ {`concept`, `system`}.
- `subdomains[].maturity` ∈ {`established`, `active`, `contested`}.
- **Every `key_concepts[]` entry has a non-empty `source`.** This is the
  load-bearing anti-confabulation check: no concept enters the map without
  tracing to something external (a source for `concept`, a pulled artifact for
  `system`).
- `coverage.surveyed` is non-empty — a map that surveyed nothing is not a map.

A claim whose only support is the model's prior — not a Survey source or a
pulled artifact — does not belong in `key_concepts` at the asserted confidence.
Either ground it or move it to the Calibrate stage's known/suspected-unknown
lists.
