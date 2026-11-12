#!/usr/bin/env python3
"""Reconstruct one source-verified original LoTSS v1.2 catalog row."""
import hashlib,io,json,sys
from pathlib import Path
import numpy as np
from astropy.io import fits
p=Path(__file__).resolve().parent;m=json.loads((p/'manifest.json').read_text())
def verify(name,digest,range_):
 b=Path(name).read_bytes()
 if len(b)!=range_[1]-range_[0]+1 or hashlib.sha256(b).hexdigest()!=digest:raise ValueError('Invalid byte range')
 return b
head=verify(sys.argv[1],m['header_sha256'],m['header_stored_range']);row=verify(sys.argv[2],m['row_sha256'],m['row_range'])
f=io.BytesIO(head);h0=fits.Header.fromfile(f);h=fits.Header.fromfile(f)
assert f.tell()==len(head) and h['NAXIS1']==len(row) and len(head)+(m['provisional_record_number']-1)*len(row)==m['row_range'][0]
h['NAXIS2']=1; reconstructed=h0.tostring().encode()+h.tostring().encode()+row+bytes((-len(row))%2880)
with fits.open(io.BytesIO(reconstructed)) as f:
 d=f[1].data[0]
 if str(d['Source_Name']).strip()!=m['identity']:raise ValueError('Source ID mismatch')
 prior=json.loads((p.parent/'macs1752-photoz-provenance'/'summary.json').read_text())
 if prior['source_id']!=m['identity']:raise ValueError('Earlier source mismatch')
 out={'source_id':m['identity'],'version':'v1.2','radio_ra_deg':float(d['RA']),'radio_dec_deg':float(d['DEC']),'z_best':float(d['z_best']),'z_source':str(d['z_source']).strip(),'zphot':float(d['zphot']),'zphot_err':float(d['zphot_err']),'photo_quality_flag':int(d['flag_qual']),'sdss_spectroscopic_available':bool(np.isfinite(d['zspec_sdss'])),'desi_spectroscopic_available':bool(np.isfinite(d['z_desi'])),'hetdex_spectroscopic_available':bool(np.isfinite(d['z_hetdex'])),'v1_1_z_best':prior['z_best'],'v1_1_z_source':prior['z_source'],'warning':'Catalog association and photometric redshift do not establish membership; other spectroscopy or catalogs may exist.'}
 assert out['z_source']=='Phot' and abs(out['zphot']-out['z_best'])<1e-10
 assert abs(out['radio_ra_deg']-267.99699456544)<1e-8 and abs(out['radio_dec_deg']-44.64713476781)<1e-8
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
