# The Clo-Author: AI Research Architecture for Medical and Clinical Research

[![Version](https://img.shields.io/github/v/release/Mindbreaker81/clo-author?style=flat-square&color=b44dff&label=version)](CHANGELOG.md)

> **Work in progress.** This repo is evolving as the workflow is adapted to clinical and translational research.

An open-source research architecture that turns your terminal into a medical-research assistant — from literature review to journal submission. The default calibration in this fork is **pulmonary medicine / interventional pulmonology**, but the structure is reusable across clinical specialties.

**Live guide:** [Mindbreaker81.github.io/clo-author](https://Mindbreaker81.github.io/clo-author/)
**Forked from:** [hugosantanna/clo-author](https://github.com/hugosantanna/clo-author) · **Originally built on:** [Pedro Sant'Anna's claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)

---

## Quick Start

### With Claude Code (Anthropic)

```bash
gh repo clone Mindbreaker81/clo-author
cd clo-author
claude
```

### With OpenAI Codex

```bash
gh repo clone Mindbreaker81/clo-author
cd clo-author
codex
```

Then paste a prompt like:

> I am starting a new clinical research project in pulmonary medicine on **[YOUR TOPIC]**.
> Read `CLAUDE.md` and help me set up the project structure.
> Start with `/discover interview [YOUR TOPIC]`.

---

## Usage Guide

### 1. Set Up Your Project

Copy or fork the repo as the base for your project. This is a **template** — a directory structure + agents + skills that lives alongside your manuscript, not a package you install.

```bash
cp -r clo-author/ my-copd-study/
cd my-copd-study/
git init   # fresh git history for your project
```

### 2. Configure for Your Study

Edit **`CLAUDE.md`** (the first file Claude reads on every session):
- **Project:** name of your study
- **Institution:** your hospital / university
- **Field:** already set to Pulmonary Medicine / Interventional Pulmonology

Then review **`.claude/references/domain-profile.md`** — it already contains datasets, journals, outcomes, and conventions for pulmonary medicine. Adjust it if your subarea is different (e.g., thoracic oncology, critical care, ILD).

### 3. The Research Pipeline

The repo is designed as a sequential pipeline. Each slash command invokes a worker-critic pair:

```
/discover interview [clinical question]  →  Research specification
/discover lit [topic]                    →  PubMed / Cochrane search + annotated bibliography
/discover data [topic]                   →  Data source evaluation (registries, EHR, cohorts)
/strategize [question]                   →  Study design + analysis plan + registration strategy
/analyze [dataset]                       →  Analysis scripts (R by default)
/write [section]                         →  IMRAD manuscript sections
/review [file]                           →  Simulated peer review with 2 referees
/revise [report]                         →  Route referee comments + response planning
/talk [format]                           →  Presentation (Beamer or Quarto)
/submit [journal]                        →  Final gate: score >= 95
```

You do **not** have to run them in order. Enter at any point depending on your project stage.

### 4. Practical Examples

**Starting from scratch (new research question):**

```
/discover interview endobronchial valves for severe emphysema
```

**Already have data, want to write a paper:**

1. Fill in `CLAUDE.md` with your project metadata
2. `/discover lit [your topic]` — generates the bibliography
3. `/strategize [your question]` — produces a design memo with the reporting guideline
4. Write your R scripts in `scripts/R/`
5. `/write introduction` — drafts the intro based on the strategy memo
6. `/review paper/main.tex --peer AJRCCM` — peer review calibrated to the target journal

**Quick code review only:**

```
/review scripts/R/01_main_analysis.R --code
```

### 5. Compile the Manuscript

```bash
cd paper
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
BIBINPUTS=..:$BIBINPUTS biber main
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
```

### 6. Where Everything Goes

| What you produce | Where it lives |
|---|---|
| LaTeX manuscript | `paper/main.tex` + `paper/sections/` |
| Figures | `paper/figures/` |
| Tables | `paper/tables/` |
| R / Python scripts | `scripts/R/` or `scripts/python/` |
| Raw data | `data/raw/` (typically gitignored) |
| Cleaned data | `data/cleaned/` |
| Plans, reviews, session logs | `quality_reports/` |
| Bibliography | `Bibliography_base.bib` |
| Clinical guidelines, protocols | `master_supporting_docs/` |

### 7. Quality Gates

The system uses weighted scores. Nothing advances without passing the gate:

| Score | Gate | When |
|---|---|---|
| >= 80 | Commit | After any code or paper change |
| >= 90 | PR | Before merging |
| >= 95 | Submission | Before sending to a journal (all components >= 80) |

Scores are computed automatically by the critic agents when you run `/review`.

---

## What It Does

### Contractor Mode

You describe the task. Claude plans the work, dispatches specialist agents, runs reviews, fixes issues, and re-verifies outputs before handoff.

### Worker-Critic Pairs

Every creator has a paired critic.

| Phase | Worker | Critic |
|------|--------|--------|
| Discovery | Librarian | librarian-critic |
| Discovery | Explorer | explorer-critic |
| Design | Strategist | strategist-critic |
| Execution | Coder / Data-engineer | coder-critic |
| Manuscript | Writer | writer-critic |
| Peer review | Editor → domain-referee + methods-referee | — |
| Presentation | Storyteller | storyteller-critic |
| Infrastructure | Orchestrator, Verifier | — |

### Medical Peer Review Simulation

`/review --peer [journal]` simulates a real medical submission:

1. **Editor desk review** — fit, novelty, ethics / reporting completeness, and bar
2. **Referee assignment** — two different dispositions chosen from: Clinical, Methodological, Evidence, Ethical, Statistical, Translational, Skeptic
3. **Blind reports** — domain and methods referees review independently
4. **Editorial decision** — accept / minor / major / reject with MUST / SHOULD / MAY buckets

### Core Commands

- `/new-project`
- `/discover`
- `/strategize`
- `/analyze`
- `/write`
- `/review`
- `/revise`
- `/talk`
- `/submit`
- `/tools`

### Quality Gates

| Score | Gate | Applies To |
|------|------|------------|
| 80 | Commit | Weighted aggregate |
| 90 | PR | Weighted aggregate |
| 95 | Submission | Aggregate + all components >= 80 |
| -- | Advisory | Talks |

---

## Project Structure

```
your-project/
├── CLAUDE.md
├── AGENTS.md
├── .claude/                 # Claude Code infrastructure (source of truth)
├── .codex/                  # OpenAI Codex infrastructure (derived)
├── .agents/                 # Shared skills (symlinks to .claude/skills/)
├── Bibliography_base.bib
├── paper/
│   ├── main.tex
│   ├── sections/
│   ├── figures/
│   ├── tables/
│   ├── talks/
│   ├── quarto/
│   ├── preambles/
│   ├── supplementary/
│   └── replication/
├── data/
├── scripts/
├── quality_reports/
├── explorations/
└── master_supporting_docs/
```

---

## Medical-First Defaults

This fork defaults to:

- **Structured abstracts**
- **IMRAD manuscript structure**
- **CONSORT / STROBE / PRISMA / STARD-aware review flows**
- **IRB / consent / registration / adverse-event checks**
- **Clinical effect reporting** (HR / OR / RR / absolute risks / NNT when relevant)
- **PubMed / Cochrane / ClinicalTrials.gov discovery workflows**

---

## Built-In Validation Fixtures

This fork intentionally keeps minimal smoke-test sources in `paper/` so the local manuscript and presentation toolchain can be verified immediately:

- `paper/main.tex` + `paper/references.bib` — minimal manuscript fixture for `xelatex` + `biber`
- `paper/talks/full_talk.tex` — minimal Beamer talk fixture
- `paper/quarto/full_talk.qmd` — minimal Quarto RevealJS talk fixture

These files are **toolchain fixtures, not real project content**. Keep them as references or replace them once a real manuscript and talks exist.

---

## Prerequisites

| Tool | Required For |
|------|--------------|
| Claude Code or OpenAI Codex | Agent orchestration (at least one) |
| XeLaTeX + biber | Paper compilation |
| R / Python / Stata / Julia | Analysis |
| gh CLI | GitHub integration |
| Quarto (optional) | Guide site / web slides |

---

## Using with OpenAI Codex

This repo supports both Claude Code and OpenAI Codex. The `.claude/` directory is the **source of truth** — `.codex/` is derived from it.

- **Agents:** 18 agents are auto-converted from `.claude/agents/*.md` (YAML frontmatter) to `.codex/agents/*.toml` (TOML). Critics run in `read-only` sandbox; workers in `workspace-write`.
- **Skills:** `.agents/skills/` contains symlinks to `.claude/skills/*/` — same format (agentskills.io), shared by both tools.
- **Sync:** After modifying agents or skills in `.claude/`, run `scripts/sync_codex.sh` to regenerate the Codex infrastructure.

```bash
bash scripts/sync_codex.sh
```

See `AGENTS.md` for the full dual-tool support reference and protected files policy.

---

## Adapting the Fork

1. Update `CLAUDE.md` with your project details
2. Fill in `.claude/references/domain-profile.md`
3. Extend `.claude/references/journal-profiles.md` if you need more journals
4. Adjust `.claude/references/reporting-guidelines.md` if your field needs additional checklists (for example TRIPOD, CARE, ARRIVE)

---

## Origin

This project is a fork of [hugosantanna/clo-author](https://github.com/hugosantanna/clo-author), which itself builds on Pedro Sant'Anna's workflow-oriented Claude setup. The current fork reorients the architecture toward clinical and translational research with a pulmonary medicine default.

---

## License

MIT License.
