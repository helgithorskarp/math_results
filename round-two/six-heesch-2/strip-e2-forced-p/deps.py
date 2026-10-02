"""Pin the published shared kernels, separate reader and literal inputs."""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).absolute().parent
OPS=Path('/scratch/research-team-sol61-six-20260929/state')
expected=json.loads((HERE/'expected.json').read_text())
for name,digest in expected['dependency_hashes'].items():
    path=HERE/name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
        raise ValueError('Missing or changed published dependency: '+name)
if hashlib.sha256((HERE/'inputs.json').read_bytes()).hexdigest()!=expected['input_sha256']:
    raise ValueError('Changed literal input table')
for folder in ('parametric-strip-obstruction','strip-contact-domains','strip-e2-branches'):
    sys.path.insert(0,str(HERE.parent/folder))


def paused():
    return any((OPS/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER.json'))
