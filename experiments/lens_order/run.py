"""L-03: SIMULATED thin-lens geometry audit; no observational data.
Python standard library only. Run: python run.py --output output
The scalar two-plane thin-lens map is established Pen & Mao (2005/2006) prior art.
"""
import argparse
import csv
import hashlib
import json
import math
import platform
import time
from pathlib import Path

I = [[1., 0.], [0., 1.]]
Z = [[0., 0.], [0., 0.]]

def add(a, b, scale=1.):
    return [[a[i][j]+scale*b[i][j] for j in range(2)] for i in range(2)]

def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def mv(a,x):
    return [sum(a[i][j]*x[j] for j in range(2)) for i in range(2)]

def tr(a):
    return [list(v) for v in zip(*a)]

def err(a,b):
    return max(abs(a[i][j]-b[i][j]) for i in range(2) for j in range(2))

def U(kappa, gamma, phi):
    c,s = gamma*math.cos(2*phi),gamma*math.sin(2*phi)
    return [[kappa+c,s],[s,kappa-c]]

def jac(u1,u2,b):
    return add(add(add(I,u1,-1),u2,-1),mm(u2,u1),b)

def omega(a):
    # Antisymmetric mapping coefficient, NOT directly a measured angle.
    return (a[1][0]-a[0][1])/2

def point_alpha(x,center,strength):
    # All angles in arcsec; strength is reduced Einstein angle squared, arcsec^2.
    d = [x[i]-center[i] for i in range(2)]
    r2 = sum(v*v for v in d)
    if r2 == 0:
        raise ValueError('Point lens singularity')
    return [strength*v/r2 for v in d]

