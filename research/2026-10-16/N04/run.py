#!/usr/bin/env python3
"""N-04: SIMULATED two-state phase modulation, exposure alias, and a null.
No observational data. Standard library only. Deterministic, no RNG.
Run: python run.py [output-dir]
"""
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

A = 0.30             # relative neutrino phase amplitude, radians
C = 0.80             # incoming mass-state coherence, not a coupling
PERIOD_H = 24.0      # stress-test field period, not measured
DAYS = 12
PER_DAY = 96         # 15-minute bins
N = DAYS * PER_DAY

def j_series(n, x):
    return sum((-1)**k * (x/2)**(2*k+n) /
               (math.factorial(k)*math.factorial(k+n)) for k in range(24))

def p_plus(x, delta, a=A, c=C):
    return 0.5 * (1 + c*math.cos(delta + a*math.cos(x)))

phase = [2*math.pi*((i+0.5)%PER_DAY)/PER_DAY for i in range(N)]
odd = [p_plus(x, math.pi/2) for x in phase]
even = [p_plus(x, 0) for x in phase]
live = [math.cos(x)>0 for x in phase]  # SIMULATED 12-hour nightly outage
avg = lambda x: sum(x)/len(x)
coeff = lambda y,k: 2*avg([v*math.cos(k*x) for x,v in zip(phase,y)])
j0,j1,j2 = [j_series(k,A) for k in (0,1,2)]
odd_mean = avg(odd)
even_mean = avg(even)
live_mean = avg([p for p,l in zip(odd,live) if l])
# An exact detector-efficiency countermodel for the two channels.
# Signal hypothesis: true P(t), time-constant efficiency 0.4 both channels.
# Null hypothesis: true P=0.5, with efficiencies eps+(t), eps-(t).
# Both predict identical observed channel rates for an arbitrary source flux.
eff0 = 0.4
eps_plus = [2*eff0*p for p in odd]
eps_minus = [2*eff0*(1-p) for p in odd]
null_error = max([abs(eff0*p-0.5*ep) for p,ep in zip(odd,eps_plus)] +
                 [abs(eff0*(1-p)-0.5*em) for p,em in zip(odd,eps_minus)])
checks = {
    'full_cycle_odd_mean_half': abs(odd_mean-0.5)<1e-14,
    'even_mean_J0':abs(even_mean-(1+C*j0)/2)<1e-14,
    'odd_first_harmonic_J1':abs(coeff(odd,1)+C*j1)<1e-13,
    'even_second_harmonic_J2':abs(coeff(even,2)+C*j2)<1e-13,
    'odd_second_harmonic_null':abs(coeff(odd,2))<1e-13,
    'even_first_harmonic_null':abs(coeff(even,1))<1e-13,
    'probabilities_bounded':all(0<=p<=1 for p in odd+even),
    'exact_half_uptime':sum(live)==N//2,
    'mask_shift':live_mean<0.45,
    'incoherent_null':all(abs(p_plus(x,math.pi/2,c=0)-0.5)<1e-14 for x in phase),
    'zero_field_limit':all(abs(p_plus(x,math.pi/2,a=0)-0.5)<1e-14 for x in phase),
    'instrumental_null_exact':null_error<1e-15 and all(0<=e<=1 for e in eps_plus+eps_minus)
}
assert all(checks.values()), {k:v for k,v in checks.items() if not v}
out = Path(sys.argv[1] if len(sys.argv)>1 else 'output')
out.mkdir(parents=True,exist_ok=True)
csv_path = out/'SIMULATED_time_bins.csv'
with csv_path.open('w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['time_hours','field_phase_rad','P_plus_Delta_pi_over_2','P_plus_Delta_0',
                'live_SIMULATED','eff_null_plus','eff_null_minus'])
    for i,x in enumerate(phase):
        w.writerow([f'{(i+0.5)*PERIOD_H/PER_DAY:.6f}',f'{x:.12g}',f'{odd[i]:.12g}',
                    f'{even[i]:.12g}',int(live[i]),f'{eps_plus[i]:.12g}',
                    f'{eps_minus[i]:.12g}'])
results={
 'id':'N-04','date':'2026-10-16',
 'status':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE','DATA_INSUFFICIENT'],
 'data_label':'SIMULATED deterministic model expectation, NOT observed events',
 'seed':None,'randomness':'none','workers':1,
 'units':{'time':'hours','phase':'radians','mass_energy':'eV','P':'dimensionless'},
 'truth':{'a_rad':A,'coherence_c':C,'period_h':PERIOD_H,'days':DAYS,
    'bins_per_period':PER_DAY,'vacuum_Delta_rad':[0,math.pi/2],
    'live_mask':'SIMULATED live when cos(field_phase)>0',
    'detector_countermodel':'fixed P=0.5; independently time-varying efficiencies'},
 'outputs':{'odd_full_cycle_mean':odd_mean,'even_full_cycle_mean':even_mean,
    'odd_live_weighted_mean':live_mean,'odd_cos_omega_coeff':coeff(odd,1),
    'even_cos_2omega_coeff':coeff(even,2),'J0':j0,'J1':j1,'J2':j2,
    'field_mass_equivalent_eV':4.135667696e-15/(PERIOD_H*3600),
    'instrument_null_max_count_rate_error':null_error},
 'checks':checks,'checks_passed':sum(checks.values()),
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'csv_sha256':hashlib.sha256(csv_path.read_bytes()).hexdigest(),
 'not_claimed':['real event inference','DM particle evidence','full three-flavor simulation',
                'estimated sensitivity','unique physical signature','measured 24-hour scalar wave']}
output=out/'results.json'
output.write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
assert json.loads(output.read_text())['checks_passed']==len(checks)
print(json.dumps({'passed':len(checks),'outputs':results['outputs'],
                  'source_sha256':results['source_sha256'],
                  'csv_sha256':results['csv_sha256']},indent=2))
