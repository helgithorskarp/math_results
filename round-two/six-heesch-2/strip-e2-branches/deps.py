"""Hash-pinned published affine geometry and separate supplier reader."""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).absolute().parent
CONTACT=HERE.parent/'strip-contact-domains'
GEOMETRY=HERE.parent/'parametric-strip-obstruction'
OPS=Path('/scratch/research-team-sol61-six-20260929/state')


def paused():
    return any((OPS/name).exists() for name in ('PAUSED','PAUSED.json','HANDOVER.json'))


expected=json.loads((HERE/'expected.json').read_text())
for name,digest in expected['dependency_hashes'].items():
    path=HERE/name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
        raise ValueError('Missing or changed published dependency: '+name)
for path in (CONTACT,GEOMETRY):
    sys.path.insert(0,str(path))
