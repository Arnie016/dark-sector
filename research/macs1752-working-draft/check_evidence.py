#!/usr/bin/env python3
"""Collect pinned summaries for the exploratory MACS J1752 research draft."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent.parent
names=['macs1752-subtraction-sensitivity','macs1752-difference-localization','macs1752-matched-centers','macs1752-model-holdout','macs1752-keck-crossmatch','macs1752-radio-optical-overlay']
inputs={}; summaries={}
for name in names:
 p=root/name/'summary.json';raw=p.read_bytes();inputs[str(p.relative_to(root.parent))]=hashlib.sha256(raw).hexdigest();summaries[name]=json.loads(raw)
s=summaries['macs1752-subtraction-sensitivity'];m=summaries['macs1752-matched-centers'];d=summaries['macs1752-difference-localization'];k=summaries['macs1752-keck-crossmatch'];o=summaries['macs1752-radio-optical-overlay'];h=summaries['macs1752-model-holdout']
assert s['configurations']==m['configurations']==9
assert d['prior_center_difference_arcsec']>15 and d['ablated_center_difference_arcsec']<.2
assert k['optical_separation_arcsec']<.1 and abs(k['z_spec']-.3708639)<1e-9
assert o['positions']['Keck galaxy']['offset_from_peak_arcsec']<4
assert h['all_finite_unconvolved_components']['rms_residual_mjy_per_beam'] < h['all_finite_restored_beam']['rms_residual_mjy_per_beam']
out={'input_summary_sha256':inputs,'same_beam_south_center_difference_range_arcsec':s['center_delta_arcsec']['S'],'same_beam_pair_difference_range_arcsec':s['pair_delta_arcsec'],'ablation_before_arcsec':d['prior_center_difference_arcsec'],'ablation_after_arcsec':d['ablated_center_difference_arcsec'],'matched_beam_pair_difference_range_arcsec':m['signed_pair_separation_difference_arcsec'],'keck_optical_offset_arcsec':k['optical_separation_arcsec'],'keck_galaxy_peak_offset_arcsec':o['positions']['Keck galaxy']['offset_from_peak_arcsec'],'keck_z':k['z_spec'],'holdout_all_pixel_rms_restored':h['all_finite_restored_beam']['rms_residual_mjy_per_beam'],'holdout_all_pixel_rms_component':h['all_finite_unconvolved_components']['rms_residual_mjy_per_beam'],'limitations':'Derived summary consistency only; not independent verification, publication readiness, or a measurement of merger-age bias.'}
(root/'macs1752-working-draft'/'evidence.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
