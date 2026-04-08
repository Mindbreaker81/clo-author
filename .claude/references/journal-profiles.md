# Journal Profiles

<!--
These profiles calibrate the editor, domain-referee, and methods-referee
when reviewing for a specific journal. Each profile describes the journal's
review culture in plain language so the LLM can adapt naturally.

Used by: editor.md, domain-referee.md, methods-referee.md, /review --peer
-->

## How This Works

When `/review --peer [journal]` is invoked:

1. **Editor reads the paper** → desk review (reject or send to referees)
2. **Editor selects referees** → draws dispositions and pet peeves from the journal's **Referee pool**
3. **Profile found below** → referees calibrate using the full profile
4. **Profile NOT found** → referees use the journal name + `.claude/references/domain-profile.md` to adapt
5. **No journal specified** → generic medical specialty referee behavior

### Referee Pool Field

Each journal profile includes a **Referee pool** that weights which dispositions the editor draws from. The two referees always get DIFFERENT dispositions.

Dispositions:
- **CLINICAL** — patient-important outcomes, bedside usefulness, guideline relevance
- **METHODOLOGICAL** — study design integrity, bias control, reporting completeness
- **EVIDENCE** — hierarchy of evidence, literature synthesis, certainty, guideline positioning
- **ETHICAL** — consent, IRB, registration, safety, transparency, conflicts
- **STATISTICAL** — effect measures, power, survival methods, multiplicity, missing data
- **TRANSLATIONAL** — mechanism-to-practice bridge, biomarker relevance, bench-to-bedside logic
- **SKEPTIC** — assumes the paper is not ready and looks for the failure mode first

---

## Medicine

**General Medicine**

### New England Journal of Medicine (NEJM)
**Focus:** Practice-changing clinical and translational medicine for a broad physician audience.
**Bar:** Major question, near-definitive evidence, and immediate implications for care or guidelines.
**Domain referee adjusts:** Patient-important outcomes, disease burden, safety, and whether the result would change decisions beyond a narrow subspecialty.
**Methods referee adjusts:** Trial conduct, endpoint choice, follow-up, missingness, subgroup restraint, and clear absolute benefits and harms.
**Typical concerns:** "Is this clinically decisive or just statistically positive?" "Are the outcomes patient-important?" "Is the safety and follow-up evidence mature enough?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (high), EVIDENCE (high), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (medium), SKEPTIC (low)

### The Lancet
**Focus:** High-impact clinical medicine, public health, and health policy with international relevance.
**Bar:** Must matter beyond one setting and speak to population health, health systems, or globally salient clinical practice.
**Domain referee adjusts:** Equity, implementation, public-health significance, and whether the paper speaks to clinicians and policy audiences across countries.
**Methods referee adjusts:** Rigorous design plus transparent limits, with explicit attention to external validity, harms, and real-world applicability.
**Typical concerns:** "Is this globally important or mainly local?" "Where is the equity or implementation insight?" "Are the policy claims too strong for the data?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (high), ETHICAL (high), STATISTICAL (medium), TRANSLATIONAL (high), SKEPTIC (medium)

### JAMA
**Focus:** Clinically consequential medicine, health systems, and public health for a broad generalist readership.
**Bar:** Important, readable, actionable findings for practicing physicians, health system leaders, or guideline-facing audiences.
**Domain referee adjusts:** Patient care, care delivery, population impact, and whether the finding is useful outside the immediate subspecialty.
**Methods referee adjusts:** Clean design, disciplined causal language, transparent effect sizes, appropriate confounding control, and restrained subgroup claims.
**Typical concerns:** "Is this too subspecialized for JAMA?" "Is the clinical importance large enough?" "Are associative data being overstated as causal?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (high), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (medium), SKEPTIC (medium)

### BMJ
**Focus:** Evidence-based medicine, clinical decision-making, health services, and policy with a strong patient and public-interest orientation.
**Bar:** Should improve real-world decisions, usually with clear implications for practice, systems, or policy rather than technical novelty alone.
**Domain referee adjusts:** Patient-centeredness, equity, overdiagnosis or overtreatment, transparency, and usefulness for clinicians or policymakers.
**Methods referee adjusts:** Careful reporting, conservative causal language, absolute risks and harms, protocol fidelity, and explicit treatment of bias, multiplicity, and missing data.
**Typical concerns:** "Does this improve decisions in practice?" "Are patient-important outcomes and harms clear?" "Is there spin, unresolved confounding, or weak transparency?"
**Referee pool:** CLINICAL (medium), METHODOLOGICAL (high), EVIDENCE (high), ETHICAL (high), STATISTICAL (high), TRANSLATIONAL (medium), SKEPTIC (high)

