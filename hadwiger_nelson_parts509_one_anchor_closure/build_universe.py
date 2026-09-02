#!/usr/bin/env python3
"""Builds the float universe used by the one-anchor enumeration.

Q = Q3 ∪ Q2K ∪ nonK: the points outside V with at least two vertex neighbours.
  Q3   : 1,158 level-1 completion points (completion_points.json of the swap closure), exact K-coordinates;
  Q2K  : 2,705 K-rational points with exactly two vertex neighbours (q2k_extra.json of the triple closure);
  nonK : 135,468 non-K intersection points of vertex pairs at distance < 2 (two_neighbour_points.nonk_row of the triple closure, 50-digit mpmath then
         binary64), sorted by their labels (i, j, s); the exact list of unit pairs among them is nonk_exact.json.
Outputs (in OUTDIR): V_float.npy (509 x 2), P_float.npy (139,331 x 2), universe_meta.json {types, nbrs, nonk_labels}.
usage: build_universe.py OUTDIR [--workers 2]
"""
import json, sys, time, argparse, importlib.util
from pathlib import Path
from multiprocessing import Pool
import numpy as np
from paths import HERE, SWAP, TRIPLE, COMPLETION, Q2K_EXTRA
sys.path.insert(0, str(HERE))
import kfield as kf
spec2 = importlib.util.spec_from_file_location('q2k', TRIPLE / 'two_neighbour_points.py')
q2k = importlib.util.module_from_spec(spec2); sys.modules['q2k'] = q2k; spec2.loader.exec_module(q2k)
ecp = q2k.ecp


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('outdir'); ap.add_argument('--workers', type=int, default=2)
    args = ap.parse_args(); out = Path(args.outdir); out.mkdir(exist_ok=True)
    t0 = time.time()
    ecp.init()
    V = np.array([[kf.to_float(x), kf.to_float(y)] for x, y in ecp.POINTS])
    comp = json.loads(COMPLETION.read_text())
    P3 = np.array([[kf.to_float(kf.from_strings(r['x'])), kf.to_float(kf.from_strings(r['y']))] for r in comp['points']])
    nb3 = [list(r['neighbors']) for r in comp['points']]
    ex = json.loads(Q2K_EXTRA.read_text())
    P2 = np.array([[kf.to_float(kf.from_strings(r['x'])), kf.to_float(kf.from_strings(r['y']))] for r in ex['q2k']])
    nb2 = [list(r['neighbors']) for r in ex['q2k']]
    labels = ex['nonk_labels']
    nonk = []
    with Pool(args.workers, initializer=ecp.init) as pool:
        for i, rows in pool.imap_unordered(q2k.nonk_row, range(len(V)), chunksize=8):
            for j, s, x, y in rows:
                nonk.append((i, j, s, x, y))
    nonk.sort()
    assert len(nonk) == len(labels) and sorted(map(tuple, labels)) == [(i, j, s) for i, j, s, _, _ in nonk], 'non-K label set mismatch'
    PN = np.array([[x, y] for _, _, _, x, y in nonk])
    P = np.vstack([P3, P2, PN])
    types = ['q3'] * len(P3) + ['q2k'] * len(P2) + ['nonk'] * len(PN)
    nbrs = nb3 + nb2 + [[i, j] for i, j, _, _, _ in nonk]
    np.save(out / 'V_float.npy', V); np.save(out / 'P_float.npy', P)
    (out / 'universe_meta.json').write_text(json.dumps({'types': types, 'nbrs': nbrs, 'nonk_labels': [[i, j, s] for i, j, s, _, _ in nonk]}))
    print(f'universe: V {len(V)}, Q3 {len(P3)}, Q2K {len(P2)}, nonK {len(PN)}, total Q {len(P)}  ({time.time()-t0:.0f}s)')


if __name__ == '__main__':
    main()
