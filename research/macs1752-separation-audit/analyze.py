#!/usr/bin/env python3
"""Compare reported lengths and equivalent angles under one published scale."""
import hashlib,json,math
from astropy.cosmology import FlatLambdaCDM
from pathlib import Path
p=Path(__file__).resolve().parent
source=p.parent/'macs1752-lotss-cutout'/'summary.json'
s=json.loads(source.read_text())
angle=s['angular_separation_arcmin']
scale=5.123 # Finner et al. reported kpc/arcsec at z=0.365
coord_length=angle*60*scale
finner_length=2323
implied_angle=finner_length/scale/60
calculated_scale=FlatLambdaCDM(H0=70,Om0=.3,Tcmb0=0).kpc_proper_per_arcmin(.365).value/60
res={'recomputed_scale_kpc_per_arcsec':calculated_scale,'recomputed_length_kpc':angle*60*calculated_scale,'scale_difference_percent':100*(scale/calculated_scale-1),'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'published_coordinate_separation_arcmin':angle,'finner_reported_scale_kpc_per_arcsec':scale,'coordinate_length_using_finner_scale_kpc':coord_length,'finner_reported_axis_projected_length_kpc':finner_length,'finner_length_equivalent_axis_angle_arcmin_at_stated_scale':implied_angle,'catalog_length_kpc':1941,'caveat':'Finner reports an axis-projected separation; Botteon coordinates give a full sky separation. Their inferred angles are different geometric quantities and are not directly comparable.'}
(p/'summary.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
