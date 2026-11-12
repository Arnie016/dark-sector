from pathlib import Path
import csv, json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
raw=(p/'snapshot-redshifts.csv').read_bytes()
rows=list(csv.DictReader(raw.decode().splitlines()))
snap=np.array([int(r['snapshot']) for r in rows]); z=np.array([float(r['redshift']) for r in rows])
assert np.array_equal(snap,np.arange(30,100)) and np.all(np.diff(z)<0)
h=.6774; om=.3089; ol=.6911
a=1/(1+z)
t=2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*a**1.5)
assert np.all(np.diff(t)>0)
t0=t[snap==70][0]
# Synthetic comoving displacement with a known derivative. Its velocity is scaled by a/h.
def evaluate(times,scale,sigma):
 x=(1000*h/.9777922217)*sigma*np.sin((times-t0)/sigma)
 exact=1000*scale*np.cos((times-t0)/sigma)
 estimated=np.gradient(x,times,edge_order=2)*scale/h*.9777922217
 return np.abs(estimated-exact)
result={'input_sha256':hashlib.sha256(raw).hexdigest(),'n_snapshots':len(t),'median_spacing_gyr':float(np.median(np.diff(t))),'models':{}}
fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
for sigma in (.1,.3,1.):
 err=evaluate(t,a,sigma)
 # Insert actual time midpoints; interpolate a only for this synthetic finer grid.
 fine=np.sort(np.r_[t,(t[:-1]+t[1:])/2]); af=np.interp(fine,t,a); ef=evaluate(fine,af,sigma)[::2]
 result['models'][str(sigma)]={'median_error_km_s':float(np.median(err[1:-1])),'p90_error_km_s':float(np.quantile(err[1:-1],.9)),'median_error_midpoint_grid_km_s':float(np.median(ef[1:-1])),'snap70_error_km_s':float(err[snap==70][0])}
 ax.plot(snap[1:-1],err[1:-1],label=f'timescale {sigma:g} Gyr')
ax.set(xlabel='TNG snapshot',ylabel='Absolute velocity error (km/s)',title='Synthetic trajectory: finite-difference error at TNG cadence');ax.legend();ax.grid(alpha=.2)
fig.savefig(p/'cadence-error.png',dpi=160);plt.close(fig)
(p/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
