# The Clo-Author: AI Research Architecture for Medical and Clinical Research

[![Version](https://img.shields.io/github/v/release/hugosantanna/clo-author?style=flat-square&color=b44dff&label=version)](CHANGELOG.md)

> **Work in progress.** This repo is evolving as the workflow is adapted to clinical and translational research.

An open-source research architecture that turns your terminal into a medical-research assistant — from literature review to journal submission. The default calibration in this fork is **pulmonary medicine / interventional pulmonology**, but the structure is reusable across clinical specialties.

**Live guide:** [hugosantanna.github.io/clo-author](https://hugosantanna.github.io/clo-author/)
**Built on:** [Pedro Sant'Anna's claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)

---

## Quick Start

```bash
gh repo fork hugosantanna/clo-author --clone
cd clo-author
claude
```

Then paste a prompt like:

> I am starting a new clinical research project in pulmonary medicine on **[YOUR TOPIC]**.
> Read `CLAUDE.md` and help me set up the project structure.
> Start with `/discover interview [YOUR TOPIC]`.

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
├── .claude/
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
| Claude Code | Everything |
| XeLaTeX + biber | Paper compilation |
| R / Python / Stata / Julia | Analysis |
| gh CLI | GitHub integration |
| Quarto (optional) | Guide site / web slides |

---

## Adapting the Fork

1. Update `CLAUDE.md` with your project details
2. Fill in `.claude/references/domain-profile.md`
3. Extend `.claude/references/journal-profiles.md` if you need more journals
4. Adjust `.claude/references/reporting-guidelines.md` if your field needs additional checklists (for example TRIPOD, CARE, ARRIVE)

---

## Origin

This project builds on Pedro Sant'Anna's workflow-oriented Claude setup, but the current fork reorients it toward clinical and translational research with a pulmonary medicine default.

---

## License

MIT License.
