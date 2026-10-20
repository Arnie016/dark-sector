"""N-06: two-flavor, source-slab matter-potential identifiability audit.
SIMULATED constant slabs, not a 3-flavor AGN spike or IceCube likelihood.
Only standard-library Python. Reproduce: python run.py --output output
"""
import argparse, cmath, csv, hashlib, json, math, platform, time
from pathlib import Path

# Physical units: E, H and V in eV, L in cm; natural-unit phase H*L/(hbar*c).
GF_EV_MINUS2 = 1.1663787e-23
HBARC_EVCM = 1.973269804e-5
PC_CM = 3.085677581491367e18
DM_COEFF = 2*math.sqrt(2)*GF_EV_MINUS2*HBARC_EVCM**3
ELECTRON_COEFF = math.sqrt(2)*GF_EV_MINUS2*HBARC_EVCM**3
THETA = math.radians(33.4) # illustrative 2-state angle, not a 3-flavor fit
DELTA_M2_EV2 = 7.42e-5 # illustrative solar scale
SLAB_CM = 1e-4*PC_CM # deliberately constant and synthetic
RHO_GEV_CM3 = 4e18 # synthetic spike-like density benchmark
MCHI_GEV = 1.
EPS_MU = -1.
DM_ASYMMETRY = 1.
V0 = DM_COEFF * (RHO_GEV_CM3/MCHI_GEV) * abs(EPS_MU)*DM_ASYMMETRY
NE0 = V0/ELECTRON_COEFF
ENERGIES_TEV = [30, 50, 75, 100, 150, 200, 300]


def prob_earth_e(E_TeV, V_e, V_mu, source_flavor='mu', slab_cm=SLAB_CM):
    """Exact 2x2 constant-H unitary, then incoherent *vacuum-mass* projection."""
    E = E_TeV*1e12
    c, s = math.cos(THETA), math.sin(THETA)
    k = DELTA_M2_EV2/(4*E)
    h00, h11, off = -k*math.cos(2*THETA)+V_e, k*math.cos(2*THETA)+V_mu, k*math.sin(2*THETA)
    tr, d = (h00+h11)/2, (h00-h11)/2
    omega = math.hypot(d,off)
    ell=slab_cm/HBARC_EVCM
    factor=cmath.exp(-1j*tr*ell)
    cs=math.cos(omega*ell)
    sinc=math.sin(omega*ell)/omega if omega else ell
    u00=factor*(cs-1j*d*sinc)
    u11=factor*(cs+1j*d*sinc)
    u01=factor*(-1j*off*sinc)
    psi_e,psi_mu=(u00,u01) if source_flavor=='e' else (u01,u11)
    mass1=c*psi_e-s*psi_mu
    mass2=s*psi_e+c*psi_mu
    p_mass1=abs(mass1)**2
    p_mass2=abs(mass2)**2
    p_earth_e=c*c*p_mass1+s*s*p_mass2
    return {'p_e':p_earth_e, 'norm':abs(psi_e)**2+abs(psi_mu)**2,
            'p_mass1':p_mass1,'p_mass2':p_mass2}


