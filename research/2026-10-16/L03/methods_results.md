# L-03 | The unresolved lens core is an exact geometric null

**16 October 2026 · v1.0 · statuses: DERIVED, SIMULATION_RESULT, conditional UNIDENTIFIABLE, observational DATA_INSUFFICIENT.**

## Physical question and source status

Can lensing distinguish a dense, core-collapsed self-interacting-dark-matter (SIDM) subhalo from an extremely tidally stripped cold-dark-matter (CDM) remnant containing a black hole? Zhang and Yu, [arXiv:2606.12909v2](https://arxiv.org/html/2606.12909v2) (revised 24 September 2026), [Physical Review D 114, 083015](https://journals.aps.org/prd/abstract/10.1103/npqp-jgrp), published 6 October 2026, examine both interpretations of an existing JVAS B1938+666 perturber observation. Their model profiles differ inside roughly 10 pc, which is unresolved in their lens inference. Approximately 3×10^5 solar masses inside 10 pc is an SIDM model benchmark, not a new independently observed mass measurement. The CDM case requires a demanding tidal-stripping history that remains uncertain.

Related physics: Silverman et al. [Mergers Matter, arXiv:2606.02566v1](https://arxiv.org/html/2606.02566) (1 June 2026 preprint) study merger-driven SIDM heat transport with finite simulation-time and convergence caveats. [SIDM Concerto, arXiv:2503.10748v2](https://arxiv.org/html/2503.10748v2) (29 September 2025) documents publicly released merger catalogs. Neither simulation's outputs were processed in this study, and none independently observes the JVAS lens.

## AHA: infinite precision cannot undo information lost by projection

For a **circular static thin lens**, define R as the light ray's projected physical distance from the mass center, Σ(R) as surface density (mass/area), and M(<R) as the projected mass inside a circle of radius R. A ring of radius u and width du has area 2πu du, so

$$M(<R)=2\pi\int_0^R\Sigma(u)u\,du.$$

The physical light-bending angle is

$$\hat\alpha(R)=\frac{4G M(<R)}{c^2 R}.$$

This angle is **not** the telescope's observed image shift. Reduced deflection additionally depends on distance geometry and the entire macrolens/source model.

### SIMULATED worked model

Use M0=3×10^5 solar masses, R0=10 pc only as a scale. Model A is a central point mass, so M_A(<R)=M0. Model B is a uniform projected disk of radius R0, so M_B(<R)=M0×min((R/R0)^2,1). Both have exactly the same exterior mass distribution.

Therefore their **physical deflections are identical for all impact radii R≥R0**, regardless of precision. For rays inside, their deflection ratio is (R/R0)^2. At 3 pc, the disk bend is only 9% of the point bend.

| Projected radius, SIMULATED | Point physical bend | Disk physical bend |
| ---: | ---: | ---: |
| 3 pc | 3.94837 mas | 0.35535 mas |
| 10 pc | 1.18451 mas | 1.18451 mas |
| 30 pc | 0.39484 mas | 0.39484 mas |

One mas is one milliarcsecond. The illustrative conversion 10 pc≈1.254 mas angular *radius* at z_lens=0.881 assumes flat LCDM H0=67.4 km/s/Mpc, Ωm=0.315. It is not a telescope-resolution claim.

**Executable boundaries.** The full standard-library-only local generator in the accompanying research archive covered 381 SIMULATED radii and passed 10/10 deterministic checks. Full generator SHA-256: 0d4b6f628906d5077a4066af9d09c2a37e52ae50bfe8e8fc0fbbf5b91c972f5e. An initial nonfatal docstring warning was corrected before successful execution. The [smaller repository verifier](verify.py) checks seven related limits; no random seed, paid compute, real lens data or observational likelihood.

**Falsifiable claim.** With circular symmetry, equal projected mass inside R0 and equal exterior profile, exterior-only deflection cannot distinguish two different core profiles: **conditional UNIDENTIFIABLE**. This does **not** apply automatically to noncircular profiles, central ray information or changes in total projected mass.

**Strongest countermodel:** a CDM halo with a black hole, severe stripping, plus source/macrolens degeneracies. Resolving evidence would require JVAS image visibilities/arc structure sensitive inside 10 pc together with source reconstruction, correlated errors and macrolens posterior. Stop at UNIDENTIFIABLE if all tested rays are exterior. Do not infer SIDM cross sections, Bayes factors, signal detection or telescope capability from this toy.

**Continuity:** unresolved L-01 lens posterior/covariance, completed N-03 neutrino phase toy and the unmerged 15 October D-01 directional study are distinct. Learning concepts: projected mass integral, bending versus observed displacement and structural null. User understanding **NOT_ASSESSED**. Next bounded step: verify available JVAS data-product radial sensitivity; no journal submission or outreach.
