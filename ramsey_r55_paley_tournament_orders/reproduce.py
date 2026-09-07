#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
for line in (root/'SHA256SUMS').read_text().splitlines():
    h,name=line.split('  ')
    if hashlib.sha256((root/name).read_bytes()).hexdigest()!=h: raise ValueError('manifest: '+name)
for script,expected in [('build.py','certificate.json'),('check.py','expected.json'),('controls.py','controls_expected.json')]:
    for flags in [[],['-O']]:
        r=subprocess.run([sys.executable,*flags,'-B',str(root/script)],capture_output=True,check=True)
        if r.stdout!=(root/expected).read_bytes() or r.stderr: raise ValueError('reproduction: '+script)
for script,expected in [('export.py','fixture.edges'),('extract.py','fixture_certificate.json')]:
    r=subprocess.run([sys.executable,'-B',str(root/script),str(root/'fixture.json')],capture_output=True,check=True)
    if r.stdout!=(root/expected).read_bytes() or r.stderr: raise ValueError('fixture: '+script)
r=subprocess.run([sys.executable,'-B',str(root/'verify.py'),str(root/'fixture.edges'),str(root/'fixture_certificate.json')],capture_output=True,check=True)
if json.loads(r.stdout)['status']!='VERIFIED_TWO_PHYSICAL_MONOCHROMATIC_FIVES': raise ValueError('physical verification')
print(json.dumps({'status':'REPRODUCED_PALEY43_ORDERING_OBSTRUCTION','kernel_orders':51,
                  'guaranteed_distinct_monochromatic_fives':2,'ramsey_bound_improved':False},sort_keys=True))
