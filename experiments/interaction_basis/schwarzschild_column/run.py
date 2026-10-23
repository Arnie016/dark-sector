#!/usr/bin/env python3
"""N-07: Schwarzschild geometry gate for an assumed AGN dark-current column.
MODEL ONLY, not detector data or neutrino-flavor propagation. Python standard library.
One deterministic numerical study with documented limiting checks.
"""
import hashlib
import json
import math
import platform
from pathlib import Path

G = 6.67430e-11                 # m^3 kg^-1 s^-2
C = 299792458.0                 # m s^-1
M_SUN = 1.98847e30             # kg
PC_M = 3.085677581491367e16   # m / pc
HBARC_EV_M = 1.973269804e-7   # eV m
HBARC_EV_CM = HBARC_EV_M * 100 # eV cm

M_BH_SOLAR = 1e7
R_S = 2 * G * M_BH_SOLAR * M_SUN / (C*C*PC_M)  # pc, Schwarzschild radius
R_PRODUCTION = 1e-5            # pc (assumed)
R_SPIKE = 700.0                # pc
R_NFW = 13000.0                # pc
RHO_S = 0.35                   # GeV cm^-3
EFT_SCALE_GEV = 1000.0
DM_MASS_GEV = 1.0
ABS_NET_ASYMMETRY = 1.0
COUPLING_ABS = 1.0

def rho_nfw(r):
    x = r / R_NFW
    return RHO_S / (x * (1+x)**2)

RHO_R = rho_nfw(R_SPIKE) / (1 - 4*R_S/R_SPIKE)**3

def rho_spike(r):
    if r < 4*R_S or r > R_SPIKE:
        return 0.0
    return RHO_R * (1 - 4*R_S/r)**3 * (R_SPIKE/r)**(7/3)

def column(upper, n, geometry=True, r_min=R_PRODUCTION, metric_rs=R_S):
    """Integral in (GeV/cm^3)*pc, log-Simpson, static proper density in Schwarzschild geometry."""
    assert n > 0 and n%2 == 0 and 0 <= metric_rs < r_min < upper <= R_SPIKE
    a,b=math.log(r_min), math.log(upper)
    step=(b-a)/n
    terms=[]
    for j in range(n+1):
        r=math.exp(a+j*step)
        factor=1/math.sqrt(1-metric_rs/r) if geometry else 1.0
        terms.append((1 if j==0 or j==n else 4 if j%2 else 2)*rho_spike(r)*factor*r)
    return math.fsum(terms)*step/3

def phase_norm(col):
    """Same unit convention and illustrative EFT as historical N-06; dimensionless."""
    return COUPLING_ABS * ABS_NET_ASYMMETRY * (col/DM_MASS_GEV) * (HBARC_EV_CM**3) / (EFT_SCALE_GEV*1e9)**2 * PC_M/HBARC_EV_M

nlevels=[2048,4096,8192]
flat={str(n):column(R_SPIKE,n,False) for n in nlevels}
curved={str(n):column(R_SPIKE,n,True) for n in nlevels}
flat_num=flat['8192']
curved_num=curved['8192']
ratio=curved_num/flat_num
bound=1/math.sqrt(1-R_S/R_PRODUCTION)

# Independent analytical bounding logic: w(r) decreases from w(r_min) toward 1.
checks={
 'source_outside_horizon': R_PRODUCTION>4*R_S,
 'recovers_prior_flat_N06_column': abs(flat_num/44526996353547.5-1)<3e-12,
 'positive_integrands': all(rho_spike(r)>=0 for r in [R_PRODUCTION,2*R_PRODUCTION,0.01,1,100,R_SPIKE]),
 'curved_column_greater_than_flat': curved_num>flat_num,
 'monotonic_geometric_bound': 1 < ratio < bound,
 'convergence_flat':abs(flat['8192']-flat['4096'])/flat_num<1e-7,
 'convergence_curved':abs(curved['8192']-curved['4096'])/curved_num<1e-7,
 'weak_field_limit': abs(column(R_SPIKE,2048,True,metric_rs=0)/column(R_SPIKE,2048,False)-1)<1e-15,
 'phase_scales_with_column':abs(phase_norm(curved_num)/phase_norm(flat_num)-ratio)<1e-12,
 'local_weight_decreases_outward': (1/math.sqrt(1-R_S/R_PRODUCTION)) > (1/math.sqrt(1-R_S/(10*R_PRODUCTION))) > 1,
 'outer_increases_little': (column(R_SPIKE,2048,True,r_min=1e-4)/column(R_SPIKE,2048,False,r_min=1e-4)-1)<.006,
}
assert all(checks.values()), [k for k,v in checks.items() if not v]

