# Plan: Soporte Dual Claude Code + OpenAI Codex

**Fecha:** 2026-04-09
**Estado:** DRAFT
**Esfuerzo estimado:** 6-10 dias
**Prerequisito:** Cuenta OpenAI con acceso a Codex (API o ChatGPT Plus/Team)
**Documento base:** `quality_reports/specs/2026-04-09_codex-compatibility-report.md`

---

## Principio de Diseno

Mantener `.claude/` intacto como fuente de verdad. Generar `.codex/` y `.agents/` de forma derivada cuando sea posible (script de conversion + symlinks). Esto evita duplicacion manual y reduce el riesgo de divergencia.

---

## Fase 1: Cimientos (dia 1)

### 1.1 Crear estructura de directorios Codex

```bash
mkdir -p .codex/agents
mkdir -p .codex/rules
mkdir -p .agents/skills
```

### 1.2 Crear `.codex/config.toml`

```toml
#:schema https://developers.openai.com/codex/config-schema.json

# --- Modelo y ejecucion ---
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "workspace-write"
approval_policy = "on-request"

# --- Features ---
[features]
multi_agent = true
codex_hooks = true
shell_tool = true
web_search = true

# --- Subagentes ---
[agents]
max_threads = 6
max_depth = 1

# --- Instrucciones del proyecto ---
# Codex lee AGENTS.md por defecto; CLAUDE.md se anade como fallback
project_doc_fallback_filenames = ["CLAUDE.md"]
project_doc_max_bytes = 65536
```

### 1.3 Symlinks de Skills

Los SKILL.md de Claude Code y Codex usan el mismo formato (agentskills.io). Crear symlinks desde `.agents/skills/` a `.claude/skills/*/`:

```bash
# Script: scripts/sync_codex_skills.sh
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
        ln -s "../.claude/skills/$skill_name" "$DST/$skill_name"
        echo "Linked: $skill_name"
    fi
done
echo "Skills sync complete."
```

### 1.4 Verificacion Fase 1

- [ ] `codex --cd . "Summarize the current instructions."` muestra contenido de AGENTS.md y CLAUDE.md
- [ ] `ls -la .agents/skills/` muestra symlinks a los 11 skills
- [ ] `.codex/config.toml` parsea sin errores

---

## Fase 2: Conversion de Agentes (dias 2-3)

### 2.1 Mapeo de Agentes: Claude Code → Codex

Cada agente se clasifica por su rol (worker/critic/infrastructure) para asignar `sandbox_mode` y `model_reasoning_effort`:

| Agente | Rol | tools (Claude) | sandbox_mode (Codex) | model | reasoning_effort |
|--------|-----|----------------|---------------------|-------|-----------------|
| orchestrator | infra | R,W,E,Bash,Grep,Glob,Task | workspace-write | gpt-5.4 | high |
| coder | worker | R,W,E,Bash,Grep,Glob | workspace-write | gpt-5.4 | high |
| data-engineer | worker | R,W,E,Bash,Grep,Glob | workspace-write | gpt-5.4 | high |
| writer | worker | R,W,E,Bash,Grep,Glob | workspace-write | gpt-5.4 | medium |
| storyteller | worker | R,W,E,Bash,Grep,Glob | workspace-write | gpt-5.4 | medium |
| strategist | worker | R,W,Grep,Glob | workspace-write | gpt-5.4 | high |
| librarian | worker | R,W,Grep,Glob,Web | workspace-write | gpt-5.4 | medium |
| explorer | worker | R,W,Grep,Glob,Web | workspace-write | gpt-5.4 | medium |
| coder-critic | critic | R,Grep,Glob | read-only | gpt-5.4 | high |
| strategist-critic | critic | R,Grep,Glob | read-only | gpt-5.4 | high |
| writer-critic | critic | R,Grep,Glob | read-only | gpt-5.4 | medium |
| librarian-critic | critic | R,Grep,Glob | read-only | gpt-5.4 | medium |
| explorer-critic | critic | R,Grep,Glob | read-only | gpt-5.4 | medium |
| storyteller-critic | critic | R,Grep,Glob | read-only | gpt-5.4 | medium |
| domain-referee | critic | R,Grep,Glob | read-only | gpt-5.4 | high |
| methods-referee | critic | R,Grep,Glob | read-only | gpt-5.4 | high |
| editor | critic | R,Grep,Glob,Web | read-only | gpt-5.4 | high |
| verifier | infra | R,Grep,Glob,Bash | workspace-write | gpt-5.4 | medium |

