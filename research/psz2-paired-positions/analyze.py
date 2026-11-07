#!/usr/bin/env python3
"""Paired bright-pixel position diagnostic at common beam for PSZ2 G181."""
import csv,hashlib,json,math,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from scipy.signal import fftconvolve
from scipy.ndimage import map_coordinates
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=Path(__file__).resolve().parent; folder=Path(sys.argv[1]); catalog=Path(sys.argv[2])
files={'T50':('PSZ2G181.06+48.47T50kpc.fits','d08c263b83712bdc40b13357ef297ce6e389437d666aee870fdf68f8489ce5b4'),'T50SUB':('PSZ2G181.06+48.47T50kpcSUB.fits','021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6')}
if hashlib.sha256(catalog.read_bytes()).hexdigest()!='4a46302883b9308a771eb2ebf914f8b0a22a22a10f6280f33477568689d70db9': raise ValueError('Catalog hash mismatch')
lines=catalog.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'))
rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'))
hits={r['Pos'].strip():r for r in rows if r['Name'].strip()=='PSZ2 G181.06+48.47'}
if set(hits)!={'N','S'}:raise ValueError('Missing or unexpected relic coordinates')
coords={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()}
img={};head={};w={}
for k,(name,sha) in files.items():
 f=folder/name
 if hashlib.sha256(f.read_bytes()).hexdigest()!=sha: raise ValueError('Image hash mismatch')
 with fits.open(f) as h:img[k]=np.squeeze(h[0].data).astype(float);head[k]=h[0].header.copy()
 if img[k].ndim!=2 or head[k].get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected image unit or dimensions')
 with warnings.catch_warnings():warnings.simplefilter('ignore');w[k]=WCS(head[k]).celestial
fwhm=25/3600;target=np.eye(2)*fwhm**2/(8*np.log(2));smooth={}
for k in files:
 h=head[k];t=np.deg2rad(h['BPA']);e=np.array([np.sin(t),np.cos(t)]);n=np.array([np.cos(t),-np.sin(t)])
 cov=(h['BMAJ']**2*np.outer(e,e)+h['BMIN']**2*np.outer(n,n))/(8*np.log(2)); inv=np.linalg.inv(w[k].pixel_scale_matrix); C=inv@(target-cov)@inv.T
 if np.linalg.eigvalsh(C).min()<=0:raise ValueError('Invalid beam kernel')
 r=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(C).max())));y,x=np.mgrid[-r:r+1,-r:r+1];v=np.stack([x,y],axis=-1);K=np.exp(-.5*np.einsum('...i,ij,...j->...',v,np.linalg.inv(C),v));K/=K.sum()
 actual=np.einsum('n,ni,nj->ij',K.ravel(),v.reshape(-1,2),v.reshape(-1,2))
 if not np.allclose(actual,C,rtol=1e-5,atol=1e-5):raise ValueError('Discretized beam mismatch')
 valid=np.isfinite(img[k]);coverage=fftconvolve(valid.astype(float),K,mode='same');smooth[k]=fftconvolve(np.where(valid,img[k],0),K,mode='same')*(fwhm**2/(h['BMAJ']*h['BMIN']))*1000;smooth[k][coverage<.999]=np.nan
Y,X=np.indices(smooth['T50SUB'].shape);sky=w['T50SUB'].pixel_to_world(X,Y);xx,yy=w['T50'].world_to_pixel(sky)
paired={'T50':map_coordinates(smooth['T50'],[yy,xx],order=1,mode='constant',cval=np.nan),'T50SUB':smooth['T50SUB']};common=np.isfinite(paired['T50'])&np.isfinite(paired['T50SUB']);J=w['T50SUB'].pixel_scale_matrix;scales=np.sqrt(np.sum(J**2,axis=0))*3600
if not np.allclose(scales,[2,2],rtol=1e-4):raise ValueError('Unexpected pixel scales')
pix={k:w['T50SUB'].world_to_pixel(v) for k,v in coords.items()};results=[]
for radius in (60,90,120):
 for threshold in (.1,.2,.3):
  centers={};samples={}
  for image,arr in paired.items():
   centers[image]={}
   for key,(cx,cy) in pix.items():
    circle=np.hypot(X-cx,Y-cy)<=radius/scales[0]
    fraction=float((circle&common).sum()/circle.sum())
    if fraction<.99:raise ValueError(f'Insufficient common coverage: {key} radius {radius} fraction {fraction:.3f}')
    mask=circle&common&(arr>threshold);iy,ix=np.where(mask);values=arr[mask]
    if len(values)<10:raise ValueError('Insufficient selected pixels')
    n=math.ceil(.1*len(values));idx=np.argsort(values,kind='stable')[-n:];coord=w['T50SUB'].pixel_to_world(np.average(ix[idx],weights=values[idx]),np.average(iy[idx],weights=values[idx]));centers[image][key]=coord;samples[image,key]=(len(values),n,fraction)
  sep={im:centers[im]['N'].separation(centers[im]['S']).arcsec for im in paired}
  for image in paired:
   for key in coords:
    coord=centers[image][key];eligible,n,coverage=samples[image,key]
    results.append({'radius_arcsec':radius,'threshold_mjy_per_target_beam':threshold,'image':image,'relic':key,'eligible_pixels':eligible,'brightest_pixels':n,'coverage_fraction':coverage,'ra_deg':float(coord.ra.deg),'dec_deg':float(coord.dec.deg),'paired_center_delta_arcsec':float(centers['T50'][key].separation(centers['T50SUB'][key]).arcsec),'paired_separation_delta_arcsec':float(sep['T50']-sep['T50SUB'])})
with (p/'variants.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(results[0]),lineterminator='\n');wr.writeheader();wr.writerows(results)
summary={'target_fwhm_arcsec':25,'radii_arcsec':[60,90,120],'thresholds_mjy_per_target_beam':[.1,.2,.3],'configurations':9,'paired_center_delta_arcsec':{key:[min(r['paired_center_delta_arcsec'] for r in results if r['relic']==key),max(r['paired_center_delta_arcsec'] for r in results if r['relic']==key)] for key in coords},'signed_pair_delta_arcsec':[min(r['paired_separation_delta_arcsec'] for r in results),max(r['paired_separation_delta_arcsec'] for r in results)],'minimum_common_coverage_fraction':min(r['coverage_fraction'] for r in results),'inputs_sha256':{k:sha for k,(name,sha) in files.items()},'catalog_sha256':hashlib.sha256(catalog.read_bytes()).hexdigest(),'caveat':'Post-hoc two-field comparison; related images, arbitrary masks, 25 arcsec target beam and bilinear interpolation; no physical clock or independent uncertainty.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7,4.5))
for key,color in [('N','#2e7293'),('S','#c46538')]:
 for j,radius in enumerate((60,90,120)):
  q=[r for r in results if r['relic']==key and r['radius_arcsec']==radius and r['image']=='T50SUB'];ax.plot([r['threshold_mjy_per_target_beam'] for r in q],[r['paired_center_delta_arcsec'] for r in q],color=color,marker=['o','s','^'][j],linestyle=['-','--',':'][j],label=f'{key}, {radius} arcsec')
ax.set(xlabel='Illustrative threshold (mJy/25-arcsec beam)',ylabel='Paired center difference (arcsec)',title='PSZ2 G181: position sensitivity across paired maps');ax.legend(ncol=2,fontsize=8);fig.text(.5,.01,'Same field, matched beam and common pixels; not a statistical uncertainty.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'paired-positions.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
