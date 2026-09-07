#!/usr/bin/env python3
"""No solver, network, catalog or omitted certificate is needed."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import extract
import family
import verify

base = Path(__file__).resolve().parent
for line in (base/'SHA256SUMS').read_text().splitlines():
    digest, name = line.split('  ')
    if hashlib.sha256((base/name).read_bytes()).hexdigest() != digest:
        raise ValueError('manifest: '+name)
expected = (base/'expected.json').read_bytes()
for flags in ([], ['-O']):
    got = subprocess.check_output([sys.executable,'-B',*flags,str(base/'audit.py')])
    if got != expected:
        raise ValueError('audit output mismatch')
parameters = json.loads((base/'fixture_parameters.json').read_text())
graph = json.loads((base/'fixture_graph.json').read_text())
certificate = json.loads((base/'fixture_certificate.json').read_text())
if family.generate(parameters) != graph or extract.extract(graph) != certificate:
    raise ValueError('stored fixture mismatch')
verify.verify(graph, certificate)
print(json.dumps({'status':'REPRODUCED_RANK4_CUT_SEARCH_REDUCTION',
                  'audit_sha256':hashlib.sha256(expected).hexdigest()}, sort_keys=True))
