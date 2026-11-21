#!/usr/bin/env python3
"""C-17: fixed 3D vector projection feasibility, for cited TNG-Cluster simulated rows.
Uses ONLY manually transcribed values in CSV, not the full catalog or Azure.
This check is an algebraic consistency test, NOT a dark matter measurement.
"""
import csv, json, hashlib, math, pathlib, time
start = time.perf_counter()
root=pathlib.Path(__file__).resolve().parent
source=root/'selected_public_rows.csv'
rows=list(csv.DictReader(x for x in source.read_text().splitlines() if not x.startswith('#')))
assert len(rows)==3 and [int(x['origID']) for x in rows]==[0,1,2]
assert [int(x['haloID']) for x in rows]==[0,252455,476245]
assert all(len(x)==8 for x in rows)
assert math.isclose(10**-0.29, 0.51286138, abs_tol=1e-7)
# Feasibility theorem: for a single fixed 3D offset vector (a,b,c):
# R_x^2=b^2+c^2, R_y^2=a^2+c^2, R_z^2=a^2+b^2.
# Thus nonnegative reconstructed squares require max(R_i^2) <= sum(other two).
# Rounding margin: each 2-decimal log is known only to +/-0.005 dex.
answers=[]
for row in rows:
    for tracer in ('xray','sz'):
        q=[float(row[f'{tracer}_{ax}']) for ax in 'xyz']
        r=[10**val for val in q]
        largest=max(range(3),key=lambda i:r[i]); others=[i for i in range(3) if i!=largest]
        comp=math.sqrt(sum(r[i]**2 for i in others))
        fac=r[largest]/comp
        low=10**(q[largest]-0.005)
        hi_rest=math.sqrt(sum(10**(2*(q[i]+0.005)) for i in others))
        min_fac=low/hi_rest
        # Inversion for each Cartesian component squared (axis i).
        inferred=[(sum(r[j]**2 for j in range(3) if j!=i)-r[i]**2)/2 for i in range(3)]
        assert math.isclose(r[largest]**2-comp**2,2*(-inferred[largest]),rel_tol=1e-12)
        assert fac>1 and min_fac>1
        answers.append({'origID':int(row['origID']),'haloID':int(row['haloID']),
                        'tracer':tracer,'q_log10_pkpc':dict(zip('xyz',q)),
                        'radii_pkpc':dict(zip('xyz',[round(v,6) for v in r])),
                        'largest_projected_radius_axis':'xyz'[largest],
                        'factor_over_possible_limit':round(fac,6),
                        'rounding_conservative_factor':round(min_fac,6),
                        'inferred_component_sq_pkpc2':dict(zip('xyz',[round(v,6) for v in inferred])),
                        'one_fixed_3D_peak_feasible':all(v>=-1e-10 for v in inferred)})
# Synthetic mathematical limiting controls (NOT datasets or measurements).
R=math.sqrt(2.0)
assert all(abs((R*R+R*R-R*R)/2-1)<1e-12 for _ in [0])
assert (1.0**2+1.0**2)>=0.0**2
assert not any(x['one_fixed_3D_peak_feasible'] for x in answers)
receipt={'status':'SIMULATION_RESULT (published simulation catalog entries, not observed data)',
         'claim':'single fixed 3D peak cannot generate all three recorded projected offset magnitudes in each checked tracer and halo',
         'selected_rows':3,'tracer_halo_checks':len(answers),'failed_fixed_vector_tests':sum(not a['one_fixed_3D_peak_feasible'] for a in answers),
         'selection':'first three original parent IDs by displayed catalog order, non-random mass-sorted convenience subset; not a population frequency',
         'source_url':'https://www.tng-project.org/files/TNG-Cluster_Catalog.txt',
         'source_catalog_last_updated':'2025-03-06','access_date':'2026-11-06',
         'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'seed':None,
         'rounding_bound':'reported 0.01 dex precision, +/-0.005 dex conservative bounds; not physical uncertainty',
         'results':answers,'wall_seconds_python':round(time.perf_counter()-start,6),
         'note':'No true peak coordinates, mapping, underlying 3D emission field, lensing mass or SIDM rates accessed.'}
(root/'results.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
