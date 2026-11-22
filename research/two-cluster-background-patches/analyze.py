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
# Candidate patches are fixed from geometry, not selected to minimise noise.
# Excluding catalog-centred circles does not prove source-free sky.
records=[];audit={}
for cluster,folder in zip(clusters,dirs):
 kpcarc=cosmo.kpc_proper_per_arcmin(cluster['z']).value/60;target_arcsec=135/kpcarc;target_fwhm=target_arcsec/3600;target=np.eye(2)*target_fwhm**2/(8*np.log(2))
 hits={r['Pos'].strip():r for r in data if r['Name'].strip()==cluster['catalog']}
 if set(hits)!={'N','S'}:raise ValueError('Missing catalog coordinates')
 coords={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()};images={};wcs={};heads={}
 for name,(filename,digest) in cluster['files'].items():
  path=folder/filename
  if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('Map hash mismatch')
  with fits.open(path) as hd:arr=np.squeeze(hd[0].data).astype(float);head=hd[0].header.copy()
  if arr.ndim!=2 or head.get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected map')
  with warnings.catch_warnings():warnings.simplefilter('ignore');w=WCS(head).celestial
  t=np.deg2rad(head['BPA']);a=np.array([np.sin(t),np.cos(t)]);b=np.array([np.cos(t),-np.sin(t)]);C0=(head['BMAJ']**2*np.outer(a,a)+head['BMIN']**2*np.outer(b,b))/(8*np.log(2));J=np.linalg.inv(w.pixel_scale_matrix);C=J@(target-C0)@J.T
  if np.linalg.eigvalsh(C).min()<=0:raise ValueError('Target beam infeasible')
  half=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(C).max())));y,x=np.mgrid[-half:half+1,-half:half+1];v=np.stack([x,y],axis=-1);K=np.exp(-.5*np.einsum('...i,ij,...j->...',v,np.linalg.inv(C),v));K/=K.sum();actual=np.einsum('n,ni,nj->ij',K.ravel(),v.reshape(-1,2),v.reshape(-1,2))
  if not np.allclose(actual,C,rtol=1e-5,atol=1e-5):raise ValueError('Kernel covariance mismatch')
  valid=np.isfinite(arr);coverage=fftconvolve(valid.astype(float),K,mode='same');sm=fftconvolve(np.where(valid,arr,0),K,mode='same')*(target_fwhm**2/(head['BMAJ']*head['BMIN']))*1000;sm[coverage<.999]=np.nan;images[name]=sm;wcs[name]=w;heads[name]=head
 Y,X=np.indices(images['T50SUB'].shape);sky=wcs['T50SUB'].pixel_to_world(X,Y);xx,yy=wcs['T50'].world_to_pixel(sky);paired={'T50':map_coordinates(images['T50'],[yy,xx],order=1,mode='constant',cval=np.nan),'T50SUB':images['T50SUB']};common=np.isfinite(paired['T50'])&np.isfinite(paired['T50SUB']);scales=np.sqrt(np.sum(wcs['T50SUB'].pixel_scale_matrix**2,axis=0))*3600
 if not np.isclose(scales[0],scales[1],rtol=1e-4):raise ValueError('Non-square grid')
 pixelpos={key:wcs['T50SUB'].world_to_pixel(pos) for key,pos in coords.items()};half=max(1,round(125/kpcarc/scales[0]));side=2*half+1;relic_exclusion_radius=(600/kpcarc)/scales[0];accepted=0
 for gx in (.2,.4,.6,.8):
  for gy in (.2,.4,.6,.8):
   x=round(gx*(X.shape[1]-1));y=round(gy*(X.shape[0]-1));left,right=x-half,x+half+1;bottom,top=y-half,y+half+1
   reason='accepted'
   if left<0 or bottom<0 or right>X.shape[1] or top>X.shape[0]:reason='outside image'
   elif any(np.hypot(x-a,y-b)<relic_exclusion_radius+np.sqrt(2)*half for a,b in pixelpos.values()):reason='near catalog relic aperture'
   elif common[bottom:top,left:right].mean()<.99:reason='insufficient common finite coverage'
   if reason!='accepted':
    records.append({'cluster':cluster['name'],'grid_x':gx,'grid_y':gy,'x':x,'y':y,'side_pixels':side,'status':reason,'product':'','median_mjy_per_beam':'','mad_sigma_mjy_per_beam':'','finite_pixels':0});continue
   accepted+=1
   for name,arr in paired.items():
    vals=arr[bottom:top,left:right][common[bottom:top,left:right]];median=float(np.median(vals));mad=float(1.482602218505602*np.median(np.abs(vals-median)))
    records.append({'cluster':cluster['name'],'grid_x':gx,'grid_y':gy,'x':x,'y':y,'side_pixels':side,'status':reason,'product':name,'median_mjy_per_beam':median,'mad_sigma_mjy_per_beam':mad,'finite_pixels':len(vals)})
 if accepted<4:raise ValueError(f"Too few valid patches for {cluster['name']}: {accepted}")
 audit[cluster['name']]={'target_beam_arcsec':float(target_arcsec),'patch_side_pixels':side,'nominal_patch_side_kpc':float(side*scales[0]*kpcarc),'accepted_patches':accepted,'median_mad_sigma_mjy_per_beam':{name:float(np.median([r['mad_sigma_mjy_per_beam'] for r in records if r['cluster']==cluster['name'] and r['status']=='accepted' and r['product']==name])) for name in paired},'patch_mad_range_mjy_per_beam':{name:[min(r['mad_sigma_mjy_per_beam'] for r in records if r['cluster']==cluster['name'] and r['status']=='accepted' and r['product']==name),max(r['mad_sigma_mjy_per_beam'] for r in records if r['cluster']==cluster['name'] and r['status']=='accepted' and r['product']==name)] for name in paired},'input_sha256':{k:v[1] for k,v in cluster['files'].items()}}
with (outdir/'patches.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');wr.writeheader();wr.writerows(records)
summary={'cosmology':'FlatLambdaCDM H0=70 km/s/Mpc, Om0=0.3, Tcmb0=0','target_beam_kpc':135,'grid_fractions':[.2,.4,.6,.8],'relic_exclusion_kpc':600,'patch_half_width_kpc':125,'clusters':audit,'catalog_sha256':catsha,'warning':'Geometry-selected patches are not demonstrated source-free; MAD-scaled variation is descriptive, not a calibrated RMS, noise significance, uncertainty or source/region model. Correlated pixels and backgrounds persist.'}
(outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8,4.5));labels=[];groups=[]
for name in ('MACS J1752','PSZ2 G181'):
 for product in ('T50','T50SUB'):
  vals=[r['mad_sigma_mjy_per_beam'] for r in records if r['cluster']==name and r['product']==product and r['status']=='accepted'];groups.append(vals);labels.append(name+'\n'+product)
ax.boxplot(groups,tick_labels=labels,showfliers=True);ax.set(ylabel='1.4826 × patch MAD (mJy/target beam)',title='Geometry-selected background-patch variation');fig.text(.5,.01,'Not verified source-free; correlated pixels and non-stationary backgrounds.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(outdir/'patch-variation.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
