#!/usr/bin/env python3
"""Export a sharp extension witness as a sorted literal edge list."""
import json
from pathlib import Path
import sys

index = int(sys.argv[1])
if not 0 <= index < 5:
    raise ValueError('class must be 0..4')
certificate = json.loads(Path(__file__).with_name('certificate.json').read_text())
g = certificate['records'][index]['maximal_witness']
print(g['n'],len(g['red_edges']))
for u,v in g['red_edges']:
    print(u,v)
