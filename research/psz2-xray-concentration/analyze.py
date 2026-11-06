#!/usr/bin/env python3
"""Approximate published X-ray concentration from a derived image, not a likelihood."""
import hashlib,json,sys,warnings
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
from matplotlib.colors import AsinhNorm
from matplotlib.patches import Circle
p=Path(__file__).resolve().parent
m=json.loads((p.parent/'psz2-multiwavelength'/'manifest.json').read_text());source=Path(sys.argv[1])
if hashlib.sha256(source.read_bytes()).hexdigest()!=m['chandra_sha256']: raise ValueError('Input digest mismatch')
with fits.open(source) as f: image=np.asarray(f[0].data,dtype=float);h=f[0].header.copy()
if image.ndim!=2: raise ValueError('Expected 2D image')
with warnings.catch_warnings(record=True) as caught:
 warnings.simplefilter('always');w=WCS(h).celestial
center=SkyCoord(144.8659*u.deg,40.7665*u.deg) # Ahn et al. mass-peak barycenter; used only to constrain peak search
cx,cy=w.world_to_pixel(center);yy,xx=np.indices(image.shape)
scale=FlatLambdaCDM(H0=70,Om0=.3).kpc_proper_per_arcmin(.24).value
pixel_arcmin=abs(h['CDELT1'])*60
if not np.isclose(abs(h['CDELT1']),abs(h['CDELT2']),rtol=1e-6): raise ValueError('Non-square pixels')
kpc_pixel=scale*pixel_arcmin
search=(xx-cx)**2+(yy-cy)**2 <= (500/kpc_pixel)**2
masked=np.where(search & np.isfinite(image),image,-np.inf)
if not np.isfinite(masked).any(): raise ValueError('No finite search pixels')
peak_y,peak_x=np.unravel_index(np.argmax(masked),image.shape)
def ratio(x,y,z):
 kpc_pix=FlatLambdaCDM(H0=70,Om0=.3).kpc_proper_per_arcmin(z).value*pixel_arcmin
 rr=(xx-x)**2+(yy-y)**2
 a=image[rr<(100/kpc_pix)**2];b=image[rr<(500/kpc_pix)**2]
 if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)) or np.sum(b)<=0: raise ValueError('Invalid aperture')
 return float(np.sum(a)/np.sum(b))
pixel_offset=5/(pixel_arcmin*60)
offsets=[('peak',0,0),('east',pixel_offset,0),('west',-pixel_offset,0),('north',0,pixel_offset),('south',0,-pixel_offset)]
values={label:ratio(peak_x+dx,peak_y+dy,.24) for label,dx,dy in offsets}
peakcoord=w.pixel_to_world(peak_x,peak_y)
summary={'source_sha256':m['chandra_sha256'],'peak_pixel_xy':[int(peak_x),int(peak_y)],'peak_ra_dec_deg':[float(peakcoord.ra.deg),float(peakcoord.dec.deg)],'kpc_per_pixel_z024':float(kpc_pixel),'pixel_aperture_ratio_z024':values,'pixel_aperture_ratio_z0234':ratio(peak_x,peak_y,.234),'paper_concentration':0.141,'paper_reported_error':0.0105,'relative_percent_difference':100*(values['peak']/.141-1),'warning':'Exploratory pixel-sum ratio, not a reproduced likelihood or measurement; no independent source mask, exposure map, blank sky, Poisson or systematics model.','wcs_warnings':[str(c.message) for c in caught]}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig=plt.figure(figsize=(7,6));ax=fig.add_subplot(111,projection=w);ax.imshow(image,origin='lower',cmap='gray',norm=AsinhNorm(linear_width=.0002,vmin=0,vmax=.008));ax.scatter(peak_x,peak_y,marker='+',color='cyan',s=100)
for radius,color in [(100,'#66ebff'),(500,'#ffb34d')]: ax.add_patch(Circle((peak_x,peak_y),radius/kpc_pixel,facecolor='none',edgecolor=color,lw=1.5,label=f'{radius} kpc'))
ax.set_xlim(peak_x-190,peak_x+190);ax.set_ylim(peak_y-190,peak_y+190);ax.set(xlabel='Right ascension',ylabel='Declination',title='Illustrative X-ray concentration apertures');ax.legend(loc='upper right');fig.text(.5,.01,'Image scale and center are illustrative; no uncertainty model or flux units inferred.',ha='center',fontsize=8);fig.subplots_adjust(left=.16,right=.94,bottom=.14,top=.90);fig.savefig(p/'concentration-apertures.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
