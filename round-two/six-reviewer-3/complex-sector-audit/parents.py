"""Source-bound reuse of this reviewer's independently audited real kernel."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'INPUTS.json').read_text())
root = HERE.parents[2]
for row in manifest['files']:
    if row.get('role') == 'own-reviewed-parent':
        raw = (root / row['path']).read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('own reviewed parent source mismatch ' + row['path'])
parent = HERE.parent / 'centered-sector-audit'
sys.path.insert(0, str(parent))
spec = importlib.util.spec_from_file_location('review9203', parent / 'audit.py')
real = importlib.util.module_from_spec(spec)
spec.loader.exec_module(real)
from exact_numbers import F, I, K, need, convolution, power, evaluate, derivative, chebyshev, embedding, enclose, up

