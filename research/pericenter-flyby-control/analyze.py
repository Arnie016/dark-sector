import csv,json,hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
src=p.parent/'merger-collision-ensemble/snapshot_redshifts.json'; z={int(x['number']):float(x['redshift']) for x in json.loads(src.read_text())}
h=.6774;om=.3089;ol=.6911;sn=np.arange(68,73);a=np.array([1/(1+z[int(s)]) for s in sn]);t=2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*a**1.5)
# Nearest snapshot after true passage is snapshot 70, as in the prototype window.
phase=np.linspace(.001,.999,101);rows=[]
for b in (50.,100.,300.,1000.):
 for v in (1500.,3000.):
  for q in phase:
   true_t=t[1]+q*(t[2]-t[1]);r=np.sqrt(b*b+(v/.9777922217*(t-true_t))**2)
   coef=np.polyfit(t-t[2],r,2); vertex=t[2]-coef[1]/(2*coef[0]); fitted=np.polyval(coef,vertex-t[2]);accepted=bool(coef[0]>0 and t[0]<=vertex<=t[-1] and fitted>=0)
   rows.append({'impact_kpc':b,'speed_km_s':v,'phase':float(q),'fit_accepted':int(accepted),'time_error_myr':float((vertex-true_t)*1000),'distance_error_kpc':float(fitted-b)})
summary={'redshifts_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'snapshots':sn.tolist(),'previous_to_collision_spacing_gyr':float(t[2]-t[1]),'phase_samples':len(phase),'cases':{}}
fig,ax=plt.subplots(figsize=(8.5,5),layout='constrained')
for b in (50.,100.,300.,1000.):
 for v in (1500.,3000.):
  s=[r for r in rows if r['impact_kpc']==b and r['speed_km_s']==v];ok=[r for r in s if r['fit_accepted']];key=f'{int(b)}kpc_{int(v)}kms';summary['cases'][key]={'accepted':len(ok),'rejected':len(s)-len(ok),'median_distance_bias_kpc':float(np.median([r['distance_error_kpc'] for r in ok])) if ok else None,'median_abs_time_error_myr':float(np.median([abs(r['time_error_myr']) for r in ok])) if ok else None}
  if v==3000:ax.plot([r['phase'] for r in s],[r['distance_error_kpc'] for r in s],label=f'impact {int(b)} kpc')
ax.set(xlabel='True passage phase between snapshots 69 and 70',ylabel='Fitted minus true minimum distance (kpc)',title='Five-point fit: synthetic straight-line flybys at 3,000 km/s');ax.legend();ax.grid(alpha=.2);fig.savefig(p/'flyby-bias.png',dpi=160);plt.close(fig)
with (p/'cases.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
