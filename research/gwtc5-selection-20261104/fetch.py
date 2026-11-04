"""Fetch the public API snapshot only if it matches the analyzed version."""
from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen

URL = 'https://gwosc.org/eventapi/jsonfull/GWTC-5.0/'
EXPECTED = '5a15bccb5e1764e67feece022711f740a7e616b8c6b866c08b114741c846fb70'
TARGET = Path(__file__).resolve().parent / 'GWTC-5.0-events.json'
with urlopen(URL, timeout=30) as response:
    raw = response.read(2_000_001)
if len(raw) > 2_000_000 or sha256(raw).hexdigest() != EXPECTED:
    raise SystemExit('API response differs from the pinned snapshot; no file written. Obtain the archived snapshot or update the analysis with a new provenance record.')
TARGET.write_bytes(raw)
print(f'Verified snapshot: {len(raw)} bytes; SHA-256 {EXPECTED}')
