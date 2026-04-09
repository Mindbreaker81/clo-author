# Informe: Compatibilidad de clo-author con OpenAI Codex

**Fecha:** 2026-04-09
**Estado:** INVESTIGACION COMPLETADA
**Veredicto:** SI es posible, con esfuerzo moderado.

---

## 1. Resumen Ejecutivo

El repo `clo-author` esta disenado como un framework de investigacion medica orquestado por agentes IA. Actualmente depende de **Claude Code** (Anthropic) para su infraestructura de agentes, skills, hooks y reglas. Tras investigar la documentacion oficial de **OpenAI Codex** (App, CLI, IDE), la conclusion es que **se puede anadir soporte para Codex** de forma paralela, ya que ambos sistemas comparten conceptos casi identicos. El esfuerzo principal esta en traducir formatos de configuracion, no en reescribir logica.

---

## 2. Arquitectura Actual (Claude Code)

```
.claude/
├── settings.json          # Permisos + hooks (JSON)
├── agents/                # 18 agentes en Markdown con frontmatter YAML
│   ├── orchestrator.md    # name, description, tools, model
│   ├── coder.md
│   ├── writer.md
│   └── ...
├── skills/                # 11 skills como /write, /discover, /analyze
│   └── */SKILL.md         # Frontmatter YAML + instrucciones Markdown
├── rules/                 # Reglas de workflow en Markdown
│   ├── workflow.md
│   ├── agents.md
│   ├── quality.md
│   └── ...
├── hooks/                 # Scripts Python/Bash
│   ├── pre-compact.py
│   ├── post-compact-restore.py
│   ├── protect-files.sh
│   └── post-merge.sh
└── references/            # Perfiles de journals, dominio
```

Ficheros clave en la raiz:
- `CLAUDE.md` — Instrucciones del proyecto (leido automaticamente)
- `AGENTS.md` — Guia del repositorio (leido automaticamente)
- `MEMORY.md` — Aprendizajes persistentes entre sesiones

---

## 3. Arquitectura de OpenAI Codex

Segun la documentacion oficial (developers.openai.com/codex):

```
.codex/
├── config.toml            # Configuracion del proyecto (TOML)
├── agents/                # Agentes custom en TOML
│   └── *.toml             # name, description, developer_instructions
├── rules/                 # Reglas de ejecucion (Starlark .rules)
│   └── *.rules
└── hooks.json             # Hooks del ciclo de vida (JSON)

.agents/
└── skills/                # Skills (estandar agentskills.io)
    └── */SKILL.md         # Mismo formato: frontmatter YAML + Markdown
```

Ficheros raiz:
- `AGENTS.md` — Instrucciones del proyecto (leido automaticamente por Codex)

---

## 4. Tabla de Compatibilidad

