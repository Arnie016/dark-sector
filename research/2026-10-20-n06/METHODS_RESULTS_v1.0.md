# N-06 | Methods/results v1.0.0

20 October 2026. Known two-flavor forward-scattering physics; no novelty or experiment claim. Three stable states:

**N-06-C1 DERIVED:** If ordinary and candidate dark potentials multiply the same flavor projector and are proportional along a path, the entire Hamiltonian, hence all coherent transition probabilities, depends on their sum. Infinite spectral resolution cannot isolate their separate amplitudes.

**N-06-C2 SIMULATION_RESULT:** For two ideal constant-density paths with shared electron normalization but different known dark-to-electron scale ratios, the finite-grid response Jacobian acquires rank 2. This is CONDITIONAL identifiability, not a detector forecast.

**N-06-C3 UNIDENTIFIABLE:** With free electron normalization in each path, the extra potential remains an exact linear combination of nuisance columns.

Use \(\hbar c=1.973269804\times10^{-7}\ \mathrm{eV\,m}\), \(\Delta m^2=2.5\times10^{-3}\ \mathrm{eV^2}\), \(\theta=8.6^\circ\), \(\ell=1300\ \mathrm{km}\), \(V_0=1.07\times10^{-13}\ \mathrm{eV}\). For each path and energy,

\[
H_\mathrm{tr}=(h_z\sigma_z+h_x\sigma_x)/2,\quad
h_x=\Delta m^2\sin2\theta/(2E),\quad
h_z=V-\Delta m^2\cos2\theta/(2E).
\]

With \(V_j=V_0(e_ja+d_jq)\) and ideal transition \(P_j(E)\), the chain rule gives

\[
J_{jk,a}=V_0e_j P'_{jk}(V_j),\qquad
J_{jk,q}=V_0d_j P'_{jk}(V_j).
\]

For single path A: \(e_A=d_A=1\), hence columns equal. For A plus B, \(e_B=1.5,d_B=1\), they become independent if matter calibration is common and responses are nonzero. With two nuisance parameters \(a_A,a_B\), \(J_{\cdot q}=J_{\cdot a_A}+(2/3)J_{\cdot a_B}\). This proves the restored null. This is a statistical-Jacobian identity, not a physical gravitational Hessian.

**Computed control:** truth \(a=1,q=0.1\), E=(0.8,1.2,1.6,2.2,3) GeV, neutrino and antineutrino. Single-path relabel residual 0. Two-path relabel max 0.0036311878568. Conditional two-path \(J^T J\) eigenvalues 0.0570159381 and 0.0005207529513, unweighted. Free-normalization null residual 3.46944695195e-12, finite-difference step 1e-5. These are synthetic expectation calculations with no noise, likelihood covariance or observational events.

**Contact-operator boundary:** \(-G_\chi(\bar\nu_{eL}\gamma_\mu\nu_{eL})(\bar\chi\gamma^\mu\chi)\) for an asymmetric Dirac dark fermion is only a low-energy illustration. Vector current cancels for equal particle/antiparticle densities; gauge completion, charged-lepton couplings, in-medium validity and other bounds were NOT analyzed. Under illustrative n_chi=0.4 cm^-3 and n_e=8.37e23 cm^-3, attaining q=.1 would require coupling ratio >2e23 relative to sqrt(2)G_F. Do not interpret this toy as a viable DM explanation.

**Reproducibility:** Python standard library only; one worker, 15-second external timeout; no random seed or GPU. 14 finite checks after fixing an off-by-one assertion in the result count; the original failure is preserved. Source SHA-256 in README. Original local results.json SHA-256: 8dccb9b58924378229f0a3f16c84f4a196014c9c7183e5f44dc593a470871ee4. Run.py regenerates the full numerical receipt and CSV. Automated checks are not external replication.

**Sources and limit:** PDG 2025 Sec. 14.5 (ordinary matter Hamiltonian); Coloma & Schwetz 2016 Phys. Rev. D 94 055005 (related NSI identifiability); Bezboruah et al. 2026 arXiv:2601.04802, preprint formalism Sec. 2 (different scalar DM correction). No measured likelihood or novelty claim. Smallest falsifier of a claim to separate ordinary from dark contributions is that marginalizing independent ordinary electron-density amplitudes restores degeneracy.
