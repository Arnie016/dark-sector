# Learning notebook | how to think like a physicist

A concept appearing in a report is **introduced**, not automatically **understood**.

Each lesson connects four things: a physical question, an intuitively meaningful scale, a worked mathematical tool and a falsifiable limiting case. Keep notation local and label units.

| Concept | Why it matters | Learning state |
|---|---|---|
| Matrix rank and dependent flux ratios | Six pairwise ratios of four fluxes contain at most three independent log contrasts. | **Introduced in prior report; mastery unassessed** |
| Fisher information and null directions | An observed flux pattern may constrain only a combination of host and subhalo parameters. | **Introduced; mastery unassessed** |
| Lensing Jacobian and eigenvalues | Local stretching can change sign or amplitude depending on host geometry. | **Introduced; mastery unassessed** |
| Covariance propagation | Rebinning expected counts does not justify independent errors for fractionally transformed observed counts. | **Introduced; mastery unassessed** |
| Poisson thinning and nuisance profiling | Missing galaxy associations and missing particles can look similar under unknown backgrounds. | **Introduced; mastery unassessed** |
| Gravothermal heat transport | Self-interactions redistribute heat, but merger history influences halo collapse. | **Introduced; mastery unassessed** |
| Solar versus sidereal modulation | A directional extraterrestrial signal does not repeat on exactly the same clock as sunlight. | **Introduced; mastery unassessed** |

**Worked example · rank:** Four measured image log fluxes \(x=(x_A,x_B,x_C,x_D)\) yield differences \(x_B-x_A\), \(x_C-x_A\) and \(x_D-x_A\). Every other pairwise log contrast is a combination of those three. If all four fluxes shift by the same logarithmic offset \(c\), the differences do not change. Therefore the measurement cannot determine the common scale using ratios alone. This algebraic fact holds regardless of the underlying lens physics.

**Limiting check:** With only one image, there are zero brightness ratios; with two images, one independent contrast.

The worked algebra is a known identity, not a test of dark matter. For a learner-assessed status, ask a new case and check the reasoning explicitly rather than assuming comprehension.
