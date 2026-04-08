---
name: systematic-review
description: Design and draft a systematic review or meta-analysis workflow, including search strategy, screening plan, extraction grid, and PRISMA-aligned outputs.
argument-hint: "[topic or question]"
allowed-tools: Read,Grep,Glob,Write,Task,WebSearch,WebFetch
---

# Systematic Review

Build a systematic-review or meta-analysis workflow.

## Workflow

1. Define the review question and eligibility criteria
2. Build a search strategy using keywords + MeSH
3. List target sources (PubMed / MEDLINE, Cochrane, Embase if available, trial registries)
4. Create screening rules for title / abstract and full text
5. Create a data-extraction grid
6. Specify bias assessment and synthesis plan
7. Draft PRISMA-aligned outputs

## Outputs

Save to `quality_reports/systematic_review_[topic]/`:
- `protocol.md`
- `search_strategy.md`
- `screening_form.md`
- `data_extraction_template.md`
- `risk_of_bias_plan.md`
- `prisma_flow_template.md`

## Principles

- Search logic must be reproducible
- Eligibility criteria must be explicit
- Narrative synthesis is acceptable when meta-analysis is not justified
- If meta-analysis is planned, define effect measure and heterogeneity strategy up front
