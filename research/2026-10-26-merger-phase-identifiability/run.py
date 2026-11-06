#!/usr/bin/env python3
"""C-06 SIMULATED cluster-chronometer identifiability test; no observational data."""
import hashlib
import json
import math
import sys

# ALL VALUES ILLUSTRATIVE (not calibrated to any simulation/observation).
# theta=(k [cm^2/g], t [Gyr], alpha [radians]).
# outputs=(radio-shock separation [kpc], halo separation [kpc], BCG LOS speed [km/s]).
KPC_PER_GYR_PER_KMS = 1.022712165
SHOCK_SPEED = 3600.0 * KPC_PER_GYR_PER_KMS  # kpc/Gyr
APOCENTER_GYR = 0.8
HALO_MAX_KPC = 1200.0
CURVATURE_KPC_GYR2 = 1400.0
DRAG_KPC_PER_K = 150.0
SIGMA = (100.0, 80.0, 50.0)  # mock independent 1-sigma, output units


def model(k, t, alpha):
    h0 = HALO_MAX_KPC - 0.5 * CURVATURE_KPC_GYR2 * (t - APOCENTER_GYR)**2
    v_kpc_gyr = -CURVATURE_KPC_GYR2 * (t - APOCENTER_GYR)
    return (SHOCK_SPEED * t,
            (h0 - DRAG_KPC_PER_K * k) * math.cos(alpha),
            v_kpc_gyr * math.sin(alpha) / KPC_PER_GYR_PER_KMS)


def jacobian(k, t, alpha):
    h0 = HALO_MAX_KPC - 0.5 * CURVATURE_KPC_GYR2 * (t - APOCENTER_GYR)**2
    v = -CURVATURE_KPC_GYR2 * (t - APOCENTER_GYR)
    return ((0.0, SHOCK_SPEED, 0.0),
            (-DRAG_KPC_PER_K * math.cos(alpha), v * math.cos(alpha),
             -(h0 - DRAG_KPC_PER_K * k) * math.sin(alpha)),
            (0.0, -CURVATURE_KPC_GYR2 * math.sin(alpha)/KPC_PER_GYR_PER_KMS,
             v * math.cos(alpha)/KPC_PER_GYR_PER_KMS))


