#!/usr/bin/env python3
"""C-05-H: SIMULATED two-reservoir merger-heating timing gate.

Standard library only. No data downloads. All values are synthetic.
Unit convention: time Gyr; alpha Gyr^-1; specific kinetic energy (km/s)^2.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

T_GYR = 10.0
ALPHA_PER_GYR = 0.1
DELTA_SPECIFIC_KINETIC_KM2_S2 = 100.0
MERGER_TIMES_GYR = {"early": 2.5, "late": 7.5}


def analytic(t_merger, alpha=ALPHA_PER_GYR, delta=DELTA_SPECIFIC_KINETIC_KM2_S2):
    duration = T_GYR - t_merger
    if not (0.0 <= t_merger <= T_GYR and alpha >= 0.0 and delta >= 0.0):
        raise ValueError("outside this model's parameter domain")
    contrast = math.exp(-2.0 * alpha * duration)
    return (0.5 * delta * (1.0 - contrast), 0.5 * delta * (1.0 + contrast))


def rk4_post_impulse(t_merger, steps, alpha=ALPHA_PER_GYR, delta=DELTA_SPECIFIC_KINETIC_KM2_S2):
    """Integrate d(core,outer)/dt = alpha*(outer-core,core-outer) after the impulse."""
    h = (T_GYR - t_merger) / steps
    core, outer = 0.0, delta
    def rhs(c, o):
        return (alpha*(o-c), alpha*(c-o))
    for _ in range(steps):
        k1c,k1o=rhs(core,outer)
        k2c,k2o=rhs(core+0.5*h*k1c,outer+0.5*h*k1o)
        k3c,k3o=rhs(core+0.5*h*k2c,outer+0.5*h*k2o)
        k4c,k4o=rhs(core+h*k3c,outer+h*k3o)
        core += h*(k1c+2*k2c+2*k3c+k4c)/6
        outer += h*(k1o+2*k2o+2*k3o+k4o)/6
    return core,outer


def main():
    runs = {}
    for label, merger_gyr in MERGER_TIMES_GYR.items():
        closed = analytic(merger_gyr)
        numeric = rk4_post_impulse(merger_gyr, 2000)
        coarse = rk4_post_impulse(merger_gyr, 1000)
        runs[label] = {
            "merger_time_Gyr": merger_gyr,
            "remaining_conduction_time_Gyr": T_GYR - merger_gyr,
            "core_analytic_km2_s2": closed[0],
            "outer_analytic_km2_s2": closed[1],
            "core_RK4_2000_km2_s2": numeric[0],
            "outer_RK4_2000_km2_s2": numeric[1],
            "max_RK4_2000_analytic_abs_error_km2_s2": max(abs(a-b) for a,b in zip(closed,numeric)),
            "max_RK4_1000_analytic_abs_error_km2_s2": max(abs(a-b) for a,b in zip(closed,coarse)),
            "total_specific_energy_km2_s2": sum(closed)
        }
    early = runs["early"]["core_analytic_km2_s2"]
    late = runs["late"]["core_analytic_km2_s2"]
    tol = 1e-9
    tests = {
        "fixed_total_transport_exposure": ALPHA_PER_GYR*T_GYR == 1.0,
        "equal_injected_energy": all(abs(v["total_specific_energy_km2_s2"]-100) < 1e-12 for v in runs.values()),
        "numeric_matches_analytic_early": runs["early"]["max_RK4_2000_analytic_abs_error_km2_s2"] < tol,
        "numeric_matches_analytic_late": runs["late"]["max_RK4_2000_analytic_abs_error_km2_s2"] < tol,
        "coarse_integrator_also_matches": all(v["max_RK4_1000_analytic_abs_error_km2_s2"] < tol for v in runs.values()),
        "earlier_merger_heats_core_more_at_fixed_alpha": early > late,
        "zero_exchange_no_core_heating": analytic(2.5, alpha=0.0)[0] == analytic(7.5, alpha=0.0)[0] == 0.0,
        "pulse_at_end_no_exchange": analytic(T_GYR)[0] == 0.0,
        "fast_exchange_equilibrates_if_time_remains": all(abs(analytic(t,alpha=10)[0] - 50) < 1e-12 for t in (2.5,7.5)),
        "no_heat_source_has_zero_response": analytic(2.5,delta=0.0) == analytic(7.5,delta=0.0) == (0.0,0.0),
        "timing_response_within_physical_bounds": 0.0 < late < early < 50.0
    }
    if not all(tests.values()):
        raise AssertionError(tests)
    receipt={
        "claim_id":"C-05-H1",
        "status":["DERIVED","SIMULATION_RESULT","DATA_INSUFFICIENT"],
        "data_label":"SIMULATED fixed-capacity two-reservoir model, NOT observed SIDM simulation data",
        "assumptions":["two equal fixed positive heat capacities; static geometry", "symmetric linear heat transfer", "single positive outer-zone impulse", "no gravity, negative heat capacity, baryons, or velocity-dependent cross sections"],
        "units":{"time":"Gyr","alpha":"Gyr^-1","specific_kinetic_energy":"(km/s)^2"},
        "generating_truth":{"horizon_Gyr":T_GYR,"alpha_Gyr^-1":ALPHA_PER_GYR,"outer_impulse_km2_s2":DELTA_SPECIFIC_KINETIC_KM2_S2,"merger_epochs_Gyr":MERGER_TIMES_GYR,"normalized_total_alpha_exposure":ALPHA_PER_GYR*T_GYR},
        "runs":runs,
        "core_difference_early_minus_late_km2_s2":early-late,
        "early_to_late_core_energy_ratio":early/late,
        "tests":tests,
        "tests_passed":sum(tests.values()),
        "random_seed":None,
        "source_SHA256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version":sys.version.split()[0],
        "scope":"ALGORITHMIC IDENTITY CHECK with SIMULATED assumptions, not calibrated or N-body physics",
        "stop_condition":"any failed conservation, limiting, or analytic-versus-RK4 check"
    }
    dest=Path(__file__).with_name("heat_order_results.json")
    dest.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"tests_passed":receipt["tests_passed"],"core_early":early,"core_late":late,"difference":early-late,"source_sha256":receipt["source_SHA256"],"receipt_path":str(dest)},indent=2))

if __name__ == "__main__":
    main()
