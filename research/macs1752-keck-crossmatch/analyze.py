#!/usr/bin/env python3
"""Reproduce the sky-coordinate cross-match from the saved VizieR TSV."""
import csv
import hashlib
import json
from pathlib import Path
from astropy.coordinates import SkyCoord
import astropy.units as u

HERE = Path(__file__).resolve().parent
raw = (HERE / 'cone.tsv').read_bytes()
lines = raw.decode('utf-8').splitlines()
start = next(i for i, line in enumerate(lines) if line.startswith('Name\tf_Name\tRAJ2000\tDEJ2000\t'))
header = lines[start].split('\t')
rows = list(csv.DictReader((line for line in lines[start+3:] if line.strip() and not line.startswith('#')), fieldnames=header, delimiter='\t'))
optical = SkyCoord(267.9954559*u.deg, 44.649425136309226*u.deg, frame='icrs')
radio = SkyCoord(267.99699456543635*u.deg, 44.64713476780804*u.deg, frame='icrs')
for row in rows:
    coord = SkyCoord(float(row['RAJ2000'])*u.deg, float(row['DEJ2000'])*u.deg, frame='icrs')
    row['opt_sep'] = optical.separation(coord).arcsec
    row['radio_sep'] = radio.separation(coord).arcsec
rows.sort(key=lambda row: row['opt_sep'])
match = rows[0]
assert match['SimbadName'].strip() == '[GDW2019] J267.99546900+44.64944397'
assert match['opt_sep'] < 0.1 and len(rows) < 1000
output = {'catalog':'J/ApJS/240/39/table7', 'query_radius_arcsec':60, 'rows':len(rows), 'source_file_sha256':hashlib.sha256(raw).hexdigest(), 'keck_object':match['SimbadName'].strip(), 'optical_separation_arcsec':match['opt_sep'], 'radio_separation_arcsec':match['radio_sep'], 'next_optical_separation_arcsec':rows[1]['opt_sep'], 'z_spec':float(match['zspec']), 'z_spec_uncertainty':float(match['e_zspec']), 'z_phot_lotss':0.3469112, 'z_phot_uncertainty':0.030810085729320768, 'cluster_reference_z':0.366, 'interpretation':'Positional optical match; association with extended radio emission and cluster membership remain unproven.'}
(HERE / 'summary.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps(output, indent=2))
