import argparse,csv,json,hashlib
from pathlib import Path
import numpy as np,h5py
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);args=ap.parse_args()
assert hashlib.sha256(args.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
source=p.parent/'merger-collision-ensemble/collision-comparison.csv'
rows=list(csv.DictReader(source.open()))
input_sha256=hashlib.sha256(source.read_bytes()).hexdigest()
assert len(rows)==1977 and len({int(r['row']) for r in rows})==1977
res=[]
with h5py.File(args.catalog) as f:
 for r in rows:
  i=int(r['row']); sc=int(f['Snap_coll'][i]);sf=int(f['Snap_full_coll'][i]);sn=f['Mhistory_snap'][i];vel=f['Mhistory_vel'][i];vc=float(f['V_coll'][i]);ds=[]
  for offset in (-1,0,1):
   k=np.flatnonzero(sn==sc+offset); assert len(k)==1
   v=vel[k[0]];ds.append(float(abs(np.linalg.norm(v[3:]-v[:3])-vc)))
  assert abs(ds[1]-float(r['vc_abs_difference_km_s']))<1e-6
  res.append({'row':i,'halo_id':int(r['halo_id']),'same_full_snapshot':int(sc==sf),'match_previous':int(ds[0]<.1),'match_current':int(ds[1]<.1),'match_next':int(ds[2]<.1),'diff_previous':ds[0],'diff_current':ds[1],'diff_next':ds[2]})
summary={'input_csv_sha256':input_sha256,'threshold_km_s':0.1}
for label,subset in [('all',res),('same_full_snapshot',[r for r in res if r['same_full_snapshot']]),('different_full_snapshot',[r for r in res if not r['same_full_snapshot']])]:
 n=len(subset)
 summary[label]={'n':n,'distinct_halos':len({r['halo_id'] for r in subset}),'matches_current':sum(r['match_current'] for r in subset),'matches_previous':sum(r['match_previous'] for r in subset),'matches_next':sum(r['match_next'] for r in subset),'matches_any_adjacent':sum(any(r[k] for k in ('match_previous','match_current','match_next')) for r in subset),'median_current_difference_km_s':float(np.median([r['diff_current'] for r in subset])) if n else None}
with (p/'audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(res[0]),lineterminator='\n');w.writeheader();w.writerows(res)
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
