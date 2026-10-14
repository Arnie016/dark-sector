# Background profiling and linear mappings

## On/off toy model

With fixed source expectation $S\geq0$, background $b\geq0$, independent control exposure $r\geq0$,

$$n\sim\mathrm{Poisson}(S+b),\qquad m\sim\mathrm{Poisson}(rb).$$

Ignoring constants, $\ell=n\ln(S+b)-(S+b)+m\ln(rb)-rb$. For an interior solution with $r>0$, differentiation gives

$$\frac{n}{S+b}+\frac{m}{b}-(1+r)=0,$$

$$ (1+r)b^2+[(1+r)S-n-m]b-mS=0.$$

Choose the nonnegative maximizing root, checking the boundary $b=0$. At $r=0$, a meaningful absent control has $m=0$ and $\hat b=\max(0,n-S)$. Flexible backgrounds can then exactly compensate for reduced signal when $n\geq S$.

This assumes a known source rate, genuine independent control, and valid Poisson model. A real background estimator is not automatically an on/off measurement. The prior numerical study is [historical](../checkpoints/2026-10-09.md), not rerun here.

## Sky coordinates and covariance

With declination $\delta$ and right ascension $\alpha$,

$$d\Omega=\cos\delta\,d\delta\,d\alpha=d(\sin\delta)\,d\alpha.$$

An overlap matrix $W$ can map rates between bins under a uniform-within-bin assumption. Count conservation requires each input column to sum to one. For independent Poisson input counts with means $\lambda$,

$$\mathrm{Cov}(Wn)=W\operatorname{diag}(\lambda)W^T.$$

Mapping means does not imply output observations are independent Poisson. Deterministic fractional splitting differs from event allocation. The official [versioned detector guidance](https://icecube.github.io/skyllh/v26.1.0/html/tutorials/index.html) motivates version/coordinate checks, but these formulas do not quantify the actual DR2 correction.
