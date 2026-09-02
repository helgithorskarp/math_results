#!/usr/bin/env python3
"""Enlarged accumulative graph: V plus every completion point appearing in ANY candidate tie
instance (certified or 4-colourable): swaps, the 63 pairs of the pair closure, the 122 triple candidates."""
import os, json
from pathlib import Path
HN = Path(os.environ.get('HN_SCRATCH', '/scratch/agents/researcher-4/hn')); REPO = Path.home() / 'math_results'; N = 509
pts = set(); dels = set()
for q, u in json.loads((REPO / 'hadwiger_nelson_parts509_pair_closure' / 'swaps.json').read_text()):
    pts.add(q); dels.add(u)
for r in json.loads((REPO / 'hadwiger_nelson_parts509_pair_replacement_classification' / 'certificate.json').read_text())['records']:
    pts.update(r['A']); dels.update(r['U'])
for r in json.loads((HN / 'ties' / 'tie_results.json').read_text())['results']:
    pts.update(r['A']); dels.update(r['D'])
added = sorted(N + q for q in pts)
start = sorted(set(range(N)) | set(added))
(HN / 'ties' / 'tie_union_all.json').write_text(json.dumps({'start': start, 'added_points': added, 'deleted_vertices': sorted(dels)}))
print(f'added points {len(added)}, vertices ever deleted (candidates) {len(dels)}, union size {len(start)}')
