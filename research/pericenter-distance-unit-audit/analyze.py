import argparse,csv,collections,hashlib,json
from pathlib import Path
import h5py,numpy as np
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);arg=ap.parse_args();assert hashlib.sha256(arg.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
src=p.parent/'merger-collision-ensemble/snapshot_redshifts.json';z={int(x['number']):float(x['redshift']) for x in json.loads(src.read_text())};h=.6774;out=[];skip=collections.Counter()
with h5py.File(arg.catalog) as f:
 for i in range(len(f['HaloID'])):
  sc=int(f['Snap_coll'][i]);sn=f['Mhistory_snap'][i];ss=[sc-1,sc,sc+1]
  if not all(s in z and 30<=s<=99 for s in ss):skip['outside_range']+=1;continue
  ix=[np.flatnonzero(sn==s) for s in ss]
  if any(len(x)!=1 for x in ix):skip['missing_unique_snapshot']+=1;continue
  pos=f['Mhistory_orbit'][i][[int(x[0]) for x in ix]];dp=float(f['d_peri'][i])
  if not np.isfinite(pos).all() or (pos<0).any() or (pos>=680000).any() or not np.isfinite(dp) or dp<=0:skip['invalid_position_or_catalog_distance']+=1;continue
  dx=(pos[:,3:]-pos[:,:3]+340000)%680000-340000;com=np.linalg.norm(dx,axis=1);proper=com*np.array([1/(1+z[s]) for s in ss])/h
  dc=abs(com-dp);pp=abs(proper-dp)
  out.append({'row':i,'snap_coll':sc,'catalog_dperi_documented_ckpc_h':dp,'comoving_center':float(com[1]),'proper_center':float(proper[1]),'best_comoving_delta':float(min(dc)),'best_proper_delta':float(min(pp)),'best_comoving_offset':int(np.argmin(dc)-1),'best_proper_offset':int(np.argmin(pp)-1)})
assert len(out)+sum(skip.values())==2083
separated=[r for r in out if abs(1/(1+z[r['snap_coll']])/h-1)>.1]
summary={'scale_separated_subset':len(separated),'scale_separated_proper_matches':sum(r['best_proper_delta']<.01 for r in separated),'scale_separated_comoving_matches':sum(r['best_comoving_delta']<.01 for r in separated),'catalog_rows':2083,'selected':len(out),'rejections':dict(skip),'threshold_numeric':.01,'within_0_01_comoving_any':sum(r['best_comoving_delta']<.01 for r in out),'within_0_01_proper_any':sum(r['best_proper_delta']<.01 for r in out),'within_0_01_both':sum(r['best_comoving_delta']<.01 and r['best_proper_delta']<.01 for r in out),'median_best_comoving_delta':float(np.median([r['best_comoving_delta'] for r in out])),'median_best_proper_delta':float(np.median([r['best_proper_delta'] for r in out])),'redshift_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'warning':'Numeric pattern cannot establish units, event identity, or catalog construction; do not use as conversion.'}
with (p/'comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]),lineterminator='\n');w.writeheader();w.writerows(out)
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
