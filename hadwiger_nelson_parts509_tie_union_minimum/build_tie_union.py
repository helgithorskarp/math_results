#!/usr/bin/env python3
"""Union of the known 509-vertex 5-chromatic ties of Parts-509 inside the ambient graph W3.

Ties: the 11 one-point swaps (swap closure), the 60 certified pair replacements
(researcher-3's classification), and the certified triple replacements (tie_results.json).
Writes tie_union.json: {'start': sorted ambient indices of V ∪ all added points,
'ties': [{'D': [...], 'A': [ambient indices]}...]} for the chained-sweep minimiser.
"""
import os, json
from pathlib import Path
HN = Path(os.environ.get('HN_SCRATCH', '/scratch/agents/researcher-4/hn'))
REPO = Path.home() / 'math_results'
N = 509
ties = []
for q, u in json.loads((REPO / 'hadwiger_nelson_parts509_pair_closure' / 'swaps.json').read_text()):
    ties.append({'kind': 'swap', 'D': [u], 'A': [N + q]})
pc = json.loads((REPO / 'hadwiger_nelson_parts509_pair_replacement_classification' / 'certificate.json').read_text())
for r in pc['records']:
    if r['status'].startswith('certified-not-4-colorable'):
        ties.append({'kind': 'pair', 'D': sorted(r['U']), 'A': [N + q for q in r['A']]})
tr = json.loads((HN / 'ties' / 'tie_results.json').read_text())
for r in tr['results']:
    if r['status'] == 'UNSAT' and r.get('drat_trim_verified'):
        ties.append({'kind': 'triple', 'D': sorted(r['D']), 'A': [N + q for q in r['A']]})
added = sorted({a for t in ties for a in t['A']})
deleted = sorted({d for t in ties for d in t['D']})
start = sorted(set(range(N)) | set(added))
out = {'start': start, 'added_points': added, 'deleted_vertices': deleted, 'ties': ties}
(HN / 'ties' / 'tie_union.json').write_text(json.dumps(out))
from collections import Counter
print('ties by kind:', Counter(t['kind'] for t in ties))
print(f'added points {len(added)}, vertices ever deleted {len(deleted)}, union size {len(start)}')
