# Vertex map: FIXTURE (bad)

Deliberately malformed. The Layer-0 self-test in ./verify requires this to
FAIL. Defects planted on purpose: no Route stage; invalid profile; a
key_concept with an empty source; empty coverage.surveyed; only one
falsification condition; no suspected-unknown-unknowns list.

## Frame
x
## Survey
y
## Map
```yaml
domain: "fixture domain"
competency_target: "x"
profile: "vibes"
surveyed_at: "2026-06-26"
subdomains:
  - name: "a"
    one_line: "x"
    maturity: "active"
prerequisite_dag: []
key_concepts:
  - term: "t1"
    gloss: "g"
    source: ""
live_controversies: []
canonical_sources: []
silos_and_bridges: []
coverage:
  surveyed: []
  deliberately_out_of_scope: []
```
## Calibrate
### A. Confidence bands
a: high.
### B. Falsification
This map is wrong if nothing.
### C. Known-unknowns
Known-unknowns: none.