**Regla de mapeo:**
- `tools` incluye Write/Edit → `sandbox_mode = "workspace-write"`
- `tools` solo Read/Grep/Glob → `sandbox_mode = "read-only"`
- Critics SIEMPRE read-only (separacion de poderes)

### 2.2 Script de Conversion: `scripts/convert_agents_to_codex.py`

```python
#!/usr/bin/env python3
"""Convert .claude/agents/*.md (YAML frontmatter) → .codex/agents/*.toml"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_AGENTS = REPO_ROOT / ".claude" / "agents"
CODEX_AGENTS = REPO_ROOT / ".codex" / "agents"

# Mapeo de tools → sandbox_mode
WRITE_TOOLS = {"Write", "Edit", "Bash", "Task"}

# Reasoning effort por patron de nombre
HIGH_REASONING = {
    "orchestrator", "coder", "data-engineer", "strategist",
    "coder-critic", "strategist-critic",
    "domain-referee", "methods-referee", "editor"
}

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extrae frontmatter YAML y cuerpo markdown."""
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
    """Escapa texto para TOML multiline string."""
    return text.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')

def convert_agent(md_path: Path) -> str:
    """Convierte un agente .md a contenido .toml."""
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
```

### 2.3 Ejemplo de Salida: `.codex/agents/coder.toml`

```toml
name = "coder"
description = "Implements the study design and analysis plan in code. Translates the strategy memo into working R/Stata/Python scripts that produce publication-ready tables and figures."
sandbox_mode = "workspace-write"
model_reasoning_effort = "high"
developer_instructions = """
You are a **research coder** — the analyst who translates the approved analysis plan into working scripts...

[... todo el cuerpo markdown del agente, intacto ...]
"""
```

### 2.4 Ejemplo de Salida: `.codex/agents/coder-critic.toml`

```toml
name = "coder-critic"
description = "Code critic for clinical analysis scripts. Reviews study-design alignment, statistical implementation, reproducibility, and publication outputs."
sandbox_mode = "read-only"
model_reasoning_effort = "high"
developer_instructions = """
You are a **code quality critic** for medical research scripts...

[... todo el cuerpo markdown del critic, intacto ...]
"""
```

### 2.5 Adaptaciones Manuales Post-Conversion

Despues del script automatico, revisar manualmente:

1. **orchestrator.toml**: Anadir nota sobre `spawn_agent` nativo de Codex en `developer_instructions`:
   ```
   When dispatching agents, use Codex native spawn_agent tool.
   Available agents: coder, data-engineer, writer, strategist, librarian, explorer, storyteller, verifier.
   Critics: coder-critic, strategist-critic, writer-critic, librarian-critic, explorer-critic, storyteller-critic.
   Reviewers: domain-referee, methods-referee, editor.
   ```

2. **Agentes con WebSearch/WebFetch** (librarian, explorer, editor): Verificar que `web_search = "live"` esta habilitado en config o anadir nota en developer_instructions.

3. **Referencias a `.claude/references/`**: Buscar y reemplazar con ruta neutra o dejar como esta (ambas herramientas pueden leer la ruta).

### 2.6 Verificacion Fase 2

- [ ] `python3 scripts/convert_agents_to_codex.py` ejecuta sin errores y genera 20 ficheros .toml
- [ ] Cada .toml tiene name, description, sandbox_mode, developer_instructions
- [ ] Critics tienen `sandbox_mode = "read-only"`
- [ ] Workers tienen `sandbox_mode = "workspace-write"`
- [ ] Contenido de developer_instructions coincide con el cuerpo markdown original

---

## Fase 3: Reglas y Gobernanza (dias 4-5)

### 3.1 Problema

Las reglas de Claude Code (`.claude/rules/*.md`) son documentos Markdown narrativos que guian el comportamiento del agente. Codex tiene dos mecanismos:

1. **AGENTS.md / developer_instructions**: Para guia de comportamiento (lo que el agente DEBE hacer)
2. **`.codex/rules/*.rules` (Starlark)**: Para control de EJECUCION de comandos (allow/prompt/forbidden)

### 3.2 Estrategia: Bifurcacion de Contenido

El contenido de las reglas Markdown se distribuye asi:

| Regla Claude Code | Destino Codex | Razon |
|-------------------|---------------|-------|
| `workflow.md` | Ya en AGENTS.md | Codex lo lee desde AGENTS.md |
| `agents.md` | Ya en AGENTS.md | Codex lo lee desde AGENTS.md |
| `quality.md` | Ya en AGENTS.md | Codex lo lee desde AGENTS.md |
| `content-standards.md` | `developer_instructions` de coder, data-engineer, writer | Especifico de ciertos agentes |
| `working-paper-format.md` | `developer_instructions` de writer, storyteller | Especifico de ciertos agentes |
| `logging.md` | `developer_instructions` del orchestrator | Infraestructura |
| `revision.md` | `developer_instructions` del editor | Especifico del editor |
| `meta-governance.md` | Ya en AGENTS.md | Codex lo lee desde AGENTS.md |

