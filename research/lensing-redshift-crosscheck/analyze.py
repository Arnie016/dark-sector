#!/usr/bin/env python3
"""Explicit cross-paper redshift join and fixed-angle sensitivity; no mass inference."""
import csv,hashlib,json
from pathlib import Path
import numpy as np
from astropy.cosmology import FlatLambdaCDM
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;gold=p.parent/'relic-gold-sample-data-check'/'distances.csv';finner=p/'finner_table1_matches.csv'
def read(path):
 with path.open(newline='') as f:return list(csv.DictReader(f))
a,b=read(gold),read(finner);byname={r['name']:r for r in a}
if len(byname)!=len(a) or len({r['gold_sample_name'] for r in b})!=8:raise ValueError('Duplicate names or incorrect crosswalk size')
if set(r['gold_sample_name'] for r in b)-set(byname):raise ValueError('Missing gold sample names')
c=FlatLambdaCDM(H0=70,Om0=.3);result=[]
for r in b:
 j=byname[r['gold_sample_name']];zj=float(j['redshift']);zf=float(r['finner_table1_z']);factor=float(c.angular_diameter_distance(zf).value/c.angular_diameter_distance(zj).value)
 result.append({'name':r['gold_sample_name'],'finner_short_name':r['finner_short_name'],'jee_z':zj,'finner_table1_z':zf,'delta_z_finner_minus_jee':zf-zj,'fixed_angle_distance_change_percent':100*(factor-1)})
with (p/'crosscheck.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
# Separately flag the published section-heading disagreement; no decision on truth.
alt_factor=float(c.angular_diameter_distance(.334).value/c.angular_diameter_distance(.304).value)
summary={'gold_sha256':hashlib.sha256(gold.read_bytes()).hexdigest(),'crosswalk_sha256':hashlib.sha256(finner.read_bytes()).hexdigest(),'matched':len(result),'different_rounded_redshift_count':sum(r['jee_z']!=r['finner_table1_z'] for r in result),'cosmology':'flat LCDM H0=70 km/s/Mpc Om0=0.3','zwcl1856_heading_z':.334,'zwcl1856_table_z':.304,'illustrative_fixed_angle_heading_vs_table_percent':100*(alt_factor-1),'caveat':'Coordinates and original angular measurements not checked; scalar fixed-angle rescaling is not a remeasurement, lensing re-fit, correction to published results or uncertainty.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8,4.5)); names=[r['finner_short_name'] for r in result];v=[r['fixed_angle_distance_change_percent'] for r in result];ax.barh(names,v,color=['#c36141' if x else '#8092a1' for x in v]);ax.axvline(0,color='black',linewidth=.7);ax.invert_yaxis();ax.set(xlabel='Fixed-angle distance change: Finner table vs Jee (%)',title='Redshift convention sensitivity in overlapping systems');fig.text(.5,.01,'Illustrative fixed-angle conversion; not a measured correction or uncertainty.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'redshift-sensitivity.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
