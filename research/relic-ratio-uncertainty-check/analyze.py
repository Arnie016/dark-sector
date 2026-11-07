import csv,hashlib,json,math
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parent;src=p.parent/'relic-gold-sample-data-check/distances.csv';rows=list(csv.DictReader(src.open()));assert len(rows)==11 and len({r['name'] for r in rows})==11
rng=np.random.default_rng(20261107);N=200000;results=[]
for r in rows:
 h=float(r['halo_mpc']);s=float(r['shock_mpc']);dh=float(r['halo_sigma_mpc']);ds=float(r['shock_sigma_mpc']);assert min(h,s,dh,ds)>0
 u=rng.standard_normal(N);v=rng.standard_normal(N)
 for rho in (-.5,0.,.5):
  hh=h+dh*u;ss=s+ds*(rho*u+math.sqrt(1-rho*rho)*v);ok=(hh>0)&(ss>0);q=np.quantile(hh[ok]/ss[ok],[.16,.5,.84]);linear=(h/s)*math.sqrt((dh/h)**2+(ds/s)**2-2*rho*(dh/h)*(ds/s))
  results.append({'name':r['name'],'rho_assumed':rho,'draws':N,'discarded_nonpositive_fraction':float(1-ok.mean()),'q16':float(q[0]),'median':float(q[1]),'q84':float(q[2]),'linear_sigma':linear})
with (p/'results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]),lineterminator='\n');w.writeheader();w.writerows(results)
z=next(r for r in results if r['name']=='ZWCL1447.2+2619' and r['rho_assumed']==0.);out={'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'seed':20261107,'draws_per_scenario':N,'systems':11,'correlation_values':[-.5,0,.5],'low_snr_example':z,'warning':'Toy bivariate normal draws centered on published estimates, conditional on positive distances, are not posterior samples; correlations are hypothetical.'}
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
