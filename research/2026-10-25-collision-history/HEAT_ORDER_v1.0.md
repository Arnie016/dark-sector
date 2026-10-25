# C-05-H | The time of heating matters even at fixed transport exposure

**25 October 2026 · v1.0 · DERIVED / SIMULATION_RESULT / DATA_INSUFFICIENT**

## What we can and cannot claim

This supplement to C-05 is an original **SIMULATED** equal-capacity two-reservoir counterexample. It proves a result **within that toy model**, not a new SIDM particle constraint, gravothermal-collapse forecast, or reproduction of an N-body simulation. It does not alter the existing C-05 collision-count/halo-history result. The source and actual calculation receipt are [heat_order_run.py](heat_order_run.py) and [heat_order_results.json](heat_order_results.json).

**Physical question:** If the total heat exchanged per unit time and the size of a merger heating impulse are held fixed, does the *time of the merger* influence the final core energy? In this declared linear model, yes. The strongest nulls are zero transfer, no impulse, and sufficiently fast thermal equilibration.

## Prior art and evidence boundary

Silverman et al., [Mergers Matter, arXiv:2606.02566v1](https://arxiv.org/html/2606.02566v1), posted **1 June 2026** (preprint), Secs. II and III.2–III.3, follow six dark-matter-only cosmological zoom-ins using 70 cm²/g SIDM. They report merger-associated changes in the heat-flow direction, using a specific kinetic-energy proxy in regions within **1 kpc** and **1–5 kpc** of halo centers. Their study motivates this test; our two-reservoir equation is not their GIZMO numerical implementation. Nadler et al., [SIDM Concerto, arXiv:2503.10748v2](https://arxiv.org/html/2503.10748v2), revised **29 September 2025** (preprint), Sec. III.2, documents (sub)halo catalogs and merger-tree methods; its public [Zenodo release](https://doi.org/10.5281/zenodo.14933624) has **not** been downloaded or fitted here. Primary methods were inspected through **25 October 2026**; no claim of literature novelty.

## One mathematical tool: eigenvectors of the heat-transfer matrix

Define x_c and x_o as perturbations of the core and outer-zone **specific kinetic energy**, in (km/s)², for two reservoirs of equal *fixed positive* capacities. With a phenomenological symmetric heat-exchange rate alpha, in Gyr⁻¹, and a merger depositing outer-zone increment Delta at t_m,

\[
\frac{d}{dt}\begin{pmatrix}x_c\\x_o\end{pmatrix}
=\alpha\begin{pmatrix}-1&1\\1&-1\end{pmatrix}
\begin{pmatrix}x_c\\x_o\end{pmatrix}
+\begin{pmatrix}0\\\Delta\end{pmatrix}\delta(t-t_m).
\]

The matrix's diagonal losses and off-diagonal gains exchange energy between reservoirs. Its eigenvector (1,1) has eigenvalue zero: equal-zone perturbations are conserved. Its eigenvector (1,-1) has eigenvalue -2 after factoring out alpha: the difference between zones decays at rate 2 alpha. These eigenvalues are **decay rates**, not probabilities or observed particle scattering cross sections.

With zero initial perturbations and an outer impulse at t_m, decomposition into the two modes gives

\[
\boxed{x_c(T;t_m)=\frac{\Delta}{2}[1-e^{-2\alpha(T-t_m)}]},\qquad
x_o(T;t_m)=\frac{\Delta}{2}[1+e^{-2\alpha(T-t_m)}].
\]

Their sum is exactly Delta. **AHA (explanatory, not a discovery):** energy injected earlier has more time to move inward. An integral that counts interactions cannot, by itself, tell us *when* an external heater acted. Important limit: with **no external forcing** and fixed exchange geometry, matrices at different times commute, so only the integral of alpha matters. This toy proves a timing dependence conditional on the impulse, not universal insufficiency of every integrated exposure statistic.

## Declared generating truth and result

Every number below is **SIMULATED**. Choose T=10 Gyr, alpha=0.1 Gyr⁻¹, Delta=100 (km/s)². Both alternatives share integrated exchange exposure alpha T = 1 and identical total injected energy. The heat-transfer parameter has **not** been calibrated from the separate C-05 scattering count (lambda approximately 0.6408); collision frequency is not automatically an energy-exchange coefficient.

| SIMULATED outer heating epoch | Core at 10 Gyr [(km/s)²] | Outer at 10 Gyr [(km/s)²] |
|---|---:|---:|
| Early, t_m = 2.5 Gyr | 38.84349199 | 61.15650801 |
| Late, t_m = 7.5 Gyr | 19.67346701 | 80.32653299 |

**C-05-H1 DERIVED:** the early-minus-late core energy difference is **19.1700249782 (km/s)²** under these stated assumptions.

**C-05-H2 SIMULATION_RESULT:** one standard-library Python CPU process under a 20-second hard timeout, no RNG/seed, completed **11 of 11** tests; closed-form versus RK4 integration at 1000 and 2000 steps, conservation, zero exchange, no heating, impulse at the endpoint and fast-exchange limits passed. Executed source SHA-256: **778dd33d292c0729f2e1965a6b27f12b524eccee86eac457ed7d63c922ae8fbf**. Exact raw JSON receipt SHA-256: **ffb5d7747988198130afe22e78805fb2fbf92df87bad08d06da854d25753d8d1**. Stored Git blobs are byte-identical to the locally executed source and locally generated raw receipt. These implementation checks are not observational verification or independent peer review.

### Limits and falsifiers

At alpha=0, both core increments are zero; at alpha(T-t_m) much larger than 1, both tend to Delta/2 so the timing becomes practically unidentifiable from the final core energy. At t_m=T, no inward transfer has occurred. The model is not self-gravitating, has no negative gravothermal heat capacity or changing geometry, and ignores baryons, orbital deposition, velocity-dependent scattering and cosmological assembly. Consequently the **direction or amount of actual halo density evolution cannot be read off from this result**.

**C-05-H3 DATA_INSUFFICIENT:** there is no observed merger timeline, calibrated velocity-dispersion covariance, independently resolved inner/outer halo kinetic-energy history or self-consistent heat-flow solver in this calculation. A useful continuation would compare an exposure-only model to a history-aware model using *actual* matched CDM/SIDM halo products, with train/test separation by independent initial halo rather than adjacent time snapshots. Failure to improve held-out predictions after controls is a stopping criterion.

**Research checkpoint:** C-05's equal-collision-count counterexample stands, and this note adds a separate source-timing counterexample. C-03's unscreened long-range modified-gravity hypothesis remains **FAILED** under its local-gravity gate. No observed dark-matter signature, halo-collapse probability, measured cross section or new publication is claimed.

**Learning checkpoint:** eigenvectors as conserved/decaying physical modes, time-localized source forcing and the distinction between collision rate versus thermal response have been introduced; understanding remains **NOT_ASSESSED**. No independent mastery evidence is inferred from this write-up.

Reproduce with Python 3 standard library: run heat_order_run.py in this directory. The generator rewrites the JSON receipt and its environment-specific Python-version entry; all measured numbers here remain SIMULATED.
