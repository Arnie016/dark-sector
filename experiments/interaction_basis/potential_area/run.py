#!/usr/bin/env python3
"""N-06: bounded forward-potential-area audit; assumed density models, no observations.
Python 3 standard library. Reproduce with: python run.py --output results.json
All numeric density choices are model inputs, not calibrated measured spikes.
"""
import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

# Codata / conventional values; SI unless stated.
G = 6.67430e-11  # m^3 kg^-1 s^-2
C_LIGHT = 299792458.0  # m/s
MSUN = 1.98847e30  # kg
PC = 3.085677581491367e16  # m
HBARC_EV_M = 1.973269804e-7  # eV m
HBARC_EV_CM = HBARC_EV_M * 100.0  # eV cm
GF_GEV2 = 1.1663787e-5  # GeV^-2

# Explicit SIMULATED/assumed AGN benchmark from Dev et al., arXiv:2609.26773v1 sec. III.
MBH_MSUN = 1e7
RS_PC = 2 * G * MBH_MSUN * MSUN / (C_LIGHT**2 * PC)
R_SPIKE_PC = 700.0
R_NFW_PC = 13000.0
RHO_S_GEV_CM3 = 0.35
R_EMISSION_PC = 1e-5
HALO_RHO_GEV_CM3 = 0.4  # separate illustrative Galactic density
HALO_PATH_PC = 10000.0
C_EFT = 1.0
LAMBDA_GEV = 1000.0
MCHI_GEV = 1.0
ASYMMETRY = 1.0  # (n_chi - n_antichi)/(n_chi+n_antichi)

def nfw_density(r_pc):
    t = r_pc / R_NFW_PC
    return RHO_S_GEV_CM3 / (t*(1+t)**2)

RHO_R = nfw_density(R_SPIKE_PC) / (1-4*RS_PC/R_SPIKE_PC)**3

def spike_density(r_pc):
    if r_pc < 4*RS_PC or r_pc > R_SPIKE_PC:
        return 0.0
    return RHO_R * (1-4*RS_PC/r_pc)**3 * (R_SPIKE_PC/r_pc)**(7/3)

def integrate_log_simpson(fn, lo_pc, hi_pc, n):
    # For r=exp(t), dr=r dt; integrate rho(r)*r over logarithmic radii.
    assert n > 0 and n % 2 == 0
    lo, hi = math.log(lo_pc), math.log(hi_pc)
    h = (hi-lo)/n
    terms=[]
    for i in range(n+1):
        t=lo+i*h
        radius=math.exp(t)
        val=fn(radius)*radius
        terms.append((1 if i in (0,n) else 4 if i%2 else 2)*val)
    return math.fsum(terms)*h/3  # (GeV cm^-3) pc

def epsilon_dimless(lam_gev, coupling):
    return (coupling/lam_gev**2)/(2*math.sqrt(2)*GF_GEV2)