### Annals of Internal Medicine
**Focus:** Evidence that directly informs adult internal medicine practice, prevention, diagnosis, therapeutics, and guideline-facing care.
**Bar:** Rigorous, clinically useful work relevant to general internists rather than only a narrow referral population.
**Domain referee adjusts:** Everyday inpatient and ambulatory applicability, patient-important outcomes, and whether the paper clarifies a common diagnostic or therapeutic decision.
**Methods referee adjusts:** Trial conduct, comparative-effectiveness logic, diagnostic performance, evidence certainty, and cautious interpretation of observational designs.
**Typical concerns:** "Would a general internist change practice?" "Is the evidence strong enough for common care decisions?" "Are applicability and harms adequately handled?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (high), EVIDENCE (high), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (low), SKEPTIC (medium)

**Respiratory Medicine**

### American Journal of Respiratory and Critical Care Medicine (AJRCCM)
**Focus:** Flagship ATS journal for pulmonary, critical care, and sleep medicine; publishes influential clinical, translational, epidemiologic, and mechanistic studies.
**Bar:** Must materially advance respiratory or ICU practice, or meaningfully deepen disease understanding; incremental work rarely clears.
**Domain referee adjusts:** Prioritizes patient-important outcomes, strong phenotyping, and a clear bridge between mechanism and clinical relevance.
**Methods referee adjusts:** Expects CONSORT/STROBE-level reporting, careful confounding control, appropriate survival methods, transparent missing-data handling, and restrained subgroup claims.
**Typical concerns:** "Is this important enough for the Blue Journal?" "Are the endpoints clinically meaningful?" "Does the mechanistic story truly support the clinical claim?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (high), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (high), SKEPTIC (medium)

### Lancet Respiratory Medicine
**Focus:** Highest-impact respiratory specialty journal for practice-changing trials, global respiratory health, critical care, and major translational advances.
**Bar:** Needs international importance, strong novelty, and clear implications for practice, policy, or the field’s direction.
**Domain referee adjusts:** Wants big clinical questions, patient-centered endpoints, and results that matter beyond a narrow subspecialty.
**Methods referee adjusts:** Trial registration, protocol fidelity, multiplicity control, safety reporting, prespecified analyses, and external validity are scrutinized heavily.
**Typical concerns:** "Is this truly practice-changing?" "Are benefits clinically important and harms fully characterized?" "Does it matter globally, not just locally?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (high), EVIDENCE (high), ETHICAL (high), STATISTICAL (high), TRANSLATIONAL (medium), SKEPTIC (medium)

### European Respiratory Journal (ERJ)
**Focus:** Flagship ERS journal covering clinical, translational, and basic respiratory science across the full spectrum of lung disease.
**Bar:** Top specialty paper with broad interest to respiratory clinicians and scientists; novelty matters, but completeness and relevance matter just as much.
**Domain referee adjusts:** Emphasizes respiratory phenotyping, guideline relevance, and a clear bridge between pathobiology and patient care.
**Methods referee adjusts:** Wants strong design, contemporary respiratory biostatistics, good sensitivity analyses, and reporting that travels across international cohorts and registries.
**Typical concerns:** "Is this more than incremental?" "Does it change disease interpretation or management?" "Are findings generalizable across settings?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (high), ETHICAL (low), STATISTICAL (medium), TRANSLATIONAL (high), SKEPTIC (medium)

### Thorax
**Focus:** High-impact BMJ / BTS journal for respiratory medicine and critical care, especially work with a crisp clinical or translational takeaway.
**Bar:** Needs a sharp message, specialty-wide interest, and visible relevance to clinicians, investigators, or guideline development.
**Domain referee adjusts:** Prefers clinically anchored mechanistic work, strong respiratory epidemiology, and manuscripts that clearly state what they add.
**Methods referee adjusts:** Demands clean reporting, causal modesty in observational work, solid sensitivity analyses, and clear safety or harms presentation.
**Typical concerns:** "What changes after reading this?" "Is the endpoint patient-important?" "Are causal claims stronger than the design allows?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (medium), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (high), SKEPTIC (medium)

