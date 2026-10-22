# S-03 | Methods and results v1.0

**Claims.** S-03-C1 **DERIVED**: Given the published angular law and a declared Maxwell speed model, distinct velocity moments \(R_1\) and \(R_5\) differ. S-03-C2 **SIMULATION_RESULT**: deterministic velocity quadrature for published input parameters but SIMULATED speed distributions. S-03-C3 **UNIDENTIFIABLE**: at fixed dispersion, a sole scalar \(R_1=\sigma_0 F_1(s/w)\) does not separately identify \(\sigma_0\) and \(w\). Observational status: **DATA_INSUFFICIENT**.

## Derivation and limiting case

For independent 1D components each distributed \(N(0,s^2)\), differences are distributed \(N(0,2s^2)\). In 3D the relative-speed density is \(f_s(v)=v^2 e^{-v^2/(4s^2)}/(2\sqrt{\pi}s^3)\). With \(u=v/(2s)\), \(f_s(v)dv=(4/\sqrt{\pi})u^2e^{-u^2}du\).

The viscosity fraction for \(y=(v/w)^2\) is
\[
S(y)=6\frac{(y+2)\ln(1+y)-2y}{y^3}
=1-y+0.9y^2+O(y^3).
\]
Our explicitly normalized angular kernel gives \(\sigma_V=\sigma_0\) in the isotropic \(y\to0\) limit.

For \(R_p=\langle v^p\sigma_V(v)\rangle/\langle v^p\rangle\), the integral becomes
\[
\frac{R_p}{\sigma_0}
=\frac{\int_0^\infty u^{p+2}e^{-u^2}S(4s^2u^2/w^2)\,du}
{\tfrac12\Gamma[(p+3)/2]}.
\]
Using \(\langle u^{p+4}\rangle/\langle u^{p+2}\rangle=(p+3)/2\), its small-\(s/w\) expansion is \(1-2(p+3)(s/w)^2+O((s/w)^4)\).

## Reproduction and evidence boundary

Executed source: [run.py](run.py); SHA-256 \`cc069fd4b835c7527f0b45113ccf8e15fc957f8b6ef0886b9558b78a9361e1e3\`. Python standard library; one CPU worker; Simpson grids of 6000 and 12000 subdivisions; \(u\in[0,10]\), upper-tail \(e^{-100}\) suppression; seed null; 26 tests pass; maximum coarse/fine difference \(5.069272875546284\times10^{-13}\). Independent data were **not** simulated or fitted. [summary.json](summary.json) records the numerical table's key entries and a rate-matched intentionally unphysical control. Running the code produces complete results.json.

The model was published in [SIDM Concerto 2503.10748v2](https://arxiv.org/html/2503.10748v2) (2025). \(v^5\) weighting is prior art in [Fischer et al. MNRAS 529 (2024), Eq. 9](https://academic.oup.com/mnras/article/529/3/2327/7624679) and Yang & Yu (2022). The calculation does **not** reproduce Concerto's N-body heat-conduction kernels. Held-out numbers are predictions of two mathematical distributions, not observed independent halos. Stellar/gas data, actual halo velocity fields, morphology selection, sample covariance and merger history remain absent. A failed Zenodo redirect does not prove public data inaccessible.

**Falsifier:** if true speed distributions and merger-history controls make the two candidate microphysical scenarios predict indistinguishable held-out observables, report **UNIDENTIFIABLE**. The next gate is the licensed, verified particle/halo catalogue and a matched baseline, not significance optimization. Reader mastery NOT_ASSESSED.
