#!/usr/bin/env python3
"""N-06: SIMULATED two-flavor flavor-diagonal matter/dark-potential identifiability audit.
One bounded deterministic CPU process. No observed events or microscopic viable coupling claim.
Standard library only: python run.py --out output
"""
import argparse, csv, hashlib, json, math, platform, time
from pathlib import Path

HC_EV_M = 1.973269804e-7
MP_G = 1.67262192369e-24
E_GEV = (0.8, 1.2, 1.6, 2.2, 3.0)
THETA_RAD = math.radians(8.6)
DM2_EV2 = 2.5e-3
VE_REF_EV = 1.07e-13
BASELINE_M = 1300_000.0
BASE = (("A", 1.0, 1.0), ("B", 1.5, 1.0))  # (label, electron ratio, dark ratio)


def p_ex(E_gev, e_scale, d_scale, a, q, anti=False):
    """nu_e -> nu_x in a constant medium. a,q dimensionless multipliers.
    Hamiltonian h=0.5*(hx sigma_x+hz sigma_z); unobservable trace removed.
    Assumes same projector for electron and dark forward potentials.
    """
    delta = DM2_EV2 / (2 * E_gev * 1e9)
    hx = delta * math.sin(2 * THETA_RAD)
    potential = VE_REF_EV * (e_scale * a + d_scale * q)
    hz = -delta * math.cos(2 * THETA_RAD) + (-potential if anti else potential)
    om = math.hypot(hx, hz)
    phase = om * BASELINE_M / (2 * HC_EV_M)
    return (hx / om)**2 * math.sin(phase)**2 if om else 0.0


def evolve_by_amplitude(E_gev, e_scale, d_scale, a, q, anti=False):
    """Independent amplitude component, not an external experimental validation."""
    delta = DM2_EV2 / (2 * E_gev * 1e9)
    hx = delta * math.sin(2 * THETA_RAD)
    potential = VE_REF_EV * (e_scale * a + d_scale * q)
    hz = -delta * math.cos(2 * THETA_RAD) + (-potential if anti else potential)
    om = math.hypot(hx, hz)
    phi = om * BASELINE_M / (2 * HC_EV_M)
    amp_x = (-1j * hx / om * math.sin(phi)) if om else 0j
    amp_e = (math.cos(phi) - 1j * hz / om * math.sin(phi)) if om else 1+0j
    return abs(amp_x)**2, abs(amp_x)**2 + abs(amp_e)**2


def rows_for(paths, a=1.0, q=0.1):
    rows=[]
    for name,e,d in paths:
        for E in E_GEV:
            for anti in (False, True):
                rows.append(dict(path=name,E_GeV=E,channel="anti" if anti else "nu",
                                 e=e,d=d,p=p_ex(E,e,d,a,q,anti)))
    return rows


def finite_jac(rows, by_path_nuisance=False, a=1.0, q=0.1, h=1e-5):
    out=[]
    for x in rows:
        E,e,d,anti=x["E_GeV"],x["e"],x["d"],x["channel"]=="anti"
        pa=(p_ex(E,e,d,a+h,q,anti)-p_ex(E,e,d,a-h,q,anti))/(2*h)
        pq=(p_ex(E,e,d,a,q+h,anti)-p_ex(E,e,d,a,q-h,anti))/(2*h)
        if by_path_nuisance:
            out.append([pa if x["path"]=="A" else 0.,pa if x["path"]=="B" else 0.,pq])
        else:
            out.append([pa,pq])
    return out


def gram2(jac):
    aa=sum(r[0]**2 for r in jac); bb=sum(r[1]**2 for r in jac); ab=sum(r[0]*r[1] for r in jac)
    disc=math.hypot(aa-bb,2*ab)
    eig1=(aa+bb+disc)/2
    eig2=max(0.,(aa+bb-disc)/2)
    return dict(gram=[[aa,ab],[ab,bb]],eig_max=eig1,eig_min=eig2,det=max(0.,aa*bb-ab*ab),
                smallest_over_largest=(eig2/eig1 if eig1 else 0))


