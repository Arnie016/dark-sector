import argparse,csv,hashlib,json
from pathlib import Path
import h5py,numpy as np
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);a=ap.parse_args()
assert hashlib.sha256(a.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
z={int(x['number']):float(x['redshift']) for x in json.loads((p.parent/'merger-collision-ensemble/snapshot_redshifts.json').read_text())}
h=.6774;om=.3089;ol=.6911
def age(x):return 2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*np.asarray(x)**1.5)
t0=float(age(1.))
with h5py.File(a.catalog) as f:
 sc=f['Snap_full_coll'][:];tc=f['T_coll'][:];ts=f['TSC_full'][:];mr=f['Mass_ratio'][:]
 valid=np.array([int(s) in z for s in sc])&np.isfinite(tc)&np.isfinite(ts)&(ts>=0)&np.isfinite(mr)
 ids=np.flatnonzero(valid);tf=age([1/(1+z[int(s)]) for s in sc[ids]])
 direct=t0-tc[ids];derived=ts[ids]+t0-tf; delta=direct-derived
 ratio=mr[ids]>=.1; one=ratio&(direct>=0)&(direct<=1);two=ratio&(derived>=0)&(derived<=1)
 summary={'valid_rows':len(ids),'t0_gyr':t0,'median_signed_direct_minus_derived_gyr':float(np.median(delta)),'p90_absolute_difference_gyr':float(np.quantile(abs(delta),.9)),'max_absolute_difference_gyr':float(np.max(abs(delta))),'direct_selection_rows':int(sum(one)),'full_snapshot_selection_rows':int(sum(two)),'intersection_rows':int(sum(one&two)),'direct_only_rows':ids[one&~two].tolist(),'full_only_rows':ids[two&~one].tolist(),'warning':'Both estimates share cosmology; this is sensitivity to field interpretation, not independent validation or a confidence interval.'}
 with (p/'comparison.csv').open('w',newline='') as out:
  w=csv.writer(out,lineterminator='\n');w.writerow(['row','snapshot_full','elapsed_tcoll_gyr','elapsed_tsc_full_gyr','delta_gyr','mass_ratio','selected_tcoll','selected_tsc_full']);w.writerows(zip(ids,sc[ids],direct,derived,delta,mr[ids],one.astype(int),two.astype(int)))
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
