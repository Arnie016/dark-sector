#!/usr/bin/env python3
"""D-01: SIMULATED expected-rate modulation and uptime alias audit.
No observed events, no microscopic material model, no Poisson significance.
One bounded deterministic CPU run; Python + numpy/matplotlib preinstalled.
"""
import json, csv, hashlib, platform, time
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
DAY_SECONDS=86400.0
SID_SECONDS=86164.0905
FSID=DAY_SECONDS/SID_SECONDS # cycles per solar day
B0=100.0  # illustrative total background events/(kg day)
A_SOL=15.0 # invented solar variation, events/(kg day)
A_SID=8.0 # invented sidereal signal, events/(kg day)
PHASE_SOL=0.37
PHASE_SID=0.81
STEPS_PER_DAY=96
NAMES=['constant','cos(solar)','sin(solar)','cos(sidereal)','sin(sidereal)']

def design(n_days,mask):
    t=(np.arange(n_days*STEPS_PER_DAY)+0.5)/STEPS_PER_DAY
    h=(t%1)*24
    days=np.floor(t).astype(int)
    full=np.ones(t.size,dtype=float)
    if mask=='night+maintenance':
        full=np.where(((h>=21)|(h<5))&(days%11!=0),1.,0.)
    cs=np.cos(2*np.pi*t); ss=np.sin(2*np.pi*t)
    cd=np.cos(2*np.pi*FSID*t); sd=np.sin(2*np.pi*FSID*t)
    X=np.stack([np.ones_like(t),cs,ss,cd,sd],axis=1)
    exposure=full/STEPS_PER_DAY # kg.day for mass 1kg per live 15-minute bin
    return t, X, exposure

def get_study(n_days,mask):
    t,X,exposure=design(n_days,mask)
    active=exposure>0
    X=X[active]; wt=exposure[active]
    # Poisson Fisher at a CONSTANT background expectation b0. First order weak-signal approximation.
    F=(X.T*(wt/B0))@X
    fnn=F[:3,:3]; fns=F[:3,3:]; fss=F[3:,3:]
    Fe=fss-fns.T@np.linalg.solve(fnn,fns)
    Fe=(Fe+Fe.T)/2
    # Information fraction: eigenvalues relative to no nuisance profiling, bounded [0,1].
    ev,V=np.linalg.eigh(fss)
    root_inv=(V/np.sqrt(ev))@V.T
    ratios=np.linalg.eigvalsh(root_inv@Fe@root_inv)
    # Direct projection in weighted observation space as an independent linear algebra calculation.
    N=X[:,:3]; S=X[:,3:]
    fit=np.linalg.lstsq((N*np.sqrt(wt[:,None])),S*np.sqrt(wt[:,None]),rcond=None)[0]
    resid=S-N@fit
    fdirect=(resid.T*wt/B0)@resid
    err=np.max(np.abs(fdirect-Fe))
    # SIMULATED Asimov expected rate, NO random event counts.
    solar=B0+A_SOL*np.cos(2*np.pi*t[active]+PHASE_SOL)
    ysolar=solar
    proj_basis=X[:,[0,3,4]]
    fitted_sid=np.linalg.lstsq(proj_basis*np.sqrt(wt[:,None]),ysolar*np.sqrt(wt),rcond=None)[0]
    false_amp=float(np.linalg.norm(fitted_sid[1:]))
    # Alternative, correct simultaneous nuisance fit for solar-only data.
    all_fit=np.linalg.lstsq(X*np.sqrt(wt[:,None]),ysolar*np.sqrt(wt),rcond=None)[0]
    correct_amp=float(np.linalg.norm(all_fit[3:]))
    # injected solar+sidereal, joint fit in the noise-free expected rates.
    both=solar+A_SID*np.cos(2*np.pi*FSID*t[active]+PHASE_SID)
    both_fit=np.linalg.lstsq(X*np.sqrt(wt[:,None]),both*np.sqrt(wt),rcond=None)[0]
    recovered_amp=float(np.linalg.norm(both_fit[3:]))
    phi_direction=np.array([np.cos(PHASE_SID),-np.sin(PHASE_SID)])
    known_phase_ratio=float((phi_direction@Fe@phi_direction)/(phi_direction@fss@phi_direction))
    return {'days':n_days,'mask':mask,'live_kg_days':float(wt.sum()),'duty_fraction':float(wt.sum()/n_days),'worst_phase_information_fraction':float(ratios[0]),'best_phase_information_fraction':float(ratios[1]),'known_injected_phase_information_fraction':known_phase_ratio,'false_sidereal_amplitude_if_solar_ignored_events_per_kgday':false_amp,'fitted_sidereal_amplitude_with_solar_nuisance_solar_only':correct_amp,'injected_sidereal_amplitude_events_per_kgday':A_SID,'joint_asimov_recovered_amplitude':recovered_amp,'matrix_projection_max_difference':float(err),'profile_fisher_eigenvalues':np.linalg.eigvalsh(Fe).tolist()}

start=time.monotonic()
rows=[]
for d in [30,90,180,365]:
    for m in ['continuous','night+maintenance']:
        rows.append(get_study(d,m))
