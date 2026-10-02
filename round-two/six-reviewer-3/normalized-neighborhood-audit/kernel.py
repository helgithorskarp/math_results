"""Hash-bound reuse of this reviewer's previous independent radial kernel."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def reviewed_inputs():
    rows = json.loads((HERE / 'OWN_INPUTS.json').read_text())['files']
    for row in rows:
        data = (ROOT / row['path']).read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError('own reviewed source mismatch: ' + row['path'])
    return rows


def radial_record():
    rows = reviewed_inputs()
    path = HERE.parent / 'radial-slack-audit' / 'verify.py'
    spec = importlib.util.spec_from_file_location('review9335_verifier', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    result = module.record()
    canonical = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    if digest != '4c0273812689454bb1875c252c3ad48a8d165a54639396c88e5b2b228bf029b2':
        raise ValueError('whole own previously reviewed radial record changed')
    return module, result, digest, len(rows)
