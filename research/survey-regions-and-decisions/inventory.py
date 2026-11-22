#!/usr/bin/env python3
"""Read-only inventory of one official archive and both decision records."""
import hashlib,json,sys,tarfile
from pathlib import Path
p=Path(__file__).resolve().parent;archive=Path(sys.argv[1]);expected='7aee2051a76ba6cb89afd0816cfd8a861df57682f2bee0010c7d5f8bcbfd03dc'
hash_archive=hashlib.sha256(archive.read_bytes()).hexdigest()
if hash_archive!=expected:raise ValueError('Archive SHA-256 mismatch')
with tarfile.open(archive,'r:gz') as tar:
 entries=[{'name':m.name,'size':m.size,'type':'file' if m.isfile() else 'other'} for m in tar.getmembers()]
if len(entries)!=10 or any(x['type']!='file' for x in entries):raise ValueError('Unexpected archive structure')
records={}
for name,token in [('psz2-decision.txt','PSZ2G181.06+48.47'),('macs-decision.txt','PSZ2G071.21+28.86')]:
 path=Path(sys.argv[2] if name=='psz2-decision.txt' else sys.argv[3]);raw=path.read_bytes();text=raw.decode();blocks=[b for b in text.split('Cluster name: ') if b.strip()]
 parsed=[]
 for block in blocks:
  lines=block.splitlines()
  if lines[0].strip()!=token:raise ValueError('Wrong cluster identifier')
  cls=next((x.split(':',1)[1].strip() for x in lines if x.startswith('Classification:')),None)
  artifact=next((x.rsplit(':',1)[1].strip() for x in lines if x.startswith('Are there significant calibration/subtraction artefacts?')),None)
  if cls is None or artifact not in ('y','n'):raise ValueError('Incomplete record')
  parsed.append({'classification':cls,'significant_artifacts_answer':artifact})
 records[token]={'source_file':name,'sha256':hashlib.sha256(raw).hexdigest(),'records':parsed}
output={'archive_sha256':hash_archive,'archive_bytes':archive.stat().st_size,'members':entries,'archive_region_or_mask_candidates':[x['name'] for x in entries if any(t in x['name'].lower() for t in ('.reg','region','mask','polygon'))],'decisions':records,'limitations':'Inventory covers only this ten-file archive and the two linked decision records; absence of named masks here does not prove masks are unavailable elsewhere or encode the paper\'s full selection.'}
(p/'summary.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
