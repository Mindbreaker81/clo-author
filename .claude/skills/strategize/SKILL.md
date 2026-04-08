---
name: strategize
description: Design a medical study or draft a protocol / registration plan. Dispatches Strategist and strategist-critic.
argument-hint: "[mode: strategy | pap | pap interactive] [research question or spec path]"
allowed-tools: Read,Grep,Glob,Write,Task
---

# Strategize

Design the study plan by dispatching the **Strategist** and **strategist-critic**.

## Modes

### `/strategize [question]` or `/strategize strategy [question]`
Build the primary study design.

**Agents:** strategist → strategist-critic

Output:
- strategy memo
- analysis plan
- robustness / sensitivity plan
- bias register

Workflow:
1. Read research spec, literature review, and data assessment if they exist
2. Read `.claude/references/domain-profile.md`
3. Dispatch Strategist to propose and rank candidate designs
4. Dispatch strategist-critic to audit design fit, bias control, inference, and reporting / ethics
5. Iterate if critical issues remain
6. Save outputs to `quality_reports/strategy_memo_[topic].md` and companion files

### `/strategize pap [spec]`
Draft a registration-ready protocol or pre-analysis plan.

**Input:** path to a research spec, a topic, or `interactive`

#### Interactive protocol flow

Ask these questions one at a time when invoked as `/strategize pap interactive`:
1. What is the research question?
2. What is the study design?
3. What is the primary outcome?
4. What is the exposure / intervention and comparator?
5. What analyses and subgroups are pre-specified?
6. What ethics, consent, safety, and registration path applies?

#### Registry / protocol targets

- **ClinicalTrials.gov** — common default for interventional studies
- **ISRCTN** — alternative trial registry
- **EudraCT / CTIS** — EU interventional studies
- **WHO ICTRP** — cross-registry discovery / international visibility
- **PROSPERO** — systematic review protocols
- **OSF** — observational or flexible protocol hosting

#### PAP / protocol sections

1. Study overview
2. Design and setting
3. Population and eligibility
4. Primary / secondary outcomes
5. Analysis populations (ITT / per-protocol / safety if relevant)
6. Statistical analysis plan
7. Missing data and sensitivity analyses
8. Sample-size or precision logic
9. Ethics / consent / safety oversight
10. Registration details and deviations log

## Principles

- Choose the design the question and data can actually support
- Distinguish exploratory analyses from pre-specified analyses
- Registration logic is design-specific: not every study belongs in the same registry
- Protocols should name the reporting guideline they will target
