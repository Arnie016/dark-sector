#!/usr/bin/env python3
"""N-11: SIMULATED two-energy-bin, two-source identifiability gate.
Only a transparent two-state CONSTANT-H toy. No detector/astrophysical data.
"""
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

COLUMNS = ((1.0, 1.0), (2.0, 0.5))  # dimensionless source columns (dark, ordinary)
ENERGIES = (1.0, 2.0)              # dimensionless E/E0, not physical TeV
HOLDOUT_ENERGY = 3.0
L = 3.0                            # dimensionless length in inverse-energy units
TRUE_THETA = (0.4, 0.2)
ALT_THETA = (0.2, 0.4)
TRUE_W = (0.7, 0.7)                 # source electron fractions, constant across E


def p(v, energy, length=L):
    delta = 1.0 / energy
    freq = math.hypot(delta, v)
    return delta**2 / freq**2 * math.sin(length * freq / 2.0)**2


def dpdv(v, energy):
    delta = 1.0 / energy
    freq = math.hypot(delta, v)
    q = L * freq / 2.0
    return delta**2 * v / freq**4 * (-2.0 * math.sin(q)**2 + q * math.sin(2.0*q))


def v(column, theta):
    return sum(a*b for a, b in zip(column, theta))


def z(vv, w, energy):
    prob = p(vv, energy)
    return (1.0-w) + (2.0*w-1.0)*prob


def recover_w(obs, vv, energy):
    prob = p(vv, energy)
    den = 2.0*prob - 1.0
    if abs(den) < 1e-12:
        raise ValueError('Source fraction cannot be recovered when p=1/2')
    return (obs - 1.0 + prob) / den


def jacobian(columns, theta, ws, energies=ENERGIES):
    output = []
    for j, column in enumerate(columns):
        vv = v(column,theta)
        for en in energies:
            deriv = (2.0*ws[j]-1.0)*dpdv(vv,en)
            row=[deriv*column[0],deriv*column[1],0.0,0.0]
            row[2+j]=2.0*p(vv,en)-1.0
            output.append(row)
    return output


def det(mat):
    n=len(mat)
    a=[list(map(float,row)) for row in mat]
    prod=1.0
    for i in range(n):
        pivot=max(range(i,n),key=lambda k: abs(a[k][i]))
        if abs(a[pivot][i])<1e-13: return 0.0
        if pivot!=i:
            a[i],a[pivot]=a[pivot],a[i]
            prod=-prod
        x=a[i][i]
        prod*=x
        for j in range(i+1,n):
            c=a[j][i]/x
            for k in range(i+1,n): a[j][k]-=c*a[i][k]
    return prod


def source_block_det(column, theta, w):
    vv=v(column,theta)
    e1,e2=ENERGIES
    s1=(2*w-1)*dpdv(vv,e1)
    s2=(2*w-1)*dpdv(vv,e2)
    return s1*(2*p(vv,e2)-1)-s2*(2*p(vv,e1)-1)


