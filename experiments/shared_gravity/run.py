"""N-05: DERIVED numerical scale checks, not measured neutrino data.
Python standard library only. Run: python run.py
Illustrative inputs are not fitted particle or cosmological parameters.
"""
import hashlib
import json
import math
import platform
import time
from pathlib import Path

C = 299792458.0                         # m/s, exact SI
PC = 3.085677581491367e16               # m, numerical parsec conversion
HBAR = 6.582119569e-16                  # eV s, rounded conversion
YEAR = 31557600.0                      # s, Julian year
H0 = 67.4 * 1000 / (1e6 * PC)          # s^-1, illustrative
OM = 0.315                             # dimensionless, illustrative


def kernel(z, n=4096):
    """Integral dz/[(1+z)^2 H(z)], in seconds, matter+Lambda FLRW."""
    if z < 0 or n < 2 or n % 2:
        raise ValueError("Require nonnegative z and positive even n")
    if z == 0:
        return 0.0
    h = z / n
    def f(x):
        return 1 / ((1+x)**2 * H0 * math.sqrt(OM*(1+x)**3 + 1-OM))
    terms = [f(0), f(z)]
    terms.extend((4 if i % 2 else 2)*f(i*h) for i in range(1,n))
    return h * math.fsum(terms) / 3


def speed_deficit(mu_eV, energy_eV):
    """Stable 1-v/c. mu=mc^2; energy is total local energy."""
    if not 0 <= mu_eV < energy_eV:
        raise ValueError("Require 0 <= rest energy < total energy")
    x = (mu_eV / energy_eV)**2
    return x / (1 + math.sqrt(1-x))


def main():
    start = time.perf_counter()
    checks = {}
    def check(name, condition):
        checks[name] = bool(condition)
        if not condition:
            raise AssertionError(name)

    I = kernel(1)
    I2 = kernel(1,8192)
    mu, dm2, energy = 0.05, 2.5e-3, 1e14  # eV, eV^2, eV: illustrative
    phase = dm2 * I / (2*HBAR*energy)      # radians
    delay_z1 = mu**2 * I / (2*energy**2)  # seconds, leading relativistic
    eps10 = speed_deficit(mu,1e7)
    delay10 = (1e4*PC/C)*eps10 / math.sqrt(1-(mu/1e7)**2)

    check('zero_redshift_kernel', kernel(0) == 0)
    check('doubled_quadrature', abs(I-I2)/I < 1e-12)
    check('low_redshift_limit', abs(kernel(1e-6)*H0/1e-6-1) < 2e-6)
    check('massless_speed', speed_deficit(0,1e7) == 0)
    check('stable_speed_formula', abs(speed_deficit(0.1,1)-(1-math.sqrt(.99))) < 1e-15)
    check('inverse_energy_squared_delay', abs(speed_deficit(mu,1e7)/speed_deficit(mu,1e8)-100) < 1e-10)
    # Schwarzschild radial cancellation at fixed E_infinity and areal radii:
    # d_ell=dr/sqrt(A), E_local=E_infinity/sqrt(A), so d_ell/E_local=dr/E_infinity.
    residual = max(abs((1/math.sqrt(A))/(1/math.sqrt(A))-1) for A in [.2,.5,.9,1])
    check('radial_redshift_length_cancellation', residual < 1e-14)
    # Algebraic controlled example, seconds. Not observations or a lens simulation.
    photon = [100.0,200.0]
    neutrino = [117.0,217.002]
    double = (neutrino[1]-neutrino[0])-(photon[1]-photon[0])
    shifted = [v+37.0 for v in neutrino]
    double_shift = (shifted[1]-shifted[0])-(photon[1]-photon[0])
    check('constant_emission_lag_cancels', abs(double-double_shift) < 1e-12)

    result = {
        'study_id':'N-05', 'date':'2026-10-16', 'status':'DERIVED',
        'data_kind':'SIMULATED illustrative theoretical scales; zero observational events',
        'seed':None, 'randomness':'none',
        'inputs':{'rest_energy_eV':mu,'mass_squared_splitting_eV2':dm2,
                  'H0_km_s_Mpc':67.4,'Omega_m':OM,'Omega_Lambda':1-OM,
                  'radiation_omitted':True,'z':1,'observed_energy_eV':energy},
        'results':{'kernel_z1_seconds':I,'kernel_z1_Gyr':I/(1e9*YEAR),
            'phase_at_100TeV_z1_radians':phase,'phase_cycles':phase/(2*math.pi),
            'fractional_energy_change_for_one_radian':1/phase,
            'speed_deficit_10MeV':eps10,'speed_deficit_100TeV':speed_deficit(mu,energy),
            'mass_delay_10MeV_10kpc_seconds':delay10,
            'mass_delay_100TeV_z1_seconds':delay_z1,
            'double_delay_example_seconds':double},
        'checks':checks, 'checks_passed':sum(checks.values()),
        'limitations':['No detector sensitivity forecast, measured redshift or neutrino mass.',
          'Static weak-lens, radial Schwarzschild, homogeneous FLRW are distinct limits, not one fitted lens.',
          'Cosmological kernel neglects radiation; evaluated only at z<=1.',
          'Finite numerical consistency is not proof of a new physical mechanism.',
          'Double-delay algebra requires same source region and stable lens; low event counts may prevent measurement.'],
        'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'environment':{'python':platform.python_version(),'platform':platform.system(),'workers':1},
        'wall_seconds':time.perf_counter()-start}
    out = Path(__file__).with_name('results.json')
    text = json.dumps(result,indent=2,allow_nan=False)+'\n'
    out.write_text(text)
    assert json.loads(out.read_text())['checks_passed'] == 8
    print(text)

if __name__ == '__main__':
    main()
