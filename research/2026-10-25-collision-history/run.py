#!/usr/bin/env python3
"""C05: synthetic fixed-trajectory SIDM collision-budget identifiability check.

Not an N-body simulation, detector fit, gravothermal core model, or measured history.
Python standard library only. No stochastic draws or user-device execution.
"""
import hashlib
import json
import math
import pathlib
import platform
import sys
import time

MSUN_G = 1.98847e33
PC_CM = 3.0856775814913673e18
YEAR_S = 365.25 * 86400.0
RHO_END_MSUN_PC3 = 0.01
V_KM_S = 30.0
T_GYR = 10.0
SIGMA_PER_MASS_CM2_G = 1.0


def density_g_cm3(x, a):
    """Fixed imposed density along a representative trajectory, x=t/T in [0,1]."""
    assert 0 <= x <= 1 and a >= 0
    return RHO_END_MSUN_PC3 * MSUN_G / PC_CM**3 * (1.0 + a * (1.0 - x))


def exposure_analytic(a):
    """Integral of rho*v*dt, with velocity fixed. Units g/cm^2."""
    rho_final = density_g_cm3(1.0, a)
    return rho_final * (V_KM_S * 1e5) * (T_GYR * 1e9 * YEAR_S) * (1 + 0.5 * a)


def exposure_midpoint(a, n):
    """Independent fixed-grid quadrature for stated synthetic history."""
    total = math.fsum(density_g_cm3((j + 0.5)/n, a) for j in range(n))
    return total / n * (V_KM_S * 1e5) * (T_GYR * 1e9 * YEAR_S)


def tau(a, cross_section):
    """Expected Poisson collisions per traced particle under imposed conditions."""
    assert cross_section >= 0
    return exposure_analytic(a) * cross_section


def probability_at_least_one(lam):
    return -math.expm1(-lam)


def early_late_ratio(a):
    """Ratio of exposures in first and second halves for imposed linear density."""
    return (1.0 + 0.75 * a)/(1.0 + 0.25 * a)


def check_close(a, b, tol=1e-12):
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def main():
    t0 = time.perf_counter()
    a_flat, k_flat = 0.0, 1.0
    a_high, k_high = 1.0, 2.0/3.0
    flat = tau(a_flat, k_flat)
    high = tau(a_high, k_high)
    high_same_k = tau(a_high, k_flat)
    midpoint = {str(n): exposure_midpoint(a_high, n) for n in (32, 256, 4096)}
    predicted = exposure_analytic(a_high)
    # Jacobian of lambda to (log kappa, a) at (kappa=1, a=0).
    # A single scalar expected-event summary yields Fisher F=J^T J/sigma^2.
    jac = [flat, 0.5 * flat]
    fisher_without_error = [[x*y for y in jac] for x in jac]
    determinant = (fisher_without_error[0][0]*fisher_without_error[1][1]
                   -fisher_without_error[0][1]*fisher_without_error[1][0])
    tests = {
        "same_endpoint_density": check_close(density_g_cm3(1,0), density_g_cm3(1,1)),
        "different_early_density": check_close(density_g_cm3(0,1),2*density_g_cm3(0,0)),
        "matched_integrated_scattering": check_close(flat, high,1e-13),
        "history_boost_50_percent_at_fixed_cross_section": check_close(high_same_k,1.5*flat),
        "zero_cross_section_null": tau(1.0, 0.0) == 0.0,
        "symmetric_half_histories_equal": check_close(early_late_ratio(0.0),1.0),
        "sloped_half_histories_ratio_1p4": check_close(early_late_ratio(1.0),1.4),
        "midpoint_quadrature_matches_analytic": all(check_close(x,predicted,1e-12) for x in midpoint.values()),
        "probability_falls_in_0_1": 0 < probability_at_least_one(flat) < 1,
        "fisher_rank_one_identity": abs(determinant) < 1e-14,
        "cm2_per_g_units_exposure_g_per_cm2": 0.5 < exposure_analytic(0.0) < 0.8,
    }
    if not all(tests.values()):
        raise AssertionError(f"C05 internal checks failed: {tests}")
    src_sha256 = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    out = {
        "study_id": "C05-2026-10-25-v1.0.0",
        "status": ["DERIVED","SIMULATION_RESULT","UNIDENTIFIABLE","DATA_INSUFFICIENT"],
        "dataset_label": "SIMULATED_FIXED_TRAJECTORY_NOT_OBSERVATIONS",
        "description": "Two imposed linear histories with equal final density but adjusted scattering cross sections giving identical integrated collision optical depths",
        "model": "inhomogeneous Poisson event count with prescribed rho(t), constant relative speed and constant sigma/m, no dynamical response",
        "generating_inputs": {"rho_final_Msun_per_pc3":RHO_END_MSUN_PC3,"v_km_per_s":V_KM_S,"duration_Gyr":T_GYR,"history_linear_a_flat":a_flat,"history_linear_a_high":a_high,"cross_section_flat_cm2_per_g":k_flat,"cross_section_high_cm2_per_g":k_high,"seed":None},
        "results": {
            "rho_final_g_per_cm3": density_g_cm3(1,0),
            "rho_initial_flat_g_per_cm3": density_g_cm3(0,0),
            "rho_initial_high_g_per_cm3": density_g_cm3(0,1),
            "collision_exposure_flat_g_per_cm2": exposure_analytic(0),
            "collision_exposure_high_g_per_cm2": exposure_analytic(1),
            "expected_collisions_flat":flat,
            "expected_collisions_high_adjusted_sigma":high,
            "expected_collisions_high_same_sigma":high_same_k,
            "P_at_least_one_flat": probability_at_least_one(flat),
            "P_at_least_one_high_adjusted_sigma": probability_at_least_one(high),
            "P_at_least_one_high_same_sigma": probability_at_least_one(high_same_k),
            "early_late_exposure_ratio_flat": early_late_ratio(0),
            "early_late_exposure_ratio_high": early_late_ratio(1),
            "sensitivity_J_at_flat_logk_a":jac,
            "fisher_proportional_2x2":fisher_without_error,
            "fisher_determinant_numeric":determinant,
            "midpoint_g_per_cm2":midpoint
        },
        "checks":tests,"checks_passed":len(tests),
        "runtime": {"environment":"ChatGPT Linux container; not user's Mac","python":platform.python_version(),"worker_count":1,"seconds_core":time.perf_counter()-t0,"source_sha256":src_sha256},
        "critical_limits": ["No cosmological expansion or radius dependence", "Frozen trajectory and constant velocity", "Expected collision count alone does not predict heat flux or gravothermal collapse", "No N-body code or paper data rerun", "No measured scattering event count", "Cross section velocity dependence ignored", "Fisher is conditional on one illustrative scalar measurement, not calibrated likelihood"]
    }
    target = pathlib.Path(__file__).with_name('results.json')
    target.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding="utf-8")
    check = json.loads(target.read_text(encoding="utf-8"))
    assert check["checks_passed"] == len(tests) and all(check["checks"].values())
    print(json.dumps({"path":str(target),"source_sha256":src_sha256,"checks":len(tests),"lam_flat":flat,"lam_high":high,"lam_high_same_k":high_same_k,"early_late_ratio":early_late_ratio(1),"fisher_determinant":determinant,"seconds_core":out["runtime"]["seconds_core"]},sort_keys=True))

if __name__ == '__main__':
    main()
