#!/usr/bin/env python3
"""Degree-threshold pools of the Parts-509 graph.

P_k = all level-1 K-rational completion points (points of K^2 \ V at unit distance from >= 3 vertices;
exact enumeration in hadwiger_nelson_parts509_swap_closure, list completion_points.json) with at least k
unit neighbours in V.  The accumulative graph A_k = V ∪ P_k uses ambient indices: V = 0..508, point q of
the completion list = 509 + q.  Output: union_deg{k}.json = {'start': [ambient indices], 'added_points': n,
'deleted_vertices': 0, 'note': ...} for each requested k.
usage: build_degree_pools.py COMPLETION_JSON OUTDIR k [k ...]
"""
import json, sys
from pathlib import Path
from collections import Counter
comp = json.loads(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2]); out.mkdir(exist_ok=True)
N = 509
deg = [len(r['neighbors']) for r in comp['points']]
print('degree histogram of the level-1 points:', dict(sorted(Counter(deg).items())))
for k in map(int, sys.argv[3:]):
    pts = [N + q for q, d in enumerate(deg) if d >= k]
    u = {'start': list(range(N)) + pts, 'added_points': len(pts), 'deleted_vertices': 0,
         'note': f'V plus all level-1 K-rational completion points with >= {k} unit neighbours in V'}
    (out / f'union_deg{k}.json').write_text(json.dumps(u))
    print(f'k={k}: {len(pts)} points, {N + len(pts)} vertices -> {out / f"union_deg{k}.json"}')
