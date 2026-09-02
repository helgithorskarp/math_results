#!/usr/bin/env python3
"""Structural statistics of the S-only killing-set family (for the README)."""
import json, sys
from collections import Counter
H = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
sets = sorted({frozenset(r['D']) for r in H}, key=len)
keep = []
for a in sets:
    if not any(b < a for b in keep if len(b) < len(a)):
        keep.append(a)
from pathlib import Path
amb = json.load(open(Path(__file__).resolve().parent.parent / 'hadwiger_nelson_parts509_pair_closure' / 'ambient_w3_edges.json'))
IS = sorted({max(a, b) for a, b in amb['edges'] if min(a, b) < 374 <= max(a, b) < 509})
print('family', len(sets), 'minimal', len(keep))
print('size histogram of minimal sets:', sorted(Counter(len(D) for D in keep).items()))
singles = sorted(v for D in keep if len(D) == 1 for v in D)
print('forced (singletons):', len(singles), 'equal to I_S:', singles == IS)
pairs = sorted(tuple(sorted(D)) for D in keep if len(D) == 2)
print('irreplaceable pairs:', len(pairs))
print('vertices in pairs:', len({v for p in pairs for v in p}))
deg = Counter(v for p in pairs for v in p)
print('pair-degree histogram:', sorted(Counter(deg.values()).items()))
print(pairs)
