#!/usr/bin/env python3
"""Illustrative dependence on artificial masks; not an independent relic measurement."""
import csv,hashlib,json,math,sys,warnings
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
p=Path(__file__).resolve().parent;m=json.loads((p.parent/'macs1752-processed-maps'/'manifest.json').read_text());image=Path(sys.argv[1]);cat=Path(sys.argv[2])
for f,key in [(image,m['selected']['T50kpcSUB.fits']),(cat,m['catalog_sha256'])]:
 if hashlib.sha256(f.read_bytes()).hexdigest()!=key:raise ValueError('Input digest mismatch')
lines=cat.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'))
rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'))
hits={r['Pos'].strip():r for r in rows if r['Name'].strip()=='PSZ2 G071.21+28.86'}
if set(hits)!={'N','S'}:raise ValueError('Unexpected catalog match')
coords={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()}
with fits.open(image) as f: data=np.squeeze(f[0].data).copy()*1000;header=f[0].header.copy()
if data.ndim!=2 or header.get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected input')
with warnings.catch_warnings(record=True) as warn:
 warnings.simplefilter('always');w=WCS(header).celestial
scale=abs(header['CDELT1'])*3600
if not np.isclose(scale,abs(header['CDELT2'])*3600):raise ValueError('Unequal pixel scale')
pixels={k:tuple(float(v) for v in w.world_to_pixel(c)) for k,c in coords.items()};yy,xx=np.indices(data.shape)
refsep=coords['N'].separation(coords['S']);cosmo=FlatLambdaCDM(H0=70,Om0=.3);kpcperarcsec=cosmo.kpc_proper_per_arcmin(.366).value/60
rows=[]
for radius in (60,90,120):
 for threshold in (.1,.2,.3):
  selected={}
  for k,(x,y) in pixels.items():
   rp=radius/scale
   if min(x,y,data.shape[1]-1-x,data.shape[0]-1-y)<rp:raise ValueError('Circle outside image')
   mask=((xx-x)**2+(yy-y)**2<=rp**2)&np.isfinite(data)&(data>threshold)
   iy,ix=np.where(mask);values=data[mask]
   if len(values)<10:raise ValueError('Too few eligible pixels')
   n=math.ceil(len(values)*.1); idx=np.argsort(values,kind='stable')[-n:];weights=values[idx]
   cx=float(np.average(ix[idx],weights=weights));cy=float(np.average(iy[idx],weights=weights));c=w.pixel_to_world(cx,cy);selected[k]=c
   rows.append({'radius_arcsec':radius,'threshold_mjy_per_beam':threshold,'relic':k,'eligible_pixels':len(values),'brightest_pixels':n,'centroid_ra_deg':float(c.ra.deg),'centroid_dec_deg':float(c.dec.deg),'offset_from_catalog_arcsec':float(c.separation(coords[k]).arcsec)})
  sep=selected['N'].separation(selected['S']);diff_arc=float(sep.arcsec-refsep.arcsec)
  for r in rows[-2:]:r.update({'pair_separation_arcsec':float(sep.arcsec),'delta_pair_kpc_z0366':diff_arc*kpcperarcsec})
with (p/'variants.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
summary={'radio_sha256':m['selected']['T50kpcSUB.fits'],'catalog_sha256':m['catalog_sha256'],'radii_arcsec':[60,90,120],'thresholds_mjy_per_beam':[.1,.2,.3],'estimator':'flux-weighted center of brightest 10% of selected positive pixels in a catalog-centered circle','offset_arcsec_range':{k:[min(r['offset_from_catalog_arcsec'] for r in rows if r['relic']==k),max(r['offset_from_catalog_arcsec'] for r in rows if r['relic']==k)] for k in ('N','S')},'pair_delta_kpc_range':[min(r['delta_pair_kpc_z0366'] for r in rows),max(r['delta_pair_kpc_z0366'] for r in rows)],'limitations':'Invented circular masks and intensity cuts, not author regions or measured noise; catalog-seeded and hence not independent; no calibrated uncertainty or merger age.','wcs_warnings':[str(v.message) for v in warn]}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7,4.6))
for k,color in [('N','#2e7293'),('S','#c46538')]:
 for j,radius in enumerate((60,90,120)):
  q=[r for r in rows if r['relic']==k and r['radius_arcsec']==radius];ax.plot([r['threshold_mjy_per_beam'] for r in q],[r['offset_from_catalog_arcsec'] for r in q],marker=['o','s','^'][j],color=color,linestyle=['-','--',':'][j],label=f'{k}, {radius}″')
ax.axhline(14.73,color='gray',alpha=.6,linestyle=':',label='Beam major FWHM');ax.set(xlabel='Illustrative brightness cut (mJy/beam)',ylabel='Offset from published position (arcsec)',title='Region-choice sensitivity of radio brightness centers');ax.legend(ncol=2,fontsize=8);fig.text(.5,.01,'Artificial catalog-centered masks; not a measurement uncertainty.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.035,1,1));fig.savefig(p/'region-sensitivity.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
