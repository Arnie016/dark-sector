import hashlib,json
from pathlib import Path
from urllib.request import urlopen
p=Path(__file__).resolve().parent;m=json.loads((p/'manifest.json').read_text());dest=p/'images';dest.mkdir(exist_ok=True)
for e in m['images']:
 assert e['url'].startswith('https://www.tng-project.org/exp/galleries/') and e['filename'] in [f'{q}_{axis}.png' for q in ('gas','xray') for axis in 'xyz']
 with urlopen(e['url'],timeout=30) as f:data=f.read(5_000_001)
 if len(data)!=e['bytes'] or hashlib.sha256(data).hexdigest()!=e['sha256']:raise SystemExit('Mismatch: '+e['filename'])
 (dest/e['filename']).write_bytes(data);print('Verified',e['filename'])
