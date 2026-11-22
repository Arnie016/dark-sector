import argparse,hashlib,json
from pathlib import Path
import numpy as np,h5py
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('mergers',type=Path);ap.add_argument('clusters',type=Path);a=ap.parse_args()
assert hashlib.sha256(a.mergers.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
assert hashlib.sha256(a.clusters.read_bytes()).hexdigest()=='9c5af9f24d8220228c58692b3b7d20777355e50f38ff484a50763a2c5afa39a2'
with h5py.File(a.mergers) as m,h5py.File(a.clusters) as c:
 ids=m['HaloID'][:];orig=c['origID'][:];virtual=c['haloID'][:];mass=c['mhalo_200c'][:];lookup={int(x):i for i,x in enumerate(orig)}
 assert len(set(map(int,orig)))==len(orig)==352 and len(set(map(int,virtual)))==352
 selected=(m['Snap_coll'][:]==99)&(m['M_Crit200_coll'][:]>0);rows=[int(i) for i in np.flatnonzero(selected) if int(ids[i]) in lookup]
 differences=np.array([np.log10(float(m['M_Crit200_coll'][i])*1e14)-float(mass[lookup[int(ids[i])]]) for i in rows])
 out={'merger_rows':len(ids),'unique_merger_ids':len(set(map(int,ids))),'cluster_rows':len(orig),'merger_rows_numerically_matching_orig_id':int(np.isin(ids,orig).sum()),'merger_rows_numerically_matching_virtual_id':int(np.isin(ids,virtual).sum()),'unique_merger_ids_matching_orig_id':len(set(map(int,ids))&set(map(int,orig))),'unique_merger_ids_matching_virtual_id':len(set(map(int,ids))&set(map(int,virtual))),'snap99_positive_collision_mass_rows':int(selected.sum()),'snap99_numerically_matching_orig_id_rows':len(rows),'snap99_log10_mass_abs_difference_median_dex':float(np.median(np.abs(differences))),'snap99_log10_mass_abs_difference_p90_dex':float(np.quantile(np.abs(differences),.9)),'snap99_matching_within_0_001_dex':int(np.sum(np.abs(differences)<.001)),'warning':'Numeric equality is not identity. Mass mismatch does not by itself establish an incorrect join; collision and z=0 estimators or epochs may differ.'}
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
