#!/usr/bin/env python3
"""S-02 reproducible transport-vs-counting SIDM differential cross-section audit.
Source model: SIDM Concerto arXiv:2503.10748v2, Eq. (1). All outputs are
DERIVED or MODEL_CALCULATED, never telescope data or reproduced N-body halos.
No random draws. Python standard library only.
Run: python run.py --output results.json
"""
import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

MODELS = {
    "GroupSIDM": {"sigma0_over_m_cm2_per_g": 147.1, "w_km_per_s": 120.0},
    "GroupSIDM-70": {"sigma0_over_m_cm2_per_g": 70.0, "w_km_per_s": 120.0},
    "MilkyWaySIDM": {"sigma0_over_m_cm2_per_g": 147.1, "w_km_per_s": 24.3},
}
VELOCITIES_KM_S = [0.0, 10.0, 30.0, 120.0, 300.0, 1000.0]

def fractions(v, w):
    """Analytically angle-integrated total and (3/2)-normalized viscosity cross sections."""
    y=(v/w)**2
    total = 1.0/(1.0+y)
    if y < 0.025:
        # Positive-powers expansion avoids catastrophic subtraction for y << 1.
        term=1.0
        visc=0.0
        for n in range(160):
            add=6.0*(n+1.0)*term/((n+2.0)*(n+3.0))
            visc+=add
            term*=-y
            if abs(add)<1e-16: break
    else:
        visc=6.0*((y+2.0)*math.log1p(y)-2.0*y)/(y**3)
    return total,visc

def numeric_simpson(v,w,n=100000):
    """Independent angular quadrature directly in mu=cos(theta), not the analytic formula."""
    if n%2: raise ValueError("Simpson intervals must be even")
    y=(v/w)**2
    h=2.0/n
    count=0.0; visc=0.0
    for i in range(n+1):
        mu=-1+i*h
        differential=0.5/(1.0+0.5*y*(1.0-mu))**2
        k=1.0 if i in (0,n) else (4.0 if i%2 else 2.0)
        count+=k*differential
        visc+=k*1.5*(1.0-mu**2)*differential
    return count*h/3.0,visc*h/3.0

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,default=Path('results.json'))
    args=p.parse_args()
    check={}
    def assert_check(name, pass_value):
        check[name]=bool(pass_value)
        if not check[name]: raise AssertionError(name)

    calculations=[]; biggest=0.0
    for name, model in MODELS.items():
        w=model['w_km_per_s']; s=model['sigma0_over_m_cm2_per_g']
        for v in VELOCITIES_KM_S:
            total,visc=fractions(v,w)
            # Independently integrate directly over cos(theta); more points in the forward peak.
            numeric_tot,numeric_vis=numeric_simpson(v,w)
            err=max(abs(total-numeric_tot),abs(visc-numeric_vis))
            biggest=max(err,biggest)
            assert_check(f'{name}_v{v:g}_angular_integral',err<1e-5)
            assert_check(f'{name}_v{v:g}_positivity', 0<=visc<=total+1e-10 and total<=1+1e-12)
            calculations.append({
                'model':name,'v_rel_km_s':v, 'transition_w_km_s':w,
                'sigma_total_over_m_cm2_per_g':s*total,
                'sigma_viscosity_over_m_cm2_per_g':s*visc,
                'viscosity_over_total':visc/total,
                'quadrature_error_max_dimensionless':err
            })
    assert_check('zero_velocity_total_equals_reference',fractions(0,120)==(1.,1.))
    assert_check('low_velocity_limit', abs(fractions(1e-6,120)[1]-1)<1e-13)
    assert_check('high_velocity_viscosity_more_suppressed',fractions(1000,24.3)[1]<fractions(1000,24.3)[0])
    assert_check('amplitude_scaling',abs(MODELS['GroupSIDM']['sigma0_over_m_cm2_per_g']/MODELS['GroupSIDM-70']['sigma0_over_m_cm2_per_g']-147.1/70)<1e-12)

    # 1D unit control: (g/cm^3)*(cm^2/g)*(cm/s)=s^-1, no cosmological claim.
    seconds_per_gyr=365.25*24*3600*1e9
    rho=1e-25
    v_cms=1000*1e5
    totals,viscous=fractions(1000,120)
    s=MODELS['GroupSIDM']['sigma0_over_m_cm2_per_g']
    result={
        'study_id':'S-02','as_of':'2026-10-21',
        'statuses':['DERIVED','MODEL_CALCULATED'],
        'data_kind':'NO OBSERVATIONS. Analytic and deterministic numerical integration of published differential scattering law.',
        'source':'Nadler et al., SIDM Concerto, arXiv:2503.10748v2 Eq. 1, 29 September 2025',
        'definition':{'mu':'cos(theta)', 'd_sigma_d_mu':'sigma0 / (2*(1+(v/w)^2*(1-mu)/2)^2)',
                      'sigma_total':'integral[-1,1] d_sigma_d_mu dmu',
                      'sigma_viscosity':'(3/2)*integral[-1,1] (1-mu^2)*d_sigma_d_mu dmu',
                      'y':'(v/w)^2',
                      'total_over_sigma0':'1/(1+y)',
                      'viscosity_over_sigma0':'6*((y+2)*log(1+y)-2*y)/y^3, with low-y series limit 1',
                      'viscosity_normalization':'For isotropic scattering sigma_V=sigma_tot.'},
        'models':MODELS,'velocity_samples_km_per_s':VELOCITIES_KM_S,
        'samples':calculations,
        'illustrative_fixed_density_event_scales':{
            'rho_g_per_cm3':rho,'relative_speed_km_per_s':1000.,'model':'GroupSIDM',
            'count_rate_per_Gyr':rho*(s*totals)*v_cms*seconds_per_gyr,
            'viscosity_weighted_rate_per_Gyr':rho*(s*viscous)*v_cms*seconds_per_gyr,
            'note':'Fixed-density, fixed-speed rate proxies; NOT a thermodynamic relaxation/core-collapse time.'},
        'validation':{'checks_passed':sum(check.values()),'checks_total':len(check),
                      'largest_angular_integral_difference_dimensionless':biggest,
                      'num_simpson_intervals_per_row':100000,
                      'independent_numeric_control':'Simpson integration over cos(theta)',
                      'no_randomness':True,'seed':None,'workers':1},
        'limitations':[
            'Published differential model, no particle potential/Lagrangian inferred or N-body code run.',
            'Viscosity cross-section is an angle-weighted transport proxy, not measured heating.',
            'Fixed relative speeds do not replace distribution averages or heat-conduction simulation.',
            'No claim of model fit to galaxy/cluster constraints; cluster and dwarf systems differ in selection/merger histories.'
        ],
        'environment':{'python':platform.python_version()},
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    verified=json.loads(args.output.read_text())
    assert verified['validation']['checks_total']==verified['validation']['checks_passed']
    print(json.dumps({'checks':verified['validation']['checks_passed'],'max_difference':biggest,
                      'illustrative_Gyr_rates':verified['illustrative_fixed_density_event_scales'],
                      'code_sha256':result['source_sha256']},indent=2))

if __name__=='__main__':
    main()
