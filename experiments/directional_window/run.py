"""D-01: SIMULATED solar-vs-sidereal Fourier-window identifiability audit.
Fixed Poisson high-count Fisher geometry; no measured events or material response.
Usage: python run.py --output results.json
Requires NumPy (already present in execution environment).
"""
import argparse, csv, hashlib, json, math, platform
from pathlib import Path
import numpy as np

OMEGA_SOL = 2 * math.pi  # radians / mean solar day
SIDEREAL_PER_SOLAR = 1.00273790935  # Earth rotation cycles per mean solar day
OMEGA_SID = OMEGA_SOL * SIDEREAL_PER_SOLAR

def simulate_days(duration, window):
    """Project two sidereal phase components off constant + two free-phase solar components."""
    n = int(24 * duration)
    t = (np.arange(n, dtype=float) + 0.5) / 24.0  # mean solar days, centers of hourly bins
    d = np.arange(n) // 24
    h = np.arange(n) % 24
    # SIMULATED uptime: 18 live hours of each day, repeated outages, plus one extra outage.
    mask = (h >= 1) & (h < 19) & ~np.isin(d % 17, [6, 7, 8]) & (d % 31 != 15)
    live = np.ones(n, dtype=bool) if window == 'uniform' else mask
    t = t[live]
    X = np.column_stack([np.ones(t.size), np.cos(OMEGA_SOL*t), np.sin(OMEGA_SOL*t)])
    S = np.column_stack([np.cos(OMEGA_SID*t), np.sin(OMEGA_SID*t)])
    # With constant expected background counts per live hour, Poisson Fisher is proportional
    # to the Gram matrix. Its overall scale cancels in relative retained information.
    Q, _ = np.linalg.qr(X, mode='reduced')
    R = S - Q @ (Q.T @ S)
    G = S.T @ S
    H = R.T @ R
    vals, vecs = np.linalg.eigh(G)
    invsqrt = (vecs * vals**(-0.5)) @ vecs.T
    retained = np.linalg.eigvalsh(invsqrt @ H @ invsqrt)
    retained = np.maximum(retained, 0.)
    return {'duration_calendar_days': duration, 'window':window,'calendar_hour_bins':n,
            'live_hour_bins':int(live.sum()),'live_fraction':float(live.mean()),
            'min_retained_fisher_fraction':float(retained[0]),
            'max_retained_fisher_fraction':float(retained[1]),
            'worst_phase_information_loss_fraction':float(1-retained[0]),
            'best_case_amplitude_signal_to_noise_retained':float(math.sqrt(retained[1])),
            'worst_case_amplitude_signal_to_noise_retained':float(math.sqrt(retained[0])),
            'no_signal_measurements':True}

def main():
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,default=Path('results.json'))
    out=a.parse_args().output
    durations=[30, 77, 180, 365]
    rows=[simulate_days(d,w) for w in ['uniform','simulated_outages'] for d in durations]
    assert len(rows)==8
    checks={
      'mean_solar_and_sidereal_distinct':OMEGA_SID>OMEGA_SOL,
      'beat_period_close_to_year':abs(1/SIDEREAL_PER_SOLAR.__sub__(1)-365.2422)<0.1,
      'fisher_fractions_bounded':all(0<=r['min_retained_fisher_fraction']<=r['max_retained_fisher_fraction']<=1+1e-11 for r in rows),
      'uniform_mask_live_fraction_one':all(r['live_fraction']==1 for r in rows if r['window']=='uniform'),
      'outage_mask_is_nontrivial':all(.45<r['live_fraction']<.8 for r in rows if r['window']=='simulated_outages'),
      'year_long_uniform_resolves_solar_vs_sidereal':next(r for r in rows if r['duration_calendar_days']==365 and r['window']=='uniform')['min_retained_fisher_fraction']>.99,
      'short_uniform_worse_than_long_uniform':next(r for r in rows if r['duration_calendar_days']==30 and r['window']=='uniform')['min_retained_fisher_fraction']<next(r for r in rows if r['duration_calendar_days']==180 and r['window']=='uniform')['min_retained_fisher_fraction'],
      'both_unknown_phases_profiled':True
    }
    if not all(checks.values()): raise AssertionError(checks)
    result={
      'claim_id':'D-01-F1', 'date':'2026-10-22',
      'status':['DERIVED','SIMULATION_RESULT','DATA_INSUFFICIENT'],
      'data_kind':'SIMULATED observation-window/design-matrix only: no particle signal or detector observations',
      'unit_definition':'t in mean solar days, duration in calendar days, 1h bins; relative Fisher fractions dimensionless',
      'source_context':['arXiv:2602.15947v1 2026-02-17, Poisson likelihood and daily modulation; this calculation is not its reproduced result',
                        'DAMIC-M arXiv:2511.13962v1 2025-11-17, Phys Rev D published 2026-08-19; 77d blinded search interval during 2024-25 observations'],
      'omega_solar_rad_per_day':OMEGA_SOL,'omega_sidereal_rad_per_day':OMEGA_SID,
      'beat_period_solar_days':1/(SIDEREAL_PER_SOLAR-1),
      'model':'High-count Poisson, constant expected background per live hour. Nuisance span [1,cos(w_solar t),sin(w_solar t)]. Signal span [cos(w_sid t),sin(w_sid t)] with unknown phase. Unweighted live-hour Gram matrix.',
      'mask':'SIMULATED only: live hours 01:00-18:59; shut days d mod 17 in [6,7,8], and d mod 31 ==15; no claim to DAMIC-M operations',
      'generating_truth':'No counts generated; exactly stated sinusoidal candidate templates and deterministic observing windows',
      'random_seed':None,'workers':1,'rows':rows,'checks':checks,'checks_passed':sum(checks.values()),
      'limitations':['Relative Fisher information only, not a physical modulation fraction, likelihood significance, Poisson injection recovery, or discovery forecast.',
                     'No material-specific scattering response, orientation, Earth shielding or detector calibration.',
                     '77d chosen as illustrative span resembling DAMIC-M D2 days, not its actual live-time mask or measured events.',
                     'Constant background per live hour and only one freely phased 24h nuisance; extra time-dependent nuisances can further reduce identifiability.',
                     'A distinct frequency is not proof of dark matter because other astronomical or instrumental processes may be sidereal.'],
      'implementation':'NumPy QR projection and symmetric two-by-two whitening/eigenvalues; no random draws',
      'python':platform.python_version(),'numpy':np.__version__,
      'runpy_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    csvpath=out.with_suffix('.csv')
    with csvpath.open('w',newline='') as f:
       ww=csv.DictWriter(f,fieldnames=list(rows[0]));ww.writeheader();ww.writerows(rows)
    result['csv_sha256']=hashlib.sha256(csvpath.read_bytes()).hexdigest()
    out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    loaded=json.loads(out.read_text());assert len(loaded['rows'])==8
    print(json.dumps({'checks_passed':loaded['checks_passed'],'windows':[(z['duration_calendar_days'],z['window'],round(z['live_fraction'],3),round(z['min_retained_fisher_fraction'],6),round(z['max_retained_fisher_fraction'],6)) for z in rows]},indent=2))
if __name__=='__main__':main()
