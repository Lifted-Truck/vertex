#!/usr/bin/env python3
"""survey_deps.py — system-profile dependency-graph extraction for Survey.

Read-only. Walks common manifest files and prints the declared dependency
surface so the Map is built against the artifact, not the model's prior.
Dependency-free (stdlib only); parses what it can and skips the rest.

Usage: python3 survey_deps.py [project_root]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def parse_package_json(p: Path) -> None:
    try:
        data = json.loads(p.read_text())
    except Exception as e:  # noqa: BLE001
        print(f"  (could not parse {p}: {e})")
        return
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        deps = data.get(key) or {}
        if deps:
            print(f"  [{key}] ({len(deps)})")
            for name, ver in sorted(deps.items()):
                print(f"    {name} {ver}")


def parse_requirements(p: Path) -> None:
    lines = [
        ln.strip()
        for ln in p.read_text().splitlines()
        if ln.strip() and not ln.strip().startswith("#") and not ln.strip().startswith("-")
    ]
    print(f"  ({len(lines)} requirements)")
    for ln in lines:
        print(f"    {ln}")


def parse_pyproject(p: Path) -> None:
    text = p.read_text()
    # tomllib is 3.11+; fall back to a light regex sweep if unavailable.
    try:
        import tomllib  # type: ignore
        data = tomllib.loads(text)
    except Exception:
        deps = re.findall(r'"([A-Za-z0-9_.\-]+(?:[<>=!~ ].*?)?)"', text)
        print("  (regex fallback — tomllib unavailable)")
        for d in deps[:80]:
            print(f"    {d}")
        return
    proj = data.get("project", {})
    for d in proj.get("dependencies", []) or []:
        print(f"    {d}")
    for grp, items in (proj.get("optional-dependencies", {}) or {}).items():
        print(f"  [optional: {grp}]")
        for d in items:
            print(f"    {d}")
    poetry = data.get("tool", {}).get("poetry", {})
    for grp in ("dependencies", "dev-dependencies"):
        deps = poetry.get(grp) or {}
        if deps:
            print(f"  [poetry.{grp}]")
            for name, ver in deps.items():
                print(f"    {name} {ver}")


def parse_simple_lines(p: Path, pattern: str) -> None:
    for m in re.finditer(pattern, p.read_text()):
        print(f"    {m.group(1).strip()}")


HANDLERS = {
    "package.json": parse_package_json,
    "requirements.txt": parse_requirements,
    "pyproject.toml": parse_pyproject,
    "Cargo.toml": lambda p: parse_simple_lines(
        p, r"^\s*([A-Za-z0-9_\-]+\s*=\s*.+)$"
    ),
    "go.mod": lambda p: parse_simple_lines(p, r"^\s*require\s+(.+)$|^\s+([^\s]+\s+v[^\s]+)$"),
}


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    found = False
    for name, handler in HANDLERS.items():
        for p in root.rglob(name):
            if any(part in {"node_modules", ".git", "vendor", ".venv", "venv"} for part in p.parts):
                continue
            found = True
            section(f"{name}  ({p.relative_to(root)})")
            try:
                handler(p)
            except Exception as e:  # noqa: BLE001
                print(f"  (handler error: {e})")
    if not found:
        section("RESULT")
        print("  no recognized dependency manifests found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
