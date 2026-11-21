# C-12 | X-ray shock compression does not, by itself, establish a merger clock

**31 October 2026** | **C12-XRAY-FLOW** | **DERIVED / UNIDENTIFIABLE (in specified frame model) / DATA_INSUFFICIENT**

## Physical question

Radio-relic separations are used as a merger chronometer, but what does an independent X-ray density jump measure? It yields a shock **Mach number relative to upstream gas**, not necessarily the speed of that shock relative to the cluster. This is a distinct nuisance from the projection/calibration uncertainties retained in C-06 through C-11.

The 28 April 2016 peer-reviewed Abell 115 study by Botteon et al. (DOI [10.1093/mnrasl/slw082](https://doi.org/10.1093/mnrasl/slw082)) reports an X-ray-derived density compression **r = 2.0 ± 0.1** and upstream **kT = 4.3 keV** (+1.0/-0.6). These are OBSERVED AS REPORTED marginal summaries, not raw event data. Abell 115 is an off-axis merger with an analyzed one-sided shock: it does *not* furnish an observed symmetric double-relic clock.

## One exact hydrodynamic relation

For a steady, nonradiative, planar monatomic gas shock, the Rankine-Hugoniot jump relation is

\[
r=\frac{\rho_d}{\rho_u}=\frac{4\mathcal M^2}{\mathcal M^2+3},
\qquad \mathcal M=\sqrt{\frac{3r}{4-r}}.
\]

The upstream sound speed is \(c_s=\sqrt{\gamma k_BT/(\mu m_p)}\), with \(\gamma=5/3\) and illustrative mean particle mass \(\mu=0.60\) proton masses. For the source's rounded r and kT this gives **Mach 1.732**, **c_s = 1069.64 km/s**, **shock speed w = 1852.68 km/s relative to upstream gas**. This is a source-anchored mathematical check, not reproduction of the published Chandra analysis.

If the upstream gas has cluster-frame velocity \(u\), the shock speed in the cluster frame is \(V=u+w\). Both **r** and **kT** can stay fixed while **u** varies. A *SIMULATED* one-megaparsec constant-speed path gives elapsed time **0.723, 0.528 or 0.416 Gyr** for *SIMULATED* u = **-500, 0 or +500 km/s**, respectively. No such u or travel path was measured for Abell 115. The model is deliberately not a time-evolving two-shock simulation.

**AHA (explanation, not discovery):** Adding a new observational channel can constrain a **relative velocity** without measuring the **reference-frame velocity** required by the intended chronometer. Repeatedly improving the gas compression error bars would not identify that missing frame speed.

## Falsifier and limits

**Smallest result:** Within this model, the pair (r,kT) cannot identify (V,t) when upstream velocity u is free. An external upstream-flow constraint and a time-dependent shock trajectory can resolve this specific ambiguity. Projection and merger geometry remain additional nuisances. The strong-shock compression limit is r→4; r=1 gives Mach 1. No SIDM cross-section or significance follows.

The 13 October 2026 preprint [TNGC-SIDM I](https://arxiv.org/html/2610.18957v1) uses AREPO moving-mesh magnetohydrodynamics, gravity and SIDM interactions. Its **SIDM simulation arrays were not accessed**; the authors state the release is future, with publication-related data available on request. [TNG-Cluster CDM data](https://www.tng-project.org/data/) are public, but are not paired SIDM trajectories. The 9 July 2026 version of [Jee et al.](https://arxiv.org/html/2605.00093v2) and its eleven-merger likelihood were likewise **not reproduced**.

## Actual execution and continuity

One Python 3 standard-library CPU process in the ChatGPT Linux environment, 20-second hard timeout, exit **0**; **8** arithmetic/limiting checks passed, no random seed. Executed script SHA-256 **ffb0582668a9e6cfdf05ea94fd914b4e64a7b4a09fb38733c3cd2e6c0fe05045**; raw JSON SHA-256 **e76e550b752fc5acc24227cf1b57b43deee07fd2ddc48399385b757f1db945e5**. Exact executable and raw output are preserved in the companion generated in the ChatGPT run; **they are not uploaded in this commit**. No CI or independent reviewer check was run.

**Research checkpoint:** C12-XRAY-FLOW DERIVED/UNIDENTIFIABLE; real upstream flow, halo trajectories, viewing angles, observational selection and full hydrodynamics are DATA_INSUFFICIENT. Preserve C-03 FAILED unscreened gravity, C-06/C-08 projection nulls, C-09/C-10 covariance/calibration gates and C-11 source-anchored clock contrasts.

**Learning checkpoint:** reference frames, Mach vs cluster-frame shock speed introduced; **demonstrated understanding NOT_ASSESSED**. Digestibility self-check: physical diagram, defined symbols, numerical scale, limiting case and extra observable must all be supplied in the user-facing report; an explanation score is not scientific validity or reader mastery.

**Recommended next bounded gate:** extract a public TNG-Cluster CDM shock track or obtain author-supplied matched CDM/SIDM tracks with upstream gas velocities; test one independently held-out merger before fitting a dark-matter response or building an AI surrogate.