def run(out):
    started=time.perf_counter()
    out.mkdir(parents=True,exist_ok=True)
    checks={}
    def ck(k, v):
        checks[k]=bool(v)
        if not v: raise AssertionError(k)
    pairs=[]
    for energy in ENERGIES_TEV:
        vacuum=prob_earth_e(energy,0,0)
        # Exactly the same effective flavor splitting for source A: ordinary e vs dark mu.
        normal_a=prob_earth_e(energy,V0,0)
        dark_a=prob_earth_e(energy,0,-V0)
        # At source B, the independently stipulated plasma and net-DM columns differ.
        normal_b=prob_earth_e(energy,0.05*V0,0)
        dark_b=prob_earth_e(energy,0,-0.60*V0)
        # A symmetric particle/antiparticle population has no net vector current.
        symmetric=prob_earth_e(energy,0,-V0*0)
        # Scale m_chi and eps_mu together at fixed mass density and asymmetry.
        rescaled=prob_earth_e(energy,0,-DM_COEFF*(RHO_GEV_CM3/2.)*2.)
        common=prob_earth_e(energy,V0,V0)
        pure_e=prob_earth_e(energy,V0,0,'e')
        ck('vacuum_mass_averaged_'+str(energy),abs(vacuum['p_e']-0.5*math.sin(2*THETA)**2)<2e-14)
        ck('flavor_summed_source_'+str(energy),abs(pure_e['p_e']+normal_a['p_e']-1)<2e-14)
        ck('source_A_indistinguishable_'+str(energy),abs(normal_a['p_e']-dark_a['p_e'])<2e-14)
        ck('charge_symmetric_vector_null_'+str(energy),abs(vacuum['p_e']-symmetric['p_e'])<2e-14)
        ck('universal_potential_null_'+str(energy),abs(vacuum['p_e']-common['p_e'])<2e-14)
        ck('coupling_mass_rescaling_null_'+str(energy),abs(dark_a['p_e']-rescaled['p_e'])<2e-14)
        for tag,a in [('vacuum',vacuum),('ordinary_A',normal_a),('dark_A',dark_a),('ordinary_B',normal_b),('dark_B',dark_b),('symmetric_DM',symmetric)]:
            ck('norm_'+tag+'_'+str(energy),abs(a['norm']-1)<2e-14 and 0 <= a['p_e'] <= 1)
        pairs.append({'energy_TeV':energy,'SIMULATED_vacuum_pe':vacuum['p_e'],
           'SIMULATED_sourceA_ordinary_pe':normal_a['p_e'],
           'SIMULATED_sourceA_dark_pe':dark_a['p_e'],
           'SIMULATED_sourceB_ordinary_pe':normal_b['p_e'],
           'SIMULATED_sourceB_dark_pe':dark_b['p_e'],
           'SIMULATED_sourceB_dark_minus_ordinary':dark_b['p_e']-normal_b['p_e']})
    ck('source_B_separates_models_in_restricted_oracle', max(abs(r['SIMULATED_sourceB_dark_minus_ordinary']) for r in pairs)>1e-4)
    ck('vector_coefficient_double_electron_coefficient',abs(DM_COEFF/ELECTRON_COEFF-2)<1e-14)
    # Flavor-degenerate directions: adding common V(r)I is a path-dependent phase,
    # scaling eps and mass together leaves the product eps*rho*A/m unchanged.
    cfile=out/'SIMULATED_probabilities.csv'
    with cfile.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(pairs[0])); writer.writeheader(); writer.writerows(pairs)
    result={
     'claim_id':'N-06-C1','date':'2026-10-20','status':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE','DATA_INSUFFICIENT'],
     'data_kind':'SIMULATED constant-density two-flavor slab, NO telescope events',
     'seed':None,'randomness':'none','assumptions':["two flavors only", "static and uniform slab of 1e-4 pc", "vacuum mass-state phase averaging after slab", "neutrino rather than antineutrino", "source flavor pure mu", "source B matter densities treated as independently known oracle values", "no attenuation, QFT gauge completion, or real detector response"],
     'inputs':{'theta_deg':33.4,'delta_m2_eV2':DELTA_M2_EV2,'length_pc':1e-4,
       'energies_TeV':ENERGIES_TEV,'rho_DM_GeV_cm3':RHO_GEV_CM3,'mchi_GeV':MCHI_GEV,
       'asymmetry':DM_ASYMMETRY,'epsilon_mu':EPS_MU,'sourceA_electron_cm3':NE0,
       'sourceA_net_DM_cm3':RHO_GEV_CM3/MCHI_GEV,
       'sourceB_electron_relative_to_A':0.05,'sourceB_net_DM_relative_to_A':0.60,
       'DM_coeff_eV_cm3':DM_COEFF,'electron_coeff_eV_cm3':ELECTRON_COEFF,
       'potential_abs_eV':V0},
     'rows':pairs,
     'max_sourceA_abs_difference':max(abs(r['SIMULATED_sourceA_dark_pe']-r['SIMULATED_sourceA_ordinary_pe']) for r in pairs),
     'max_sourceB_abs_difference':max(abs(r['SIMULATED_sourceB_dark_minus_ordinary']) for r in pairs),
     'checks_passed':sum(checks.values()),'checks_total':len(checks),
     'checks':checks,
     'identifiability':['only flavor-potential differences matter', 'only product epsilon*asymmetry*rho_DM/mchi is constrained at fixed shape','ordinary and dark mechanisms with same potential-difference profile cannot be separated by flavor propagation alone','a freely adjustable source flavor composition can restore additional degeneracies'],
     'not_claimed':['three-flavor physical forecast','three-flavor MSW profile reproduction','AGN gas or dark matter density measurement','IceCube likelihood or flavor sensitivity','new particle or novel theorem'],
     'environment':{'python':platform.python_version(),'system':platform.system(),'workers':1},
     'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'csv_sha256':hashlib.sha256(cfile.read_bytes()).hexdigest(),
     'wall_seconds':time.perf_counter()-started}
    p=out/'results.json'; p.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n'); assert json.loads(p.read_text())['checks_passed']==len(checks)
    print(json.dumps({k:result[k] for k in ('claim_id','max_sourceA_abs_difference','max_sourceB_abs_difference','checks_passed','checks_total','wall_seconds')},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('output'));run(ap.parse_args().output)
