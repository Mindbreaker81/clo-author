#!/usr/bin/env python3
"""Convert .claude/agents/*.md (YAML frontmatter) -> .codex/agents/*.toml"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_AGENTS = REPO_ROOT / ".claude" / "agents"
CODEX_AGENTS = REPO_ROOT / ".codex" / "agents"

DEFAULT_MODEL = "gpt-4.1"

WRITE_TOOLS = {"Write", "Edit", "Bash", "Task"}

HIGH_REASONING = {
    "orchestrator", "coder", "data-engineer", "strategist",
    "coder-critic", "strategist-critic",
    "domain-referee", "methods-referee", "editor"
}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and markdown body."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    fm_text, body = match.groups()
    fm = {}
    for line in fm_text.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm, body.strip()


def infer_sandbox(tools_str: str) -> str:
    tools = {t.strip() for t in tools_str.split(",")}
    return "workspace-write" if tools & WRITE_TOOLS else "read-only"


def escape_toml_multiline(text: str) -> str:
    return text.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')


def convert_agent(md_path: Path) -> str:
    """Convert a single .md agent to .toml content."""
    text = md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    name = fm.get("name", md_path.stem)
    description = fm.get("description", "")
    tools = fm.get("tools", "Read")
    sandbox = infer_sandbox(tools)
    reasoning = "high" if name in HIGH_REASONING else "medium"

    lines = [
        f'name = "{name}"',
        f'description = "{description}"',
        f'model = "{DEFAULT_MODEL}"',
        f'sandbox_mode = "{sandbox}"',
        f'model_reasoning_effort = "{reasoning}"',
        f'developer_instructions = """',
        escape_toml_multiline(body),
        '"""',
    ]
    return "\n".join(lines) + "\n"


def main():
    CODEX_AGENTS.mkdir(parents=True, exist_ok=True)
    converted = 0
    for md_file in sorted(CLAUDE_AGENTS.glob("*.md")):
        toml_content = convert_agent(md_file)
        out_path = CODEX_AGENTS / f"{md_file.stem}.toml"
        out_path.write_text(toml_content, encoding="utf-8")
        converted += 1
        print(f"  {md_file.name} -> {out_path.name}")
    print(f"\nConverted {converted} agents.")


if __name__ == "__main__":
    main()
