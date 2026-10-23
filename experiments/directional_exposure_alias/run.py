#!/usr/bin/env python3
"""D-07: SIMULATED exposure-window solar/sidereal identifiability audit.

No detector event data, physical material rate, fitted signal or scientific novelty claim.
One deterministic analytical Fisher/design-matrix audit; no stochastic draws.
Command: python run.py --output results.json
"""
import argparse
import hashlib
import json
import math
import platform
import time
from pathlib import Path

import numpy as np

F_SIDEREAL = 1.00273790935  # cycles per mean solar day (idealized constant)
F_SOLAR = 1.0
BACKGROUND = 10.0  # expected counts per live 1-hour time bin
SOLAR_FRACTION = 0.18
SOLAR_PHASE = 0.37  # radians
DAY_WINDOWS = (14, 60, 180, 365)


def build_times(days, mask="masked"):
    """Half-open 1h bins; center timestamp in mean solar days since day zero."""
    times = []
    for d in range(days):
        for h in range(24):
            if mask == "masked":
                # Weekdays, local 07:00-18:59, plus planned outages.
                live = (d % 7 < 5) and (7 <= h < 19) and (d % 13 != 4) and (d % 29 != 6)
            elif mask == "continuous":
                live = True
            else:
                raise ValueError(mask)
            if live:
                times.append(d + (h + 0.5) / 24)
    return np.array(times, dtype=float)


def harmonics(times, freq):
    phase = 2 * np.pi * freq * times
    return np.column_stack((np.cos(phase), np.sin(phase)))


def residualize(y, nuisance):
    q, _ = np.linalg.qr(nuisance, mode="reduced")
    return y - q @ (q.T @ y)


def one_case(days, mask):
    t = build_times(days, mask)
    solar = harmonics(t, F_SOLAR)
    sid = harmonics(t, F_SIDEREAL)
    b = np.column_stack((np.ones(len(t)), solar))
    c = np.ones((len(t), 1))
    mu = BACKGROUND * (1 + SOLAR_FRACTION * np.cos(2 * np.pi * t + SOLAR_PHASE))
    assert np.min(mu) > 0
    ws = 1 / np.sqrt(mu)
    sw = sid * ws[:, None]
    bw = b * ws[:, None]
    cw = c * ws[:, None]
    prof = residualize(sw, bw)
    const = residualize(sw, cw)
    full_gram = const.T @ const
    prof_gram = prof.T @ prof
    assert np.min(np.linalg.eigvalsh(full_gram)) > 0
    L = np.linalg.cholesky(full_gram)
    relative_gram = np.linalg.solve(L, prof_gram)
    relative_gram = np.linalg.solve(L, relative_gram.T).T
    fractions = np.clip(np.linalg.eigvalsh((relative_gram+relative_gram.T)/2), 0, 1)

    # A deliberate misspecification: fit solar-only Asimov means with a
    # sidereal signal and intercept, omitting the true solar nuisance.
    wrong = np.column_stack((np.ones(len(t)), sid))
    bad_beta, _, _, _ = np.linalg.lstsq(wrong, mu, rcond=None)
    bad_amplitude = float(np.hypot(bad_beta[1],bad_beta[2]))
    good = np.column_stack((np.ones(len(t)), solar, sid))
    right_beta, _, _, _ = np.linalg.lstsq(good, mu, rcond=None)
    prof_amplitude = float(np.hypot(right_beta[-2],right_beta[-1]))
    sigma_bad_dir = 1/math.sqrt(float(np.min(np.linalg.eigvalsh(prof_gram))))
    sigma_const_bad_dir = 1/math.sqrt(float(np.min(np.linalg.eigvalsh(full_gram))))
    return {
        "span_solar_days":days,
        "mask":mask,
        "live_hour_bins":len(t),
        "live_hours":len(t),
        "calendar_hours":24*days,
        "duty_fraction":round(len(t)/(24*days),8),
        "sidereal_information_fraction_min":float(fractions[0]),
        "sidereal_information_fraction_max":float(fractions[1]),
        "worst_phase_profiled_sigma_counts_per_live_hour":sigma_bad_dir,
        "worst_phase_const_only_sigma_counts_per_live_hour":sigma_const_bad_dir,
        "asimov_solar_only_apparent_sidereal_amplitude_if_solar_omitted_counts_per_live_hour":bad_amplitude,
        "asimov_solar_only_sidereal_amplitude_with_solar_profiled_counts_per_live_hour":prof_amplitude,
        "baseline_phase_drift_solar_hours":days*(1-1/F_SIDEREAL)*24,
        "condition_full_design":float(np.linalg.cond(good)),
    }


