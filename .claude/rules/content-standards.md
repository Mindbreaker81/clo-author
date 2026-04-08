---
paths:
  - "**/*.R"
  - "**/*.py"
  - "**/*.jl"
  - "**/*.do"
  - "**/*.tex"
  - "paper/tables/**"
  - "paper/figures/**"
  - "master_supporting_docs/**"
  - "explorations/**"
---

# Content Standards: Medical Tables, Figures, and Outputs

## 1. Table Standards

**Target:** Publication-quality clinical tables suitable for respiratory, internal medicine, and general medical journals.

### Core Rules

- Never embed titles, notes, or sources inside the table body
- Use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) and zero vertical lines
- Use `threeparttable` for notes
- Label variables in plain clinical language, not raw code names
- Report effect estimates with 95% confidence intervals; do not report isolated p-values without estimates
- Include denominators and missingness when they materially affect interpretation

### Baseline Characteristics (Table 1)

```latex
\toprule
Characteristic & Treatment (n=120) & Control (n=118) & p-value \\
\midrule
Age, years & 65.2 \pm 8.1 & 64.8 \pm 7.9 & 0.45 \\
Male sex, n (\%) & 72 (60.0) & 70 (59.3) & 0.91 \\
FEV1, \% predicted & 42.3 \pm 12.1 & 43.1 \pm 11.8 & 0.52 \\
Current smoker, n (\%) & 28 (23.3) & 26 (22.0) & 0.81 \\
\bottomrule
```

### Clinical Effect Estimates

```latex
\toprule
Variable & HR & 95\% CI & p-value \\
\midrule
Endobronchial valve treatment & 0.72 & (0.58--0.89) & 0.003 \\
Age (per year) & 1.02 & (1.01--1.03) & 0.001 \\
Male sex & 1.15 & (0.92--1.44) & 0.22 \\
\bottomrule
```

Prefer:
- HR for time-to-event outcomes
- OR or RR for binary outcomes
- Mean difference / standardized difference for continuous outcomes
- Absolute risk difference and NNT/NNH when clinically useful

### Descriptive and Safety Tables

- Adverse-event tables should separate any event, serious events, and key pre-specified complications
- Procedural papers should report technical success, clinical success, and complication grades
- Diagnostic papers should report sensitivity, specificity, PPV, NPV, and confidence intervals

### Preferred R Packages

- `gtsummary` / `gt` for publication-ready clinical tables
- `tableone` for baseline summaries
- `survival` + `survminer` for time-to-event analyses
- `meta` / `metafor` for meta-analysis
- `forestplot` for forest plots
- `yardstick`, `pROC`, or equivalent for diagnostic and prediction summaries

### File Naming

```
paper/tables/
├── baseline_table1.tex
├── primary_outcome_cox.tex
├── adverse_events.tex
├── subgroup_analysis.tex
└── supplementary_sensitivity.tex
```

---

## 2. Figure Standards

### Core Rules

- Use clear axis labels with clinical units
- Prefer sentence case; avoid decorative titles inside the figure canvas
- Legends belong where they do not obscure the data
- Use color palettes that remain legible in grayscale and for color-vision deficiency
- Ensure reproducible dimensions and transparent backgrounds where appropriate

### Default Figure Types

- **Kaplan-Meier curve** with numbers at risk for survival outcomes
- **Forest plot** for subgroup or meta-analytic effects
- **CONSORT / study flow diagram** for participant accounting
- **ROC curve and calibration plot** for diagnostic or prediction studies
- **Longitudinal line plot / spaghetti summary** for repeated measures when interpretable

### Survival Figure Template

- Show confidence bands or clearly explain if omitted
- Define time origin and censoring rules
- Include numbers at risk below the x-axis when space permits

### Procedural / Safety Figure Rules

- Complication visuals should preserve denominators
- Imaging-based figures need clear modality, plane, and annotations
- Before/after procedural panels should use consistent scales and legends

---

## 3. Output and Export Rules

- R output should save bare `tabular` fragments for tables unless the downstream manuscript explicitly needs a full float
- Save every computed object needed downstream with `saveRDS()` or language-equivalent serialization
- Tables go to `paper/tables/`; figures go to `paper/figures/`
- Generated filenames should describe the endpoint or clinical question, not the temporary script state

---

## 4. Prohibited Patterns

| Pattern | Reason |
|---------|--------|
| `\hline` or vertical rules | Not publication quality |
| Reporting only stars / p-values | Clinically uninformative without estimate and CI |
| Raw variable names in final tables | Readers need clinical labels |
| Missing harms table for interventional work | Safety reporting is mandatory |
| Default gray ggplot theme in final figures | Not publication ready |
| No participant flow accounting | Sample construction becomes opaque |
