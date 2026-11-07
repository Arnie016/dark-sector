#!/usr/bin/env python3
"""Independent NumPy-FFT and explicit bilinear PSZ2 position replay."""
import csv,hashlib,json,math,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

out=Path(__file__).resolve().parent;root=out.parent;folder=Path(sys.argv[1]);cat=Path(sys.argv[2]);oldpath=root/'two-cluster-physical-beam'/'variants.csv'
cat_digest='4a46302883b9308a771eb2ebf914f8b0a22a22a10f6280f33477568689d70db9'
if hashlib.sha256(cat.read_bytes()).hexdigest()!=cat_digest:raise ValueError('Catalog digest mismatch')
lines=cat.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'));table=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'));hits={r['Pos'].strip():r for r in table if r['Name'].strip()=='PSZ2 G181.06+48.47'}
if set(hits)!={'N','S'}:raise ValueError('Catalog identity mismatch')
positions={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()};scale=FlatLambdaCDM(H0=70,Om0=.3).kpc_proper_per_arcmin(.234).value/60;target=135/scale/3600
files={'T50':('PSZ2G181.06+48.47T50kpc.fits','d08c263b83712bdc40b13357ef297ce6e389437d666aee870fdf68f8489ce5b4'),'T50SUB':('PSZ2G181.06+48.47T50kpcSUB.fits','021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6')}
# Linear convolution using zero-padded NumPy real FFTs and explicit same crop.
def linear_same(image,kernel):
 shape=tuple(a+b-1 for a,b in zip(image.shape,kernel.shape));result=np.fft.irfftn(np.fft.rfftn(image,s=shape,axes=(0,1))*np.fft.rfftn(kernel,s=shape,axes=(0,1)),s=shape,axes=(0,1));start=((kernel.shape[0]-1)//2,(kernel.shape[1]-1)//2)
 return result[start[0]:start[0]+image.shape[0],start[1]:start[1]+image.shape[1]]
# Test the independent convolution on an impulse and a tiny directly summed example.
delta=np.zeros((9,9));delta[4,4]=1;test=np.arange(9,dtype=float).reshape(3,3);assert np.allclose(linear_same(delta,test)[3:6,3:6],test,atol=1e-12)
small=np.arange(20,dtype=float).reshape(4,5);k=np.array([[0.,1.,0.],[1.,2.,1.],[0.,1.,0.]]);v=linear_same(small,k);padded=np.pad(small,1);direct=np.array([[np.sum(padded[y:y+3,x:x+3]*k[::-1,::-1]) for x in range(5)] for y in range(4)]);assert np.allclose(v,direct,atol=1e-12)
images={};wcs={};hds={}
for name,(filename,digest) in files.items():
 f=folder/filename
 if hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise ValueError('Image digest mismatch')
 with fits.open(f) as hd:a=np.squeeze(hd[0].data).astype(float);head=hd[0].header.copy()
 if a.ndim!=2 or head.get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected FITS')
 with warnings.catch_warnings():warnings.simplefilter('ignore');w=WCS(head).celestial
 angle=np.deg2rad(head['BPA']);Q=np.array([[np.sin(angle),np.cos(angle)],[np.cos(angle),-np.sin(angle)]]);beam=Q@np.diag([head['BMAJ']**2,head['BMIN']**2])@Q.T/(8*np.log(2));target_cov=np.eye(2)*target**2/(8*np.log(2));J=np.linalg.inv(w.pixel_scale_matrix);cov=J@(target_cov-beam)@J.T
 if np.linalg.eigvalsh(cov).min()<=0:raise ValueError('Beam infeasible')
 half=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(cov).max())));yy,xx=np.mgrid[-half:half+1,-half:half+1];inv=np.linalg.inv(cov);kernel=np.exp(-.5*(inv[0,0]*xx**2+2*inv[0,1]*xx*yy+inv[1,1]*yy**2));kernel/=kernel.sum();valid=np.isfinite(a);coverage=linear_same(valid.astype(float),kernel);smoothed=linear_same(np.where(valid,a,0),kernel)*target**2/(head['BMAJ']*head['BMIN'])*1000;smoothed[coverage<.999]=np.nan;images[name]=smoothed;wcs[name]=w;hds[name]=head
