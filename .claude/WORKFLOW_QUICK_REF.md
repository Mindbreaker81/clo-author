# Workflow Quick Reference

**Model:** Contractor (you direct, Claude orchestrates via dependency graph)

---

## The Research Pipeline

```
/discover interview → Research Spec + Domain Profile
    ↓
/discover lit → Literature Synthesis (Librarian + librarian-critic)
    ↓
/discover data → Data Assessment (Explorer + explorer-critic)
    ↓
/strategize → Study Design / Protocol Memo (Strategist + strategist-critic)
    ↓
/analyze → Scripts + Output (Coder/Data-engineer + coder-critic)
    ↓
/write → Manuscript Sections (Writer + writer-critic)
    ↓
/review → Weighted Score + Peer Review (domain-referee + methods-referee)
    ↓
/submit → Final Gate (score >= 95, all components >= 80)
```

Enter at any stage. Use `/new-project` for the full pipeline.

---

## The 10 Commands

| Command | What It Does |
|---------|-------------|
| `/new-project [topic]` | Full pipeline: question to manuscript |
| `/discover [interview|lit|data]` | Research spec, literature review, or data discovery |
| `/strategize [question]` | Study design + methods review |
| `/analyze [dataset]` | End-to-end analysis: scripts, output, code review |
| `/write [section]` | Draft manuscript sections + humanizer pass |
| `/review [file]` | Multi-agent quality review + peer review |
| `/revise [report]` | Route referee comments and response planning |
| `/talk [format]` | Presentation creation / audit |
| `/submit [journal]` | Final gate: score >= 95, all components >= 80 |
| `/tools [subcommand]` | commit, compile, validate-bib, journal, context, deploy, learn |

---

## Quality Gates at a Glance

| Score | Gate | What It Means |
|-------|------|--------------|
| >= 95 | Submission | Ready for journal submission |
| >= 90 | PR | Ready to merge |
| >= 80 | Commit | Ready to commit |
| < 80 | **Blocked** | Must fix critical / major issues |
| -- | Advisory | Talks only |

Weighted aggregate: Literature 15% + Data 15% + Study design 25% + Code 10% + Paper 25% + Polish 5% + Replication 5%

---

## I Ask You When

- **Design forks:** "Option A vs. Option B. Which?"
- **Endpoint choice:** "Time-to-event vs binary endpoint as primary?"
- **Registry / ethics ambiguity:** "Which registration or approval path applies?"
- **After 3 strikes:** "Worker and critic disagree — your call"

## I Just Execute When

- Code fix is obvious
- Verification or static checks are mechanical
- Reporting alignment is straightforward
- Formatting or routing changes are clearly implied by the chosen design

---

## Exploration Mode

For experimental work:
- Work in `explorations/`
- 60/100 quality threshold (vs. 80/100 for production)
- No plan needed — just a research-value check
- See `.claude/rules/content-standards.md`

---

## Next Step

You provide task → I plan (if needed) → Your approval → Execute → Done.
