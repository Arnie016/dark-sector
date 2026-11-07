#!/usr/bin/env python3
"""Overlay optical and radio positions on the paired 50 kpc survey maps."""
import hashlib,json,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.nddata import Cutout2D
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

here=Path(__file__).resolve().parent; root=here.parent; data=Path(sys.argv[1])
expected={'T50kpc.fits':'ad491b8e9df67889f1e9ee8f3e9f323052698705ca553c8875e3b7d0262bd124','T50kpcSUB.fits':'d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de'}
images={}; wcs={}; headers={}
for name,digest in expected.items():
 p=data/name
 if hashlib.sha256(p.read_bytes()).hexdigest()!=digest: raise ValueError('Unexpected map hash: '+name)
 with fits.open(p) as h:
  headers[name]=h[0].header.copy(); images[name]=np.squeeze(h[0].data).astype(float)*1000
 if images[name].ndim!=2 or headers[name]['BUNIT'].upper()!='JY/BEAM': raise ValueError('Unexpected dimensions or unit')
 with warnings.catch_warnings():
  warnings.simplefilter('ignore');wcs[name]=WCS(headers[name]).celestial
w=wcs['T50kpc.fits']; z=wcs['T50kpcSUB.fits'];shape=images['T50kpc.fits'].shape
if images['T50kpcSUB.fits'].shape!=shape: raise ValueError('Different image dimensions')
test=np.array([100,808,1500]);sky=w.pixel_to_world(test,test);xx,yy=z.world_to_pixel(sky)
if np.max(np.abs(xx-test))>1e-5 or np.max(np.abs(yy-test))>1e-5: raise ValueError('Grid mismatch')
for key in ('BMAJ','BMIN','BPA'):
 if not np.isclose(headers['T50kpc.fits'][key],headers['T50kpcSUB.fits'][key],rtol=1e-6,atol=2e-5 if key=='BPA' else 1e-9): raise ValueError('Beam mismatch')
prev=json.loads((root/'macs1752-difference-localization'/'summary.json').read_text())
peak=SkyCoord(*prev['peak_position_deg'],unit='deg')
positions={'difference peak':peak,'LoTSS radio':SkyCoord(267.99699456543635,44.64713476780804,unit='deg'),'LoTSS optical':SkyCoord(267.9954559,44.649425136309226,unit='deg'),'Keck galaxy':SkyCoord(267.99546900,44.64944397,unit='deg')}
diff=images['T50kpc.fits']-images['T50kpcSUB.fits']; cut=Cutout2D(diff,peak,(120*u.arcsec,120*u.arcsec),wcs=w,mode='strict');sl=cut.slices_original
rows={}
for name,pos in positions.items():
 px,py=w.world_to_pixel(pos);ix,iy=int(np.rint(px)),int(np.rint(py))
 if not (0<=ix<shape[1] and 0<=iy<shape[0]) or not np.isfinite(diff[iy,ix]): raise ValueError('Position outside finite coverage')
 rows[name]={'offset_from_peak_arcsec':float(peak.separation(pos).arcsec),'nearest_pixel_difference_mjy_per_beam':float(diff[iy,ix]),'nearest_pixel_x':ix,'nearest_pixel_y':iy}
fig,axes=plt.subplots(1,3,figsize=(13,4.4))
for ax,arr,title in zip(axes,[images['T50kpc.fits'][sl],images['T50kpcSUB.fits'][sl],diff[sl]],['T50','T50SUB','T50 − T50SUB']):
 im=ax.imshow(arr,origin='lower',cmap='inferno',vmin=-1,vmax=12)
 for name,marker,color in [('difference peak','+','cyan'),('LoTSS radio','x','lime'),('LoTSS optical','o','white'),('Keck galaxy','1','deepskyblue')]:
  px,py=cut.wcs.world_to_pixel(positions[name]);ax.scatter(px,py,marker=marker,s=60,edgecolors=color if marker=='o' else None,facecolors='none' if marker=='o' else color,linewidths=1.4,label=name)
 ax.set_title(title);ax.set_xlabel('Cutout pixel x');ax.set_ylabel('Cutout pixel y')
axes[2].legend(loc='lower left',fontsize=7,framealpha=.8);fig.colorbar(im,ax=axes,location='right',fraction=.025,pad=.02,label='mJy/beam (display clipped)')
fig.suptitle('MACS J1752: paired maps and catalog positions');fig.text(.5,.01,'Related radio products; positions are catalog associations, not proof of physical identity.',ha='center',fontsize=8);fig.subplots_adjust(left=.06,right=.88,bottom=.16,top=.87,wspace=.35);fig.savefig(here/'radio-optical-overlay.png',dpi=180);plt.close(fig)
output={'input_sha256':expected,'beam_arcsec':[headers['T50kpc.fits']['BMAJ']*3600,headers['T50kpc.fits']['BMIN']*3600],'plot_width_arcsec':120,'positions':rows,'warning':'Nearest-pixel samples are correlated with the selected peak, beam-limited, post-hoc diagnostics, not fluxes or evidence of physical association.'}
(here/'summary.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
