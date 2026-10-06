"""Source-integrity metadata only; no mathematical functions are imported."""
from pathlib import Path
import hashlib
import json

p=Path(__file__).resolve().parent
m=json.loads((p/'SOURCE_MANIFEST.json').read_bytes())
for row in m['files']:
    f=p/row['path'];raw=f.read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
print('PASS: '+str(len(m['files']))+' named source files match the manifest.')
