# Requirements Specification: Audit of Commit `9f8a6f7`

**Date:** 2026-04-08
**Status:** APPROVED

---

## Objective

Audit commit `9f8a6f7` (`Refactor clo-author for pulmonary medicine workflows`) against `PLAN _REFACTOR.md` and `quality_reports/session_logs/2026-04-08_medical-refactor-audit-handoff.md`.

Success means determining whether the medical refactor is:

1. aligned with the approved refactor plan plus agreed critical gaps,
2. internally consistent across runtime files,
3. free of high-confidence leftover economics defaults in active medical paths,
4. accurately represented by the handoff document,
5. a safe baseline for future work.

---

## Required Inputs

The auditor must use these artifacts as the source of truth:

- `PLAN _REFACTOR.md`
- `quality_reports/session_logs/2026-04-08_medical-refactor-audit-handoff.md`
- commit `9f8a6f7`

The scope of the audit is **the content introduced by commit `9f8a6f7`**. If the repository has moved on, the auditor should still anchor conclusions to that commit.

---

## Scope

### In Scope

- `.claude/**` runtime files changed by commit `9f8a6f7`
- `CLAUDE.md`
- `README.md`
- `guide/*.qmd`
- smoke-test fixtures in `paper/`
- consistency between the commit and the handoff document

### Explicit Audit Targets

1. replacement of economics/social-science defaults with medical-first defaults,
2. consistency of the new reviewer taxonomy,
3. quality-rule and formatting-rule rewrites,
4. fixture strategy and documentation,
5. known limitation around `.claude/references/journal-profiles.html`,
6. runtime support files: `.claude/settings.json`, `.claude/WORKFLOW_QUICK_REF.md`, `.claude/rules/meta-governance.md`,
7. new files introduced by the commit: `.claude/references/reporting-guidelines.md`, `.claude/skills/systematic-review/SKILL.md`.

> The targets above are areas of maximum priority. The auditor should also perform a sweep of the full diff to detect unanticipated inconsistencies across all 45 changed files.

### Out of Scope

- implementing fixes,
- new feature work,
- unrelated repository cleanup,
- judging style preferences without a concrete correctness or maintainability impact.

---

## MUST Have (Non-Negotiable)

- [ ] Read `PLAN _REFACTOR.md` completely.
- [ ] Read `quality_reports/session_logs/2026-04-08_medical-refactor-audit-handoff.md` completely.
- [ ] Inspect the full diff for commit `9f8a6f7`.
- [ ] Verify whether active runtime files still contain high-confidence economics defaults or assumptions.
- [ ] Verify whether the medical reviewer taxonomy is internally consistent across:
  - `.claude/agents/editor.md`
  - `.claude/agents/domain-referee.md`
  - `.claude/agents/methods-referee.md`
  - `.claude/skills/review/SKILL.md`
  - `.claude/references/journal-profiles.md`
- [ ] Verify whether the smoke-test fixtures exist and match the documentation claims.
- [ ] Verify that new files introduced by the commit (`.claude/references/reporting-guidelines.md`, `.claude/skills/systematic-review/SKILL.md`) align with the plan (Phases 7 and 6.4).
- [ ] Verify that `.claude/settings.json` changes are consistent with the `biber` toolchain and contain no leftover economics-specific permissions.
- [ ] Check whether the handoff document accurately describes the implemented changes.
- [ ] Report only high-confidence, evidence-backed findings.
- [ ] Distinguish confirmed defects from preferences or possible improvements.

### SHOULD Have (Preferred)

- [ ] Assess whether major prompt simplifications removed important repository-specific guidance.
- [ ] Check whether public docs and runtime prompts tell the same story.
- [ ] Call out scope drift: planned but missing changes, or extra changes not described in the handoff.
- [ ] Give an explicit recommendation on `.claude/references/journal-profiles.html`: regenerate, remove, or ignore.

### MAY Have (Optional, If Time)

- [ ] Re-run the targeted validation commands cited in the handoff.
- [ ] Suggest a minimal follow-up patch list if issues are found.

---

## Suggested Audit Workflow

### 1. Read the intent documents first

- Read `PLAN _REFACTOR.md`
- Read `quality_reports/session_logs/2026-04-08_medical-refactor-audit-handoff.md`

### 2. Inspect the commit itself

- Review summary and file list
- Review the exact patch
- Classify changed files by category:
  - runtime
  - references/rules
  - docs
  - fixtures
  - audit metadata

### 3. Audit runtime consistency

Check whether the commit leaves behind contradictory assumptions in active `.claude` files, especially:

- economics/econometrics wording in active medical paths,
- references to economics-specific venues or taxonomies,
- outdated review logic,
- compile/tooling instructions inconsistent with `biber`,
- stale command descriptions that contradict the medical runtime.

