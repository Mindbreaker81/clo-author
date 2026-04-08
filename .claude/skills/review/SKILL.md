---
name: review
description: Quality reviews for medical manuscripts, code, reporting, and peer-review simulation.
argument-hint: "[file path or --flag] Options: --peer [journal], --stress [journal], --methods, --proofread, --code, --reporting [guideline], --all"
allowed-tools: Read,Grep,Glob,Write,Bash,Task
---

# Review

Unified review command that routes to the appropriate critics based on target and flags.

## Routing Logic

### Auto-detect by file type
- `.tex` paper file → writer-critic + strategist-critic + verifier
- `.R`, `.py`, `.do`, `.jl` → coder-critic
- talk file → storyteller-critic

### Explicit flags
- `--peer [journal]` → editor → domain-referee + methods-referee → editor decision
- `--peer --r2 [journal]` → revision round with memory of prior concerns
- `--stress [journal]` → hostile peer review
- `--methods` → strategist-critic standalone study-design audit
- `--proofread` → writer-critic standalone
- `--code` → coder-critic standalone
- `--reporting [guideline]` → focused reporting-guideline audit (`consort`, `strobe`, `prisma`, `stard`, `tripod`)
- `--all` → all relevant critics in parallel + weighted score

## Full Peer Review (`--peer [journal]`)

### Phase 1: Editor Desk Review
The editor reads the paper, checks novelty claims, and decides: desk reject or send to referees.

### Phase 2: Referee Reports
The editor assigns each referee:
- one disposition from: CLINICAL, METHODOLOGICAL, EVIDENCE, ETHICAL, STATISTICAL, TRANSLATIONAL, SKEPTIC
- one critical pet peeve
- one constructive pet peeve

Dispatch domain-referee and methods-referee in parallel. Every major comment must include **what would change my mind**.

### Phase 3: Editorial Decision
The editor classifies concerns as FATAL / ADDRESSABLE / TASTE and issues the final decision.

### Save Reports
Save to `quality_reports/reviews/`.

## Reporting Audit (`--reporting [guideline]`)

Focused checklist audit using `.claude/references/reporting-guidelines.md`.

- `consort` → randomized trials
- `strobe` → observational studies
- `prisma` → systematic reviews / meta-analyses
- `stard` → diagnostic accuracy studies
- `tripod` → prediction models

If the guideline is omitted, infer the best match from the manuscript and state the inference explicitly.

## Principles

- Peer review is adversarial, but not theatrical
- Reporting reviews are separate from design reviews, though they often overlap
- A paper can be statistically correct and still fail on ethics / reporting / clinical relevance