def point_U(x,center,strength):
    d = [x[i]-center[i] for i in range(2)]
    r2 = sum(v*v for v in d)
    if r2 == 0:
        raise ValueError('Point lens singularity')
    return [[strength*((1 if i==j else 0)/r2-2*d[i]*d[j]/r2**2)
             for j in range(2)] for i in range(2)]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('output'))
    out=parser.parse_args().output
    out.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter()
    checks={}
    def check(name,value):
        checks[name]=bool(value)
        if not checks[name]:
            raise AssertionError(name)

    k1,k2,g1,g2,b=.2,.15,.1,.08,.5
    u1=U(k1,g1,0.)
    rows=[]
    max_formula_error=0.
    for degree in range(-90,91):
        phi=math.radians(degree)
        u2=U(k2,g2,phi)
        a=jac(u1,u2,b)
        expected=b*g1*g2*math.sin(2*phi)
        max_formula_error=max(max_formula_error,abs(omega(a)-expected))
        rows.append([degree,omega(a),expected,omega(jac(u1,u2,0.))])
    example=jac(u1,U(k2,g2,math.pi/4),b)
    check('no_lens_identity',err(jac(Z,Z,b),I)==0)
    check('one_scalar_plane_is_symmetric',err(jac(u1,Z,b),tr(jac(u1,Z,b)))<1e-15)
    check('zero_plane_separation_factor_null',abs(omega(jac(u1,U(k2,g2,.7),0.)))<1e-15)
    check('aligned_axes_commute',abs(omega(jac(u1,U(k2,g2,0.),b)))<1e-15)
    check('perpendicular_axes_commute',abs(omega(jac(u1,U(k2,g2,math.pi/2),b)))<1e-15)
    check('angular_formula_181_points',max_formula_error<1e-15)
    check('transpose_on_algebraic_order_reversal',err(jac(U(k2,g2,math.pi/4),u1,b),tr(example))<1e-15)
    check('isotropic_terms_do_not_change_antisymmetry',abs(omega(example)-omega(jac(U(0,g1,0),U(0,g2,math.pi/4),b)))<1e-15)
    angle=.37
    q=[[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]]
    rotated=jac(mm(mm(q,u1),tr(q)),mm(mm(q,U(k2,g2,math.pi/4)),tr(q)),b)
    check('proper_basis_rotation_preserves_omega',abs(omega(rotated)-omega(example))<1e-15)
    check('fixed_lens_count_different_geometry',abs(omega(example)-.004)<1e-15 and omega(jac(u1,U(k2,g2,0.),b))==0.)

    # Independent check: differentiate a NONLINEAR two-point-lens ray map.
    x=[.1,.6]; c1=[-.5,.1]; c2=[.4,-.3]; s1=.02; s2=.03
    def ray(x):
        a1=point_alpha(x,c1,s1)
        x2=[x[i]-b*a1[i] for i in range(2)]
        a2=point_alpha(x2,c2,s2)
        return [x[i]-a1[i]-a2[i] for i in range(2)]
    a1=point_alpha(x,c1,s1)
    x2=[x[i]-b*a1[i] for i in range(2)]
    analytic=jac(point_U(x,c1,s1),point_U(x2,c2,s2),b)
    def fd(h):
        a=[[0.,0.],[0.,0.]]
        for j in range(2):
            xp=x.copy(); xm=x.copy(); xp[j]+=h; xm[j]-=h
            yp,ym=ray(xp),ray(xm)
            for i in range(2): a[i][j]=(yp[i]-ym[i])/(2*h)
        return a
    e1,e2=err(analytic,fd(1e-5)),err(analytic,fd(5e-6))
    check('nonlinear_ray_finite_difference',max(e1,e2)<2e-9)

    csvpath=out/'SIMULATED_orientation_scan.csv'
    with csvpath.open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['relative_shear_angle_deg','omega_matrix_dimensionless','omega_formula_dimensionless','omega_no_coupling_dimensionless'])
        w.writerows(rows)
    result={
        'study_id':'L-03','version':'1.0.0','as_of':'2026-10-16',
        'status':['DERIVED','SIMULATION_RESULT'],
        'data_kind':'SIMULATED local lens maps; zero observations',
        'seed':None,'randomness':'none; deterministic finite-domain audit',
        'assumptions':['Two scalar thin-lens planes, flat-sky geometric optics.',
          'Tidal matrices evaluated along the deflected ray; static lenses.',
          'No near-horizon Kerr ray tracing, photon polarization rotation or quantum interference.',
          'Changing algebraic order at fixed reduced strengths is not moving real lenses while preserving cosmological distances.'],
        'inputs':{'kappa1':k1,'gamma1':g1,'kappa2':k2,'gamma2':g2,'distance_factor_b':b,
          'all_matrix_entries_dimensionless':True,'scan_relative_angles_deg':[-90,90],
          'scan_count':len(rows),'nonlinear_control':{'x_arcsec':x,'center1_arcsec':c1,
          'center2_arcsec':c2,'strength1_arcsec2':s1,'strength2_arcsec2':s2}},
        'example_at_45deg':{'A_image_to_source':example,'omega_dimensionless':omega(example),
          'omega_is_not_a_measured_angle':True},
        'errors':{'max_angular_identity_error':max_formula_error,
          'nonlinear_finite_difference_h1e5_arcsec':e1,'nonlinear_finite_difference_h5e6_arcsec':e2},
        'checks':checks,'checks_passed':sum(checks.values()),
        'not_claimed':['Dark matter particle identification','Observed lens rotation','Fibonacci or pi-based lens law',
          'Unique mass-map recovery','Number of physical lenses recovered','Full observational likelihood reproduction'],
        'environment':{'python':platform.python_version(),'platform':platform.system(),'workers':1},
        'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'csv_sha256':hashlib.sha256(csvpath.read_bytes()).hexdigest(),
        'core_wall_seconds':time.perf_counter()-start}
    text=json.dumps(result,indent=2,allow_nan=False)+'\n'
    tmp=out/'results.json.tmp'; tmp.write_text(text); tmp.replace(out/'results.json')
    assert json.loads((out/'results.json').read_text())['checks_passed']==11
    print(text)

if __name__=='__main__':
    main()
