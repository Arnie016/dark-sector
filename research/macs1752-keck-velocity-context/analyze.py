#!/usr/bin/env python3
"""Compare one spectrum to published subcluster velocity scales, not membership."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

here=Path(__file__).resolve().parent
spectrum=json.loads((here.parent/'macs1752-keck-crossmatch'/'summary.json').read_text())
z=spectrum['z_spec']; c=299792.458
components=[{'name':'Subcluster 1','z':0.36482,'z_uncertainty':0.00046,'dispersion_km_s':1006,'dispersion_uncertainty_km_s':68,'n':93}, {'name':'Subcluster 2','z':0.36430,'z_uncertainty':0.00055,'dispersion_km_s':1038,'dispersion_uncertainty_km_s':77,'n':69}]
fig,ax=plt.subplots(figsize=(8,4.7)); x=np.linspace(-4000,4000,1000)
for item,color in zip(components,['#148b6a','#ce752c']):
    item['relative_velocity_km_s']=c*(z-item['z'])/(1+item['z'])
    item['velocity_in_dispersion_units']=item['relative_velocity_km_s']/item['dispersion_km_s']
    ax.plot(x,np.exp(-0.5*(x/item['dispersion_km_s'])**2),color=color,label=f"{item['name']}: σ = {item['dispersion_km_s']} km/s")
    ax.axvline(item['relative_velocity_km_s'],color=color,linestyle='--',linewidth=1.6,label=f"Galaxy relative to {item['name']}: {item['relative_velocity_km_s']:.0f} km/s")
ax.set(xlabel='Velocity relative to each subcluster mean (km/s)',ylabel='Illustrative Gaussian, normalized to peak',title='MACS J1752: galaxy velocity in published context')
ax.grid(alpha=.2);ax.legend(fontsize=8,loc='upper left');fig.tight_layout();fig.savefig(here/'velocity_context.png',dpi=160);plt.close(fig)
result={'source':'Golovich et al. 2019, Fig. 29, arXiv:1806.10619','formula':'c * (z_galaxy - z_component) / (1 + z_component)','galaxy_z':z,'galaxy_z_uncertainty':spectrum['z_spec_uncertainty'],'components':components,'c_km_s':c,'caveat':'Descriptive velocity offsets only; published fit may use this spectrum. No membership probability, independent test, or radio association inferred.'}
(here/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
