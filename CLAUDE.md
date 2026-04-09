<coding_guidelines>
# CLAUDE.MD -- Medical Research with Claude Code

**Project:** Pulmonary Outcomes Research Project
**Institution:** Academic Medical Center / University Hospital
**Field:** Pulmonary Medicine / Interventional Pulmonology
**Branch:** main

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- compile or validate outputs at the end of every task
- **Single source of truth** -- `paper/main.tex` is authoritative; talks and supplements derive from it
- **Quality gates** -- weighted aggregate score; nothing ships below 80/100; see `quality.md`
- **Worker-critic pairs** -- every creator has a paired critic; critics never edit files
- **Reporting first** -- match the study design to the right reporting guideline (CONSORT, STROBE, PRISMA, STARD)
- **Clinical compliance** -- ethics approval, consent, registration, safety reporting, and conflicts disclosure are never optional when applicable

---

## Getting Started

1. Replace the generic project metadata above if you want project-specific values
2. Run `/discover interview [clinical topic]` to build the research specification
3. Or run `/new-project [clinical topic]` for the full orchestrated pipeline

---

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.md                    # This file
├── .claude/                     # Claude Code infrastructure (source of truth)
├── .codex/                      # OpenAI Codex infrastructure (derived)
├── .agents/                     # Shared skills (symlinks to .claude/skills/)
├── Bibliography_base.bib        # Centralized bibliography
├── paper/                       # Main LaTeX manuscript (source of truth)
│   ├── main.tex                 # Primary paper file
│   ├── sections/                # Section-level .tex files
│   ├── figures/                 # Generated figures (.pdf, .png)
│   ├── tables/                  # Generated tables (.tex)
│   ├── talks/                   # Beamer presentations
│   ├── quarto/                  # Quarto RevealJS presentations
│   ├── preambles/               # Shared LaTeX headers
│   ├── supplementary/           # Online appendix
│   └── replication/             # Submission / data-sharing package
├── data/                        # Project data
│   ├── raw/                     # Original untouched data (often gitignored)
│   └── cleaned/                 # Processed datasets ready for analysis
├── scripts/                     # Analysis code (R, Stata, Python, Julia)
├── quality_reports/             # Plans, session logs, reviews, scores
├── explorations/                # Research sandbox
├── templates/                   # Session log, quality report, spec templates
└── master_supporting_docs/      # Clinical guidelines, protocols, reference docs
```

---

## Commands

```bash
# Paper compilation (3-pass, XeLaTeX + biber)
cd paper && TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
BIBINPUTS=..:$BIBINPUTS biber main
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex

# Talk compilation
cd paper/talks && TEXINPUTS=../preambles:$TEXINPUTS xelatex -interaction=nonstopmode full_talk.tex

# Quality scoring (if applicable to the target artifact)
python3 scripts/quality_score.py <artifact>
```

---

## Quality Thresholds

| Score | Gate | Applies To |
|-------|------|------------|
| 80 | Commit | Weighted aggregate (blocking) |
| 90 | PR | Weighted aggregate (blocking) |
| 95 | Submission | Aggregate + all components >= 80 |
| -- | Advisory | Talks (reported, non-blocking) |

See `quality.md` for weighted aggregation and medical checks.

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/new-project [topic]` | Full pipeline: question → manuscript |
| `/discover [mode] [topic]` | Discovery: interview, literature, data, ideation |
| `/strategize [question]` | Study design, protocol, or registration plan |
| `/analyze [dataset]` | End-to-end clinical or observational analysis |
| `/write [section]` | Draft manuscript sections + humanizer pass |
| `/review [file/--flag]` | Quality reviews (paper, code, peer, reporting) |
| `/revise [report]` | Route referee comments and revision cycle |
| `/talk [mode] [format]` | Create, audit, or compile slides |
| `/submit [mode]` | Journal targeting → package → audit → final gate |
| `/tools [subcommand]` | Utilities: commit, compile, validate-bib, journal, etc. |

---

## Presentation Formats

| Format | Effect | Use Case |
|--------|--------|----------|
| `full-length` | Full narrative | Grand rounds, plenary, invited seminar |
| `seminar` | Standard research talk | Department or journal club |
| `short` | Condensed story | Conference oral presentation |
| `lightning` | One-result pitch | Fast talk / poster spotlight |

---

## Output Organization

Output organization: by-script

---

## Current Project State

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Manuscript | `paper/main.tex` | smoke-test fixture | Minimal IMRAD manuscript kept to validate XeLaTeX + biber |
| Data | `scripts/R/` | planned | Clinical / registry / EHR analysis |
| Replication | `paper/replication/` | not started | Submission package + reporting checklist |
| Protocol | `quality_reports/strategy_memo_[topic].md` | planned | Study design, analysis plan, safety/ethics notes |
| Talk | `paper/talks/full_talk.tex` | smoke-test fixture | Minimal Beamer deck kept to validate talk compilation |
| Quarto Talk | `paper/quarto/full_talk.qmd` | smoke-test fixture | Minimal RevealJS deck kept to validate Quarto rendering |
| Codex Support | `.codex/`, `.agents/` | implemented | Dual-tool infrastructure; run `scripts/sync_codex.sh` after agent changes |
</coding_guidelines>