def main():
    start=time.perf_counter()
    output=[]
    for m in ("masked","continuous"):
        for d in DAY_WINDOWS:
            output.append(one_case(d,m))
    # Negative controls and implementation checks.
    ts=build_times(60,"masked")
    solar=harmonics(ts,F_SOLAR)
    nil=residualize(solar,np.column_stack((np.ones(len(ts)),solar)))
    worst_norm=float(np.linalg.norm(nil))
    checks={
        "solar_as_signal_is_null_after_solar_profile":worst_norm<1e-11,
        "profiling_never_increases_information":all(0<=r["sidereal_information_fraction_min"]<=r["sidereal_information_fraction_max"]<=1.00000000001 for r in output),
        "continuous_count_exact":all(r["live_hour_bins"]==24*r["span_solar_days"] for r in output if r["mask"]=="continuous"),
        "masked_duty_below_one":all(0<r["duty_fraction"]<1 for r in output if r["mask"]=="masked"),
        "correctly_profiled_asimov_sidereal_zero":all(abs(r["asimov_solar_only_sidereal_amplitude_with_solar_profiled_counts_per_live_hour"])<1e-10 for r in output),
        "mask_low_span_false_sidereal":next(r for r in output if r["mask"]=="masked" and r["span_solar_days"]==14)["asimov_solar_only_apparent_sidereal_amplitude_if_solar_omitted_counts_per_live_hour"]>0.1,
        "longer_baseline_adds_identifiability":next(r for r in output if r["mask"]=="masked" and r["span_solar_days"]==365)["sidereal_information_fraction_min"]>next(r for r in output if r["mask"]=="masked" and r["span_solar_days"]==14)["sidereal_information_fraction_min"],
    }
    assert all(checks.values()),checks
    me=Path(__file__)
    result={
        "study":"D-07",
        "date":"2026-10-23",
        "status":["DERIVED","SIMULATION_RESULT","DATA_INSUFFICIENT"],
        "not_a_detector_fit":True,
        "code_sha256":hashlib.sha256(me.read_bytes()).hexdigest(),
        "seed":None,
        "model":{
            "sidereal_frequency_per_solar_day":F_SIDEREAL,
            "solar_frequency_per_solar_day":F_SOLAR,
            "base_background_counts_per_live_hour":BACKGROUND,
            "solar_background_fraction":SOLAR_FRACTION,
            "solar_background_phase_radians":SOLAR_PHASE,
            "observation":"1h centers, weekdays 07:00-19:00 unless day modulo 13 equals 4 or day modulo 29 equals 6; continuous control",
            "fisher":"Poisson weak-signal Fisher at background means, one constant plus 2 free-phase solar backgrounds, 2 free-phase sidereal signal coefficients",
            "information_fraction":"generalized eigenvalues of profiled sidereal Fisher divided by constant-only Fisher",
            "asimov":"exact expected bin counts; not actual counts or a random synthetic trial"
        },
        "cases":output,
        "checks":checks,
        "checks_passed":sum(checks.values()),
        "execution":{"python":platform.python_version(),"numpy":np.__version__,"elapsed_seconds":time.perf_counter()-start},
        "limitations":["Assumes pure sinusoidal stationary 1 cycle/day and sidereal profiles. Actual material response has higher harmonics and seasonality.","No scattering rate, target crystal, location, sky direction, shielding, efficiency, time calibration or measured event data.","No actual Poisson data draw, empirical likelihood, exclusion limit or discovery significance.","Rates given per live 1-hour bin; effect of realistic changing bin exposures not simulated."]
    }
    return result


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="results.json")
    args=parser.parse_args()
    result=main()
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    verify=json.loads(Path(args.output).read_text(encoding="utf-8"))
    assert verify["code_sha256"]==result["code_sha256"] and len(verify["cases"])==8
    print(json.dumps({"status":"PASS","checks":result["checks_passed"],"elapsed_s":result["execution"]["elapsed_seconds"],"cases":result["cases"]},indent=2))
