#!/usr/bin/env python3
"""Evaluate published Table 1 / Eq 3 fits; not a fit to simulation data."""
import csv,hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.special import erf
from scipy.optimize import minimize_scalar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;source=p/'parameters.csv'
with source.open(newline='') as f: rows=list(csv.DictReader(f))
if len(rows)!=4 or len({(r['sample'],r['aperture']) for r in rows})!=4:raise ValueError('Unexpected parameter table')
def curve(t,r):
 a,s0,s1,sigma,t0,gamma=[float(r[k]) for k in ('a0','s0','s1','sigma','t0','gamma')]
 x=(t-t0)/sigma
 return (a/(math.sqrt(2*math.pi)*sigma))*np.exp(-.5*x*x)*(1+erf(gamma*x/math.sqrt(2)))+s0*t+s1
# Small bounded phase range, not an inference about validity outside the paper.
time=np.linspace(0,1.5,301);summary={'parameters_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'interval_gyr':[0,1.5],'curves':{}}
fig,axs=plt.subplots(1,2,figsize=(10,4),sharex=True)
for r in rows:
 y=curve(time,r);result=minimize_scalar(lambda t:-float(curve(t,r)),bounds=(0,1.5),method='bounded',options={'xatol':1e-12})
 if not result.success or min(y)<=0:raise ValueError('Optimization or positivity failed in selected interval')
 label=r['sample']+'/'+r['aperture'];summary['curves'][label]={'peak_gyr':float(result.x),'peak_power_1e20_w_hz':float(-result.fun),'at_0_5_gyr':float(curve(.5,r)),'at_1_0_gyr':float(curve(1.,r)),'at_1_5_gyr':float(curve(1.5,r))}
 ax=axs[0 if r['sample']=='groups' else 1];ax.plot(time,y,label=r['aperture'],linestyle='--' if r['aperture']=='2R200' else '-')
for ax,title in zip(axs,['Groups','Clusters']):ax.set(title=title,xlabel='Time after core passage (Gyr)',ylabel='Model power (10²⁰ W/Hz)');ax.legend();ax.grid(alpha=.2)
fig.suptitle('Published The Three Hundred median-fit curves');fig.text(.5,.01,'Parameterized simulation medians; not measurements of individual radio relics.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,.93));fig.savefig(p/'published-radio-curves.png',dpi=160);plt.close(fig)
summary['limitations']='Published fitted medians, not raw light curves or new simulation; correlated parameters and selection unmodeled; total shock emission is not individual relic luminosity.'
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
