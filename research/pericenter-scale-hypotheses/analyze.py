import argparse,csv,hashlib,json
from pathlib import Path
import h5py,numpy as np
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);a=ap.parse_args();assert hashlib.sha256(a.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
src=p.parent/'pericenter-distance-unit-audit/comparison.csv';base=list(csv.DictReader(src.open()));assert len(base)==1977 and len({int(x['row']) for x in base})==1977
zf=p.parent/'merger-collision-ensemble/snapshot_redshifts.json';z={int(x['number']):float(x['redshift']) for x in json.loads(zf.read_text())};h=.6774;rows=[]
with h5py.File(a.catalog) as f:
 for r in base:
  i=int(r['row']);sc=int(r['snap_coll']);ss=[sc-1,sc,sc+1];sn=f['Mhistory_snap'][i];ix=[np.flatnonzero(sn==s) for s in ss];assert all(len(x)==1 for x in ix)
  pos=f['Mhistory_orbit'][i][[int(x[0]) for x in ix]];v=(pos[:,3:]-pos[:,:3]+340000)%680000-340000;d=np.linalg.norm(v,axis=1);scale=np.array([1/(1+z[s]) for s in ss]);target=float(f['d_peri'][i]);assert target>0
  multipliers={'raw':np.ones(3),'divide_h':np.full(3,1/h),'multiply_a':scale,'a_over_h':scale/h,'a_over_h_0_67':scale/.67,'a_over_h_0_69':scale/.69}
  dct={'row':i,'snap_coll':sc}
  for name,m in multipliers.items():dct['best_relative_'+name]=float(np.min(np.abs(d*m-target))/target);dct['best_absolute_'+name]=float(np.min(np.abs(d*m-target)))
  rows.append(dct)
models=['raw','divide_h','multiply_a','a_over_h','a_over_h_0_67','a_over_h_0_69'];out={'catalog_rows':len(rows),'prior_selection_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'h_official':h,'model_results':{}}
for name in models:
 rel=np.array([r['best_relative_'+name] for r in rows]);ab=np.array([r['best_absolute_'+name] for r in rows]);out['model_results'][name]={'median_best_relative_difference':float(np.median(rel)),'absolute_matches_under_0_01':int(np.sum(ab<.01)),'relative_matches_under_0_001':int(np.sum(rel<.001))}
with (p/'comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
