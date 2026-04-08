---
name: write
description: Draft medical manuscript sections with IMRAD defaults, structured abstracts, and humanizer pass.
argument-hint: "[section or mode: intro | methods | strategy | results | discussion | conclusion | abstract | full | humanize] [file path (optional)]"
allowed-tools: Read,Grep,Glob,Write,Edit,Task
---

# Write

Draft paper sections or apply the humanizer pass by dispatching the **Writer** agent.

## Modes

### `/write [section]`
Draft `intro`, `methods`, `strategy` (alias for methods / analysis framing), `results`, `discussion`, `conclusion`, `abstract`, or `full`.

Workflow:
1. Read existing manuscript files, supporting docs, strategy outputs, domain profile, and generated tables / figures
2. Dispatch Writer with IMRAD and reporting-guideline context
3. Save to `paper/sections/[section].tex`
4. Run a self-check before presenting

### `/write humanize [file]`
Strip AI writing patterns from existing prose without changing substance.

## Quality Self-Check

Before presenting the draft:
- relevant reporting guideline reflected?
- structured abstract used when drafting an abstract?
- primary outcomes and analysis populations described consistently?
- effect estimates reported with 95% CI and clinical context?
- harms / safety language present when relevant?
- no overstated causal claims?
- all cited tables / figures actually exist?

## Section Standards

| Section | Length | Key Requirements |
|---------|--------|-----------------|
| Introduction | 800-1400 words | clinical problem, gap, contribution, main takeaway |
| Methods / Strategy | 900-1400 words | design, participants, outcomes, analysis, ethics |
| Results | 800-1500 words | flow, baseline table, primary analysis, harms, sensitivity |
| Discussion | 700-1200 words | interpretation, comparison with evidence, limits, implications |
| Conclusion | 300-600 words | concise take-home and next step |
| Abstract | 150-300 words | Background / Methods / Results / Conclusions |

## Principles

- Never fabricate results
- Use TBD placeholders when estimates are missing
- Make clinical meaning explicit, not just statistical significance
- Keep the paper consistent with the strategy memo and outputs
