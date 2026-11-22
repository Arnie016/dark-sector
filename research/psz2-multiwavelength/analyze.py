#!/usr/bin/env python3
"""Register published coordinates on processed survey maps; no inference from pixels."""
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
from matplotlib.colors import AsinhNorm
p=Path(__file__).resolve().parent;m=json.loads((p/'manifest.json').read_text())
paths=[Path(v) for v in sys.argv[1:]]
if len(paths)!=3: raise SystemExit('Provide radio FITS, Chandra FITS, VizieR TSV')
for path,key in zip(paths,['radio_sha256','chandra_sha256','catalog_sha256']):
    if hashlib.sha256(path.read_bytes()).hexdigest()!=m[key]: raise ValueError('Digest mismatch: '+path.name)
lines=paths[2].read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'))
rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'))
hits={r['Pos'].strip():r for r in rows if r['Name'].strip()=='PSZ2 G181.06+48.47'}
if set(hits)!={'N','S'}: raise ValueError('Unexpected relic match')
relic={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()}
# Published mass-peak coordinates from Ahn+ Table 1, not BCG coordinates or a reconstructed lensing map.
peaks={'N':SkyCoord(144.8875*u.deg,40.7894*u.deg),'S':SkyCoord(144.8589*u.deg,40.7591*u.deg)}
products=[]
for path in paths[:2]:
    with fits.open(path) as f:
        data=np.squeeze(f[0].data).copy();header=f[0].header.copy()
    if data.ndim!=2: raise ValueError('Expected 2D image')
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always'); w=WCS(header).celestial
    loc={kind+name:tuple(float(v) for v in w.world_to_pixel(c)) for kind,d in [('relic_',relic),('mass_',peaks)] for name,c in d.items()}
    if any(not (0<=x<data.shape[1] and 0<=y<data.shape[0]) for x,y in loc.values()): raise ValueError('Coordinates outside FITS array')
    # An algebraic WCS round trip checks transformations only, not absolute astrometric accuracy.
    errs=[float(c.separation(w.pixel_to_world(*w.world_to_pixel(c))).arcsec) for d in (relic,peaks) for c in d.values()]
    products.append((data,header,w,loc,[str(t.message) for t in caught],max(errs)))
cosmo=FlatLambdaCDM(H0=70,Om0=.3);scale=cosmo.kpc_proper_per_arcmin(.234).value
arc={kind:float(d['N'].separation(d['S']).arcmin) for kind,d in [('relic',relic),('mass',peaks)]}
summary={'redshift':.234,'cosmology':'flat LCDM H0=70 km/s/Mpc, Om0=0.3','separation_arcmin':arc,'separation_kpc':{k:float(v*scale) for k,v in arc.items()},'ratio_mass_to_relic':arc['mass']/arc['relic'],'radio_shape':list(products[0][0].shape),'chandra_shape':list(products[1][0].shape),'chandra_bunit':products[1][1].get('BUNIT'),'wcs_roundtrip_max_arcsec':{k:t[5] for k,t in zip(['radio','chandra'],products)},'wcs_warnings':{k:t[4] for k,t in zip(['radio','chandra'],products)}}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig=plt.figure(figsize=(11,5.5))
for i,(d,h,w,loc,ws,err) in enumerate(products):
    ax=fig.add_subplot(1,2,i+1,projection=w)
    if i==0:
        ax.imshow(d*1000,origin='lower',cmap='magma',norm=AsinhNorm(linear_width=.10,vmin=-.2,vmax=3)); title='Source-subtracted LOFAR'
    else:
        # The file lacks BUNIT. Use only relative display stretch, not calibrated X-ray units.
        hi=np.percentile(d[np.isfinite(d)],99.9);ax.imshow(d,origin='lower',cmap='gray',norm=AsinhNorm(linear_width=max(hi/50,1e-12),vmin=0,vmax=hi));title='Processed Chandra image'
    for kind,marker,color in [('relic','+','#00f5ed'),('mass','x','#84f13a')]:
        for name in ('N','S'):
            x,y=loc[kind+'_'+name];ax.scatter(x,y,marker=marker,c=color,s=80,linewidths=1.5)
    ax.set_title(title);ax.set_xlabel('Right ascension');ax.set_ylabel('Declination')
fig.text(.5,.025,'Cyan +: catalog radio positions   |   Green ×: published lensing mass peaks',ha='center',fontsize=9)
fig.text(.5,.005,'Different maps and scales; markers are published coordinates, not new measurements.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.06,1,1));fig.savefig(p/'radio-xray-mass-peaks.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