**Accion:** Verificar que AGENTS.md ya contiene la informacion clave de workflow, agents, quality y meta-governance (ya lo tiene). Para content-standards y working-paper-format, incluir referencia en el developer_instructions de los agentes relevantes:

```
Read `.claude/rules/content-standards.md` for table and figure standards.
```

### 3.3 Crear Reglas Starlark para Proteccion de Comandos

Fichero: `.codex/rules/safety.rules`

```python
# Proteger contra comandos destructivos
prefix_rule(
    pattern = ["rm", "-rf"],
    decision = "forbidden",
    justification = "Destructive recursive deletion blocked. Use targeted rm instead.",
    match = ["rm -rf /", "rm -rf ~", "rm -rf ."],
)

prefix_rule(
    pattern = ["rm", "-r"],
    decision = "prompt",
    justification = "Recursive deletion requires confirmation.",
)

# Permitir git sin fricciones
prefix_rule(
    pattern = ["git", "status"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "diff"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "log"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "add"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "commit"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "push"],
    decision = "prompt",
    justification = "Push to remote requires confirmation.",
)

# Permitir compilacion LaTeX
prefix_rule(
    pattern = ["xelatex"],
    decision = "allow",
)

prefix_rule(
    pattern = ["biber"],
    decision = "allow",
)

prefix_rule(
    pattern = ["latexmk"],
    decision = "allow",
)

# Permitir ejecucion de scripts de analisis
prefix_rule(
    pattern = ["Rscript"],
    decision = "allow",
)

prefix_rule(
    pattern = ["python3"],
    decision = "allow",
)

# Permitir quarto
prefix_rule(
    pattern = ["quarto", "render"],
    decision = "allow",
)
```

### 3.4 Verificacion Fase 3

- [ ] `codex execpolicy check --rules .codex/rules/safety.rules -- rm -rf /` devuelve `forbidden`
- [ ] `codex execpolicy check --rules .codex/rules/safety.rules -- git add .` devuelve `allow`
- [ ] `codex execpolicy check --rules .codex/rules/safety.rules -- git push origin main` devuelve `prompt`
- [ ] Agentes con content-standards en developer_instructions referencian la ruta correcta

---

## Fase 4: Hooks (dias 5-6)

### 4.1 Limitaciones Actuales de Codex Hooks

- **Experimentales** (feature flag requerido)
- `PreToolUse` solo intercepta `Bash` (no Write/Edit)
- No hay equivalente directo de `PreCompact` de Claude Code
- `SessionStart` funciona de forma similar

### 4.2 Crear `.codex/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.claude/hooks/post-compact-restore.py\"",
            "timeout": 10,
            "statusMessage": "Restoring session context"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/pre-bash-guard.py\"",
            "timeout": 5,
            "statusMessage": "Checking command safety"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/stop-context-save.py\"",
            "timeout": 10,
            "statusMessage": "Saving session context"
          }
        ]
      }
    ]
  }
}
```

### 4.3 Crear `.codex/hooks/pre-bash-guard.py`

Adaptacion de protect-files.sh para interceptar comandos Bash que modifiquen ficheros protegidos:

```python
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

def main():
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")

    # Buscar si el comando escribe a ficheros protegidos
    for pattern in PROTECTED_PATTERNS:
        if re.search(pattern, command):
            # Verificar si es un comando de escritura
            write_indicators = [">", ">>", "tee ", "mv ", "cp ", "sed -i", "rm "]
            if any(ind in command for ind in write_indicators):
                result = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"Protected file pattern matched: {pattern}. Edit manually."
                    }
                }
                json.dump(result, sys.stdout)
                return

    # Permitir por defecto
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 4.4 Crear `.codex/hooks/stop-context-save.py`

Equivalente funcional del pre-compact de Claude Code, ejecutado al final de cada turno:

```python
#!/usr/bin/env python3
"""Stop hook: remind to save context before session ends."""
import json
import sys
from pathlib import Path

def main():
    data = json.load(sys.stdin)

    # Solo actuar si ya fue continuado por Stop (evitar loop)
    if data.get("stop_hook_active", False):
        json.dump({"continue": False}, sys.stdout)
        return

    # Verificar si hay un plan activo sin guardar
    repo_root = Path(data.get("cwd", "."))
    plans_dir = repo_root / "quality_reports" / "plans"
    memory = repo_root / "MEMORY.md"

    reminders = []
    if not plans_dir.exists() or not any(plans_dir.iterdir()):
        reminders.append("No saved plans found in quality_reports/plans/")
    if not memory.exists():
        reminders.append("MEMORY.md not found")

    if reminders:
        result = {
            "systemMessage": "Context check: " + "; ".join(reminders),
        }
        json.dump(result, sys.stdout)
    # No bloquear, solo informar

if __name__ == "__main__":
    main()
```

