#!/usr/bin/env python3
"""Read only two named members of an official tar within a compressed-byte cap."""
import hashlib,json,sys,tarfile
from pathlib import Path
import requests
url='https://lofar-surveys.org/public/clusterdata/PSZ2G099.48%2B55.60/PSZ2G099.48%2B55.60_FITS.tar.gz';cap=75000000;out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
wanted={f'PSZ2G099.48+55.60{x}.fits' for x in ('T50kpc','T50kpcSUB')}; found={};seen=[]
class LimitReader:
 def __init__(self,raw):self.raw=raw;self.count=0
 def read(self,n=-1):
  if n<0 or self.count+n>cap:raise OSError('Compressed-byte budget reached')
  b=self.raw.read(n);self.count+=len(b);return b
response=requests.get(url,stream=True,timeout=(10,30));response.raise_for_status();reader=LimitReader(response.raw)
try:
 with tarfile.open(fileobj=reader,mode='r|gz') as tar:
  for member in tar:
   seen.append({'name':member.name,'size':member.size,'regular':member.isfile()})
   if member.name in wanted:
    if not member.isfile() or member.size>40000000 or member.name in found:raise ValueError('Unexpected member')
    f=tar.extractfile(member)
    if f is None:raise ValueError('Member not readable')
    data=f.read(member.size+1)
    if len(data)!=member.size:raise ValueError('Truncated member')
    (out/member.name).write_bytes(data);found[member.name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    if set(found)==wanted:break
 if set(found)!=wanted:raise ValueError('Both named images were not found')
finally:response.close()
manifest={'url':url,'compressed_bytes_consumed':reader.count,'compressed_byte_cap':cap,'http_content_length':response.headers.get('Content-Length'),'last_modified':response.headers.get('Last-Modified'),'etag':response.headers.get('ETag'),'members_scanned':seen,'selected':found,'limitation':'Partial sequential read only; original complete tarball was not downloaded or hashed.'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
