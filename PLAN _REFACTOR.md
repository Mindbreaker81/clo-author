# Plan: Adaptar clo-author para Medicina (Neumología)

**Versión:** 2.0
**Fecha:** 2026-04-08
**Status:** REVISADO

---

## Resumen Ejecutivo

Adaptar el framework clo-author (diseñado para ciencias sociales/economía) para investigación médica, específicamente neumología clínica e intervencionista.

**Principio rector:** clo-author ya fue diseñado para ser adaptable a otros campos via `domain-profile.md` y `journal-profiles.md`. La mayoría de agentes, skills, reglas y hooks son domain-agnostic. La adaptación consiste en **configurar el sistema**, no en reescribirlo.

**Alcance real:** ~14 archivos (8 core + 4 secundarios + 2 nuevos), no ~40.
**Tiempo estimado:** ~5-6 horas.
**Uso de subagentes:** Sí (3 paralelos para perfiles de journals).

---

## Diagnóstico: Errores del Plan v1.0

### ERROR 1: Renombrar agentes rompe la arquitectura

El plan v1.0 proponía `librarian → evidence-reviewer`, `coder → biostatistician`, etc. Esto rompe el orchestrator, los skills, las reglas de workflow, los pares worker-critic, y el sistema de logging -- todos referencian agentes por nombre funcional.

**Corrección:** NO renombrar agentes. Modificar los **prompts internos** de cada agente para calibrar al contexto médico. Los agentes ya leen `domain-profile.md` para auto-calibrarse -- ese es el mecanismo de adaptación previsto.

### ERROR 2: Migrar de LaTeX a Word/HTML es inviable como fase inicial

Toda la pipeline (compilation, working-paper-format, content-standards, writer, writer-critic, verifier) está construida sobre XeLaTeX. Migrar requiere reescribir ~6 archivos core.

**Corrección:** Mantener LaTeX como base. Adaptar `working-paper-format.md` a formato IMRAD médico (dentro de LaTeX). Agregar export a Word via `pandoc` como fase futura opcional.

### ERROR 3: Ponderaciones de quality gates incorrectas

El plan v1.0 reduce Paper quality de 25% → 10%. En medicina, la adherencia a reporting guidelines (CONSORT, STROBE, abstract estructurado, IMRAD) es **criterio de rechazo inmediato**. Los reviewers verifican esto antes de leer el contenido.

**Corrección:** Ver ponderaciones revisadas en Fase 4.

### ERROR 4: Alcance sobredimensionado

El plan proponía modificar ~40 archivos. El `meta-governance.md` del repo establece que las diferencias de campo se manejan via los archivos de configuración.

**Corrección:** El núcleo de la adaptación son 8 archivos. El resto son ajustes menores o no necesitan cambios.

---

## Diagnóstico: Elementos Críticos Faltantes en v1.0

### FALTANTE 1: Guías de reporte médico (EQUATOR Network)

El plan v1.0 solo menciona CONSORT. La investigación médica exige un ecosistema completo:

| Guía | Tipo de estudio | Obligatoriedad |
|------|-----------------|----------------|
| CONSORT | RCTs | Obligatorio |
| STROBE | Observacionales (cohorte, caso-control, transversal) | Obligatorio |
| PRISMA | Systematic reviews y meta-análisis | Obligatorio |
| STARD | Estudios de precisión diagnóstica | Obligatorio |
| SPIRIT | Protocolos de ensayos clínicos | Recomendado |
| ARRIVE | Investigación animal | Si aplica |
| CARE | Case reports | Si aplica |
| TRIPOD | Modelos de predicción | Si aplica |

Debe integrarse en: content-standards.md, writer agent, writer-critic, review skill.

### FALTANTE 2: Ética e IRB

Completamente ausente. En medicina, **ningún** estudio con pacientes avanza sin aprobación ética. Debe incluirse:
- Sección en domain-profile.md sobre requerimientos éticos
- Quality gate: verificación de mención de IRB/comité de ética en el manuscrito
- Checklist de ethical compliance en review skill

### FALTANTE 3: Registro de estudios clínicos

El plan no menciona ClinicalTrials.gov / ISRCTN / WHO ICTRP / EudraCT. Debe integrarse en:
- `/strategize pap` → modo de registro clínico (no solo AEA/OSF/EGAP)
- Sección en domain-profile.md
- Verificación en quality gates

### FALTANTE 4: Formatos de tablas y figuras médicas

