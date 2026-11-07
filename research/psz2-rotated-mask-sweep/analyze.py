#!/usr/bin/env python3
"""Post-hoc symmetric map exclusion, PSZ2 G181 600 kpc region."""
import csv,hashlib,json,math,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
from scipy.signal import fftconvolve
from scipy.ndimage import map_coordinates
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;folder=Path(sys.argv[1]);cat=Path(sys.argv[2]);priorpath=p.parent/'two-cluster-physical-beam'/'summary.json';prior=json.loads(priorpath.read_text())
files={'T50':('PSZ2G181.06+48.47T50kpc.fits','d08c263b83712bdc40b13357ef297ce6e389437d666aee870fdf68f8489ce5b4'),'T50SUB':('PSZ2G181.06+48.47T50kpcSUB.fits','021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6')}
if hashlib.sha256(cat.read_bytes()).hexdigest()!=prior['catalog_sha256']:raise ValueError('Unexpected catalog')
lines=cat.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'));rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'));hits={r['Pos'].strip():r for r in rows if r['Name'].strip()=='PSZ2 G181.06+48.47'}
if set(hits)!={'N','S'}:raise ValueError('Catalog identity mismatch')
coords={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()};scale=FlatLambdaCDM(H0=70,Om0=.3).kpc_proper_per_arcmin(.234).value/60;fwhm=(135/scale)/3600;target=np.eye(2)*fwhm**2/(8*np.log(2));smooth={};w={}
for k,(name,digest) in files.items():
 f=folder/name
 if hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise ValueError('Image hash mismatch')
 with fits.open(f) as h:a=np.squeeze(h[0].data).astype(float);head=h[0].header.copy()
 if a.ndim!=2 or head.get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected FITS')
 with warnings.catch_warnings():warnings.simplefilter('ignore');w[k]=WCS(head).celestial
 t=np.deg2rad(head['BPA']);e=np.array([np.sin(t),np.cos(t)]);n=np.array([np.cos(t),-np.sin(t)]);cov=(head['BMAJ']**2*np.outer(e,e)+head['BMIN']**2*np.outer(n,n))/(8*np.log(2));inv=np.linalg.inv(w[k].pixel_scale_matrix);C=inv@(target-cov)@inv.T
 if np.linalg.eigvalsh(C).min()<=0:raise ValueError('Invalid target beam')
 r=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(C).max())));y,x=np.mgrid[-r:r+1,-r:r+1];v=np.stack([x,y],axis=-1);K=np.exp(-.5*np.einsum('...i,ij,...j->...',v,np.linalg.inv(C),v));K/=K.sum();actual=np.einsum('n,ni,nj->ij',K.ravel(),v.reshape(-1,2),v.reshape(-1,2))
 if not np.allclose(actual,C,rtol=1e-5,atol=1e-5):raise ValueError('Kernel covariance')
 valid=np.isfinite(a);coverage=fftconvolve(valid.astype(float),K,mode='same');smooth[k]=fftconvolve(np.where(valid,a,0),K,mode='same')*(fwhm**2/(head['BMAJ']*head['BMIN']))*1000;smooth[k][coverage<.999]=np.nan
Y,X=np.indices(smooth['T50SUB'].shape);sky=w['T50SUB'].pixel_to_world(X,Y);xx,yy=w['T50'].world_to_pixel(sky);images={'T50':map_coordinates(smooth['T50'],[yy,xx],order=1,mode='constant',cval=np.nan),'T50SUB':smooth['T50SUB']};common=np.isfinite(images['T50'])&np.isfinite(images['T50SUB']);J=w['T50SUB'].pixel_scale_matrix;pixscale=np.sqrt(np.sum(J**2,axis=0))*3600
if not np.allclose(pixscale,[2,2],rtol=1e-4):raise ValueError('Pixel scale mismatch')
pixels={k:w['T50SUB'].world_to_pixel(c) for k,c in coords.items()};peakdata=prior['psz2_southern_difference_peak'];peak=SkyCoord(peakdata['ra_deg']*u.deg,peakdata['dec_deg']*u.deg);px,py=w['T50SUB'].world_to_pixel(peak);sx,sy=pixels['S'];cx,cy=2*sx-px,2*sy-py;controls={'peak':(px,py),'reflected':(cx,cy),'rotated_90':(sx-(py-sy),sy+(px-sx)),'rotated_minus90':(sx+(py-sy),sy-(px-sx))}
# Evenly spaced pixel-plane rotations keep the same radial distance from the
# southern catalog position; nearby masks overlap and are not independent.
dx,dy=px-sx,py-sy
controls={}
for angle in range(0,360,10):
 theta=np.deg2rad(angle);controls[angle]=(sx+dx*np.cos(theta)-dy*np.sin(theta),sy+dx*np.sin(theta)+dy*np.cos(theta))
