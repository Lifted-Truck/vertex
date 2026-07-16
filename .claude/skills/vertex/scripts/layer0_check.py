#!/usr/bin/env python3
"""layer0_check.py — deterministic, CI-blocking gate for a Vertex terrain map.

Parses a persisted vertex/<domain>_<date>.md artifact and FAILS (exit 1) unless
the run is structurally sound. This gate is mechanical and cannot be charmed by
fluency — it catches the structural ways a run degrades. It does NOT judge
whether the terrain is accurate (that is the Layer-E known-domain audit, run by
a human).

Checks:
  1. All five stage sections present (Frame, Survey, Map, Route, Calibrate).
  2. The Map block is a fenced ```yaml block that validates against
     references/terrain-schema.md: all required top-level keys present;
     profile in {concept, system}; every key_concept has a non-empty source;
     coverage.surveyed non-empty.
  3. Calibrate contains: confidence-band tags, >= 3 falsification conditions,
     and BOTH unknown lists (known-unknowns and suspected unknown-unknowns),
     kept separate.

Usage: python3 layer0_check.py vertex/<file>.md
Exit:  0 = pass, 1 = fail, 2 = usage / file error.

PyYAML is used if available for a precise schema check; otherwise a regex
fallback enforces the same rules structurally.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_STAGES = ["Frame", "Survey", "Map", "Route", "Calibrate"]
REQUIRED_KEYS = [
    "domain", "competency_target", "profile", "surveyed_at", "subdomains",
    "prerequisite_dag", "key_concepts", "live_controversies",
    "canonical_sources", "silos_and_bridges", "coverage",
]

failures: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def find_yaml_block(text: str) -> str | None:
    m = re.search(r"```ya?ml\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else None


def stage_body(text: str, stage: str) -> str:
    """Return the markdown under a stage heading, including its subsections.

    Reads from the stage heading until the next heading of the SAME or higher
    level (fewer-or-equal '#'), so deeper '###' subsections stay inside.
    """
    m = re.search(
        rf"^(#{{1,6}})\s*(?:\d+\.\s*)?{re.escape(stage)}\b.*?$",
        text, re.MULTILINE | re.IGNORECASE,
    )
    if not m:
        return ""
    level = len(m.group(1))
    rest = text[m.end():]
    nxt = re.search(rf"^#{{1,{level}}}\s", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def check_stages(text: str) -> None:
    for stage in REQUIRED_STAGES:
        if not re.search(rf"^#{{1,6}}\s*(?:\d+\.\s*)?{re.escape(stage)}\b",
                         text, re.MULTILINE | re.IGNORECASE):
            fail(f"missing stage section: {stage}")


def check_map_with_yaml(block: str) -> bool:
    try:
        import yaml  # type: ignore
    except Exception:
        return False
    try:
        data = yaml.safe_load(block)
    except Exception as e:  # noqa: BLE001
        fail(f"Map yaml does not parse: {e}")
        return True
    if not isinstance(data, dict):
        fail("Map yaml is not a mapping")
        return True
    for key in REQUIRED_KEYS:
        if key not in data:
            fail(f"Map missing required key: {key}")
    prof = data.get("profile")
    if prof not in ("concept", "system"):
        fail(f"profile must be concept|system, got: {prof!r}")
    for i, c in enumerate(data.get("key_concepts") or []):
        if not isinstance(c, dict) or not str(c.get("source", "")).strip():
            fail(f"key_concepts[{i}] has empty/missing source")
    cov = data.get("coverage") or {}
    if not (isinstance(cov, dict) and cov.get("surveyed")):
        fail("coverage.surveyed is empty — a map that surveyed nothing is not a map")
    for sd in data.get("subdomains") or []:
        mat = isinstance(sd, dict) and sd.get("maturity")
        if mat not in ("established", "active", "contested"):
            fail(f"subdomain maturity invalid: {mat!r}")
    return True


def check_map_regex(block: str) -> None:
    warn("PyYAML not installed — using regex fallback for the Map schema check")
    for key in REQUIRED_KEYS:
        if not re.search(rf"^{key}\s*:", block, re.MULTILINE):
            fail(f"Map missing required key: {key}")
    if not re.search(r"^profile\s*:\s*(concept|system)\b", block, re.MULTILINE):
        fail("profile must be concept|system")
    # Within key_concepts, every 'term:' must be matched by a non-empty 'source:'.
    kc = re.search(r"^key_concepts\s*:(.*?)(?=^\w|\Z)", block,
                   re.DOTALL | re.MULTILINE)
    if kc:
        terms = len(re.findall(r"\bterm\s*:", kc.group(1)))
        sources = len(re.findall(r"\bsource\s*:\s*\S+", kc.group(1)))
        if terms == 0:
            fail("key_concepts has no entries")
        elif sources < terms:
            fail(f"key_concepts: {terms} terms but only {sources} non-empty sources")


def check_calibrate(text: str) -> None:
    body = stage_body(text, "Calibrate")
    if not body.strip():
        fail("Calibrate section is empty")
        return
    low = body.lower()
    if not re.search(r"\b(high|medium|low)\b", low):
        fail("Calibrate: no confidence-band tags (high/medium/low) found")
    falsifications = len(re.findall(r"wrong if", low))
    if falsifications < 3:
        fail(f"Calibrate: need >= 3 'wrong if ___' conditions, found {falsifications}")
    has_known = "known-unknown" in low or "known unknown" in low
    has_suspected = "suspected unknown-unknown" in low or "unknown-unknown" in low \
        or "unknown unknown" in low
    if not has_known:
        fail("Calibrate: missing known-unknowns list")
    if not has_suspected:
        fail("Calibrate: missing suspected unknown-unknowns list")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 layer0_check.py vertex/<file>.md", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"error: not a file: {path}", file=sys.stderr)
        return 2
    text = path.read_text()

    check_stages(text)
    block = find_yaml_block(text)
    if block is None:
        fail("no fenced ```yaml Map block found")
    elif not check_map_with_yaml(block):
        check_map_regex(block)
    check_calibrate(text)

    for w in warnings:
        print(f"WARN  {w}")
    if failures:
        print(f"\nLAYER-0 FAIL ({len(failures)}): {path}")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"LAYER-0 PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