El `content-standards.md` actual está calibrado para economía (coeficientes OLS, standard errors, stars). Medicina necesita:
- **Tablas:** Hazard ratios (HR) con IC 95%, odds ratios (OR), risk ratios (RR), NNT
- **Figuras:** Curvas Kaplan-Meier, forest plots, CONSORT flow diagrams, funnel plots
- **Abstract estructurado:** Background, Methods, Results, Conclusions
- **MeSH Terms** en lugar de JEL Codes

### FALTANTE 5: Referee dispositions incompletas

El plan v1.0 propone 6 dispositions pero faltan dos críticas para medicina:

| Disposition | Prior intelectual |
|-------------|-------------------|
| ETHICAL | Consentimiento, seguridad del paciente, conflictos de interés, data safety monitoring board |
| STATISTICAL | Bioestadístico puro: tamaño de muestra, poder, supervivencia, riesgos competitivos, múltiples comparaciones |

El mapping desde economía: CREDIBILITY → METHODOLOGICAL es correcto, pero STRUCTURAL no aplica en medicina (eliminar).

---

## Partes Buenas a Mantener del v1.0

- Selección de journals médicos y estructura de subagentes paralelos
- Domain profile para neumología (fuentes de datos, outcomes, guías)
- Concepto de dispositions de referees (con las correcciones)
- Formato IMRAD para secciones del paper
- Búsqueda via PubMed + MeSH terms para `/discover lit`
- Skill nuevo `systematic-review`

---

## Plan Revisado

### Fase 1: Configuración Base (30 min)

#### 1.1: Rellenar CLAUDE.md (10 min)

Reemplazar placeholders con datos del proyecto médico:
- **Project:** [nombre del proyecto de neumología]
- **Institution:** [hospital/universidad]
- **Field:** Pulmonary Medicine / Interventional Pulmonology
- Mantener comandos XeLaTeX sin cambios
- Mantener quality thresholds 80/90/95

#### 1.2: Llenar domain-profile.md para neumología (20 min)

Contenido a completar en `.claude/references/domain-profile.md`:

**Field:**
- Primary: Pulmonary Medicine / Interventional Pulmonology
- Adjacent: Critical Care, Thoracic Surgery, Oncology, Radiology

**Target Journals:** (ver lista completa en Fase 3)

**Common Data Sources:**

| Dataset | Tipo | Acceso | Notas |
|---------|------|--------|-------|
| PubMed/MEDLINE | Bibliográfico | Público | Búsqueda via MeSH terms |
| ClinicalTrials.gov | Registro de ensayos | Público | Ensayos registrados, resultados |
| EHR/HCE institucional | Datos clínicos | Restringido | Requiere IRB, anonimización |
| SEER (NCI) | Registro de cáncer | Público/Restringido | Supervivencia, estadificación |
| NHANES | Encuesta poblacional | Público | Espirometría, función pulmonar |
| BOLD Study | Epidemiológico EPOC | Restringido | Prevalencia internacional |
| COPDGene | Cohorte EPOC | Restringido | Genómica, CT, función pulmonar |
| UK Biobank | Cohorte poblacional | Restringido | Espirometría, imaging, genómica |

**Common Study Designs:**

| Diseño | Aplicación típica | Supuesto clave a defender |
|--------|-------------------|--------------------------|
| RCT | Nuevos tratamientos, procedimientos | Randomización, cegamiento, CONSORT compliance |
| Cohorte prospectiva | Historia natural, factores pronósticos | Seguimiento completo, control de confusión |
| Caso-control | Factores de riesgo de enfermedades raras | Selección apropiada de controles |
| Transversal | Prevalencia, asociaciones | No causalidad, sesgo de supervivencia |
| Systematic review / Meta-análisis | Síntesis de evidencia | Búsqueda exhaustiva, PRISMA compliance |
| Estudio diagnóstico | Precisión de tests | STARD compliance, espectro de enfermedad |

**Outcomes comunes en neumología:**
- Supervivencia (overall, disease-free, progression-free)
- FEV1, FVC, FEV1/FVC, DLCO (función pulmonar)
- 6MWD (capacidad de ejercicio)
- Escalas: mMRC, CAT, SGRQ (calidad de vida)
- Hospitalizaciones, exacerbaciones
- Complicaciones procedimentales (neumotórax, sangrado)
- Éxito técnico y clínico de procedimientos

