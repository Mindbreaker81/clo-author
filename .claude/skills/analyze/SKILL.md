---
name: analyze
description: End-to-end medical data analysis dispatching Coder and Data-engineer for implementation and coder-critic for review.
argument-hint: "[dataset path or goal] Options: --dual [lang1,lang2]"
allowed-tools: Read,Grep,Glob,Write,Edit,Bash,Task
---

# Analyze

Run end-to-end analysis by dispatching the **Coder**, **Data-engineer**, and **coder-critic**.

## Workflow

### Step 1: Context Gathering
1. Read `.claude/references/domain-profile.md`
2. Read the strategy memo if it exists
3. Check existing scripts for project patterns

### Step 2: Data Preparation
If raw or semi-processed data are provided, dispatch Data-engineer first:
- clean data and document cohort construction
- define outcomes, exposures, covariates, and time windows
- generate a baseline table and descriptive figures
- save cleaned data and codebook

### Step 3: Main Analysis
Dispatch Coder:
- main specification from the strategy memo
- harms / safety analysis when relevant
- planned sensitivity analyses
- publication-ready tables and figures
- `results_summary.md` with key estimates and interpretation notes

Preferred packages depend on the problem:
- `survival`, `survminer` for time-to-event analyses
- `gtsummary`, `gt`, `tableone` for clinical tables
- `meta`, `metafor`, `forestplot` for evidence synthesis
- `fixest`, `glm`, `lme4`, or equivalents when appropriate to the design

### Step 4: Code Review
Dispatch coder-critic for the 12-category review.

Key sanity questions:
- do event counts and follow-up make sense?
- do estimates and harms move in a clinically plausible direction?
- is the analysis population consistent with the protocol?
- are the right outputs generated (Table 1, primary effect table, harms, survival / diagnostic visuals as needed)?

### Step 5: Present Results
Report:
- main estimates with uncertainty
- scripts created
- tables / figures generated
- coder-critic score
- missing-data or sensitivity TODOs
