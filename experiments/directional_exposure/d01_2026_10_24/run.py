#!/usr/bin/env python3
"""D-01: solar/sidereal exposure-geometry identifiability, SIMULATED DESIGN.
One deterministic CPU calculation. This is NOT a dark-matter rate or data fit.
Dependencies: Python 3.10+ and NumPy. No RNG or external input files.
"""
import json
import math
import time
import hashlib
import platform
from pathlib import Path
import numpy as np

P_SOLAR_H = 24.0
P_SIDEREAL_H = 23.9344696  # rounded mean sidereal day, see USNO reference
DURATIONS_DAYS = (30, 120, 365)
BIN_H = 1.0


def make_design(days: int, mode: str, sidereal_h=P_SIDEREAL_H):
    t = np.arange(int(days * 24), dtype=float) + 0.5  # hours since arbitrary start
    if mode == 'continuous':
        e = np.ones_like(t)
    elif mode == 'night_6in7':
        hour = np.floor(t).astype(int) % 24
        day = np.floor(t / 24).astype(int)
        e = (((hour >= 18) | (hour < 6)) & (day % 7 != 0)).astype(float)
    else:
        raise ValueError(mode)
    t = t[e > 0]
    s = np.column_stack((np.cos(2 * np.pi * t / P_SOLAR_H),
                         np.sin(2 * np.pi * t / P_SOLAR_H)))
    d = np.column_stack((np.cos(2 * np.pi * t / sidereal_h),
                         np.sin(2 * np.pi * t / sidereal_h)))
    return t, s, d


def subspace_result(solar, sidereal):
    # Project away unknown constant background first.
    n = len(solar)
    ones = np.ones((n, 1)) / math.sqrt(n)
    Sc = solar - ones @ (ones.T @ solar)
    Dc = sidereal - ones @ (ones.T @ sidereal)
    qs, rs = np.linalg.qr(Sc, mode='reduced')
    qd, rd = np.linalg.qr(Dc, mode='reduced')
    # Principal angles: maximal cross-channel mimicry for unknown phases.
    canonical = np.linalg.svd(qs.T @ qd, compute_uv=False)
    rho = float(canonical[0])
    # Worst-phase retained sidereal Fisher information after profiling over
    # constant + both solar quadratures, relative to constant-only profiling.
    retained = max(0., 1.0 - rho ** 2)
    return {'max_canonical_correlation': rho,
            'worst_phase_retained_info_fraction': retained,
            'conditional_sd_inflation': None if retained <= 1e-12 else 1/math.sqrt(retained),
            'both_two_column_bases_full_rank': bool(np.min(np.abs(np.diag(rs))) > 1e-8 and np.min(np.abs(np.diag(rd))) > 1e-8),
            'solar_sidereal_min_principal_angle_deg': math.degrees(math.acos(min(1.,max(0.,rho))))}


def main():
    t0 = time.perf_counter()
    out = {'study':'D-01', 'date':'2026-10-24', 'classification':'SIMULATED DESIGN; NOT OBSERVATIONAL DATA',
           'model':'constant + free-phase solar frequency + free-phase sidereal frequency',
           'solar_period_h':P_SOLAR_H, 'sidereal_period_h':P_SIDEREAL_H,
           'frequency_beat_period_days':1.0/abs(24.0/P_SIDEREAL_H-1.0),
           'bin_width_h': BIN_H, 'masks':{
                'continuous':'all hourly midpoints observed',
                'night_6in7':'solar hours [18,24) or [0,6); discard every seventh full day beginning with day 0'},
           'results':{}, 'checks':{}, 'seed':None, 'true_particle_signal':None,
           'covariance':'idealized equal-variance independent equal-exposure bins; no physical rate/likelihood'}
    for mode in ['continuous','night_6in7']:
        out['results'][mode] = {}
        for days in DURATIONS_DAYS:
            t,s,d=make_design(days,mode)
            result=subspace_result(s,d)
            result['n_observed_hourly_bins'] = int(len(t))
            result['observed_exposure_hours'] = float(len(t))
            out['results'][mode][str(days)]=result
    # Distinct checks. The equal-period null is algebraically exact within floating-point tolerance.
    t,s,dsame=make_design(30,'continuous',sidereal_h=P_SOLAR_H)
    equal=subspace_result(s,dsame)
    out['checks']['same_frequency_information_zero']=equal['worst_phase_retained_info_fraction'] < 1e-12
    out['checks']['frequency_beat_roughly_one_year']=364 < out['frequency_beat_period_days'] < 366
    for mode in out['results']:
        R=out['results'][mode]
        out['checks'][mode+'_resolves_with_longer_baseline']=(R['365']['worst_phase_retained_info_fraction']>R['120']['worst_phase_retained_info_fraction']>R['30']['worst_phase_retained_info_fraction'])
        out['checks'][mode+'_full_rank']=all(R[str(d)]['both_two_column_bases_full_rank'] for d in DURATIONS_DAYS)
        out['checks'][mode+'_valid_bounds']=all(0<=R[str(d)]['worst_phase_retained_info_fraction']<=1 for d in DURATIONS_DAYS)
    out['checks_passed'] = sum(out['checks'].values())
    assert all(out['checks'].values()), out['checks']
    out['compute_elapsed_seconds']=time.perf_counter()-t0
    out['runtime_python']=platform.python_version()
    out['numpy_version']=np.__version__
    out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    p=Path(__file__).with_name('results.json')
    p.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks_passed':out['checks_passed'],'checks_total':len(out['checks']),
           'duration_s':out['compute_elapsed_seconds'],'beat_days':out['frequency_beat_period_days'],
           'results':{key:{days:{k:(round(v,9) if isinstance(v,float) else v) for k,v in row.items() if k in ('max_canonical_correlation','worst_phase_retained_info_fraction','conditional_sd_inflation','n_observed_hourly_bins')} for days,row in val.items()} for key,val in out['results'].items()},
           'source_sha256':out['source_sha256']},indent=2))

if __name__ == '__main__':
    main()