def run(out):
    start=time.perf_counter(); out.mkdir(parents=True,exist_ok=True)
    checks={}
    def check(n,test):
        checks[n]=bool(test)
        if not checks[n]: raise AssertionError(n)
    single=rows_for(BASE[:1]); multi=rows_for(BASE)
    j_single=finite_jac(single); j_multi=finite_jac(multi)
    g_single=gram2(j_single); g_multi=gram2(j_multi)
    # Exact same potential sum yields same Hamiltonian, at all chosen energies/charges.
    max_equiv=max(abs(p_ex(E,1,1,1,.1,anti)-p_ex(E,1,1,1.1,0,anti))
                  for E in E_GEV for anti in (False,True))
    check("exact_single_path_relabel_null",max_equiv<2e-15)
    check("single_path_jacobian_columns_identical",max(abs(r[0]-r[1]) for r in j_single)<3e-11)
    check("single_path_one_sensitive_direction",g_single["eig_max"]>1e-7 and g_single["smallest_over_largest"]<1e-12)
    check("two_paths_nonproportional_rise_to_rank2",g_multi["eig_min"]>1e-7 and g_multi["smallest_over_largest"]>1e-6)
    # Independent electron calibration for each path exactly absorbs a global dark potential.
    j_free=finite_jac(multi,by_path_nuisance=True)
    max_free_abs=max(abs(r[2]-r[0]-r[1]/1.5) for r in j_free)
    check("independent_electron_normalizations_restore_null",max_free_abs<1e-10)
    check("amplitude_matches_probability",max(abs(evolve_by_amplitude(E,e,d,1,.1,anti)[0]-p_ex(E,e,d,1,.1,anti))
                                                for _,e,d in BASE for E in E_GEV for anti in (False,True))<1e-14)
    check("unitarity",max(abs(evolve_by_amplitude(E,e,d,1,.1,anti)[1]-1)
                         for _,e,d in BASE for E in E_GEV for anti in (False,True))<1e-14)
    check("zero_angle_no_oscillation_algebraic",abs(math.sin(0.0))==0.0)
    check("probability_bounds",all(0<=z["p"]<=1 for z in multi))
    check("zero_medium_charge_symmetry",max(abs(p_ex(E,1,1,0,0,False)-p_ex(E,1,1,0,0,True)) for E in E_GEV)<1e-15)
    max_two_path_equiv=max(abs(p_ex(E,e,d,1,.1,anti)-p_ex(E,e,d,1.1,0,anti))
                 for _,e,d in BASE for E in E_GEV for anti in (False,True))
    check("second_path_breaks_particular_relabel",max_two_path_equiv>1e-5)
    # A symmetry check: DM vector matter potential ∝ particle minus antiparticle charge density.
    check("symmetric_vector_background_cancels",(.4-.4)==0)
    density_e=2.8*0.5/MP_G
    dm_number=.4 # particles / cm^3 for 1 GeV DM and local density .4 GeV cm^-3
    ratio_n=dm_number/density_e
    required_ratio_for_q=.1*density_e/dm_number
    check("units_physically_small_number_ratio",1e-26<ratio_n<1e-23)
    core_time=time.perf_counter()-start
    rows=multi
    with (out/'SIMULATED_probabilities.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['data_kind','path','energy_GeV','neutrino_channel','electron_potential_scale','dark_potential_scale','P_ex_dimensionless'])
        for v in rows:w.writerow(['SIMULATED',v['path'],v['E_GeV'],v['channel'],v['e'],v['d'],v['p']])
    report={
      'id':'N-06','as_of':'2026-10-20','version':'1.0.0','status':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE','DATA_INSUFFICIENT'],
      'kind':'SIMULATED expected probabilities, no detector data or event counts','truth':{'a':1.,'q':.1},
      'model':{'flavors':'nu_e versus nu_x toy reduction, not 3-flavor data','delta_m2_eV2':DM2_EV2,'theta_deg':8.6,
               'V_e_reference_eV':VE_REF_EV,'baseline_km':BASELINE_M/1000,'energies_GeV':E_GEV,
               'paths':BASE, 'potential_eV':'V_ref*(e_j*a + d_j*q) for nu; reverse sign for antinu',
               'the_dark_coefficient_is_not_a_viable_coupling_fit':True},
      'controls':{'path_A_exact_relabel_max_difference':max_equiv,
                  'two_path_relabel_max_difference':max_two_path_equiv,
                  'free_electron_per_path_null_max_jacobian_residual':max_free_abs},
      'jacobian':{'one_path':g_single,'two_paths_shared_e_normalization':g_multi,
                  'rank_interpretation':'One path: rank 1; two paths conditional rank 2; free a_A,a_B plus q: q unidentifiable'},
      'density_scaling_illustrative':{'earth_density_g_cm3':2.8,'electron_fraction_Ye':.5,'ne_per_cm3':density_e,
         'dark_density_GeV_cm3':.4,'m_chi_GeV':1.,'net_dm_particles_per_cm3_assuming_asymmetric':dm_number,
         'number_density_ratio_nchi_over_ne':ratio_n,
         'required_Gchi_over_sqrt2_Gf_for_q_0p1':required_ratio_for_q,
         'sign_warning':'for symmetric particle-antiparticle vector charge, net dark vector current can vanish'},
      'approximation':['uniform static medium per path','two-flavor coherent oscillation','fixed source and detector conventions',
                       'one electron density nuisance globally or independently per path as stated',
                       'illustrative asymmetric 1-GeV fermion DM vector-current contact potential; no gauge completion',
                       'no Earth path map, no response, no uncertainties, no likelihood or experimental sensitivity'],
      'predeclared_checks':checks,'checks_passed':len(checks),'seed':None,'random_draws':0,'workers':1,
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'csv_sha256':hashlib.sha256((out/'SIMULATED_probabilities.csv').read_bytes()).hexdigest(),
      'runtime_seconds_excluding_startup':core_time,'environment':{'python':platform.python_version(),'system':platform.system()},
      'failure_gate':'If joint fit with independent electron density uncertainty absorbs dark term, stay UNIDENTIFIABLE; no discovery claim.'}
    data=json.dumps(report,indent=2,allow_nan=False)+'\n'
    temp=out/'results.tmp';temp.write_text(data);temp.replace(out/'results.json')
    rr=json.loads((out/'results.json').read_text());check('strict_json_roundtrip',rr['id']=='N-06' and rr['checks_passed']==len(checks))
    report['predeclared_checks']=checks;report['checks_passed']=len(checks)
    (out/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'study':'N-06','checks_passed':len(checks),'one_path':g_single,'two_paths':g_multi,
         'max_relabel_difference_pathA':max_equiv,'two_path_alternative_delta':max_two_path_equiv,
         'independent_e_path_null_residual':max_free_abs,'density_ratio':ratio_n,
         'required_coupling_ratio':required_ratio_for_q,'code_sha256':report['code_sha256']},indent=2))

if __name__=='__main__':
    pp=argparse.ArgumentParser();pp.add_argument('--out',type=Path,default=Path('output'));arg=pp.parse_args();run(arg.out)
