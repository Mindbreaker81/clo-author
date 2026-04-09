#!/usr/bin/env python3
"""Apply manual patches to generated .codex/agents/*.toml after conversion.

These are Codex-specific additions that don't exist in .claude/agents/*.md.
Run after convert_agents_to_codex.py.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CODEX_AGENTS = REPO_ROOT / ".codex" / "agents"

NICKNAME_MAP = {
    "coder": '["Analyst", "Scripter", "Pipeline"]',
    "coder-critic": '["Auditor", "Inspector", "Checker"]',
    "writer": '["Drafter", "Scribe", "Author"]',
    "librarian": '["Scholar", "Searcher", "Curator"]',
    "explorer": '["Scout", "Surveyor", "Mapper"]',
}

ORCHESTRATOR_CODEX_SECTION = """
## Codex-Specific Dispatch

When running under Codex, use `spawn_agent` to dispatch workers and critics. Example:

1. Spawn worker: `spawn_agent(agent="coder", prompt="Implement analysis plan from strategy_memo.md")`
2. Wait for result: `wait_agent`
3. Spawn critic: `spawn_agent(agent="coder-critic", prompt="Review the coder output in scripts/R/")`
4. Wait and evaluate score
5. If score < 80, send feedback to worker via `send_input`

For parallel dispatch (e.g., librarian + explorer simultaneously):
1. `spawn_agent(agent="librarian", prompt="...")`
2. `spawn_agent(agent="explorer", prompt="...")`
3. Wait for both, then proceed to strategy phase.

Available workers: coder, data-engineer, writer, strategist, librarian, explorer, storyteller, verifier.
Available critics: coder-critic, strategist-critic, writer-critic, librarian-critic, explorer-critic, storyteller-critic.
Available reviewers: domain-referee, methods-referee, editor."""


def add_nicknames():
    """Insert nickname_candidates after model_reasoning_effort line."""
    patched = 0
    for agent_name, nicknames in NICKNAME_MAP.items():
        toml_path = CODEX_AGENTS / f"{agent_name}.toml"
        if not toml_path.exists():
            continue
        content = toml_path.read_text(encoding="utf-8")
        if "nickname_candidates" in content:
            continue
        content = content.replace(
            'developer_instructions = """',
            f'nickname_candidates = {nicknames}\ndeveloper_instructions = """',
        )
        toml_path.write_text(content, encoding="utf-8")
        patched += 1
    print(f"  Nicknames: patched {patched} agents")


def patch_orchestrator():
    """Append Codex dispatch section to orchestrator."""
    toml_path = CODEX_AGENTS / "orchestrator.toml"
    if not toml_path.exists():
        return
    content = toml_path.read_text(encoding="utf-8")
    if "Codex-Specific Dispatch" in content:
        print("  Orchestrator: already patched")
        return
    # Insert before closing triple-quote
    content = content.rstrip()
    if content.endswith('"""'):
        content = content[:-3] + ORCHESTRATOR_CODEX_SECTION + '\n"""\n'
    toml_path.write_text(content, encoding="utf-8")
    print("  Orchestrator: patched with Codex dispatch section")


def main():
    print("Applying post-conversion patches...")
    add_nicknames()
    patch_orchestrator()
    print("Patches complete.")


if __name__ == "__main__":
    main()
