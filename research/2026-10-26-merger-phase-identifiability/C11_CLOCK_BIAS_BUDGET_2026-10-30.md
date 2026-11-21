# C-11 | A non-identical radio shock clock can still discriminate under stated bounds

**30 October 2026 | C11-C1 DERIVED (conditional), C11-C2 SOURCE-ANCHORED SIMULATION_RESULT, C11-C3 DATA_INSUFFICIENT.** No observational SIDM fit, novelty claim or new particle result.

## Physical question and source

A radio-relic separation is *not* mathematically invariant to SIDM. Yet its small mismatches may have little effect on the inferred halo separation because the halo separation evolves more slowly. We inspected Section 4.1, Figures 11-13, and Sections 5.1/5.2 of **W. Lee et al., [TNGC-SIDM I](https://arxiv.org/html/2610.18957v1), arXiv:2610.18957v1, 13 October 2026 (preprint)** on 30 October. This study uses **two independent selected cluster mergers**, with matched CDM/SIDM simulations. The following values concern only the **massive M9 merger**, comparing collisionless DM with velocity-independent SIDM at **sigma_T/m_chi = 1 cm²/g**. The source also reports different outcomes in the lower-mass case and resolution dependence. Simulation data were offered on reasonable request, not publicly released in the paper's data-availability statement.

The paper gives an approximate **200-kpc mismatch in relic-to-relic separation** between M9 models. When translated to the predicted halo separation at fixed relic separation, this changes the halo comparison by approximately **4 kpc at 2 R500c** or **35 kpc at 3 R500c**. The corresponding SIDM/CDM halo contrasts at those states are approximately **100 kpc and 200 kpc**, respectively. These are **SIMULATED, rounded, source-reported** quantities, not observed values or an independent re-run of the astrophysical simulations.

The authors explicitly report an early-phase relic expansion speed difference of about 20% and a later-phase difference of about 6%. Thus 'shock independent of dark matter physics' is an approximation, not an exact invariance; the smaller induced *halo* prediction shift is the consequential quantity. They also caution about projection-angle selection, merger phase, minor mergers and simulation resolution.

## One reproducible analytical bound

Let D be a predicted SIDM/CDM halo-separation contrast at fixed relic separation, in kpc. Let b be a model/clock-induced shift, and **condition** on an uncertainty class |b| <= B. By the reverse triangle inequality,

|D+b| >= max(0, D-B).

For illustrative independent Gaussian halo-distance error sigma_H, define a **nominal scale comparison** z_min = max(0,D-B)/sigma_H. This is **not a real observational likelihood or significance**, since B here is a single source-reported model difference, **not a validated bound for all halos or astrophysical uncertainties**. A nominal z_* threshold within this restrictive model requires sigma_H <= (D-B)/z_* when D>B.

A source-anchored finite transfer factor, |Delta H_clock|/|Delta S|, gives **4/200 = 0.020** at 2 R500c and **35/200 = 0.175** at 3 R500c. These are finite ratios between rounded quantities, *not universal derivatives*. Relative clock-to-signal ratios are **4%** and **17.5%**.

| Approximate M9 location | D, kpc | B, kpc | Conditional D-B, kpc | Nominal margin / 100-kpc error | Max sigma_H for nominal 3-sigma |
|---|---:|---:|---:|---:|---:|
| 2 R500c | ~100 | ~4 | ~96 | 0.96 | ~32 kpc |
| 3 R500c | ~200 | ~35 | ~165 | 1.65 | ~55 kpc |

The 100-kpc error is a **typical scale quoted by the source** for specified ground-based lensing conditions, not a measured uncertainty for this M9 example. The 3-sigma column is an **illustrative instrument/design precision target**, not a detection claim. No Gaussian distribution is assumed for the bounded model shift. Combining it in quadrature as if it were independent random noise would be unjustified. The additional astrophysical errors may be larger.

## Verdict, null and next gate

**C11-C1 DERIVED (conditional):** for |b|<=B, the contrast floor is max(0,D-B). **C11-C2 SIMULATION_RESULT (source-anchored arithmetic):** the rounded M9 example yields 96/165 kpc conditional margins. This arithmetic is new to our notebook, not new physics or independent simulation replication. **C11-C3 DATA_INSUFFICIENT:** B is not a calibrated error bound and the source provides only two independent example halos, no general population distribution.

The strongest conventional explanation is ordinary merger geometry, prior mass assembly, gas physics or selection. Those can shift the halo/relic relation without dark scattering. A matched *independent-halo* residual distribution with B >= D at the relevant cross-section would destroy the conditional guarantee.

**Next test:** obtain angle-resolved matched CDM/SIDM separation trajectories and observational selection/likelihood inputs, then quantify B from held-out independent initial conditions. The source's suggestion is to focus on major double-relic mergers beyond about 2 R500c, before second pericenter. Do **not** extrapolate the sigma/m=1 illustration linearly to the Jee et al. observed upper limit of 0.22 cm²/g. See [Jee, Park & Lee, ApJ 1007, 56, published 10 August 2026](https://doi.org/10.3847/1538-4357/ae88fb); its posterior has **not** been reproduced here.

## Execution and continuity

One deterministic ChatGPT Linux Python standard-library CPU process, 20-second timeout, observed wall 1.22 s, exit 0, no random seed, 10 arithmetic/limiting tests passed. Executed code SHA-256: `fe186bd2bb9dd4e81c22b8feb4d949c4b1dad2d0c81b67fcc780d3cece2475ef`. Raw JSON SHA-256: `b8c7cd7983632bac915743cda64d5b1f87481a8f8092fe31726b40fe5d500d32`. Source and raw results remain in the ChatGPT run's companion package; **they are not claimed as files uploaded to this PR**. The checks do not validate the astrophysical model.

Retain C-06/C-08 toy angle/turnaround degeneracies, C-09 within-system error arithmetic, C-10 hypothetical shared nuisance floor, C-03 **FAILED** globally unscreened gravity and N-06 particle/antiparticle sign correction. Reader learning introduced: bounded systematic versus measurement standard deviation and sensitivity-transfer ratios. **Demonstrated understanding NOT_ASSESSED**. No new email, manuscript or journal submission.