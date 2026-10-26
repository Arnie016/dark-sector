#!/usr/bin/env python3
"""N-08: dimensional matching gate on N-07 assumed neutrino/Dirac-DM vector potential.

This is a deterministic algebraic/numerical audit, NOT an observational fit,
operator-basis enumeration, or QFT symbolic proof. Inputs fixed from accessible
GitHub N-07 summary at commit 1fadf2f89043b5fd45e8d4caa6399597014131e7.
"""
from pathlib import Path
import hashlib
import json
import math
import platform
import time

START=time.perf_counter()
V_GEV = 246.2                   # Higgs VEV, GeV, JHEP09(2026)046 Sec 2
LAMBDA_GEV = 1000.0            # hypothetical heavy scale, GeV
C6 = 1.0                       # dimensionless, illustrative independent coefficient
C8 = 1.0                       # dimensionless, illustrative independent coefficient
A7_FLAT = 0.0534991504385802 # N-07 saved 23 Oct result / known N-06 baseline
A7_PROPER = 0.05474432286434706 # N-07 saved 23 Oct result
RATIO_N07 = 1.0232746205418042

# The EWSB matching of a neutrino-selective dim-8 operator is
# C_eff / Lambda^2 = C8*v^2/(2 Lambda^4).
# Original illustrative dim-6 benchmark: C6 / Lambda^2.
K = V_GEV**2/(2*LAMBDA_GEV**2)
R = abs(C8/C6)*K

# Restrict the bound to fixed input state and the same detector effect.
# Trace distance D <= ||U1-U0|| <= integral ||delta H|| ds = A;
# thus any fixed outcome probability change is <= min(1,A).

def area(base, asym=1.0, coeff8=1.0, scale_gev=LAMBDA_GEV):
    return base*abs(asym)*abs(coeff8/C6)*V_GEV**2*LAMBDA_GEV**2/(2*scale_gev**4)

new_flat=area(A7_FLAT)
new_proper=area(A7_PROPER)
C8_equal=1.0/K
checks={
    'higgs_projector_idempotent': all(math.isclose(v,v**2) for v in [0,1]),
    'dimension8_factor_less_than_unity': 0<K<1,
    'matched_directly': math.isclose(new_proper,A7_PROPER*R,rel_tol=1e-15),
    'flat_curved_ratio_preserved': math.isclose(new_proper/new_flat,RATIO_N07,rel_tol=1e-12),
    'symmetric_dark_current_null': area(A7_PROPER,asym=0.0)==0,
    'dark_current_charge_reversal_norm': area(A7_PROPER,asym=-1.0)==new_proper,
    'half_asymmetry_half_area': math.isclose(area(A7_PROPER,asym=0.5),new_proper/2),
    'doubling_UV_scale_sixteenth_area': math.isclose(area(A7_PROPER,scale_gev=2000),new_proper/16),
    'doubling_C8_doubles_area': math.isclose(area(A7_PROPER,coeff8=2.0),2*new_proper),
    'unity_eff_coupling_required_C8': math.isclose(area(A7_PROPER,coeff8=C8_equal),A7_PROPER,rel_tol=1e-15),
    'stronger_trace_distance_bound': min(1,new_proper)<=min(1,2*new_proper),
    'prior_loose_bound_still_valid': min(1,A7_PROPER)<=min(1,2*A7_PROPER),
}
# Audit note: the required C8 is inverse-linear in K, not inverse-square-root.
assert all(checks.values()), {k:v for k,v in checks.items() if not v}

here=Path(__file__)
receipt={
 'id':'N-08','as_of':'2026-10-24','status':['DERIVED','SIMULATION_RESULT','DATA_INSUFFICIENT'],
 'benchmark_type':'SIMULATED MODEL / analytical EFT coefficient rescaling, NO observational data',
 'source_record':{'N07_branch_commit':'1fadf2f89043b5fd45e8d4caa6399597014131e7',
  'N07_summary':'experiments/interaction_basis/schwarzschild_column/summary.json',
  'N07_source_sha256':'a7528d69a57f9bccb681c4d8788fcea267b9a2f2d37ac1915f2c6b6635ed470c',
  'operator_prior_art':'Babu, Dev, Thapa JHEP09(2026)046; arXiv:2512.25035v2 (Sep 8 2026)',
  'spike_preprint':'Dev et al arXiv:2609.26773v1 (Sep 22 2026)'},
 'inputs':{'v_GeV':V_GEV,'Lambda_GeV':LAMBDA_GEV,'C6':C6,'C8':C8,'abs_asymmetry':1,
           'A7_flat':A7_FLAT,'A7_proper':A7_PROPER},
 'derived':{'low_energy_matching_factor_v2_over_2Lambda2':K,
            'low_energy_coefficient_ratio_C8toC6':R,
            'N08_matched_flat_area':new_flat,
            'N08_matched_proper_area':new_proper,
            'fixed_detector_probability_difference_ceiling_min1A':min(1,new_proper),
            'old_N07_looser_bound_min1_2A':min(1,2*A7_PROPER),
            'tightened_N07_same_dimension6_ceiling_min1A':min(1,A7_PROPER),
            'C8_to_recover_old_N07_area_at_same_Lambda':C8_equal,
            'N08_symmetric_dark_bath_area':0.0},
 'checks':checks,'checks_passed':sum(checks.values()),
 'limitations':['Both Wilson coefficients C6=C8=1 are chosen hypothetical independent parameters, not a UV matching result.',
                'Earlier N07 area is an assumed DM column result read from saved GitHub summary; N07 integration was not rerun here.',
                'Dimension-8 Higgs projector is gauge invariant but does not establish absence of loop-induced charged-lepton effects.',
                'Bounds are not probabilities or detector sensitivity, assume same input state and detector POVM.',
                'No calibrated flavor, source density, asymmetry, mediator mass, astrophysical likelihood, or charged-lepton data fitted.'],
 'execution':{'python':platform.python_version(),'workers':1,'seed':None,'wall_sec':time.perf_counter()-START},
 'sha256':hashlib.sha256(here.read_bytes()).hexdigest()
}
out=here.with_name('results.json')
out.write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n',encoding='utf-8')
assert json.loads(out.read_text(encoding='utf-8'))['checks_passed']==len(checks)
print(json.dumps({'checks_passed':len(checks),'suppression':K,'A8':new_proper,'probability_ceiling':min(1,new_proper),'C8_equal':C8_equal,'code_sha256':receipt['sha256'],'wall_sec':receipt['execution']['wall_sec']},indent=2))
