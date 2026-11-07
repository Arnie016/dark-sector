#!/usr/bin/env python3
"""Compare difference patch with the archive's nominal compact-model map."""
import hashlib,json,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from scipy.signal import fftconvolve
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;d=Path(sys.argv[1]);files={'T50kpc.fits':'ad491b8e9df67889f1e9ee8f3e9f323052698705ca553c8875e3b7d0262bd124','T50kpcSUB.fits':'d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de','compact-model.fits':'3791a6d8d8e34c2f2e23c6fbbe96486f1331d23abf5e9ce81b86cdc575d7c03e'}
images={};heads={};world={}
for n,sha in files.items():
 f=d/n
 if hashlib.sha256(f.read_bytes()).hexdigest()!=sha:raise ValueError('Unexpected input hash')
 with fits.open(f) as hd:
  heads[n]=hd[0].header.copy();images[n]=np.squeeze(hd[0].data).astype(float)
 if images[n].ndim!=2 or heads[n].get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected FITS unit')
 with warnings.catch_warnings():warnings.simplefilter('ignore');world[n]=WCS(heads[n]).celestial
shape=images['T50kpc.fits'].shape
assert all(v.shape==shape for v in images.values())
w=world['T50kpc.fits']; points=np.array([100,808,1500]);sky=w.pixel_to_world(points,points)
for z in world.values():
 x,y=z.world_to_pixel(sky);assert max(np.max(np.abs(x-points)),np.max(np.abs(y-points)))<1e-5
h= heads['T50kpc.fits']; sub=heads['T50kpcSUB.fits']; hm=heads['compact-model.fits']
for k in ('BMAJ','BMIN','BPA'): assert np.isclose(h[k],sub[k],rtol=1e-6,atol=2e-5 if k=='BPA' else 1e-9)
def cov(q):
 t=np.deg2rad(q['BPA']);a=np.array([np.sin(t),np.cos(t)]);b=np.array([np.cos(t),-np.sin(t)])
 return (q['BMAJ']**2*np.outer(a,a)+q['BMIN']**2*np.outer(b,b))/(8*np.log(2))
kern=cov(h)-cov(hm)
if np.linalg.eigvalsh(kern).min()<=0:raise ValueError('Beam cannot be matched')
J=w.pixel_scale_matrix;inv=np.linalg.inv(J);kp=inv@kern@inv.T;half=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(kp).max())))
y,x=np.mgrid[-half:half+1,-half:half+1]; xy=np.stack([x,y],axis=-1);kernel=np.exp(-.5*np.einsum('...i,ij,...j->...',xy,np.linalg.inv(kp),xy));kernel/=kernel.sum()
real=np.einsum('n,ni,nj->ij',kernel.ravel(),xy.reshape(-1,2),xy.reshape(-1,2));assert np.allclose(real,kp,rtol=1e-5,atol=1e-5)
model=images['compact-model.fits']; valid=np.isfinite(model); coverage=fftconvolve(valid.astype(float),kernel,mode='same'); ratio=h['BMAJ']*h['BMIN']/(hm['BMAJ']*hm['BMIN'])
matched=fftconvolve(np.where(valid,model,0),kernel,mode='same')*ratio*1000;matched[coverage<.999]=np.nan
diff=(images['T50kpc.fits']-images['T50kpcSUB.fits'])*1000
prior=json.loads((p.parent/'macs1752-difference-localization'/'summary.json').read_text());coord=SkyCoord(*prior['peak_position_deg'],unit='deg'); cx,cy=w.world_to_pixel(coord); yy,xx=np.indices(shape);region=(np.hypot(xx-cx,yy-cy)*1.5<=30)&np.isfinite(diff)&np.isfinite(matched)
if region.sum()<100:raise ValueError('Not enough finite pixels')
cor=float(np.corrcoef(diff[region],matched[region])[0,1]); peak=np.unravel_index(np.argmax(np.where(region,matched,-np.inf)),shape);pc=w.pixel_to_world(peak[1],peak[0]); offset=pc.separation(coord).arcsec
summary={'comparison_region_radius_arcsec':30,'pixels':int(region.sum()),'pixel_pearson_r':cor,'model_peak_offset_from_difference_peak_arcsec':offset,'model_peak_mjy_per_target_beam':float(matched[peak]),'difference_peak_mjy_per_beam':prior['peak_positive_difference_mjy_per_beam'],'peak_amplitude_ratio_difference_to_smoothed_model':prior['peak_positive_difference_mjy_per_beam']/float(matched[peak]),'beam_area_ratio':ratio,'warning':'Same survey products and correlated pixels; Gaussian beam approximation; nominal model data semantics unverified. Correlation is descriptive, not significance or evidence of a physical source identity.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,axs=plt.subplots(1,2,figsize=(9,4));r=35;ix,iy=round(float(cx)),round(float(cy));sl=np.s_[iy-r:iy+r+1,ix-r:ix+r+1]
for ax,arr,title in zip(axs,(diff,matched),('T50 − T50SUB','Gaussian-smoothed compact-model')):
 im=ax.imshow(arr[sl],origin='lower',cmap='inferno',vmin=-.2,vmax=12);ax.scatter([r],[r],marker='+',color='cyan',label='Difference peak');ax.set_title(title);ax.set_xlabel('Pixel x (1.5″ each)');ax.set_ylabel('Pixel y (1.5″ each)')
fig.colorbar(im,ax=axs,label='mJy / target beam',fraction=.03,pad=.02);fig.suptitle('MACS J1752: local image products');fig.text(.5,.01,'Same observations; model representation and subtraction details not independently verified.',ha='center',fontsize=8);fig.subplots_adjust(bottom=.17,top=.85,right=.88,wspace=.3);fig.savefig(p/'model-comparison.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
