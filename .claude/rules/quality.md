# Quality: Scoring, Thresholds, and Severity

## 1. Scoring Protocol

### Weighted Aggregation

The overall project score that gates submission is the weighted aggregate below:

| Component | Weight | Source Agent |
|-----------|--------|-------------|
| Literature coverage | 15% | librarian-critic |
| Data quality | 15% | explorer-critic |
| Study design validity | 25% | strategist-critic |
| Code quality | 10% | coder-critic |
| Paper quality | 25% | Average of domain-referee + methods-referee |
| Manuscript polish | 5% | writer-critic |
| Replication / submission readiness | 5% | verifier |

### Minimum Per Component

No component can be below 80 for submission.

### Gate Thresholds

| Gate | Overall Score | Per-Component Minimum | Action |
|------|--------------|----------------------|--------|
| Commit | >= 80 | None enforced | Allowed |
| PR | >= 90 | None enforced | Allowed |
| Submission | >= 95 | >= 80 per component | Allowed |
| Below 80 | < 80 | — | Blocked |

### When Components Are Missing

If a component has not been scored, exclude it and renormalize the remaining weights.

---

## 2. Medical Gate Add-ons

The following checks should be treated as high-severity quality items when applicable:

- Correct reporting guideline matched to design (CONSORT, STROBE, PRISMA, STARD, TRIPOD)
- Ethics / IRB / consent statement
- Trial or protocol registration for interventional work
- Clinically meaningful primary outcomes and effect sizes
- Harms / adverse-event reporting
- Missing-data strategy and sensitivity analysis
- Conflict-of-interest and funding disclosure
- Clear distinction between statistical significance and clinical significance

---

## 3. Severity Gradient

| Phase | Critic Stance | Rationale |
|-------|--------------|-----------|
| Discovery | Encouraging | Early ideas need room to develop |
| Design | Constructive | Study design and protocol flaws should be caught early |
| Execution | Strict | Errors in analysis or manuscript structure are costly |
| Peer Review | Adversarial | Simulates real clinical peer review |
| Presentation | Professional | Talks should be polished but remain advisory |

### Example Deduction Scaling

| Issue | Discovery | Design | Execution | Peer Review |
|-------|-----------|--------|-----------|-------------|
| Missing key clinical citation | -2 | -5 | -10 | -15 |
| Missing ethics / registration detail | -5 | -10 | -15 | -20 |
| Missing harms analysis | — | -5 | -15 | -20 |
| Overstated causal language in observational work | -2 | -5 | -10 | -15 |

### Principle

Early phases are about choosing the right clinical question and defensible design. Late phases are about correctness, transparency, and submission readiness.
