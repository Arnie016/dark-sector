import csv,hashlib,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
src=p.parent/'timing-crosscheck/comparison.csv';rows=list(csv.DictReader(src.open()))
a=np.array([float(r['elapsed_tcoll_gyr']) for r in rows]);b=np.array([float(r['elapsed_tsc_full_gyr']) for r in rows]);mass=np.array([float(r['mass_ratio']) for r in rows]);eligible=mass>=.1
limits=np.arange(.2,1.401,.05);a_counts=[];b_counts=[];dis=[]
for limit in limits:
 aa=eligible&(a>=0)&(a<=limit);bb=eligible&(b>=0)&(b<=limit)
 a_counts.append(int(aa.sum()));b_counts.append(int(bb.sum()));dis.append(int(np.count_nonzero(aa^bb)))
with (p/'sensitivity.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['cutoff_gyr','count_tcoll','count_tsc_full','symmetric_difference_rows']);w.writerows(zip(np.round(limits,2),a_counts,b_counts,dis))
out={'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'eligible_rows_mass_ratio_ge_0_1':int(eligible.sum()),'selected_points':{str(round(float(limits[i]),2)):{'tcoll':a_counts[i],'tsc_full':b_counts[i],'different_rows':dis[i]} for i in (6,16,24)},'warning':'Descriptive threshold sensitivity, not uncertainty, observed rate, or independent verification.'}
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
fig,ax=plt.subplots(2,1,figsize=(8.5,6),sharex=True,layout='constrained');ax[0].plot(limits,a_counts,label='From T_coll');ax[0].plot(limits,b_counts,label='From TSC_full',ls='--');ax[0].set_ylabel('Selected event rows');ax[0].legend();ax[1].plot(limits,dis,color='#a65d3f');ax[1].set(xlabel='Elapsed-time cutoff [Gyr]',ylabel='Rows selected by only one');
for a0 in ax:a0.axvline(1,color='grey',ls=':');a0.grid(alpha=.2)
fig.suptitle('Selection sensitivity to two merger-clock estimates');fig.savefig(p/'selection-sensitivity.png',dpi=160);plt.close(fig);print(json.dumps(out,indent=2))
