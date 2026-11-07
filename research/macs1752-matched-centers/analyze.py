#!/usr/bin/env python3
"""Paired mask sensitivity on two beam-matched images, not an uncertainty."""
import csv,json,math,runpy,sys
from pathlib import Path
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
folder=sys.argv[1]
# Reuse the existing validated pipeline; it also regenerates its own figure and summary.
sys.argv=[str(p.parent/'macs1752-beam-match'/'analyze.py'),folder]
state=runpy.run_path(sys.argv[0])
w=state['wb']; images={'matched_T50':state['matched']*1000,'T100':state['b']*1000}
coords={'N':SkyCoord(268.0816*u.deg,44.7043*u.deg),'S':SkyCoord(267.9735*u.deg,44.6313*u.deg)}
y,x=np.indices(images['T100'].shape); pix={k:w.world_to_pixel(c) for k,c in coords.items()}
rows=[]
for radius in (60,90,120):
 for cut in (.1,.2,.3):
  centers={}
  for image_name,img in images.items():
   centers[image_name]={}
   for key,(px,py) in pix.items():
    # Same target grid, region and finite coverage for both images.
    mask=((x-px)**2+(y-py)**2<=(radius/3)**2)&np.isfinite(images['matched_T50'])&np.isfinite(images['T100'])&(img>cut)
    yy,xx=np.where(mask); v=img[mask]
    if len(v)<10: raise ValueError('Too few eligible pixels')
    n=math.ceil(.1*len(v)); idx=np.argsort(v,kind='stable')[-n:]
    cx=np.average(xx[idx],weights=v[idx]);cy=np.average(yy[idx],weights=v[idx])
    c=w.pixel_to_world(cx,cy);centers[image_name][key]=c
    rows.append({'radius_arcsec':radius,'cut_mjy_per_target_beam':cut,'image':image_name,'relic':key,'eligible_pixels':len(v),'brightest_pixels':n,'center_ra_deg':c.ra.deg,'center_dec_deg':c.dec.deg})
  sep={name:centers[name]['N'].separation(centers[name]['S']).arcsec for name in images}
  for r in rows[-4:]:
   r['paired_center_difference_arcsec']=centers['matched_T50'][r['relic']].separation(centers['T100'][r['relic']]).arcsec
   r['paired_separation_difference_arcsec']=sep['matched_T50']-sep['T100']
with (p/'variants.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
result={'configurations':9,'center_difference_arcsec':{key:[min(r['paired_center_difference_arcsec'] for r in rows if r['relic']==key),max(r['paired_center_difference_arcsec'] for r in rows if r['relic']==key)] for key in coords},'signed_pair_separation_difference_arcsec':[min(r['paired_separation_difference_arcsec'] for r in rows),max(r['paired_separation_difference_arcsec'] for r in rows)],'warning':'Same data and catalog-centered illustrative masks; correlated pixels, beam model approximation and different imaging; not a systematic uncertainty or physical result.'}
(p/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7,4.5))
for key,col in [('N','#2e7293'),('S','#c46538')]:
 for j,radius in enumerate((60,90,120)):
  q=[r for r in rows if r['relic']==key and r['radius_arcsec']==radius and r['image']=='T100']
  ax.plot([r['cut_mjy_per_target_beam'] for r in q],[r['paired_center_difference_arcsec'] for r in q],color=col,marker=['o','s','^'][j],linestyle=['-','--',':'][j],label=f'{key}, {radius}″')
ax.set(xlabel='Illustrative brightness cut (mJy/target beam)',ylabel='Difference between paired centers (arcsec)',title='MACS J1752: matched-map position sensitivity');ax.legend(ncol=2,fontsize=8)
fig.text(.5,.01,'Catalog-centered regions; paired maps share observations.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'matched-centers.png',dpi=160);plt.close(fig)
print(json.dumps(result,indent=2))
