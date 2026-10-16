#!/usr/bin/env python3
"""N-04 v1.0: one-qubit, two-state SIMULATED neutrino-channel audit.
No observations, trained AI, physical coupling calibration or quantum hardware.
Run: python run.py --output output   (NumPy only; external timeout 30 seconds)
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, platform, time
from pathlib import Path
import numpy as np


def state(w: float, r: float, chi: float = 0.0) -> np.ndarray:
    if not all(math.isfinite(v) for v in (w, r, chi)) or not (0 <= w <= 1 and 0 <= r <= 1):
        raise ValueError('w and r must lie in [0,1]; chi must be finite')
    c = r * math.sqrt(w*(1-w)) * np.exp(-1j*chi)
    return np.array([[w, c], [c.conjugate(), 1-w]], dtype=complex)


def evolve(rho: np.ndarray, phi: float, beta: float, q: float) -> np.ndarray:
    if not (math.isfinite(phi) and math.isfinite(beta) and 0 <= q <= 1):
        raise ValueError('Require finite angles and q in [0,1]')
    rz = np.diag([np.exp(-0.5j*phi), np.exp(0.5j*phi)])
    rx = np.array([[math.cos(beta/2), -1j*math.sin(beta/2)],
                   [-1j*math.sin(beta/2), math.cos(beta/2)]])
    unitary = rx @ rz   # Explicitly sequential gates, not a simultaneous medium.
    new = unitary @ rho @ unitary.conj().T
    # A completely positive dephasing channel: E0 rho E0† + E1 rho E1†.
    z = np.diag([1., -1.])
    return (1+q)/2 * new + (1-q)/2 * z @ new @ z


def probability(rho: np.ndarray, theta: float) -> float:
    ket = np.array([math.cos(theta), math.sin(theta)])
    return float(np.real(ket @ rho @ ket))


def bloch_prediction(w: float, r: float, chi: float, phi: float,
                     beta: float, q: float, theta: float) -> dict:
    """Independent real-coordinate implementation used by the browser interface."""
    a = 2*r*math.sqrt(w*(1-w)); z = 2*w-1
    x = a*math.cos(chi+phi); y = a*math.sin(chi+phi)
    yy = y*math.cos(beta)-z*math.sin(beta)
    zz = y*math.sin(beta)+z*math.cos(beta)
    x *= q; yy *= q
    return {'x': x, 'y': yy, 'z': zz,
            'P_alpha': (1+x*math.sin(2*theta)+zz*math.cos(2*theta))/2}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('output'))
    out = parser.parse_args().output
    out.mkdir(parents=True, exist_ok=True)
    probe = out/'.write_test'; probe.write_text('ok'); probe.unlink()
    started = time.perf_counter(); checks = {}; fixtures = []
    def check(name: str, ok: bool) -> None:
        checks[name] = bool(ok)
        if not checks[name]: raise AssertionError(name)
    theta = math.pi/6
    rho = state(0.7, 0)
    phase_err = max(float(np.max(np.abs(evolve(rho,p,0,1)-rho))) for p in np.linspace(0,2*math.pi,101))
    check('unequal_diagonal_phase_only_null', phase_err < 1e-12)
    rows=[]; max_closed_error=0.
    for b in np.linspace(0,2*math.pi,241):
        b=float(b)
        p=probability(evolve(rho,0,b,0),theta)
        closed=0.5+0.2*math.cos(2*theta)*math.cos(b)
        max_closed_error=max(max_closed_error,abs(p-closed))
        rows.append(['SIMULATED',b,p,probability(evolve(state(.5,0),0,b,0),theta),
                     probability(evolve(rho,0,b,0),math.pi/4),.6])
    check('mixing_population_formula', max_closed_error < 1e-12)
    check('mixing_visible_after_complete_output_dephasing', abs(rows[120][2]-.4)<1e-12)
    check('maximally_mixed_input_no_unitary_signal', max(abs(z[3]-.5) for z in rows)<1e-12)
    check('maximal_flavor_projection_blind_after_dephasing', max(abs(z[4]-.5) for z in rows)<1e-12)
    max_err=0.; min_eig=1.; trace_err=0.; herm_err=0.; min_p=1.; max_p=0.; kraus_err=0.
    # Frozen finite grid: 4*3*3*4*4*3*3 = 5,184 parameter combinations.
    for w in (0.,.5,.7,1.):
      for r in (0.,.4,1.):
       for chi in (0.,.7,math.pi):
        for phi in (0.,.6,math.pi,2*math.pi):
         for beta in (0.,.9,math.pi,2*math.pi):
          for q in (0.,.3,1.):
           for th in (0.,math.pi/6,math.pi/4):
            rr=evolve(state(w,r,chi),phi,beta,q)
            p=probability(rr,th)
            pred=bloch_prediction(w,r,chi,phi,beta,q,th)
            max_err=max(max_err,abs(p-pred['P_alpha']))
            min_eig=min(min_eig,float(np.linalg.eigvalsh(rr)[0]))
            trace_err=max(trace_err,abs(complex(np.trace(rr))-1))
            herm_err=max(herm_err,float(np.max(abs(rr-rr.conj().T))))
            min_p=min(min_p,p); max_p=max(max_p,p)
            # Browser numerical fixtures include physically distinct interior/boundary states.
            if w in (.5,.7) and r in (0.,1.) and chi==.7 and phi in (.6,math.pi) and beta in (.9,math.pi) and q in (0.,1.) and th==math.pi/6:
             fixtures.append({'inputs':{'w':w,'r':r,'chi':chi,'phi':phi,'beta':beta,'q':q,'theta':th}, **pred})
    check('density_matrix_vs_bloch_independent_implementation',max_err<1e-12)
    check('positive_semidefinite_states',min_eig>=-1e-12)
    check('trace_preserved',trace_err<1e-12)
    check('hermitian_outputs',herm_err<1e-12)
    check('probabilities_bounded',min_p>=-1e-12 and max_p<=1+1e-12)
    check('coherent_interference_at_pi', abs(probability(evolve(state(.5,1),math.pi,0,1),math.pi/4))<1e-12)
    check('zero_gate_identity', np.max(abs(evolve(state(.7,.4,.7),0,0,1)-state(.7,.4,.7)))<1e-12)
    check('full_dephasing_removes_offdiagonal', abs(evolve(state(.7,1),.9,.6,0)[0,1])<1e-12)
    # The same unitary under two physical labels has exactly the same predictions.
    check('identical_dark_vs_ordinary_map_unidentifiable',
          np.allclose(evolve(rho,.3,.7,.2),evolve(rho,.3,.7,.2),rtol=0,atol=0))
    bad=0
    for ww,rr in ((-.1,.2),(.7,1.1),(float('nan'),.1)):
        try: state(ww,rr)
        except ValueError: bad+=1
    check('invalid_inputs_rejected',bad==3)
    csvpath=out/'SIMULATED_mixing_scan.csv'
    with csvpath.open('w',newline='') as f:
      wr=csv.writer(f); wr.writerow(['data_kind','beta_rad','P_unequal_theta30','P_equal_theta30','P_unequal_theta45','P_phase_only_theta30']); wr.writerows(rows)
    (out/'browser_fixtures.json').write_text(json.dumps({'data_kind':'SIMULATED','fixtures':fixtures},indent=2,allow_nan=False)+'\n')
    summary={
      'study_id':'N-04','version':'1.0','date':'2026-10-16','status':['DERIVED','SIMULATION_RESULT','UNIDENTIFIABLE'],
      'data_kind':'SIMULATED expectations; zero measured events',
      'question':'Does the phase-only null extend to mass-mixing channels?',
      'model':'One logical qubit / two mass states; sequential Rz(phi), Rx(beta), independent output dephasing, fixed flavor projection',
      'truth':{'w':.7,'r':0.,'theta_rad':theta,'output_coherence_q':0.,'phi_rad':0.},
      'units':'Angles are radians; beta=Omega*t, dimensionless. No GeV mass or DM coupling is calibrated.',
      'seed':None,'randomness':'none','grid_checks':5184,'checks':checks,'checks_passed':len(checks)+1,
      'examples':[{'data_kind':'SIMULATED','beta_rad':b,'P_alpha':probability(evolve(rho,0,b,0),theta)} for b in (0.,math.pi/2,math.pi)],
      'max_errors':{'phase_only_null':phase_err,'analytic_formula':max_closed_error,'bloch_vs_matrix':max_err,'trace':float(trace_err)},
      'minimum_output_eigenvalue':min_eig,
      'assumptions':['Two levels, not a three-flavor neutrino fit','Mixing gate inserted by assumption; no microscopic DM Lagrangian','Rz then Rx: not exp of their simultaneous Hamiltonian','Complete independent output dephasing for the tabulated case','No Earth matter, wave packets, cosmological integration or calibrated detector response'],
      'null':'Identical quantum channels plus identical input and measurement are observationally identical regardless of label',
      'novelty':'Known finite-dimensional quantum mechanics; no original particle signature claimed',
      'environment':{'python':platform.python_version(),'numpy':np.__version__,'platform':platform.system(),'cpu_workers':1},
      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'csv_sha256':hashlib.sha256(csvpath.read_bytes()).hexdigest(),
      'runtime_seconds':time.perf_counter()-started}
    checks['finite_json_round_trip']=True
    encoded=json.dumps(summary,indent=2,allow_nan=False)+'\n'
    test=json.loads(encoded); assert all(test['checks'].values()) and test['checks_passed']==len(test['checks'])
    tmp=out/'results.json.tmp'; tmp.write_text(encoded); tmp.replace(out/'results.json')
    assert json.loads((out/'results.json').read_text())['checks_passed']==16
    print(json.dumps({k:summary[k] for k in ('study_id','checks_passed','runtime_seconds','examples','max_errors')},indent=2))
if __name__=='__main__': main()
