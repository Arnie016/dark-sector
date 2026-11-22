# Merger-clock paper candidate: three-source comparison

Research synthesis, 7 November 2026. This is a literature-grounded study design, not a new result, a reanalysis of the observational data, or a journal-ready manuscript. Statements below are attributed to the respective papers and remain conditional on their methods and assumptions.

## Existing results and overlap

1. [Lee et al., double-radio-relic statistics, arXiv:2510.21632](https://arxiv.org/html/2510.21632) describe simulations in TNG-Cluster and TNG300. They report an empirical time-since-collision relation with double relic separation normalized by R500c, with approximately 0.2 Gyr accuracy for their studied sample. They also discuss projection, off-axis geometry, detection thresholds and ambiguous relic/event associations. Their merger catalog description uses a quadratic fit to separation. This already covers the basic claim that radio-relic separation can be a merger clock.
2. [Jee, Park & Lee, arXiv:2605.00093v2](https://arxiv.org/html/2605.00093) use 576 idealized simulations, 20 off-grid tests, mock validation, an 11-system observed gold sample and 15 TNG-Cluster analogs. The authors report a 95% upper limit of 0.63 cm²/g under their forward model and priors. That is **their preprint's conditional result**, not a measurement or reproduction by this project. They discuss projection, mass, impact parameter, collision speed, phase and concentration systematics. Their gold selection requires weak-lensing bimodality and double relic morphology. A claim of a novel radio-relic SIDM clock without engaging this study would be untenable.
3. [TNGC-SIDM I, arXiv:2610.18957](https://arxiv.org/html/2610.18957) presents matched CDM/SIDM re-simulations for two target systems and reports similar shock-separation evolution but model- and merger-dependent halo evolution. The authors emphasize sample selection and discuss baryonic drag and different minor-merger behavior. This is a limited set of simulations, not an independent observational validation of every assumption in the idealized inference. Their data availability statement says publication-related data are available on reasonable request and a public suite release is planned; we have not verified that a later release exists. Do not claim this project has those SIDM data.

## Relevance of our catalog audit

Our corrected TNG-Cluster merger catalog is a CDM simulation catalog, not the matched TNGC-SIDM data or the 11 observed weak-lensing/radio measurements. We found an unresolved numerical relationship between released `d_peri` values and nearby proper-scaled separations; catalog documentation labels `d_peri` ckpc/h, and source construction has not been independently confirmed. The existence of that ambiguity does **not** demonstrate that the published TSC-relic calibration or SIDM limits are incorrect: those studies may use different pipeline inputs and definitions. No quantitative effect on either paper has been measured.

## Narrow testable candidate

A defensible candidate is a **measurement-pipeline robustness study**, not a new SIDM limit: quantify how competing, source-verified pericenter/time definitions and halo/relic matching choices shift an already published TSC calibration or its held-out mock predictions. Predefine (a) the exact simulation and catalog versions, (b) a matched set of independently traced event/halo/relic IDs and sightlines, (c) a benchmark statistic and source code, (d) selection and missingness, and (e) comparison metrics and held-out cases. First reproduce one paper's baseline; then perturb one definition at a time. Report clock shifts and confidence/selection limitations before considering any inference effect. The two-target TNGC-SIDM suite would support only a limited matched-model stress test, not population-wide generalization.

## Required inputs and blockers

- Corrected TNG-Cluster merger catalog and documented event-to-halo links; verify `d_peri`, `T_coll`, time and length conventions before using them.
- Publicly accessible, versioned shock/relic positions and radio maps with snapshot and projection IDs, and their selection recipe; verify access and licensing before downloading. A list of 3D orbits alone cannot reconstruct radio relics.
- For observation comparison, per-system weak-lensing mass/centroid data, radio-relic positions, covariance and angular-to-physical distance assumptions, plus the precise gold selection. The cited preprint has a table but its full inference inputs and likelihood code have not been validated locally.
- Matched SIDM/CDM initial conditions and data provenance; the TNGC-SIDM paper says data are on request and a future public release is planned. No request may be sent without the user's explicit approval.
- Source code or author clarification for catalog timing and distance fields; verify whether the prior question draft still reflects the exact release and evidence before sending.

## Promotion gate

A data-quality or methodology note may be versioned as research, but a journal manuscript requires a frozen question, a matched and documented sample, baseline reproduction, independent computational verifier, uncertainty and sensitivity analysis, a scoped novelty review, citations and reproducibility. This project has not yet met those conditions. Journal submissions and emails require explicit approval.
