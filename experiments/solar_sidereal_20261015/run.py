"""D-01 v1: deterministic SIMULATED solar/sidereal template-identifiability audit.

Execute: python run.py --output output
Requires NumPy. No real detector measurements, random draws, network or GPU.
Model: fractional rate 1+0.04*cos(2*pi*t solar/day), zero true sidereal component.
Live masks below are INVENTED; they are NOT DAMIC-M uptime data.
"""
import argparse
import csv
import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np

SOLAR_DAY_S = 86400.0
YEAR_D = 365.2422  # approximate tropical year used for mean solar/sidereal beat
SIDEREAL_DAY_S = SOLAR_DAY_S / (1 + 1 / YEAR_D)
OMEGA_SOLAR = 2 * math.pi
OMEGA_SID = OMEGA_SOLAR * SOLAR_DAY_S / SIDEREAL_DAY_S
DAYS = (30, 77, 180, 365)
RATE_PER_LIVE_HOUR = 100.0  # SIMULATED illustrative count scale; results are ratio-based
SOLAR_MOD = 0.04  # SIMULATED fractional modulation


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def matrix_information(sid, nuisance, w):
    """Schur complement (profiled Fisher information) for sidereal coefficients."""
    v = nuisance.T @ (w[:, None] * nuisance)
    cross = nuisance.T @ (w[:, None] * sid)
    info = sid.T @ (w[:, None] * sid) - cross.T @ np.linalg.solve(v, cross)
    return (info + info.T) / 2


def fit(X, z, w):
    root = np.sqrt(w)
    return np.linalg.lstsq(X * root[:, None], z * root, rcond=None)[0]