**Guías clínicas relevantes:**
- GOLD (EPOC)
- GINA (Asma)
- ATS/ERS (función pulmonar, broncoscopia, ILD)
- NCCN (cáncer de pulmón)
- BTS (guías británicas)
- SEPAR (guías españolas)

**Requerimientos éticos:**
- Aprobación IRB/Comité de Ética obligatoria para estudios con pacientes
- Consentimiento informado documentado
- Registro en ClinicalTrials.gov obligatorio para RCTs (ICMJE requirement)
- Data Safety Monitoring Board para ensayos con endpoints de seguridad
- Declaración de conflictos de interés (ICMJE form)
- Cumplimiento GDPR/LOPD para datos de pacientes europeos

**Field Conventions:**
- Resultados de supervivencia → Kaplan-Meier + log-rank + Cox regression
- Outcomes binarios → OR/RR con IC 95%, no p-values aislados
- Siempre reportar NNT/NNH cuando sea clínicamente relevante
- Significancia clínica > significancia estadística
- Abstract estructurado obligatorio (Background, Methods, Results, Conclusions)
- Word count limits estrictos según journal
- MeSH Terms en lugar de JEL Codes

**Seminal References:**

| Paper | Por qué importa |
|-------|-----------------|
| GOLD Report (actualización anual) | Clasificación y manejo de EPOC |
| NELSON Trial (de Koning et al., NEJM 2020) | Screening CT cáncer de pulmón |
| NLST (National Lung Screening Trial, NEJM 2011) | Screening CT vs radiografía |
| TORCH (Calverley et al., NEJM 2007) | Salmeterol/fluticasona en EPOC |
| UPLIFT (Tashkin et al., NEJM 2008) | Tiotropio en EPOC |
| IMPACT (Lipson et al., NEJM 2018) | Triple terapia en EPOC |
| LIBERATE (Criner et al., AJRCCM 2018) | Válvulas endobronquiales |
| VENT (Sciurba et al., NEJM 2010) | Válvulas endobronquiales en enfisema |

---

### Fase 2: Perfiles de Journals Médicos (2-2.5h con subagentes)

Estrategia: 3 subagentes paralelos. Formato idéntico al existente en `journal-profiles.md`.

#### 2.1: Subagente 1 -- Top Tier / Medicina General (30 min)

Crear perfiles para:
- **New England Journal of Medicine (NEJM)**
- **The Lancet**
- **JAMA (Journal of the American Medical Association)**
- **BMJ (British Medical Journal)**
- **Annals of Internal Medicine**

#### 2.2: Subagente 2 -- Revistas de Medicina Respiratoria Internacional (30 min)

Crear perfiles para:
- **American Journal of Respiratory and Critical Care Medicine (AJRCCM)** -- Blue Journal, top en neumología
- **Lancet Respiratory Medicine** -- Alto impacto, respiratory specialty del Lancet
- **European Respiratory Journal (ERJ)** -- Journal oficial de la ERS
- **Thorax** -- BMJ group, fuerte en UK/Europa
- **Chest** -- Journal oficial del ACCP
- **Respiratory Medicine** -- Amplio scope respiratorio
- **Respiration** -- European scope, procedimientos
- **ERJ Open Research** -- Open access de la ERS
- **BMC Pulmonary Medicine** -- Open access, scope amplio

#### 2.3: Subagente 3 -- Revistas Intervencionistas + Revistas Españolas (30 min)

**Intervencionistas:**
- **Journal of Bronchology and Interventional Pulmonology** -- Nicho intervencionista
- **Journal of Thoracic Oncology (JTO)** -- Oncología torácica
- **Radiology** -- Imaging torácico, procedimientos guiados por imagen
- **Journal of Vascular and Interventional Radiology (JVIR)** -- Procedimientos intervencionistas

**Revistas españolas y de ámbito hispanohablante:**
- **Archivos de Bronconeumología** -- Journal oficial de SEPAR, indexada en JCR, bilingüe (español/inglés), principal revista respiratoria en español
- **Revista de Patología Respiratoria** -- SEPAR, revisiones y casos clínicos
- **Open Respiratory Archives** -- Open access de SEPAR (antes Revista Española de Patología Torácica)
- **Medicina Clínica** -- Medicina general española, acepta neumología, Elsevier
- **Revista Clínica Española** -- SEMI, scope general pero con secciones respiratorias

#### 2.4: Formato de perfil (idéntico al existente)

