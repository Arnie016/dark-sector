"""D-01A: SIMULATED solar/sidereal alias with fixed synthetic uptime.
No detector response or measured events. Requires NumPy, Python >=3.11.
Run: python run.py
"""
import hashlib
import json
import math
from pathlib import Path
import numpy as np

SIDEREAL_SEC = 86164.0905
SEGMENT_RATES = np.array([.97, 1.05, .94, 1.08, 1., .95, 1.02])


def design(spread):
    times, segments = [], []
    for j in range(7):
        for d in range(11):
            if j == 3 and 4 <= d < 6:  # SIMULATED two-day outage
                continue
            for h in range(48):
                if 4 <= h < 8:  # SIMULATED 02:00-04:00 daily outage
                    continue
                times.append(j * (52 if spread else 11) + d + (h+.5)/48)
                segments.append(j)
    t, g = np.array(times), np.array(segments)
    sid = np.stack((np.cos(2*np.pi*t*86400/SIDEREAL_SEC),
                    np.sin(2*np.pi*t*86400/SIDEREAL_SEC)), axis=1)
    sun = np.stack((np.cos(2*np.pi*t), np.sin(2*np.pi*t)), axis=1)
    group = np.eye(7)[g]
    weight = 25 * SEGMENT_RATES[g]  # SIMULATED expected counts per live bin
    return t, sid, sun, group, weight


def projected_fisher(s, nuisance, w):
    sqrt = np.sqrt(w)[:, None]
    q, r = np.linalg.qr(nuisance * sqrt, mode='reduced')
    assert min(abs(np.diag(r))) > 1e-7
    remaining = s * sqrt - q @ (q.T @ (s * sqrt))
    return remaining.T @ remaining


def study(spread):
    t, sid, sun, group, w = design(spread)
    original = projected_fisher(sid, group, w)
    profiled = projected_fisher(sid, np.column_stack((group,sun)), w)
    eig, vec = np.linalg.eigh(original)
    transform = (vec / np.sqrt(eig)) @ vec.T
    frac = np.linalg.eigvalsh(transform @ profiled @ transform)
    solar_only = .04 * np.cos(2*np.pi*t+.7)  # SIMULATED background-only truth
    injected = solar_only + .02*np.cos(2*np.pi*t*86400/SIDEREAL_SEC+.4)

    def fit(nuis, truth):
        x = np.column_stack((group,nuis,sid))
        beta = np.linalg.lstsq(x*np.sqrt(w[:,None]),truth*np.sqrt(w),rcond=None)[0]
        assert np.max(np.abs(x@beta-truth)) < 1e-10 if len(nuis.T)==2 else True
        return float(np.linalg.norm(beta[-2:]))

    naive = fit(np.zeros((len(t),0)), solar_only)
    profiled_false = fit(sun,solar_only)
    recovered = fit(sun,injected)
    assert len(t) == 3300 and .0 < frac[0] <= frac[1] < 1.00000001
    assert profiled_false < 1e-11 and abs(recovered-.02) < 1e-11
    return {'calendar_span_days':323 if spread else 77,
            'live_half_hour_bins':len(t),'live_days_equivalent':len(t)/48,
            'simulated_expected_counts':float(w.sum()),
            'retained_fisher_eigenvalues':frac.tolist(),
            'worst_retained_fraction':float(frac[0]),
            'max_solar_sidereal_overlap':float(np.sqrt(max(0,1-frac[0]))),
            'worst_direction_sigma_ratio':float(1/np.sqrt(np.linalg.eigvalsh(profiled)[0]) /
                                                  (1/np.sqrt(eig[0]))),
            'solar_only_false_sidereal_amplitude_without_solar_nuisance':naive,
            'solar_only_false_sidereal_amplitude_with_solar_nuisance':profiled_false,
            'injected_2pct_sidereal_recovered_joint_fit':recovered}


def main():
    a,b=study(False),study(True)
    assert a['live_half_hour_bins']==b['live_half_hour_bins']
    assert a['simulated_expected_counts']==b['simulated_expected_counts']
    assert a['worst_retained_fraction']<b['worst_retained_fraction']
    assert a['solar_only_false_sidereal_amplitude_without_solar_nuisance'] > b['solar_only_false_sidereal_amplitude_without_solar_nuisance']
    result={'id':'D-01A','date':'2026-10-18','status':['DERIVED','SIMULATION_RESULT','DATA_INSUFFICIENT'],
            'data':'SIMULATED Asimov expectations and synthetic masks; no measured events',
            'periods_seconds':{'solar':86400,'sidereal':SIDEREAL_SEC},
            'truth':{'solar_amplitude_fraction':.04,'sidereal_injection_amplitude_fraction':.02,
                     'per_bin_expected_counts':25,'sampling_minutes':30,
                     'segments':7,'segment_days':11,'invented_daily_outage_hours':2,
                     'invented_extra_outage_days':2,'random_seed':None,'random_draws':0},
            'contiguous':a,'season_spread':b,
            'limitations':['Harmonic template, no material-specific response',
                          'Fisher approximation and noiseless Asimov injection, not real Poisson sample',
                          'Fixed sidereal phase ignores annual Galactic-wind phase drift',
                          'Solar sinusoid and seven segment offsets omit real detector-temperature effects',
                          'Synthetic uptime is NOT the DAMIC-M exposure mask'],
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path('results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'contiguous_retained_fraction':a['worst_retained_fraction'],
                      'spread_retained_fraction':b['worst_retained_fraction'],
                      'solar_only_false_amp_contiguous':a['solar_only_false_sidereal_amplitude_without_solar_nuisance'],
                      'solar_only_false_amp_spread':b['solar_only_false_sidereal_amplitude_without_solar_nuisance']},indent=2))


if __name__ == '__main__':
    main()
