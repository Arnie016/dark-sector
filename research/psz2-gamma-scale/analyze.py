#!/usr/bin/env python3
"""Compare published angular scales, without fitting photon data."""
from pathlib import Path
import json
import numpy as np
import astropy.units as u
from astropy.cosmology import FlatLambdaCDM
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
c=FlatLambdaCDM(H0=70*u.km/u.s/u.Mpc, Om0=.3, Tcmb0=2.725*u.K)
z=.234
DA=c.angular_diameter_distance(z).to_value(u.Mpc)
sigma=.4
r68=sigma*np.sqrt(-2*np.log(1-.68))
def angle(mpc): return np.degrees(mpc/DA)
result={'cosmology': 'FlatLambdaCDM: H0=70 km/s/Mpc, Om0=0.3, Tcmb0=2.725 K; illustrative', 'redshift':z, 'angular_diameter_distance_Mpc':DA, 'gamma_sigma_deg':sigma, 'gamma_68_containment_deg':r68, 'gamma_68_projected_Mpc_at_cluster_redshift': DA*np.radians(r68), 'lensing_R200c_Mpc':1.43, 'lensing_R200c_angle_deg':angle(1.43), 'radio_relic_separation_Mpc_approx':2.7, 'radio_relic_separation_deg_approx':angle(2.7), 'qualification':'Gaussian containment radius, lensing radius and relic separation are different quantities; gamma-ray distance and association unverified.'}
assert abs(r68-.604)<.002
(p/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7.5,3.6))
labels=['Lensing R200c\n(radius)', 'Radio relic separation\n(full separation)', 'Gamma Gaussian 68%\n(containment radius)']
values=[angle(1.43),angle(2.7),r68]
ax.barh(labels,values,color=['#496e9c','#a55a3d','#8769a4']); ax.invert_yaxis()
ax.set(xlabel='Angle on sky (degrees)',title='PSZ2 G181: different published angular scales')
for y,v in enumerate(values): ax.text(v+.01,y,f'{v:.3f}°',va='center')
ax.set_xlim(0,.73); ax.grid(axis='x',alpha=.25); fig.tight_layout(); fig.savefig(p/'angular-scales.png',dpi=160)
print(json.dumps(result,indent=2))