```markdown
### [Nombre del Journal] ([Abreviatura])
**Focus:** [Scope y audiencia]
**Bar:** [Qué nivel de paper acepta]
**Domain referee adjusts:** [Qué busca el referee de contenido]
**Methods referee adjusts:** [Qué busca el referee de métodos]
**Typical concerns:** [Preguntas frecuentes de referees]
**Referee pool:** CLINICAL (X), METHODOLOGICAL (X), EVIDENCE (X), ETHICAL (X), STATISTICAL (X), TRANSLATIONAL (X), SKEPTIC (X)
```

#### 2.5: Consolidación (15 min)

- Unificar outputs de los 3 subagentes en `.claude/references/journal-profiles.md`
- Agregar bajo una nueva sección `## Medicine` (después de `## Economics`)
- Mantener la sección "How This Works" existente
- Verificar consistencia de formato

---

### Fase 3: Adaptar Reglas de Formato y Contenido (1h)

#### 3.1: Adaptar working-paper-format.md a IMRAD médico (30 min)

Cambios:
- Section Structure → IMRAD: Introduction, Methods, Results, Discussion (+ Conclusion opcional)
- Abstract → estructurado con subsecciones (Background, Methods, Results, Conclusions)
- Reemplazar "JEL Codes" por "MeSH Terms"
- Reemplazar "Keywords" → mantener (también se usa en medicina)
- Agregar: Trial Registration number (si aplica)
- Agregar: Word count (requisito de la mayoría de journals médicos)
- Agregar: "What this study adds" box (requerido por BMJ, Thorax, etc.)
- Mantener preamble LaTeX existente (funciona igual)
- Writer-critic checks: agregar verificación de IMRAD, abstract estructurado, MeSH terms

#### 3.2: Agregar estándares médicos a content-standards.md (30 min)

Agregar sección "Medical Table Standards":

**Tabla de resultados clínicos (HR/OR/RR):**
```
\toprule
Variable        & HR    & 95\% CI       & p-value \\
\midrule
Treatment       & 0.72  & (0.58--0.89)  & 0.003   \\
Age (per year)  & 1.02  & (1.01--1.03)  & 0.001   \\
Male sex        & 1.15  & (0.92--1.44)  & 0.22    \\
\bottomrule
```

**Tabla baseline characteristics:**
```
\toprule
Characteristic       & Treatment (n=XX) & Control (n=XX) & p-value \\
\midrule
Age, years (mean±SD) & 65.2 ± 8.1       & 64.8 ± 7.9     & 0.45    \\
Male, n (\%)         & 120 (60.0)        & 118 (59.0)      & 0.84    \\
FEV1, \% pred        & 42.3 ± 12.1       & 43.1 ± 11.8     & 0.52    \\
\bottomrule
```

**Figuras médicas:**
- Kaplan-Meier: `survminer::ggsurvplot()` con number at risk table
- Forest plot: `forestplot` package o `meta::forest()`
- CONSORT flow diagram: `consort` package en R o TikZ
- Funnel plot: `meta::funnel()`

**Paquetes R recomendados:**
- `survival` + `survminer` (análisis de supervivencia)
- `meta` + `metafor` (meta-análisis)
- `tableone` (baseline characteristics)
- `gtsummary` (tablas clínicas publicables)
- `consort` (diagramas CONSORT)
- `forestplot` (forest plots)

---

### Fase 4: Quality Gates Adaptados (20 min)

#### 4.1: Ponderaciones para medicina

Ajustar en `.claude/rules/quality.md`:

| Componente | Peso Economía | Peso Medicina | Justificación |
|------------|---------------|---------------|---------------|
| Literature coverage | 10% | 15% | Systematic reviews más importantes, pero no todo es SR |
| Data quality | 10% | 15% | Datos clínicos requieren alta calidad, compliance regulatorio |
| Study design validity | 25% | 25% | Mantener -- diseño es igualmente crítico |
| Code quality | 15% | 10% | Menos peso relativo; el código es medio, no fin |
| Paper quality | 25% | 25% | **MANTENER** -- adherencia a CONSORT/STROBE es criterio de rechazo |
| Manuscript polish | 10% | 5% | Reducir ligeramente |
| Replication readiness | 5% | 5% | Mantener |

#### 4.2: Métricas específicas de medicina

