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
settings=[('none',0)]+[(name,r) for name in controls for r in (20,40,60)];records=[]
for name,rad in settings:
 exclusion=np.zeros_like(common,dtype=bool) if name=='none' else np.hypot(X-controls[name][0],Y-controls[name][1])<=rad/pixscale[0]
 centers={};counts={}
 for image,arr in images.items():
  centers[image]={}
  for key,(x,y) in pixels.items():
   circle=np.hypot(X-x,Y-y)<=(600/scale)/pixscale[0]
   if (circle&common).sum()/circle.sum()<.99:raise ValueError('Coverage')
   mask=circle&common&~exclusion&(arr>.2);iy,ix=np.where(mask);v=arr[mask]
   if len(v)<10:raise ValueError('Too few eligible pixels')
   n=math.ceil(.1*len(v));sel=np.argsort(v,kind='stable')[-n:];centers[image][key]=w['T50SUB'].pixel_to_world(np.average(ix[sel],weights=v[sel]),np.average(iy[sel],weights=v[sel]));counts[image,key]=(len(v),n)
 seps={k:centers[k]['N'].separation(centers[k]['S']).arcsec for k in images};delta=seps['T50']-seps['T50SUB']
 for image in images:
  for key in coords:
   c=centers[image][key];eligible,chosen=counts[image,key];records.append({'exclusion':name,'radius_arcsec':rad,'image':image,'relic':key,'ra_deg':float(c.ra.deg),'dec_deg':float(c.dec.deg),'eligible':eligible,'selected':chosen,'center_delta_arcsec':float(centers['T50'][key].separation(centers['T50SUB'][key]).arcsec),'pair_delta_arcsec':float(delta),'pair_delta_kpc':float(delta*scale)})
base=next(r for r in records if r['exclusion']=='none');priorrows=list(csv.DictReader((p.parent/'two-cluster-physical-beam'/'variants.csv').open()));reference=next(r for r in priorrows if r['cluster']=='PSZ2 G181' and r['radius_kpc']=='600' and float(r['threshold_mjy_per_beam'])==.2)
if abs(base['pair_delta_kpc']-float(reference['pair_difference_kpc']))>1e-6:raise ValueError('Baseline mismatch')
with (p/'variants.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');wr.writeheader();wr.writerows(records)
summary={'aperture_kpc':600,'threshold_mjy_per_beam':.2,'target_beam_kpc':135,'kpc_per_arcsec':float(scale),'peak_ra_deg':peak.ra.deg,'peak_dec_deg':peak.dec.deg,'reflected_control_ra_deg':float(w['T50SUB'].pixel_to_world(cx,cy).ra.deg),'reflected_control_dec_deg':float(w['T50SUB'].pixel_to_world(cx,cy).dec.deg),'prior_summary_sha256':hashlib.sha256(priorpath.read_bytes()).hexdigest(),'cases':{f"{r['exclusion']}_{r['radius_arcsec']}":{'pair_delta_kpc':r['pair_delta_kpc'],'south_center_delta_arcsec':r['center_delta_arcsec']} for r in records if r['image']=='T50' and r['relic']=='S'},'warning':'Post-hoc exclusion applied to both maps; three control locations are arbitrary and may contain no eligible pixels. No randomization, independence, uncertainty or causal source identity.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7,4.5))
for name,color in [('peak','#be5536'),('reflected','#1c7698'),('rotated_90','#579b46'),('rotated_minus90','#8066ab')]:
 q=[r for r in records if r['image']=='T50' and r['relic']=='S' and r['exclusion']==name];ax.plot([r['radius_arcsec'] for r in q],[r['pair_delta_kpc'] for r in q],marker='o',color=color,label=name+' exclusion')
ax.axhline(base['pair_delta_kpc'],color='gray',ls='--',label='No exclusion');ax.axhline(0,color='gray',lw=.8);ax.set(xlabel='Exclusion radius (arcsec)',ylabel='T50 minus T50SUB separation (kpc)',title='PSZ2: post-hoc exclusion sensitivity');ax.legend();fig.text(.5,.01,'Same mask applied to both maps; exploratory controls; not a causal test.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.05,1,1));fig.savefig(p/'ablation.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