# Explicit bilinear interpolation; output points outside the source grid are NaN.
Y,X=np.indices(images['T50SUB'].shape);world=wcs['T50SUB'].pixel_to_world(X,Y);xf,yf=wcs['T50'].world_to_pixel(world);valid=np.isfinite(xf)&np.isfinite(yf)&(xf>=0)&(yf>=0)&(xf<=images['T50'].shape[1]-1)&(yf<=images['T50'].shape[0]-1)
x0=np.floor(np.where(valid,xf,0)).astype(int);y0=np.floor(np.where(valid,yf,0)).astype(int);x1=np.minimum(x0+1,images['T50'].shape[1]-1);y1=np.minimum(y0+1,images['T50'].shape[0]-1);fx=xf-x0;fy=yf-y0;src=images['T50'];sample=(1-fy)*((1-fx)*src[y0,x0]+fx*src[y0,x1])+fy*((1-fx)*src[y1,x0]+fx*src[y1,x1]);sample[~valid]=np.nan
paired={'T50':sample,'T50SUB':images['T50SUB']};common=np.isfinite(sample)&np.isfinite(images['T50SUB']);scales=np.sqrt(np.sum(wcs['T50SUB'].pixel_scale_matrix**2,axis=0))*3600
if not np.allclose(scales,[2,2],rtol=1e-4):raise ValueError('Pixel scale mismatch')
old=list(csv.DictReader(oldpath.open()));results=[]
for radius in (300,450,600):
 for threshold in (.1,.2,.3):
  centers={im:{} for im in paired};input_counts={}
  for im,arr in paired.items():
   for relic,pos in positions.items():
    x,y=wcs['T50SUB'].world_to_pixel(pos);rp=radius/scale/scales[0]
    if min(x,y,X.shape[1]-1-x,X.shape[0]-1-y)<rp:raise ValueError('Aperture clipped')
    circle=np.hypot(X-x,Y-y)<=rp
    if (circle&common).sum()/circle.sum()<.99:raise ValueError('Insufficient common coverage')
    mask=circle&common&(arr>threshold);indices=np.flatnonzero(mask);values=arr.ravel()[indices];n=math.ceil(.1*len(indices));pick=np.argsort(values,kind='stable')[-n:];ys,xs=np.unravel_index(indices[pick],arr.shape);c=wcs['T50SUB'].pixel_to_world(np.average(xs,weights=values[pick]),np.average(ys,weights=values[pick]));centers[im][relic]=c;input_counts[im,relic]=(len(indices),n)
  separation={im:centers[im]['N'].separation(centers[im]['S']).arcsec for im in paired};delta=(separation['T50']-separation['T50SUB'])*scale
  for im in paired:
   for relic in positions:
    prior=[r for r in old if r['cluster']=='PSZ2 G181' and int(r['radius_kpc'])==radius and float(r['threshold_mjy_per_beam'])==threshold and r['image']==im and r['relic']==relic]
    if len(prior)!=1:raise ValueError('Missing prior row')
    r=prior[0];c=centers[im][relic];prev=SkyCoord(float(r['ra_deg'])*u.deg,float(r['dec_deg'])*u.deg,frame=c.frame.replicate_without_data());eligible,selected=input_counts[im,relic]
    results.append({'radius_kpc':radius,'threshold_mjy_per_beam':threshold,'image':im,'relic':relic,'eligible':eligible,'selected':selected,'eligible_difference':eligible-int(r['eligible_pixels']),'selected_difference':selected-int(r['selected_pixels']),'position_difference_arcsec':float(c.separation(prev).arcsec),'pair_difference_delta_kpc':float(delta-float(r['pair_difference_kpc']))})
if max(abs(r['eligible_difference']) for r in results) or max(abs(r['selected_difference']) for r in results):raise ValueError('Selection count mismatch')
maxpos=max(r['position_difference_arcsec'] for r in results);maxpair=max(abs(r['pair_difference_delta_kpc']) for r in results)
if maxpos>1e-5 or maxpair>1e-4:raise ValueError('Position or pair disagreement')
with (out/'comparison.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(results[0]),lineterminator='\n');wr.writeheader();wr.writerows(results)
summary={'prior_variants_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),'catalog_sha256':cat_digest,'inputs_sha256':{k:v[1] for k,v in files.items()},'configurations':9,'rows':len(results),'max_abs_position_difference_arcsec':maxpos,'max_abs_pair_difference_kpc':maxpair,'eligible_and_selected_count_differences':0,'independent_components':'NumPy zero-padded FFT convolution and explicit bilinear interpolation; direct convolution and impulse checks','shared_components':'Astropy WCS, FITS data, cosmology and scientific assumptions; same post-hoc masks, ranking rules and beam approximation','limitations':'Computational reproduction of one field, not independent observations, a verification of source reduction or transfer functions, uncertainty, or a merger-clock validation.'}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
