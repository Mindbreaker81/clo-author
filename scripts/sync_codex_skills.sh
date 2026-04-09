#!/bin/bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
SRC="$REPO_ROOT/.claude/skills"
DST="$REPO_ROOT/.agents/skills"

mkdir -p "$DST"

# Limpiar symlinks muertos
find "$DST" -maxdepth 1 -type l ! -exec test -e {} \; -delete

# Crear symlinks para cada skill
for skill_dir in "$SRC"/*/; do
    skill_name="$(basename "$skill_dir")"
    if [ ! -e "$DST/$skill_name" ]; then
        ln -s "../../.claude/skills/$skill_name" "$DST/$skill_name"
        echo "Linked: $skill_name"
    fi
done
echo "Skills sync complete."
