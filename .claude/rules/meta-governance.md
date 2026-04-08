# Meta-Governance: This Repository's Dual Nature

This repository is both a working project and a public template for medical and clinical research workflows, with a default calibration to pulmonary medicine / interventional pulmonology.

## Working Project
- We develop manuscripts, protocols, talks, and supporting research materials
- We accumulate project-specific clinical context, reviewer feedback, and methodological conventions
- We test and iterate on the architecture itself

## Public Template
- Others can fork this repo to run their own clinical research workflows
- They share the same pipeline (discover → design → analyze → write → review → submit)
- Field-specific differences are handled by `.claude/references/domain-profile.md`, `.claude/references/journal-profiles.md`, and `.claude/references/reporting-guidelines.md`

## The One Rule

Before committing, ask: **would another clinical researcher forking this repo benefit from this?**

- **Yes** → commit (workflow patterns, skills, agents, rules, templates)
- **No** → keep local in `.claude/state/` (machine paths, tool versions, institutional requirements, secrets)
