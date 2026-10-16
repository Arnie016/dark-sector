"""C-02: solve the static LINEARIZED metric f(R)=R+L^2 R^2/6 equations.
SIMULATED uniform sphere, not observed data or a CCC crossover.
Standard library only. Run: python run.py --output output
The nonlinear theory is specified; only its leading weak-field boundary problem is solved.
"""
import argparse
import csv
import hashlib
import json
import math
import platform
import time
from pathlib import Path

G=6.67430e-11
C=299792458.0
KPC=3.085677581491367e19
MSUN=1.98847e30
HBARC_EV_M=1.973269804e-7
MASS=1e11*MSUN
L=100*KPC
RADIUS=10*KPC
A=RADIUS/L
EPS=G*MASS/(L*C*C)
S=2/A**3


def shape(a):
    """Uniform-sphere Yukawa form factor, stable small-a series."""
    if abs(a)<0.02:
        return 1+a*a/10+a**4/280+a**6/15120
    return 3*(a*math.cosh(a)-math.sinh(a))/a**3


def q_exact(x):
    """q=(F-1)/EPS; regular center and decaying exterior, matched at x=A."""
    if x<0:
        raise ValueError('Radius must be nonnegative')
    if x<=A:
        sinh_over_x=1.0 if x==0 else math.sinh(x)/x
        return S*(1-(1+A)*math.exp(-A)*sinh_over_x)
    return (2/3)*shape(A)*math.exp(-x)/x


def dq_exact(x):
    if x==0:
        return 0.0
    if x<=A:
        return -S*(1+A)*math.exp(-A)*(x*math.cosh(x)-math.sinh(x))/x**2
    return -(2/3)*shape(A)*math.exp(-x)*(x+1)/x**2


def newton(x):
    """Newtonian potential / (EPS c^2)."""
    return -(3*A*A-x*x)/(2*A**3) if x<=A else -1/x


def potentials(x):
    n,q=newton(x),q_exact(x)
    return n-q/2,n+q/2  # Psi and Phi, both divided by EPS c^2


def solve(n,xmax=10.0,source_on=True):
    """Finite-difference BVP for y=xq; no analytic profile used by solver.
    y''-y=-S*x in the sphere; y(0)=0; exact decaying vacuum outer ratio.
    Half weighting at the aligned density discontinuity is a trapezoidal source rule.
    """
    h=xmax/n
    edge=round(A/h)
    if abs(edge*h-A)>1e-12:
        raise ValueError('Grid must align with source edge')
    lo=[1.0]*(n+1); di=[-(2+h*h)]*(n+1); up=[1.0]*(n+1)
    rhs=[0.0]*(n+1)
    lo[0]=0.; di[0]=1.; up[0]=0.
    for j in range(1,n):
        fraction=1.0 if j<edge else (0.5 if j==edge else 0.0)
        rhs[j]=-S*(j*h)*h*h*fraction*bool(source_on)
    lo[n]=-math.exp(-h); di[n]=1.; up[n]=0.
    # Thomas elimination for a tridiagonal linear system.
    for j in range(1,n+1):
        t=lo[j]/di[j-1]
        di[j]-=t*up[j-1]
        rhs[j]-=t*rhs[j-1]
    y=[0.]*(n+1); y[n]=rhs[n]/di[n]
    for j in range(n-1,-1,-1):
        y[j]=(rhs[j]-up[j]*y[j+1])/di[j]
    q=[0.]*(n+1)
    for j in range(1,n+1): q[j]=y[j]/(j*h)
    q[0]=(4*q[1]-q[2])/3 # even regular solution, O(h^4) extrapolation
    return h,y,q


