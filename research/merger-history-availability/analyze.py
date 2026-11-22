import csv,collections,hashlib,json
from pathlib import Path
import numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
c=p.parent/'merger-collision-ensemble/collision-comparison.csv';g=p.parent/'trajectory-grouping-audit/grouping.csv'
rows=list(csv.DictReader(c.open()));gr=list(csv.DictReader(g.open()));ids={int(r['event_row']) for r in gr}
assert len(ids)==len(gr) and len({int(r['row']) for r in rows})==len(rows)
bins=[(30,49),(50,69),(70,84),(85,98)];out=[]
for lo,hi in bins:
 rr=[r for r in rows if lo<=int(r['snap_coll'])<=hi]; yes=[r for r in rr if int(r['row']) in ids];no=[r for r in rr if int(r['row']) not in ids]
 med=lambda x:float(np.median([float(r['discrepancy_km_s']) for r in x])) if x else None
 out.append({'snap_lo':lo,'snap_hi':hi,'n':len(rr),'available':len(yes),'unavailable':len(no),'available_fraction':len(yes)/len(rr) if rr else None,'available_median_discrepancy':med(yes),'unavailable_median_discrepancy':med(no)})
assert sum(x['n'] for x in out)==len(rows)
summary={'collision_input_sha256':hashlib.sha256(c.read_bytes()).hexdigest(),'grouping_input_sha256':hashlib.sha256(g.read_bytes()).hexdigest(),'groups':out,'warning':'Exploratory, selected catalog events; availability is not proven causal and halo IDs not independently mapped.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(2,1,figsize=(8,7),layout='constrained');x=np.arange(len(out));labels=[f"{r['snap_lo']}–{r['snap_hi']}\nn={r['n']} ({r['unavailable']} unavailable)" for r in out]
ax[0].bar(x,[r['available_fraction'] for r in out],color='#467e8d');ax[0].set(ylabel='Fraction with usable snapshot-99 fingerprint',ylim=(0,1))
ax[1].plot(x,[r['available_median_discrepancy'] for r in out],marker='o',label='Fingerprint available');ax[1].plot(x,[r['unavailable_median_discrepancy'] for r in out],marker='o',label='Unavailable');ax[1].set(ylabel='Median estimator difference (km/s)',xlabel='Collision snapshot range');ax[1].legend()
for a in ax:a.set_xticks(x,labels);a.grid(axis='y',alpha=.2)
fig.savefig(p/'availability-by-collision.png',dpi=160);plt.close(fig);print(json.dumps(summary,indent=2))
