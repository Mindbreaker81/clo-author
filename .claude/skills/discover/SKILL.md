---
name: discover
description: Discovery phase combining clinical research interviews, literature search, data discovery, and ideation. Routes to appropriate agents based on arguments.
argument-hint: "[mode: interview | lit | data | ideate] [topic or query]"
allowed-tools: Read,Grep,Glob,Write,Edit,WebSearch,WebFetch,Task
---

# Discover

Launch the discovery phase of a medical research project.

## Modes

### Default or `/discover interview [topic]`
Conduct a structured interview to formalize the clinical research question.

Interview structure:
1. Clinical problem and why it matters
2. Population, intervention / exposure, comparator, outcomes
3. Available data and setting
4. Feasible study designs
5. Expected results and what would be clinically meaningful
6. Contribution relative to current evidence or guidelines

Output:
- research specification in `quality_reports/research_spec_[topic].md`
- update `.claude/references/domain-profile.md` if it is still template-like

### `/discover lit [topic]`
Search and synthesize the evidence base.

**Agents:** librarian → librarian-critic

Workflow:
1. Read `.claude/references/domain-profile.md`
2. Check `master_supporting_docs/` and `Bibliography_base.bib`
3. Search PubMed / MEDLINE using keywords + MeSH
4. Search Cochrane and recent guidelines if relevant
5. Search ClinicalTrials.gov for ongoing / unpublished / recent trials when relevant
6. Follow forward and backward citation chains
7. Assign proximity scores:
   - 1 direct competitor
   - 2 closely related
   - 3 related disease / design / population
   - 4 methods or background support
   - 5 tangential context
8. Dispatch librarian-critic for gaps, evidence hierarchy, and recency

### `/discover data [requirements]`
Find and assess datasets for the question.

**Agents:** explorer → explorer-critic

Workflow:
1. Read the research spec and domain profile
2. Identify variables needed: population, exposure / intervention, outcomes, follow-up, covariates
3. Search EHR / registry options, public surveys, registries, and specialty cohorts
4. Grade feasibility:
   - A ready to use
   - B accessible with moderate effort
   - C restricted but realistic
   - D very difficult
5. Critique each dataset for measurement validity, selection, external validity, design compatibility, and known issues

### `/discover ideate [topic]`
Generate 3-5 research questions with design ideas, outcome definitions, data requirements, and novelty ranking.

## Principles

- Never fabricate citations
- Always distinguish high-certainty evidence from exploratory evidence
- Use MeSH terms when appropriate
- Coverage must include guidelines and evidence syntheses when they exist
- Worker-critic pairing is mandatory for literature and data discovery
