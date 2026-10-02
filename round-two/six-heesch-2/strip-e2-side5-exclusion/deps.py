"""Byte-pinned published dependencies; no network or solver."""
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
OPS=Path('/scratch/research-team-sol61-six-20260929/state')
def paused():
    return any((OPS/n).exists() for n in ['PAUSED','PAUSED.json','HANDOVER.json'])
expected=json.loads((HERE/'expected.json').read_text())
for name,digest in expected['dependency_hashes'].items():
    p=HERE/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
        raise ValueError('Missing or altered published dependency: '+name)
for directory in ['strip-e2-branches','strip-contact-domains','parametric-strip-obstruction']:
    sys.path.append(str(HERE.parent/directory))
