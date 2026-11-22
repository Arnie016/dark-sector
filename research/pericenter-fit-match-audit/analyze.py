import csv,hashlib,json,collections,statistics
from pathlib import Path
p=Path(__file__).resolve().parent
fa=p.parent/'five-point-pericenter/fits.csv'; fb=p.parent/'pericenter-sampled-minimum/comparison.csv'
fits=list(csv.DictReader(fa.open()));base=list(csv.DictReader(fb.open()));lookup={int(r['row']):r for r in fits};assert len(lookup)==len(fits) and len({int(r['row']) for r in base})==len(base)
rows=[]
for r in base:
 i=int(r['row'])
 if i not in lookup:continue
 f=lookup[i];target=float(r['catalog_value']);assert abs(target-float(f['catalog_dperi_ckpc_h']))<1e-9
 rows.append({'row':i,'matched_nearby_proper':int(r['matches_nearby_proper']),'fit_proper_minus_catalog_numeric':float(f['fit_sep_proper_kpc'])-target,'fit_comoving_minus_catalog_numeric':float(f['fit_sep_comoving_ckpc_h'])-target,'sampled_min_minus_catalog_numeric':float(r['sampled_min_proper'])-target})
def stats(rs,field):
 x=[abs(r[field]) for r in rs];return {'n':len(x),'median_absolute_numeric_difference':statistics.median(x),'within_0_01_count':sum(v<.01 for v in x)}
groups={}
for label,val in [('nearby_match',1),('nearby_nonmatch',0)]:
 subset=[r for r in rows if r['matched_nearby_proper']==val];groups[label]={k:stats(subset,k) for k in ('fit_proper_minus_catalog_numeric','fit_comoving_minus_catalog_numeric','sampled_min_minus_catalog_numeric')}
out={'five_point_csv_sha256':hashlib.sha256(fa.read_bytes()).hexdigest(),'sampled_minimum_csv_sha256':hashlib.sha256(fb.read_bytes()).hexdigest(),'joined_rows':len(rows),'groups':groups,'warning':'Comparisons assume incompatible possible distance units and a provisional fit; do not infer error, true units, or author method.'}
with (p/'comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
