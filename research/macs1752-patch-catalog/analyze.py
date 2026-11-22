#!/usr/bin/env python3
"""Inspect a bounded VizieR positional match, without physical identification."""
import csv,hashlib,json,sys
from pathlib import Path
from astropy.coordinates import SkyCoord
import astropy.units as u
p=Path(__file__).resolve().parent;m=json.loads((p/'manifest.json').read_text())
def read(path,digest):
 f=Path(path); data=f.read_bytes()
 if hashlib.sha256(data).hexdigest()!=digest:raise ValueError('Catalog digest mismatch')
 lines=data.decode().splitlines(); i=next(i for i,s in enumerate(lines) if s.startswith('_r\tSource\t'))
 return list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip() and not s.startswith('#')],delimiter='\t'))
a=read(sys.argv[1],m['radio_query_sha256']);b=read(sys.argv[2],m['value_added_query_sha256'])
if len(a)!=1 or len(b)!=1:raise ValueError('Unexpected number of matches')
x,y=a[0],b[0]
if x['Source'].strip()!=y['Source'].strip():raise ValueError('Catalog source ID mismatch')
previous=json.loads((p.parent/'macs1752-difference-localization'/'summary.json').read_text()); ra,dec=previous['peak_position_deg']
peak=SkyCoord(ra*u.deg,dec*u.deg); raw=SkyCoord(float(x['RAJ2000'])*u.deg,float(x['DEJ2000'])*u.deg); va=SkyCoord(float(y['RAJ2000'])*u.deg,float(y['DEJ2000'])*u.deg)
sep=peak.separation(raw).arcsec
if abs(sep-float(x['_r']))>.03:raise ValueError('Reported separation inconsistent')
res={'query_radius_arcsec':20,'radio_catalog_returned_rows':len(a),'source_id':x['Source'].strip(),'separation_from_difference_peak_arcsec':sep,'radio_value_added_coordinate_difference_arcsec':raw.separation(va).arcsec,'radio_catalog_scode':x['SCode'].strip(),'radio_catalog_major_fwhm_arcsec':float(x['Maj']),'radio_catalog_minor_fwhm_arcsec':float(x['Min']),'warning':'Positional association only; same survey data, extended/multiple-component catalog fit; no proof of identity, subtraction mechanism, redshift type, cluster membership or causation.'}
(p/'summary.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
