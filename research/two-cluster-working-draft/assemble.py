#!/usr/bin/env python3
"""Recalculate the central descriptive results used by the working draft."""
import csv,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent;p=Path(__file__).resolve().parent
sources=['two-cluster-physical-beam/variants.csv','psz2-boundary-ablation/variants.csv','psz2-bright-fraction-sensitivity/variants.csv','psz2-selection-mechanism/contributions.csv','aperture-edge-audit/summary.json']
paths=[root/s for s in sources]; hashes={str(x.relative_to(root.parent)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
def read(name):
 with (root/name).open(newline='') as f:return list(csv.DictReader(f))
two=read(sources[0]);abl=read(sources[1]);frac=read(sources[2]);con=read(sources[3]);ap=json.loads(paths[4].read_text())
if (len(two),len(abl),len(frac),len(con),len(ap['apertures']))!=(72,52,96,48,4):raise ValueError('Unexpected source row count')
result={'source_sha256':hashes,'physical_beam_pair_difference_kpc':{}}
for cluster in ('MACS J1752','PSZ2 G181'):
 result['physical_beam_pair_difference_kpc'][cluster]={}
 for radius in (300,450,600):
  g=[float(r['pair_difference_kpc']) for r in two if r['cluster']==cluster and int(r['radius_kpc'])==radius and r['image']=='T50' and r['relic']=='N']
  if len(g)!=3:raise ValueError('Missing threshold configurations')
  result['physical_beam_pair_difference_kpc'][cluster][str(radius)]=[min(g),max(g)]
def one(rows,**filters):
 matches=[r for r in rows if all(r.get(k)==str(v) for k,v in filters.items())]
 if len(matches)!=1:raise ValueError(f'Expected one row: {filters}, got {len(matches)}')
 return matches[0]
result['psz2_exclusion_pair_difference_kpc']={}
for exclusion,rad in [('none',0),('peak',20),('peak',40),('peak',60)]:
 r=one(abl,exclusion=exclusion,radius_arcsec=rad,image='T50',relic='S');result['psz2_exclusion_pair_difference_kpc'][f'{exclusion}_{rad}']=float(r['pair_delta_kpc'])
result['psz2_selection']={}
for fraction in ('0.01','0.05','0.1'):
 r=one(frac,mask='none',reference='T50',fraction=fraction,image='T50',relic='S');a=one(con,reference='T50',fraction=fraction,image='T50',relic='S');b=one(con,reference='T50',fraction=fraction,image='T50SUB',relic='S')
 result['psz2_selection'][fraction]={'pair_difference_kpc':float(r['pair_delta_kpc']),'selected_count':int(a['selected_count']),'boundary_selected_count':int(a['boundary_selected_count']),'boundary_weight_fraction_T50':float(a['boundary_weight_fraction']),'boundary_weight_fraction_T50SUB':float(b['boundary_weight_fraction'])}
result['min_reference_image_margin_arcsec']=min(a['minimum_margin_arcsec'] for a in ap['apertures']);result['limitations']='Summary and source-hash reconciliation only; not an independent analysis, uncertainty estimate, simulation-clock reproduction or manuscript approval.'
(p/'evidence.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
