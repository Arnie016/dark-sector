#!/usr/bin/env python3
"""S-03: Maxwell relative-speed averaging of the SIDM Concerto angular law.
MODEL-CALCULATED, never an observed halo or a gravothermal solver.
No random sampling, Python standard library only, one CPU process.
"""
import hashlib
import json
import math
import platform
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODELS = {
    'GroupSIDM': {'sigma0_cm2_per_g': 147.1, 'w_km_per_s': 120.0},
    'MilkyWaySIDM': {'sigma0_cm2_per_g': 147.1, 'w_km_per_s': 24.3},
}
DISPERSIONS_KM_S = (10.0, 30.0, 100.0, 300.0, 1000.0)


def angular_fraction(y):
    """(3/2) viscosity moment divided by sigma0 for Concerto Eq. (1)."""
    if y < 0.0:
        raise ValueError('y must be nonnegative')
    if y < 0.03:
        ans = 0.0
        power = 1.0
        for n in range(140):
            term = 6.0*(n+1)*power/((n+2)*(n+3))
            ans += term
            if abs(term) < 1.e-16:
                break
            power *= -y
        return ans
    return 6.0*((y+2.0)*math.log1p(y)-2.0*y)/y**3


def speed_average(w, s, moment, n=12000, angular='viscosity'):
    """<v^moment sigma(v)>/<v^moment>/sigma0.
    Relative Maxwell speed for independent isotropic Gaussian velocity vectors,
    each with 1D dispersion s; v=2*s*u; density du=4*u^2 exp(-u^2)/sqrt(pi).
    Moment is 1 for a rate proxy and 5 for a conductivity-inspired proxy.
    """
    if n % 2:
        raise ValueError('Simpson intervals must be even')
    h = 10.0/n
    acc = 0.0
    for i in range(n+1):
        u = i*h
        y = (2*s*u/w)**2
        ratio = angular_fraction(y) if angular == 'viscosity' else 1.0/(1.0+y)
        kernel = u**(moment+2) * math.exp(-u*u) * ratio
        weight = 1 if i==0 or i==n else (4 if i % 2 else 2)
        acc += weight*kernel
    numerator = acc*h/3.0
    denominator = 0.5*math.gamma((moment+3.0)/2.0)
    return numerator / denominator


