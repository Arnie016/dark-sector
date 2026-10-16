# L-03 | Geometry, not a special lens count

**16 October 2026. Status: DERIVED + SIMULATION_RESULT.** Known multi-plane lensing mathematics, independently implemented over a bounded finite domain. No observations, particle discovery, special Fibonacci law or unique mass-map reconstruction.

[Code](run.py) · [Actual numerical results](results.json)

## Physical question

Can a sequence of gravitating structures leave information in a light beam's image distortion beyond the sum of their individual effects? Yes, in the scalar thin-lens model: the deflection by one plane changes the point at which the ray encounters the other. The effect depends on mass geometry and distance factors, not only the number of black holes. These lenses need not be black holes.

## Derive the intermediate relation

Trace a ray from the observer through two ordered lens planes. Let x be its observed angular position, x2 its angular coordinate on plane 2 and y the corresponding source coordinate. Reduced deflections alpha1 and alpha2 include the source-distance scaling. Then

$$x_2=x-b\alpha_1(x),\qquad y=x-\alpha_1(x)-\alpha_2(x_2).$$

Here b=D12 Ds/(D2 D1s), a dimensionless ratio of angular-diameter distances. The two entries of each vector are sky coordinates, not quantum amplitudes. Define U_i as the derivative of alpha_i with respect to its own plane coordinates. Each entry answers how a small angular displacement changes a deflection component. For a scalar lens potential, U_i is a symmetric physical potential Hessian, not a likelihood Hessian.

Apply the chain rule, keeping the intermediate x2 dependence:

$$A=\frac{\partial y}{\partial x}=I-U_1-U_2(I-bU_1)=I-U_1-U_2+bU_2U_1.$$

A maps small image displacements to source displacements. Because the individual U matrices are symmetric,

$$A-A^T=b(U_2U_1-U_1U_2).$$

The difference of the two products is a commutator. It records whether the transformations depend on their order. This is the established two-plane relation of [Pen & Mao, Rotation in Gravitational Lenses, Eqs. 6-7](https://arxiv.org/abs/astro-ph/0506053), published in MNRAS 367 (2006), 1543-1550, DOI 10.1111/j.1365-2966.2006.10056.x. Methods and observability caveats were read; this is not a claim to reproduce their full forecasts.

## Worked example: SIMULATED

Use dimensionless tidal matrices U1=diag(0.30,0.10), U2=[[0.15,0.08],[0.08,0.15]] and b=0.5. Then

$$A=\begin{pmatrix}0.5725&-0.076\\-0.068&0.7575\end{pmatrix}.$$

The antisymmetric coefficient omega=(A21-A12)/2 is 0.004. This is NOT a directly measured rotation angle. With U_i=kappa_i I+gamma_i [[cos(2phi_i),sin(2phi_i)],[sin(2phi_i),-cos(2phi_i)]], direct multiplication gives

$$\omega=b\gamma_1\gamma_2\sin[2(\phi_2-\phi_1)].$$

The same two lens strengths give omega=0 for aligned axes, +0.004 at relative angle +45 degrees and -0.004 at -45 degrees. Thus a fixed count is insufficient to specify the mapping. kappa is isotropic focusing, gamma is shear strength, and phi is the shear-axis orientation; all entries and omega are dimensionless.

Limits: no second lens, b=0, aligned or perpendicular shear axes give zero antisymmetric part. Arbitrarily many scalar deflectors within one thin plane still have a symmetric summed Hessian. Symmetric shear can change an ellipse's apparent major-axis direction, so zero antisymmetric part does not mean every apparent reorientation vanishes.

## What actually ran

One standard-library Python CPU process, 20-second hard timeout, exit code 0. The deterministic scan used 181 integer angles from -90 to +90 degrees. Eleven implementation/limiting checks passed. A separate check inside the same process finite-differenced the full nonlinear two-point-lens ray map; maximum Jacobian discrepancy across two step sizes was 1.20e-11. Direct angular formula discrepancy was 5.21e-18. These are consistency checks, not independent physical validations.

Run `python run.py --output output`. Numerical core 0.00200247 s; total process including startup 0.657294 s. Python 3.13.5 on Linux, one worker, no random draws, no installs or paid service. Strict finite JSON export/readback passed. Code SHA-256: `25cefebeabde6002c1b025389597274c7de13929a3006bec892d2e709f835609`.

The chat companion package additionally contains the saved CSV, high-resolution figure and conceptual roadmap. Those visual assets are not uploaded in this compact PR. The script regenerates its own CSV and result receipt.

## What would make this observable?

A single local matrix does not uniquely reveal the mass distribution or an unlensed source orientation. Uniform additional lensing can be absorbed into a transformed source model. Pen & Mao explain why differential information across resolved multiple images matters. This result is not photon polarization rotation, a quantum interference pattern, near-horizon black-hole ray tracing or a dark-matter composition measurement.

**Smallest supported claim:** the scalar two-plane map can have a nonzero antisymmetric component controlled by noncommuting tidal matrices.

**Strongest null:** a flexible single-plane model plus source-shape uncertainty explains the resolved images.

**Recommended next bounded test:** choose resolved components of one multiply imaged source, fit a single-plane baseline versus a two-plane model and hold out component positions. Stop with DATA_INSUFFICIENT without image/astrometric covariance and foreground redshifts. Reject a proposed detection if the advantage disappears with source freedom or held-out validation. Do not infer a Fibonacci pattern by selecting counts after observing the result.

## Continuity and learning

Actual main HEAD and open PRs were read. N-04 methods were recovered with Files; N-05 shared-gravity notes were read at their pinned commit. Their experiments were not rerun. Existing PRs #4 and #5 remain untouched. L-03 connects their propagation discussion to a concrete gravitational mapping, without introducing a new particle interaction.

New explanation: chain rule through a deflected ray; potential Hessian; commutator versus count; observable mapping versus source-coordinate ambiguity. Learner understanding is NOT_ASSESSED. Prior failures remain historical, not retroactively repaired. No schedule change, outreach, manuscript submission or affiliation claim.
