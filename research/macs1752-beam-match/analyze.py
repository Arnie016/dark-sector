#!/usr/bin/env python3
"""Match Gaussian restoring beams and grids; descriptive imaging diagnostic."""
import hashlib,json,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.signal import fftconvolve
from scipy.ndimage import map_coordinates
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
manifest=json.loads((p.parent/'macs1752-processed-maps'/'manifest.json').read_text())
folder=Path(sys.argv[1]); items=[]
for name in ('T50kpcSUB.fits','T100kpcSUB.fits'):
 f=folder/name
 if hashlib.sha256(f.read_bytes()).hexdigest()!=manifest['selected'][name]: raise ValueError('Input digest mismatch')
 with fits.open(f) as h:
  head=h[0].header.copy(); arr=np.squeeze(h[0].data).astype(float)
 if arr.ndim!=2 or head.get('BUNIT','').upper()!='JY/BEAM': raise ValueError('Unexpected FITS units')
 with warnings.catch_warnings():
  warnings.simplefilter('ignore'); w=WCS(head).celestial
 items.append((arr,head,w))
a,ha,wa=items[0]; b,hb,wb=items[1]
# Gaussian covariance in east/north tangent-plane degrees; FITS BPA is east of north.
def cov(h):
 t=np.deg2rad(h['BPA']); major=np.array([np.sin(t),np.cos(t)]); minor=np.array([np.cos(t),-np.sin(t)])
 return (h['BMAJ']**2*np.outer(major,major)+h['BMIN']**2*np.outer(minor,minor))/(8*np.log(2))
ca,cb=cov(ha),cov(hb); ck=cb-ca
if np.linalg.eigvalsh(ck).min()<=0: raise ValueError('Target beam cannot be formed by Gaussian smoothing')
# Local celestial WCS pixel scale matrix maps image pixels to east/north tangent-plane degrees.
J=wa.pixel_scale_matrix; inv=np.linalg.inv(J); kp=inv@ck@inv.T
assert np.linalg.eigvalsh(kp).min()>0
half=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(kp).max())))
y,x=np.mgrid[-half:half+1,-half:half+1]; pos=np.stack([x,y],axis=-1)
k=np.exp(-.5*np.einsum('...i,ij,...j->...',pos,np.linalg.inv(kp),pos));k/=k.sum()
assert abs(k.sum()-1)<1e-12
realized=np.einsum('n,ni,nj->ij',k.ravel(),pos.reshape(-1,2),pos.reshape(-1,2))
assert np.allclose(realized,kp,rtol=1e-5,atol=1e-5)
assert np.allclose(np.sqrt(np.sum(wb.pixel_scale_matrix**2,axis=0))*3600,[3,3],rtol=1e-4)
# Jy per source beam to Jy per target beam after normalized convolution.
area_ratio=(hb['BMAJ']*hb['BMIN'])/(ha['BMAJ']*ha['BMIN'])
valid=np.isfinite(a); coverage=fftconvolve(valid.astype(float),k,mode='same')
smooth=fftconvolve(np.where(valid,a,0),k,mode='same')*area_ratio
smooth[coverage<.999]=np.nan
# Interpolate matched source image onto target grid via celestial WCS.
yb,xb=np.indices(b.shape); sky=wb.pixel_to_world(xb,yb); xa,ya=wa.world_to_pixel(sky)
matched=map_coordinates(smooth,[ya,xa],order=1,mode='constant',cval=np.nan)
mask=np.isfinite(matched)&np.isfinite(b)
# Near the two catalog positions, compare pixels inside 120 arcsec; no significance or source masks.
from astropy.coordinates import SkyCoord
import astropy.units as u
coords=[SkyCoord(268.0816*u.deg,44.7043*u.deg),SkyCoord(267.9735*u.deg,44.6313*u.deg)]
regions=np.zeros(b.shape,dtype=bool)
for c in coords:
 x0,y0=wb.world_to_pixel(c); regions|=((xb-x0)**2+(yb-y0)**2)<=(120/3)**2
mask &= regions
if mask.sum()<100: raise ValueError('Insufficient shared coverage')
diff=(matched-b)*1000
stats={'pixels':int(mask.sum()),'median_difference_mjy_per_target_beam':float(np.median(diff[mask])), 'rms_difference_mjy_per_target_beam':float(np.sqrt(np.mean(diff[mask]**2))), 'median_absolute_difference_mjy_per_target_beam':float(np.median(np.abs(diff[mask]))),'beam_area_ratio':area_ratio,'kernel_covariance_eigenvalues_pixels2':np.linalg.eigvalsh(kp).tolist(),'limits':'Gaussian beam approximation and bilinear interpolation only; differing imaging, subtraction and noise remain. Catalog-centered regions and pixels are not independent.'}
(p/'summary.json').write_text(json.dumps(stats,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7,4)); ax.hist(diff[mask],bins=120,range=(-3,3),color='#537aa4');ax.axvline(0,color='black',lw=.8);ax.set(xlabel='Matched 50 kpc image − 100 kpc image (mJy / target beam)',ylabel='Pixel count',title='MACS J1752: matched-beam image differences');fig.text(.5,.01,'Two catalog-centered 120″ regions; correlated pixels, not independent measurements.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.05,1,1));fig.savefig(p/'matched-difference.png',dpi=150);plt.close(fig)
print(json.dumps(stats,indent=2))
