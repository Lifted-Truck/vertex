# Edit Brief — Vertex Skill: replace the concept/system binary with the Field/Artifact/System trinary

**For:** the Claude Code agent maintaining the `vertex` skill.
**Type:** revision of an existing, already-built skill. Do not rebuild from scratch. Read the current `vertex/SKILL.md`, `references/terrain-schema.md`, `references/calibration.md`, and any `scripts/` and Layer-0 validator, then apply the changes below. Where the actual files differ from what this brief assumes, preserve the *intent* of each change rather than the literal target text.

---

## 1. Why this change (do not skip — it governs every edit)

The v1 skill sorts delves into `concept` vs `system`. That binary was cut along the wrong axis: it sorts by **grounding instrument** (search vs. local artifact pull), not by **the object being mapped**. "System" was a bucket meaning "things I reconnoiter with my hands instead of with search" — a tool partition, not a terrain partition. That's why the object of a "system delve" was never well-defined.

Re-cut by the ontology of the terrain — *what would settle a dispute about it* — yields **three** types, not two. The old `system` bucket was two distinct objects glued together because they shared a grounding instrument.

The routing diagnostic, used everywhere below:

> **What would settle a dispute about this terrain — the literature, the object itself, or watching it run?**
> Literature → **Field.** The object itself → **Artifact.** Watching it run → **System.**

### The three terrain types

- **Field** — an open body of knowledge or practice (a discipline, a theory, an ecosystem-as-subject). Unbounded, distributed, contested, evolving. Settled by triangulating fallible sources. Has true unknown-unknowns; the field may be larger and differently shaped than any survey reached. Dominant failure mode: **confabulation** (the confident, well-organized map of a field that was partly invented). This is the old `concept`, essentially unchanged.