### 4. Audit documentation consistency

Check whether:

- `CLAUDE.md`, `README.md`, and `guide/*.qmd` are aligned with the runtime,
- fixture files are documented as intentional smoke tests,
- docs overclaim anything not implemented by the runtime.

### 5. Audit known risk areas

Pay special attention to:

- `.claude/references/journal-profiles.html` being stale relative to the rewritten markdown source — specifically, check whether the HTML still contains the old economics taxonomy (STRUCTURAL, CREDIBILITY, MEASUREMENT, POLICY, THEORY) as concrete evidence for the regenerate/remove/ignore decision,
- large prompt rewrites that may have removed repository-specific nuance,
- any changed file category that was omitted from the handoff.

### 6. Verify key claims where useful

If feasible in the current environment, re-run targeted checks cited by the handoff, such as:

- `git diff --check`
- `quarto render guide`
- manuscript smoke-test compile
- Beamer smoke-test compile
- Quarto talk render

These are verification aids, not the primary basis of the audit.

---

## Suggested Commands

These are recommended, not mandatory:

```bash
git show --stat --summary 9f8a6f7
git diff 9f8a6f7^..9f8a6f7
git diff 9f8a6f7^..9f8a6f7 -- .claude CLAUDE.md README.md guide paper
git grep -nE 'economics|economic|econometric|top-5|NBER|AEA|JEL' 9f8a6f7 -- .claude CLAUDE.md README.md guide
git grep -nE 'CLINICAL|METHODOLOGICAL|EVIDENCE|ETHICAL|STATISTICAL|TRANSLATIONAL|SKEPTIC' 9f8a6f7 -- .claude
git grep -nE 'STRUCTURAL|CREDIBILITY|MEASUREMENT|POLICY|THEORY' 9f8a6f7 -- .claude/references/journal-profiles.html
```

**Note:** All `git grep` commands use `9f8a6f7` instead of `HEAD` so results remain valid even if the repository has moved on. To inspect a specific file at committed state, use `git show 9f8a6f7:path/to/file`.

---

## Deliverable Format

The auditor should return a structured report with:

1. **Overall verdict**
   - `PASS`
   - `PASS WITH RISKS`
   - `FAIL`

2. **Findings by severity**
   - High
   - Medium
   - Low

3. **For each finding**
   - title,
   - affected file(s),
   - evidence (path + line or exact diff region),
   - why it matters,
   - recommendation.

4. **Coverage checklist**
   - Plan alignment: Yes/No
   - Runtime consistency: Yes/No
   - Docs consistency: Yes/No
   - Validation claims credible: Yes/No
   - Fixture policy coherent: Yes/No
   - New files validated against plan: Yes/No
   - `settings.json` consistent with medical toolchain: Yes/No
   - `journal-profiles.html` decision made: Yes/No

5. **Final recommendation**
   - Is commit `9f8a6f7` a safe baseline for future work?
   - What are the smallest follow-up actions, if any?

---

## Exact Prompt for Another Agent

Use this prompt verbatim if you want another agent to perform the audit:

> Audit commit `9f8a6f7` in this repository.
>  
> First read:
> - `PLAN _REFACTOR.md`
> - `quality_reports/session_logs/2026-04-08_medical-refactor-audit-handoff.md`
> - `quality_reports/session_logs/2026-04-08_medical-refactor-audit-instructions.md`
>  
> Then audit whether commit `9f8a6f7` correctly refactors the runtime from economics/social-science defaults to medical-first pulmonary medicine defaults.
>  
> Focus on:
> 1. alignment with the approved plan plus agreed critical gaps,
> 2. internal consistency of active `.claude` runtime files,
> 3. leftover economics assumptions in active medical paths,
> 4. consistency of the reviewer taxonomy across editor/referee/journal-profile files,
> 5. consistency between runtime, docs, fixtures, and the handoff document,
> 6. whether `.claude/references/journal-profiles.html` is a meaningful stale artifact.
>  
> Report only high-confidence findings with concrete evidence.
> Distinguish actual defects from stylistic preferences.
>  
> Output a structured audit with:
> - overall verdict (`PASS`, `PASS WITH RISKS`, or `FAIL`),
> - findings grouped by severity,
> - exact file/path evidence,
> - a coverage checklist,
> - a final recommendation on whether commit `9f8a6f7` is a safe baseline for future work.

---

## Success Criteria

- Another agent can perform the audit without additional clarification.
- The scope is pinned to commit `9f8a6f7`.
- The handoff and plan are explicitly required inputs.
- The expected output format is concrete enough to compare audit results across agents.
