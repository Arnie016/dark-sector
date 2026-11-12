import argparse,hashlib,json
from pathlib import Path
import numpy as np,h5py
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('catalog',type=Path);a=ap.parse_args()
assert hashlib.sha256(a.catalog.read_bytes()).hexdigest()=='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
src=p/'independent_subhalo_99_0.json';j=json.loads(src.read_text());assert j['id']==0 and j['snap']==99
pos=np.array([j['pos_'+c] for c in 'xyz']);vel=np.array([j['vel_'+c] for c in 'xyz']);matches=[];eligible=0
with h5py.File(a.catalog) as f:
 for i in range(len(f['HaloID'])):
  idx=np.flatnonzero(f['Mhistory_snap'][i]==99)
  if len(idx)!=1:continue
  eligible+=1;k=idx[0];dp=float(np.max(np.abs(f['Mhistory_orbit'][i,k,:3]-pos)));dv=float(np.max(np.abs(f['Mhistory_vel'][i,k,:3]-vel)))
  if dp<1 and dv<.002:matches.append({'event_row':i,'halo_id':int(f['HaloID'][i]),'max_pos_difference_ckpc_h':dp,'max_vel_difference_km_s':dv})
assert 5 in [x['event_row'] for x in matches]
out={'api_observation_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'snapshot':99,'subhalo_id':0,'eligible_event_rows':eligible,'matches':matches,'position_tolerance_ckpc_h':1,'velocity_tolerance_km_s':.002,'caveat':'One cached API check; matching phase-space coordinates is not independent merger-tree or group membership proof.'}
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print('Eligible:',eligible,'Matching histories:',len(matches),'IDs:',sorted({x['halo_id'] for x in matches}))
