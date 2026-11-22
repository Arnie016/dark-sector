#!/usr/bin/env python3
"""Illustrative local uncertainty propagation; no inferred posterior."""
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

p = Path(__file__).resolve().parent
x = json.loads((p / 'input.json').read_text())
n, s = x['north']['central'], x['south']['central']
sn = (x['north']['lower_error'] + x['north']['upper_error']) / 2
ss = (x['south']['lower_error'] + x['south']['upper_error']) / 2
rho = x['pearson_correlation']
grad = np.array([1 / s, -n / s**2])
def width(r):
    covariance = np.array([[sn**2, r*sn*ss], [r*sn*ss, ss**2]])
    assert np.linalg.eigvalsh(covariance).min() >= 0
    return float(np.sqrt(grad @ covariance @ grad))
# Check the gradient numerically and the covariance formula independently.
eps = 1e-6
fd = np.array([((n+eps)/s-(n-eps)/s)/(2*eps), (n/(s+eps)-n/(s-eps))/(2*eps)])
assert np.allclose(grad, fd, rtol=1e-9, atol=1e-10)
independent = (n/s)*np.sqrt((sn/n)**2+(ss/s)**2-2*rho*(sn/n)*(ss/s))
assert np.isclose(width(rho), independent)
result = {'central_north_south_ratio': n/s, 'proxy_sigma_north': sn, 'proxy_sigma_south': ss,
          'published_correlation': rho, 'approx_ratio_sigma_correlated': width(rho),
          'approx_ratio_sigma_zero_correlation': width(0),
          'relative_increase_percent': (width(rho)/width(0)-1)*100,
          'qualification': x['approximation']}
(p/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
rs = np.linspace(-0.9, 0.9, 301)
fig, ax = plt.subplots(figsize=(7, 4.4))
ax.plot(rs, [width(r) for r in rs], color='#365a9e', lw=2)
for r, label in [(rho, 'Published correlation'), (0, 'Zero correlation')]:
    ax.scatter([r], [width(r)], zorder=3, label=f'{label}: ρ={r:.3f}')
ax.set(xlabel='Assumed mass correlation ρ', ylabel='Approximate ratio uncertainty',
       title='PSZ2 G181: mass-ratio sensitivity to correlation')
ax.grid(alpha=.25); ax.legend(frameon=False); fig.tight_layout()
fig.savefig(p/'covariance-sensitivity.png', dpi=160)
print(json.dumps(result, indent=2))
