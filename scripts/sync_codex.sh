#!/bin/bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
echo "=== Syncing Codex infrastructure from Claude Code ==="

# 1. Convert agents
echo "[1/3] Converting agents..."
python3 "$REPO_ROOT/scripts/convert_agents_to_codex.py"

# 1b. Apply manual patches (nicknames, orchestrator dispatch)
echo "[1b/4] Applying patches..."
python3 "$REPO_ROOT/.codex/patches/post-convert.py"

# 2. Sync skills
echo "[2/4] Syncing skills..."
bash "$REPO_ROOT/scripts/sync_codex_skills.sh"

# 3. Verify structure
echo "[3/4] Verifying structure..."
ERRORS=0
[ -f "$REPO_ROOT/.codex/config.toml" ] || { echo "MISSING: .codex/config.toml"; ERRORS=$((ERRORS+1)); }
[ -f "$REPO_ROOT/.codex/hooks.json" ] || { echo "MISSING: .codex/hooks.json"; ERRORS=$((ERRORS+1)); }
[ -d "$REPO_ROOT/.codex/agents" ] || { echo "MISSING: .codex/agents/"; ERRORS=$((ERRORS+1)); }
[ -d "$REPO_ROOT/.agents/skills" ] || { echo "MISSING: .agents/skills/"; ERRORS=$((ERRORS+1)); }

AGENT_COUNT=$(ls "$REPO_ROOT/.codex/agents/"*.toml 2>/dev/null | wc -l)
SKILL_COUNT=$(ls -d "$REPO_ROOT/.agents/skills/"*/ 2>/dev/null | wc -l)
echo "  Agents: $AGENT_COUNT TOML files"
echo "  Skills: $SKILL_COUNT linked"

if [ "$ERRORS" -gt 0 ]; then
    echo "FAILED: $ERRORS errors found."
    exit 1
fi
echo "=== Sync complete ==="
