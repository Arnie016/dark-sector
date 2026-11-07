#!/usr/bin/env python3
"""Post-hoc symmetric map exclusion, PSZ2 G181 600 kpc region."""
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
p=Path(__file__).resolve().parent;folder=Path(sys.argv[1]);cat=Path(sys.argv[2]);priorpath=p.parent/'two-cluster-physical-beam'/'summary.json';prior=json.loads(priorpath.read_text())
files={'T50':('PSZ2G181.06+48.47T50kpc.fits','d08c263b83712bdc40b13357ef297ce6e389437d666aee870fdf68f8489ce5b4'),'T50SUB':('PSZ2G181.06+48.47T50kpcSUB.fits','021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6')}
if hashlib.sha256(cat.read_bytes()).hexdigest()!=prior['catalog_sha256']:raise ValueError('Unexpected catalog')
lines=cat.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'));rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'));hits={r['Pos'].strip():r for r in rows if r['Name'].strip()=='PSZ2 G181.06+48.47'}
if set(hits)!={'N','S'}:raise ValueError('Catalog identity mismatch')
coords={k:SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg) for k,r in hits.items()};scale=FlatLambdaCDM(H0=70,Om0=.3).kpc_proper_per_arcmin(.234).value/60;fwhm=(135/scale)/3600;target=np.eye(2)*fwhm**2/(8*np.log(2));smooth={};w={}
for k,(name,digest) in files.items():
 f=folder/name
 if hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise ValueError('Image hash mismatch')
 with fits.open(f) as h:a=np.squeeze(h[0].data).astype(float);head=h[0].header.copy()
 if a.ndim!=2 or head.get('BUNIT','').upper()!='JY/BEAM':raise ValueError('Unexpected FITS')
 with warnings.catch_warnings():warnings.simplefilter('ignore');w[k]=WCS(head).celestial
 t=np.deg2rad(head['BPA']);e=np.array([np.sin(t),np.cos(t)]);n=np.array([np.cos(t),-np.sin(t)]);cov=(head['BMAJ']**2*np.outer(e,e)+head['BMIN']**2*np.outer(n,n))/(8*np.log(2));inv=np.linalg.inv(w[k].pixel_scale_matrix);C=inv@(target-cov)@inv.T
 if np.linalg.eigvalsh(C).min()<=0:raise ValueError('Invalid target beam')
 r=int(np.ceil(6*np.sqrt(np.linalg.eigvalsh(C).max())));y,x=np.mgrid[-r:r+1,-r:r+1];v=np.stack([x,y],axis=-1);K=np.exp(-.5*np.einsum('...i,ij,...j->...',v,np.linalg.inv(C),v));K/=K.sum();actual=np.einsum('n,ni,nj->ij',K.ravel(),v.reshape(-1,2),v.reshape(-1,2))
 if not np.allclose(actual,C,rtol=1e-5,atol=1e-5):raise ValueError('Kernel covariance')
 valid=np.isfinite(a);coverage=fftconvolve(valid.astype(float),K,mode='same');smooth[k]=fftconvolve(np.where(valid,a,0),K,mode='same')*(fwhm**2/(head['BMAJ']*head['BMIN']))*1000;smooth[k][coverage<.999]=np.nan
