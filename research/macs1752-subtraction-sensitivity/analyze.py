#!/usr/bin/env python3
"""Compare catalog-seeded bright-pixel centers across two matched-grid images."""
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
p=Path(__file__).resolve().parent
files={'T50':('T50kpc.fits','ad491b8e9df67889f1e9ee8f3e9f323052698705ca553c8875e3b7d0262bd124'),'T50SUB':('T50kpcSUB.fits','d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de')}
folder=Path(sys.argv[1]); imgs={}; heads={}; wcs={}
for k,(name,sha) in files.items():
 f=folder/name
 if hashlib.sha256(f.read_bytes()).hexdigest()!=sha: raise ValueError('File hash mismatch')
 with fits.open(f) as h: imgs[k]=np.squeeze(h[0].data).astype(float)*1000;heads[k]=h[0].header.copy()
 if imgs[k].ndim!=2 or heads[k].get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected image')
 with warnings.catch_warnings():
  warnings.simplefilter('ignore');wcs[k]=WCS(heads[k]).celestial
assert imgs['T50'].shape==imgs['T50SUB'].shape
for key in ('BMAJ','BMIN','BPA'):
 assert np.isclose(heads['T50'][key],heads['T50SUB'][key],rtol=1e-6,atol=2e-5 if key=='BPA' else 1e-9)
y,x=np.indices(imgs['T50'].shape); w=wcs['T50SUB']
test_x=np.array([100,808,1500]);test_y=np.array([100,808,1500]); sky=w.pixel_to_world(test_x,test_y);check_x,check_y=wcs['T50'].world_to_pixel(sky)
assert max(np.max(np.abs(check_x-test_x)),np.max(np.abs(check_y-test_y)))<1e-5
scale=np.sqrt(np.sum(w.pixel_scale_matrix**2,axis=0))*3600
assert np.allclose(scale,[1.5,1.5],rtol=1e-4)
coords={'N':SkyCoord(268.0816*u.deg,44.7043*u.deg),'S':SkyCoord(267.9735*u.deg,44.6313*u.deg)}
pix={k:w.world_to_pixel(v) for k,v in coords.items()}; common=np.isfinite(imgs['T50'])&np.isfinite(imgs['T50SUB']); rows=[]
for radius in (60,90,120):
 for cut in (.1,.2,.3):
  centers={}
  for name,img in imgs.items():
   centers[name]={}
   for k,(px,py) in pix.items():
    mask=((x-px)**2+(y-py)**2<=(radius/scale[0])**2)&common&(img>cut)
    yy,xx=np.where(mask);v=img[mask]
    if len(v)<10: raise ValueError('Too few pixels')
    n=math.ceil(.1*len(v));z=np.argsort(v,kind='stable')[-n:]
    c=w.pixel_to_world(np.average(xx[z],weights=v[z]),np.average(yy[z],weights=v[z]));centers[name][k]=c
    rows.append({'radius_arcsec':radius,'cut_mjy_per_beam':cut,'image':name,'relic':k,'eligible_pixels':len(v),'brightest_pixels':n,'ra_deg':c.ra.deg,'dec_deg':c.dec.deg})
  sep={k:centers[k]['N'].separation(centers[k]['S']).arcsec for k in imgs}
  for r in rows[-4:]:
   r['paired_center_delta_arcsec']=centers['T50'][r['relic']].separation(centers['T50SUB'][r['relic']]).arcsec
   r['paired_separation_delta_arcsec']=sep['T50']-sep['T50SUB']
with (p/'variants.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
result={'configurations':9,'center_delta_arcsec':{k:[min(r['paired_center_delta_arcsec'] for r in rows if r['relic']==k),max(r['paired_center_delta_arcsec'] for r in rows if r['relic']==k)] for k in coords},'pair_delta_arcsec':[min(r['paired_separation_delta_arcsec'] for r in rows),max(r['paired_separation_delta_arcsec'] for r in rows)],'note':'Catalog-centered illustrative masks and cuts; maps share data. SUB versus non-SUB processing not independently documented. No uncertainty or physical inference.'}
(p/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7,4.5))
for key,color in [('N','#2e7293'),('S','#c46538')]:
 for j,radius in enumerate((60,90,120)):
  q=[r for r in rows if r['relic']==key and r['radius_arcsec']==radius and r['image']=='T50SUB']
  ax.plot([r['cut_mjy_per_beam'] for r in q],[r['paired_center_delta_arcsec'] for r in q],color=color,marker=['o','s','^'][j],linestyle=['-','--',':'][j],label=f'{key}, {radius}″')
ax.set(xlabel='Illustrative brightness cut (mJy/beam)',ylabel='Paired center difference (arcsec)',title='MACS J1752: T50 and T50SUB comparison');ax.legend(ncol=2,fontsize=8)
fig.text(.5,.01,'Catalog-centered regions; maps share observations and similar beam headers.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'subtraction-sensitivity.png',dpi=160);plt.close(fig)
print(json.dumps(result,indent=2))
