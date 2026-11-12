#!/usr/bin/env python3
"""Frame-aware targeted LoTSS catalog comparison to two difference peaks."""
import csv,hashlib,json,sys,warnings
from pathlib import Path
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord,FK5
import astropy.units as u
p=Path(__file__).resolve().parent;root=p.parent;fitsfile,nfile,sfile=map(Path,sys.argv[1:]);expected={fitsfile:'9a27db5ff41df8e825315b0d70afd99c2fbe4f23a04d354c6d6a11a5f5f538f7',nfile:'3245bde4ca59aaf51ad50f0e19aef9f3f37e7753a0b1079e6727745162357600',sfile:'cfc578f93e5676e6bca56a717447ca37347d3a028c340027e38a3031873436d9'}
for f,h in expected.items():
 if hashlib.sha256(f.read_bytes()).hexdigest()!=h:raise ValueError('Input hash mismatch')
with warnings.catch_warnings():warnings.simplefilter('ignore');w=WCS(fits.getheader(fitsfile)).celestial
priorpath=root/'g099-feature-influence'/'summary.json';prior=json.loads(priorpath.read_text());out={}
for label,path in [('N',nfile),('S',sfile)]:
 peak=prior['peaks'][label];world=w.pixel_to_world(peak['x'],peak['y'])
 if world.frame.name!='fk5' or abs(world.frame.equinox.jyear-2000)>1e-9:raise ValueError('Unexpected WCS frame')
 saved=SkyCoord(peak['ra_deg_fk5']*u.deg,peak['dec_deg_fk5']*u.deg,frame=FK5(equinox='J2000'))
 if world.separation(saved).arcsec>1e-6:raise ValueError('Peak WCS mismatch')
 lines=path.read_text().splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('Source\tRAJ2000\tDEJ2000\t'));rows=list(csv.DictReader([lines[i]]+[x for x in lines[i+3:] if x.strip() and not x.startswith('#')],delimiter='\t'))
 if not rows or len(rows)>=1000 or any('overflow' in x.lower() for x in lines if x.startswith('#')):raise ValueError('Empty or capped query')
 candidates=[]
 for row in rows:
  c=SkyCoord(float(row['RAJ2000'])*u.deg,float(row['DEJ2000'])*u.deg,frame='icrs');distance=float(world.separation(c).arcsec)
  candidates.append({'source_id':row['Source'].strip(),'separation_arcsec':distance,'catalog_major_fwhm_arcsec':float(row['Maj']),'catalog_minor_fwhm_arcsec':float(row['Min']),'catalog_peak_mjy_per_beam':float(row['Speak']),'catalog_morphology_code':row['SCode'].strip()})
 candidates.sort(key=lambda r:r['separation_arcsec'])
 if any(c['separation_arcsec']>70.1 for c in candidates):raise ValueError('Unexpected cone result')
 out[label]={'query_center_icrs_deg':[float(world.icrs.ra.deg),float(world.icrs.dec.deg)],'query_radius_arcsec':70,'rows':len(candidates),'candidates':candidates,'response_sha256':expected[path]}
summary={'peak_summary_sha256':hashlib.sha256(priorpath.read_bytes()).hexdigest(),'input_fits_sha256':expected[fitsfile],'catalog':'J/A+A/659/A1/catalog','catalog_position_frame_assumption':'J2000 coordinates treated as ICRS; absolute astrometric frame and uncertainty not verified','results':out,'warning':'Post-hoc positional association with related LoTSS survey data, not independent detection, a source identity proof, a cluster membership determination or a calibrated association probability.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
