#!/usr/bin/env python3
"""Separate published noise values by actual image product."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from bs4 import BeautifulSoup
from astropy.io import fits
p=Path(__file__).resolve().parent;snapshot,mac,psz=map(Path,sys.argv[1:]);expected={mac:'d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de',psz:'021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6'}
for f,digest in expected.items():
 if hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise ValueError('Unexpected map hash')
soup=BeautifulSoup(snapshot.read_bytes(),'html.parser');out={}
for name,path,expect in [('PSZ2 G071.21+28.86',mac,.101),('PSZ2 G181.06+48.47',psz,.066)]:
 rows=[tr for tr in soup.find_all('tr') if (cells:=tr.find_all(['td','th'])) and cells[0].get_text(' ',strip=True)==name]
 if len(rows)!=1:raise ValueError('Missing or duplicate source')
 tr=rows[0];headers=[x.get_text(' ',strip=True) for x in tr.find_parent('table').find_all('tr')[0].find_all(['td','th'])];values=[x.get_text(' ',strip=True) for x in tr.find_all(['td','th'])]
 if 'rms [mJy/beam]' not in headers or len(headers)!=len(values):raise ValueError('Unexpected table layout')
 rms=float(values[headers.index('rms [mJy/beam]')]);assert np.isclose(rms,expect)
 with fits.open(path) as hd:
  h=hd[0].header;beam=[float(h['BMAJ']*3600),float(h['BMIN']*3600)];shape=list(np.squeeze(hd[0].data).shape)
 out[name]={'published_reference_rms_mjy_per_beam':rms,'twice_reference_rms_mjy_per_beam':2*rms,'reference_description':'Botteon et al. Table 1 reference image, robust=-0.5, no uv taper','archived_t50sub_beam_arcsec':beam,'archived_t50sub_shape':shape,'archived_t50sub_sha256':expected[path]}
summary={'table_snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),'survey_source':'https://lofar-surveys.org/planck_dr2.html','paper_methods_source':'https://arxiv.org/html/2202.11720#S3.SS3','clusters':out,'additional_psz2_paper_values_transcribed_from':'https://arxiv.org/html/2501.08390','psz2_later_lofar_maps':[{'id':'IM1','beam_arcsec':[8.1,5.3],'rms_microjy_per_beam':70},{'id':'IM2','beam_arcsec':[20,20],'rms_microjy_per_beam':200},{'id':'IM3','beam_arcsec':[20,20],'rms_microjy_per_beam':210}], 'warning':'Values are for explicitly described published products, not verified RMS for our archived T50SUB or 135 kpc smoothed maps. Source regions, spatial covariance and correlated noise remain missing.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
