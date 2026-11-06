import hashlib,json
from pathlib import Path
from urllib.request import urlopen
p=Path(__file__).resolve().parent;manifest=json.loads((p/'manifest.json').read_text());dest=p/'images';dest.mkdir(exist_ok=True)
for entry in manifest['images']:
 assert entry['url'].startswith('https://www.tng-project.org/exp/galleries/lee23/') and entry['filename'] in ('x.png','y.png','z.png')
 with urlopen(entry['url'],timeout=30) as response:data=response.read(5_000_001)
 if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:raise SystemExit('Upstream image changed or is too large; no file saved for '+entry['filename'])
 (dest/entry['filename']).write_bytes(data);print('Verified',entry['filename'])
