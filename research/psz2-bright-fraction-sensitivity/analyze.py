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
fractions=(.01,.05,.10,.20,.50,1.0);records=[]
for masked in (False,True):
 exclusion=np.hypot(X-px,Y-py)<=40/pixscale[0] if masked else np.zeros_like(common,dtype=bool)
 for fraction in fractions:
  for reference in ('T50','T50SUB'):
   centers={im:{} for im in images};nsel={}
   for relic,(x,y) in pixels.items():
    if min(x,y,X.shape[1]-1-x,X.shape[0]-1-y) < (600/scale)/pixscale[0]: raise ValueError('Aperture extends outside image')
    circle=(np.hypot(X-x,Y-y)<=(600/scale)/pixscale[0])&common&~exclusion
    joint=circle&(images['T50']>.2)&(images['T50SUB']>.2);ids=np.flatnonzero(joint)
    if len(ids)<100:raise ValueError('Insufficient joint pixels')
    n=math.ceil(fraction*len(ids));chosen=ids[np.argsort(images[reference].ravel()[ids],kind='stable')[-n:]];iy,ix=np.unravel_index(chosen,images[reference].shape);nsel[relic]=(len(ids),n)
    for im in images:
     weights=images[im].ravel()[chosen]
     if np.any(weights<=0):raise ValueError('Nonpositive weights')
     centers[im][relic]=w['T50SUB'].pixel_to_world(np.average(ix,weights=weights),np.average(iy,weights=weights))
   pair=(centers['T50']['N'].separation(centers['T50']['S']).arcsec-centers['T50SUB']['N'].separation(centers['T50SUB']['S']).arcsec)*scale
   for im in images:
    for relic in coords:
     c=centers[im][relic];total,n=nsel[relic];records.append({'mask':'peak40' if masked else 'none','reference':reference,'fraction':fraction,'image':im,'relic':relic,'joint_eligible':total,'selected':n,'ra_deg':float(c.ra.deg),'dec_deg':float(c.dec.deg),'pair_delta_kpc':float(pair)})
old=json.loads((p.parent/'psz2-shared-pixel-test'/'summary.json').read_text())
for mask in ('none','peak40'):
 for reference,key in [('T50','shared_t50_rank'),('T50SUB','shared_sub_rank')]:
  r=next(r for r in records if r['mask']==mask and r['reference']==reference and r['fraction']==.1)
  if abs(r['pair_delta_kpc']-old['results_kpc'][mask][key])>1e-6:raise ValueError('10 percent baseline mismatch')
for mask in ('none','peak40'):
 a=next(r['pair_delta_kpc'] for r in records if r['mask']==mask and r['reference']=='T50' and r['fraction']==1.)
 b=next(r['pair_delta_kpc'] for r in records if r['mask']==mask and r['reference']=='T50SUB' and r['fraction']==1.)
 if not np.isclose(a,b,atol=1e-8):raise ValueError('Full support must match')
with (p/'variants.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');wr.writeheader();wr.writerows(records)
summary={'fractions':list(fractions),'target_beam_kpc':135,'aperture_kpc':600,'threshold_mjy_per_beam':.2,'results_kpc':{mask:{reference:{str(f):next(r['pair_delta_kpc'] for r in records if r['mask']==mask and r['reference']==reference and r['fraction']==f) for f in fractions} for reference in ('T50','T50SUB')} for mask in ('none','peak40')},'limitations':'Post-hoc fixed threshold, related observations and jointly selected sky support; reference ranking is not an independent replication, probability, published mask or physical inference.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8,4.5))
for reference,color in [('T50','#b45436'),('T50SUB','#23728c')]:
 for mask,style in [('none','-'),('peak40','--')]:
  vals=[summary['results_kpc'][mask][reference][str(f)] for f in fractions];ax.plot([f*100 for f in fractions],vals,color=color,ls=style,marker='o',label=reference+'; '+mask)
ax.set_xscale('log');ax.set_xticks([1,5,10,20,50,100],['1','5','10','20','50','100']);ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter());ax.axhline(0,color='gray',lw=.8);ax.set(xlabel='Brightest fraction of jointly eligible pixels (%)',ylabel='T50 minus T50SUB pair separation (kpc)',title='PSZ2: effect of bright-pixel fraction');ax.legend(fontsize=8);fig.text(.5,.01,'Joint support, map-specific brightness weights; post-hoc selection.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'fraction-sensitivity.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
