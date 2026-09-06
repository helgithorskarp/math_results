#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
for line in (root/'SHA256SUMS').read_text().splitlines():
    digest, name = line.split('  ')
    if hashlib.sha256((root/name).read_bytes()).hexdigest() != digest:
        raise ValueError('manifest mismatch: '+name)
for script, expected in [('bounds.py','bounds_expected.json'),
                         ('controls.py','controls_expected.json'),
                         ('compare.py','comparison.json')]:
    for flags in [[],['-O']]:
        p = subprocess.run([sys.executable,*flags,'-B',str(root/script)],
                           capture_output=True,check=True)
        if p.stdout != (root/expected).read_bytes():
            raise ValueError('reproduction mismatch: '+script)
        if p.stderr:
            raise ValueError('unexpected diagnostics: '+script)
for flags in [[], ['-O']]:
    p = subprocess.run([sys.executable,*flags,'-B',str(root/'extract.py'),str(root/'fixture.json')],
                       capture_output=True,check=True)
    if p.stdout != (root/'fixture_certificate.json').read_bytes():
        raise ValueError('physical fixture extraction mismatch')
    p = subprocess.run([sys.executable,*flags,'-B',str(root/'verify.py'),str(root/'fixture.json'),
                        str(root/'fixture_certificate.json')],capture_output=True,check=True)
    if p.stdout != b'VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE\n':
        raise ValueError('physical fixture verification mismatch')
print(json.dumps({'status':'REPRODUCED_MODULE_RESILIENCE_PACKAGE',
                  'ramsey_graph_found':False,'bound_improved':False},sort_keys=True))