def check_results():
    checks={}
    def chk(name,condition):
        checks[name]=bool(condition)
        if not condition: raise AssertionError(name)
    observations=[]
    alternative_constant=[]
    alternative_flexible=[]
    alternatives_w=[]
    for j,col in enumerate(COLUMNS):
        vt=v(col,TRUE_THETA)
        va=v(col,ALT_THETA)
        obs1=z(vt,TRUE_W[j],ENERGIES[0])
        wa=recover_w(obs1,va,ENERGIES[0])
        alternatives_w.append(wa)
        for en in ENERGIES:
            obs=z(vt,TRUE_W[j],en)
            observations.append(obs)
            alternative_constant.append(z(va,wa,en))
            alternative_flexible.append(z(va,recover_w(obs,va,en),en))
    J=jacobian(COLUMNS,TRUE_THETA,TRUE_W)
    d=det(J)
    cd=COLUMNS[0][0]*COLUMNS[1][1]-COLUMNS[0][1]*COLUMNS[1][0]
    block=source_block_det(COLUMNS[0],TRUE_THETA,TRUE_W[0])*source_block_det(COLUMNS[1],TRUE_THETA,TRUE_W[1])
    chk('all_truth_probabilities_physical',all(0<=x<=1 for x in observations))
    chk('fixed_spectrum_4x4_local_rank',abs(d)>1e-7)
    chk('determinant_factors_into_column_and_spectral_gates',abs(abs(d)-abs(cd*block))<1e-12)
    chk('analytic_derivative_agrees_with_finite_difference',all(abs(dpdv(v(COLUMNS[j],TRUE_THETA),en)-(p(v(COLUMNS[j],TRUE_THETA)+1e-5,en)-p(v(COLUMNS[j],TRUE_THETA)-1e-5,en))/2e-5)<1e-9 for j in range(2) for en in ENERGIES))
    chk('two_sources_fit_first_bin_after_nuisance_adjustment',all(abs(observations[2*j]-alternative_constant[2*j])<1e-13 for j in range(2)))
    chk('alternative_constant_source_fails_second_bin',abs(observations[3]-alternative_constant[3])>1e-3)
    chk('free_energy_dependent_source_exactly_mimics_two_bins',max(abs(a-b) for a,b in zip(observations,alternative_flexible))<1e-12)
    ws_flexible=[recover_w(obs,v(COLUMNS[j],ALT_THETA),en) for j in range(2) for en,obs in zip(ENERGIES,observations[2*j:2*j+2])]
    chk('all_alternative_source_fractions_are_physical',all(0<=w<=1 for w in ws_flexible))
    chk('proportional_columns_have_zero_rank',det(jacobian(((1,1),(2,2)),TRUE_THETA,TRUE_W))==0)
    chk('maximally_mixed_source_blind_to_potential',det(jacobian(COLUMNS,TRUE_THETA,(0.5,0.7)))==0)
    chk('zero_potential_first_derivative',dpdv(0,1.0)==0)
    chk('global_sign_flip_exactly_invariant',all(abs(z(v(col,TRUE_THETA),TRUE_W[j],en)-z(v(col,tuple(-q for q in TRUE_THETA)),TRUE_W[j],en))<1e-14 for j,col in enumerate(COLUMNS) for en in ENERGIES))
    chk('spectral_dependence_is_not_constant',any(abs(p(v(col,TRUE_THETA),1)-p(v(col,TRUE_THETA),2))>1e-2 for col in COLUMNS))
    chk('zero_path_length_limit',all(abs(p(v(col,TRUE_THETA),en,length=0.0))<1e-15 for col in COLUMNS for en in ENERGIES))
    holdout=[z(v(col,TRUE_THETA),TRUE_W[j],HOLDOUT_ENERGY) for j,col in enumerate(COLUMNS)]
    alternative_holdout=[z(v(col,ALT_THETA),alternatives_w[j],HOLDOUT_ENERGY) for j,col in enumerate(COLUMNS)]
    chk('holdout_rejects_first_bin_tuned_alt_for_source_2',abs(holdout[1]-alternative_holdout[1])>1e-3)
    return dict(study='N-11',date='2026-10-26',status='DERIVED + SIMULATION_RESULT + UNIDENTIFIABLE + DATA_INSUFFICIENT',data_class='SIMULATED TOY MODEL ONLY: no astrophysical or detector data',seed=None,
       model='constant two-state H=(Delta(E) sigma_x + v sigma_z)/2, Delta(E)=1/E, L=3, v=theta_chi*x+theta_e*y',
       units='all energy/length/density/coupling coordinates dimensionless and normalized, no TeV/GeV prediction',
       parameters=dict(columns=COLUMNS,energies=ENERGIES,holdout_energy=HOLDOUT_ENERGY,L=L,theta_truth=TRUE_THETA,theta_alt=ALT_THETA,w_truth=TRUE_W),
       observations_simulated=observations,alternative_same_w_per_source=alternative_constant,alternative_free_w_per_energy=alternative_flexible,
       alternative_w_from_first_bin=alternatives_w,alternative_w_per_energy=ws_flexible,holdout_truth=holdout,holdout_alt_fixed_w=alternative_holdout,
       jacobian=J,jacobian_determinant=d,column_determinant=cd,source_spectral_det_product=block,
       checks=checks,checks_passed=len(checks),limitations=['Fixed two-state coherent toy, not phase-averaged 3-flavor source-to-detector likelihood.',
          'Production fractions held constant with energy only in the conditional identification test.',
          'Equal-prior full-rank Jacobian does not imply finite detector sensitivity or absence of global discrete degeneracy.',
          'Sign reversal of both matter couplings is exactly invisible in this constant-H model.',
          'No source-resolved flavors, IceCube detector response, covariance, physical density columns, electroweak model or paid compute.'])


def main():
    result=check_results()
    result['environment']={'python':platform.python_version(),'system':platform.system()}
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('results.json')
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    reread=json.loads(path.read_text())
    assert reread['checks_passed']==len(reread['checks']) and all(reread['checks'].values())
    print(json.dumps({'checks':result['checks_passed'],'detJ':result['jacobian_determinant'],
                     'truth':result['observations_simulated'],'alternative':result['alternative_same_w_per_source'],
                     'w_flexible':result['alternative_w_per_energy'],'holdout':result['holdout_truth'],
                     'alt_holdout':result['holdout_alt_fixed_w'],'source_sha256':result['source_sha256']}))

if __name__=='__main__':
    main()