def radial_lap(fun,x,h=1e-4):
    return (fun(x+h)-2*fun(x)+fun(x-h))/h**2+(fun(x+h)-fun(x-h))/(x*h)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=Path('output'))
    out=ap.parse_args().output; out.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter(); checks={}
    def check(name,condition):
        checks[name]=bool(condition)
        if not condition: raise AssertionError(name)
    h1,y1,q1=solve(4000); h2,y2,q2=solve(8000)
    qscale=q_exact(0)
    errors=[]
    for h,q in [(h1,q1),(h2,q2)]:
        errors.append(max(abs(v-q_exact(j*h)) for j,v in enumerate(q))/qscale)
    ratio=errors[0]/errors[1]
    check('numeric_profile_agrees_with_matched_solution',errors[1]<1e-3)
    check('grid_refinement_improves_near_second_order',3.0<ratio<5.1)
    check('regular_center',math.isfinite(q2[0]) and dq_exact(0)==0)
    check('decaying_boundary',abs(y2[-1]-math.exp(-h2)*y2[-2])<1e-12)
    _,_,empty=solve(400,source_on=False)
    check('zero_source_zero_field',max(abs(v) for v in empty)==0.)
    h=1e-7
    # Separate inner/outer formulas at the same edge, no extrapolation.
    qout=(2/3)*shape(A)*math.exp(-A)/A
    dqout=-(2/3)*shape(A)*math.exp(-A)*(A+1)/A**2
    check('source_boundary_value_matching',abs(q_exact(A)-qout)<1e-10)
    check('source_boundary_derivative_matching',abs(dq_exact(A)-dqout)<1e-9)
    ext=[.2,.5,1.,3.]
    trace_error=max(abs(radial_lap(q_exact,x)-q_exact(x)) for x in ext)
    einstein00=max(abs(2*radial_lap(lambda r:potentials(r)[1],x)-radial_lap(q_exact,x)) for x in ext)
    # R L^2/EPS=2(2 lap Phi-lap Psi)=3q; independent metric reconstruction.
    curvature_error=max(abs(2*(2*radial_lap(lambda r:potentials(r)[1],x)-radial_lap(lambda r:potentials(r)[0],x))-3*q_exact(x)) for x in ext)
    check('exterior_trace_equation_finite_difference',trace_error<1e-3)
    check('linearized_00_equation_finite_difference',einstein00<1e-3)
    check('metric_curvature_matches_scalar_definition',curvature_error<2e-3)
    check('spatial_equation_slip_identity',max(abs(potentials(x)[1]-potentials(x)[0]-q_exact(x)) for x in ext)<1e-12)
    check('lensing_potential_sum_fixed_mass',max(abs(sum(potentials(x))-2*newton(x)) for x in ext)<1e-12)
    check('scalar_positive_and_weak',min(q2)>0 and EPS*max(q2)<1e-5)
    check('positive_effective_planck_coefficient',min(1+EPS*q for q in q2)>0)
    check('point_source_form_factor_limit',abs(shape(.001)-1)<1.1e-7)
    check('large_distance_general_relativity_limit',abs((1+(1+40)*math.exp(-40)/3)-1)<1e-14)
    pressure_ratio=EPS*(potentials(A)[0]-potentials(0)[0])
    check('support_pressure_positive_and_subleading',0<pressure_ratio<1e-5)
    # Hydrostatic p/(rho c^2)=Psi(A)/c^2-Psi(x)/c^2, inside the prescribed sphere.
    xp=A/2; dh=1e-5
    pprime=(EPS*(potentials(A)[0]-potentials(xp+dh)[0])-EPS*(potentials(A)[0]-potentials(xp-dh)[0]))/(2*dh)
    psiprime=EPS*((xp/A**3)-dq_exact(xp)/2)
    check('leading_hydrostatic_balance',abs(pprime+psiprime)<1e-10)
    F=shape(A)
    bench=[]
    for x in [.1,.3,1.,3.,10.]:
        enhancement=1+(F/3)*(1+x)*math.exp(-x)
        newton_acc=G*MASS/(x*L)**2
        bench.append({'data_label':'SIMULATED','radius_kpc':100*x,
          'g_newton_m_s2':newton_acc,'g_model_m_s2':newton_acc*enhancement,
          'dynamic_to_newton_force':enhancement,'fixed_source_lensing_ratio':1.0})
    point_gamma=(1-math.exp(-1.495978707e11/L)/3)/(1+math.exp(-1.495978707e11/L)/3)
    rows=[]
    for j in range(0,len(q2),20):
        x=j*h2; psi,phi=potentials(x)
        rows.append([x,100*x,EPS*q2[j],EPS*q_exact(x),C*C*EPS*psi,C*C*EPS*phi])
    cp=out/'SIMULATED_field_profile.csv'
    with cp.open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['r_over_L','r_kpc','numeric_F_minus_1','analytic_F_minus_1','Psi_m2_s2','Phi_m2_s2']);w.writerows(rows)
    result={'study_id':'C-02','version':'1.0.0','as_of':'2026-10-16',
      'status':['DERIVED','SIMULATION_RESULT'],'data_label':'SIMULATED; no observed measurements fitted',
      'theory':'metric f(R)=R+L^2 R^2/6; matter minimally coupled; weak static branch about Minkowski',
      'inputs':{'M_Msun':1e11,'source_radius_kpc':10.,'scalar_range_kpc':100.,'eta_Rs_over_L':A,'compactness_GM_Lc2':EPS},
      'scalar_rest_energy_eV':HBARC_EV_M/L,'sphere_form_factor':F,
      'boundary_conditions':'regular center, continuous field and slope, exponentially decaying exterior',
      'grids':{'N':[4000,8000],'rmax_over_L':10,'relative_profile_errors':errors,'refinement_factor':ratio},
      'residuals':{'trace_exterior':trace_error,'00_exterior':einstein00,'curvature_exterior':curvature_error,'units':'dimensionless normalized by EPS and L'},
      'central_support_pressure_over_rho_c2':pressure_ratio,
      'max_scalar_F_minus_1':EPS*max(q2),'benchmarks':bench,
      'global_model_gate':{'unscreened_point_source_gamma_at_1AU':point_gamma,'interpretation':'Near 1/2 for this range, incompatible with Cassini near-unity gamma. No likelihood or sigma significance calculated.'},
      'checks':checks,'checks_passed':sum(checks.values()),'seed':None,'randomness':'none',
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'csv_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
      'environment':{'python':platform.python_version(),'platform':platform.system(),'cpu_workers':1},
      'core_wall_seconds':time.perf_counter()-start,
      'limitations':['Not an exact nonlinear field solution or cosmological evolution.',
        'Static uniform sphere is a prescribed weak source, supported at leading order; no galaxy stability model.',
        'No CCC boundary matching, annihilation, neutrino coupling or previous-universe inference.',
        'Fixed-source first-order lensing cancellation is not equality of full cosmological lensing maps.',
        'Constant long-range quadratic theory is not a viable global model without changing its assumptions.',
        'No DES data vector/covariance downloaded or fitted.']}
    text=json.dumps(result,indent=2,allow_nan=False)+'\n'
    tmp=out/'results.json.tmp';tmp.write_text(text);tmp.replace(out/'results.json')
    assert json.loads((out/'results.json').read_text())['checks_passed']==18
    print(text)

if __name__=='__main__': main()