def determinant(m):
    a,b,c = m[0]
    d,e,f = m[1]
    g,h,i = m[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def profile_information(j):
    f = [[sum(j[r][a]*j[r][b]/SIGMA[r]**2 for r in range(3))
          for b in range(3)] for a in range(3)]
    n11, n12, n22 = f[1][1], f[1][2], f[2][2]
    dn = n11*n22 - n12*n12
    assert dn > 0.0
    q1, q2 = f[0][1], f[0][2]
    loss = (n22*q1*q1 - 2*n12*q1*q2 + n11*q2*q2)/dn
    info = f[0][0] - loss
    assert info > -1e-9, 'Schur complement must be nonnegative'
    return max(0.0, info)


def main():
    k, alpha = 1.0, math.radians(30.0)
    series = []
    for t in (0.5, 0.6, 0.7, 0.79, 0.8):
        j = jacobian(k, t, alpha)
        v_kms = -CURVATURE_KPC_GYR2*(t-APOCENTER_GYR)/KPC_PER_GYR_PER_KMS
        identity = SHOCK_SPEED * DRAG_KPC_PER_K * v_kms * math.cos(alpha)**2
        info = profile_information(j)
        series.append({'time_Gyr':t, 'simulated_observables':dict(zip(
            ('shock_kpc','halo_kpc','BCG_LOS_km_s'), model(k,t,alpha))),
            'jacobian_determinant':determinant(j), 'analytic_determinant':identity,
            'profiled_information_per_k_squared':info,
            'profiled_sigma_k_cm2_g': (1.0/math.sqrt(info) if info>1e-10 else None)})

    # Exact mimic with alternative k near first apocenter. No events are simulated.
    target = model(k, APOCENTER_GYR, alpha)
    alternative_k = 0.5
    alternative_alpha = math.acos(target[1]/(HALO_MAX_KPC-DRAG_KPC_PER_K*alternative_k))
    mimic = model(alternative_k, APOCENTER_GYR, alternative_alpha)
    # Independently finite-difference every analytic Jacobian entry.
    max_fd_error = 0.0
    for t in (0.6, 0.8):
        x = (k, t, alpha)
        j = jacobian(*x)
        for col in range(3):
            xplus, xminus = list(x), list(x)
            xplus[col] += 1e-6; xminus[col] -= 1e-6
            up, dn = model(*xplus), model(*xminus)
            for row in range(3):
                max_fd_error = max(max_fd_error, abs((up[row]-dn[row])/(2e-6)-j[row][col]))
    checks = {
        'all_mock_outputs_finite':all(math.isfinite(v) for row in series for v in row['simulated_observables'].values()),
        'jacobian_finite_difference':max_fd_error<2e-6,
        'determinant_identity':all(abs(row['jacobian_determinant']-row['analytic_determinant']) < 1e-6 for row in series),
        'apocenter_rank_deficiency':abs(series[-1]['jacobian_determinant'])<1e-9,
        'apocenter_zero_LOS':abs(target[2])<1e-12,
        'apocenter_exact_mimic':max(abs(a-b) for a,b in zip(target,mimic))<1e-10,
        'alternative_angle_physical':0<alternative_alpha<math.pi/2,
        'preapocenter_information_positive':series[1]['profiled_information_per_k_squared']>1e-5,
        'apocenter_profiled_information_zero':series[-1]['profiled_information_per_k_squared']<1e-9,
        'zero_drag_no_k_sensitivity':abs(jacobian(k,0.6,alpha)[1][0]+DRAG_KPC_PER_K*math.cos(alpha))<1e-10,
        'units_conversion':abs((SHOCK_SPEED/KPC_PER_GYR_PER_KMS)-3600.0)<1e-9,
    }
    assert all(checks.values()), checks
    with open(__file__,'rb') as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    receipt = {'claim':'C06-C1', 'status':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE','DATA_INSUFFICIENT'],
               'label':'SIMULATED MODEL, NOT OBSERVATIONAL DATA',
               'source_sha256':sha,'python_version':sys.version.split()[0], 'seed':None,
               'units':{'k':'cm^2/g','t':'Gyr','alpha':'radian','shock':'kpc','halo':'kpc','LOS':'km/s'},
               'truth':{'k_cm2_g':k,'alpha_deg':30.,'apocenter_Gyr':APOCENTER_GYR},
               'assumptions':{'shock_velocity_km_s':3600.,'halo_max_kpc':HALO_MAX_KPC,
                   'halo_curve_kpc_Gyr2':CURVATURE_KPC_GYR2,'drag_kpc_per_cm2g':DRAG_KPC_PER_K,
                   'measurement_sigma_shock_kpc':SIGMA[0], 'measurement_sigma_halo_kpc':SIGMA[1],
                   'measurement_sigma_los_km_s':SIGMA[2], 'independent_gaussian_errors':True},
               'series':series,
               'apocenter_exact_mimic':{'alternative_k_cm2_g':alternative_k,
                   'alternative_alpha_deg':math.degrees(alternative_alpha),
                   'truth_observables':target,'alternative_observables':mimic},
               'max_fd_abs_error':max_fd_error,'checks':checks,'checks_passed':sum(checks.values()),
               'limitations':['Parameterization is an invented local linearization, not a calibrated cluster model.',
                    'The 3600 km/s scale is merely illustrative; shocks are not exactly insensitive to SIDM.',
                    'No covariance, selection function, simulation likelihood or observed events were fitted.',
                    'BCG LOS velocity is set proportional to a toy orbital derivative, not simulated stars.',
                    'A vanishing Jacobian determinant is a local identifiability warning, not a global impossibility theorem.']}
    print(json.dumps(receipt,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
