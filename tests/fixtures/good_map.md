# Vertex map: FIXTURE (good)

Minimal well-formed terrain map. The Layer-0 self-test in ./verify requires
this to PASS. Keep it schema-valid; if the schema changes, update this fixture
in the same change.

## 1. Frame
Competency target and boundary.

## 2. Survey
Surveyed with sources.

## 3. Map
```yaml
domain: "fixture domain"
competency_target: "hold a conversation"
profile: "concept"
surveyed_at: "2026-06-26"
subdomains:
  - name: "a"
    one_line: "x"
    maturity: "active"
prerequisite_dag:
  - node: "a"
    depends_on: []
key_concepts:
  - term: "t1"
    gloss: "g"
    source: "https://example.com"
live_controversies: []
canonical_sources: []
silos_and_bridges: []
coverage:
  surveyed: ["a"]
  deliberately_out_of_scope: []
```

## 4. Route
1. do a.

## 5. Calibrate
### A. Confidence bands
a: high. low-confidence load-bearing: 0.
### B. Falsification
This map is wrong if a is not a subdomain. This map is wrong if t1 is fringe. This map is wrong if the field merges a and b.
### C. Known-unknowns vs suspected unknown-unknowns
Known-unknowns: none named.
Suspected unknown-unknowns: probably a whole subarea b.
### D. Comfort-convergence check
Does this map feel clean? No.
