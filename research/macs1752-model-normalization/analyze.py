#!/usr/bin/env python3
"""Test two model-unit hypotheses against one selected radio-map region."""
import hashlib,json,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from scipy.signal import fftconvolve
import astropy.units as u
p=Path(__file__).resolve().parent;d=Path(sys.argv[1]);items={'T50kpc.fits':'ad491b8e9df67889f1e9ee8f3e9f323052698705ca553c8875e3b7d0262bd124','T50kpcSUB.fits':'d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de','compact-model.fits':'3791a6d8d8e34c2f2e23c6fbbe96486f1331d23abf5e9ce81b86cdc575d7c03e'}
a={};h={};w={}
for name,sha in items.items():
 f=d/name
 if hashlib.sha256(f.read_bytes()).hexdigest()!=sha:raise ValueError('Unexpected source hash')
 with fits.open(f) as x:a[name]=np.squeeze(x[0].data).astype(float);h[name]=x[0].header.copy()
 if a[name].ndim!=2 or h[name].get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected FITS metadata')
 with warnings.catch_warnings():warnings.simplefilter('ignore');w[name]=WCS(h[name]).celestial
assert len({x.shape for x in a.values()})==1
base=w['T50kpc.fits']; points=np.array([100,808,1500]);sky=base.pixel_to_world(points,points)
for z in w.values():
 x,y=z.world_to_pixel(sky);assert max(np.max(abs(x-points)),np.max(abs(y-points)))<1e-5
ht=h['T50kpc.fits'];hs=h['T50kpcSUB.fits'];hm=h['compact-model.fits']
for k in ('BMAJ','BMIN','BPA'):assert np.isclose(ht[k],hs[k],rtol=1e-6,atol=2e-5 if k=='BPA' else 1e-9)
def cov(h):
 theta=np.deg2rad(h['BPA']);e=np.array([np.sin(theta),np.cos(theta)]);n=np.array([np.cos(theta),-np.sin(theta)])
 return (h['BMAJ']**2*np.outer(e,e)+h['BMIN']**2*np.outer(n,n))/(8*np.log(2))
J=base.pixel_scale_matrix;inv=np.linalg.inv(J)
def gaussian(C):
 C=inv@C@inv.T
 if np.linalg.eigvalsh(C).min()<=0:raise ValueError('Nonpositive kernel covariance')
 r=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(C).max())));y,x=np.mgrid[-r:r+1,-r:r+1];pos=np.stack([x,y],axis=-1)
 q=np.exp(-.5*np.einsum('...i,ij,...j->...',pos,np.linalg.inv(C),pos)); return q
src=np.where(np.isfinite(a['compact-model.fits']),a['compact-model.fits'],0)
# Hypothesis A: restored Jy/source-beam model. Hypothesis B: un-convolved Jy/pixel components.
kA=gaussian(cov(ht)-cov(hm));kA/=kA.sum();ratio=ht['BMAJ']*ht['BMIN']/(hm['BMAJ']*hm['BMIN'])
kB=gaussian(cov(ht)); assert np.isclose(kB.max(),1)
predA=fftconvolve(src,kA,mode='same')*ratio*1000;predB=fftconvolve(src,kB,mode='same')*1000
diff=(a['T50kpc.fits']-a['T50kpcSUB.fits'])*1000
prev=json.loads((p.parent/'macs1752-difference-localization'/'summary.json').read_text());c=SkyCoord(*prev['peak_position_deg'],unit='deg');cx,cy=base.world_to_pixel(c);yy,xx=np.indices(diff.shape);scale=np.sqrt(np.sum(base.pixel_scale_matrix**2,axis=0))*3600
assert np.allclose(scale,[1.5,1.5],rtol=1e-4)
region=(np.hypot(xx-cx,yy-cy)*scale[0]<=30)&np.isfinite(diff)&np.isfinite(a['compact-model.fits'])
assert region.sum()>100
peak_idx=np.unravel_index(np.argmax(np.where(region,diff,-np.inf)),diff.shape)
rr=kB.shape[0]//2; py,px=peak_idx
local=a['compact-model.fits'][py-rr:py+rr+1,px-rr:px+rr+1]
assert local.shape==kB.shape and np.isfinite(local).all()
assert np.isclose(np.sum(local*kB)*1000,predB[py,px],rtol=1e-10,atol=1e-10)
def stats(pred):
 err=pred[region]-diff[region]
 return {'peak_mjy_per_beam':float(np.max(pred[region])),'difference_to_model_peak_ratio':float(np.max(diff[region])/np.max(pred[region])),'rms_residual_mjy_per_beam':float(np.sqrt(np.mean(err**2))),'pixel_pearson_r':float(np.corrcoef(pred[region],diff[region])[0,1])}
res={'pixels':int(region.sum()),'region_radius_arcsec':30,'difference_peak_mjy_per_beam':float(np.max(diff[region])),'A_restored_beam_hypothesis':stats(predA),'B_unconvolved_components_hypothesis':stats(predB),'warning':'Post-hoc unit hypotheses, same data and correlated pixels; actual model provenance, units and processing remain unverified.'}
(p/'summary.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
