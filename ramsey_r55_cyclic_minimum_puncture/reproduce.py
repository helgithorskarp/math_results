#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
for line in (root/'SHA256SUMS').read_text().splitlines():
    h,name = line.split('  ')
    if hashlib.sha256((root/name).read_bytes()).hexdigest() != h:
        raise ValueError('manifest mismatch: '+name)
for script,expected in [('check.py','expected.json'),('controls.py','controls_expected.json')]:
    for flags in [[],['-O']]:
        p = subprocess.run([sys.executable,*flags,'-B',str(root/script)],capture_output=True,check=True)
        if p.stdout != (root/expected).read_bytes() or p.stderr:
            raise ValueError('reproduction mismatch: '+script)
p = subprocess.run([sys.executable,'-B',str(root/'export.py'),'1'],capture_output=True,check=True)
if p.stdout != (root/'maximum40.edges').read_bytes():
    raise ValueError('edge-list export mismatch')
p = subprocess.run([sys.executable,'-B',str(root/'verify_graph.py'),str(root/'maximum40.edges')],
                   capture_output=True,check=True)
g = json.loads(p.stdout)
if g['n'] != 40 or not g['ramsey_5_5']:
    raise ValueError('stand-alone graph verification failed')
print(json.dumps({'status':'REPRODUCED_CYCLIC_MINIMUM_PUNCTURE_SPECTRUM',
                  'maximum_orders':[39,40,39,40,38],'ramsey_bound_improved':False},sort_keys=True))
