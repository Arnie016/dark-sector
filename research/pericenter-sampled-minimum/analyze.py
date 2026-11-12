import argparse,csv,collections,hashlib,json
from pathlib import Path
import numpy as np,h5py
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);arg=ap.parse_args();assert hashlib.sha256(arg.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
src=p.parent/'pericenter-distance-unit-audit/comparison.csv';base=list(csv.DictReader(src.open()));assert len(base)==1977 and len({int(x['row']) for x in base})==len(base)
zfile=p.parent/'merger-collision-ensemble/snapshot_redshifts.json';z={int(r['number']):float(r['redshift']) for r in json.loads(zfile.read_text())};rows=[]
with h5py.File(arg.catalog) as f:
 for entry in base:
  i=int(entry['row']);sc=int(entry['snap_coll']);ss=[sc-1,sc,sc+1];history=f['Mhistory_snap'][i];ii=[np.flatnonzero(history==s) for s in ss];assert all(len(x)==1 for x in ii)
  pos=f['Mhistory_orbit'][i][[int(x[0]) for x in ii]];delta=(pos[:,3:]-pos[:,:3]+340000)%680000-340000;com=np.linalg.norm(delta,axis=1);proper=com*np.array([1/(1+z[s]) for s in ss])/.6774;target=float(f['d_peri'][i]);mi=int(np.argmin(proper));v=abs(target-proper);best=int(np.argmin(v));matched=bool(v[best]<.01)
  rows.append({'row':i,'snap_coll':sc,'matches_nearby_proper':int(matched),'best_match_offset':best-1,'sampled_min_offset':mi-1,'distance_to_sampled_min':abs(target-proper[mi]),'matches_sampled_min':int(abs(target-proper[mi])<.01),'catalog_value':target,'sampled_min_proper':float(proper[mi])})
matched=[r for r in rows if r['matches_nearby_proper']];sumry={'input_csv_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'total':len(rows),'matches_nearby_proper':len(matched),'matches_minimum_of_three':sum(r['matches_sampled_min'] for r in rows),'matches_nearby_but_not_minimum':sum(not r['matches_sampled_min'] for r in matched),'best_match_offsets':dict(collections.Counter(str(r['best_match_offset']) for r in matched)),'minimum_offsets':dict(collections.Counter(str(r['sampled_min_offset']) for r in matched)),'tolerance_numeric':.01,'warning':'Association within the same catalog, not independent evidence of units or exact construction.'}
with (p/'comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(p/'summary.json').write_text(json.dumps(sumry,indent=2)+'\n');print(json.dumps(sumry,indent=2))
