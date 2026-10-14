# Local lensing and finite-source assumptions

For a host Jacobian $A_0=\operatorname{diag}(\lambda_t,\lambda_r)$ and local perturber Hessian

$$H_s=\begin{pmatrix}\kappa+\gamma\cos2\phi&\gamma\sin2\phi\\\gamma\sin2\phi&\kappa-\gamma\cos2\phi\end{pmatrix},\quad A=A_0-H_s,$$

$$\det A=(\lambda_t-\kappa)(\lambda_r-\kappa)-\gamma^2+(\lambda_t-\lambda_r)\gamma\cos2\phi.$$

Signed magnification is $\mu=1/\det A$; observed brightness uses its absolute magnitude. For an isotropic host the orientation term vanishes. Zero perturber recovers the host. Near $\det A=0$, point-source local approximations are especially fragile.

This fixed-position expression is not a complete lens-equation solution. Physical modeling needs calibrated mass, distances, profiles, multiple lens planes where relevant, re-solved image positions, and finite-source integration.

## Pure fold translation

Let $u$ measure displacement perpendicular to an ideal straight fold. A point-source fold contribution has the form $K\,\Theta(u)/\sqrt{u}$. A normalized extended brightness profile averages it over source coordinates. If host offset $h$ and halo shift $s$ enter only through $u=u_0+h-s$, only that combination is identifiable. A compensating shift preserves every source-size average.

Curvature or extra images need not share this symmetry. Independent astrometry/arcs can constrain host freedom. The prior integration and Fisher numbers remain [historical reports](../checkpoints/2026-10-13.md); this file records the model assumptions, not a fresh sensitivity forecast.
