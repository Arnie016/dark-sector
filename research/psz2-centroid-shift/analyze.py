#!/usr/bin/env python3
"""Check centroid shift using processed Chandra image; no counts-based uncertainty."""
import csv, hashlib, json, sys, warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;manifest=json.loads((p.parent/'psz2-multiwavelength'/'manifest.json').read_text());path=Path(sys.argv[1])
if hashlib.sha256(path.read_bytes()).hexdigest()!=manifest['chandra_sha256']: raise ValueError('Input digest mismatch')
with fits.open(path) as f: image=np.asarray(f[0].data,dtype=float);header=f[0].header.copy()
if image.ndim!=2 or not np.isclose(abs(header['CDELT1']),abs(header['CDELT2']),rtol=1e-6): raise ValueError('Unexpected pixel grid')
with warnings.catch_warnings(record=True) as caught:
 warnings.simplefilter('always');wcs=WCS(header).celestial
ref=SkyCoord(144.8659*u.deg,40.7665*u.deg);x0,y0=wcs.world_to_pixel(ref);yy,xx=np.indices(image.shape)
arcsec_pixel=abs(header['CDELT1'])*3600
kpc_arcsec=FlatLambdaCDM(H0=70,Om0=.3).kpc_proper_per_arcmin(.24).value/60
kpc_pixel=kpc_arcsec*arcsec_pixel
search=(xx-x0)**2+(yy-y0)**2<=(500/kpc_pixel)**2
im=np.where(np.isfinite(image)&search,image,-np.inf)
if not np.isfinite(im).any(): raise ValueError('Empty search')
py,px=np.unravel_index(np.argmax(im),image.shape)
max_arcsec=500/kpc_arcsec
radii=5*np.arange(1,int(max_arcsec//5)+1,dtype=float)
if len(radii)<2: raise ValueError('Insufficient apertures')
r2=(xx-px)**2+(yy-py)**2
out=[]
for radius in radii:
 mask=r2<(radius/arcsec_pixel)**2; vals=image[mask]
 if not np.all(np.isfinite(vals)) or np.sum(vals)<=0: raise ValueError('Invalid aperture data')
 x=float(np.sum(xx[mask]*vals)/np.sum(vals));y=float(np.sum(yy[mask]*vals)/np.sum(vals))
 out.append({'aperture_arcsec':float(radius),'aperture_kpc':float(radius*kpc_arcsec),'centroid_x_pixel':x,'centroid_y_pixel':y,'peak_to_centroid_kpc':float(np.hypot(x-px,y-py)*kpc_pixel)})
with (p/'aperture-centroids.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(out[0]));wr.writeheader();wr.writerows(out)
d=[r['peak_to_centroid_kpc'] for r in out];shift=float(np.std(d,ddof=1)/500)
summary={'chandra_sha256':manifest['chandra_sha256'],'redshift':.24,'peak_pixel_xy':[int(px),int(py)],'number_apertures':len(out),'maximum_aperture_kpc':out[-1]['aperture_kpc'],'shift_from_image':shift,'published_shift':.0695,'published_shift_error':.00304,'difference':shift-.0695,'caution':'Provisional pixel-weighted summary; point source mask, underlying counts, background/exposure products, exact author center, and uncertainty procedure are not independently reproduced.','wcs_warnings':[str(v.message) for v in caught]}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7,4));ax.plot([r['aperture_kpc'] for r in out],d,marker='.',color='#327292');ax.set(xlabel='Aperture radius (kpc)',ylabel='Peak-to-centroid distance (kpc)',title='X-ray centroid offsets at increasing aperture size');ax.grid(alpha=.25);fig.text(.5,.01,'Processed map, illustrative center; no counts-based uncertainty.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.035,1,1));fig.savefig(p/'centroid-apertures.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