### 4.5 Nota sobre Protect-Files

El hook `protect-files.sh` de Claude Code intercepta `Edit|Write` tools directamente. Codex NO puede hacer esto todavia (PreToolUse solo intercepta Bash). Opciones:

1. **Corto plazo:** El `pre-bash-guard.py` cubre comandos Bash que escriban a ficheros protegidos
2. **Medio plazo:** Esperar a que Codex extienda PreToolUse a mas tools
3. **Alternativa:** Usar permisos de filesystem del sandbox para proteger ficheros

Anadir nota en AGENTS.md:

```markdown
## Protected Files (applies to both Claude Code and Codex)
Do NOT modify these files without explicit user approval:
- `.claude/settings.json` / `.codex/config.toml`
- `strategy-memo-*.md`, `referee-report-*.md`, `quality-score-*.json`
```

### 4.6 Verificacion Fase 4

- [ ] `hooks.json` parsea correctamente
- [ ] SessionStart hook ejecuta post-compact-restore.py
- [ ] PreToolUse hook bloquea `bash -c "echo foo > settings.json"`
- [ ] Stop hook muestra recordatorio de contexto

---

## Fase 5: Subagentes y Orquestacion (dias 7-8)

### 5.1 Configuracion de Subagentes en config.toml

Ya configurado en Fase 1:
```toml
[agents]
max_threads = 6
max_depth = 1
```

### 5.2 Adaptacion del Orchestrator

El orchestrator de Codex usa `spawn_agent` nativo en lugar de `Task` tool. Anadir seccion al final de `developer_instructions` de `.codex/agents/orchestrator.toml`:

```markdown
## Codex-Specific Dispatch

Use `spawn_agent` to dispatch workers and critics. Example workflow:

1. Spawn worker: `spawn_agent(agent="coder", prompt="Implement analysis plan from strategy_memo.md")`
2. Wait for result: `wait_agent`
3. Spawn critic: `spawn_agent(agent="coder-critic", prompt="Review the coder output in scripts/R/")`
4. Wait and evaluate score
5. If score < 80, send feedback to worker via `send_input`

For parallel dispatch (e.g., librarian + explorer simultaneously):
1. `spawn_agent(agent="librarian", prompt="...")`
2. `spawn_agent(agent="explorer", prompt="...")`
3. Wait for both, then proceed to strategy phase.

Use `spawn_agents_on_csv` for batch operations like systematic literature reviews.
```

### 5.3 Nickname Candidates para Agentes

Anadir `nickname_candidates` a agentes que se instancian multiples veces para legibilidad en el TUI:

```toml
# En .codex/agents/coder.toml
nickname_candidates = ["Analyst", "Scripter", "Pipeline"]

# En .codex/agents/coder-critic.toml
nickname_candidates = ["Auditor", "Inspector", "Checker"]
```

### 5.4 Verificacion Fase 5

- [ ] Codex puede resolver `spawn_agent(agent="coder", ...)` al agente correcto
- [ ] Agentes criticos corren en read-only y no pueden escribir ficheros
- [ ] Orchestrator puede despachar multiples agentes en paralelo
- [ ] `max_threads = 6` limita correctamente la concurrencia

---

## Fase 6: Integracion y Script de Sync (dias 9-10)

### 6.1 Script Maestro: `scripts/sync_codex.sh`

Script que regenera toda la infraestructura Codex a partir de la fuente de verdad (`.claude/`):

```bash
#!/bin/bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
echo "=== Syncing Codex infrastructure from Claude Code ==="

# 1. Convertir agentes
echo "[1/3] Converting agents..."
python3 "$REPO_ROOT/scripts/convert_agents_to_codex.py"

# 2. Sincronizar skills
echo "[2/3] Syncing skills..."
bash "$REPO_ROOT/scripts/sync_codex_skills.sh"

# 3. Verificar estructura
echo "[3/3] Verifying structure..."
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
```

### 6.2 Actualizacion de AGENTS.md

Anadir seccion al final de AGENTS.md indicando soporte dual:

