#!/usr/bin/env python3
"""N-06: two-flavor adiabatic forward-scattering identifiability, SIMULATED.
No detector events, AGN propagation, or 3-flavor likelihood are claimed.
Run python run.py. Standard library only. Deterministic.
"""
import csv, hashlib, json, math, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
GF_EV2=1.1663787e-23 # eV^-2
HBARC=1.973269804e-5 # eV cm
RHO=3e18 # GeV / cm^3; CONDITIONAL spike benchmark, 2609.26773
THETA=math.radians(33.0) # illustrative
DM2=7.5e-5 # eV^2, illustrative two-flavor splitting
E_TEV=[10.,20.,40.,80.,100.,300.,1000.]
TRIPLETS=[(1.,.5,1.),(2.,.5,2.),(5.,.2,2.)] # epsilon, asymmetry eta, mchi GeV

def potential(par,rho=RHO):
    eps,eta,m=par
    return 2*math.sqrt(2)*GF_EV2*eps*eta*(rho/m)*HBARC**3

def prob(EteV,V,anti=False):
    # adiabatic pure electron-type production; incoherent mass eigenstates at vacuum detector
    d=DM2/(2*EteV*1e12)
    v=-V if anti else V
    c2m=(d*math.cos(2*THETA)-v)/math.hypot(d*math.cos(2*THETA)-v,d*math.sin(2*THETA))
    return .5*(1+math.cos(2*THETA)*c2m)

def feature(p):
    v=potential(p)
    return [prob(e,v,anti) for anti in (False,True) for e in E_TEV]

def main():
    checks={}
    def chk(k,v):
        checks[k]=bool(v)
        if not v: raise AssertionError(k)
    qs=[a*b/c for a,b,c in TRIPLETS]
    vv=[potential(p) for p in TRIPLETS]
    vac=1-0.5*math.sin(2*THETA)**2
    rows=[{'energy_TeV':E,'SIMULATED_nu_e_adiabatic_Pee':prob(E,vv[0]),
           'SIMULATED_antinu_e_adiabatic_Pee':prob(E,vv[0],True),
           'SIMULATED_symmetric_DM_Pee':prob(E,0)} for E in E_TEV]
    chk('distinct_parameters',len(set(TRIPLETS))==3)
    chk('identical_epsilon_eta_over_mass',max(abs(q-qs[0]) for q in qs)<1e-15)
    chk('identical_potentials',max(abs(v-vv[0]) for v in vv)<1e-32)
    chk('identical_energy_predictions',max(abs(a-b) for p in TRIPLETS for a,b in zip(feature(p),feature(TRIPLETS[0])))<1e-14)
    chk('eta_zero_vector_null',potential((100.,0.,1.))==0)
    chk('symmetric_DM_vacuum',max(abs(r['SIMULATED_symmetric_DM_Pee']-vac) for r in rows)<1e-14)
    chk('nu_antinu_sign_control',max(abs(prob(E,v,True)-prob(E,-v)) for E in E_TEV for v in vv)<1e-14)
    chk('finite_and_unit_interval',all(0<=v<=1 for row in rows for key,v in row.items() if key!='energy_TeV'))
    chk('nonzero_change_positive_eta',max(abs(r['SIMULATED_nu_e_adiabatic_Pee']-vac) for r in rows)>.1)
    chk('low_energy_vacuum_limit',abs(prob(1e-6,vv[0])-vac)<1e-7)
    chk('large_mass_vacuum_limit',abs(prob(100,potential((1,.5,1e20)))-vac)<1e-12)
    # Numerical Jacobian of synthetic output with respect to three log parameters.
    h=1e-5
    jac=[]
    for i in range(3):
        p1=list(TRIPLETS[0]);p2=list(TRIPLETS[0]);p1[i]*=math.exp(h);p2[i]*=math.exp(-h)
        jac.append([(a-b)/(2*h) for a,b in zip(feature(p1),feature(p2))])
    d12=max(abs(a-b) for a,b in zip(jac[0],jac[1]))
    d13=max(abs(a+b) for a,b in zip(jac[0],jac[2]))
    chk('log_parameter_jacobian_rank_at_most_1',max(d12,d13)<1e-10)
    chk('nonzero_response_gradient',max(abs(x) for x in jac[0])>.03)
    chk('flavor_universal_potential_is_identity',all(abs(prob(E,vv[0]-vv[0])-vac)<1e-14 for E in E_TEV))
    chk('density_ratio_order_of_magnitude',math.isclose(RHO/.3,1e19,rel_tol=1e-12))
    Eres=DM2*math.cos(2*THETA)/(2*vv[0])/1e12
    chk('resonance_inside_energy_grid',20<Eres<100)
    chk('phase_averaged_resonance_Pee_half',abs(prob(Eres,vv[0])-.5)<1e-13)
    path=HERE/'SIMULATED_energy_scan.csv'
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    results={
        'claim_id':'N-06-C1','as_of':'2026-10-21',
        'status':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE'],
        'evidence_kind':'SIMULATED two-flavor adiabatic model; zero observed events',
        'generating_truth':{'theta_degrees':33,'delta_m2_eV2':DM2,'rho_GeV_cm3':RHO,
                          'rho_is_not_measured':True,'parameter_triplet':TRIPLETS[0],
                          'sample_model':'pure nu_e production, slow adiabatic density falloff, decohered vacuum mass states'},
        'input_triplets_epsilon_eta_massGeV':TRIPLETS,
        'energies_TeV':E_TEV,'V_eV':vv[0],'resonance_energy_TeV':Eres,
        'vacuum_averaged_Pee':vac,'simulated_predictions':rows,
        'log_jacobian_max_abs_col1_minus_col2':d12,
        'log_jacobian_max_abs_col1_plus_col3':d13,
        'parameter_sensitivity_rank_upper_bound':1,
        'checks':checks,'checks_passed':len(checks),
        'seed':None,'random_draws':0,'workers':1,
        'assumptions':['nonrelativistic DM fermion and antifermion with vector contact interactions',
                       'DM net number density = eta rho/m, eta in [-1,1]',
                       'production at prescribed density; two-flavor adiabatic limit; vacuum phase averaging',
                       'no nonadiabatic transitions, full 3-flavor dynamics, attenuation, source or detector likelihood'],
        'not_claimed':['reproduced 2609.26773','new detector bound','particle discovery','actual DM density or asymmetry measurement'],
        'sources':['arXiv:2609.26773, v1 first posted 2026-09-22, Sections II-IV and Appendix A',
                   'PDG neutrino mixing 2025, Section 14.5',
                   'IceCube arXiv:2510.24957, 11.4-year MESE flavor analysis'],
        'csv_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python':sys.version.split()[0]}
    out=HERE/'results.json'; out.write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
    assert json.loads(out.read_text())['checks_passed']==len(checks)
    print(json.dumps({'checks':len(checks),'V_eV':vv[0],'resonance_TeV':Eres,'vacuum_Pee':vac,
                      'rows':rows,'jacobian_max_differences':[d12,d13],
                      'code_sha256':results['code_sha256']}))
if __name__=='__main__':main()