# Contribution of physical radial shells: cumulative phase is dominated by inner region, but no new events.
radius_limits=[1e-5,2e-5,1e-4,1e-3,.01,.1,1,10,100,700]
cumulative=[]
for r in radius_limits[1:]:
    cumulative.append({'to_radius_pc':r,'flat_fraction':column(r,4096,False)/flat_num,'curved_fraction':column(r,4096,True)/curved_num})

results={
 'id':'N-07','as_of':'2026-10-23','status':['DERIVED','SIMULATION_RESULT','DATA_INSUFFICIENT'],
 'data_kind':'SIMULATED MODEL of an assumed AGN spike, not measured DM or IceCube data',
 'source_model':'arXiv:2609.26773v1 2026-09-22 Section III, parameters reused from N-06',
 'prior_art':'arXiv:2610.25053v1 2026-10-18 radial leading vacuum cancellation; older neutrino GR work Cardall-Fuller PRD 55 (1997)',
 'geometry':'Schwarzschild f=1-R_S/r, static local number density, outward radial null ray; neglect spike backreaction and rotation',
 'assumptions':{'R_S_pc':R_S,'M_BH_solar':M_BH_SOLAR,'r_emission_pc':R_PRODUCTION,'r_spike_pc':R_SPIKE,'r_NFW_pc':R_NFW,'rho_s_GeV_cm3':RHO_S,'density':'rho_R*(1-4R_S/r)^3*(R_sp/r)^(7/3)','C_abs':COUPLING_ABS,'Lambda_GeV':EFT_SCALE_GEV,'mchi_GeV':DM_MASS_GEV,'abs_asymmetry':ABS_NET_ASYMMETRY},
 'columns_GeV_cm_3_pc':{'flat':flat,'Schwarzschild_proper':curved},
 'geometry_ratio':ratio,
 'geometric_pointwise_upper_bound':bound,
 'enhancement_percent':(ratio-1)*100,
 'integrated_phase_norm':{'flat':phase_norm(flat_num),'Schwarzschild_proper':phase_norm(curved_num)},
 'worst_case_probability_difference_ceiling':{'flat':min(1,2*phase_norm(flat_num)), 'Schwarzschild_proper':min(1,2*phase_norm(curved_num))},
 'cumulative':cumulative,
 'checks':checks,'checks_passed':sum(checks.values()),
 'limitation':'The norm area is a ceiling, not a flavor transition probability. Fixed local density and constant asymmetry, no curved halo dynamics, no three-flavor full evolution, no source or detector likelihood.',
 'execution':{'python':platform.python_version(),'seed':None,'workers':1,'quadrature':'deterministic log-Simpson 2048/4096/8192 plus radial shell controls'},
 'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
}
output=Path(__file__).parent/'results.json'
output.write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
assert json.loads(output.read_text())['checks_passed']==len(checks)
print(json.dumps({'R_S_pc':R_S,'ratio':ratio,'ratio_upper_bound':bound,'flat_phase':phase_norm(flat_num),'proper_phase':phase_norm(curved_num),'old_ceiling':2*phase_norm(flat_num),'new_ceiling':2*phase_norm(curved_num),'counts':len(checks),'sha256':results['sha256'],'cumulative':cumulative},indent=2))
