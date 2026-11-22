#!/usr/bin/env python3
"""Plot the three targeted fields' identical-radius descriptive comparisons."""
import csv,hashlib,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;old=p.parent/'two-cluster-physical-beam'/'variants.csv';new=p/'variants.csv';rows=[]
for path in (old,new):
 with path.open(newline='') as f:rows.extend(csv.DictReader(f))
fig,ax=plt.subplots(figsize=(8,4.6))
for name,color,marker in [('MACS J1752','#aa4a32','o'),('PSZ2 G181','#26788f','s'),('PSZ2 G099','#73569a','^')]:
 for j,radius in enumerate((300,450,600)):
  group=[r for r in rows if r['cluster']==name and int(r['radius_kpc'])==radius and r['image']=='T50' and r['relic']=='N']
  if len(group)!=3:raise ValueError('Missing configuration')
  group.sort(key=lambda r:float(r['threshold_mjy_per_beam']))
  ax.plot([float(r['threshold_mjy_per_beam']) for r in group],[float(r['pair_difference_kpc']) for r in group],color=color,marker=marker,ls=['-',':','--'][j],label=f'{name}, {radius} kpc')
ax.axhline(0,color='gray',lw=.8);ax.set(xlabel='Brightness threshold (mJy / target beam)',ylabel='T50 minus T50SUB pair separation (kpc)',title='Three targeted cluster fields: position-rule sensitivity');ax.legend(ncol=3,fontsize=7);fig.text(.5,.01,'Exploratory regions and related images; not physical clock biases.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'three-cluster-comparison.png',dpi=160);plt.close(fig)
print(json.dumps({'previous_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'new_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'configurations':27},indent=2))