Y,X=np.indices(smooth['T50SUB'].shape);sky=w['T50SUB'].pixel_to_world(X,Y);xx,yy=w['T50'].world_to_pixel(sky);images={'T50':map_coordinates(smooth['T50'],[yy,xx],order=1,mode='constant',cval=np.nan),'T50SUB':smooth['T50SUB']};common=np.isfinite(images['T50'])&np.isfinite(images['T50SUB']);J=w['T50SUB'].pixel_scale_matrix;pixscale=np.sqrt(np.sum(J**2,axis=0))*3600
if not np.allclose(pixscale,[2,2],rtol=1e-4):raise ValueError('Pixel scale mismatch')
pixels={k:w['T50SUB'].world_to_pixel(c) for k,c in coords.items()};peakdata=prior['psz2_southern_difference_peak'];peak=SkyCoord(peakdata['ra_deg']*u.deg,peakdata['dec_deg']*u.deg);px,py=w['T50SUB'].world_to_pixel(peak);sx,sy=pixels['S'];cx,cy=2*sx-px,2*sy-py;controls={'peak':(px,py),'reflected':(cx,cy),'rotated_90':(sx-(py-sy),sy+(px-sx)),'rotated_minus90':(sx+(py-sy),sy-(px-sx))}
# Three selection rules share their sky support as specified below. Each map's
# own positive brightness supplies weights for its position estimate.
modes=('independent','shared_eligible_independent_rank','shared_t50_rank','shared_sub_rank');records=[];diagnostics={}
for masked in (False,True):
 exclusion=np.hypot(X-px,Y-py)<=40/pixscale[0] if masked else np.zeros_like(common,dtype=bool)
 centers={mode:{im:{} for im in images} for mode in modes}
 for key,(x,y) in pixels.items():
  circle=(np.hypot(X-x,Y-y)<=(600/scale)/pixscale[0])&common&~exclusion
  if circle.sum()<100:raise ValueError('Insufficient sky support')
  eligible={im:circle&(arr>.2) for im,arr in images.items()};joint=eligible['T50']&eligible['T50SUB']
  if joint.sum()<100:raise ValueError('Too few jointly eligible pixels')
  def brightest(mask,arr):
   ids=np.flatnonzero(mask);n=math.ceil(.1*len(ids));return ids[np.argsort(arr.ravel()[ids],kind='stable')[-n:]]
  independent={im:brightest(eligible[im],arr) for im,arr in images.items()}
  common_rank={im:brightest(joint,arr) for im,arr in images.items()}
  choices={'independent':independent,'shared_eligible_independent_rank':common_rank,'shared_t50_rank':{im:common_rank['T50'] for im in images},'shared_sub_rank':{im:common_rank['T50SUB'] for im in images}}
  for mode in modes:
   for im in images:
    ids=choices[mode][im]; yy,xx=np.unravel_index(ids,images[im].shape);weights=images[im].ravel()[ids]
    if np.any(weights<=0):raise ValueError('Nonpositive position weights')
    centers[mode][im][key]=w['T50SUB'].pixel_to_world(np.average(xx,weights=weights),np.average(yy,weights=weights))
    records.append({'mask':'peak40' if masked else 'none','mode':mode,'image':im,'relic':key,'ra_deg':float(centers[mode][im][key].ra.deg),'dec_deg':float(centers[mode][im][key].dec.deg),'selected_pixels':len(ids),'joint_eligible_pixels':int(joint.sum())})
  diagnostics[f"{'peak40' if masked else 'none'}_{key}"]={'eligible_T50':int(eligible['T50'].sum()),'eligible_T50SUB':int(eligible['T50SUB'].sum()),'joint_eligible':int(joint.sum()),'independent_selected_overlap':len(np.intersect1d(independent['T50'],independent['T50SUB'])),'independent_selected_union':len(np.union1d(independent['T50'],independent['T50SUB'])),'joint_rank_selected_overlap':len(np.intersect1d(common_rank['T50'],common_rank['T50SUB'])),'joint_rank_selected_count':len(common_rank['T50'])}
 for mode in modes:
  separations={im:centers[mode][im]['N'].separation(centers[mode][im]['S']).arcsec for im in images};delta=(separations['T50']-separations['T50SUB'])*scale
  for r in records:
   if r['mask']==('peak40' if masked else 'none') and r['mode']==mode:r['pair_delta_kpc']=float(delta)
old=json.loads((p.parent/'psz2-boundary-ablation'/'summary.json').read_text())
for mask,case in [('none','none_0'),('peak40','peak_40')]:
 r=next(r for r in records if r['mask']==mask and r['mode']=='independent')
 if abs(r['pair_delta_kpc']-old['cases'][case]['pair_delta_kpc'])>1e-6:raise ValueError('Baseline mismatch')
with (p/'variants.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');wr.writeheader();wr.writerows(records)
summary={'target_beam_kpc':135,'aperture_kpc':600,'threshold_mjy_per_beam':.2,'results_kpc':{mask:{mode:next(r['pair_delta_kpc'] for r in records if r['mask']==mask and r['mode']==mode) for mode in modes} for mask in ('none','peak40')},'selection_diagnostics':diagnostics,'warning':'Shared support is exploratory and reference-dependent; separately weighted maps still share observations, and the feature and mask were selected post-hoc. No author-pipeline, uncertainty, or clock inference.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(8,4.5));width=.34;x=np.arange(len(modes))
for offset,mask,color in [(-width/2,'none','#b65739'),(width/2,'peak40','#247693')]:ax.bar(x+offset,[summary['results_kpc'][mask][m] for m in modes],width,label=mask,color=color)
ax.axhline(0,color='gray',lw=.8);ax.set_xticks(x,['Independent','Joint eligibility\nindependent rank','Joint, T50\nshared rank','Joint, SUB\nshared rank'],fontsize=8);ax.set(ylabel='T50 minus T50SUB pair separation (kpc)',title='PSZ2: dependence on selected sky pixels');ax.legend();fig.text(.5,.01,'Each map uses its own brightness weights; masks and rules are exploratory.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'shared-selection.png',dpi=160);plt.close(fig)
print(json.dumps(summary,indent=2))
