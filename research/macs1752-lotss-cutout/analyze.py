#!/usr/bin/env python3
"""Plot published relic coordinates on a pinned LoTSS DR2 cutout."""
import csv, hashlib, json, sys
from pathlib import Path
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import AsinhNorm
p=Path(__file__).resolve().parent
m=json.loads((p/'manifest.json').read_text())
def verify(name,sha):
    data=Path(name)
    if hashlib.sha256(data.read_bytes()).hexdigest()!=sha: raise ValueError('Unexpected source digest')
    return data
im=verify(sys.argv[1],m['cutout_sha256']); cat=verify(sys.argv[2],m['catalog_sha256'])
lines=cat.read_text().splitlines(); i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'))
rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'))
hits={r['Pos'].strip():r for r in rows if r['Name'].strip()=='PSZ2 G071.21+28.86'}
if set(hits)!={'N','S'}: raise ValueError('Unexpected relic rows')
coord={k:SkyCoord(float(v['RAJ2000'])*u.deg,float(v['DEJ2000'])*u.deg) for k,v in hits.items()}
with fits.open(im) as h:
    hdr=h[0].header; data=np.array(h[0].data); w=WCS(hdr).celestial
if data.ndim!=2 or hdr.get('BUNIT','').upper()!='JY/BEAM': raise ValueError('Unexpected FITS units or shape')
xy={k:w.world_to_pixel(c) for k,c in coord.items()}
for x,y in xy.values():
    if not (0<=x<data.shape[1] and 0<=y<data.shape[0] and np.isfinite(data[round(float(y)),round(float(x))])): raise ValueError('Catalog position outside finite coverage')
summary={'catalog_identifier':'PSZ2 G071.21+28.86','cluster':'MACS J1752.0+4440','image_shape':list(data.shape),'beam_fwhm_arcsec':[hdr['BMAJ']*3600,hdr['BMIN']*3600],'frequency_hz':hdr.get('RESTFRQ'),'coordinates_deg':{k:[v.ra.deg,v.dec.deg] for k,v in coord.items()},'catalog_separation_kpc':int(hits['N']['DRR-RR']),'catalog_separation_error_kpc':int(hits['N']['e_DRR-RR']),'angular_separation_arcmin':coord['N'].separation(coord['S']).arcmin,'caveat':'Markers are published coordinates, not positions measured in this image; no flux, shock, uncertainty, or merger age inferred.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig=plt.figure(figsize=(7,6));ax=fig.add_subplot(111,projection=w)
image=ax.imshow(data*1000,origin='lower',cmap='magma',norm=AsinhNorm(linear_width=.15,vmin=-.3,vmax=8))
for k,(x,y) in xy.items():
    ax.scatter([x],[y],marker='+',s=160,c='#3be4f5',linewidths=2); ax.annotate(k,(x,y),xytext=(8,8),textcoords='offset points',color='#3be4f5')
ax.set(xlabel='Right ascension (ICRS)',ylabel='Declination (ICRS)',title='LoTSS DR2: MACS J1752.0+4440')
fig.colorbar(image,ax=ax,pad=.02,label='Radio brightness (mJy/beam)',ticks=[-.2,0,.2,1,5],format='%g')
fig.text(.5,.01,'Crosses: published catalog coordinates; field includes compact sources.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.035,1,1));fig.savefig(p/'lotss-cutout.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
