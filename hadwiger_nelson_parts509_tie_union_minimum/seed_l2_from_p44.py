#!/usr/bin/env python3
"""Transplant killing sets of the P25/P44 unions into the (pruned) level-2 union: a witness colouring of
A*_P44 − D is extended greedily to the extra points (a point whose coloured neighbours use all 4 colours joins D);
the result D' ⊇ D with a proper colouring of A*_L2 − D' is a killing set of the level-2 union.  No solver calls.
Writes thin2_results_L2_seed9.json (family only) for merging by the running ihs_thin2 processes."""
import os, json
from pathlib import Path
HN = Path(os.environ.get('HN_SCRATCH', '/scratch/agents/researcher-4/hn'))
amb = json.loads((HN / 'level2' / 'ambient_lvl2_edges.json').read_text())
U2 = json.loads((HN / 'ties' / 'tie_union_lvl2_pruned.json').read_text()); STAR2 = sorted(U2['start']); S2 = set(STAR2)
F2 = json.loads((HN / 'ties' / 'forced_lvl2_pruned.json').read_text()); Fset = set(F2['forced']); R2 = [v for v in STAR2 if v not in Fset]
ADJ = {v: set() for v in STAR2}
for a, b in amb['edges']:
    if a in S2 and b in S2:
        ADJ[a].add(b); ADJ[b].add(a)
K = 4
out = []; seen = set()
for uf, rf in [('tie_union_all.json', 'thin2_results_P44_seed1.json'), ('tie_union.json', 'thin2_results_P25_seed1.json')]:
    U = json.loads((HN / 'ties' / uf).read_text()); STAR = sorted(U['start'])
    res = json.loads((HN / 'ties' / rf).read_text())
    for row in res['family']:
        D = set(row['D']); verts = [v for v in STAR if v not in D]
        col = {v: int(c) for v, c in zip(verts, row['witness'])}
        # sanity: proper on the level-2 edge list restricted to the coloured vertices
        assert all(col[w] != col[v] for v in col for w in ADJ.get(v, ()) if w in col), 'improper transplanted witness'
        D2 = set(D)
        for p in STAR2:
            if p in col or p in D2:
                continue
            used = {col[w] for w in ADJ[p] if w in col}
            free = [c for c in range(K) if c not in used]
            if free:
                col[p] = free[0]
            else:
                D2.add(p)
        D2 = {v for v in D2 if v in S2}      # points pruned from the level-2 union are irrelevant
        assert D2 <= set(R2), 'killing set touches a forced vertex'
        assert set(col) | D2 == S2
        key = frozenset(D2)
        if key in seen:
            continue
        seen.add(key)
        out.append({'D': sorted(D2), 'witness': ''.join(str(col[v]) for v in STAR2 if v not in D2)})
Path(HN / 'ties' / 'thin2_results_L2_seed9.json').write_text(json.dumps({'R': R2, 'F_size': len(Fset), 'family': out, 'history': [], 'status': 'seed'}))
from collections import Counter
print(f'transplanted {len(out)} killing sets into the level-2 union; sizes {sorted(Counter(len(r["D"]) for r in out).items())}')
