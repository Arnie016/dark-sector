#!/usr/bin/env python3
"""Check actual celestial aperture extent and guard behavior."""
import ast,csv,hashlib,json,sys,warnings
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
p=Path(__file__).resolve().parent;root=p.parent;cat=Path(sys.argv[3]);digest=hashlib.sha256(cat.read_bytes()).hexdigest()
if digest!='4a46302883b9308a771eb2ebf914f8b0a22a22a10f6280f33477568689d70db9':raise ValueError('Unexpected catalog')
lines=cat.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'));rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'));cos=FlatLambdaCDM(H0=70,Om0=.3);out=[]
clusters=[('MACS J1752','PSZ2 G071.21+28.86',.366,Path(sys.argv[1])/'T50kpcSUB.fits','d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de'),('PSZ2 G181','PSZ2 G181.06+48.47',.234,Path(sys.argv[2])/'PSZ2G181.06+48.47T50kpcSUB.fits','021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6')]
for name,catname,z,path,sha in clusters:
 if hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise ValueError('Map hash mismatch')
 with fits.open(path) as h:
  shape=np.squeeze(h[0].data).shape;head=h[0].header.copy()
  with warnings.catch_warnings():warnings.simplefilter('ignore');w=WCS(head).celestial
 scales=np.sqrt(np.sum(w.pixel_scale_matrix**2,axis=0))*3600
 if not np.isclose(scales[0],scales[1],rtol=1e-4):raise ValueError('Non-square pixels')
 radius=(600/(cos.kpc_proper_per_arcmin(z).value/60))/scales[0]
 for row in rows:
  if row['Name'].strip()!=catname:continue
  coord=SkyCoord(float(row['RAJ2000'])*u.deg,float(row['DEJ2000'])*u.deg);x,y=w.world_to_pixel(coord);margin=min(x,y,shape[1]-1-x,shape[0]-1-y)-radius
  if margin<0:raise ValueError('Aperture is clipped')
  out.append({'cluster':name,'relic':row['Pos'].strip(),'image_shape':list(shape),'aperture_radius_pixels':float(radius),'minimum_margin_pixels':float(margin),'minimum_margin_arcsec':float(margin*scales[0])})
if len(out)!=4:raise ValueError('Missing catalog records')
names=['two-cluster-common-beam','two-cluster-physical-beam','psz2-paired-positions','psz2-boundary-ablation','psz2-rotated-mask-sweep','psz2-shared-pixel-test','psz2-bright-fraction-sensitivity','psz2-selection-mechanism']
for name in names:
 tree=ast.parse((root/name/'analyze.py').read_text());checks=[n for n in ast.walk(tree) if isinstance(n,ast.If) and any(isinstance(x,ast.Constant) and x.value=='Aperture extends outside image' for x in ast.walk(n))]
 if len(checks)!=1:raise ValueError('Missing or ambiguous edge guard: '+name)
 expr=compile(ast.Expression(checks[0].test),'<edge guard>','eval');env={'X':np.zeros((100,100)),'x':50.,'y':50.,'cx':50.,'cy':50.,'angular':20.,'radius':20.,'scale':30.,'scales':[1.,1.],'pixscale':[1.,1.]}
 if eval(expr,{},env):raise ValueError('Inside aperture rejected: '+name)
 env.update(x=1.,cx=1.)
 if not eval(expr,{},env):raise ValueError('Clipped aperture accepted: '+name)
result={'catalog_sha256':digest,'apertures':out,'edge_guard_scripts':names,'guard_tests':'Each actual AST condition accepts an interior synthetic aperture and rejects a left-edge clipped one.','limitations':'This verifies image-plane containment and the newly added guards, not survey masks, beam/noise covariance, or physical inference.'}
(p/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