Agregar al checklist del quality gate:
- Reporting guideline compliance (CONSORT/STROBE/PRISMA según tipo de estudio)
- Sample size / power calculation justification
- Clinical significance vs statistical significance (discusión explícita)
- Adverse events reporting (obligatorio en estudios intervencionistas)
- Conflict of interest disclosure
- IRB/Ethics committee approval statement
- Trial registration number (si aplica)
- Structured abstract compliance

---

### Fase 5: Adaptar Agentes Clave (45 min)

**IMPORTANTE:** NO renombrar archivos. Solo modificar prompts internos.

#### 5.1: editor.md -- Agregar dispositions médicas (20 min)

Agregar a la tabla de Referee Dispositions:

| ID | Disposition | Prior intelectual |
|----|-------------|-------------------|
| CLINICAL | Clinical Relevance | "¿Cambia esto la práctica clínica? ¿Cuál es el impacto en el paciente?" |
| METHODOLOGICAL | Methodological Rigor | "¿El diseño es apropiado? ¿CONSORT/STROBE compliance?" |
| EVIDENCE | Evidence Strength | "¿Cuál es el nivel de evidencia (GRADE)? ¿Systematic review disponible?" |
| ETHICAL | Ethics & Safety | "¿IRB aprobado? ¿Consentimiento? ¿DSMB? ¿Conflictos de interés?" |
| STATISTICAL | Biostatistics | "¿Poder estadístico? ¿Análisis de supervivencia correcto? ¿Múltiples comparaciones?" |
| TRANSLATIONAL | Bench to Bedside | "¿De la investigación básica a la aplicación clínica? ¿Mecanismo?" |
| SKEPTIC | Professional Skeptic | "¿El resultado es probablemente artefacto? Muéstrame los fallos." |

Eliminar STRUCTURAL (no aplica en medicina).

Agregar **pet peeves médicos** (critical pool):
- "Exige diagrama CONSORT en todo RCT"
- "Verifica que el cálculo de tamaño de muestra sea pre-especificado"
- "Demanda ITT analysis como análisis primario"
- "Quiere ver number needed to treat, no solo p-values"
- "Exige curvas Kaplan-Meier con número en riesgo"
- "Sospecha de resultados subgrupo no pre-especificados"
- "Demanda reporte completo de adverse events"
- "Verifica que los endpoints sean clinically meaningful"
- "Exige disclosure de conflictos de interés de TODOS los autores"
- "Quiere ver análisis de sensibilidad para missing data"
- "Demanda adherencia completa a la guía de reporte correspondiente"
- "Verifica registro previo del ensayo en ClinicalTrials.gov"

Agregar pet peeves médicos (constructive pool):
- "Valora análisis de significancia clínica además de estadística"
- "Aprecia patient-centered outcomes"
- "Da crédito por diseño pragmático que refleja práctica real"
- "Valora transparencia en limitaciones y data sharing"
- "Aprecia pre-registro y adherencia al protocolo"
- "Valora reporte de adverse events aunque sean negativos"
- "Da crédito por incluir perspectiva del paciente"
- "Aprecia análisis de cost-effectiveness junto con eficacia"

#### 5.2: domain-referee.md -- Calibrar a reporting guidelines (15 min)

Agregar instrucción para leer `reporting-guidelines.md` y verificar adherencia según tipo de estudio. Agregar checklist de clinical relevance assessment.

#### 5.3: methods-referee.md -- Calibrar a bioestadística clínica (10 min)

Agregar conocimiento de: análisis de supervivencia (Cox, Kaplan-Meier), mixed models para medidas repetidas, análisis de non-inferiority/equivalence, competing risks, propensity score methods en observacionales.

---

### Fase 6: Adaptar Skills Clave (45 min)

Solo los skills que requieren cambios sustantivos:

#### 6.1: discover/SKILL.md -- Agregar PubMed/MeSH (15 min)

En modo `/discover lit`:
- Reemplazar "top-5 generals (AER, Econometrica...)" → PubMed/MEDLINE, Cochrane Library
- Agregar búsqueda con MeSH terms
- Agregar Cochrane Database of Systematic Reviews
- Agregar ClinicalTrials.gov para ensayos en curso
- Mantener citation chains (funciona igual)
- Proximity scores: mantener escala 1-5

#### 6.2: strategize/SKILL.md -- Agregar PAP clínico (15 min)

