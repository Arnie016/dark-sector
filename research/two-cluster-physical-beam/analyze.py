#!/usr/bin/env python3
"""Exploratory paired-map comparison at one angular beam and physical apertures."""
import csv,hashlib,json,math,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
from scipy.signal import fftconvolve
from scipy.ndimage import map_coordinates
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

outdir=Path(__file__).resolve().parent; dirs=[Path(sys.argv[1]),Path(sys.argv[2])];catalog=Path(sys.argv[3])
catsha='4a46302883b9308a771eb2ebf914f8b0a22a22a10f6280f33477568689d70db9'
if hashlib.sha256(catalog.read_bytes()).hexdigest()!=catsha:raise ValueError('Unexpected catalog hash')
lines=catalog.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'));data=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'))
clusters=[{'name':'MACS J1752','catalog':'PSZ2 G071.21+28.86','z':.366,'files':{'T50':('T50kpc.fits','ad491b8e9df67889f1e9ee8f3e9f323052698705ca553c8875e3b7d0262bd124'),'T50SUB':('T50kpcSUB.fits','d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de')}},{'name':'PSZ2 G181','catalog':'PSZ2 G181.06+48.47','z':.234,'files':{'T50':('PSZ2G181.06+48.47T50kpc.fits','d08c263b83712bdc40b13357ef297ce6e389437d666aee870fdf68f8489ce5b4'),'T50SUB':('PSZ2G181.06+48.47T50kpcSUB.fits','021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6')}}]
cosmo=FlatLambdaCDM(H0=70,Om0=.3);results=[];summary={'catalog_sha256':catsha,'cosmology':'FlatLambdaCDM H0=70 km/s/Mpc, Om0=0.3, Tcmb0=0','target_beam_kpc':135,'apertures_kpc':[300,450,600],'thresholds_mjy_per_target_beam':[.1,.2,.3],'clusters':{}}
for cluster,folder in zip(clusters,dirs):
 kpcarc=cosmo.kpc_proper_per_arcmin(cluster['z']).value/60;target_arcsec=135/kpcarc;target_fwhm=target_arcsec/3600;target=np.eye(2)*target_fwhm**2/(8*np.log(2))
 hits={r['Pos'].strip():r for r in data if r['Name'].strip()==cluster['catalog']}
 if set(hits)!={'N','S'}:raise ValueError('Catalog identity mismatch')
 coords={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()};imgs={};heads={};wcs={};smooth={}
 for k,(name,sha) in cluster['files'].items():
  f=folder/name
  if hashlib.sha256(f.read_bytes()).hexdigest()!=sha:raise ValueError('Map hash mismatch: '+name)
  with fits.open(f) as h:imgs[k]=np.squeeze(h[0].data).astype(float);heads[k]=h[0].header.copy()
  if imgs[k].ndim!=2 or heads[k].get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected FITS data')
  with warnings.catch_warnings():warnings.simplefilter('ignore');wcs[k]=WCS(heads[k]).celestial
  h=heads[k];t=np.deg2rad(h['BPA']);a=np.array([np.sin(t),np.cos(t)]);b=np.array([np.cos(t),-np.sin(t)]);C0=(h['BMAJ']**2*np.outer(a,a)+h['BMIN']**2*np.outer(b,b))/(8*np.log(2));J=np.linalg.inv(wcs[k].pixel_scale_matrix);C=J@(target-C0)@J.T
  if np.linalg.eigvalsh(C).min()<=0:raise ValueError('Beam kernel is not positive definite')
  n=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(C).max())));y,x=np.mgrid[-n:n+1,-n:n+1];v=np.stack([x,y],axis=-1);K=np.exp(-.5*np.einsum('...i,ij,...j->...',v,np.linalg.inv(C),v));K/=K.sum();actual=np.einsum('n,ni,nj->ij',K.ravel(),v.reshape(-1,2),v.reshape(-1,2))
  if not np.allclose(actual,C,rtol=1e-5,atol=1e-5):raise ValueError('Kernel covariance mismatch')
  valid=np.isfinite(imgs[k]);coverage=fftconvolve(valid.astype(float),K,mode='same');smooth[k]=fftconvolve(np.where(valid,imgs[k],0),K,mode='same')*(target_fwhm**2/(h['BMAJ']*h['BMIN']))*1000;smooth[k][coverage<.999]=np.nan
 Y,X=np.indices(smooth['T50SUB'].shape);sky=wcs['T50SUB'].pixel_to_world(X,Y);ix,iy=wcs['T50'].world_to_pixel(sky);paired={'T50':map_coordinates(smooth['T50'],[iy,ix],order=1,mode='constant',cval=np.nan),'T50SUB':smooth['T50SUB']};common=np.isfinite(paired['T50'])&np.isfinite(paired['T50SUB']);J=wcs['T50SUB'].pixel_scale_matrix;scales=np.sqrt(np.sum(J**2,axis=0))*3600
 if not np.isclose(scales[0],scales[1],rtol=1e-4):raise ValueError('Non-square pixels')
 pix={k:wcs['T50SUB'].world_to_pixel(v) for k,v in coords.items()}; kpcarc=cosmo.kpc_proper_per_arcmin(cluster['z']).value/60; block=[]
 for radius in (300,450,600):
  angular=radius/kpcarc
  for cut in (.1,.2,.3):
   centers={};sizes={}
   for image,arr in paired.items():
    centers[image]={}
    for key,(cx,cy) in pix.items():
     if min(cx,cy,X.shape[1]-1-cx,X.shape[0]-1-cy) < angular/scales[0]: raise ValueError('Aperture extends outside image')
     circle=np.hypot(X-cx,Y-cy)<=angular/scales[0];coverage=float((circle&common).sum()/circle.sum())
     if coverage<.99:raise ValueError(f"{cluster['name']} {key} insufficient common coverage {coverage:.3f}")
     mask=circle&common&(arr>cut);y,x=np.where(mask);v=arr[mask]
     if len(v)<10:raise ValueError('Too few pixels')
     n=math.ceil(.1*len(v));sel=np.argsort(v,kind='stable')[-n:];centers[image][key]=wcs['T50SUB'].pixel_to_world(np.average(x[sel],weights=v[sel]),np.average(y[sel],weights=v[sel]));sizes[image,key]=(len(v),n,coverage)
   sep={im:centers[im]['N'].separation(centers[im]['S']).arcsec for im in paired}
   for image in paired:
    for key in coords:
     c=centers[image][key];eligible,n,coverage=sizes[image,key];r={'cluster':cluster['name'],'radius_kpc':radius,'radius_arcsec':float(angular),'threshold_mjy_per_beam':cut,'image':image,'relic':key,'eligible_pixels':eligible,'selected_pixels':n,'coverage_fraction':coverage,'ra_deg':float(c.ra.deg),'dec_deg':float(c.dec.deg),'center_difference_arcsec':float(centers['T50'][key].separation(centers['T50SUB'][key]).arcsec),'pair_difference_arcsec':float(sep['T50']-sep['T50SUB']),'pair_difference_kpc':float((sep['T50']-sep['T50SUB'])*kpcarc)};results.append(r);block.append(r)
 if cluster['name']=='PSZ2 G181':
  cx,cy=pix['S'];radius=600/kpcarc;circle=np.hypot(X-cx,Y-cy)<=radius/scales[0];difference=paired['T50']-paired['T50SUB'];region=circle&common
  py,px=np.unravel_index(np.argmax(np.where(region,difference,-np.inf)),difference.shape);peak=wcs['T50SUB'].pixel_to_world(px,py)
  peak_info={'ra_deg':float(peak.ra.deg),'dec_deg':float(peak.dec.deg),'positive_difference_mjy_per_beam':float(difference[py,px]),'offset_south_catalog_arcsec':float(peak.separation(coords['S']).arcsec),'search_radius_kpc':600,'selection':'maximum positive T50 minus T50SUB in southern catalog-centered aperture'}
  summary['psz2_southern_difference_peak']=peak_info
  fig,axes=plt.subplots(1,3,figsize=(11,4));window=180/scales[0];x0=max(0,int(cx-window));x1=min(X.shape[1],int(cx+window)+1);y0=max(0,int(cy-window));y1=min(X.shape[0],int(cy+window)+1)
  for ax,arr,title in zip(axes,[paired['T50'],paired['T50SUB'],difference],['T50','T50SUB','T50 minus T50SUB']):
   im=ax.imshow(arr[y0:y1,x0:x1],origin='lower',cmap='inferno',vmin=-1,vmax=12);ax.scatter(px-x0,py-y0,color='cyan',marker='+',s=80);ax.scatter(cx-x0,cy-y0,facecolors='none',edgecolors='white',s=70);ax.add_patch(plt.Circle((cx-x0,cy-y0),radius/scales[0],fill=False,color='white',ls='--',lw=.8));ax.set_title(title);ax.set_xlabel('Cutout pixel x');ax.set_ylabel('Cutout pixel y')
  fig.colorbar(im,ax=axes,location='right',fraction=.025,label='mJy/target beam (clipped)');fig.suptitle('PSZ2 G181: southern 600 kpc aperture');fig.text(.5,.01,'White circle: catalog position and aperture; cyan plus: post-hoc difference peak.',ha='center',fontsize=8);fig.subplots_adjust(left=.06,right=.88,bottom=.17,top=.86,wspace=.35);fig.savefig(outdir/'psz2-difference.png',dpi=160);plt.close(fig)
 summary['clusters'][cluster['name']]={'z':cluster['z'],'kpc_per_arcsec':float(kpcarc),'beam_fwhm_kpc':135,'beam_fwhm_arcsec':float(target_arcsec),'center_difference_arcsec':{k:[min(r['center_difference_arcsec'] for r in block if r['relic']==k),max(r['center_difference_arcsec'] for r in block if r['relic']==k)] for k in coords},'pair_difference_arcsec':[min(r['pair_difference_arcsec'] for r in block),max(r['pair_difference_arcsec'] for r in block)],'pair_difference_kpc':[min(r['pair_difference_kpc'] for r in block),max(r['pair_difference_kpc'] for r in block)],'min_coverage':min(r['coverage_fraction'] for r in block),'input_sha256':{k:sha for k,(_,sha) in cluster['files'].items()}}
with (outdir/'variants.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(results[0]),lineterminator='\n');wr.writeheader();wr.writerows(results)
summary['caveat']='Post-hoc two-field case study; common nominal physical beam and physical apertures, arbitrary thresholds and regions; no calibrated uncertainty or merger-age inference.'
(outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(7,4.5))
for cluster,color in [('MACS J1752','#b85435'),('PSZ2 G181','#1f7795')]:
 for j,radius in enumerate((300,450,600)):
  q=[r for r in results if r['cluster']==cluster and r['radius_kpc']==radius and r['image']=='T50SUB' and r['relic']=='N'];ax.plot([r['threshold_mjy_per_beam'] for r in q],[r['pair_difference_kpc'] for r in q],color=color,marker=['o','s','^'][j],linestyle=['-','--',':'][j],label=f'{cluster}, {radius} kpc')
ax.axhline(0,color='grey',lw=.8);ax.set(xlabel='Illustrative threshold (mJy / target beam)',ylabel='T50 minus T50SUB pair separation (kpc)',title='Paired-map sensitivity in two cluster fields');ax.legend(ncol=2,fontsize=8);fig.text(.5,.01,'Exploratory choices; shared observations; common 135 kpc nominal beam.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(outdir/'comparison.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
