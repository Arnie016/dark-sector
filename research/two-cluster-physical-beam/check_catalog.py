#!/usr/bin/env python3
"""Check the saved cone response against the selected map difference peak."""
import csv,hashlib,json,sys
from pathlib import Path
from astropy.coordinates import SkyCoord
import astropy.units as u
p=Path(__file__).resolve().parent;f=Path(sys.argv[1]);raw=f.read_bytes();digest=hashlib.sha256(raw).hexdigest()
if digest!='048f02d6aba1bd5723e55a5c61379e4adeea03bb6e0baecd388e11e1ce04f257':raise ValueError('Unexpected catalog response')
lines=raw.decode().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('Source\tRAJ2000\tDEJ2000\t'));rows=list(csv.DictReader([lines[i]]+[x for x in lines[i+3:] if x.strip()],delimiter='\t'))
if len(rows)!=1 or rows[0]['Source'].strip()!='ILTJ093927.01+404350.3':raise ValueError('Unexpected result')
r=rows[0];prior=json.loads((p/'summary.json').read_text());peak=prior['psz2_southern_difference_peak'];a=SkyCoord(peak['ra_deg']*u.deg,peak['dec_deg']*u.deg);b=SkyCoord(float(r['RAJ2000'])*u.deg,float(r['DEJ2000'])*u.deg)
out={'catalog':'J/A+A/659/A1/catalog','catalog_doi':'10.26093/cds/vizier.36590001','query_radius_arcsec':30,'response_sha256':digest,'rows':len(rows),'source_id':r['Source'].strip(),'offset_from_difference_peak_arcsec':float(a.separation(b).arcsec),'catalog_morphology_code':r['SCode'].strip(),'catalog_major_fwhm_arcsec':float(r['Maj']),'catalog_minor_fwhm_arcsec':float(r['Min']),'caveat':'Nearby extended catalog source; related survey observations; separation and post-hoc search do not identify the physical origin of the image difference.'}
(p/'catalog-summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