En modo `/strategize pap`:
- Agregar plataformas de registro: ClinicalTrials.gov, ISRCTN, EudraCT, WHO ICTRP
- Agregar template SPIRIT para protocolos
- Agregar sección de DSMB/seguridad
- Agregar análisis de non-inferiority/equivalence margin justification
- Mantener secciones PAP existentes (power, outcomes, subgroups)

#### 6.3: review/SKILL.md -- Agregar modo reporting guidelines (10 min)

Agregar flag `--reporting [guideline]`:
- `--reporting consort` → checklist CONSORT para RCTs
- `--reporting strobe` → checklist STROBE para observacionales
- `--reporting prisma` → checklist PRISMA para SR/MA
- `--reporting stard` → checklist STARD para diagnósticos
- Auto-detectar tipo de estudio si no se especifica

#### 6.4: Crear systematic-review/SKILL.md -- Skill nuevo (5 min)

Workflow: PubMed search strategy → MeSH terms → Screening → Data extraction → Meta-analysis → PRISMA diagram.
Output: Protocolo PRISMA-P + búsqueda documentada + PRISMA flow diagram.

---

### Fase 7: Crear Archivo de Reporting Guidelines (30 min)

Crear `.claude/references/reporting-guidelines.md` con checklists resumidas de:
- CONSORT 2010 (25 items)
- STROBE (22 items)
- PRISMA 2020 (27 items)
- STARD 2015 (30 items)

Cada checklist con: item number, sección del paper donde va, descripción breve.

---

### Fase 8: Verificación Final (15 min)

#### 8.1: Checklist de archivos

**Archivos modificados (core):**
- [ ] `CLAUDE.md` -- placeholders rellenados
- [ ] `.claude/references/domain-profile.md` -- neumología completo
- [ ] `.claude/references/journal-profiles.md` -- sección Medicine con ~23 journals
- [ ] `.claude/rules/working-paper-format.md` -- IMRAD + abstract estructurado
- [ ] `.claude/rules/content-standards.md` -- tablas/figuras médicas agregadas
- [ ] `.claude/agents/editor.md` -- dispositions + pet peeves médicos
- [ ] `.claude/agents/domain-referee.md` -- calibrado a reporting guidelines
- [ ] `.claude/agents/methods-referee.md` -- calibrado a bioestadística

**Archivos modificados (secundarios):**
- [ ] `.claude/skills/discover/SKILL.md` -- PubMed/MeSH
- [ ] `.claude/skills/strategize/SKILL.md` -- PAP clínico
- [ ] `.claude/skills/review/SKILL.md` -- modo reporting guidelines
- [ ] `.claude/rules/quality.md` -- ponderaciones medicina

**Archivos nuevos:**
- [ ] `.claude/references/reporting-guidelines.md` -- CONSORT/STROBE/PRISMA/STARD
- [ ] `.claude/skills/systematic-review/SKILL.md` -- SR/meta-análisis

#### 8.2: Archivos que NO se modifican

- Agentes: librarian, explorer, strategist, coder, writer, storyteller (y sus critics) -- se calibran via domain-profile
- `.claude/rules/workflow.md` -- totalmente genérico
- `.claude/rules/agents.md` -- totalmente genérico
- `.claude/rules/logging.md` -- totalmente genérico
- `.claude/rules/meta-governance.md` -- totalmente genérico
- `.claude/rules/revision.md` -- totalmente genérico
- `.claude/hooks/*` -- totalmente genéricos
- `templates/*` -- totalmente genéricos
- Estructura de directorios -- se mantiene idéntica

#### 8.3: Test de integración

- Verificar que `CLAUDE.md` se lea correctamente
- Verificar que journal-profiles.md tenga formato consistente
- Verificar que domain-profile.md esté completo
- Compilar un paper de prueba con formato IMRAD

---

## Journals Médicos Completos (23 perfiles)

### Tier 1 -- Medicina General (5)

| Journal | IF aprox. | Scope |
|---------|-----------|-------|
| New England Journal of Medicine (NEJM) | ~170 | Medicina general, máximo impacto |
| The Lancet | ~170 | Medicina general, salud global |
| JAMA | ~120 | Medicina general, salud pública |
| BMJ | ~105 | Medicina general, fuerte en UK/Europa |
| Annals of Internal Medicine | ~50 | Medicina interna, guidelines |

### Tier 2 -- Respiratorio Internacional (9)

