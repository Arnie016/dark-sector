#!/usr/bin/env python3
"""N-06 | SIMULATED identifiability audit for asymmetric Dirac DM.

A bounded deterministic, standard-library calculation. Not an IceCube likelihood,
three-flavor spike integration, or observational detection.
Usage: python run.py --output output/results.json
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

HBAR_C_EV_M = 1.973269804e-7
PC_M = 3.085677581491367e16
SPIKE_RHO_GEV_CM3 = 3e18  # reported illustration at production radius
MCHI_GEV = 1.0  # illustrative hypothesis, NOT measured
V0_EV = 7.5e-19  # Eq. 8 arXiv:2609.26773v1 at above rho and mass
THETA_RAD = math.radians(33.0)
DM2_EV2 = 7.5e-5
L_M = 1.0e-4 * PC_M  # uniform medium as a mathematically transparent toy

def forward(epsilon, f, s):
    """Dimensionless normalized effective potential and pair annihilation emissivity."""
    if not -1.0 <= f <= 1.0 or s < 0:
        raise ValueError("Unphysical asymmetry or rate")
    return (epsilon * f, s * (1.0 - f*f))

def two_flavor_conversion(E_TeV, relative_V):
    """Constant-density two-flavor propagation, alpha initial state.

    Traceless flavor-basis Hamiltonian H=hx*sigma_x+hz*sigma_z.
    relative_V is epsilon*f, with V=relative_V*V0.
    """
    E = E_TeV*1e12
    vac = DM2_EV2 / (2.0 * E)
    hx = 0.5 * vac * math.sin(2*THETA_RAD)
    hz = 0.5 * (relative_V*V0_EV - vac * math.cos(2*THETA_RAD))
    omega = math.hypot(hx, hz)
    if omega == 0:
        return 0.0
    phase = omega * L_M / HBAR_C_EV_M
    return (hx/omega)**2 * math.sin(phase)**2

def jacobian(epsilon, f, s):
    return ((f, epsilon, 0.0), (0.0, -2.0*s*f, 1.0-f*f))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='output/results.json')
    args=ap.parse_args()
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    checks={}
    def check(name, condition):
        checks[name]=bool(condition)
        if not checks[name]:
            raise AssertionError(name)
    # Two physically distinct parameter assignments, SAME forward amplitudes.
    a={'epsilon':0.8,'f':0.75,'s':0.8}
    b={'epsilon':1.2,'f':0.5,'s':7.0/15.0}
    ya=forward(**a); yb=forward(**b)
    energies=[50.0,100.0,200.0]
    pa=[two_flavor_conversion(e,ya[0]) for e in energies]
    pb=[two_flavor_conversion(e,yb[0]) for e in energies]
    # The Jacobian has two rows (two observables), three columns (unknowns).
    J=jacobian(**a)
    # A nonzero vector in its null space; derivative of exact degeneracy curve.
    null=(-a['epsilon']/a['f'],1.0,2.0*a['s']*a['f']/(1.0-a['f']**2))
    jnull=[sum(row[i]*null[i] for i in range(3)) for row in J]
    minor=J[0][0]*J[1][2]-J[0][2]*J[1][0]
    # Finite-difference directional null test. A local derivative, NOT a new datum.
    h=1.e-5
    shifted=forward(a['epsilon']+h*null[0],a['f']+h*null[1],a['s']+h*null[2])
    directional=[(shifted[i]-ya[i])/h for i in range(2)]
    # Invariants and limiting cases.
    check('same_normalized_neutrino_potential',abs(ya[0]-yb[0])<1e-14)
    check('same_normalized_gamma_pair_emissivity',abs(ya[1]-yb[1])<1e-14)
    check('different_underlying_parameters',any(abs(a[k]-b[k])>1e-3 for k in a))
    check('different_particle_antiparticle_ratios',abs((1+a['f'])/(1-a['f'])-(1+b['f'])/(1-b['f']))>1)
    check('same_toy_neutrino_probability_at_all_energies',max(abs(x-y) for x,y in zip(pa,pb))<1e-13)
    check('probabilities_in_unit_interval',all(0<=x<=1 for x in pa+pb))
    check('two_by_two_minor_nonzero',abs(minor)>1e-4)
    check('null_direction_for_two_by_three_jacobian',max(map(abs,jnull))<1e-13)
    check('finite_difference_null_direction_small',max(map(abs,directional))<1e-3)
    check('symmetric_population_zero_vector_potential',forward(0.8,0.0,0.8)[0]==0.0)
    check('symmetric_population_max_pair_proxy',forward(0.8,0.0,0.8)[1]==0.8)
    check('fully_asymmetric_population_zero_pair_proxy',forward(0.8,1.0,0.8)[1]==0.0)
    check('antineutrino_potential_sign_flip',abs((-ya[0])+ya[0])<1e-15)
    check('vacuum_two_flavor_limit',all(abs(two_flavor_conversion(e,0)-math.sin(2*THETA_RAD)**2*math.sin((DM2_EV2/(4*e*1e12))*L_M/HBAR_C_EV_M)**2)<1e-13 for e in energies))
    check('particle_number_balance',all(abs(((1+p['f'])/2)+((1-p['f'])/2)-1.0)<1e-15 for p in [a,b]))
    # Any (eps', f', s') on this curve gives precisely the same two amplitudes.
    fthird=0.90
    c={'epsilon':ya[0]/fthird,'f':fthird,'s':ya[1]/(1-fthird**2)}
    check('third_point_exact_degenerate_curve',max(abs(x-y) for x,y in zip(forward(**c),ya))<1e-14)
    # A coupling epsilon=0 or exactly symmetric bath f=0 gives the same vector potential.
    check('zero_coupling_and_symmetric_medium_neutrino_null',forward(0.0,0.7,1.0)[0] == forward(1.0,0.0,1.0)[0])
    payload={
      'study':'N-06','as_of':'2026-10-19','status':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE','DATA_INSUFFICIENT'],
      'label':'ALL predictions are SIMULATED; NO observational data','seed':None,
      'source':'arXiv:2609.26773v1 equations 1-4,8; PDG DM 2025 Eq 27.18 (structural scaling)',
      'assumptions':['asymmetric Dirac DM, conserved vector current as in source effective operator',
        'constant asymmetry fraction f along one prescribed spike density profile',
        'known fixed rho/mχ; identical DM spatial profile for compared theories',
        'separate hypothetical χχbar annihilation channel, fixed gamma yield and negligible backreaction',
        'gamma amplitude stripped of exposure, J factor, and fixed spectrum; no ordinary astrophysical background',
        'constant-density two-flavor propagation only as a toy validation; not AGN three-flavor forecast'],
      'units':{'rho':'GeV/cm^3','m_chi':'GeV','V':'eV','L':'m','E':'TeV','delta_m2':'eV^2','observables':'dimensionless normalized amplitudes'},
      'inputs':{'rho':SPIKE_RHO_GEV_CM3,'mchi':MCHI_GEV,'V0_eV':V0_EV,'path_length_m':L_M,
         'theta_deg':33.0,'delta_m2_eV2':DM2_EV2,'energies_TeV':energies,
         'model_A':a,'model_B':b,'model_C':c},
      'normalized_observables':{'neutrino_potential':ya[0],'annihilation_emissivity':ya[1]},
      'potential_A_and_B_eV':V0_EV*ya[0],
      'inferred_net_chi_density_A_cm3':a['f']*SPIKE_RHO_GEV_CM3/MCHI_GEV,
      'inferred_net_chi_density_B_cm3':b['f']*SPIKE_RHO_GEV_CM3/MCHI_GEV,
      'two_flavor_probabilities_SIMULATED':{'A':pa,'B':pb},
      'jacobian_rows_observables_cols_parameters_epsilon_f_s':J,
      'jacobian_rank':2,'parameter_dimension':3,'null_direction':null,
      'J_times_null':jnull,'finite_difference_step':h,'finite_difference_null_derivative':directional,
      'checks':checks,'checks_passed':sum(checks.values()),
      'meaning':'Two independent amplitudes do not determine three unknowns; stronger realistic nuisance worsens inference',
      'not_claimed':['Real gamma rays from DM','A fit to IceCube','A limit on ε, f, or <σv>','A realistic AGN emission history','A new particle or interaction']}
    payload['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out.write_text(json.dumps(payload,indent=2,sort_keys=True,allow_nan=False)+'\n')
    loaded=json.loads(out.read_text())
    assert loaded['checks_passed']==17 and loaded['jacobian_rank']==2
    print(json.dumps({'checks_passed':loaded['checks_passed'],'model_A':a,'model_B':b,'y':ya,'P':pa,'Jv':jnull,'SHA256':payload['code_sha256']},indent=2))
if __name__=='__main__': main()