### CHEST
**Focus:** Broad pulmonary, critical care, sleep, and thoracic medicine journal with strong emphasis on bedside applicability and multidisciplinary care.
**Bar:** Strong clinically useful paper; it need not be field-defining, but it must inform management, diagnosis, procedures, or care delivery.
**Domain referee adjusts:** Rewards pragmatic studies, guideline-relevant questions, procedural papers with real-world detail, and outcomes clinicians can act on.
**Methods referee adjusts:** Expects transparent inclusion criteria, appropriate comparators, practical subgroup analyses, complication reporting, and statistics clinicians can trust.
**Typical concerns:** "Will this change what I do tomorrow?" "Is the cohort representative of real practice?" "Are procedural risks and implementation details clear?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (high), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (low), SKEPTIC (low)

### Respiratory Medicine
**Focus:** Broad clinical respiratory journal centered on diagnosis, management, therapeutics, rehabilitation, and real-world respiratory care.
**Bar:** Well-executed applied respiratory study with clear clinical relevance; novelty threshold is solid but not elite-journal level.
**Domain referee adjusts:** Likes treatment effectiveness, symptom and function outcomes, chronic disease management, and data that can inform routine care.
**Methods referee adjusts:** Sound design and clear reporting matter more than flashy methods; expects adequate power, appropriate adjustment, and conclusions matched to evidence.
**Typical concerns:** "Is the clinical contribution large enough?" "Is this underpowered or too single-center?" "Are outcomes meaningful to respiratory practice?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (medium), ETHICAL (low), STATISTICAL (medium), TRANSLATIONAL (low), SKEPTIC (low)

### Respiration
**Focus:** Clinical and experimental pulmonology with notable strength in interventional pulmonology, respiratory physiology, critical care, and sleep-related work.
**Bar:** Strong specialty paper, especially for procedural, diagnostic, device, or physiology-driven studies with clear patient relevance.
**Domain referee adjusts:** Expects technical credibility, careful safety reporting, and a persuasive link from procedural or physiologic findings to patient benefit.
**Methods referee adjusts:** Diagnostic accuracy, feasibility, and intervention studies must describe operators, complications, follow-up, and sources of bias in detail.
**Typical concerns:** "Is this reproducible beyond expert centers?" "Are safety events fully described?" "Does the physiology translate into meaningful clinical value?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (medium), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (high), SKEPTIC (medium)

### ERJ Open Research
**Focus:** Fully open-access ERS journal for broad respiratory research, with an inclusive and rapid-publication orientation.
**Bar:** Must be clearly relevant and methodologically sound; novelty helps, but solid execution can beat lack of flash.
**Domain referee adjusts:** Welcomes clinically useful, emerging, confirmatory, and niche respiratory studies if the question is clear and the reporting is complete.
**Methods referee adjusts:** Prioritizes transparency, reporting-guideline compliance, sensible statistics, and conclusions that stay proportional to the design.
**Typical concerns:** "Is the respiratory relevance clear?" "Is the reporting complete enough for reproducibility?" "Are claims too strong for the study design?"
**Referee pool:** CLINICAL (medium), METHODOLOGICAL (high), EVIDENCE (medium), ETHICAL (low), STATISTICAL (medium), TRANSLATIONAL (medium), SKEPTIC (low)

### BMC Pulmonary Medicine
**Focus:** Broad open-access pulmonary journal publishing scientifically valid work on prevention, diagnosis, management, and outcomes across lung disease.
**Bar:** Sound pulmonary study with clear methods and reporting; novelty threshold is moderate, validity threshold is not.
**Domain referee adjusts:** Suits real-world cohorts, observational studies, and clinically practical questions with pulmonary or public-health relevance.
**Methods referee adjusts:** Emphasizes ethical compliance, transparent reporting, reproducibility, appropriate adjustment, and statistical correctness over splashiness.
**Typical concerns:** "Is the study scientifically sound?" "Are definitions and analyses reproducible?" "Do the conclusions outrun the data?"
**Referee pool:** CLINICAL (medium), METHODOLOGICAL (high), EVIDENCE (medium), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (low), SKEPTIC (low)

**Interventional, Oncology, and Spanish-Language Journals**

