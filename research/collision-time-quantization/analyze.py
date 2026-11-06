#!/usr/bin/env python3
"""Catalog-internal collision-time concentration diagnostic; no physical inference."""
import csv, hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path
import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
CAT_HASH = 'd9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
CAT = Path(sys.argv[1])
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if sha(CAT) != CAT_HASH: raise SystemExit('Unexpected merger catalog digest')
prior = HERE.parent/'pericenter-time-distance-association'/'comparison.csv'
with h5py.File(CAT) as f:
    times = f['T_coll'][:]; snaps = f['Snap_coll'][:]; halos = f['HaloID'][:]
if not np.all(np.isfinite(times)): raise SystemExit('Non-finite collision times require review')
with prior.open(newline='') as f: rows=list(csv.DictReader(f))
if len({int(r['row']) for r in rows}) != len(rows): raise SystemExit('Duplicate input rows')
by_snap=defaultdict(Counter)
for s,t in zip(snaps,times): by_snap[int(s)][float(t)] += 1
# Deterministic tie break; the modal time is determined from all 2083 catalog events.
modes={s: sorted(c.items(),key=lambda x:(-x[1],x[0]))[0] for s,c in by_snap.items()}
results=[]
for r in rows:
    i=int(r['row']); s=int(snaps[i]); t=float(times[i])
    if s != int(r['snap_coll']) or t != float(r['tcoll_gyr']): raise SystemExit('Input tables disagree')
    results.append({'row':i,'snap_coll':s,'recorded_halo_label':int(halos[i]),'nearby_proper_match':int(r['nearby_proper_match']),'tcoll_gyr':t,'modal_time_same_snap_gyr':modes[s][0],'is_modal_time_same_snap':int(t == modes[s][0])})
with (HERE/'event_diagnostic.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
groups={}
for m in (1,0):
    v=[r for r in results if r['nearby_proper_match']==m]
    groups[str(m)]={'events':len(v),'modal_time_events':sum(r['is_modal_time_same_snap'] for r in v),'distinct_recorded_halo_labels':len({r['recorded_halo_label'] for r in v})}
counts=Counter(float(t) for t in times)
summary={'catalog_sha256':CAT_HASH,'prior_csv_sha256':sha(prior),'all_rows':len(times),'unique_time_values':len(counts),'rows_with_duplicate_time':sum(n for n in counts.values() if n>1),'selected_groups':groups,'caution':'Exploratory association, pooled events not independent clusters; modal time is not proven to be snapshot age or error.'}
(HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7,4.3))
labels=['Nearby distance\nmatch','No nearby\ndistance match']
values=[groups[str(i)]['modal_time_events']/groups[str(i)]['events'] for i in (1,0)]
ax.bar(labels,values,color=['#356b87','#d68956']);ax.set_ylim(0,1);ax.set_ylabel('Share with modal collision time within snapshot')
for i,(v,g) in enumerate(zip(values,[groups['1'],groups['0']])): ax.text(i,v+0.025,f"{g['modal_time_events']}/{g['events']} ({v:.1%})",ha='center')
ax.set_title('Exact collision-time repeats in selected events')
fig.text(.5,.01,'Same catalog; exploratory descriptive counts, not independent clusters',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.04,1,1));fig.savefig(HERE/'collision-time-modes.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
