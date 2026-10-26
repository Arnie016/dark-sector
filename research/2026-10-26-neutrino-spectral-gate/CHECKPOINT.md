# N-11 | Research and learning checkpoint, 26 October 2026

## Research

- **N11-C1 DERIVED:** For a two-source, two-energy, four-unknown coherent normalized toy, the exact local identification gate is \(|\det J|=|x_1y_2-x_2y_1||D_1D_2|\). Different source columns and energy-shared production fractions can give local rank four. Global sign-flip ambiguity remains.
- **N11-C2 SIMULATION_RESULT:** A first-bin-matched alternative misses source-2 E=2 by 0.12031179 and held-out E=3 by 0.18390870. Every observation and parameter is SIMULATED.
- **N11-C3 UNIDENTIFIABLE:** Two physically allowed energy-specific source fractions 0.45205207 and 0.84756354 exactly reproduce both source-2 energy bins under alternative couplings.
- **N11-C4 DATA_INSUFFICIENT:** No observed event response, joint covariance, source production constraints or three-flavor source-level likelihood exists in this run. No particle evidence established.
- **Run:** two bounded attempts; first vacuous zero-length test corrected. Final single standard-library Python process on Linux 3.13.5, timeout 20 s, wall 1.03 s, exit 0, 15/15 checks, no RNG. Executed source SHA-256 08cf78770bf2d52edd9c6e887babf810fc3e0b806308140e98e2aaac584f70ba; receipt SHA-256 78744205b072305b68b607dcf3fae2e14ec09e129688bd9a264de8bb740edba8.
- **Continuity:** original main b6b85682f0843ae0d097b5f192d90b51b130788d, latest N-10 in open PR #4. Preserve C-03's FAILED unscreened gravity model, C-05's SIMULATED heat/history results and N-06 sign correction. Named September ZIPs not recovered. No archive claimed reproduced.
- **Primary sources checked through 26 October:** arXiv:2609.26773v1 sections II, IV-VI and Appendix B (preprint 22 September 2026), PRD 112 043019 journal abstract only (published 13 August 2025, older 7.5-year HESE observations); ALBERT 2603.28935v1 is background, not run.

## Learning

Newly **introduced**, not demonstrated: source/energy sensitivity Jacobian, local versus global identifiability, spectral information and nuisance freedom, held-out prediction. **USER UNDERSTANDING: NOT_ASSESSED**.

**Next gate:** test ordinary-NSI and source-spectrum nuisances with a three-flavor phase-averaged calculation and physically calibrated source/detector response. Stop if profile rank collapses or inputs are absent.
