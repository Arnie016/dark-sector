import csv,hashlib,json,collections
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
c=p.parent/'merger-collision-ensemble/collision-comparison.csv';g=p.parent/'trajectory-grouping-audit/grouping.csv'
cr=list(csv.DictReader(c.open()));gr=list(csv.DictReader(g.open()));lookup={int(r['event_row']):r for r in gr}
assert len(lookup)==len(gr) and len({int(r['row']) for r in cr})==len(cr)
subset=[(r,lookup[int(r['row'])]) for r in cr if int(r['row']) in lookup]
assert all(int(r['halo_id'])==int(s['recorded_halo_id']) for r,s in subset)
bylabel=collections.defaultdict(list);byvector=collections.defaultdict(list)
for r,s in subset:
 d=float(r['discrepancy_km_s']);assert np.isfinite(d);bylabel[int(r['halo_id'])].append(d);byvector[int(s['vector_group'])].append(d)
events=np.array([float(r['discrepancy_km_s']) for r,s in subset]);lab=np.array([np.median(v) for v in bylabel.values()]);vec=np.array([np.median(v) for v in byvector.values()]);all_events=np.array([float(r['discrepancy_km_s']) for r in cr]);excluded=np.array([float(r['discrepancy_km_s']) for r in cr if int(r['row']) not in lookup]);assert len(excluded)+len(subset)==len(cr)
out={'collision_csv_sha256':hashlib.sha256(c.read_bytes()).hexdigest(),'grouping_csv_sha256':hashlib.sha256(g.read_bytes()).hexdigest(),'all_collision_rows':len(cr),'full_collision_sample_median_km_s':float(np.median(all_events)),'matched_subset_rows':len(subset),'missing_from_fingerprint_subset':len(cr)-len(subset),'excluded_subset_event_median_km_s':float(np.median(excluded)),'matched_subset_event_median_km_s':float(np.median(events)),'recorded_labels':len(lab),'median_of_label_medians_km_s':float(np.median(lab)),'fingerprint_groups':len(vec),'median_of_fingerprint_group_medians_km_s':float(np.median(vec)),'warning':'Group medians use distinct estimands and unverified grouping keys; no causal or independent-cluster interpretation.'}
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained'); names=['Event rows','Halo-label medians','Fingerprint medians'];vals=[np.median(events),np.median(lab),np.median(vec)];ax.barh(names,vals,color=['#39798c','#bd8255','#7a6696']);ax.set(xlabel='Median estimator discrepancy (km/s)',title='Different weighting choices on the same matched subset');ax.grid(axis='x',alpha=.2);fig.savefig(p/'weighting-sensitivity.png',dpi=160);plt.close(fig)
print(json.dumps(out,indent=2))