checks={
 'sidereal_period_less_than_solar':SID_SECONDS<DAY_SECONDS,
 'near_one_annual_cycle_difference':abs((FSID-1)*365.2422-1)<1e-5,
 'all_profile_information_in_0_1':all(-1e-8<=r['worst_phase_information_fraction']<=r['best_phase_information_fraction']<=1+1e-8 for r in rows),
 'projection_two_implementations':all(r['matrix_projection_max_difference']<1e-9 for r in rows),
 'no_false_detection_when_solar_profiled':all(r['fitted_sidereal_amplitude_with_solar_nuisance_solar_only']<1e-7 for r in rows),
 'asimov_joint_fit_recovers_injection':all(abs(r['joint_asimov_recovered_amplitude']-A_SID)<1e-7 for r in rows),
 'profiles_more_reliably_with_long_baseline':rows[0]['worst_phase_information_fraction']<rows[6]['worst_phase_information_fraction'],
 'masked_uptime_less_than_full':all(rows[i+1]['duty_fraction']<rows[i]['duty_fraction'] for i in range(0,len(rows),2)),
 'zero_injected_signal_not_claimed_as_data':True,
}
assert all(checks.values()), checks
# Explicit exact-frequency degeneracy limiting case: nuisance contains all sidereal templates if periods equal.
D=90; _, X, e=design(D,'continuous'); X=X[e>0]; w=e[e>0]/B0
N=X[:,:3]; S_equal=X[:,1:3]; F_equal=(N.T*w)@N
P_eq=(S_equal.T*w)@S_equal-(S_equal.T*w)@N@np.linalg.solve(F_equal,(N.T*w)@S_equal)
checks['equal_solar_sidereal_frequency_is_unidentifiable']=bool(np.max(np.abs(P_eq))<1e-9)
assert checks['equal_solar_sidereal_frequency_is_unidentifiable']

with (OUT/'SIMULATED_summary.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=[k for k in rows[0] if k!='profile_fisher_eigenvalues']);writer.writeheader();writer.writerows([{k:v for k,v in row.items() if k!='profile_fisher_eigenvalues'} for row in rows])

fig,ax=plt.subplots(figsize=(9.2,5.4))
for mask in ['continuous','night+maintenance']:
    subset=[r for r in rows if r['mask']==mask]
    ax.plot([r['days'] for r in subset],[100*r['worst_phase_information_fraction'] for r in subset],marker='o',label=('Continuous 24 h' if mask=='continuous' else 'SIMULATED 8 h daily + every 11th day off'))
ax.set(xlabel='Elapsed calendar time (solar days)',ylabel='Worst-phase sidereal information retained after profiling (%)',title='SIMULATED: solar-day backgrounds hide short-baseline sidereal signals',ylim=(0,106))
ax.grid(alpha=.22);ax.legend(loc='lower right',fontsize=9)
fig.text(.5,.02,'Exposure masks and harmonic rates are invented. Not an event-rate forecast or detected modulation.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.05,1,1));fig.savefig(OUT/'SIMULATED_identifiability.png',dpi=220)
plt.close(fig)

result={'study_id':'D-01','date':'2026-10-17','status':['DERIVED','SIMULATION_RESULT','DATA_INSUFFICIENT'],'meaning':'Deterministic SIMULATED rate/Fisher audit, not observations or material sensitivity','inputs':{'solar_day_seconds':DAY_SECONDS,'sidereal_day_seconds':SID_SECONDS,'sidereal_cycles_per_solar_day':FSID,'samples_per_day':STEPS_PER_DAY,'detector_mass_kg':1,'background_rate_events_per_kgday':B0,'solar_cosine_amplitude_events_per_kgday':A_SOL,'injected_sidereal_amplitude_events_per_kgday':A_SID,'solar_phase_rad':PHASE_SOL,'sidereal_phase_rad':PHASE_SID,'uptime_mask':'21:00-05:00 solar clock, every day except day index multiple 11','random_seed':None,'random_draws':0},'method':'Expected-rate least squares and leading background-dominated Poisson Fisher; nuisance basis constant+unknown-phase solar 24 h sine/cosine; candidate signal unknown-phase sidereal sine/cosine. Profile by Schur complement. Ratios relative to same-mask unprofiled Fisher, not detection power.','rows':rows,'checks':checks,'check_count':len(checks),'limitations':['No actual detector timestamps, live-time or efficiency masks','Signal pure sidereal cosine with fixed amplitude and phase; true DM wind has annual amplitude/phase evolution','No material response or target angular scattering calculation','No Poisson sampling, upper limit or statistical discovery significance','Asimov real-valued expected counts, not measured integer events','Solar background only sinusoidal; harmonics, drift, seasonal components could worsen identifiability','No experimental event-rate parameter priors or sensor calibration'],'source_methods':['https://arxiv.org/html/2602.15947v1 Sections II,III,V,VI','https://journals.aps.org/prd/abstract/10.1103/c9fm-ymf2'], 'runtime_s':float(time.monotonic()-start),'environment':{'python':platform.python_version(),'numpy':np.__version__,'platform':platform.platform()},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
assert json.loads((OUT/'results.json').read_text())['check_count']==len(checks)
print('script sha',result['code_sha256']);print('checks',checks)
for r in rows:print(r['days'],r['mask'],'duty',round(r['duty_fraction'],3),'info(worst)',round(r['worst_phase_information_fraction'],6),'info(best)',round(r['best_phase_information_fraction'],6),'false amplitude',round(r['false_sidereal_amplitude_if_solar_ignored_events_per_kgday'],6))
print('runtime',result['runtime_s'])
