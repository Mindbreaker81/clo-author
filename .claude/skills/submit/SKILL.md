---
name: submit
description: Submission pipeline — journal targeting, submission package, audit, and final gate for medical manuscripts.
argument-hint: "[mode: target | package | audit | final] [journal name (optional)]"
allowed-tools: Read,Grep,Glob,Write,Bash,Task
---

# Submit

Submission pipeline with four modes covering journal targeting through final verification.

## Modes

### `/submit target`
Get ranked journal recommendations based on fit, evidence level, design, audience, and bar.

### `/submit package`
Assemble a journal-ready package.

Produces:
- manuscript inventory
- figure / table inventory
- reporting checklist draft
- disclosure / funding / data-sharing statement draft
- submission notes or cover-letter draft

### `/submit audit`
Verify submission package completeness.

Checks:
1. manuscript assets organized
2. reporting checklist present
3. ethics / consent / registration statements present where needed
4. disclosures and funding documented
5. data provenance or sharing statement included
6. dependencies listed
7. tables / figures trace back to scripts
8. no obvious hardcoded sensitive paths

### `/submit final [journal]`
Run final verification and the score gate:
1. run comprehensive review if needed
2. run submission audit
3. check score gate: aggregate >= 95 and all components >= 80
4. if pass: generate final checklist and submission notes
5. if fail: list blockers and stop

## Principles

- Do not prepare a submission package for a failing paper
- Submission readiness includes reporting and ethics, not just analysis correctness
- Journal choice should match the contribution and design honestly
