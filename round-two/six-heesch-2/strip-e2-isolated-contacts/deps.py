"""Pinned published source dependencies; no network or solver."""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
OPS=Path('/scratch/research-team-sol61-six-20260929/state')
def paused():
    return any((OPS/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER.json'))

for relative,digest in json.loads((HERE/'expected.json').read_text())['dependency_hashes'].items():
    p=HERE.parent/relative
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
        raise ValueError('Missing or changed published dependency: '+relative)
for directory in ('parametric-strip-obstruction','strip-contact-domains'):
    sys.path.append(str(HERE.parent/directory))
