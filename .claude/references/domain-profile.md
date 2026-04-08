# Domain Profile

<!--
Medical-first default profile for pulmonary medicine / interventional pulmonology.
Adapt further for a specific disease area, intervention, or registry if needed.
-->

## Field

**Primary:** Pulmonary Medicine / Interventional Pulmonology
**Adjacent subfields:** Critical Care, Thoracic Oncology, Thoracic Surgery, Radiology, Epidemiology, Biostatistics

---

## Target Journals (ranked by tier)

| Tier | Journals |
|------|----------|
| General medicine | NEJM, The Lancet, JAMA, BMJ, Annals of Internal Medicine |
| Respiratory flagship | AJRCCM, Lancet Respiratory Medicine, ERJ, Thorax, CHEST |
| Respiratory broad | Respiratory Medicine, Respiration, ERJ Open Research, BMC Pulmonary Medicine |
| Interventional / thoracic oncology | JTO, JOBIP, Radiology, JVIR |
| Spanish-language / regional | Archivos de Bronconeumología, Open Respiratory Archives, Revista de Patología Respiratoria, Medicina Clínica, Revista Clínica Española |

---

## Common Data Sources

| Dataset | Type | Access | Notes |
|---------|------|--------|-------|
| PubMed / MEDLINE | Bibliographic | Public | Primary literature search via keywords + MeSH |
| Cochrane Library | Evidence synthesis | Subscription / public abstracts | High-value source for systematic reviews and trials |
| ClinicalTrials.gov | Trial registry | Public | Registration, protocol metadata, posted results |
| Institutional EHR / HCE | Clinical registry / EHR | Restricted | Requires ethics approval, governance, de-identification |
| SEER | Cancer registry | Restricted / public extracts | Useful for thoracic oncology, staging, survival |
| NHANES | Population survey | Public | Spirometry, smoking exposure, respiratory symptoms |
| BOLD Study | Cohort / epidemiology | Restricted | COPD prevalence and lung function across settings |
| COPDGene | Cohort | Restricted | Imaging, genomics, lung function, outcomes |
| UK Biobank | Population cohort | Restricted | Imaging, spirometry, outcomes, linkage potential |
| Local bronchoscopy / pleural registries | Procedural registry | Restricted | Interventional pulmonology outcomes and complications |

---

## Common Study Designs

| Design | Typical Use | Key Assumption to Defend |
|--------|-------------|--------------------------|
| Randomized controlled trial | New therapy, device, or procedural strategy | Randomization integrity, adherence, outcome completeness |
| Pragmatic trial | Comparative effectiveness in routine care | Real-world implementation without compromising allocation integrity |
| Prospective cohort | Prognosis, natural history, longitudinal outcomes | Follow-up completeness and confounding control |
| Retrospective cohort | Comparative effectiveness, safety, utilization | Selection bias, confounding, missingness, exposure definition |
| Case-control | Rare disease or rare outcome etiologic questions | Control selection, exposure ascertainment, temporality |
| Cross-sectional study | Prevalence, association, care patterns | Representativeness and careful non-causal interpretation |
| Diagnostic accuracy study | Test validation, staging, screening | Reference standard quality, blinding, disease spectrum |
| Prediction model study | Risk stratification, prognosis tools | Overfitting control, calibration, external validation |
| Systematic review / meta-analysis | Evidence synthesis | Search completeness, bias assessment, heterogeneity handling |

---

## Common Outcomes and Endpoints

- Overall survival, disease-free survival, progression-free survival
- Time to exacerbation, hospitalization, ICU transfer, ventilation, reintervention
- FEV1, FVC, FEV1/FVC, DLCO, oxygen requirement, exercise tolerance
- 6-minute walk distance, mMRC, CAT, SGRQ, symptom burden, quality of life
- Technical success, clinical success, complication rates, pneumothorax, bleeding
- Diagnostic sensitivity, specificity, PPV, NPV, AUC, calibration
- Adverse events, serious adverse events, treatment discontinuation

---

## Clinical Guidelines and Standards

- GOLD (COPD)
- GINA (Asthma)
- ATS / ERS statements and technical standards
- NCCN (thoracic oncology)
- BTS and SEPAR guidance when regionally relevant
- EQUATOR reporting guidance: CONSORT, STROBE, PRISMA, STARD, TRIPOD
- ICMJE recommendations for authorship, disclosures, and trial registration

---

## Field Conventions

- Prefer clinically interpretable effect measures: HR, OR, RR, risk difference, NNT/NNH when meaningful
- Pair relative effects with absolute risks or event rates whenever possible
- Time-to-event work should usually show Kaplan-Meier curves and an appropriate survival model
- Baseline characteristics belong in a Table 1 style summary with transparent missingness
- Always report harms, complications, and protocol deviations when applicable
- Structured abstracts are the default: Background, Methods, Results, Conclusions
- MeSH terms replace legacy field codes; registration identifiers replace generic working-manuscript metadata
- Clinical significance matters as much as statistical significance
- Claims must be proportional to the design: observational work is not randomized evidence

---

## Notation Conventions

| Symbol / Term | Meaning | Anti-pattern |
|---------------|---------|-------------|
| HR | Hazard ratio | Do not report p-values without the estimate and 95% CI |
| OR | Odds ratio | Do not present OR as if it were risk without clarifying |
| RR | Risk ratio | Avoid switching RR and OR across text/tables without warning |
| 95% CI | Precision interval | Avoid “significant / not significant” without interval context |
| aHR / aOR | Adjusted effect estimate | Define adjustment set or model clearly |
| ITT | Intention-to-treat analysis | Do not relabel per-protocol results as primary ITT |

---

## Seminal References

| Paper / Standard | Why It Matters |
|------------------|---------------|
| GOLD Report | Core COPD classification and management framework |
| National Lung Screening Trial (NLST) | Landmark CT screening trial in lung cancer |
| NELSON Trial | Key evidence on LDCT screening effectiveness |
| TORCH | Foundational COPD therapeutic trial |
| UPLIFT | Major COPD long-term outcome trial |
| IMPACT | Triple-therapy evidence in COPD |
| VENT | Seminal endobronchial valve trial |
| LIBERATE | Important bronchoscopic lung volume reduction trial |
| ATS / ERS bronchoscopy and pulmonary function standards | Technical and reporting expectations for procedures and lung function |

---

## Field-Specific Referee Concerns

- Is the study aligned with the correct reporting guideline for its design?
- Are ethics approval, consent, and registry information clearly reported when required?
- Are the primary endpoints clinically meaningful or merely statistically convenient?
- Is survival or recurrent-event analysis appropriate for the outcome process?
- Are harms and complications described as thoroughly as benefits?
- Is the study too dependent on expert-center practice to generalize?
- Are subgroup, biomarker, or prediction claims externally validated and pre-specified?
- Is missing data handled credibly and described transparently?

---

## Quality Tolerance Thresholds

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Point estimates | 1e-4 relative | Small numerical differences across software are expected |
| Standard errors | 1e-3 relative | Survival / GLM implementations may differ slightly |
| Survival probabilities | ± 0.005 | Landmark estimates are sensitive to rounding and tie handling |
| AUC / C-index | ± 0.002 | Minor resampling and optimization drift is acceptable |
| Meta-analysis pooled effects | 1e-3 relative | Package defaults can vary slightly |
