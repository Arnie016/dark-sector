#!/usr/bin/env python3
"""C10: published rounded Table 2 error arithmetic + SIMULATED shared-bias control.
Source: Jee, Park & Lee, arXiv:2605.00093v2, Table 2, 9 Jul 2026.
Not a reanalysis of the published likelihood or a bound on sigma/m.
"""
import json, math, hashlib, pathlib, sys
P=pathlib.Path(__file__)
# (name, shock Mpc, shock s.d. Mpc, halo Mpc, halo s.d. Mpc).
# OBSERVED AS REPORTED rounded marginals, not event/posterior data.
rows=[
 ('Abell 3376',2.08,.02,1.10,.11),
 ('ZWCL 0008.8+5215',1.61,.02,1.02,.10),
 ('Abell 2345',2.28,.02,1.00,.10),
 ('CIZA J2242.8+5301',2.56,.03,1.07,.29),
 ('Abell 1240',2.23,.02,1.10,.16),
 ('PSZ2 G181.06+48.47',2.70,.02,.50,.12),
 ('RXC J1314.4-2515',1.50,.01,.54,.09),
 ('ZWCL 1856.8+6616',1.92,.02,.66,.09),
 ('MACS J1752.0+4440',2.10,.02,1.19,.07),
 ('ZWCL1447.2+2619',2.01,.02,.36,.15),
 ('ACT-CL J0102-4915',1.82,.02,.77,.13)
]
# MODEL CONTRACT, deliberately restrictive:
# y_i=log(H_i/S_i)-baseline_i = delta + b + eps_i,
# each eps_i independent Gaussian with variance from diagonal-only delta-method,
# delta common hypothetical residual shift, b common unknown calibration error.
# Physical baseline_i and d(logQ)/d(cross-section) are NOT known here.
# The b=0.02 prior s.d. is SIMULATED, NOT an estimate from interpolation tests.
measured=[]
for name,S,sS,H,sH in rows:
    assert min(S,sS,H,sH)>0
    v=(sS/S)**2+(sH/H)**2
    measured.append({'cluster':name,'Q_reported':H/S,'relative_sigma_approx':math.sqrt(v),'variance_logQ_approx':v,'weight':1/v})
ws=[x['weight'] for x in measured]; W=sum(ws)
sigma_stat=1/math.sqrt(W)
effective_n=W*W/sum(w*w for w in ws)
# Project linear-information matrix for theta=(delta,b) with shared calibration prior N(0,tau²).
# F=[[W,W],[W,W+tau^-2]], profiled I_delta = W-W²/(W+tau^-2)
# so variance exactly 1/W+tau² under this declared Gaussian linear model.
tau=.02
prof=W-W**2/(W+tau**-2)
profile_sigma=1/math.sqrt(prof)
closed_sigma=math.sqrt(sigma_stat*sigma_stat+tau*tau)
# deliberately no prior on b: the two columns are identical (rank one).
JtJ=[[W,W],[W,W]]
checks={
 'all_11_positive':len(rows)==11 and all(x['variance_logQ_approx']>0 for x in measured),
 'scale_invariance':all(abs(((10*sS)/(10*S))**2+((10*sH)/(10*H))**2-x['variance_logQ_approx'])<1e-16 for (_,S,sS,H,sH),x in zip(rows,measured)),
 'computed_weights_positive':all(w>0 for w in ws),
 'profile_equals_gaussian_closed_form':abs(profile_sigma-closed_sigma)<1e-12,
 'positive_shared_prior_increases_uncertainty':profile_sigma>sigma_stat,
 'effective_n_valid':1<=effective_n<=11,
 'uninformative_calibration_rank_one':abs(JtJ[0][0]*JtJ[1][1]-JtJ[0][1]*JtJ[1][0])<1e-8,
 'zero_shared_error_limit':abs(math.sqrt(sigma_stat**2+0)-sigma_stat)<1e-15,
 'many_cluster_shared_floor':math.sqrt((sigma_stat/1000)**2+tau**2)>=tau,
}
assert all(checks.values()),checks
out={
 'claim_ids':['C10-C1','C10-C2','C10-C3'],
 'statuses':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE','DATA_INSUFFICIENT'],
 'as_of':'2026-10-29','source':'arXiv:2605.00093v2 Table 2, dated 2026-07-09',
 'data_label':'OBSERVED AS REPORTED rounded marginal distances; NO event observations',
 'hypothetical_model_label':'SIMULATED common-offset nuisance model; NOT published physical likelihood',
 'units':{'shock':'Mpc','halo':'Mpc','Q':'unitless','logQ':'unitless','tau':'unitless'},
 'true_physical_delta':None,'invented_measurements':False,'seed':None,
 'assumptions':['independent per-system Gaussian log-ratio errors','zero within-system correlation for this example','equal unit sensitivity to a hypothetical common shift','shared additive calibration prior N(0,0.02²) for example only','log-linear delta-method, potentially inaccurate for large fractional errors'],
 'n_clusters':11,'sigma_independent_common_shift':sigma_stat,'effective_n_by_inverse_variance':effective_n,
 'assumed_shared_sigma_logQ':tau,'sigma_with_shared_nuisance':profile_sigma,
 'inflation_factor':profile_sigma/sigma_stat,
 'no_prior_joint_information':JtJ,
 'limiting_identifiability':'without a prior, delta and shared b are exactly unidentifiable if sensitivity vectors coincide',
 'per_cluster_data':measured,
 'checks':checks,'checks_passed':sum(checks.values()),
 'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),
 'python':sys.version.split()[0],
 'limitations':['No posterior samples, cluster-specific physical response derivatives, mass priors, shared simulation calibration distribution or selection function fitted.','The 2% assumed shared nuisance is NOT the published within-simulator interpolation test result.','The weighted mean of log-ratio residuals is a schematic common-offset diagnostic, not a physical combined SIDM cross-section.','The 11 published clusters are independent observed systems, but their emulator and geometry calibration may introduce correlated epistemic uncertainty.']}
print(json.dumps(out,indent=2,sort_keys=True))
