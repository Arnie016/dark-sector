#!/usr/bin/env python3
"""Illustrative sensitivity of the published Lee+ clock, not a cluster age fit."""
import csv, json, math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
# Ahn+ cosmology, weak-lensing combined spherical-overdensity mass in solar masses.
G=4.30091e-9 # Mpc (km/s)^2 / solar mass
h0=70.; om=0.3; z=0.234; mass=2.90e14
hz=h0*math.sqrt(om*(1+z)**3+1-om)
rho=3*hz**2/(8*math.pi*G)
r_wl=(3*mass/(4*math.pi*500*rho))**(1/3)
d=2.694 # projected LOFAR relic coordinate separation, Mpc
estimates=[('X-ray',0.87),('Weak lensing, derived',r_wl),('Planck SZ',1.06)]
rows=[{'radius_source':label,'radius_mpc':r,'projected_separation_mpc':d,'ratio_projected':d/r,'lee_line_illustrative_gyr':0.52*d/r-0.24} for label,r in estimates]
with (p/'sensitivity.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'radius_difference_clock_shift_gyr':rows[0]['lee_line_illustrative_gyr']-rows[2]['lee_line_illustrative_gyr'],'weak_lensing_derived_radius_mpc':r_wl,'warning':'Illustrative substitution of projected LOFAR distance for simulation fit; no corrected time, posterior, significance, or SIDM inference.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
x=[0.78+i*(0.42/400) for i in range(401)];y=[0.52*d/t-0.24 for t in x]
fig,ax=plt.subplots(figsize=(7,4.5));ax.plot(x,y,color='#376f91',label='Lee line using fixed projected distance');ax.axhspan(.4,1.,color='#b0a1a0',alpha=.16,label='Jee fiducial phase prior')
for row in rows: ax.scatter(row['radius_mpc'],row['lee_line_illustrative_gyr'],s=55,label=row['radius_source'])
ax.set(xlabel='Illustrative R500c (Mpc)',ylabel='Formula output (Gyr)',title='Sensitivity to radius: PSZ2 G181.06+48.47');ax.legend(fontsize=8);fig.text(.5,.01,'Illustration only: projected bright-pixel distance differs from 3D relic centers.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'radius-sensitivity.png',dpi=160)
print(json.dumps({'rows':rows,**summary},indent=2))
