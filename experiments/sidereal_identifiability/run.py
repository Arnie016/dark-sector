#!/usr/bin/env python3
"""DIR-20261019-C1. Deterministic SIMULATED timing-design audit.
No detector event data, material response, Poisson likelihood or sensitivity claim.
"""
import hashlib, json, math, platform
from pathlib import Path
import numpy as np

DAY = 86400.0
YEAR = 365.2422
SID = DAY * YEAR/(YEAR+1.0)
STEP = 3600.0

def design(days,mask):
    t=(np.arange(days*24, dtype=float)+.5)*STEP
    d=np.floor(t/DAY).astype(int)
    h=(t%DAY)/3600.
    live=np.ones(len(t),dtype=bool) if mask=='full' else ((d%7)<5)&((h>=18)|(h<6))
    return t[live]

def matrices(t):
    so=2*np.pi*t/DAY
    si=2*np.pi*t/SID
    return np.column_stack((np.ones(len(t)),np.cos(so),np.sin(so))),np.column_stack((np.cos(si),np.sin(si)))

def project_away(x,z):
    return x-z@np.linalg.lstsq(z,x,rcond=None)[0]

def information(t):
    b,s=matrices(t)
    s0=project_away(s,b[:,:1]); sp=project_away(s,b)
    g0=s0.T@s0; gp=sp.T@sp
    values,vectors=np.linalg.eigh(g0)
    if values.min() <=1.e-8: raise ValueError('singular baseline')
    inv=(vectors/np.sqrt(values))@vectors.T
    eig=np.linalg.eigvalsh(inv@gp@inv)
    return {'observed_hours':len(t),'information_fraction_worst':float(eig[0]),
       'information_fraction_best':float(eig[1]),
       'noise_inflation_worst':float(1/math.sqrt(max(eig[0],1e-30))),
       'design_rank':int(np.linalg.matrix_rank(np.column_stack((b,s)),tol=1e-8))}

def holdout(mask):
    train=design(7,mask)
    valid=design(187,mask)
    valid=valid[(valid>=180*DAY)&(valid<187*DAY)]
    truth=lambda t:1.+.05*np.cos(2*np.pi*t/DAY+.4)
    b0,s0=matrices(train); b1,s1=matrices(valid)
    c0=np.column_stack((np.ones(len(train)),s0));c1=np.column_stack((np.ones(len(valid)),s1))
    w=np.linalg.lstsq(c0,truth(train),rcond=None)[0]
    s=np.linalg.lstsq(b0,truth(train),rcond=None)[0]
    rms=lambda a:float(np.sqrt(np.mean(a*a)))
    return {'truth':'SIMULATED solar-only relative rate 1+0.05*cos(2*pi*t/86400+0.4); zero sidereal',
      'train_days':'[0,7)','heldout_days':'[180,187)',
      'train_observed_hours':len(train),'heldout_observed_hours':len(valid),
      'solar_fit_train_rms':rms(b0@s-truth(train)),
      'solar_fit_heldout_rms':rms(b1@s-truth(valid)),
      'wrong_sidereal_fit_train_rms':rms(c0@w-truth(train)),
      'wrong_sidereal_fit_heldout_rms':rms(c1@w-truth(valid)),
      'wrong_sidereal_fit_coefficients':[float(v) for v in w]}

def main():
    cases=[]
    for mask in ('full','weekday_nights'):
        for days in (7,30,90,365):
            x=information(design(days,mask));x.update(mask=mask,elapsed_days=days,live_fraction=x['observed_hours']/(24*days));cases.append(x)
    hh=holdout('weekday_nights')
    checks={}
    def check(name,x):
        checks[name]=bool(x)
        if not checks[name]: raise AssertionError(name)
    check('sidereal_shorter_than_solar',SID<DAY)
    check('annual_beat_identity',abs(DAY/SID-1-1/YEAR)<1e-13)
    check('weekday_night_reduced_exposure',all(x['live_fraction']<1 for x in cases if x['mask']=='weekday_nights'))
    check('all_five_columns_full_rank',all(x['design_rank']==5 for x in cases))
    check('information_between_zero_and_one',all(-1e-11<=x['information_fraction_worst']<=x['information_fraction_best']<=1+1e-11 for x in cases))
    check('seven_days_almost_collinear',all(x['information_fraction_worst']<.01 for x in cases if x['elapsed_days']==7))
    check('year_recoverable',all(x['information_fraction_worst']>.90 for x in cases if x['elapsed_days']==365))
    check('information_growth',all(np.all(np.diff([x['information_fraction_worst'] for x in cases if x['mask']==mask])>0) for mask in ('full','weekday_nights')))
    check('correct_solar_fit_recovers_holdout',hh['solar_fit_heldout_rms']<1e-12)
    check('incorrect_sidereal_fit_fails_holdout',hh['wrong_sidereal_fit_heldout_rms']>10*hh['wrong_sidereal_fit_train_rms'])
    result={'claim_id':'DIR-20261019-C1','as_of':'2026-10-19','status':['DERIVED','SIMULATION_RESULT','DATA_INSUFFICIENT'],
      'input':{'solar_day_s':DAY,'sidereal_day_s':SID,'year_days':YEAR,'sample_hours':1,
        'mask_full':'100%','mask_weekday_nights':'18:00-06:00 each day_index%7<5; 0 otherwise',
        'zero_randomness':True,'seed':None,'mask_is_SIMULATED':True},
      'physical_observable':'none; timing design and template identifiability only',
      'mathematics':'least squares profile out intercept and unknown-phase solar sin/cos; generalized information fractions for unknown-phase sidereal cos/sin',
      'cases':cases,'holdout':hh,'checks':checks,'checks_passed':sum(checks.values()),
      'limitations':['No Poisson count draws or p-value','No actual detector data, exposure, material response or scattering cross sections',
        'Pure first-harmonic signal; annual wind-direction drift omitted',
        'Equal weight exposed hourly bins; no day/season dependent background amplitude',
        'Fractions are local information geometry, not detection significance'],
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'environment':{'python':platform.python_version(),'numpy':np.__version__,'workers':1}}
    p=Path(__file__).with_name('results.json');p.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    assert json.loads(p.read_text())['checks_passed']==len(checks)
    print(json.dumps({'cases':cases,'holdout':hh,'checks_passed':len(checks)},indent=2))
if __name__=='__main__':main()
