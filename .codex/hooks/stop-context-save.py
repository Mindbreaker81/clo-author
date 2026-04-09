#!/usr/bin/env python3
"""Stop hook: check context state before session ends."""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        data = {}

    cwd = Path(data.get("cwd", "."))
    plans_dir = cwd / "quality_reports" / "plans"
    memory = cwd / "MEMORY.md"

    reminders = []

    # Check for recently modified plans (last 24h) that are still DRAFT
    if plans_dir.exists():
        cutoff = datetime.now().timestamp() - 86400
        for plan in plans_dir.glob("*.md"):
            if plan.stat().st_mtime > cutoff:
                content = plan.read_text(encoding="utf-8", errors="ignore")
                if "DRAFT" in content.upper() and "COMPLETED" not in content.upper():
                    reminders.append(f"Draft plan pending: {plan.name}")
                    break

    if not memory.exists():
        reminders.append("MEMORY.md not found -- session learnings may be lost")

    if reminders:
        result = {"systemMessage": "Context check: " + "; ".join(reminders)}
        json.dump(result, sys.stdout)


if __name__ == "__main__":
    main()
