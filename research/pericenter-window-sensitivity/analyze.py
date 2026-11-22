import argparse,csv,hashlib,json,collections
from pathlib import Path
import h5py,numpy as np
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);a=ap.parse_args();assert hashlib.sha256(a.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
src=p.parent/'merger-collision-ensemble/snapshot_redshifts.json';z={int(x['number']):float(x['redshift']) for x in json.loads(src.read_text())};h=.6774;om=.3089;ol=.6911
age=lambda x:2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*x**1.5)
def fit(t,y):
 c=np.polyfit(t-t[2],y,2)
 if c[0]<=0:return None
 v=t[2]-c[1]/(2*c[0]);d=np.polyval(c,v-t[2])
 return (float(v),float(d)) if t[0]<=v<=t[-1] and d>=0 else None
rows=[];skip=collections.Counter()
with h5py.File(a.catalog) as f:
 for i in range(len(f['HaloID'])):
  sc=int(f['Snap_coll'][i]);sn=f['Mhistory_snap'][i];ss=list(range(sc-3,sc+3))
  if min(ss)<30 or max(ss)>99 or not all(s in z for s in ss):skip['outside_snapshot_range']+=1;continue
  ix=[np.flatnonzero(sn==s) for s in ss]
  if any(len(q)!=1 for q in ix):skip['missing_unique_snapshot']+=1;continue
  pos=f['Mhistory_orbit'][i][[int(q[0]) for q in ix]]
  if not np.isfinite(pos).all() or (pos<0).any() or (pos>=680000).any():skip['invalid_position']+=1;continue
  d=(pos[:,3:]-pos[:,:3]+340000)%680000-340000;d=np.unwrap(d*2*np.pi/680000,axis=0)*680000/(2*np.pi);sep=np.linalg.norm(d,axis=1);t=age(np.array([1/(1+z[s]) for s in ss]))
  left=fit(t[:5],sep[:5]);right=fit(t[1:],sep[1:])
  if left is None or right is None:skip['at_least_one_invalid_fit']+=1;continue
  rows.append({'row':i,'halo_id':int(f['HaloID'][i]),'snap_coll':sc,'left_time_gyr':left[0],'right_time_gyr':right[0],'left_sep_ckpc_h':left[1],'right_sep_ckpc_h':right[1],'abs_window_time_shift_gyr':abs(left[0]-right[0]),'abs_window_sep_shift_ckpc_h':abs(left[1]-right[1]),'catalog_tcoll_gyr':float(f['T_coll'][i]),'catalog_dperi_ckpc_h':float(f['d_peri'][i])})
assert len(rows)+sum(skip.values())==2083
qt=lambda k:[float(v) for v in np.quantile([r[k] for r in rows],[.5,.9])]
out={'catalog_rows':2083,'paired_accepted':len(rows),'rejections':dict(skip),'median_p90_abs_window_time_shift_gyr':qt('abs_window_time_shift_gyr'),'median_p90_abs_window_sep_shift_ckpc_h':qt('abs_window_sep_shift_ckpc_h'),'snapshot_redshifts_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'warning':'Selection and alternative windows are exploratory; neither reproduces verified paper pipeline.'}
with (p/'paired.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
