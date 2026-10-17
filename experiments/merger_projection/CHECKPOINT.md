# S-01 research and learning checkpoint | 17 October 2026

**Status:** DERIVED (restricted model Jacobian), SIMULATION_RESULT (noiseless deterministic synthetic injection), UNIDENTIFIABLE from a single projected separation plus an idealized stage clock, DATA_INSUFFICIENT for measured cluster inference.

**Source checkpoint:** Lee et al., TNGC-SIDM I, arXiv:2610.18957v1, submitted 13 Oct 2026. Read methods 2.1, sensitivity sections 4.1/5.2, resolution 5.1 and Data Availability. The paper's two pilot paired cluster simulations are NOT downloaded or reproduced. Observational covariance/selection functions were not retrieved. Silverman et al., Mergers Matter, June 2026, covers dwarf-halo histories at vastly different scattering velocities. The 29 Sep dark-sector Atlas is a historical source, not new exposure.

**Actual execution:** one process Python 3.13.5, stdlib only, deterministic grid of 151 s values and 501 viewing angles, 15 implementation/limiting checks passed. SHA-256 for exact executed source is 74acf95719277d3066ccf2a7619b0709a0e8de5e1b21ebf3dc3fd5ec2eb84d71. Source outputs in output/results.json. Synthetic best fit (s,theta)=(0.8,15 deg); s=0 exactly mimics projected H at 30.36 deg. With independent Gaussian mock velocity uncertainty, the profiled s=0 squared residual is 2.93131, not a statistical exclusion.

**Strongest null and stop:** collisionless CDM plus projection/merger-phase/mass selection fits. Without independent inclinations the model is UNIDENTIFIABLE. A physically calibrated simulation might show different sign evolution after second pericenter or strong resolution dependence; stop using the local linear response if either occurs.

**Next gate:** obtain source-specific multiwavelength data/covariance or licensed matched simulation tracks and validate a CDM nuisance baseline on held-out independent clusters. No cherry-picked snapshots counted as independent.

**Learning checkpoint:** new mathematical tool is the observable-parameter Jacobian, with columns as changes under parameter perturbations and rows as measured channels. A second channel increases rank only when its sensitivity differs. At apocenter relative LOS speed can vanish, removing leverage. The user did not supply a worked solution; mastery remains NOT_ASSESSED.

**Continuity:** main HEAD and five open PRs inspected, none overwritten or merged. Previous C-03 failed globally unscreened f(R) model remains FAILED. This study neither repairs nor reproduces earlier neutrino or lensing work. No extra scheduler, publication, paid compute or outreach.