def case(days, mask_name):
    times = (np.arange(days * 24, dtype=float) + 0.5) / 24  # hourly bin centers; days
    hour = np.arange(days * 24) % 24
    day = np.arange(days * 24) // 24
    live = np.ones(len(times), dtype=bool)
    if mask_name == 'SIMULATED_gapped':
        # Invented continuous detector: 02:00-04:00 outage each day plus three
        # deterministic multiday gaps and a single day per week with 08:00-12:00 off.
        live &= ~((hour >= 2) & (hour < 4))
        for start, stop in ((10, 13), (48, 52), (160, 166)):
            live &= ~((day >= start) & (day < stop))
        live &= ~((day % 7 == 6) & (hour >= 8) & (hour < 12))
    elif mask_name != 'SIMULATED_uniform':
        raise ValueError(mask_name)
    weights = RATE_PER_LIVE_HOUR * live.astype(float)
    solar = np.column_stack((np.cos(OMEGA_SOLAR * times), np.sin(OMEGA_SOLAR * times)))
    sid = np.column_stack((np.cos(OMEGA_SID * times), np.sin(OMEGA_SID * times)))
    intercept = np.ones((len(times), 1))
    nuisance = np.column_stack((intercept, solar))
    base = matrix_information(sid, intercept, weights)
    prof = matrix_information(sid, nuisance, weights)
    lam, v = np.linalg.eigh(base)
    root_inv = (v / np.sqrt(lam)) @ v.T
    retained = root_inv @ prof @ root_inv
    retained = (retained + retained.T) / 2
    eig = np.linalg.eigvalsh(retained)
    # Deterministic Asimov expected count rates. No Poisson noise is sampled.
    fractional = SOLAR_MOD * solar[:, 0]
    wrong = fit(np.column_stack((intercept, sid)), fractional, weights)
    full = fit(np.column_stack((nuisance, sid)), fractional, weights)
    return {
        'days': days, 'mask': mask_name, 'live_hours': int(live.sum()),
        'uptime_fraction': float(live.mean()),
        'retained_info_worst_phase': float(eig.min()),
        'retained_info_best_phase': float(eig.max()),
        'solar_only_false_sid_amplitude_fraction': float(np.linalg.norm(wrong[-2:])),
        'solar_profiling_sid_amplitude_fraction': float(np.linalg.norm(full[-2:])),
        'information_matrix_sid_given_flat': base.tolist(),
        'information_matrix_sid_given_solar': prof.tolist(),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, default=Path('output'))
    out = ap.parse_args().output
    out.mkdir(parents=True, exist_ok=True)
    records = [case(days, mask) for mask in ('SIMULATED_uniform', 'SIMULATED_gapped')
               for days in DAYS]
    by = {(r['days'], r['mask']): r for r in records}
    check = {}
    def ensure(name, condition):
        check[name] = bool(condition)
        if not check[name]:
            raise AssertionError(name)
    ensure('sidereal_shorter_than_solar', 86160 < SIDEREAL_DAY_S < 86170)
    ensure('difference_frequency_one_beat_per_year', abs((OMEGA_SID / OMEGA_SOLAR - 1) * YEAR_D - 1) < 1e-10)
    ensure('correct_profile_zero_Asimov_sidereal', all(r['solar_profiling_sid_amplitude_fraction'] < 1e-11 for r in records))
    ensure('omitted_solar_background_creates_false_sidereal', by[(77, 'SIMULATED_uniform')]['solar_only_false_sid_amplitude_fraction'] > 0.02)
    ensure('information_fraction_in_0_to_1', all(-1e-8 <= r['retained_info_worst_phase'] <= r['retained_info_best_phase'] <= 1+1e-8 for r in records))
    ensure('short_vs_year_information_improves_uniform', by[(30,'SIMULATED_uniform')]['retained_info_worst_phase'] < by[(365,'SIMULATED_uniform')]['retained_info_worst_phase'])
    ensure('gaps_reduce_exposure', all(by[(d,'SIMULATED_gapped')]['live_hours'] < by[(d,'SIMULATED_uniform')]['live_hours'] for d in DAYS))
    ensure('all_masks_have_positive_information', all(r['retained_info_worst_phase'] >= -1e-9 for r in records))
    ensure('normalization_is_nonnegative', 1-SOLAR_MOD > 0)
    # Exact equality of solar and sidereal clocks makes the signal indistinguishable
    # from the freely fitted solar background, for any exposure window.
    t = (np.arange(77*24, dtype=float)+0.5)/24
    s = np.column_stack((np.cos(OMEGA_SOLAR*t), np.sin(OMEGA_SOLAR*t)))
    n = np.column_stack((np.ones(len(t)), s))
    same_freq = matrix_information(s, n, np.ones(len(t)))
    ensure('equal_frequency_is_not_identifiable', np.max(np.abs(same_freq)) < 1e-9)
    csv_path = out / 'SIMULATED_solar_sidereal_windows.csv'
    keys = ['days','mask','live_hours','uptime_fraction','retained_info_worst_phase',
            'retained_info_best_phase','solar_only_false_sid_amplitude_fraction',
            'solar_profiling_sid_amplitude_fraction']
    with csv_path.open('w',newline='') as f:
        wr = csv.DictWriter(f,fieldnames=keys)
        wr.writeheader()
        for row in records:
            wr.writerow({k:row[k] for k in keys})
    summary = {
        'claim_id':'D-01', 'version':'1.0.0', 'date':'2026-10-15',
        'status':['DERIVED','SIMULATION_RESULT','DATA_INSUFFICIENT'],
        'kind':'SIMULATED ASIMOV MODEL, not real detector events or measured sensitivity',
        'truth':{'sidereal_fraction':0.0,'solar_cosine_fraction':SOLAR_MOD,
                 'baseline_counts_per_live_hour':RATE_PER_LIVE_HOUR,
                 'solar_period_seconds':SOLAR_DAY_S,
                 'sidereal_period_seconds':SIDEREAL_DAY_S,
                 'frequency_difference_cycles_per_solar_day':1/YEAR_D,
                 'bin_length_hours':1.0,'start_time':'arbitrary reference t=0',
                 'uptime':'invented masks written explicitly in run.py'},
        'random_seed':None,'reason':'deterministic weighted Gram matrices and noiseless Asimov means',
        'interpretation':'Fisher information fractions and false fitted fractional amplitudes, not discovery significances',
        'records':records,'checks':check,'checks_passed':sum(check.values()),
        'python':sys.version.split()[0],'numpy':np.__version__,'platform':platform.system(),
        'code_sha256':digest(__file__),'csv_sha256':digest(csv_path),
        'limitations':['No real timestamps or uptime from DAMIC-M',
            'No calibrated material response/DM direction',
            'Sinusoidal templates only; sidereal amplitude and phase free',
            'Gaussian/Fisher information at a fixed Asimov baseline, not a Poisson limit',
            'Temperature correlations and time-varying efficiency excluded',
            'No particle cross-section or discovery significance']
    }
    result_path=out/'results.json'
    result_path.write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    assert json.loads(result_path.read_text())['checks_passed']==len(check)
    print('D-01 SIMULATED: checks',len(check),'passed; results',result_path)
    for r in records:
        print(f"{r['days']:>3} d {r['mask']:<17} uptime {r['uptime_fraction']:.3f} "
              f"worst retained {r['retained_info_worst_phase']:.5f} "
              f"false sid amp {r['solar_only_false_sid_amplitude_fraction']:.5f}")


if __name__ == '__main__':
    main()
