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
# This is a post-hoc decomposition on the exact shared support and ranking.
# Pixel-value sums are used only as weights, not as integrated fluxes.
fractions=(.01,.05,.10,.20,.50,1.0);feature=np.hypot(X-px,Y-py)<=40/pixscale[0];records=[];verification={}
for reference in ('T50','T50SUB'):
 for fraction in fractions:
  centers={im:{} for im in images}
  for relic,(cx,cy) in pixels.items():
   circle=(np.hypot(X-cx,Y-cy)<=(600/scale)/pixscale[0])&common;joint=circle&(images['T50']>.2)&(images['T50SUB']>.2);ids=np.flatnonzero(joint)
   if len(ids)<100:raise ValueError('Insufficient joint pixels')
   n=math.ceil(fraction*len(ids));chosen=ids[np.argsort(images[reference].ravel()[ids],kind='stable')[-n:]];iy,ix=np.unravel_index(chosen,images[reference].shape);inside=feature.ravel()[chosen]
   for im in images:
    weights=images[im].ravel()[chosen];total=weights.sum()
    if not np.isfinite(total) or np.any(weights<=0):raise ValueError('Invalid weights')
    xbar=np.average(ix,weights=weights);ybar=np.average(iy,weights=weights)
    if inside.any() and (~inside).any():
     q=weights[inside].sum()/total
     assert np.allclose([xbar,ybar],q*np.array([np.average(ix[inside],weights=weights[inside]),np.average(iy[inside],weights=weights[inside])])+(1-q)*np.array([np.average(ix[~inside],weights=weights[~inside]),np.average(iy[~inside],weights=weights[~inside])]),atol=1e-10)
    c=w['T50SUB'].pixel_to_world(xbar,ybar);centers[im][relic]=c
    records.append({'reference':reference,'fraction':fraction,'image':im,'relic':relic,'selected_count':n,'boundary_selected_count':int(inside.sum()),'boundary_selected_fraction':float(inside.mean()),'boundary_weight_fraction':float(weights[inside].sum()/total),'ra_deg':float(c.ra.deg),'dec_deg':float(c.dec.deg)})
  pair=(centers['T50']['N'].separation(centers['T50']['S']).arcsec-centers['T50SUB']['N'].separation(centers['T50SUB']['S']).arcsec)*scale
  verification[f'{reference}_{fraction}']=float(pair)
oldpath=p.parent/'psz2-bright-fraction-sensitivity'/'summary.json';old=json.loads(oldpath.read_text())
for ref in ('T50','T50SUB'):
 for f in fractions:
  if abs(verification[f'{ref}_{f}']-old['results_kpc']['none'][ref][str(f)])>1e-6:raise ValueError('Fraction baseline mismatch')
with (p/'contributions.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');wr.writeheader();wr.writerows(records)
summary={'input_fraction_summary_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),'region':'40 arcsec around post-hoc PSZ2 difference peak','southern_region_contributions':{ref:{str(f):{im:next({'selected':r['selected_count'],'in_region':r['boundary_selected_count'],'selected_fraction':r['boundary_selected_fraction'],'weight_fraction':r['boundary_weight_fraction']} for r in records if r['reference']==ref and r['fraction']==f and r['image']==im and r['relic']=='S') for im in images} for f in fractions} for ref in ('T50','T50SUB')},'limitations':'Same correlated images, source region selected after inspection; weights are sums of correlated pixel values, not integrated flux. No inference about source physics, measurement uncertainty or clock bias.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8,4.5))
for ref,color in [('T50','#b45436'),('T50SUB','#23728c')]:
 for im,style in [('T50','-'),('T50SUB','--')]:
  vals=[summary['southern_region_contributions'][ref][str(f)][im]['weight_fraction'] for f in fractions];ax.plot([f*100 for f in fractions],vals,color=color,ls=style,marker='o',label=ref+' reference, '+im+' weights')
ax.set_xscale('log');ax.set_xticks([1,5,10,20,50,100],['1','5','10','20','50','100']);ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter());ax.set(xlabel='Brightest fraction of jointly eligible pixels (%)',ylabel='Fraction of selected weight in boundary circle',title='PSZ2: selected weights near the difference peak');ax.legend(fontsize=8);fig.text(.5,.01,'Correlated pixel weights are not integrated flux; region selected post-hoc.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'weight-contributions.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