def phase_area(column_gev_cm3_pc, lam_gev=LAMBDA_GEV, mchi_gev=MCHI_GEV, asym=ASYMMETRY, coupling=C_EFT):
    # V = C*Delta n/Lambda^2; Delta n=(asym)*rho/mchi in cm^-3.
    # Convert n_cm^-3 -> eV^3 via (hbar*c)^3, then path to eV^-1.
    n_column_cm3_pc = asym*column_gev_cm3_pc/mchi_gev
    return abs(coupling)*n_column_cm3_pc*(HBARC_EV_CM**3)/(lam_gev*1e9)**2*(PC/HBARC_EV_M)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('results.json'))
    a=parser.parse_args()
    assert 4*RS_PC < R_EMISSION_PC < R_SPIKE_PC < R_NFW_PC
    # One deterministic bounded numerical audit, with grid-refinement controls.
    sp={str(n):integrate_log_simpson(spike_density,R_EMISSION_PC,R_SPIKE_PC,n) for n in (2048,4096,8192)}
    ext={str(n):integrate_log_simpson(nfw_density,R_SPIKE_PC,HALO_PATH_PC,n) for n in (2048,4096,8192)}
    spike_col=sp['8192']; outer_col=ext['8192']
    halo_col=HALO_RHO_GEV_CM3*HALO_PATH_PC
    phase_spike=phase_area(spike_col)
    phase_outer=phase_area(outer_col)
    phase_halo=phase_area(halo_col)
    vac_scale_ev=2.5e-3/(4*1e14)  # Delta m^2 / (4 E), E=100TeV = 1e14eV
    potential_at_prod_eV=(RHO_R and spike_density(R_EMISSION_PC)/MCHI_GEV*(HBARC_EV_CM**3)/(LAMBDA_GEV*1e9)**2)
    # A potential-area bound: |Delta P| <= min(1,2*integral||delta H||dr/(hbar*c)).
    checks={
      'source_outside_horizon': 4*RS_PC < R_EMISSION_PC,
      'nonnegative_density': all(spike_density(r)>=0 for r in (R_EMISSION_PC,1e-4,.01,1,100)),
      'spike_matches_nfw_at_radius': abs(spike_density(R_SPIKE_PC)/nfw_density(R_SPIKE_PC)-1)<1e-10,
      'simpson_spike_convergence': abs(sp['8192']-sp['4096'])/spike_col<1e-7,
      'simpson_outer_convergence': abs(ext['8192']-ext['4096'])/outer_col<1e-8,
      'symmetric_DM_vector_potential_null': phase_area(spike_col,asym=0)==0,
      'doubling_lam_quarters_phase': abs(phase_area(spike_col,lam_gev=2000)/phase_spike-.25)<1e-14,
      'halving_mass_doubles_phase': abs(phase_area(spike_col,mchi_gev=.5)/phase_spike-2)<1e-14,
      'rescaling_asym_scales_linearly': abs(phase_area(spike_col,asym=.1)/phase_spike-.1)<1e-14,
      'halo_constant_column_check': halo_col==4000.0,
      'small_halo_upper_bound': 2*phase_halo<1e-9,
      'local_potential_smaller_than_vacuum_scale': potential_at_prod_eV<vac_scale_ev,
    }
    if not all(checks.values()):
        raise AssertionError({k:v for k,v in checks.items() if not v})
    result={
      'study_id':'N-06','as_of':'2026-10-21','status':['DERIVED','SIMULATION_RESULT','DATA_INSUFFICIENT'],
      'data_kind':'SIMULATED MODEL DENSITY; no observed events or calibrated halo measurement',
      'source':'Dev, Gaido, Ibarra, Porto, arXiv:2609.26773v1 (2026-09-22), Section III; density profile parameters assumed by authors',
      'theory':'C/Lambda^2 * (nu-current)(chi-vector-current), contact limit, maximally asymmetric benchmark; toy e-mu off-diagonal shares potential norm, not demonstrated viable UV completion',
      'inputs':{'MBH_Msun':MBH_MSUN,'Schwarzschild_radius_pc':RS_PC,'r_emission_pc':R_EMISSION_PC,'r_spike_pc':R_SPIKE_PC,'r_NFW_pc':R_NFW_PC,'rho_s_GeV_per_cm3':RHO_S_GEV_CM3,'rho_emission_GeV_per_cm3':spike_density(R_EMISSION_PC),'rho_local_GeV_per_cm3':HALO_RHO_GEV_CM3,'halo_path_pc':HALO_PATH_PC,'mchi_GeV':MCHI_GEV,'Lambda_GeV':LAMBDA_GEV,'C':C_EFT,'asymmetry_fraction':ASYMMETRY,'neutrino_energy_TeV':100.0,'atmospheric_Delta_m2_eV2':.0025},
      'integral_rho_dr_GeV_per_cm3_pc':{'spike_2048':sp['2048'],'spike_4096':sp['4096'],'spike_8192':spike_col,'outer_8192':outer_col,'uniform_halo_10kpc':halo_col},
      'predictions':{'epsilon_equivalent_to_2sqrt2GF':epsilon_dimless(LAMBDA_GEV,C_EFT),
       'potential_at_emission_eV':potential_at_prod_eV,'vacuum_delta_scale_eV':vac_scale_ev,
       'potential_to_vacuum_ratio_at_emission':potential_at_prod_eV/vac_scale_ev,
       'integrated_norm_phase_spike':phase_spike,
       'integrated_norm_phase_outer_to_10kpc':phase_outer,
       'integrated_norm_phase_10kpc_uniform_halo':phase_halo,
       'conservative_probability_shift_upper_spike':min(1,2*phase_spike),
       'conservative_probability_shift_upper_halo':min(1,2*phase_halo),
       'Lambda_GeV_for_spike_probability_bound_0p1':LAMBDA_GEV*math.sqrt(2*phase_spike/.1),
       'symmetric_dark_bath_bound':0.0},
      'checks':checks,'checks_passed':sum(checks.values()),
      'limitations':['Perturbation norm bound is a worst-case ceiling, not a predicted flavor fraction or detector sensitivity.','Weak/flat radial path dr: near-horizon GR propagation and redshift corrections omitted.','Density spike and maximally asymmetric charge are assumptions of a source benchmark, not independently measured.','No neutrino production mixture, PMNS 3-flavor evolution, detector efficiency, covariance or charged-lepton viability fit.','A single conventional or novel forward potential can be observationally degenerate with source/ordinary NSI nuisances.'],
      'runtime':{'workers':1,'random_seed':None,'method':'deterministic log-Simpson quadrature','python':platform.python_version()},
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    assert json.loads(a.output.read_text())['checks_passed']==len(checks)
    print(json.dumps({'phase_spike':phase_spike,'phase_halo':phase_halo,'spike_column':spike_col,'spike_bound':2*phase_spike,'epsilon':epsilon_dimless(LAMBDA_GEV,C_EFT),'checks':len(checks),'sha':result['code_sha256']},indent=2))
if __name__=='__main__':main()
