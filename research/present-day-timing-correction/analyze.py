import argparse,hashlib,json
from pathlib import Path
import h5py,numpy as np
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);arg=ap.parse_args()
assert hashlib.sha256(arg.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
h=.6774;om=.3089;ol=.6911
t0=2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om))
zs={int(x['number']):float(x['redshift']) for x in json.loads((p.parent/'merger-collision-ensemble/snapshot_redshifts.json').read_text())}
with h5py.File(arg.catalog) as f:
 t=f['T_coll'][:];ratio=f['Mass_ratio'][:];halo=f['HaloID'][:];old=(f['Snap_full_coll'][:]==99)&(f['TSC_full'][:]>=0)&(f['TSC_full'][:]<=1)&(ratio>=.1); elapsed=t0-t;new=(np.isfinite(t))&(elapsed>=0)&(elapsed<=1)&(ratio>=.1)
 sf=f['Snap_full_coll'][:];ts=f['TSC_full'][:];valid=np.array([int(x) in zs for x in sf]) & (ts>=0)
 a=1/(1+np.array([zs[int(x)] for x in sf[valid]])); t_full=2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*a**1.5)
 residual=np.abs(t_full-t[valid]-ts[valid])
 result={'time_consistency_rows':int(valid.sum()),'median_timing_residual_gyr':float(np.median(residual)),'p90_timing_residual_gyr':float(np.quantile(residual,.9)),'max_timing_residual_gyr':float(np.max(residual)),'cosmological_age_z0_gyr':float(t0),'old_selection_event_rows':int(old.sum()),'new_selection_event_rows':int(new.sum()),'old_recorded_halo_ids':int(len(np.unique(halo[old]))),'new_recorded_halo_ids':int(len(np.unique(halo[new]))),'overlap_event_rows':int((old&new).sum()),'new_rows':np.flatnonzero(new).tolist(),'assumption':'T_coll is cosmic time in Gyr, consistent with catalog fields and prior analysis; numerical epoch approximation excludes radiation.'}
(p/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
