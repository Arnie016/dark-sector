# Flux-ratio information

For positive fluxes $F_A,F_B,F_C,F_D$, set $x_i=\ln F_i$. In row order B/A, C/A, C/B, D/A, D/B, D/C,

$$
y=Bx,\qquad B=\begin{pmatrix}
-1&1&0&0\\
-1&0&1&0\\
0&-1&1&0\\
-1&0&0&1\\
0&-1&0&1\\
0&0&-1&1
\end{pmatrix}.
$$

$B\mathbf1=0$: common normalization cancels. The three rows comparing B, C, D to A are independent; the others are differences of those rows. Thus $\operatorname{rank}B=3$.

For a finite log-flux covariance $C_x$,

$$C_y=BC_xB^T,\qquad \operatorname{rank}C_y\leq3.$$

This is exact for logarithmic ratios constructed from the same flux variables, not a general claim about nonlinear unlogged covariance. For illustrative $C_x=0.03^2I$, variances are $2(0.03)^2$ and some correlations ±0.5. This is **assumed covariance**, unrelated to measured marginal errors in Table 2.

Use three independent contrasts with their joint uncertainty, or a correctly supported singular likelihood. Do not invert a fabricated full-rank six-ratio diagonal covariance and call it measured. Numerical rank uses tolerance $10^{-12}$ in the included experiment.

The source table contains rounded summaries. Ratios of medians need not equal medians of ratios, and rounding also prevents exact closure. Agreement at displayed precision is a consistency check, not proof of a correct spectral/lens fit or an error in the authors' analysis.

**Input provenance:** [Table 2](https://arxiv.org/html/2606.23808v1#S4.T2). **Implementation:** [new audit](../../experiments/ratio_closure/run.py). **Missing:** joint fitted flux samples and host posterior.
