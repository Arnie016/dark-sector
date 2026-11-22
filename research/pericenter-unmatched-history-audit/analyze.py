import argparse,csv,hashlib,json
from pathlib import Path
import numpy as np,h5py
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);a=ap.parse_args();assert hashlib.sha256(a.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
src=p.parent/'pericenter-sampled-minimum/comparison.csv';base=list(csv.DictReader(src.open()));sel=[r for r in base if int(r['matches_nearby_proper'])==0];assert len(sel)==549
zs=p.parent/'merger-collision-ensemble/snapshot_redshifts.json';z={int(x['number']):float(x['redshift']) for x in json.loads(zs.read_text())};rows=[]
with h5py.File(a.catalog) as f:
 for r in sel:
  i=int(r['row']);sn=f['Mhistory_snap'][i];pos=f['Mhistory_orbit'][i];valid=np.array([int(s) in z and 30<=int(s)<=99 for s in sn]) & np.isfinite(pos).all(axis=1)&(pos>=0).all(axis=1)&(pos<680000).all(axis=1); ss=sn[valid];pos=pos[valid];assert len(ss)>0 and len(set(map(int,ss)))==len(ss)
  dx=(pos[:,3:]-pos[:,:3]+340000)%680000-340000;proper=np.linalg.norm(dx,axis=1)*np.array([1/(1+z[int(s)]) for s in ss])/.6774;dp=float(f['d_peri'][i]);d=np.abs(proper-dp);best=int(np.argmin(d));rows.append({'row':i,'snap_coll':int(r['snap_coll']),'best_snapshot':int(ss[best]),'best_difference':float(d[best]),'difference_from_history_min':float(abs(np.min(proper)-dp)),'match_any_snapshot':int(d[best]<.01),'match_history_min':int(abs(np.min(proper)-dp)<.01)})
out={'prior_input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'nonmatching_nearby_rows':len(rows),'match_any_valid_snapshot':sum(x['match_any_snapshot'] for x in rows),'match_history_min':sum(x['match_history_min'] for x in rows),'median_best_difference_numeric':float(np.median([x['best_difference'] for x in rows])),'warning':'Broad search is exploratory, uses same catalog and does not establish field units or interpolation.'}
with (p/'comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
