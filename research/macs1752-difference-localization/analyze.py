#!/usr/bin/env python3
"""Locate differences between two official same-grid image products."""
import csv,hashlib,json,math,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent; folder=Path(sys.argv[1]); inputs={'T50kpc.fits':'ad491b8e9df67889f1e9ee8f3e9f323052698705ca553c8875e3b7d0262bd124','T50kpcSUB.fits':'d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de'}
arrays={}; headers={}; wcs={}
for name,sha in inputs.items():
 f=folder/name
 if hashlib.sha256(f.read_bytes()).hexdigest()!=sha:raise ValueError('Input hash mismatch')
 with fits.open(f) as h:
  headers[name]=h[0].header.copy();arrays[name]=np.squeeze(h[0].data).astype(float)*1000
 if arrays[name].ndim!=2 or headers[name].get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected image')
 with warnings.catch_warnings(): warnings.simplefilter('ignore');wcs[name]=WCS(headers[name]).celestial
assert arrays['T50kpc.fits'].shape==arrays['T50kpcSUB.fits'].shape
w=wcs['T50kpcSUB.fits'];w2=wcs['T50kpc.fits']; testx=np.array([100,808,1500]);testy=np.array([100,808,1500]);x2,y2=w2.world_to_pixel(w.pixel_to_world(testx,testy));assert max(np.max(np.abs(testx-x2)),np.max(np.abs(testy-y2)))<1e-5
h1=headers['T50kpc.fits'];h2=headers['T50kpcSUB.fits'];assert all(np.isclose(h1[k],h2[k],rtol=1e-6,atol=2e-5 if k=='BPA' else 1e-9) for k in ['BMAJ','BMIN','BPA'])
coord=SkyCoord(267.9735*u.deg,44.6313*u.deg);cx,cy=w.world_to_pixel(coord);yy,xx=np.indices(arrays['T50kpc.fits'].shape);r=np.hypot(xx-cx,yy-cy)*1.5
valid=np.isfinite(arrays['T50kpc.fits'])&np.isfinite(arrays['T50kpcSUB.fits'])
diff=arrays['T50kpc.fits']-arrays['T50kpcSUB.fits'];outer=valid&(r<=120);inner=valid&(r<60);ann=valid&(r>=60)&(r<=120)
assert np.all(valid[np.rint(cy).astype(int)-80:np.rint(cy).astype(int)+81,np.rint(cx).astype(int)-80:np.rint(cx).astype(int)+81])
maxy,maxx=np.unravel_index(np.argmax(np.where(outer,diff,-np.inf)),diff.shape);peak=w.pixel_to_world(maxx,maxy)
def stats(m):
 d=diff[m];return {'pixels':len(d),'median_mjy_per_beam':float(np.median(d)),'max_mjy_per_beam':float(np.max(d)),'positive_pixel_sum_mjy_per_beam':float(np.sum(np.maximum(d,0)))}
prior=p.parent/'macs1752-subtraction-sensitivity'/'variants.csv'; prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest()
rows=list(csv.DictReader(prior.open()))
hit=[v for v in rows if v['relic']=='S' and v['radius_arcsec']=='90' and float(v['cut_mjy_per_beam'])==.2]; assert len(hit)==2
centers={v['image']:SkyCoord(float(v['ra_deg'])*u.deg,float(v['dec_deg'])*u.deg) for v in hit}
# Post-hoc ablation: remove a 20-arcsecond disk around the image-difference maximum.
ablated={}
for name in arrays:
 region=valid&(r<=90)&(np.hypot(xx-maxx,yy-maxy)*1.5>20)&(arrays[name]>.2)
 sy,sx=np.where(region);vals=arrays[name][region]
 if len(vals)<10:raise ValueError('Insufficient ablation pixels')
 n=math.ceil(.1*len(vals));ii=np.argsort(vals,kind='stable')[-n:]
 ablated[name]=w.pixel_to_world(np.average(sx[ii],weights=vals[ii]),np.average(sy[ii],weights=vals[ii]))
res={'prior_variants_sha256':prior_hash,'region_radius_arcsec':120,'peak_positive_difference_mjy_per_beam':float(diff[maxy,maxx]),'peak_position_deg':[peak.ra.deg,peak.dec.deg],'peak_offset_from_south_catalog_arcsec':peak.separation(coord).arcsec,'inner_0_60':stats(inner),'annulus_60_120':stats(ann),'displayed_prior_config':'90 arcsec, 0.2 mJy/beam, S','prior_centers_deg':{k:[v.ra.deg,v.dec.deg] for k,v in centers.items()},'prior_center_difference_arcsec':centers['T50'].separation(centers['T50SUB']).arcsec,'posthoc_ablation_radius_arcsec':20,'ablated_center_difference_arcsec':ablated['T50kpc.fits'].separation(ablated['T50kpcSUB.fits']).arcsec,'caveat':'Pixel sum is not flux; differences are between related image products, not proven point sources or uncertainty.'}
(p/'summary.json').write_text(json.dumps(res,indent=2)+'\n')
fig=plt.figure(figsize=(9,7));ax=fig.add_subplot(111,projection=w);lim=80;ix,iy=round(float(cx)),round(float(cy)); crop=diff[iy-lim:iy+lim+1,ix-lim:ix+lim+1]
im=ax.imshow(crop,origin='lower',extent=[ix-lim,ix+lim,iy-lim,iy+lim],cmap='RdBu_r',vmin=-3,vmax=3)
ax.scatter([float(cx)],[float(cy)],marker='+',color='black',s=120,label='Catalog position')
for key,c in centers.items():
 x0,y0=w.world_to_pixel(c);ax.scatter([x0],[y0],marker='x',s=70,label=key+' center')
ax.scatter([maxx],[maxy],marker='o',facecolors='none',edgecolors='yellow',s=70,label='Maximum positive difference')
for rad in (60,90,120):ax.add_patch(plt.Circle((float(cx),float(cy)),rad/1.5,fill=False,edgecolor='gray',lw=.8,ls=':'))
ax.set(xlabel='Right ascension (ICRS)',ylabel='Declination (ICRS)',title='Southern region: T50 − T50SUB');ax.legend(fontsize=7,loc='upper right');fig.colorbar(im,ax=ax,label='Image difference (mJy/beam)',pad=.02);fig.subplots_adjust(left=.13,right=.86,bottom=.13,top=.92);fig.savefig(p/'southern-difference.png',dpi=160);plt.close(fig)
print(json.dumps(res,indent=2))