### Journal of Bronchology and Interventional Pulmonology (JOBIP)
**Focus:** Interventional pulmonology, bronchoscopy, pleural procedures, central airway disease, and procedure-driven innovation for pulmonary specialists.
**Bar:** A specialized clinical paper with clear procedural relevance, solid technique description, and credible safety / outcome reporting.
**Domain referee adjusts:** Wants practical value for bronchoscopists: patient selection, technical nuance, complication management, learning curve, and whether the paper changes how a procedure is done.
**Methods referee adjusts:** Expects clear endpoint definitions, standardized complication reporting, appropriate comparators when possible, and follow-up long enough to assess durability and safety.
**Typical concerns:** "Is this more than a case series?" "Are the complications fully reported?" "Can other centers reproduce this technique?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (medium), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (medium), SKEPTIC (low)

### Journal of Thoracic Oncology (JTO)
**Focus:** Multidisciplinary thoracic oncology, including prevention, screening, diagnosis, staging, systemic therapy, radiation, surgery, biomarkers, and translational cancer research.
**Bar:** Very high. The paper should be practice-changing, field-advancing, or a major translational contribution with strong clinical consequences.
**Domain referee adjusts:** Wants clear relevance to thoracic malignancies, clinically meaningful endpoints, molecular or therapeutic context, and a contribution that matters to oncologists across disciplines.
**Methods referee adjusts:** Expects CONSORT / STROBE / REMARK-level reporting, robust survival methods, careful subgroup handling, external validation for biomarkers/models, and strong control of bias.
**Typical concerns:** "Will this change management?" "Is the biomarker or subgroup claim truly validated?" "Are the survival analyses and multiplicity handled correctly?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (high), EVIDENCE (high), ETHICAL (medium), STATISTICAL (high), TRANSLATIONAL (high), SKEPTIC (medium)

### Radiology
**Focus:** High-impact diagnostic imaging, quantitative imaging, image-guided intervention, imaging technology, and clinically relevant radiologic science across subspecialties.
**Bar:** Extremely high. Novelty alone is not enough; the paper needs broad relevance, technical rigor, and convincing clinical or workflow impact.
**Domain referee adjusts:** Wants a clear imaging question, reproducible protocol, real incremental value over current practice, and generalizability across readers, scanners, and institutions.
**Methods referee adjusts:** Expects strong reference standards, reader-study rigor when relevant, reproducibility metrics, external validation, and careful handling of model performance and spectrum bias.
**Typical concerns:** "Is this broadly relevant or just technically clever?" "Does it generalize beyond one center or scanner?" "What is the incremental value over standard imaging practice?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (high), EVIDENCE (medium), ETHICAL (low), STATISTICAL (high), TRANSLATIONAL (medium), SKEPTIC (high)

### Journal of Vascular and Interventional Radiology (JVIR)
**Focus:** Minimally invasive image-guided vascular and nonvascular procedures, devices, peri-procedural care, quality improvement, and real-world interventional outcomes.
**Bar:** Strong procedural paper with clear clinical importance, standardized outcome reporting, and convincing safety data; multicenter and comparative studies are especially favored.
**Domain referee adjusts:** Wants clear indications, technical success, complication grading, reintervention burden, and whether the study changes interventional practice.
**Methods referee adjusts:** Expects SIR-style reporting standards, consistent endpoint definitions, appropriate time-to-event or patency analyses, and serious attention to selection bias and operator effects.
**Typical concerns:** "Is there a meaningful comparator?" "Are durability and complications reported transparently?" "Is the result generalizable beyond expert operators?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (high), EVIDENCE (medium), ETHICAL (medium), STATISTICAL (high), TRANSLATIONAL (medium), SKEPTIC (medium)

### Archivos de Bronconeumología
**Focus:** Broad respiratory medicine and thoracic surgery for an international and Spanish-speaking audience, including original research, reviews, guidelines, and society-relevant clinical work.
**Bar:** High for a specialty respiratory journal. The paper should be clinically meaningful, well executed, and relevant beyond a single local unit.
**Domain referee adjusts:** Wants strong respiratory relevance, alignment with current pneumology practice, and a clear takeaway for clinicians dealing with common or important thoracic disease.
**Methods referee adjusts:** Expects solid observational or clinical methods, guideline-compliant reporting, sensible adjustment strategy, and enough robustness to support applied claims.
**Typical concerns:** "Is the contribution novel beyond a local series?" "Does this matter to the wider respiratory community?" "Are the methods strong enough for the claim?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (high), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (low), SKEPTIC (low)

