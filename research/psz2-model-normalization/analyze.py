#!/usr/bin/env python3
"""Compare model normalizations on a second cluster at matched restoring beam."""
import hashlib,json,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from scipy.signal import fftconvolve
from scipy.ndimage import map_coordinates
import astropy.units as u
p=Path(__file__).resolve().parent;d=Path(sys.argv[1]);files={'T50':'PSZ2G181.06+48.47T50kpc.fits','T50SUB':'PSZ2G181.06+48.47T50kpcSUB.fits','model':'PSZ2G181.06+48.47compact-model.fits'}
sha={'T50':'d08c263b83712bdc40b13357ef297ce6e389437d666aee870fdf68f8489ce5b4','T50SUB':'021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6','model':'96830980a2bc4284a5c8fd0efcf81ffed2806e599b0afdb3f6dc010ed6e6744d'}
a={};h={};w={}
for k,name in files.items():
 f=d/name
 if hashlib.sha256(f.read_bytes()).hexdigest()!=sha[k]: raise ValueError('Digest mismatch')
 with fits.open(f) as z: a[k]=np.squeeze(z[0].data).astype(float);h[k]=z[0].header.copy()
 if a[k].ndim!=2 or h[k].get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected FITS input')
 with warnings.catch_warnings():warnings.simplefilter('ignore');w[k]=WCS(h[k]).celestial
fwhm=25/3600;target=np.eye(2)*fwhm**2/(8*np.log(2))
def covariance(head):
 t=np.deg2rad(head['BPA']);e=np.array([np.sin(t),np.cos(t)]);n=np.array([np.cos(t),-np.sin(t)])
 return (head['BMAJ']**2*np.outer(e,e)+head['BMIN']**2*np.outer(n,n))/(8*np.log(2))
def kernel(k,C,normalization):
 J=w[k].pixel_scale_matrix;inv=np.linalg.inv(J);C=inv@C@inv.T
 if np.linalg.eigvalsh(C).min()<=0:raise ValueError('Cannot convolve to target beam')
 r=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(C).max())));y,x=np.mgrid[-r:r+1,-r:r+1];v=np.stack([x,y],axis=-1)
 z=np.exp(-.5*np.einsum('...i,ij,...j->...',v,np.linalg.inv(C),v))
 normalized=z/z.sum();actual=np.einsum('n,ni,nj->ij',normalized.ravel(),v.reshape(-1,2),v.reshape(-1,2))
 assert np.allclose(actual,C,rtol=1e-5,atol=1e-5)
 return normalized if normalization=='integral' else z/z.max()
def convolve(k,C,kind):
 K=kernel(k,C,kind);valid=np.isfinite(a[k]);norm=K/K.sum(); coverage=fftconvolve(valid.astype(float),norm,mode='same')
 out=fftconvolve(np.where(valid,a[k],0),K,mode='same');out[coverage<.999]=np.nan
 return out
# two radio images are restored in Jy/input beam; smooth to 25-arcsec common beam
rest={}
for k in ('T50','T50SUB'):
 rest[k]=convolve(k,target-covariance(h[k]),'integral')*(fwhm*fwhm/(h[k]['BMAJ']*h[k]['BMIN']))
modelA=convolve('model',target-covariance(h['model']),'integral')*(fwhm*fwhm/(h['model']['BMAJ']*h['model']['BMIN']))
modelB=convolve('model',target,'peak')
# interpolate all products onto T50SUB celestial grid
Y,X=np.indices(rest['T50SUB'].shape);sky=w['T50SUB'].pixel_to_world(X,Y)
def resample(img,k):
 xx,yy=w[k].world_to_pixel(sky);return map_coordinates(img,[yy,xx],order=1,mode='constant',cval=np.nan)
I=rest['T50SUB']; D=(resample(rest['T50'],'T50')-I)*1000;A=resample(modelA,'model')*1000;B=resample(modelB,'model')*1000
center=SkyCoord(144.8706*u.deg,40.7810*u.deg);cx,cy=w['T50SUB'].world_to_pixel(center);scale=np.sqrt(np.sum(w['T50SUB'].pixel_scale_matrix**2,axis=0))*3600
assert np.allclose(scale,[2,2],rtol=1e-4)
r=np.hypot(X-cx,Y-cy)*scale[0];valid=np.isfinite(D)&np.isfinite(A)&np.isfinite(B)&(r<=180);sel=valid&(B>.5)
if valid.sum()<1000 or sel.sum()<50:raise ValueError('Insufficient coverage or signal')
def stats(pred,mask):
 e=pred[mask]-D[mask];return {'pixels':int(mask.sum()),'rms_mjy_per_beam':float(np.sqrt(np.mean(e**2))),'median_abs_mjy_per_beam':float(np.median(abs(e))),'pixel_correlation':float(np.corrcoef(pred[mask],D[mask])[0,1])}
out={'target_fwhm_arcsec':25,'radius_arcsec':180,'all_finite':{'restored':stats(A,valid),'per_pixel':stats(B,valid)},'model_signal_above_0_5_mjy_per_beam':{'restored':stats(A,sel),'per_pixel':stats(B,sel)},'limits':'Same survey processing family; approximate Gaussian beams and interpolation; model-selected pixels correlated; model units and processing unverified.'}
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
