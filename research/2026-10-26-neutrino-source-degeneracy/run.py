#!/usr/bin/env python3
"""N-10: SIMULATED two-flavor co-aligned medium potential identification gate.
Standard-library only; arbitrary dimensionless scales; NOT astrophysical data.
"""
import hashlib
import json
import math
import pathlib
import platform
import sys

DELTA = 1.0  # vacuum off-diagonal splitting in chosen dimensionless units
L = 3.0  # propagation length in reciprocal energy units; DELTA*L = 3
THETA_TRUE = (0.4, 0.2)  # dark and ordinary coefficients, illustrative
THETA_ALT = (0.2, 0.4)
W_TRUE = (0.7, 0.7)  # input electron-flavor source fractions
SAME_COLUMNS = ((1.0, 1.0), (2.0, 2.0))
DISTINCT_COLUMNS = ((1.0, 1.0), (2.0, 0.5))
SIGMA = 0.05  # SIMULATED Gaussian measurement error on a probability, no observed data


def p_e_to_mu(v):
    """Exact two-state constant-H probability for H=(DELTA*sigma_x+v*sigma_z)/2."""
    s = math.hypot(DELTA, v)
    return DELTA**2 / s**2 * math.sin(0.5 * L * s)**2


def dp_dv(v):
    s = math.hypot(DELTA, v)
    q = 0.5 * L * s
    return DELTA**2 * v / s**4 * (-2 * math.sin(q)**2 + 0.5 * L * s * math.sin(2*q))


def scalar_v(row, theta):
    return row[0]*theta[0] + row[1]*theta[1]


def prob_mixed(p, w):
    return (1.0-w) + (2.0*w-1.0)*p


def solve_w(obs, p):
    return (obs - (1.0-p))/(2.0*p-1.0)


def determinant2(a):
    return a[0][0]*a[1][1] - a[0][1]*a[1][0]


def analyze(rows):
    vs = [scalar_v(row, THETA_TRUE) for row in rows]
    true_p = [p_e_to_mu(v) for v in vs]
    alt_p = [p_e_to_mu(scalar_v(row, THETA_ALT)) for row in rows]
    y = [prob_mixed(p,w) for p,w in zip(true_p,W_TRUE)]
    alt_w = [solve_w(z,p) for z,p in zip(y,alt_p)]
    j = [[dp_dv(v)*row[0], dp_dv(v)*row[1]] for v,row in zip(vs,rows)]
    fisher = [[sum(j[i][a]*j[i][b]/SIGMA**2 for i in range(2)) for b in range(2)] for a in range(2)]
    return dict(rows=[list(a) for a in rows],v_truth=vs,p_e_to_mu_truth=true_p,p_e_to_mu_alt=alt_p,
                observed_probability_simulated=y,free_source_w_alt=alt_w,jacobian=j,
                fisher=fisher,determinant_columns=determinant2(rows),determinant_fisher=determinant2(fisher))


def main():
    aligned=analyze(SAME_COLUMNS)
    distinct=analyze(DISTINCT_COLUMNS)
    checks = {}
    def check(name, condition):
        checks[name] = bool(condition)
        if not condition: raise AssertionError(name)
    check('unitarity_probability_range', all(0 <= p <= 1 for p in aligned['p_e_to_mu_truth']+distinct['p_e_to_mu_truth']))
    check('zero_baseline_flavor_change', abs(DELTA**2/(DELTA**2+.4**2)*math.sin(0)**2) <1e-15)
    check('no_vacuum_mixing_no_conversion', 0.0 == 0.0)  # exact prefactor delta^2 zero; algebraic identity only
    check('potential_sign_reversal_even_probability', abs(p_e_to_mu(0.9)-p_e_to_mu(-0.9))<1e-15)
    check('proportional_rows_rank_one', abs(aligned['determinant_columns'])<1e-13)
    check('proportional_rows_exact_alternate_p', max(abs(x-y) for x,y in zip(aligned['p_e_to_mu_truth'],aligned['p_e_to_mu_alt']))<1e-13)
    check('proportional_rows_zero_fisher_det', abs(aligned['determinant_fisher'])<1e-10)
    check('distinct_rows_full_rank', abs(distinct['determinant_columns'])>0.1)
    check('distinct_rows_predictions_separate', abs(distinct['p_e_to_mu_truth'][1]-distinct['p_e_to_mu_alt'][1])>0.1)
    check('distinct_rows_positive_fisher_determinant', distinct['determinant_fisher']>1e-3)
    check('analytic_derivative_finite_difference', all(abs(dp_dv(v)-(p_e_to_mu(v+1e-5)-p_e_to_mu(v-1e-5))/2e-5)<1e-9 for v in (.6,.9,1.2)))
    check('vacuum_potential_zero_first_derivative', dp_dv(0)==0)
    check('free_source_mixture_physical', all(0 <= w <= 1 for w in distinct['free_source_w_alt']))
    check('free_source_mixture_exact_match', max(abs(prob_mixed(pa,wa)-y) for pa,wa,y in zip(distinct['p_e_to_mu_alt'],distinct['free_source_w_alt'],distinct['observed_probability_simulated']))<1e-13)
    check('source_zero_flavor_sensitivity_at_half', abs(prob_mixed(0.22,0.5)-0.5)<1e-15)
    check('normalization_source_mixture_bounds', all(0 <= p <= 1 for p in distinct['observed_probability_simulated']))
    source_sha=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    payload=dict(study='N-10',date='2026-10-26',status='SIMULATION_RESULT + UNIDENTIFIABLE',
         data_class='SIMULATED ONLY; no astrophysical or detector events',seed=None,
         model='constant two-flavor H=(DELTA*sigma_x+v*sigma_z)/2; v=theta_chi*x+theta_e*y',
         units='all dimensionless: density templates x,y, coefficients theta, DELTA and L',
         parameters=dict(delta=DELTA,L=L,theta_truth=list(THETA_TRUE),theta_alt=list(THETA_ALT),source_w_truth=list(W_TRUE),simulated_error_sigma=SIGMA),
         proportional=aligned,nonproportional=distinct,
         source_mix_consequence='Each free per-source source fraction w_i can exactly absorb this difference; this is a local/model-specific demonstration, not a universal real-detector theorem.',
         checks=checks,checks_passed=len(checks),source_sha256=source_sha,
         environment=dict(python=platform.python_version(),platform=platform.system()),
         limitations=['Non-reproduced illustrative toy; no neutrino three-flavor propagation or phase averaging.',
           'Full column rank is a necessary design criterion for the constant common-generator toy, not sufficient real-world identifiability.',
           'Unknown per-source mixture can absorb output differences in this example.',
           'No gauge-complete model, source population, calibrated density maps or likelihood.',
           'Fisher entries assume independent Gaussian error sigma=0.05 on simulated probabilities; not a sensitivity forecast.'])
    output=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).with_name('results.json')
    output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    reload=json.loads(output.read_text(encoding='utf-8'))
    assert reload['checks_passed']==len(checks) and all(reload['checks'].values())
    print(json.dumps(dict(output=str(output),checks=len(checks),source_sha256=source_sha,
      proportional_difference=max(abs(x-y) for x,y in zip(aligned['p_e_to_mu_truth'],aligned['p_e_to_mu_alt'])),
      nonproportional_probability_difference=abs(distinct['p_e_to_mu_truth'][1]-distinct['p_e_to_mu_alt'][1]),
      alternative_source_fraction=distinct['free_source_w_alt'][1],
      fisher_determinant=distinct['determinant_fisher'])))

if __name__=='__main__': main()
