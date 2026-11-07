#!/usr/bin/env python3
"""Transform stored FK5 WCS peak coordinates before catalog comparisons."""
import csv,hashlib,io,json,sys,warnings
from pathlib import Path
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord,FK5
import astropy.units as u
p=Path(__file__).resolve().parent;root=p.parent
macmap,pszmap,header,row,cone=map(Path,sys.argv[1:]);inputs={macmap:'d89cf4f1f58e6d369d0ae928bd5115bce7b2189c63c7d476ef12e489160e59de',pszmap:'021144b3d9118b607e851ed9851f97efe149d220903ddb0c64d0617083d369f6',header:'39f8a3f1cad273f1c7d79875ac95c41a24a5185eeb207e1c2c422504d4cec761',row:'cb9145dfe3bba33ebc0e3a8c566ee3c110feb087c6a284ea8d29d8f7e7d39095',cone:'048f02d6aba1bd5723e55a5c61379e4adeea03bb6e0baecd388e11e1ce04f257'}
for path,digest in inputs.items():
 if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('Input hash mismatch: '+path.name)
for image in (macmap,pszmap):
 with warnings.catch_warnings():
  warnings.simplefilter('ignore'); c=WCS(fits.getheader(image)).celestial.pixel_to_world(10,10)
 if c.frame.name!='fk5' or abs(c.frame.equinox.jyear-2000)>1e-9:raise ValueError('Unexpected map WCS reference frame')
raw=io.BytesIO(header.read_bytes());h0=fits.Header.fromfile(raw);h=fits.Header.fromfile(raw);b=row.read_bytes()
if h['NAXIS1']!=len(b):raise ValueError('Unexpected row width')
h['NAXIS2']=1
with fits.open(io.BytesIO(h0.tostring().encode()+h.tostring().encode()+b+bytes((-len(b))%2880))) as hd:
 d=hd[1].data[0]
 if str(d['Source_Name']).strip()!='ILTJ175159.28+443849.6':raise ValueError('Unexpected LoTSS row')
 macradio=(float(d['RA']),float(d['DEC']));macopt=(float(d['optRA']),float(d['optDec']))
text=cone.read_text().splitlines();i=next(i for i,s in enumerate(text) if s.startswith('Source\tRAJ2000\tDEJ2000\t'));rs=list(csv.DictReader([text[i]]+[s for s in text[i+3:] if s.strip()],delimiter='\t'))
if len(rs)!=1 or rs[0]['Source'].strip()!='ILTJ093927.01+404350.3':raise ValueError('Unexpected radio catalog result')
pszradio=(float(rs[0]['RAJ2000']),float(rs[0]['DEJ2000']))
mac=json.loads((root/'macs1752-difference-localization'/'summary.json').read_text())['peak_position_deg'];ps=json.loads((root/'two-cluster-physical-beam'/'summary.json').read_text())['psz2_southern_difference_peak'];pspeak=(ps['ra_deg'],ps['dec_deg'])
# VizieR labels positions J2000; the catalog radio/optical coordinates are
# treated as ICRS as in prior analyses, not as a claim of sub-arcsecond absolute astrometry.
keckfile=root/'macs1752-keck-crossmatch'/'cone.tsv'
keckhash=hashlib.sha256(keckfile.read_bytes()).hexdigest()
if keckhash!='68a293f0dfd84c872f69a9a75a7b33618a70dd229281bd4dcfa5929c08e7f395':raise ValueError('Keck response hash mismatch')
kecklines=keckfile.read_text().splitlines();k=next(i for i,s in enumerate(kecklines) if s.startswith('Name\tf_Name\tRAJ2000\tDEJ2000\t'));keckrows=list(csv.DictReader([kecklines[k]]+[s for s in kecklines[k+3:] if s.strip()],delimiter='\t'));km=[r for r in keckrows if r['SimbadName'].strip()=='[GDW2019] J267.99546900+44.64944397']
if len(km)!=1:raise ValueError('Keck object missing or ambiguous')
keck=(float(km[0]['RAJ2000']),float(km[0]['DEJ2000']))
catalog={'MACS radio':macradio,'MACS optical':macopt,'MACS Keck object':keck,'PSZ2 radio':pszradio}
results={}
for cluster,rawpos in [('MACS',mac),('PSZ2',pspeak)]:
 fk=SkyCoord(*rawpos,unit='deg',frame=FK5(equinox='J2000'));wrong=SkyCoord(*rawpos,unit='deg',frame='icrs');icrs=fk.icrs
 for label,xy in catalog.items():
  if not label.startswith(cluster+' '):continue
  c=SkyCoord(*xy,unit='deg',frame='icrs');actual=fk.separation(c).arcsec;old=wrong.separation(c).arcsec
  results[label]={'catalog_ra_deg':xy[0],'catalog_dec_deg':xy[1],'peak_fk5_ra_deg':rawpos[0],'peak_fk5_dec_deg':rawpos[1],'peak_icrs_ra_deg':float(icrs.ra.deg),'peak_icrs_dec_deg':float(icrs.dec.deg),'old_naive_arcsec':float(old),'frame_corrected_arcsec':float(actual),'correction_arcsec':float(actual-old)}
summary={'catalog_frame_assumption':'Catalog numerical coordinates treated as ICRS, as in prior work; catalog labels J2000 and absolute astrometry need source-level verification.','results':results,'limitations':'Frame-aware positional comparison only, no astrometric error budget or physical source association. Prior map-based paired separations use common WCS and are unaffected by this cross-catalog correction.'}
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
