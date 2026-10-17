#!/usr/bin/env python3
"""S-01 deterministic SIMULATED merger-projection identifiability check.
No observations or original TNGC-SIDM simulations used. Standard library only.
Run: python run.py --output output
"""
import argparse
import hashlib
import json
import math
import platform
import time
from pathlib import Path


def model(s, theta_deg, h0_kpc=1500.0, response_kpc=200.0, v_kms=1800.0):
    """Predicted projected halo separation (kpc) and relative LOS speed (km/s).
    s=(sigma/m)/(1 cm^2/g), theta measured from the sky plane in degrees.
    Fixed merger phase is assumed known from a synthetic radio-relic clock.
    """
    t = math.radians(theta_deg)
    return ((h0_kpc-response_kpc*s)*math.cos(t), v_kms*math.sin(t))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, default=Path('output'))
    args = p.parse_args()
    tic = time.perf_counter()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    h0, A, V = 1500.0, 200.0, 1800.0
    sig_h, sig_v = 70.0, 200.0
    s_true, theta_true = 0.8, 15.0
    Hobs, Vobs = model(s_true, theta_true, h0, A, V)
    relic_obs_kpc = 3000.0  # Fixed-stage idealization. Not a real relic observation.
    theta_cdm_deg = math.degrees(math.acos(Hobs/h0))
    H_cdm, V_cdm = model(0.0, theta_cdm_deg, h0, A, V)
    t = math.radians(theta_true)
    # Rows: H in kpc and Vlos in km/s. Columns: s and theta in radians.
    J = [[-A*math.cos(t), -(h0-A*s_true)*math.sin(t)],
         [0.0, V*math.cos(t)]]
    determinant = J[0][0]*J[1][1]-J[0][1]*J[1][0]
    sigma_s_linear = math.hypot(1.0/(A*math.cos(t))*sig_h,
                                ((h0-A*s_true)*math.tan(t)/A)*sig_v/(V*math.cos(t)))

    s_values = [i/100 for i in range(0,151)]  # 0 to 1.50
    theta_values = [i/10 for i in range(0,501)] # 0 to 50 degrees
    profiles = []
    for s in s_values:
        best = (float('inf'), None)
        for theta in theta_values:
            hp,vp = model(s, theta, h0, A, V)
            chisq = ((hp-Hobs)/sig_h)**2 + ((vp-Vobs)/sig_v)**2
            if chisq < best[0]: best = (chisq, theta)
        profiles.append({'s':s,'profile_chi2':best[0],'best_angle_deg':best[1]})
    minimum = min(profiles, key=lambda row: row['profile_chi2'])
    at_cdm = profiles[0]
    nominal_95 = [row['s'] for row in profiles
                  if row['profile_chi2']-minimum['profile_chi2'] <= 3.841458820694124]
    # Only the H measurement: exact ridge, with s>=0 and theta in [0, 50] deg.
    max_exact_s_from_H = (h0-Hobs)/A
    min_exact_s_from_H = max(0.0,(h0-Hobs/math.cos(math.radians(50.0)))/A)
    controls = {
      'fixed_stage_relic_invariant_by_model_definition': relic_obs_kpc == 3000.0,
      'injection_recovered_on_grid': abs(minimum['s']-s_true)<1e-12 and abs(minimum['best_angle_deg']-theta_true)<1e-12,
      'collisionless_orientation_exact_H_match': abs(H_cdm-Hobs)<1e-9,
      'collisionless_alt_within_50deg': 0<=theta_cdm_deg<=50,
      'collisionless_LOS_speed_differs': abs(V_cdm-Vobs)>400,
      'unconstrained_H_ridge_contains_truth_and_cdm': min_exact_s_from_H <= 0.0 <= s_true <= max_exact_s_from_H,
      'determinant_nonzero_active_merger': abs(determinant)>1,
      'determinant_zero_at_apocenter_v_zero': abs(-A*0.0*math.cos(t)**2)<1e-15,
      'linear_error_finite': 0<sigma_s_linear<2,
      'full_profile_peak_at_injection': minimum['profile_chi2']<1e-15,
      'nominal_profile_region_contains_injection': min(nominal_95)<=s_true<=max(nominal_95),
      'profile_finite_nonnegative': all(math.isfinite(x['profile_chi2']) and x['profile_chi2']>=0 for x in profiles),
      'grid_has_151_profiles': len(profiles)==151,
      'H_only_does_not_identify_s': max_exact_s_from_H-min_exact_s_from_H>1.0,
      'velocity_differentiates_exact_H_mimic': at_cdm['profile_chi2']>0,
    }
    assert all(controls.values()), controls
    receipt = {
      'study_id':'S-01','as_of':'2026-10-17',
      'status':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE_H_ONLY','DATA_INSUFFICIENT_OBSERVATIONS'],
      'evidence':'SIMULATED ONLY; noiseless generating truth and an illustrative Gaussian error model',
      'generating_truth':{'s_dimensionless':s_true,'theta_deg_from_sky_plane':theta_true,
          'H_kpc':Hobs,'Vlos_km_s':Vobs,'relic_separation_kpc':relic_obs_kpc},
      'assumptions':{
          'stage':'held fixed by idealized double-radio-relic reference, not inferred from observational data',
          'h0_kpc':h0,'response_kpc_per_unit_s':A,'v_km_s':V,
          'cross_section_conversion':'s = (sigma/m)/(1 cm^2 g^-1)',
          'H_formula':'(h0-A*s)*cos(theta)', 'Vlos_formula':'V*sin(theta)',
          'relic_formula':'constant stage reference, exact by construction',
          'errors_illustrative':{'sigma_H_kpc':sig_h,'sigma_Vlos_km_s':sig_v,'independent_Gaussian':True},
          'parameter_grid':{'s_min':0.,'s_max':1.50,'s_step':0.01,
                            'theta_min_deg':0.,'theta_max_deg':50.,'theta_step_deg':0.1},
          'limitations':['not calibrated to TNGC-SIDM simulation tracks',
             'not a fit to observed halo/relic/galaxy velocities',
             'relic projection is not exactly angle-independent in real data',
             'relative 3D speed is unknown in real mergers and approaches zero at apocenter',
             'halo mass, impact parameter, phase, source selection, centroids, covariances absent',
             'linear response in s is a pedagogical local approximation, not a physical law',
             'Delta chi2 contour not coverage-calibrated or a confidence limit']},
      'analytic':{'theta_cdm_mimic_deg':theta_cdm_deg,'H_cdm_mimic_kpc':H_cdm,
           'Vlos_cdm_mimic_km_s':V_cdm,
           'H_only_exact_ridge_s_interval':[min_exact_s_from_H,max_exact_s_from_H],
           'Jacobian_rows_H_kpc_and_V_km_s_columns_s_theta_rad':J,
           'Jacobian_determinant_units_kpc_km_s_per_s_per_rad':determinant,
           'linearized_sigma_s_with_velocity':sigma_s_linear},
      'grid':{'best_fit':minimum,'at_s_0':at_cdm,
         'delta_chisquare_s0':at_cdm['profile_chi2']-minimum['profile_chi2'],
         'nominal_delta_chisquare_3p84_s_interval':[min(nominal_95),max(nominal_95)],
         'count_s':len(s_values),'count_theta':len(theta_values),
         'profile_note':'Deterministic normalized-residual squared; not a calibrated p-value or coverage statement'},
      'checks':controls,'checks_passed':sum(controls.values()),
      'random_seed':None,'randomness':'none, deterministic truth and grid',
      'runtime':{'python':platform.python_version(),'workers':1,
                 'core_seconds':time.perf_counter()-tic},
      'source_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    (out/'profile_SIMULATED.csv').write_text('s_dimensionless,profile_chi2,best_theta_deg\n'+''.join(
        f"{p['s']:.2f},{p['profile_chi2']:.12g},{p['best_angle_deg']:.1f}\n" for p in profiles))
    (out/'results.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    assert json.loads((out/'results.json').read_text())['checks_passed']==len(controls)
    print(json.dumps({'best':minimum,'s0':at_cdm,'Honly':receipt['analytic']['H_only_exact_ridge_s_interval'],
          'sigma_s':sigma_s_linear,'nominal_range':receipt['grid']['nominal_delta_chisquare_3p84_s_interval'],
          'checks':len(controls),'code_sha256':receipt['source_code_sha256']},indent=2))

if __name__=='__main__':
    main()
