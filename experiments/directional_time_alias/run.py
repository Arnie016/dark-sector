#!/usr/bin/env python3
"""D-01: SIMULATED exposure geometry, not dark-matter detector rates.
One deterministic, bounded Fisher-design test, without random draws.
Requires numpy. Run: python run.py --output results.json
"""
import argparse, hashlib, json, math, platform, time
from pathlib import Path
import numpy as np
YEAR_DAYS=365.2422
OMEGA_SOL=2*math.pi
OMEGA_SID=2*math.pi*(1+1/YEAR_DAYS)
HOURS=tuple(range(8,16)) # 8 hourly observations per solar day

def sample(days):
    # Each hourly grid center is a hypothetical valid observation, equal weight.
    return np.asarray([d+(h+0.5)/24 for d in days for h in HOURS],dtype=float)

def orth(A):
    # Orthogonal columns for nuisance basis; singularity indicates badly posed nuisance design.
    u,s,v=np.linalg.svd(A,full_matrices=False)
    if s[-1] < 1e-11*s[0]:
        raise AssertionError('nuisance basis singular')
    return u

def trial(label,blocks,independent_bg):
    days=[d for block in blocks for d in block]
    t=sample(days)
    block_id=np.asarray([k for k,blk in enumerate(blocks) for d in blk for _ in HOURS],dtype=int)
    columns=[(block_id==k).astype(float) for k in range(len(blocks))]
    base=np.column_stack(columns)
    csol=np.cos(OMEGA_SOL*t)
    ssol=np.sin(OMEGA_SOL*t)
    if independent_bg:
        for k in range(len(blocks)):
            gate=(block_id==k)
            columns.extend((csol*gate,ssol*gate))
    else:columns.extend((csol,ssol))
    nuisance=np.column_stack(columns)
    sid=np.column_stack((np.cos(OMEGA_SID*t),np.sin(OMEGA_SID*t)))
    q0=orth(base); sid0=sid-q0@(q0.T@sid)
    qsid=orth(sid0)
    qn=orth(nuisance)
    res=qsid-qn@(qn.T@qsid)
    eig=np.linalg.eigvalsh(res.T@res)
    return {'mask':label,'days':len(days),'samples':len(t),'live_hours':len(t),
      'nuisance_parameters':int(nuisance.shape[1]),'retained_information_worst_phase':float(eig[0]),
      'retained_information_best_phase':float(eig[1]),'worst_phase_sd_inflation':float(1/math.sqrt(max(eig[0],1e-30))),
      'sidereal_solar_period_difference_minutes':float((1-1/(1+1/YEAR_DAYS))*1440),
      'condition_scope':'equal-variance Gaussian rate residuals; phase amplitudes free; no Poisson count model'}

def run():
    b30=list(range(30)); b60=list(range(60)); b365=list(range(365)); b30late=list(range(180,210))
    return [trial('30-day_contiguous_global_solar', [b30],False),
        trial('60-day_contiguous_global_solar',[b60],False),
        trial('30-plus-30_gap180_global_solar',[b30,b30late],False),
        trial('30-plus-30_gap180_each_campaign_solar',[b30,b30late],True),
        trial('365-day_contiguous_global_solar',[b365],False)]

def checks(rows):
    r={x['mask']:x for x in rows}; short=r['30-day_contiguous_global_solar']; cont=r['60-day_contiguous_global_solar'];gap=r['30-plus-30_gap180_global_solar'];free=r['30-plus-30_gap180_each_campaign_solar'];full=r['365-day_contiguous_global_solar']
    # Nulls: same-frequency solar/sidereal cannot be distinguished even with long timeline.
    ts=sample(range(30)); sol=np.column_stack((np.ones(len(ts)),np.cos(OMEGA_SOL*ts),np.sin(OMEGA_SOL*ts)))
    ss=np.column_stack((np.cos(OMEGA_SOL*ts),np.sin(OMEGA_SOL*ts)))
    q=orth(sol)
    exact_null=np.linalg.norm(ss-q@(q.T@ss)) / np.linalg.norm(ss)
    results={
      'all_fractions_between_zero_and_one': all(0<=x['retained_information_worst_phase']<=x['retained_information_best_phase']<=1+1e-10 for x in rows),
      'same-frequency-null':exact_null<1e-12,
      '60-days-improves-on-30-days':cont['retained_information_worst_phase']>short['retained_information_worst_phase'],
      'separated-campaigns-improve-if-solar-background-is-shared':gap['retained_information_worst_phase']>cont['retained_information_worst_phase'],
      'independent-solar-campaign-backgrounds-reduce-information':free['retained_information_worst_phase']<gap['retained_information_worst_phase'],
      'one-year-gives-more-information-than-short-30-day-window':full['retained_information_worst_phase']>short['retained_information_worst_phase'],
      'equal-live-hours-across-two-60-day-masks':gap['live_hours']==cont['live_hours']==free['live_hours']==480,
      'sidereal-period-shorter-than-solar':all(3<x['sidereal_solar_period_difference_minutes']<5 for x in rows)
    }
    results={k:bool(v) for k,v in results.items()}
    assert all(results.values()),results
    return results,float(exact_null)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='results.json');arg=ap.parse_args()
    start=time.perf_counter(); rows=run(); validations,exactnull=checks(rows)
    path=Path(__file__); payload={'id':'D-01','date':'2026-10-23','status':'SIMULATION_RESULT','synthetic':True,
        'parameters':{'solar_period_days':1,'sidereal_period_days':1/(1+1/YEAR_DAYS),'beat_days':YEAR_DAYS,'solar_hours_each_day':list(HOURS),'weights':'uniform/equal','random_seed':None},
        'scenarios':rows,'checks':validations,'checks_passed':len(validations),'same_frequency_null_relative_residual':exactnull,
        'method':'SVD orthonormal subspace projection; eigenvalues of retained Fisher information for sidereal cosine/sine after profiling backgrounds',
        'limitations':['No detector response, events, environmental diagnostics or count-rate model','Solar/sidereal only constant-phase harmonics: actual dark-wind phase and amplitude drift seasonally','Equal independent Gaussian rate residuals rather than Poisson low-count likelihood','Phase coherence across seasons is assumed for the global-solar background hypothesis','Prior-art known frequency separation, not a new particle discovery'],
        'code_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'runtime_seconds':time.perf_counter()-start,
        'platform':platform.platform(),'numpy_version':np.__version__}
    Path(arg.output).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(validations),'runtime_seconds':payload['runtime_seconds'],'cases':[{k:x[k] for k in ('mask','retained_information_worst_phase','retained_information_best_phase','worst_phase_sd_inflation')} for x in rows]},indent=2))
if __name__=='__main__':main()
