import csv,hashlib,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;src=p.parent/'merger-collision-ensemble/snapshot_redshifts.json';z={int(x['number']):float(x['redshift']) for x in json.loads(src.read_text())}
h=.6774;om=.3089;ol=.6911;sn=np.arange(68,73);scale=np.array([1/(1+z[int(s)]) for s in sn]);t=2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*scale**1.5)
conv=.9777922217; mass=1e14; mu=4.30091e-6*mass/conv**2
# Newtonian relative orbit in physical kpc and Gyr; state at known pericenter.
def ode(t,y):
 r=y[:2];return np.r_[y[2:],-mu*r/np.linalg.norm(r)**3]
rows=[];summary={'mass_total_msun':mass,'snapshots':sn.tolist(),'redshifts_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'phase_samples':101,'cases':{}}
fig,ax=plt.subplots(figsize=(8,5),layout='constrained')
for rp in (100.,300.,1000.):
 for vk in (3000.,5000.):
  v=vk/conv;assert v*v>mu/rp
  y0=np.array([rp,0,0,v]); span=.6
  neg=solve_ivp(ode,(0,-span),y0,method='DOP853',rtol=1e-11,atol=1e-11,dense_output=True);pos=solve_ivp(ode,(0,span),y0,method='DOP853',rtol=1e-11,atol=1e-11,dense_output=True);assert neg.success and pos.success
  def state(tt):return (neg if tt<0 else pos).sol(tt)
  test=np.column_stack([state(tt) for tt in np.linspace(-span,span,401)]); rr=np.linalg.norm(test[:2],axis=0);energy=np.sum(test[2:]**2,axis=0)/2-mu/rr;ang=test[0]*test[3]-test[1]*test[2];eerr=float(np.max(abs((energy-energy[200])/energy[200])));herr=float(np.max(abs((ang-ang[200])/ang[200])));assert eerr<1e-7 and herr<1e-7 and rr.min()>=rp*(1-1e-9)
  case=[]
  for phase in np.linspace(.001,.999,101):
   tc=t[1]+phase*(t[2]-t[1]);rel=t-tc;assert max(abs(rel))<span
   dist=np.array([np.linalg.norm(state(q)[:2]) for q in rel]);coef=np.polyfit(t-t[2],dist,2);vertex=t[2]-coef[1]/(2*coef[0]);minimum=np.polyval(coef,vertex-t[2]);ok=bool(coef[0]>0 and t[0]<=vertex<=t[-1] and minimum>=0)
   x={'r_peri_kpc':rp,'v_peri_km_s':vk,'phase':float(phase),'accepted':int(ok),'distance_bias_kpc':float(minimum-rp),'time_error_myr':float((vertex-tc)*1000)};case.append(x);rows.append(x)
  good=[q for q in case if q['accepted']];summary['cases'][f'{int(rp)}kpc_{int(vk)}kms']={'accepted':len(good),'median_distance_bias_kpc':float(np.median([q['distance_bias_kpc'] for q in good])) if good else None,'median_abs_time_error_myr':float(np.median([abs(q['time_error_myr']) for q in good])) if good else None,'max_relative_energy_drift':eerr,'max_relative_angular_momentum_drift':herr}
  if vk==3000:ax.plot([q['phase'] for q in case],[q['distance_bias_kpc'] for q in case],label=f'pericenter {int(rp)} kpc')
ax.set(xlabel='True passage phase between snapshots 69 and 70',ylabel='Fitted minus true pericenter (kpc)',title='Newtonian two-body control · 100 trillion solar masses');ax.legend();ax.grid(alpha=.2);fig.savefig(p/'two-body-bias.png',dpi=160);plt.close(fig)
with (p/'cases.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
