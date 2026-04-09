#!/usr/bin/env python3
"""Pre-Bash hook: block commands that would modify protected files."""
import json
import sys
import re

PROTECTED_PATTERNS = [
    r"settings\.json",
    r"config\.toml",
    r"strategy[-_]memo.*\.md",
    r"referee[-_]report.*\.md",
    r"quality[-_]score.*\.json",
]

WRITE_INDICATORS = [">", ">>", "tee ", "mv ", "cp ", "sed -i", "rm "]


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")

    for pattern in PROTECTED_PATTERNS:
        if re.search(pattern, command):
            if any(ind in command for ind in WRITE_INDICATORS):
                result = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            f"Protected file pattern matched: {pattern}. "
                            "Edit manually or remove protection in .codex/hooks/pre-bash-guard.py"
                        ),
                    }
                }
                json.dump(result, sys.stdout)
                return

    sys.exit(0)


if __name__ == "__main__":
    main()
