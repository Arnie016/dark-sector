"""C-01: SIMULATED ideal lensing tomography; no telescope data or CCC solver.
Run: python run.py --output output
Python standard library only. One deterministic finite calculation.
"""
import argparse
import csv
import hashlib
import json
import math
import platform
import time
from pathlib import Path

C_KMS = 299792.458
H0 = 67.4
OM = .315
OL = 1-OM

def distance(z: float, n: int = 2048) -> float:
    """Comoving distance in Mpc, flat matter+Lambda only, domain 0<=z<=3."""
    if not 0 <= z <= 3 or n < 2 or n % 2:
        raise ValueError('Require 0<=z<=3 and an even n>=2')
    if z == 0:
        return 0.
    h = z/n
    def f(x):
        return 1/math.sqrt(OM*(1+x)**3+OL)
    total = f(0)+f(z)+math.fsum((4 if i%2 else 2)*f(i*h) for i in range(1,n))
    return C_KMS/H0*h*total/3

def weights(lens_chi, source_chi):
    return [max(0.,1-x/source_chi) if source_chi>0 else 0. for x in lens_chi]

def dot(x,y):
    return math.fsum(a*b for a,b in zip(x,y))

def det(w):
    return w[0][0]*w[1][1]-w[0][1]*w[1][0]

def solve(w,y):
    d=det(w)
    if abs(d)<1e-14:
        raise ValueError('Unidentifiable or ill-conditioned 2x2 map')
    return [(w[1][1]*y[0]-w[0][1]*y[1])/d,(-w[1][0]*y[0]+w[0][0]*y[1])/d]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('output'))
    out=p.parse_args().output
    out.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter()
    tests={}
    def check(name,value):
        tests[name]=bool(value)
        if not tests[name]:
            raise AssertionError(name)
    zl=[.3,.8]; zs=[1.,2.]
    xl=[distance(z) for z in zl]; xs=[distance(z) for z in zs]
    W=[weights(xl,s) for s in xs]
    qa=[.02,.01]
    qb=[qa[0]+.006*W[0][1]/W[0][0],qa[1]-.006]
    ya=[dot(w,qa) for w in W]; yb=[dot(w,qb) for w in W]
    d=det(W); d_exact=(xl[1]-xl[0])*(1/xs[0]-1/xs[1])
    check('distance_zero',distance(0)==0)
    check('monotonic_distances',all(x<y for x,y in zip(xl+xs,(xl+xs)[1:])))
    check('quadrature_doubling',max(abs(distance(z)-distance(z,4096))/distance(z) for z in zl+zs)<1e-11)
    check('low_redshift_distance',abs(distance(1e-6)/(C_KMS/H0*1e-6)-1)<1e-6)
    check('source_in_front_null',weights(xl,distance(.1))==[0.,0.])
    check('source_at_lens_null',weights([xl[0]],xl[0])==[0.])
    check('no_excess_mass_null',dot(W[0],[0.,0.])==0)
    check('positive_strengths',all(q>0 for q in qa+qb))
    check('first_source_degenerate',abs(ya[0]-yb[0])<1e-14)
    check('second_source_separates_selected_pair',abs(ya[1]-yb[1])>1e-4)
    check('determinant_identity',abs(d-d_exact)<1e-14 and d>0)
    check('recover_both_amplitudes',max(abs(x-y) for q,yv in [(qa,ya),(qb,yb)] for x,y in zip(solve(W,yv),q))<1e-14)
    check('duplicate_source_no_extra_rank',det([W[0],W[0]])==0)
    check('coincident_lens_no_extra_rank',abs(det([weights([xl[0]]*2,s) for s in xs]))<1e-14)
    # Algebraic illustration of g_kk=0, not an optical ray-tracing simulation.
    gkk=max(abs(-1+math.cos(t)**2+math.sin(t)**2) for t in [0.,.3,1.2,2.4])
    check('null_metric_contraction',gkk<1e-15)
    accel=-.5*OM+OL
    check('background_acceleration_positive',accel>0)
    rows=[]
    for i in range(121):
        z=i/40
        w=weights(xl,distance(z))
        rows.append([z,dot(w,qa),dot(w,qb)])
    cp=out/'SIMULATED_source_redshift_scan.csv'
    with cp.open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['source_redshift','kappa_model_A','kappa_model_B'])
        writer.writerows(rows)
    result={
      'study_id':'C-01','version':'1.0.0','date':'2026-10-16',
      'status':['DERIVED','SIMULATION_RESULT'],
      'data_kind':'SIMULATED ideal convergence expectations; no sampled or observed events',
      'random_seed':None,'randomness':'none',
      'cosmology':{'H0_km_s_Mpc':H0,'Omega_m':OM,'Omega_Lambda':OL,'flat':True,'radiation_omitted':True},
      'lens_redshifts':zl,'source_redshifts':zs,'lens_comoving_Mpc':xl,'source_comoving_Mpc':xs,
      'W_dimensionless':W,'determinant':d,
      'plane_strengths_dimensionless':{'A':qa,'B':qb},
      'SIMULATED_convergences':{'A':ya,'B':yb},
      'second_source_absolute_difference':abs(ya[1]-yb[1]),
      'background_acceleration_over_H0_squared_today':accel,
      'checks':tests,'checks_passed':sum(tests.values()),
      'limitations':['Fixed two-plane geometry and known angular profiles; no unique arbitrary 3D reconstruction.',
        'Absolute convergence is assumed available; shear alone has additional mass-sheet/source ambiguities.',
        'No noise, covariance, photometric redshift uncertainty or survey selection.',
        'Linear/Born weak lensing; does not include L-03 lens-lens coupling.',
        'No annihilation interaction, time-varying constants, CCC boundary solution or neutrino detector forecast.',
        'Lambda-null is direct Ricci focusing only; cosmological distances and growth still depend on Lambda.'],
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'csv_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
      'environment':{'python':platform.python_version(),'platform':platform.system(),'workers':1},
      'numerical_wall_seconds':time.perf_counter()-start}
    text=json.dumps(result,indent=2,allow_nan=False)+'\n'
    tmp=out/'results.tmp'; tmp.write_text(text); tmp.replace(out/'results.json')
    assert json.loads((out/'results.json').read_text())['checks_passed']==16
    print(text)
if __name__=='__main__':
    main()
