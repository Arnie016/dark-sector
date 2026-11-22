#!/usr/bin/env python3
"""Compare two published time-since-collision summaries; not independent inference."""
import csv, hashlib, json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
raw=p/'sources.csv'
with raw.open(newline='') as f: rows=list(csv.DictReader(f))
if len(rows)!=4 or len({r['cluster'] for r in rows})!=4: raise ValueError('Expected four distinct systems')
for r in rows:
    x=float(r['normalized_separation_approx'])
    if not 1 <= x <= 3.5: raise ValueError('Outside Lee et al. stated fit range')
    r['jee_reported_upper_endpoint_gyr']=float(r['jee_phase_median_gyr'])+float(r['jee_phase_upper_gyr'])
    r['jee_reported_endpoint_above_stated_prior']=r['jee_reported_upper_endpoint_gyr'] > 1.0 + 1e-9
    r['lee_linear_central_gyr']=0.52*x-0.24
    r['lee_minus_jee_gyr']=r['lee_linear_central_gyr']-float(r['jee_phase_median_gyr'])
    r['illustrative_15pct_separation_increase_shift_gyr']=0.52*x*0.15
with (p/'comparison.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
fig,ax=plt.subplots(figsize=(8,4.6))
y=list(range(len(rows)))
ax.axvspan(0.4,1.0,color='lightgray',alpha=.35,label='Jee et al. phase prior')
ax.errorbar([float(r['jee_phase_median_gyr']) for r in rows],y,xerr=[[float(r['jee_phase_lower_gyr']) for r in rows],[float(r['jee_phase_upper_gyr']) for r in rows]],fmt='o',color='#a65130',capsize=3,label='Jee et al. posterior (reported 1σ)')
ax.scatter([r['lee_linear_central_gyr'] for r in rows],y,marker='D',color='#306c88',label='Lee et al. line, approximate input')
ax.set_yticks(y, [r['cluster'] for r in rows]);ax.invert_yaxis();ax.set_xlabel('Time since collision (Gyr)');ax.set_title('Published summaries for four overlapping systems')
ax.legend(loc='lower right',fontsize=8);fig.text(.5,.015,'Different models and shared data: not an independent validation or tension test.',ha='center',fontsize=8)
fig.text(.5,.055,'PSZ2: published rounded interval reaches 1.01 Gyr; prior stated to end at 1.00 Gyr.',ha='center',fontsize=7)
fig.tight_layout(rect=(0,.09,1,1));fig.savefig(p/'published-clock-comparison.png',dpi=160);plt.close(fig)
summary={'input_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'systems':len(rows),'reported_intervals_above_stated_prior':[{'cluster':r['cluster'],'reported_upper_endpoint_gyr':round(r['jee_reported_upper_endpoint_gyr'],2)} for r in rows if r['jee_reported_endpoint_above_stated_prior']],'lee_minus_jee_gyr':[round(r['lee_minus_jee_gyr'],3) for r in rows],'notes':'Approximate inputs; model comparison only, shared data and distinct uncertainties; no significance test.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