- **Artifact** — a closed, determinate object you could in principle exhaustively enumerate (a specific codebase, a document corpus, a dataset, a filesystem). Settled by **reading the object itself — the artifact is its own oracle.** Ignorance is bounded ("haven't looked yet") and a delve can actually *finish*. Dominant failure mode: **the static surface not predicting dynamic behavior** (the file tree doesn't tell you about the race condition); and the completeness illusion (claiming the whole when only part was read).

- **System** — a live, behaving thing whose structure is *inferred from how it acts* (a running service under load, an organization, a market). There is no literature that *is* it and you cannot read it; you **instrument** it (logs, traces, telemetry, interviews) and infer structure from behavior. Emergent, partially opaque even with full access to its parts, never completable; unknown-unknowns are emergent rather than merely unread. Dominant failure mode: **mistaking inferred structure for observed behavior** (over-fitting a clean model to noisy observations).

### Naming note (so the agent doesn't fight the rename)
The word "system" in v1 was applied to the *most enumerable* object — a greppable codebase — which is precisely the **least** system-like terrain (it has no emergent behavior; you can list every file). Under the trinary, the greppable codebase is an **Artifact**, and "System" is reserved for genuinely emergent, behavior-inferred objects. The v1 `system` profile's *grounding scripts* (file tree, grep, deps) belong to **Artifact**, not to the new `System`.

### Composition (important — terrains are typed, not situations)
A real entry usually decomposes into more than one delve. Example: "I'm picking up an unfamiliar JUCE plugin repo" is simultaneously an **Artifact** delve (read the repo), a **Field** delve (JUCE idioms and audio-plugin domain knowledge — triangulate the docs/ecosystem), and potentially a **System** delve (why the running plugin glitches under buffer pressure — instrument it). The skill must support **composite delves**: detect the constituent types, run one Survey→Map per type, and merge into a combined map.

---

## 2. Edits

Apply in order. Each item states the target; reconcile with the actual file.

### 2.1 — Replace the profile flag with a terrain-type
Wherever v1 reads the `concept|system` argument (likely `$1`):
- New values: `field | artifact | system`. Default to `field` when absent (this replaces the old `concept` default).
- The flag is now a **hint/override**, not the sole router. Frame (2.2) detects type via the diagnostic; an explicit flag overrides detection.
- Migration mapping for any persisted maps or examples: old `concept` → `field`; old `system` → **decide per case** between `artifact` and `system` using the diagnostic (most existing `system` runs were almost certainly **artifact**). Do not auto-map `system`→`system`; flag any ambiguous case for the user.

### 2.2 — Frame stage: add type routing + composite detection
In the Frame section of `SKILL.md`, after fixing the domain boundary and competency target, insert a routing step:
1. Apply the diagnostic question to classify the terrain as `field`, `artifact`, or `system`.
2. Check for composition: if settling a dispute about the entry would require *more than one* of {literature, the object, watching it run}, the delve is composite. Enumerate the constituent typed sub-delves.
3. Record `terrain_type` (single value, or a list for composite).
For composite delves, run stages 2–4 (Survey/Map/Route) once per constituent type, then produce a single merged map with a top-level note on how the sub-maps relate (e.g., which Field concepts explain which Artifact structures).

### 2.3 — Survey stage: fork three ways
Replace the two-way grounding fork with three:
- **field** → web search + source triangulation across subareas, schools, key figures, canonical texts, open disputes. Reach for *disconfirming* sources, not only corroborating ones.
- **artifact** → pull and **read the object**: file tree, `grep`, dependency manifests, schemas, the real API surface. The artifact is its own oracle — prefer reading the thing over asserting about it. Track what was read vs. not (ignorance here is bounded and must be reported as coverage).
- **system** → **instrument behavior**: logs, traces, telemetry, load/latency observations, or interviews for a human system. Infer structure from observed behavior. Never assert structure from a static surface alone — that's the Artifact move, and using it here is the System failure mode.
Keep the existing recommendation to run Survey in a forked/subagent context for all three.

### 2.4 — `references/terrain-schema.md`: add `terrain_type` + a type-conditional block
Keep the shared spine (`domain`, `competency_target`, `surveyed_at`, `coverage`, source-tagging). Add:
- `terrain_type: field | artifact | system` (or a list for composite).
- A **type-specific section**, only one of which is populated per (sub-)map:

```
# FIELD block (≈ current schema)
subdomains, prerequisite_dag, key_concepts (each with source),
live_controversies, canonical_sources, silos_and_bridges

# ARTIFACT block
surface_inventory:    [ modules / entry points / files of record ]
read_coverage:        { read: [..], unread: [..] }   # bounded — this can reach "complete"
static_structure:     [ how the parts depend / call / compose ]
dynamic_behavior_gaps:[ what the static read CANNOT tell you — concurrency,
                        runtime config, side effects, env-dependent paths ]

# SYSTEM block
observed_behaviors:   [ what it actually did, with the observation source ]
inferred_structure:   [ each item explicitly tagged INFERRED, not observed ]
instrumentation_used: [ logs / traces / interviews / load tests ]
behavioral_unknowns:  [ emergent regions not yet provoked or observed ]
```
Retain the rule that empty fields are explicit (`"none found"` / `"unknown"`), never silently omitted.

### 2.5 — `references/calibration.md`: fork the doctrine per type (this is the load-bearing edit)
The comfort-convergence / El Dorado check stays **universal** — it is the residue with the most durable reason to persist, and it remains the mandatory final pass for every type. Do not weaken it. Add a type-specific check ahead of it:

- **Field** → guard **confabulation.** Did Survey reach disconfirming sources or only corroborating ones? Downgrade any structure whose only support was the model's prior. Populate suspected unknown-unknowns (a Field with an empty unknown-unknowns list is the tool failing).
- **Artifact** → guard **static-vs-dynamic and the completeness illusion.** Report `read_coverage` honestly (X of Y modules actually read). Every behavioral claim that wasn't *observed running* must be tagged as inferred-from-static-read. Populate `dynamic_behavior_gaps` — the things the read cannot predict.
- **System** → guard **inference-as-observation.** Every structural claim must trace to an observed behavior and be tagged INFERRED where it is. Flag where a clean model may be over-fit to noisy observation. `behavioral_unknowns` must be non-empty; emergent unknown-unknowns are expected, not a defect.

Then the universal comfort-convergence check (unchanged): does the map *feel* clean/authoritative, and where might that polish cover a gap; name the single claim you're least entitled to.

### 2.6 — Cardinal rule: keep, but sharpen per type
Keep "chart what is there; never confabulate terrain that isn't." Add the per-type sharpening to the relevant stage prompts:
- Artifact: **never assert what you haven't read.**
- System: **never present inference as observation.**

### 2.7 — Layer-0 validator: branch on `terrain_type`
Update the deterministic gate to:
- read `terrain_type` and validate the **type-appropriate** schema block is present and populated;
- require the **type-appropriate** calibration fields to be non-empty (e.g., `dynamic_behavior_gaps` for artifact; tagged `inferred_structure` + non-empty `behavioral_unknowns` for system; suspected-unknown-unknowns for field);
- for composite maps, validate each sub-map against its own type;
- keep the universal checks (all five stages present; comfort-convergence block present).

### 2.8 — `scripts/`
The v1 `system`-profile scripts (file tree, deps, grep) move conceptually under **artifact**. Rename/retag references accordingly. If a genuine `system` profile is wanted, its tooling is instrumentation-oriented (log/trace parsing), which is a separate future addition — do not fabricate it now; leave a stub note.

---

## 3. Preserve (do not regress)
- The protected, non-skippable **Calibrate** gate and its bundling in a separate reference file.
- The **universal comfort-convergence check**.
- **Persistence** to `vertex/<domain>.md` and the diffable-corpus property. (For composite delves, persist the merged map as one file.)
- Schema's **explicit-empty** discipline.

---

## 4. Acceptance checklist (agent self-verifies before reporting done)
- [ ] Flag accepts `field|artifact|system`, defaults to `field`; old `concept`/`system` values handled per 2.1 migration (no silent `system`→`system`).
- [ ] Frame routes via the diagnostic and detects composite delves.
- [ ] Survey forks three ways; system path instruments behavior and never asserts structure from static surface alone.
- [ ] Schema carries `terrain_type` + exactly one populated type block per (sub-)map; empties explicit.
- [ ] Calibrate forks per type AND retains the universal comfort-convergence pass.
- [ ] Layer-0 branches on `terrain_type` and validates composite sub-maps.
- [ ] Cardinal-rule sharpenings present in artifact/system stage prompts.
- [ ] A known-domain Layer-E run on each type produces a non-empty type-appropriate unknowns field.

---

## 5. Surface to the user — do not decide unilaterally
- Any existing persisted map whose old `system` type is ambiguous between `artifact` and `system`.
- Whether composite delves should persist as one merged file (assumed) or one file per constituent type.
- Whether to scaffold the real `system`-instrumentation tooling now or leave the stub (2.8).
- Overwrite-in-place vs. timestamped versioning for persisted maps (open since the original scaffold).
