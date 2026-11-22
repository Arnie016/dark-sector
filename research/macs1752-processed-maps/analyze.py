#!/usr/bin/env python3
"""Validate two official processed maps and show published catalog positions."""
import csv,hashlib,json,sys
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import AsinhNorm
p=Path(__file__).resolve().parent
m=json.loads((p/'manifest.json').read_text())
def checked(path, digest):
    p=Path(path)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=digest: raise ValueError('Input digest mismatch')
    return p
folder=Path(sys.argv[1]); catalog=checked(sys.argv[2],m['catalog_sha256'])
lines=catalog.read_text().splitlines(); start=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'))
rows=list(csv.DictReader([lines[start]]+[s for s in lines[start+3:] if s.strip()],delimiter='\t'))
hits={r['Pos'].strip():r for r in rows if r['Name'].strip()=='PSZ2 G071.21+28.86'}
assert set(hits)=={'N','S'}
coords={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()}
fig=plt.figure(figsize=(12,5.4)); results={}
for index,(name,digest) in enumerate(m['selected'].items()):
 f=checked(folder/name,digest)
 with fits.open(f) as h:
  head=h[0].header; data=np.squeeze(h[0].data).copy(); w=WCS(head).celestial
 if data.ndim!=2 or head.get('BUNIT','').upper()!='JY/BEAM': raise ValueError('Unexpected units or dimensions')
 xy={k:w.world_to_pixel(c) for k,c in coords.items()}
 for x,y in xy.values():
  if not (0<=x<data.shape[1] and 0<=y<data.shape[0] and np.isfinite(data[round(float(y)),round(float(x))])): raise ValueError('Coordinates not in finite coverage')
 results[name]={'shape':list(data.shape),'beam_fwhm_arcsec':[head['BMAJ']*3600,head['BMIN']*3600], 'positions_pixels_xy':{k:[float(v) for v in xy0] for k,xy0 in xy.items()}}
 ax=fig.add_subplot(1,2,index+1,projection=w); ax.imshow(data*1000,origin='lower',cmap='magma',norm=AsinhNorm(linear_width=.2,vmin=-.3,vmax=8))
 for k,(x,y) in xy.items(): ax.scatter([x],[y],marker='+',color='cyan',s=110);ax.annotate(k,(x,y),xytext=(6,6),textcoords='offset points',color='cyan')
 ax.set(xlabel='Right ascension (ICRS)',ylabel='Declination (ICRS)',title=name.replace('SUB.fits',''))
fig.suptitle('MACS J1752: source-subtracted radio maps');fig.text(.5,.01,'Markers: published catalog positions; colors show brightness with common display stretch (mJy/beam).',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.04,1,.95));fig.savefig(p/'processed-maps.png',dpi=150);plt.close(fig)
(p/'summary.json').write_text(json.dumps({'maps':results,'warning':'Images have different beams; plotted catalog positions are not measurements of shocks or image centroids.'},indent=2)+'\n')
print(json.dumps(results,indent=2))
