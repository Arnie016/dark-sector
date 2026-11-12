import argparse,csv,hashlib,json
from pathlib import Path
import numpy as np,h5py
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);a=ap.parse_args();assert hashlib.sha256(a.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
src=p.parent/'pericenter-sampled-minimum/comparison.csv';base=list(csv.DictReader(src.open()));assert len(base)==1977 and len({int(x['row']) for x in base})==len(base)
zf=p.parent/'merger-collision-ensemble/snapshot_redshifts.json';z={int(x['number']):float(x['redshift']) for x in json.loads(zf.read_text())};h=.6774;om=.3089;ol=.6911
age=lambda a:2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*a**1.5)
rows=[]
with h5py.File(a.catalog) as f:
 for x in base:
  i=int(x['row']);s=int(x['snap_coll']);tc=float(f['T_coll'][i]);times=np.array([age(1/(1+z[q])) for q in (s-1,s,s+1)]);ds=times-tc
  rows.append({'row':i,'snap_coll':s,'nearby_proper_match':int(x['matches_nearby_proper']),'tcoll_gyr':tc,'delta_center_gyr':float(ds[1]),'nearest_three_abs_delta_gyr':float(np.min(np.abs(ds))),'nearest_time_offset':int(np.argmin(abs(ds))-1)})
summary={'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'warning':'Cosmic time convention is an assumption; association does not establish causality or construction.','groups':{}}
for key,val in [('distance_match',1),('distance_nonmatch',0)]:
 subset=[r for r in rows if r['nearby_proper_match']==val]; x=np.array([r['delta_center_gyr'] for r in subset]); y=np.array([r['nearest_three_abs_delta_gyr'] for r in subset]); summary['groups'][key]={'n':len(subset),'median_signed_center_delta_gyr':float(np.median(x)),'median_nearest_abs_delta_gyr':float(np.median(y)),'p90_nearest_abs_delta_gyr':float(np.quantile(y,.9)),'nearest_within_0_01_gyr':int(np.sum(y<.01))}
with (p/'comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
