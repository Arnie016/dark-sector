# D-01 | Solar versus sidereal modulation: exposure identifiability

**24 October 2026 · v1.0.0 · DERIVED / SIMULATION_RESULT / UNIDENTIFIABLE / DATA_INSUFFICIENT**

**Scope:** This is a SIMULATED EXPOSURE DESIGN, not physical detector simulation, an observational fit or a new theorem. Reproducible [executed source](run.py), [raw JSON receipt](results.json), and [checkpoints](CHECKPOINT.md) accompany this report.

## Physical question

Galactic-halo dark matter can cause a detector's directional rate to repeat with Earth's rotation against the stars (sidereal day, about 23 h 56 min 4 s). The laboratory environment can have an ordinary 24-hour solar-day cycle. Can a short run reliably distinguish the two when the oscillation phase is not known?

**AHA, an explanation rather than a discovery:** those cycles shift by only about 3 minutes 56 seconds each solar day, accumulating a full phase separation over approximately one year. A short run can have a powerful *time-template degeneracy*, even with accurate timestamps. More precisely, an ordinary solar-period nuisance can mimic a putative Galactic signal. This does not mean that every solar-period signal is instrumental: solar-reflected dark matter is a physically different proposed mechanism.

## Primary sources and continuity

Blanco, Foster, Kahn and Lillard, [arXiv:2602.15947v1](https://arxiv.org/html/2602.15947), posted **17 February 2026**, sections II, III, V, VI.3, already develop directional detector Fisher likelihoods, backgrounds and shifted sidereal stacking. This study is a **KNOWN** methodological limiting case, not a novelty claim. Their material-dependent Galactic wind signal need not be exactly sinusoidal with fixed phase across a year.

DAMIC-M Collaboration, Aggarwal et al., [Physical Review D 114, 032010](https://journals.aps.org/prd/abstract/10.1103/c9fm-ymf2), **published 19 August 2026**, [arXiv:2511.13962v1](https://arxiv.org/html/2511.13962): a 1.257 kg-day search reported no significant daily modulation. Data were acquired **October 2024–January 2025**, with a roughly 77-day blind-analysis segment; they documented CCD downtime and temperature-correlated single-electron backgrounds. The August publication is an analysis of earlier exposure, not new independent August photons. No event timestamps or live-time files were obtained here. [USNO](https://aa.usno.navy.mil/data/siderealtime) supplies authoritative sidereal-time context.

A separately recovered September Atlas described a distinct 120-day SIMULATED paired-detector switching experiment. We have not rerun its code or claim its results are independent support.

## Mathematical tool: principal angles between prediction spaces

At each hourly midpoint t_i [hours], construct two solar nuisance columns

$$S_{i,:}=(\cos(2\pi t_i/24),\ \sin(2\pi t_i/24))$$

and two sidereal candidate columns

$$D_{i,:}=(\cos(2\pi t_i/23.9344696),\ \sin(2\pi t_i/23.9344696)).$$

Two columns per frequency allow an **unknown phase**. Each row is a sampled time; these numbers are neither measured event probabilities nor detector-response amplitudes. Remove the unknown constant intercept, then orthonormalize the two sets of columns to form Q_S and Q_D. Their maximum possible unknown-phase overlap is

$$\rho=\sigma_{\max}(Q_S^T Q_D),\qquad 0\le\rho\le1.$$

The worst-phase *fraction* of sidereal Fisher information remaining after fitting the solar nuisance is

$$\boxed{\eta=1-\rho^2}.$$

Why? The squared projection of a normalized sidereal waveform into the solar nuisance subspace is at most rho squared; the perpendicular component carries the distinguishing information. This assumes equally weighted independent observations and a constant-rate weak-modulation approximation. The relative standard-deviation penalty is 1/sqrt(eta), not a dark-matter significance. For an equal-frequency limiting case the prediction spaces coincide and eta = 0 exactly: **UNIDENTIFIABLE**.

The solar/sidereal frequency difference beats over 365.24223 solar days for the fixed periods chosen here. For uniform coverage and many daily cycles their approximate positive-frequency overlap is abs(sin(DeltaOmega*T/2)/(DeltaOmega*T/2)).

## One deterministic CPU computation: SIMULATED EXPOSURE

**One process:** Linux ChatGPT container, Python 3.13.5 and NumPy 2.3.5, timeout 25 seconds, exit **0**, numerical core **0.023401 s**, **8/8 implementation/limiting checks pass**. No RNG or event counts; seed null. Run python3 run.py from this directory. Source SHA-256 **2ff9e8c6a987c1b78861a5ac9e98125bcfe8e5bb2428280ab4cb9205f36bbecf**; initial receipt SHA-256 **1697dabdbe92cd136a859a239de7509f8d2bb2c85f521e12c7b5ecac49c26d4a**. The original checked source and receipt are included byte-identically; reruns naturally change runtime metadata.

The hourly masks are explicitly invented: continuous coverage, or only solar-clock 18:00–06:00 with every seventh entire day omitted starting day zero. Same periods and nuisance structure in every case.

| Window | SIMULATED mask | Hour bins | Max correlation rho | Worst retained information eta | Relative SD penalty |
|---:|---|---:|---:|---:|---:|
| 30 days | Continuous | 720 | 0.989009 | **0.021861** | 6.763 |
| 120 days | Continuous | 2880 | 0.832325 | 0.307236 | 1.804 |
| 365 days | Continuous | 8760 | 0.000665 | 0.9999996 | 1.0000 |
| 30 days | Night/6-in-7 | 300 | 0.989451 | **0.020987** | 6.903 |
| 120 days | Night/6-in-7 | 1224 | 0.832472 | 0.306991 | 1.805 |
| 365 days | Night/6-in-7 | 3744 | 0.003399 | 0.999988 | 1.0000 |

**Meaning:** an unknown solar-period nuisance absorbs roughly 98% of the *worst-phase relative sidereal information* in either 30-day mock design. The ideal frequencies separate by a year. The night mask still supplies far fewer hours, so near-perfect *fractional* retention does not imply equal absolute sensitivity. These values are not detector efficiencies or modulation fractions. Controls checked equal-frequency zero information, increasing temporal discrimination, full rank of each two-column design and valid [0,1] fractions.

## Stable claim ledger, competitors and stopping condition

**D01-C1 DERIVED / KNOWN:** identical solar/sidereal periods give identical sinusoid prediction subspaces, hence zero statistical separation regardless of duration. Reject if a correct independent projection disagrees.

**D01-C2 SIMULATION_RESULT:** these exact masks produce the numerical table. Reject if an independent implementation with the same times and frequencies disagrees beyond numerical tolerance.

**D01-C3 UNIDENTIFIABLE:** an unconstrained *sidereal-period* ordinary background with the same waveform as the candidate cannot be identified in one observed channel by waiting longer. Additional target/orientation response predictions with independently calibrated backgrounds would be required.

**D01-C4 DATA_INSUFFICIENT:** missing calibrated event timestamps, selection functions, temperature series, actual live-time, material electron/phonon response and covariance. A harmonic rank test is not a microscopic dark-matter interaction bound. Do not infer discovery significance or propose expensive hardware from this result.

**Next bounded step:** get a legal public detector exposure/temperature sequence, reproduce its ordinary background baseline, then replace ideal sine/cosine with an actual material response and check holdout predictions. Keep N-06 sign correction, N-07 gravity path, N-08 electroweak operator, N-09 mediator degeneracy, old switched-detector controls and C-03 **FAILED** unscreened long-range gravity result intact.

**Learning checkpoint:** principal angles and nuisance-profiled Fisher information introduced. Reader mastery **NOT_ASSESSED**, not established by the presence of this derivation.
