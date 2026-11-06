import csv,hashlib,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;src=p.parent/'pericenter-time-distance-association/comparison.csv';rows=list(csv.DictReader(src.open()));assert len(rows)==1977 and len({int(r['row']) for r in rows})==1977
bins=[(30,49),(50,69),(70,84),(85,98)];out=[]
for lo,hi in bins:
 r=[x for x in rows if lo<=int(x['snap_coll'])<=hi];item={'snap_min':lo,'snap_max':hi,'events':len(r)}
 for name,v in [('distance_match',1),('distance_nonmatch',0)]:
  group=[x for x in r if int(x['nearby_proper_match'])==v];n=len(group);k=sum(float(x['nearest_three_abs_delta_gyr'])<.01 for x in group);item[name]={'n':n,'within_0_01_gyr':k,'fraction':k/n if n else None}
 out.append(item)
assert sum(x['events'] for x in out)==len(rows)
sumry={'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'threshold_gyr':.01,'bins':out,'warning':'Exploratory within-catalog stratification; no independent clusters or uncertainty-corrected causal inference.'};(p/'summary.json').write_text(json.dumps(sumry,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(9,5),layout='constrained');x=np.arange(len(out));width=.35
for j,(name,col) in enumerate([('distance_match','#39798c'),('distance_nonmatch','#d08b52')]):
 vals=[r[name]['fraction'] for r in out];bars=ax.bar(x+(j-.5)*width,vals,width,label=name.replace('_',' '),color=col)
 for bar,item in zip(bars,out):
  group=item[name];ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+.018,f"{group['within_0_01_gyr']}/{group['n']}",ha='center',fontsize=8)
ax.set_xticks(x,[f"{r['snap_min']}–{r['snap_max']}" for r in out]);ax.set(ylim=(0,1.15),xlabel='Collision snapshot range',ylabel='Fraction near a snapshot time',title='Timing association by collision snapshot');ax.legend();ax.grid(axis='y',alpha=.2);fig.savefig(p/'timing-association.png',dpi=160);plt.close(fig);print(json.dumps(sumry,indent=2))
