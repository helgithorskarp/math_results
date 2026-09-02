#!/usr/bin/env python3
"""Build the exact union graph of Parts-509 and an aligned Heule graph (aligned_*.json from align.py).
Points: exact K-coordinates (8 Fractions per coordinate, basis of parts509.py); edges: float screen (|d^2-1| < 1e-6)
then exact confirmation; the screen is complete because all coordinates are exact elements of K evaluated in binary64
with relative error far below 1e-6 at these magnitudes (all points lie within radius 4).
usage: union_graph.py aligned.json out.json [more aligned.json ...]"""
import sys, json, time
from fractions import Fraction
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality'))
sys.path.insert(0, str(Path.home() / 'math_results' / 'hadwiger_nelson_parts509_swap_closure'))
import parts509 as ps
import kfield as kf
PARTS = Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality' / 'parts509.vtx'


def main():
    out = sys.argv[2]; files = [sys.argv[1]] + sys.argv[3:]
    t0 = time.time()
    P = ps.parse_points(PARTS)
    pts = list(P); index = {pt: i for i, pt in enumerate(P)}
    prov = [['P'] for _ in P]
    for f in files:
        d = json.load(open(f)); tag = Path(d['vtx']).stem
        for xs, ys in d['aligned_H']:
            pt = (kf.from_strings(xs), kf.from_strings(ys))
            if pt in index:
                prov[index[pt]].append(tag)
            else:
                index[pt] = len(pts); pts.append(pt); prov.append([tag])
    n = len(pts)
    F = np.array([[kf.to_float(x), kf.to_float(y)] for x, y in pts])
    d2 = ((F[:, None, :] - F[None, :, :]) ** 2).sum(-1)
    iu = np.triu_indices(n, 1)
    cand = [(int(a), int(b)) for a, b in zip(*iu) if abs(d2[a, b] - 1.0) < 1e-6]
    near = [(a, b) for a, b in cand if abs(d2[a, b] - 1.0) > 1e-9]
    edges = [(a, b) for a, b in cand if ps.squared_distance(pts[a], pts[b]) == ps.ONE]
    print(f'{n} points, float candidates {len(cand)} (near-miss in (1e-9,1e-6): {len(near)}), exact unit edges {len(edges)} ({time.time()-t0:.1f}s)')
    # per-provenance edge counts
    for tag in sorted(set(t for pr in prov for t in pr)):
        S = set(i for i in range(n) if tag in prov[i])
        print(f'  {tag}: {len(S)} points, {sum(1 for a, b in edges if a in S and b in S)} internal edges')
    json.dump({'points': [[kf.to_strings(x), kf.to_strings(y)] for x, y in pts], 'float': F.tolist(), 'provenance': prov, 'edges': edges,
               'sources': files}, open(out, 'w'))
    print('wrote', out)


if __name__ == '__main__':
    main()
