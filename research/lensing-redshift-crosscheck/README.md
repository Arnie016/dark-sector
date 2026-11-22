# Redshift provenance in overlapping radio-relic lensing samples

This is a cross-paper provenance check, not a new lensing measurement, a correction to published physical separations, or an assessment of an SIDM constraint. The [Finner et al. 2025 weak-lensing study](https://inspirehep.net/files/a376dbb30c4397fffb5a1dd49088860f), Table 1, contains cluster identifiers and redshifts for 29 systems. The [Jee, Park & Lee preprint v2](https://arxiv.org/html/2605.00093v2), Table 2, lists 11 selected double-relic systems. We explicitly cross-walk eight recognizable names in `finner_table1_matches.csv` to the previously checked [gold-sample transcription](../relic-gold-sample-data-check/distances.csv); there is no fuzzy or automatic sky-position matching. These observations and author lists overlap, so they are not independent datasets. The VizieR query for `J/ApJS/277/28` returned “Table or Catalog not found” on 6 November 2026; this does not establish that no other machine-readable release exists. The Finner table values here are an attributed manual transcription.

Four of the eight matched systems have different redshifts at the reported precision:

| System | Finner Table 1 | Jee Table 2 |
| --- | ---: | ---: |
| Abell 2345 | 0.179 | 0.176 |
| CIZA J2242.8+5301 | 0.189 | 0.192 |
| MACS J1752.0+4440 | 0.365 | 0.366 |
| ZwCl 1447.2+2619 | 0.376 | 0.372 |

The data sources, member-selection methods and rounding may differ; the table alone does not identify a correct redshift or demonstrate an error. The original [ZwCl 1447 radio and lensing paper](https://arxiv.org/html/2109.00593) uses 0.376, while Jee et al. list 0.372. Any attempted reassessment needs the authors' underlying angular measurements, member redshifts, lensing fit and their exact choices, rather than blindly replacing a published value.

There is an additional **within-paper ambiguity** for ZwCl 1856.8+6616: Finner et al. Table 1 gives 0.304, but the heading of §4.25 gives 0.334. Their earlier [dedicated lensing analysis](https://arxiv.org/html/2010.02226) uses 0.304, as does Jee Table 2. This evidence favors using 0.304 as the traceable table value for this comparison, but does not prove why the later heading differs or which redshift was used in any particular calculation. Do not infer an error in a published mass or constraint.

## Fixed-angle sensitivity only

For a fixed angular separation, flat Ωm = 0.3, H0 = 70 km/s/Mpc, `physical separation = angle × angular-diameter distance`. In our eight matched table comparisons, swapping Jee's listed redshift for Finner's Table 1 value changes that *hypothetical* physical length by approximately −1.24% to +1.37% for the four differing cases (`crosscheck.csv`). For the separate ZwCl 1856 heading/table comparison, substituting 0.334 for 0.304 changes the same hypothetical length by **+6.57%**. The actual angular separations, exact source cosmologies and redshift choices for each published measurement were not checked, and no published length was remeasured or corrected. The redshift sensitivity is not an uncertainty distribution.

If two distances are both measured as angular separations at the same source redshift and use the same angular-diameter distance, their ratio is unchanged by this common rescaling. That algebra does not guarantee that the published halo and shock measurements share identical redshifts, cosmologies, definitions or covariance; mass estimates, R500 and lensing geometry can have additional redshift dependence. We have not recalculated any SIDM posterior, radio clock, mass, or significance.

Run `python analyze.py` with Astropy, NumPy and matplotlib; it checks exact-name uniqueness, joins the eight explicitly listed identities and regenerates `crosscheck.csv`, `summary.json` and the plot. Both source transcriptions are hashed in the summary. A separate SciPy numerical integral independently verified all eight angular-diameter distance ratios and the heading example. The original angular measurements, data products, potential source selection, and shared systematics remain required for a scientifically defensible comparison. No email was sent.