```markdown
## Dual-Tool Support

This repository supports both **Claude Code** (Anthropic) and **OpenAI Codex**.

| Tool | Config Dir | Agent Format | Skill Dir |
|------|-----------|-------------|-----------|
| Claude Code | `.claude/` | YAML frontmatter `.md` | `.claude/skills/` |
| OpenAI Codex | `.codex/` | TOML `.toml` | `.agents/skills/` (symlinks) |

**Source of truth:** `.claude/` directory. Run `scripts/sync_codex.sh` after modifying agents or skills to regenerate Codex infrastructure.

### Protected Files (applies to both tools)
Do NOT modify without explicit user approval:
- `.claude/settings.json` / `.codex/config.toml`
- `strategy-memo-*.md`, `referee-report-*.md`, `quality-score-*.json`
```

### 6.3 Actualizacion de .gitignore

No ignorar `.codex/` ni `.agents/` — deben ser versionados para que funcionen al clonar.

### 6.4 Estructura Final del Repo

```
clo-author/
├── AGENTS.md                    # Leido por AMBOS
├── CLAUDE.md                    # Claude Code (+ Codex via fallback)
├── MEMORY.md                    # Agnostico
│
├── .claude/                     # FUENTE DE VERDAD
│   ├── settings.json
│   ├── agents/                  # 20 agentes (.md)
│   ├── skills/                  # 11 skills (SKILL.md)
│   ├── rules/                   # Reglas narrativas (.md)
│   ├── hooks/                   # Scripts Python/Bash
│   ├── references/
│   └── WORKFLOW_QUICK_REF.md
│
├── .codex/                      # DERIVADO (generado por sync_codex.sh)
│   ├── config.toml              # Manual (no generado)
│   ├── agents/                  # 20 agentes (.toml) — generados
│   ├── rules/
│   │   └── safety.rules         # Manual (Starlark)
│   ├── hooks.json               # Manual
│   └── hooks/
│       ├── pre-bash-guard.py    # Manual
│       └── stop-context-save.py # Manual
│
├── .agents/                     # Skills compartidos (symlinks)
│   └── skills/ → .claude/skills/*/
│
├── scripts/
│   ├── convert_agents_to_codex.py  # Conversion automatica
│   ├── sync_codex_skills.sh        # Symlinks de skills
│   └── sync_codex.sh               # Script maestro
│
├── paper/                       # Agnostico
├── data/                        # Agnostico
├── quality_reports/             # Agnostico
├── templates/                   # Agnostico
└── ...
```

---

## Ficheros a Crear (resumen)

| # | Fichero | Tipo | Fase |
|---|---------|------|------|
| 1 | `.codex/config.toml` | Manual | 1 |
| 2 | `scripts/sync_codex_skills.sh` | Manual | 1 |
| 3 | `.agents/skills/*` (symlinks) | Generado | 1 |
| 4 | `scripts/convert_agents_to_codex.py` | Manual | 2 |
| 5 | `.codex/agents/*.toml` (x20) | Generado | 2 |
| 6 | `.codex/rules/safety.rules` | Manual | 3 |
| 7 | `.codex/hooks.json` | Manual | 4 |
| 8 | `.codex/hooks/pre-bash-guard.py` | Manual | 4 |
| 9 | `.codex/hooks/stop-context-save.py` | Manual | 4 |
| 10 | `scripts/sync_codex.sh` | Manual | 6 |

**Total ficheros manuales:** 8
**Total ficheros generados:** 20 agentes + 11 symlinks = 31

---

## Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|-------------|---------|------------|
| Hooks de Codex cambian de API | Alta | Medio | Mantener hooks simples; revisar changelog de Codex |
| PreToolUse no intercepta Write/Edit | Confirmado | Medio | Proteger via AGENTS.md + sandbox; esperar soporte |
| Divergencia .claude/ vs .codex/ | Media | Alto | Script `sync_codex.sh` como unica via de actualizacion |
| Coste de tokens con subagentes | Media | Bajo | Configurar `model_reasoning_effort` por agente |
| Skills con rutas hardcoded a .claude/ | Baja | Bajo | Los symlinks resuelven la ruta correcta |

---

## Criterio de Exito

- [ ] `codex` arranca en el repo y lee AGENTS.md + CLAUDE.md
- [ ] Todos los skills son accesibles via `$skill-name` en Codex
- [ ] `spawn_agent(agent="coder")` despacha el agente correcto con sandbox_mode="workspace-write"
- [ ] `spawn_agent(agent="coder-critic")` despacha con sandbox_mode="read-only"
- [ ] Hooks de SessionStart y PreToolUse funcionan
- [ ] `scripts/sync_codex.sh` regenera toda la infraestructura sin errores
- [ ] El workflow completo `/new-project` es ejecutable desde Codex
