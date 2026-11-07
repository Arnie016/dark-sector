#!/usr/bin/env python3
"""Read the pinned original FITS header and one bounded, identity-verified row."""
import hashlib,io,json,sys
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
p=Path(__file__).resolve().parent;m=json.loads((p/'manifest.json').read_text())
def verify(path, key, span):
 b=Path(path).read_bytes()
 if hashlib.sha256(b).hexdigest()!=m[key] or len(b)!=span[1]-span[0]+1:raise ValueError('Range digest or length mismatch')
 return b
head=verify(sys.argv[1],'header_sha256',m['header_range']);row=verify(sys.argv[2],'row_sha256',m['row_range'])
f=io.BytesIO(head);h0=fits.Header.fromfile(f);h=fits.Header.fromfile(f);assert f.tell()==len(head)
assert h['NAXIS1']==len(row) and m['row_range'][0]==len(head)+(m['vizier_record_pointer']-1)*len(row)
h['NAXIS2']=1
b=h0.tostring().encode()+h.tostring().encode()+row+bytes((-len(row))%2880)
with fits.open(io.BytesIO(b)) as f:
 d=f[1].data[0]
 if str(d['Source_Name']).strip()!='ILTJ175159.28+443849.6':raise ValueError('Original catalog identity mismatch')
 radio=SkyCoord(float(d['RA'])*u.deg,float(d['DEC'])*u.deg);opt=SkyCoord(float(d['optRA'])*u.deg,float(d['optDec'])*u.deg)
 out={'source_id':str(d['Source_Name']).strip(),'z_best':float(d['z_best']),'z_source':str(d['z_source']).strip(),'zphot':float(d['zphot']),'zphot_err':float(d['zphot_err']),'photo_quality_flag':int(d['flag_qual']),'position_method':str(d['Position_from']).strip(),'optical_radio_separation_arcsec':radio.separation(opt).arcsec,'sdss_spec_available':bool(np.isfinite(d['zspec_sdss'])),'desi_spec_available':bool(np.isfinite(d['z_desi'])),'hetdex_spec_available':bool(np.isfinite(d['z_hetdex'])),'warning':'Catalog-reported optical association and photometric redshift, not verified membership or spectroscopic confirmation; peak-to-radio positional match is not an identity proof.'}
 assert out['z_source']=='Phot' and abs(out['z_best']-out['zphot'])<1e-10
(p/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
