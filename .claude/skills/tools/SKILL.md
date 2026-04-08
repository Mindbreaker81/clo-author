---
name: tools
description: Utility commands — commit, compile, validate-bib, journal, context-status, deploy, learn.
argument-hint: "[subcommand: commit | compile | validate-bib | journal | context | deploy | learn | upgrade] [args]"
allowed-tools: Read,Grep,Glob,Write,Edit,Bash,Task
---

# Tools

Utility subcommands for project maintenance and infrastructure.

## Subcommands

### `/tools commit [message]`
Stage changes, create commit, optionally create PR.

### `/tools compile [file]`
3-pass XeLaTeX + biber compilation.

For papers:
```bash
cd paper && TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode [file]
BIBINPUTS=..:$BIBINPUTS biber [file_base]
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode [file]
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode [file]
```

For talks:
```bash
cd paper/talks && TEXINPUTS=../preambles:$TEXINPUTS xelatex -interaction=nonstopmode [file]
```

### `/tools validate-bib`
Cross-reference all `\cite{}` keys in paper and talk files against `Bibliography_base.bib`.

### `/tools journal`
Regenerate the research journal timeline from quality reports and git history.

### `/tools context`
Show current context status and session health.

### `/tools deploy`
Render the Quarto guide site and publish to GitHub Pages.

### `/tools learn`
Extract reusable workflow knowledge from the current session.

### `/tools upgrade`
Upgrade `.claude/` while preserving filled-in profiles and local settings.

## Principles

- Compile uses XeLaTeX + biber
- `validate-bib` catches broken citation drift before review or submission
- Upgrade preserves project content outside `.claude/`
