# Repository Guidelines

## Project Structure & Module Organization

```
clo-author/
├── CLAUDE.md                  # Project config (fill in bracketed placeholders)
├── Bibliography_base.bib      # Centralized BibTeX bibliography
├── paper/                     # LaTeX manuscript (single source of truth)
│   ├── main.tex               # Primary paper file
│   ├── sections/              # Section-level .tex includes
│   ├── figures/               # Generated figures (.pdf, .png)
│   ├── tables/                # Generated tables (.tex)
│   ├── talks/                 # Beamer presentations
│   ├── quarto/                # Quarto RevealJS slides
│   ├── preambles/             # Shared LaTeX headers
│   ├── supplementary/         # Online appendix
│   └── replication/           # Replication package for deposit
├── data/raw/                  # Original untouched data (often gitignored)
├── data/cleaned/              # Processed datasets
├── scripts/                   # Analysis code (R, Stata, Python, Julia)
├── quality_reports/           # Plans, session logs, reviews, scores
│   ├── plans/                 # Saved plans from plan-first workflow
│   └── specs/                 # Requirements specs (YYYY-MM-DD_description.md)
├── explorations/              # Research sandbox
├── templates/                 # Session log, quality report, spec templates
├── master_supporting_docs/    # Reference papers and data documentation
└── .claude/                   # Claude Code infrastructure
    ├── agents/                # Worker-critic agent definitions
    ├── skills/                # Slash command implementations
    ├── rules/                 # Governance, quality, workflow rules
    ├── references/            # Journal profiles, domain profile
    └── hooks/                 # Pre-compact, protect-files, post-compact
```

## Build & Compilation Commands

Paper compilation requires XeLaTeX with a 3-pass build:

```bash
cd paper && TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
BIBINPUTS=..:$BIBINPUTS bibtex main
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
```

Talk compilation:

```bash
cd paper/talks && TEXINPUTS=../preambles:$TEXINPUTS xelatex -interaction=nonstopmode talk.tex
```

Quality scoring (Python):

```bash
python3 scripts/quality_score.py
```

## Coding Style & Naming Conventions

- **Output organization:** `by-script` (default). Figures go to `paper/figures/<script_name>/`, tables to `paper/tables/<script_name>/`.
- **Specs:** `quality_reports/specs/YYYY-MM-DD_description.md`.
- **LaTeX:** XeLaTeX only. Preambles live in `paper/preambles/`. Use `biblatex` for bibliography management.
- **Scripts:** R is the default language; Stata, Python, and Julia also supported.
- **No sensitive data** in committed files. Raw data directories are typically gitignored.

## Quality Gates & Testing

This project uses a weighted aggregate scoring system (0-100) enforced by worker-critic agent pairs. Every creator artifact must be reviewed by its paired critic before advancing.

| Gate       | Minimum Score | Requirement                        |
|------------|---------------|------------------------------------|
| Commit     | >= 80         | Weighted aggregate                 |
| PR         | >= 90         | Weighted aggregate                 |
| Submission | >= 95         | Aggregate + all components >= 80   |
| Talks      | Advisory      | Reported but non-blocking          |

Weighted components: Literature (10%), Data quality (10%), Study design validity (25%), Code quality (15%), Paper quality (25%), Manuscript polish (10%), Replication readiness (5%).

## Commit & Pull Request Guidelines

Commit messages follow a concise descriptive style. Examples from history:

```
Update working paper format: biblatex + polished preamble
Release v3.1.1: Output organization + path fixes + plan mode
Fix stale uppercase paths across agents, skills, and rules
```

- Use imperative mood or descriptive present tense.
- Prefix with `Fix`, `Add`, `Update`, `Release`, `Remove` as appropriate.
- Release commits include version and a brief summary of changes.
- PRs must pass the >= 90 quality gate before merge.

## Agent Architecture

The system uses adversarial worker-critic pairs. Critics review but never edit files; creators produce artifacts but never self-score. Max 3 rounds per pair before escalation (to a senior agent or the user).

| Worker          | Critic              | Domain                        |
|-----------------|---------------------|-------------------------------|
| librarian       | librarian-critic    | Literature coverage           |
| explorer        | explorer-critic     | Data feasibility              |
| strategist      | strategist-critic   | Study design strategy         |
| coder           | coder-critic        | Script quality                |
| data-engineer   | coder-critic        | Data pipeline                 |
| writer          | writer-critic       | Manuscript polish             |
| storyteller     | storyteller-critic  | Presentations                 |

Peer review uses `editor`, `domain-referee`, and `methods-referee` agents.

## Core Workflow Principles

1. **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`.
2. **Verify after** -- compile and confirm output at the end of every task.
3. **Single source of truth** -- `paper/main.tex` is authoritative; talks and supplements derive from it.
4. **Spec-then-plan** -- for complex tasks (>1 hour or >3 files), run requirements spec before planning.
5. **Memory persistence** -- corrections go in `MEMORY.md` as `[LEARN:category]` entries.
