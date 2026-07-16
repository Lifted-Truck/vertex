#!/usr/bin/env bash
# survey_repo.sh — system-profile ground truth for the Survey stage.
# Prints a low-resolution map of the repo: file tree, language/LoC breakdown,
# and likely entry points. Read-only. Run from the project root.
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

echo "=== ROOT ==="
pwd
echo

echo "=== FILE TREE (depth 3, code/config only, vendor dirs pruned) ==="
PRUNE='-name node_modules -o -name .git -o -name dist -o -name build -o -name target -o -name .venv -o -name venv -o -name __pycache__ -o -name vendor'
if command -v tree >/dev/null 2>&1; then
  tree -L 3 -I 'node_modules|.git|dist|build|target|.venv|venv|__pycache__|vendor'
else
  find . -maxdepth 3 \( $PRUNE \) -prune -o -type f -print | sed 's|^\./||' | sort
fi
echo

echo "=== FILE COUNT BY EXTENSION (top 25) ==="
find . \( $PRUNE \) -prune -o -type f -name '*.*' -print \
  | sed 's|.*\.|.|' | sort | uniq -c | sort -rn | head -25
echo

echo "=== APPROX LINES OF CODE BY EXTENSION (top 15) ==="
find . \( $PRUNE \) -prune -o -type f -name '*.*' -print0 \
  | xargs -0 wc -l 2>/dev/null \
  | awk '{ ext=$2; sub(/.*\./,".",ext); loc[ext]+=$1 } END { for (e in loc) printf "%10d  %s\n", loc[e], e }' \
  | sort -rn | head -15
echo

echo "=== LIKELY ENTRY POINTS / MANIFESTS ==="
for f in package.json pyproject.toml setup.py setup.cfg requirements.txt \
         Cargo.toml go.mod pom.xml build.gradle Gemfile composer.json \
         Makefile Dockerfile docker-compose.yml main.py app.py index.js \
         src/main.rs cmd/main.go; do
  [ -e "$f" ] && echo "  present: $f"
done
echo

echo "=== README HEADINGS (first file found) ==="
README=$(find . -maxdepth 2 -iname 'readme*' | head -1 || true)
if [ -n "${README:-}" ]; then
  echo "  ($README)"
  grep -E '^#{1,3} ' "$README" | head -30 || true
else
  echo "  none found"
fi
