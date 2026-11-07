#!/usr/bin/env python3
"""Spatial holdout evaluation of two fixed model conventions."""
import json,runpy,sys
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parent;folder=sys.argv[1]
sys.argv=[str(p.parent/'macs1752-model-normalization'/'analyze.py'),folder]
s=runpy.run_path(sys.argv[0]);preds={'restored_beam':s['predA'],'unconvolved_components':s['predB']};diff=s['diff'];x=s['xx'];y=s['yy'];cx=s['cx'];cy=s['cy'];scale=float(s['scale'][0]);r=np.hypot(x-cx,y-cy)*scale
# Split is fixed before inspecting this test's output. The 45 arcsec gap reduces direct overlap with the fitting region.
valid=np.isfinite(diff)&np.isfinite(preds['restored_beam'])&np.isfinite(preds['unconvolved_components'])&np.isfinite(s['a']['compact-model.fits'])
all_area=valid&(r>=45)&(r<=240)
mask=all_area&(preds['unconvolved_components']>.5)
if mask.sum()<100: raise ValueError('Insufficient model-selected pixels in spatial holdout')
def metrics(p,sel):
 err=p[sel]-diff[sel]; return {'rms_residual_mjy_per_beam':float(np.sqrt(np.mean(err**2))),'median_absolute_residual_mjy_per_beam':float(np.median(abs(err))),'pixel_correlation':float(np.corrcoef(p[sel],diff[sel])[0,1])}
out={'region':'45 to 240 arcsec from previously selected difference peak','selection':'fixed unconvolved-components predicted brightness > 0.5 mJy/target beam','selected_pixels':int(mask.sum()),'restored_beam':metrics(preds['restored_beam'],mask),'unconvolved_components':metrics(preds['unconvolved_components'],mask),'all_finite_pixels':int(all_area.sum()),'all_finite_restored_beam':metrics(preds['restored_beam'],all_area),'all_finite_unconvolved_components':metrics(preds['unconvolved_components'],all_area),'limitation':'Spatial holdout from same image and model, correlated pixels; selection conditions on one hypothesis; no independent observation or statistical significance.'}
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
