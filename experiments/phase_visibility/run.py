"""N-03 v1: deterministic SIMULATED MODEL audit, not observed neutrino data.
Run: python run.py --output output
Requires NumPy + SciPy. No random draws, network, GPU, or subprocesses.
"""
import argparse
import csv
import hashlib
import json
import math
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.special import j0, jn_zeros, roots_laguerre


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def native(value):
    """Normalize NumPy scalars explicitly; never hide nonfinite outputs."""
    if isinstance(value, np.ndarray):
        return native(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): native(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [native(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('output'))
    out = parser.parse_args().output
    out.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    checks = {}

    def check(name, condition):
        checks[name] = bool(condition)
        if not checks[name]:
            raise AssertionError(name)

    # Freeze the finite domain: 61 phase-amplitude values, 0 to 6 radians.
    a = np.linspace(0.0, 6.0, 61)
    xi = 2 * np.pi * (np.arange(2048) + 0.5) / 2048
    fixed = np.mean(np.exp(1j * a[:, None] * np.cos(xi)), axis=1)
    fixed_half = np.mean(np.exp(1j * a[:, None] * np.cos(xi[::2])), axis=1)
    analytic_fixed = j0(a)

    # r has density 2 r exp(-r^2), so u=r^2 has density exp(-u).
    # This describes an ensemble that samples amplitudes, NOT a short run's
    # single fixed-but-unknown amplitude and NOT an assumed iid event likelihood.
    u, weights = roots_laguerre(64)
    rayleigh = j0(a[:, None] * np.sqrt(u)[None, :]) @ weights
    u32, w32 = roots_laguerre(32)
    rayleigh_half = j0(a[:, None] * np.sqrt(u32)[None, :]) @ w32

    # Independent Cartesian integral: X ~ Normal(0, 1/2), delta=a X.
    # Gauss-Legendre quadrature on [-10,10]; discarded tail < 3e-45.
    nodes, w = np.polynomial.legendre.leggauss(160)
    x, wx = 10 * nodes, 10 * w
    gaussian = np.cos(a[:, None] * x) @ (wx * np.exp(-x*x) / np.sqrt(np.pi))
    analytic_gaussian = np.exp(-a*a / 4)

    check('fixed_phase_integral_matches_J0', np.max(abs(fixed-analytic_fixed)) < 1e-12)
    check('phase_grid_converged', np.max(abs(fixed-fixed_half)) < 1e-12)
    check('rayleigh_average_matches_exp', np.max(abs(rayleigh-analytic_gaussian)) < 1e-11)
    check('rayleigh_quadrature_converged', np.max(abs(rayleigh-rayleigh_half)) < 1e-10)
    check('gaussian_noise_matches_same_exp', np.max(abs(gaussian-analytic_gaussian)) < 1e-11)
    check('zero_perturbation_limit', abs(fixed[0]-1) < 1e-14 and abs(rayleigh[0]-1) < 1e-12)
    check('positive_density_matrices', np.min((1-abs(fixed))/2) > -1e-12)
    check('return_probabilities_bounded', np.all((1+fixed.real)/2 >= 0) and np.all((1+fixed.real)/2 <= 1+1e-12))

    rho = np.diag([0.8, 0.2]).astype(complex)
    D = np.diag([1, np.exp(1j * 1.234)])
    check('unequal_mass_diagonal_state_invariant', np.max(abs(D @ rho @ D.conj().T-rho)) < 1e-14)
    R = np.array([[1, -1], [1, 1]]) / np.sqrt(2)
    check('mass_mixing_negative_control_changes_state', np.max(abs(R @ rho @ R.T-rho)) > 0.29)
    small = np.array([0.02, 0.04])
    fourth = (np.exp(-small**2/4)-j0(small))/small**4
    check('matched_variance_difference_starts_at_fourth_order', np.max(abs(fourth-1/64)) < 1e-5)
    check('native_numpy_bool_serialization', json.loads(json.dumps(native({'ok': np.bool_(True)}))) == {'ok': True})

    rows = []
    for i, aa in enumerate(a):
        rows.append([float(aa), float(fixed[i].real), float(rayleigh[i]), float(gaussian[i]),
                     float((1+fixed[i].real)/2), float((1+0.25*fixed[i].real)/2), 0.5,
                     float((1+rayleigh[i])/2)])
    csv_path = out / 'SIMULATED_phase_scan.csv'
    with csv_path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['a_radians','C_fixed','C_rayleigh','C_gaussian_noise',
                         'P_fixed_c1','P_fixed_c025','P_c0','P_rayleigh_c1'])
        writer.writerows(rows)

    result = {
        'study_id': 'N-03', 'version': '1.0.0', 'date': '2026-10-14',
        'status': ['DERIVED', 'SIMULATION_RESULT', 'UNIDENTIFIABLE'],
        'data_label': 'SIMULATED MODEL; deterministic expectations, no sampled observations',
        'seed': None, 'seed_reason': 'Deterministic numerical quadrature; no random generator',
        'generating_truth': {'state': 'rho=0.5*[[1,c],[c,1]], c in {1,0.25,0}',
            'propagation': 'D=diag(1,exp(i*delta)), vacuum phase set to zero for plot',
            'fixed_delta': 'a*cos(xi), xi uniform [0,2pi)',
            'rayleigh_delta': 'a*r*cos(xi), p(r)=2*r*exp(-r^2)',
            'ordinary_noise_delta': 'a*X, X Gaussian with mean 0 and variance 1/2'},
        'units': 'a and delta are phases in radians (dimensionless); all probabilities dimensionless',
        'domain': {'a_min': 0, 'a_max': 6, 'a_count': 61, 'phase_nodes': 2048,
                   'laguerre_nodes': 64, 'gaussian_nodes': 160, 'gaussian_domain': [-10,10]},
        'max_abs_errors': {'fixed_vs_J0': np.max(abs(fixed-analytic_fixed)),
            'rayleigh_vs_exp': np.max(abs(rayleigh-analytic_gaussian)),
            'gaussian_vs_exp': np.max(abs(gaussian-analytic_gaussian)),
            'rayleigh_vs_gaussian': np.max(abs(rayleigh-gaussian))},
        'examples': [{'a_radians': float(aa), 'P_fixed_c1': float((1+j0(aa))/2),
            'P_rayleigh_or_gaussian_c1': float((1+np.exp(-aa*aa/4))/2),
            'P_c0': 0.5} for aa in [0,1,2,3,4,6]],
        'first_zero_fixed_C_radians': float(jn_zeros(0,1)[0]),
        'checks': checks, 'passed': sum(checks.values()),
        'environment': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
                        'platform': platform.system(), 'cpu_workers': 1},
        'code_sha256': sha256(__file__), 'csv_sha256': sha256(csv_path),
        'calculation_wall_seconds': time.perf_counter()-started,
        'not_claimed': ['Original missing run reproduced', 'New particle signature', 'Real neutrino fit',
            'Detector sensitivity', 'Cross-section limit', 'Full three-flavor or matter evolution',
            'Temporal likelihood equivalence', 'Independent peer review']}
    text = json.dumps(native(result), indent=2, allow_nan=False) + '\n'
    json.loads(text)  # Verify serialization before claiming success.
    temporary = out / 'results.json.tmp'
    temporary.write_text(text)
    temporary.replace(out / 'results.json')
    print(text)


if __name__ == '__main__':
    main()
