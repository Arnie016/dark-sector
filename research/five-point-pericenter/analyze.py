import argparse,csv,hashlib,json,collections
from pathlib import Path
import h5py,numpy as np
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);a=ap.parse_args();assert hashlib.sha256(a.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
z={int(x['number']):float(x['redshift']) for x in json.loads((p.parent/'merger-collision-ensemble/snapshot_redshifts.json').read_text())}
h=.6774;om=.3089;ol=.6911
age=lambda x:2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*x**1.5)
def fit(t,y):
 center=t[2];coef=np.polyfit(t-center,y,2);curv,slope,intercept=coef
 if curv<=0:return None
 tv=center-slope/(2*curv);yv=np.polyval(coef,tv-center)
 if not (t[0]<=tv<=t[-1]) or yv<0:return None
 return float(tv),float(yv)
# Irregular cadence: a known quadratic has exact minimum t=0.17, y=5.
test_t=np.array([-.4,-.1,.05,.4,.9]);test=fit(test_t,5+3*(test_t-.17)**2);assert np.allclose(test,[.17,5],atol=1e-10)
rows=[];rejections=collections.Counter()
with h5py.File(a.catalog) as f:
 for i in range(len(f['HaloID'])):
  sc=int(f['Snap_coll'][i]);sn=f['Mhistory_snap'][i];ss=list(range(sc-2,sc+3))
  if min(ss)<30 or max(ss)>99 or not all(s in z for s in ss):rejections['window_outside_range']+=1;continue
  ix=[np.flatnonzero(sn==s) for s in ss]
  if any(len(x)!=1 for x in ix):rejections['missing_unique_history']+=1;continue
  pos=f['Mhistory_orbit'][i][[int(x[0]) for x in ix]]
  if not np.isfinite(pos).all() or (pos<0).any() or (pos>=680000).any():rejections['invalid_position']+=1;continue
  delta=(pos[:,3:]-pos[:,:3]+340000)%680000-340000;delta=np.unwrap(delta*2*np.pi/680000,axis=0)*680000/(2*np.pi)
  sep=np.linalg.norm(delta,axis=1);scale=np.array([1/(1+z[s]) for s in ss]);t=age(scale)
  cm=fit(t,sep);pm=fit(t,sep*scale/h)
  if cm is None or pm is None:rejections['invalid_or_unbracketed_fit']+=1;continue
  tc=float(f['T_coll'][i]);dp=float(f['d_peri'][i]);rows.append({'row':i,'halo_id':int(f['HaloID'][i]),'snap_coll':sc,'fit_time_comoving_gyr':cm[0],'fit_sep_comoving_ckpc_h':cm[1],'fit_time_proper_gyr':pm[0],'fit_sep_proper_kpc':pm[1],'catalog_tcoll_gyr':tc,'catalog_dperi_ckpc_h':dp,'abs_time_difference_gyr':abs(cm[0]-tc),'abs_sep_difference_ckpc_h':abs(cm[1]-dp)})
assert len(rows)+sum(rejections.values())==2083
x=np.array([r['abs_time_difference_gyr'] for r in rows]);y=np.array([r['abs_sep_difference_ckpc_h'] for r in rows]);shift=np.array([abs(r['fit_time_comoving_gyr']-r['fit_time_proper_gyr']) for r in rows]);out={'catalog_rows':2083,'accepted':len(rows),'rejections':dict(rejections),'unique_recorded_halo_labels':len({r['halo_id'] for r in rows}),'median_abs_tcoll_difference_gyr':float(np.median(x)),'p90_abs_tcoll_difference_gyr':float(np.quantile(x,.9)),'median_abs_dperi_difference_ckpc_h':float(np.median(y)),'p90_abs_dperi_difference_ckpc_h':float(np.quantile(y,.9)),'median_comoving_vs_proper_vertex_time_shift_gyr':float(np.median(shift)),'p90_comoving_vs_proper_vertex_time_shift_gyr':float(np.quantile(shift,.9)),'warning':'Centered snapshot window and fit assumptions are provisional; this is not an exact reproduction of Lee et al. or a catalog error measurement.'}
with (p/'fits.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
