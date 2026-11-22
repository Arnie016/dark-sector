#!/usr/bin/env python3
"""Inventory Jones et al.'s published FITS index and compare map metadata."""
import csv,hashlib,json,sys
from pathlib import Path
import numpy as np
from astropy.io import fits
p=Path(__file__).resolve().parent;index,mac,psz=map(Path,sys.argv[1:])
sha={'mac':'d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de','psz':'021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6'}
for path,digest in [(mac,sha['mac']),(psz,sha['psz'])]:
 if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('Existing map hash mismatch')
lines=index.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('RAJ2000\tDEJ2000\tNx\tNy\t'));rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'))
if len(rows)!=46:raise ValueError(f'Expected 46 rows, got {len(rows)}; possible truncation')
output={'index_sha256':hashlib.sha256(index.read_bytes()).hexdigest(),'index_rows':len(rows),'clusters':{}}
for name,path in [('PSZ2 G071.21+28.86',mac),('PSZ2 G181.06+48.47',psz)]:
 selected=[r for r in rows if r['Name'].strip()==name]
 if len(selected)!=2:raise ValueError('Unexpected number of indexed images')
 radio=[r for r in selected if 'LOFAR' in r['Title']]
 if len(radio)!=1:raise ValueError('Unexpected radio index')
 with fits.open(path) as h:shape=list(np.squeeze(h[0].data).shape);header=h[0].header;freq=header.get('RESTFRQ',header.get('RESTFREQ'))
 r=radio[0];indexshape=[int(r['Ny']),int(r['Nx'])]
 output['clusters'][name]={'listed_images':[{'filename':z['FileName'].strip(),'type':z['Title'].strip(),'size_kib':int(z['size'])} for z in selected],'radio_index_shape':indexshape,'archived_sub_shape':shape,'shape_matches':shape==indexshape,'radio_index_frequency_hz':float(r['Freq']),'archived_sub_frequency_hz':float(freq) if freq is not None else None,'archive_map_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
output['limitations']='Index metadata similarity is not a file hash comparison, proof of identical image, or a region mask. Index is a snapshot of a 46-entry service response.'
(p/'summary.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
