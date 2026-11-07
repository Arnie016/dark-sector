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
files={'T50':('PSZ2G099.48+55.60T50kpc.fits','d0b6497804569ba90299d7160aefd68ab42f27981f4a87478a0ca29e17033db4'),'T50SUB':('PSZ2G099.48+55.60T50kpcSUB.fits','9a27db5ff41df8e825315b0d70afd99c2fbe4f23a04d354c6d6a11a5f5f538f7')}
if hashlib.sha256(cat.read_bytes()).hexdigest()!=prior['catalog_sha256']:raise ValueError('Unexpected catalog')
lines=cat.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'));rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'));hits={r['Pos'].strip():r for r in rows if r['Name'].strip()=='PSZ2 G099.48+55.60'}
if set(hits)!={'N','S'}:raise ValueError('Catalog identity mismatch')
coords={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()};scale=FlatLambdaCDM(H0=70,Om0=.3).kpc_proper_per_arcmin(.105).value/60;fwhm=(135/scale)/3600;target=np.eye(2)*fwhm**2/(8*np.log(2));smooth={};w={}
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
if not np.allclose(pixscale,[5,5],rtol=1e-4):raise ValueError('Pixel scale mismatch')
pixels={k:w['T50SUB'].world_to_pixel(c) for k,c in coords.items()};difference=images['T50']-images['T50SUB'];peaks={};radius_pixels=(600/scale)/pixscale[0]
for relic,(x,y) in pixels.items():
 if min(x,y,X.shape[1]-1-x,X.shape[0]-1-y)<radius_pixels:raise ValueError('Aperture outside map')
 region=(np.hypot(X-x,Y-y)<=radius_pixels)&common
 if region.sum()/((np.hypot(X-x,Y-y)<=radius_pixels).sum())<.99:raise ValueError('Insufficient finite coverage')
 iy,ix=np.unravel_index(np.argmax(np.where(region,difference,-np.inf)),difference.shape);sky=w['T50SUB'].pixel_to_world(ix,iy);peaks[relic]={'x':int(ix),'y':int(iy),'ra_deg_fk5':float(sky.ra.deg),'dec_deg_fk5':float(sky.dec.deg),'difference_mjy_per_beam':float(difference[iy,ix]),'offset_catalog_arcsec':float(sky.separation(coords[relic]).arcsec)}
beam_arcsec=135/scale;cases={'none':(), 'north':('N',),'south':('S',),'both':('N','S')};rows=[]
for label,masked in cases.items():
 exclusion=np.zeros_like(common,dtype=bool)
 for k in masked:exclusion |= np.hypot(X-peaks[k]['x'],Y-peaks[k]['y'])<=beam_arcsec/pixscale[0]
 centers={im:{} for im in images};counts={}
 for im,arr in images.items():
  for relic,(x,y) in pixels.items():
   circle=np.hypot(X-x,Y-y)<=radius_pixels;mask=circle&common&~exclusion&(arr>.2);iy,ix=np.where(mask);values=arr[mask]
   if len(values)<10:raise ValueError('Too few pixels after exclusion')
   n=math.ceil(.1*len(values));sel=np.argsort(values,kind='stable')[-n:];centers[im][relic]=w['T50SUB'].pixel_to_world(np.average(ix[sel],weights=values[sel]),np.average(iy[sel],weights=values[sel]));counts[im,relic]=(len(values),n)
 pair=(centers['T50']['N'].separation(centers['T50']['S']).arcsec-centers['T50SUB']['N'].separation(centers['T50SUB']['S']).arcsec)*scale
 for im in images:
  for relic in coords:
   c=centers[im][relic];eligible,n=counts[im,relic];rows.append({'case':label,'image':im,'relic':relic,'ra_fk5_deg':float(c.ra.deg),'dec_fk5_deg':float(c.dec.deg),'eligible':eligible,'selected':n,'pair_delta_kpc':float(pair)})
old=list(csv.DictReader((p.parent/'g099-paired-positions'/'variants.csv').open()));reference=next(r for r in old if int(r['radius_kpc'])==600 and float(r['threshold_mjy_per_beam'])==.2 and r['image']=='T50' and r['relic']=='N');baseline=next(r['pair_delta_kpc'] for r in rows if r['case']=='none')
if abs(baseline-float(reference['pair_difference_kpc']))>1e-6:raise ValueError('Saved baseline mismatch')
with (p/'variants.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');wr.writeheader();wr.writerows(rows)
summary={'target_beam_kpc':135,'mask_radius_arcsec':float(beam_arcsec),'aperture_kpc':600,'threshold_mjy_per_beam':.2,'peaks':peaks,'pair_delta_kpc':{case:next(r['pair_delta_kpc'] for r in rows if r['case']==case) for case in cases},'warning':'Peak locations and exclusions chosen after data inspection; two products share observations. Masks are not author regions; no causal source identification, uncertainty or physical clock inference.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,axes=plt.subplots(1,2,figsize=(10,4.2));window=(800/scale)/pixscale[0]
for ax,relic in zip(axes,('N','S')):
 x,y=pixels[relic];x0=max(0,int(x-window));x1=min(X.shape[1],int(x+window)+1);y0=max(0,int(y-window));y1=min(X.shape[0],int(y+window)+1)
 im=ax.imshow(difference[y0:y1,x0:x1],origin='lower',cmap='coolwarm',vmin=-5,vmax=5);ax.add_patch(plt.Circle((x-x0,y-y0),radius_pixels,fill=False,color='black',ls='--'));ax.add_patch(plt.Circle((peaks[relic]['x']-x0,peaks[relic]['y']-y0),beam_arcsec/pixscale[0],fill=False,color='lime'));ax.scatter(peaks[relic]['x']-x0,peaks[relic]['y']-y0,marker='+',color='lime');ax.set_title(relic+' relic region');ax.set_xlabel('Cutout pixel x');ax.set_ylabel('Cutout pixel y')
fig.colorbar(im,ax=axes,location='right',fraction=.03,label='T50 minus T50SUB mJy/beam (clipped)');fig.suptitle('Abell 1925: post-hoc difference peaks and masks');fig.text(.5,.01,'Black: 600 kpc aperture; green: one-beam peak exclusion.',ha='center',fontsize=8);fig.subplots_adjust(left=.07,right=.88,bottom=.17,top=.86,wspace=.3);fig.savefig(p/'difference-regions.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