| Journal | IF aprox. | Scope |
|---------|-----------|-------|
| American Journal of Respiratory and Critical Care Medicine (AJRCCM) | ~30 | Top neumología, ATS journal |
| Lancet Respiratory Medicine | ~45 | Respiratory del Lancet, alto impacto |
| European Respiratory Journal (ERJ) | ~25 | ERS journal, Europa |
| Thorax | ~12 | BMJ group, UK/Europa |
| Chest | ~10 | ACCP journal, amplio scope |
| Respiratory Medicine | ~4 | Scope amplio respiratorio |
| Respiration | ~3 | European scope, procedimientos |
| ERJ Open Research | ~5 | Open access ERS |
| BMC Pulmonary Medicine | ~3 | Open access, scope amplio |

### Tier 3 -- Intervencionista / Oncología Torácica (4)

| Journal | IF aprox. | Scope |
|---------|-----------|-------|
| Journal of Thoracic Oncology (JTO) | ~20 | Oncología torácica |
| Journal of Bronchology and Interventional Pulmonology | ~2 | Nicho intervencionista |
| Radiology | ~20 | Imaging, procedimientos guiados |
| Journal of Vascular and Interventional Radiology (JVIR) | ~4 | Intervencionismo |

### Tier 4 -- Revistas Españolas e Hispanohablantes (5)

| Journal | IF aprox. | Scope | Idioma |
|---------|-----------|-------|--------|
| Archivos de Bronconeumología | ~9 | Principal respiratoria en español, SEPAR, JCR | ES/EN |
| Open Respiratory Archives | ~2 | Open access SEPAR | ES/EN |
| Revista de Patología Respiratoria | -- | Revisiones y casos, SEPAR | ES |
| Medicina Clínica | ~2 | General española, acepta neumología | ES/EN |
| Revista Clínica Española | ~2 | SEMI, secciones respiratorias | ES/EN |

---

## Referee Dispositions para Medicina (7)

| ID | Disposition | Prior Intelectual |
|----|-------------|-------------------|
| CLINICAL | Clinical Relevance | Impacto en la práctica clínica y en el paciente |
| METHODOLOGICAL | Methodological Rigor | Diseño del estudio, compliance con reporting guidelines |
| EVIDENCE | Evidence Strength | Nivel de evidencia GRADE, systematic reviews |
| ETHICAL | Ethics & Safety | IRB, consentimiento, DSMB, conflictos de interés |
| STATISTICAL | Biostatistics | Poder, análisis de supervivencia, múltiples comparaciones |
| TRANSLATIONAL | Bench to Bedside | Mecanismo, aplicación de básica a clínica |
| SKEPTIC | Professional Skeptic | El resultado es probablemente artefacto |

---

## Timeline Resumen

| Fase | Descripción | Tiempo |
|------|-------------|--------|
| Fase 1 | Configuración base (CLAUDE.md + domain-profile.md) | 30 min |
| Fase 2 | Perfiles de journals (3 subagentes paralelos) | 45 min |
| Fase 3 | Formato y contenido (working-paper-format + content-standards) | 1h |
| Fase 4 | Quality gates | 20 min |
| Fase 5 | Agentes (editor, referees) | 45 min |
| Fase 6 | Skills (discover, strategize, review, systematic-review) | 45 min |
| Fase 7 | Reporting guidelines reference | 30 min |
| Fase 8 | Verificación final | 15 min |
| | **Total** | **~5-6h** |

---

## Riesgos y Mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Perfiles de journals pueden no reflejar cultura de revisión actual | Verificar con publicaciones recientes y autor guidelines de cada journal |
| Reporting guidelines se actualizan (CONSORT 2025, PRISMA 2020) | Documentar versión usada, revisión periódica |
| LaTeX no es estándar en todos los journals médicos | Mantener LaTeX como base, agregar export pandoc como fase futura |
| Calibración de dispositions requiere experiencia real en peer review médico | Iterar basado en feedback de uso con proyectos reales |

---

## Filosofía de la Adaptación

El plan v1.0 trataba la adaptación como "reescribir todo". El plan v2.0 trata la adaptación como "configurar el sistema que ya está diseñado para ser configurado". Esto es más rápido, menos propenso a errores, y mantiene compatibilidad con futuras actualizaciones del clo-author base.

Los agentes (`librarian`, `coder`, `strategist`, `writer`, `editor`) son **roles funcionales** genéricos. No necesitan renombrarse -- necesitan contexto médico, que obtienen leyendo `domain-profile.md`. Este es el mecanismo de adaptación que el framework ya provee.