### Open Respiratory Archives
**Focus:** Open-access respiratory medicine from the SEPAR orbit, including clinical research, reviews, practice-oriented studies, and broader specialty communication.
**Bar:** A solid respiratory paper with a clear message and practical value; the standard is real peer-reviewed rigor, but not necessarily field-defining novelty.
**Domain referee adjusts:** Wants usefulness for respiratory clinicians, a clean clinical message, and fit with everyday pulmonary practice, education, or real-world care.
**Methods referee adjusts:** Expects transparent design, complete reporting, appropriate statistics for the scale of the study, and claims that stay proportional to the evidence.
**Typical concerns:** "Is the message clear enough?" "Are the conclusions too strong for the design?" "Does the paper add enough beyond routine local experience?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (medium), ETHICAL (low), STATISTICAL (medium), TRANSLATIONAL (low), SKEPTIC (low)

### Revista de Patología Respiratoria
**Focus:** Spanish-language respiratory medicine with emphasis on clinical updates, reviews, case reports, small series, and educational material for practicing pulmonologists.
**Bar:** More practice-oriented than high-impact specialty journals; clarity, relevance, and teaching value can matter as much as novelty.
**Domain referee adjusts:** Wants a concrete clinical lesson, strong imaging or bronchoscopic documentation when relevant, and obvious value for respiratory clinicians in routine care.
**Methods referee adjusts:** Expects rigor proportional to the format: case reports need clear novelty and consent context; series need transparent selection, outcomes, and limitations.
**Typical concerns:** "What is genuinely new here?" "Is the teaching point strong enough?" "Is this adequately documented rather than anecdotal?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (low), EVIDENCE (low), ETHICAL (medium), STATISTICAL (low), TRANSLATIONAL (low), SKEPTIC (low)

### Medicina Clínica
**Focus:** Broad clinical medicine and internal medicine for a Spanish and hospital-based readership, including original research, reviews, consensus documents, and specialty work with general clinical relevance.
**Bar:** A good clinically relevant paper with implications beyond a narrow subspecialty niche; broad medical usefulness matters more than frontier novelty.
**Domain referee adjusts:** Wants a message that internists and hospital clinicians can use, not just subspecialists; practical implications, comorbidity context, and external clinical relevance are important.
**Methods referee adjusts:** Expects competent observational or clinical study design, reporting-guideline compliance, sensible confounding control, and appropriately cautious inference.
**Typical concerns:** "Why should a broad clinical readership care?" "Is the sample or setting too narrow?" "Are the conclusions stronger than the evidence permits?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (medium), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (low), SKEPTIC (medium)

### Revista Clínica Española
**Focus:** Internal medicine, hospital medicine, multimorbidity, diagnostic reasoning, and real-world clinical care for the SEMI community and a broad Spanish-speaking medical audience.
**Bar:** A practical, well-executed paper that informs internists’ decisions; registry studies, pragmatic cohorts, and clinically grounded reviews fit well if the message is clear.
**Domain referee adjusts:** Wants relevance to internal medicine workflow, multimorbidity, diagnostic complexity, inpatient-outpatient coordination, and problems seen in general clinical practice.
**Methods referee adjusts:** Expects solid real-world clinical methods, transparent definitions, reasonable adjustment for case-mix, and statistics that support bedside-facing conclusions without overreach.
**Typical concerns:** "Is this useful to internists rather than a single specialty service?" "Have you handled confounding and heterogeneity adequately?" "Does the paper change practice or only describe experience?"
**Referee pool:** CLINICAL (high), METHODOLOGICAL (medium), EVIDENCE (medium), ETHICAL (medium), STATISTICAL (medium), TRANSLATIONAL (low), SKEPTIC (low)

---

## Custom Journal Template

### [Journal Name]
**Focus:** [Scope and audience]
**Bar:** [What level of contribution is needed]
**Domain referee adjusts:** [What the content referee emphasizes]
**Methods referee adjusts:** [What the methods referee emphasizes]
**Typical concerns:** [Common reviewer questions]
**Referee pool:** CLINICAL (high/medium/low), METHODOLOGICAL (high/medium/low), EVIDENCE (high/medium/low), ETHICAL (high/medium/low), STATISTICAL (high/medium/low), TRANSLATIONAL (high/medium/low), SKEPTIC (high/medium/low)
