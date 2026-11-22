import argparse,csv,hashlib,json
from pathlib import Path
import numpy as np,h5py
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);a=ap.parse_args()
assert hashlib.sha256(a.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
src=p.parent/'merger-collision-ensemble/collision-comparison.csv';rows=list(csv.DictReader(src.open()));zs={int(x['number']):float(x['redshift']) for x in json.loads((p.parent/'merger-collision-ensemble/snapshot_redshifts.json').read_text())};h=.6774;om=.3089;ol=.6911
age=lambda scale:2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*scale**1.5)
results=[]
with h5py.File(a.catalog) as f:
 for r in rows:
  i=int(r['row']);sc=int(r['snap_coll']);sn=f['Mhistory_snap'][i]; ix=[int(np.flatnonzero(sn==s)[0]) for s in (sc-1,sc,sc+1)]
  pos=f['Mhistory_orbit'][i][ix];scale=np.array([1/(1+zs[s]) for s in (sc-1,sc,sc+1)]);time=age(scale)
  dx=(pos[:,3:]-pos[:,:3]+340000)%680000-340000;dx=np.unwrap(dx*2*np.pi/680000,axis=0)*680000/(2*np.pi);proper=np.linalg.norm(dx,axis=1)*scale/h
  radial=float(np.gradient(proper,time,edge_order=2)[1]*.9777922217); v=float(f['V_coll'][i]);results.append({'row':i,'halo_id':int(r['halo_id']),'snap_coll':sc,'proper_separation_derivative_km_s':radial,'catalog_V_coll_km_s':v,'abs_radial_minus_catalog_km_s':abs(abs(radial)-v)})
assert len(results)==1977
x=np.array([r['abs_radial_minus_catalog_km_s'] for r in results]);summary={'input_event_csv_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'events':len(results),'median_abs_difference_km_s':float(np.median(x)),'p90_abs_difference_km_s':float(np.quantile(x,.9)),'median_catalog_vcoll_km_s':float(np.median([r['catalog_V_coll_km_s'] for r in results])),'median_abs_proper_separation_rate_km_s':float(np.median([abs(r['proper_separation_derivative_km_s']) for r in results])),'warning':'Three-point rate at Snap_coll is NOT reproduction of paper five-point fit or a matched estimator; descriptive only.'}
with (p/'comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]),lineterminator='\n');w.writeheader();w.writerows(results)
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