def main():
    checks={}
    def check(name, condition):
        checks[name] = bool(condition)
        if not checks[name]:
            raise AssertionError(name)
    check('zero_speed_viscosity_limit', angular_fraction(0.0)==1.0)
    for y in (0.001,0.1,1.,10.,100.,10000.):
        check(f'bounded_angular_y{y}', 0.0<angular_fraction(y)<=1.0)
    scan=[]
    largest_refine_error=0.0
    for name, config in MODELS.items():
        sigma0 = config['sigma0_cm2_per_g']
        w = config['w_km_per_s']
        for s in DISPERSIONS_KM_S:
            f1 = speed_average(w,s,1)
            f5 = speed_average(w,s,5)
            f1_coarse=speed_average(w,s,1,n=6000)
            f5_coarse=speed_average(w,s,5,n=6000)
            largest_refine_error=max(largest_refine_error,abs(f1-f1_coarse),abs(f5-f5_coarse))
            check(f'{name}_{s:g}_heat_below_rate',0 < f5 <= f1 <= 1.0)
            scan.append({
                'model':name,'one_particle_1d_dispersion_km_per_s':s,
                'mean_relative_speed_km_per_s':4*s/math.sqrt(math.pi),
                'viscosity_rate_effective_cm2_per_g':sigma0*f1,
                'viscosity_v5_effective_cm2_per_g':sigma0*f5,
                'v5_over_v1':f5/f1,
                'viscosity_at_mean_speed_cm2_per_g':sigma0*angular_fraction((4*s/(w*math.sqrt(math.pi)))**2),
                'count_rate_effective_cm2_per_g':sigma0*speed_average(w,s,1,angular='total'),
            })
    check('resolution_stability',largest_refine_error<3e-9)
    # Normalization and the low-dispersion series are limiting-case diagnostics.
    for p in (1,5):
        s=0.025
        ratio=speed_average(120.,s,p)
        approx=1.0-2*(p+3)*(s/120.)**2
        check(f'low_dispersion_series_p{p}', abs(ratio-approx)<2e-12)
        check(f'constant_kernel_unit_p{p}', abs(speed_average(120.,0.,p)-1)<3e-12)
    check('mean_relative_speed_formula',abs(4*30/math.sqrt(math.pi)-67.702750)<1e-5)
    # Rate-matched, purely constructed shape control. It is not a particle-model fit.
    s=100.
    group_f1=speed_average(120.,s,1)
    group_f5=speed_average(120.,s,5)
    mw_f1=speed_average(24.3,s,1)
    mw_f5=speed_average(24.3,s,5)
    target_rate=147.1*group_f1
    tuned_sigma0=target_rate/mw_f1
    matched_heat=tuned_sigma0*mw_f5
    reference_heat=147.1*group_f5
    check('tuned_rate_is_equal',abs(tuned_sigma0*mw_f1-target_rate)<1e-11)
    check('heat_differs_with_equal_rate',abs(matched_heat-reference_heat)>1e-3)
    held_out=[]
    for dispersion in (30.,300.):
        r_a=147.1*speed_average(120.,dispersion,1)
        r_b=tuned_sigma0*speed_average(24.3,dispersion,1)
        held_out.append({'one_particle_1d_dispersion_km_per_s':dispersion,
                         'reference_v1_cm2_per_g':r_a,
                         'tuned_alternative_v1_cm2_per_g':r_b,
                         'alternative_over_reference':r_b/r_a})
    check('heldout_rate_separates_shapes',all(abs(t['alternative_over_reference']-1)>0.1 for t in held_out))
    output={
        'study':'S-03', 'as_of':'2026-10-22', 'status':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE'],
        'data_kind':'MODEL-CALCULATED; no halo events, observations or simulation snapshots',
        'published_model':'Nadler et al. 2503.10748v2 Eq(1), 29 Sep 2025',
        'prior_art_heat_kernel':'Fischer et al. MNRAS 529 (2024), Eq(9), based on Yang & Yu (2022)',
        'assumptions':['independent isotropic one-particle Gaussian velocity vectors',
                       'relative Maxwell speed law with 1D component dispersion sqrt(2)*s',
                       'velocity kernel at a single location with constant scalar dispersion',
                       'viscosity angular definition (3/2) integral[-1,1] (1-mu^2) dsigma/dmu',
                       'v^5 is a published effective-scattering proxy, not directly heat flux',
                       'no density evolution, baryons, merger streaming or self-consistent halo physics'],
        'equations':{'maxwell_relative_speed_density':'f(v)=v^2/(2 sqrt(pi) s^3) exp[-v^2/(4s^2)]',
                     'rate_proxy':'R1=<v sigma_V(v)>/<v>',
                     'thermal_proxy':'R5=<v^5 sigma_V(v)>/<v^5>',
                     'small_dispersion':'Rp/sigma0=1-2(p+3)*(s/w)^2+O((s/w)^4)'},
        'models':MODELS,'samples':scan,
        'matched_rate_control':{'one_particle_1d_dispersion_km_per_s':s,
                                'same_v1_effective_cm2_per_g':target_rate,
                                'GroupSIDM_sigma0_cm2_per_g':147.1,
                                'MilkyWay_shape_calibrated_sigma0_cm2_per_g':tuned_sigma0,
                                'GroupSIDM_v5_effective_cm2_per_g':reference_heat,
                                'MilkyWay_shape_v5_effective_cm2_per_g':matched_heat,
                                'v5_ratio_model_B_over_A':matched_heat/reference_heat,
                                'heldout_dispersions':held_out,
                                'warning':'SIMULATED model shape control, not observed/allowed couplings'},
        'validation':{'max_grid_refinement_abs_fraction_error':largest_refine_error,
                      'coarse_intervals':6000,'fine_intervals':12000,'speed_u_upper_bound':10.0,
                      'checks':checks,'checks_passed':sum(checks.values()),'checks_total':len(checks),
                      'seed':None,'randomness':'none','workers':1},
        'limitations':['not an N-body or hydrodynamic reproduction',
                       'effective thermal-scattering proxy not identical to halo heat conductivity',
                       'rate-matched alternative changes sigma0 without checking particle constraints',
                       'one radial velocity dispersion does not specify a merger velocity distribution',
                       'no observational likelihood or covariance fitted'],
        'environment':{'python':platform.python_version()},
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    outfile=ROOT/'results.json'
    outfile.write_text(json.dumps(output,indent=2,sort_keys=True,allow_nan=False)+'\n')
    recovered=json.loads(outfile.read_text())
    assert recovered['validation']['checks_passed']==recovered['validation']['checks_total']
    print(json.dumps({'checks':recovered['validation']['checks_passed'],
                      'max_grid_error':largest_refine_error,
                      'matched':output['matched_rate_control'],
                      'scan':scan},indent=2))

if __name__=='__main__':
    main()
