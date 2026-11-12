#!/usr/bin/env python3
"""Check a pinned VizieR ASU-TSV response without treating pair rows as independent."""
import csv, hashlib, json, sys
from pathlib import Path
p=Path(sys.argv[1]); raw=p.read_bytes()
manifest=json.loads((Path(__file__).resolve().parent/'catalog-manifest.json').read_text())
if hashlib.sha256(raw).hexdigest()!=manifest['sha256']: raise SystemExit('Unexpected catalog bytes')
lines=raw.decode().splitlines()
i=next(i for i,s in enumerate(lines) if s.startswith('recno\tName\t'))
rows=list(csv.DictReader([lines[i]]+[s for s in lines[i+3:] if s.strip()],delimiter='\t'))
hits=[r for r in rows if r['Name'].strip()=='PSZ2 G181.06+48.47']
if len(rows)!=35 or len(hits)!=2: raise SystemExit('Unexpected table or match size')
assert {r['Pos'].strip() for r in hits}=={'N','S'}
assert all(r['DRR-RR'].strip()=='2694' and r['e_DRR-RR'].strip()=='39' for r in hits)
print('35 rows; one named pair, two records: 2694 ± 39 kpc')