| Componente | Claude Code | OpenAI Codex | Compatibilidad | Esfuerzo |
|-----------|-------------|--------------|----------------|----------|
| **AGENTS.md** | Leido automaticamente | Leido automaticamente | DIRECTA | Ninguno |
| **CLAUDE.md** | Leido como instrucciones | Codex usa `AGENTS.md` o `model_instructions_file` | Se puede anadir al fallback con `project_doc_fallback_filenames` | Minimo |
| **MEMORY.md** | Leido manualmente | Idem, referenciable desde AGENTS.md | DIRECTA | Ninguno |
| **Skills (SKILL.md)** | `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` | Formato IDENTICO (frontmatter YAML + MD). Solo cambia la ruta | Bajo: copiar o symlink |
| **Agentes** | `.claude/agents/*.md` (YAML frontmatter) | `.codex/agents/*.toml` (TOML nativo) | Requiere TRADUCCION de formato | Moderado |
| **Configuracion** | `.claude/settings.json` (JSON) | `.codex/config.toml` (TOML) | Requiere TRADUCCION | Moderado |
| **Reglas** | `.claude/rules/*.md` (Markdown narrativo) | `.codex/rules/*.rules` (Starlark) | INCOMPATIBLE como reglas de ejecucion. El contenido Markdown se mueve a AGENTS.md o developer_instructions | Moderado |
| **Hooks** | settings.json + scripts Python/Bash | hooks.json + scripts | Eventos similares pero no identicos | Moderado-Alto |
| **Permisos** | Patrones explícitos `Bash(git *)` | `sandbox_mode` + `approval_policy` + `.rules` | Modelo diferente; Codex usa sandbox | Moderado |
| **Subagentes** | Task dispatch via frontmatter `tools: Task` | `spawn_agent` nativo con config TOML | Concepto equivalente, API diferente | Moderado |
| **Paper/data/scripts/** | Agnostico de herramienta | Agnostico de herramienta | DIRECTA | Ninguno |

---

## 5. Lo Que Se Puede Reusar Directamente

### 5.1 AGENTS.md (compatibilidad 100%)
Codex lee `AGENTS.md` en la raiz del repo exactamente como Claude Code. El fichero actual ya funciona tal cual. Esta es la pieza mas importante.

### 5.2 Skills (compatibilidad ~90%)
Codex adopto el estandar `agentskills.io` para skills. El formato es el mismo: carpeta con `SKILL.md` que tiene frontmatter YAML (`name`, `description`) + instrucciones Markdown. La unica diferencia:
- Claude Code: `.claude/skills/*/SKILL.md`
- Codex: `.agents/skills/*/SKILL.md`

**Solucion:** Crear `.agents/skills/` con symlinks a `.claude/skills/*/`, o copiar. Opcionalmente usar un script de sync.

### 5.3 Contenido de agentes (compatibilidad ~70%)
Las instrucciones en `.claude/agents/*.md` (el cuerpo Markdown) son puro texto que funciona con cualquier LLM. Lo que cambia es el envoltorio:

**Claude Code (YAML frontmatter en .md):**
```yaml
---
name: coder
description: Implements the study design...
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
---
[instrucciones markdown]
```

**Codex (TOML en .toml):**
```toml
name = "coder"
description = "Implements the study design..."
model = "gpt-5.4"
sandbox_mode = "workspace-write"
developer_instructions = """
[instrucciones markdown]
"""
```

El contenido de instrucciones se reutiliza intacto. Solo cambia el formato del contenedor.

### 5.4 MEMORY.md, paper/, data/, scripts/, templates/
Todo esto es contenido agnostico de la herramienta. Funciona igual.

---

## 6. Lo Que Necesita Traduccion

### 6.1 Agentes: MD → TOML
**18 ficheros** de agente necesitan conversion. Script automatizable:

```python
# Pseudocodigo de conversion
# Leer frontmatter YAML de .claude/agents/coder.md
# Extraer name, description, tools, model
# Generar .codex/agents/coder.toml con:
#   name = "coder"
#   description = "..."
#   developer_instructions = """..."""
#   sandbox_mode = inferir de tools (Read-only vs Read+Write)
```

**Mapeo de campos:**

| Claude Code (YAML) | Codex (TOML) |
|---------------------|--------------|
| `name` | `name` |
| `description` | `description` |
| `tools` | `sandbox_mode` (read-only vs workspace-write) |
| `model: inherit` | Omitir (hereda del padre) |
| Cuerpo markdown | `developer_instructions` |

**Nota:** Codex no tiene un campo `tools` equivalente; el acceso a herramientas se controla via `sandbox_mode` y `skills.config`.

### 6.2 Configuracion: settings.json → config.toml

**Claude Code (.claude/settings.json):**
```json
{
  "permissions": { "allow": ["Bash(git *)"] },
  "hooks": { "PreToolUse": [...] }
}
```

**Codex (.codex/config.toml):**
```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[features]
multi_agent = true
codex_hooks = true

[agents]
max_threads = 6
max_depth = 1
```

### 6.3 Reglas: Markdown → Starlark + AGENTS.md

Las reglas de Claude Code (`.claude/rules/*.md`) son instrucciones narrativas en Markdown que guian el comportamiento del agente. En Codex, este contenido tiene dos destinos:

1. **Guia de comportamiento** → Se incorpora al `AGENTS.md` o a `developer_instructions` de los agentes
2. **Reglas de ejecucion** → Se traducen a `.codex/rules/*.rules` en formato Starlark solo si controlan permisos de comandos

Ejemplo Starlark:
```python
prefix_rule(
    pattern = ["rm", "-rf"],
    decision = "forbidden",
    justification = "Destructive deletion blocked"
)
```

### 6.4 Hooks: settings.json → hooks.json

| Evento Claude Code | Evento Codex Equivalente | Notas |
|--------------------|--------------------------|-------|
| `PreToolUse` (Edit\|Write) | `PreToolUse` (Bash) | Codex solo intercepta Bash por ahora; protect-files requiere adaptacion |
| `PreCompact` | `Stop` | No hay equivalente directo; se puede usar Stop hook para guardar contexto |
| `SessionStart` (compact\|resume) | `SessionStart` (startup\|resume) | Casi identico |
| (no existe) | `PostToolUse` | Disponible en Codex, no usado actualmente |
| (no existe) | `UserPromptSubmit` | Disponible en Codex, no usado actualmente |

**Nota critica:** Los hooks de Codex estan marcados como **experimentales** y actualmente solo interceptan `Bash`. El hook `protect-files.sh` (que protege CLAUDE.md y settings.json de ediciones) no tiene equivalente directo en Codex porque `PreToolUse` no intercepta `Write` o `Edit` todavia.

---

## 7. Diferencias Conceptuales Importantes

### 7.1 Modelo de Subagentes
- **Claude Code:** Los agentes se invocan via `Task` tool con instrucciones in-band. El orchestrator despacha manualmente.
- **Codex:** Tiene `spawn_agent`, `send_input`, `wait_agent`, `close_agent` nativos. Soporta `spawn_agents_on_csv` para batch. Mas sofisticado pero diferente API.

### 7.2 Modelo de Permisos
- **Claude Code:** Whitelist explicita de patrones `Bash(comando *)` en settings.json
- **Codex:** Tres niveles de sandbox (`read-only`, `workspace-write`, `danger-full-access`) + reglas Starlark para control granular + `approval_policy`

### 7.3 Worker-Critic Pairs
- Ambos soportan el concepto, pero la orquestacion la hace el AGENTS.md / developer_instructions, no la plataforma.
- En Codex, puedes asignar diferentes modelos y sandbox a cada agente (ej: critics en `read-only`, workers en `workspace-write`), lo cual es una MEJORA sobre el sistema actual.

---

## 8. Plan de Implementacion Propuesto

### Fase 1: Compatibilidad basica (esfuerzo: 1-2 dias)
1. Crear `.codex/config.toml` con configuracion base
2. Configurar `project_doc_fallback_filenames = ["CLAUDE.md"]` para que Codex lea el CLAUDE.md existente
3. Crear `.agents/skills/` con symlinks a `.claude/skills/*/`
4. Verificar que Codex lee AGENTS.md correctamente

### Fase 2: Traduccion de agentes (esfuerzo: 1-2 dias)
1. Escribir script `scripts/convert_agents_to_codex.py` que convierta los 18 agentes de `.claude/agents/*.md` → `.codex/agents/*.toml`
2. Adaptar `developer_instructions` para referenciar convenciones Codex
3. Asignar `sandbox_mode` apropiado a cada agente (critics → read-only, workers → workspace-write)
4. Configurar `model` y `model_reasoning_effort` por agente

### Fase 3: Hooks y reglas (esfuerzo: 2-3 dias)
1. Crear `.codex/hooks.json` con SessionStart hook para post-compact-restore
2. Adaptar protect-files a un PreToolUse hook (limitado a Bash por ahora)
3. Mover contenido de `.claude/rules/*.md` a secciones del AGENTS.md o developer_instructions
4. Crear reglas Starlark basicas en `.codex/rules/`

### Fase 4: Subagentes avanzados (esfuerzo: 2-3 dias)
1. Adaptar el orchestrator para usar `spawn_agent` nativo de Codex
2. Configurar `agents.max_threads` y `agents.max_depth` para el pipeline
3. Aprovechar la asignacion de modelo por agente de Codex (sparks para exploracion, gpt-5.4 para analisis)

### Esfuerzo total estimado: 6-10 dias

---

## 9. Estructura Propuesta del Repo Dual

```
clo-author/
├── AGENTS.md               # Leido por AMBOS (fuente de verdad compartida)
├── CLAUDE.md                # Leido por Claude Code (+ Codex via fallback)
├── MEMORY.md                # Agnostico
├── .claude/                 # Infraestructura Claude Code (existente)
│   ├── settings.json
│   ├── agents/*.md
│   ├── skills/*/SKILL.md
│   ├── rules/*.md
│   └── hooks/
├── .codex/                  # Infraestructura Codex (NUEVO)
│   ├── config.toml
│   ├── agents/*.toml
│   ├── rules/*.rules
│   └── hooks.json
├── .agents/                 # Skills compartidos (NUEVO, estandar agentskills.io)
│   └── skills/              # Symlinks o copias de .claude/skills/
├── paper/                   # Agnostico
├── data/                    # Agnostico
├── scripts/                 # Agnostico
│   └── convert_agents_to_codex.py  # Script de conversion
└── ...
```

---

## 10. Ventajas de Soportar Ambos

1. **Resiliencia:** No depender de un solo proveedor de IA
2. **Flexibilidad de modelo:** Codex permite asignar modelos diferentes por agente (gpt-5.4 para criticos, gpt-5.3-codex-spark para workers rapidos)
3. **Batch processing:** `spawn_agents_on_csv` de Codex es ideal para revisiones sistematicas
4. **IDE integration:** Codex tiene extension de VS Code con soporte nativo de skills
5. **GitHub Action:** Codex tiene accion de GitHub para automatizacion CI/CD

## 11. Riesgos y Limitaciones

1. **Hooks experimentales:** Los hooks de Codex estan en desarrollo activo; `PreToolUse` solo intercepta Bash
2. **Divergencia de features:** Mantener dos configuraciones en sync requiere disciplina
3. **Coste de tokens:** Los subagentes de Codex consumen mas tokens que single-agent
4. **SKILL.md location:** Codex busca en `.agents/skills/`, no en `.claude/skills/` — requiere duplicacion o symlinks
5. **Rules incompatibles:** Las reglas Markdown de Claude Code no se traducen 1:1 a Starlark

---

## 12. Conclusion

**SI se puede.** La buena noticia es que el componente mas importante — `AGENTS.md` — funciona identico en ambos sistemas. Las skills comparten formato. El contenido de los agentes (instrucciones en Markdown) se reutiliza intacto. Lo que cambia es el empaquetado (YAML frontmatter vs TOML) y algunos mecanismos de plataforma (hooks, permisos, subagentes).

El esfuerzo estimado de 6-10 dias de trabajo produce un repo que funciona con ambas herramientas, dando flexibilidad de proveedor y acceso a las ventajas unicas de cada plataforma.
