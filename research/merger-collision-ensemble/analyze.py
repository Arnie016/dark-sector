"""Compare distinct velocity estimators at catalog collision snapshots."""
import argparse,csv,hashlib,json
from pathlib import Path
import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
q=argparse.ArgumentParser();q.add_argument('catalog',type=Path);arg=q.parse_args()
expected='d9d103b13a40cb8088914e025310fd2d8f99eb20f679e57e54b6eb5dcf78253d'
assert hashlib.sha256(arg.catalog.read_bytes()).hexdigest()==expected, 'Incorrect catalog version'
zs={int(i['number']):float(i['redshift']) for i in json.loads((p/'snapshot_redshifts.json').read_text())}
h=.6774;om=.3089;ol=.6911; box=680000.
def age(a):return 2*9.7779222168/(3*h*np.sqrt(ol))*np.arcsinh(np.sqrt(ol/om)*a**1.5)
records=[];reject={}
def skip(reason):reject[reason]=reject.get(reason,0)+1
with h5py.File(arg.catalog) as f:
 for i in range(len(f['HaloID'])):
  sc=int(f['Snap_coll'][i]);sn=f['Mhistory_snap'][i];ids=[]
  for s in (sc-1,sc,sc+1):
   match=np.flatnonzero(sn==s)
   if len(match)!=1:break
   ids.append(int(match[0]))
  if len(ids)!=3 or sc-1<30 or sc+1>99 or not all(s in zs for s in (sc-1,sc,sc+1)):
   skip('missing_unique_adjacent_snapshots');continue
  pos=f['Mhistory_orbit'][i][ids];vel=f['Mhistory_vel'][i][ids]
  if not np.all(np.isfinite(pos)) or not np.all(np.isfinite(vel)) or np.any(pos<0) or np.any(pos>=box):
   skip('invalid_position_or_velocity');continue
  a=1/(1+np.array([zs[s] for s in (sc-1,sc,sc+1)]));t=age(a)
  dx=(pos[:,3:]-pos[:,:3]+box/2)%box-box/2
  dx=np.unwrap(dx*2*np.pi/box,axis=0)*box/(2*np.pi)
  fd=np.gradient(dx,t,axis=0,edge_order=2)[1]*(a[1]/h)*.9777922217
  v=vel[1,3:]-vel[1,:3]; norm=float(np.linalg.norm(fd-v)); speed=float(np.linalg.norm(v)); vc=float(f['V_coll'][i])
  records.append(dict(row=i,halo_id=int(f['HaloID'][i]),snap_coll=sc,discrepancy_km_s=norm,catalog_speed_km_s=speed,v_coll_km_s=vc,vc_abs_difference_km_s=abs(vc-speed)))
assert records
err=np.array([r['discrepancy_km_s'] for r in records]);vc=np.array([r['vc_abs_difference_km_s'] for r in records]);halos={r['halo_id'] for r in records}
summary={'catalog_sha256':expected,'total_rows':2083,'selected_rows':len(records),'distinct_halo_ids':len(halos),'rejections':reject,'median_discrepancy_km_s':float(np.median(err)),'p90_discrepancy_km_s':float(np.quantile(err,.9)),'median_abs_vcoll_difference_km_s':float(np.median(vc)),'fraction_vcoll_within_0_1_km_s':float(np.mean(vc<.1)),'warning':'Estimator discrepancy, not velocity error or evidence of new physics. Rows can share halos.'}
with (p/'collision-comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8,5),layout='constrained');ax.hist(err,bins=np.arange(0,4001,100),color='#477c8d');ax.set(xlabel='3D estimator discrepancy at collision [km/s]',ylabel='Catalog merger events',title='Selected TNG-Cluster collision snapshots');ax.text(.98,.95,f'{np.sum(err>=4000)} events ≥ 4000 km/s omitted',transform=ax.transAxes,ha='right',va='top');ax.grid(axis='y',alpha=.2);fig.savefig(p/'collision-discrepancy.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