records=[]
for angle,point in [(None,None)]+list(controls.items()):
 exclusion=np.zeros_like(common,dtype=bool) if point is None else np.hypot(X-point[0],Y-point[1])<=40/pixscale[0]
 centers={};counts={}
 for image,arr in images.items():
  centers[image]={}
  for key,(x,y) in pixels.items():
   circle=np.hypot(X-x,Y-y)<=(600/scale)/pixscale[0]
   if (circle&common).sum()/circle.sum()<.99:raise ValueError('Insufficient common coverage')
   mask=circle&common&~exclusion&(arr>.2);iy,ix=np.where(mask);values=arr[mask]
   if len(values)<10:raise ValueError('Too few eligible pixels')
   n=math.ceil(.1*len(values));selection=np.argsort(values,kind='stable')[-n:];centers[image][key]=w['T50SUB'].pixel_to_world(np.average(ix[selection],weights=values[selection]),np.average(iy[selection],weights=values[selection]));counts[image,key]=(len(values),n)
 sep={k:centers[k]['N'].separation(centers[k]['S']).arcsec for k in images};delta=sep['T50']-sep['T50SUB']
 for image in images:
  for key in coords:
   c=centers[image][key];eligible,n=counts[image,key];records.append({'angle_deg':'baseline' if angle is None else angle,'image':image,'relic':key,'ra_deg':float(c.ra.deg),'dec_deg':float(c.dec.deg),'eligible':eligible,'selected':n,'pair_delta_kpc':float(delta*scale)})
base=next(r for r in records if r['angle_deg']=='baseline' and r['image']=='T50' and r['relic']=='S');selected=next(r for r in records if r['angle_deg']==0 and r['image']=='T50' and r['relic']=='S')
old=json.loads((p.parent/'psz2-boundary-ablation'/'summary.json').read_text())
if abs(base['pair_delta_kpc']-old['cases']['none_0']['pair_delta_kpc'])>1e-6 or abs(selected['pair_delta_kpc']-old['cases']['peak_40']['pair_delta_kpc'])>1e-6:raise ValueError('Baseline or selected peak differs from prior')
base_counts={im:next(r['eligible'] for r in records if r['angle_deg']=='baseline' and r['image']==im and r['relic']=='S') for im in images}
for r in records:
 r['removed_eligible_south']=base_counts[r['image']]-next(x['eligible'] for x in records if x['angle_deg']==r['angle_deg'] and x['image']==r['image'] and x['relic']=='S')
with (p/'variants.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');wr.writeheader();wr.writerows(records)
byangle={angle:{im:next(r for r in records if r['angle_deg']==angle and r['image']==im and r['relic']=='S') for im in images} for angle in controls}
peak_removed={im:byangle[0][im]['removed_eligible_south'] for im in images};eligible_match=[a for a in controls if a!=0 and all(abs(byangle[a][im]['removed_eligible_south']-peak_removed[im])<=.25*peak_removed[im] for im in images)]
other=[byangle[a]['T50']['pair_delta_kpc'] for a in controls if a!=0]
summary={'angles_deg':list(controls),'mask_radius_arcsec':40,'baseline_pair_delta_kpc':base['pair_delta_kpc'],'selected_peak_pair_delta_kpc':selected['pair_delta_kpc'],'peak_removed_eligible_south':peak_removed,'other_angles_pair_delta_kpc_range':[min(other),max(other)],'other_angles_at_least_as_close_to_zero':sum(abs(v)<=abs(selected['pair_delta_kpc']) for v in other),'eligible_count_matching_rule':'For each image, southern threshold-eligible pixels removed within 25% of selected peak count; post-hoc descriptive filter.','matching_angles':eligible_match,'matching_angle_pair_deltas_kpc':{str(a):byangle[a]['T50']['pair_delta_kpc'] for a in eligible_match},'prior_summary_sha256':hashlib.sha256(priorpath.read_bytes()).hexdigest(),'warning':'Post-hoc peak selection, overlapping masks, related maps and nonrandom control angles: counts and ranking are descriptive, not p-values, causal identification or population inference.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8,4.5));angles=list(controls);ax.plot(angles,[byangle[a]['T50']['pair_delta_kpc'] for a in angles],color='#226e89',marker='o',ms=3);ax.scatter([0],[selected['pair_delta_kpc']],color='#d05134',s=70,label='Selected difference peak');ax.axhline(base['pair_delta_kpc'],color='gray',ls='--',label='No exclusion');ax.axhline(0,color='gray',lw=.8);ax.set(xlabel='Rotation of mask around southern catalog position (degrees)',ylabel='T50 minus T50SUB pair separation (kpc)',title='PSZ2: rotated 40-arcsecond exclusion masks');ax.legend(fontsize=8);fig.text(.5,.01,'Post-hoc peak; adjacent masks overlap and controls are not independent.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'sweep.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
