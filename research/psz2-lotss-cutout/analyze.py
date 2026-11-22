#!/usr/bin/env python3
"""Place catalog coordinates on the pinned LOFAR image and test redshift conversion."""
import csv, hashlib, json, sys
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
p=Path(__file__).resolve().parent
manifest=json.loads((p/'manifest.json').read_text())
def load_checked(arg, digest):
    path=Path(arg)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest: raise ValueError('Input SHA-256 mismatch: '+path.name)
    return path
image=load_checked(sys.argv[1],manifest['cutout_sha256'])
table=load_checked(sys.argv[2],manifest['catalog_sha256'])
lines=table.read_text().splitlines(); i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'))
rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'))
hits={r['Pos'].strip():r for r in rows if r['Name'].strip()=='PSZ2 G181.06+48.47'}
if set(hits)!={'N','S'}: raise ValueError('Unexpected source match')
coords={k:SkyCoord(float(v['RAJ2000'])*u.deg,float(v['DEJ2000'])*u.deg) for k,v in hits.items()}
with fits.open(image) as hdul:
    hdr=hdul[0].header; data=np.array(hdul[0].data); w=WCS(hdr).celestial
if data.ndim!=2 or hdr.get('BUNIT','').upper()!='JY/BEAM': raise ValueError('Unexpected image dimensions or units')
pixels={k:w.world_to_pixel(c) for k,c in coords.items()}
if not all(0<=x<data.shape[1] and 0<=y<data.shape[0] for x,y in pixels.values()): raise ValueError('Catalog position outside cutout')
sep=coords['N'].separation(coords['S']).arcmin
cosmo=FlatLambdaCDM(H0=70,Om0=.3)
distances={str(z):float(sep*cosmo.kpc_proper_per_arcmin(z).value) for z in (.240,.234)}
summary={'cutout_shape_pixels':list(data.shape),'beam_fwhm_arcsec':[hdr['BMAJ']*3600,hdr['BMIN']*3600],'frequency_hz':hdr.get('RESTFRQ'),'catalog_positions_pixels_xy':{k:[float(x),float(y)] for k,(x,y) in pixels.items()},'coordinate_separation_arcmin':float(sep),'assumed_cosmology':'flat LCDM H0=70 km/s/Mpc Om0=0.3','separation_kpc_by_redshift':distances,'catalog_separation_kpc':2694,'catalog_separation_error_kpc':39,'warning':'Coordinate-based conversion uses rounded catalog coordinates and illustrative cosmology; no image-based centroid, flux, shock, or lensing inference.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig=plt.figure(figsize=(7.3,6.5));ax=fig.add_subplot(111,projection=w)
im=ax.imshow(data*1000,origin='lower',cmap='magma',norm=AsinhNorm(linear_width=.15,vmin=-.3,vmax=8))
for k,(x,y) in pixels.items(): ax.scatter([x],[y],marker='+',s=160,c='#3be4f5',linewidths=2);ax.annotate(k,(x,y),xytext=(8,8),textcoords='offset points',color='#3be4f5',fontsize=10)
ax.set_xlabel('Right ascension (ICRS)');ax.set_ylabel('Declination (ICRS)');ax.set_title('LoTSS DR2: PSZ2 G181.06+48.47');fig.colorbar(im,ax=ax,pad=.02,label='Radio brightness (mJy/beam)',ticks=[-.2,0,.2,1,5],format='%g')
fig.text(.5,.01,'Crosses: published catalog coordinates; field includes compact sources.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.035,1,1));fig.savefig(p/'lotss-cutout.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
