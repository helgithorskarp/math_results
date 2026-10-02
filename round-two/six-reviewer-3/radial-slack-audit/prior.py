"""Source-bound reuse of this reviewer's independently audited kernels."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
root = HERE.parents[2]
manifest = json.loads((HERE / 'INPUTS.json').read_text())
for row in manifest['files']:
    if row.get('role') == 'own-reviewed-parent':
        raw = (root / row['path']).read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('own parent source mismatch ' + row['path'])
directory = HERE.parent / 'complex-sector-audit'
sys.path.insert(0, str(directory))
def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, directory / filename)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj
cx = module('complex_sector', 'complex_sector.py')
literal_parent = module('review9289literal', 'literal_checks.py')
G, Jet = literal_parent.G, literal_parent.J
from parents import F, I, K, need, real, embedding, enclose, convolution, power, evaluate, derivative
