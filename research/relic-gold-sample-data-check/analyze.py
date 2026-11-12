import csv,hashlib,json,math,statistics
from pathlib import Path
p=Path(__file__).resolve().parent;src=p/'distances.csv';raw=list(csv.DictReader(src.open()));assert len(raw)==11 and len({r['name'] for r in raw})==11
out=[]
for r in raw:
 shock=float(r['shock_mpc']);halo=float(r['halo_mpc']);shs=float(r['shock_sigma_mpc']);hs=float(r['halo_sigma_mpc']);assert all(math.isfinite(x) and x>0 for x in (shock,halo,shs,hs))
 ratio=halo/shock;err=ratio*math.sqrt((hs/halo)**2+(shs/shock)**2)
 out.append({'name':r['name'],'redshift':float(r['redshift']),'halo_to_shock_ratio':ratio,'ratio_sigma_linear_independent':err,'halo_fractional_sigma':hs/halo,'shock_fractional_sigma':shs/shock})
with (p/'ratios.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]),lineterminator='\n');w.writeheader();w.writerows(out)
s={'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'observed_systems':len(out),'median_ratio':statistics.median(x['halo_to_shock_ratio'] for x in out),'min_ratio':min(x['halo_to_shock_ratio'] for x in out),'max_ratio':max(x['halo_to_shock_ratio'] for x in out),'median_halo_fractional_sigma':statistics.median(x['halo_fractional_sigma'] for x in out),'median_shock_fractional_sigma':statistics.median(x['shock_fractional_sigma'] for x in out),'warning':'Derived descriptive ratios only. Independent Gaussian first-order propagation is assumed and may fail for low S/N; no posterior, covariance or selection correction.'}
(p/'summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))
