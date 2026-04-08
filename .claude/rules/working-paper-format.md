# Medical Manuscript Format Standard

All LaTeX papers generated or reviewed by this system must conform to a medical-manuscript baseline. This rule applies to the writer, writer-critic, and verifier agents.

## Document Class and Layout

- `\documentclass[12pt]{article}`
- Margins: 1 inch all sides
- Body text: `\doublespacing`
- References: `\singlespacing` or `\small`
- Page numbers centered in footer via `fancyhdr`
- Manuscript structure defaults to IMRAD unless the study design clearly requires a different structure

## Reference Preamble

The following preamble is the medical-first default. New papers should use this structure unless the target journal requires a different class file.

```latex
\documentclass[12pt]{article}
\usepackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\usepackage{setspace}
\doublespacing
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0pt}

\usepackage{lmodern}
\usepackage{microtype}
\usepackage[T1]{fontenc}
\usepackage{titlesec}
\usepackage[title]{appendix}
\usepackage{titling}
\usepackage{amssymb, amsmath, amsfonts, mathtools}
\usepackage{amsthm}
\usepackage{array, booktabs, makecell, cellspace}
\usepackage{siunitx}
\usepackage[flushleft]{threeparttable}
\usepackage{rotating, tabularx}
\usepackage{graphicx, subcaption}
\usepackage{pdflscape, tikz}
\usepackage{caption}
\captionsetup{font=small, labelfont=bf, justification=justified}
\usepackage{float}
\usepackage{enumitem}
\usepackage{xurl}
\usepackage{xcolor}

\usepackage[backend=biber,
            style=numeric-comp,
            sorting=none,
            maxbibnames=99,
            giveninits=true,
            doi=true,
            url=true,
            natbib=true]{biblatex}
\addbibresource{references.bib}

\usepackage[hidelinks, breaklinks]{hyperref}
```

## Title Page Format

```latex
\title{Paper Title\thanks{Funding, acknowledgments, or disclosures.}}

\author{
Author One\thanks{Affiliation and email.} \quad
Author Two\thanks{Affiliation and email.}
}

\date{\today}
```

Rules:
- Keep the title page on one page when possible
- Affiliations and emails belong in `\thanks{}` footnotes unless a journal requires another pattern
- Suppress page number on title page with `\thispagestyle{empty}`
- Reset page numbering after title page with `\newpage \setcounter{page}{1}`

## Abstract and Metadata

```latex
\begin{abstract}
\noindent\singlespacing
\textbf{Background:} ...
\textbf{Methods:} ...
\textbf{Results:} ...
\textbf{Conclusions:} ...
\end{abstract}

\vspace{0.5em}
\noindent \textbf{Trial Registration:} ClinicalTrials.gov NCTXXXXXXX

\vspace{0.5em}
\noindent \textbf{MeSH Terms:} Pulmonary Disease, Bronchoscopy, Survival Analysis

\vspace{0.5em}
\noindent \textbf{Keywords:} pulmonary medicine, interventional pulmonology, cohort study

\vspace{0.5em}
\noindent \textbf{Word Count:} 2998
```

Rules:
- Use a structured abstract by default: Background, Methods, Results, Conclusions
- Report the study design in the abstract when possible
- Include registration information when applicable
- MeSH terms replace legacy field codes in this medical-first workflow

## Section Structure

Standard order for most manuscripts:
1. Introduction
2. Methods
3. Results
4. Discussion
5. Conclusion (optional)

Methods should usually include:
- Design and setting
- Participants / data source
- Exposure or intervention
- Outcomes
- Statistical analysis
- Ethics / consent / registration

Results should usually include:
- Participant flow or sample construction
- Baseline characteristics
- Main effect estimates with 95% CI
- Harms / complications when relevant
- Sensitivity or secondary analyses

## Tables and Figures

- Place tables and figures inline unless the journal requires otherwise
- Use `threeparttable` for table notes
- Use `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`) — never `\hline`
- Baseline characteristics should appear as a Table 1-style summary
- Clinical effect tables should favor HR / OR / RR / absolute risk difference with 95% CI
- Survival analyses should usually include a Kaplan-Meier figure with numbers at risk
- Randomized trials should usually include a CONSORT flow diagram

## Additional Required Statements

Most medical manuscripts should include dedicated statements for:
- Ethics approval / IRB / waiver status
- Informed consent or waiver
- Trial or protocol registration
- Funding
- Conflicts of interest
- Data sharing / availability

## Bibliography

```latex
\clearpage
\small \printbibliography
```

- `\printbibliography` replaces `\bibliography{}` / `\bibliographystyle{}`
- Compile with `biber`: `xelatex → biber → xelatex → xelatex`
- Keep the bibliography on a new page

## Compilation

```bash
cd paper && TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
BIBINPUTS=..:$BIBINPUTS biber main
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
TEXINPUTS=preambles:$TEXINPUTS xelatex -interaction=nonstopmode main.tex
```

## What the Writer-Critic Checks

The writer-critic deducts points for:
- Missing structured abstract (-5)
- Missing MeSH terms, registration, or word count when applicable (-3 each)
- Missing ethics / consent / conflicts statement when required (-10)
- Non-IMRAD structure without justification (-5)
- Reporting only p-values without effect estimate and 95% CI (-5)
- Missing harms / complications in interventional work (-8)
- `\hline` instead of `booktabs` rules (-3)
- Undefined references or citations (-15)
- Using `bibtex` instead of `biber` (-3)
- Failing to identify the relevant reporting guideline (-5)
