"""C-01 exact toy identity audit. All numbers SIMULATED, no observations.
Run: python verify_core.py (Python standard library only)
"""
import json
from math import log

z_pivot, z_early = 1.0, 3.0
P_pivot, g_true, g_alt = 0.8, 0.9, 1.0

def a(z): return 1.0 / (1.0 + z)
def power(z, g): return P_pivot * (a(z)/a(z_pivot))**(2*g)
def bias(z): return (a(z)/a(z_pivot))**(g_true-g_alt)

ell = log(a(z_early)/a(z_pivot))
X_g = ((1,0,2,0),(1,2*ell,0,2))
null_amplitude = (2,0,-1,-1)
null_growth = (0,1,0,-ell)
checks = {
    "same_pivot_amplitude": abs(power(z_pivot,g_true)-power(z_pivot,g_alt)) < 1e-13,
    "matter_two_epoch_rank_two": abs(2*ell)>1,
    "galaxy_jacobian_has_two_independent_rows": X_g[0][2]*X_g[1][3]==4,
    "amplitude_bias_null": all(abs(sum(x*v for x,v in zip(row,null_amplitude)))<1e-13 for row in X_g),
    "growth_bias_null": all(abs(sum(x*v for x,v in zip(row,null_growth)))<1e-13 for row in X_g),
    "true_vs_alt_matter_differs_at_z3": power(z_early,g_true)>power(z_early,g_alt),
    "galaxy_bias_exactly_masks_every_sampled_redshift": all(abs(power(z,g_true)-bias(z)**2*power(z,g_alt))<1e-13 for z in [1+i/50 for i in range(101)]),
    "positive_everywhere": all(power(z,g_true)>0 and power(z,g_alt)>0 and bias(z)>0 for z in [1+i/50 for i in range(101)]),
}
assert all(checks.values()), checks
print(json.dumps({"status":"DERIVED, SIMULATION_RESULT, conditional UNIDENTIFIABLE",
                  "data":"SIMULATED ONLY", "z":z_early,
                  "true_matter":power(z_early,g_true),
                  "alternative_matter":power(z_early,g_alt),
                  "alternative_bias":bias(z_early),
                  "checks_passed":sum(checks.values())},indent=2))
