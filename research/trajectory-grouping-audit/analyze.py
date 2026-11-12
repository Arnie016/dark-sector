import argparse,collections,csv,hashlib,json
from pathlib import Path
import h5py,numpy as np
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);a=ap.parse_args()
assert hashlib.sha256(a.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
groups=collections.defaultdict(list);labels=collections.defaultdict(set);invalid=missing=0
with h5py.File(a.catalog) as f:
 for i in range(len(f['HaloID'])):
  ix=np.flatnonzero(f['Mhistory_snap'][i]==99)
  if len(ix)!=1:missing+=1;continue
  k=ix[0];pos=f['Mhistory_orbit'][i,k,:3];vel=f['Mhistory_vel'][i,k,:3]
  if not np.isfinite(pos).all() or not np.isfinite(vel).all() or (pos<0).any() or (pos>=680000).any():invalid+=1;continue
  key=tuple(map(float,np.r_[pos,vel])); label=int(f['HaloID'][i]);groups[key].append((i,label));labels[label].add(key)
assert sum(map(len,groups.values()))+missing+invalid==2083
pairs=[]
for label,vs in labels.items():
 vs=sorted(vs)
 for v in vs[1:]:
  x=np.array(v)-np.array(vs[0]);pairs.append((float(np.max(abs(x[:3]))),float(np.max(abs(x[3:])))))
out={'catalog_rows':2083,'missing_or_duplicate_99_rows':missing,'invalid_phase_space_rows':invalid,'valid_rows':sum(map(len,groups.values())),'unique_exact_phase_space_vectors':len(groups),'unique_recorded_labels':len(labels),'vectors_associated_with_multiple_labels':sum(len({q[1] for q in v})>1 for v in groups.values()),'labels_associated_with_multiple_vectors':sum(len(v)>1 for v in labels.values()),'largest_vector_group_event_count':max(map(len,groups.values())),'within_label_comparisons_to_sorted_first':len(pairs),'within_label_pairs_below_both_1_ckpc_h_and_0_002_km_s':sum(x<1 and y<.002 for x,y in pairs),'median_within_label_max_component_pos_difference_ckpc_h':float(np.median([x for x,y in pairs])),'median_within_label_max_component_vel_difference_km_s':float(np.median([y for x,y in pairs])),'warning':'Exact vector fingerprints at one epoch, not independently verified subhalo, group, or tree identities.'}
with (p/'grouping.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['vector_group','event_row','recorded_halo_id','group_event_count'])
 for n,(key,vals) in enumerate(sorted(groups.items())):
  for row,label in vals:w.writerow([n,row,label,len(vals)])
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
