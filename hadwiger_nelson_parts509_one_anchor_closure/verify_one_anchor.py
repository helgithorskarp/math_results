#!/usr/bin/env python3
"""Solver-free verifier for the compact one-anchor closure certificate (certificate.json.gz).

Expands every configuration into vertex-neighbour lists and internal edges from the committed data:
  'q3:I'  -> neighbours of completion point I (completion_points.json of the swap closure),
  'k2:I'  -> neighbours of q2k_points[I] of triple_certificate.json,
  'n:I:J:S' -> {I, J},
  'x:X:Y:N..' -> the listed neighbours,
  edge code e -> star from x plus the coded pairs among the other three points.
Then, for every vertex u, recomputes with the committed witness libraries (base, swap, pair, triple rows) plus the
certificate's fresh rows (re-validated) which configurations are covered, and asserts that every uncovered
(configuration, u) is declared; recomputes the |Û(A)| histogram and checks max |Û(A)| ≤ 4.
usage: verify_compact.py CERT.json.gz [--workers W]
"""
import argparse, gzip, json, sys, time, importlib.util
from pathlib import Path
from multiprocessing import Pool
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location('ds', HERE / ('declared_sets.py' if (HERE / 'declared_sets.py').exists() else 'cover4.py'))
ds = importlib.util.module_from_spec(spec); spec.loader.exec_module(ds)
N, K = ds.N, ds.K
G = {}


def expand(cert, q3nbrs, k2nbrs):
    nbrs_list, keys = [], []
    PAIRS = [(1, 2), (1, 3), (2, 3)]
    for g in cert['groups']:
        for t in ('I', 'II'):
            for rec in g[t]:
                pts = [g['xn']]
                for r in rec[:3]:
                    f = r.split(':')
                    if f[0] == 'q3': pts.append(q3nbrs[int(f[1])])
                    elif f[0] == 'k2': pts.append(k2nbrs[int(f[1])])
                    elif f[0] == 'n': pts.append([int(f[1]), int(f[2])])
                    elif f[0] == 'x': pts.append([int(z) for z in f[3].split(',')])
                    else: raise ValueError(r)
                e = rec[3]
                edges = [(0, 1), (0, 2), (0, 3)] + [PAIRS[b] for b in range(3) if (e >> b) & 1]
                nbrs_list.append(pts); keys.append(tuple(sorted(edges)))
    assert len(nbrs_list) == cert['n_configs']
    return nbrs_list, keys


def init(cert_path):
    with gzip.open(cert_path, 'rb') as f:
        cert = json.loads(f.read())
    from paths import SWAP, TRIPLE
    q3nbrs = [list(r['neighbors']) for r in json.loads((SWAP / 'completion_points.json').read_text())['points']]
    k2nbrs = [list(r['neighbors']) for r in json.loads((TRIPLE / 'triple_certificate.json').read_text())['q2k_points']]
    parts, edges, lib, qnb, qq_edges, ntrip = ds.cu.load_libraries()
    fresh = {}
    for r in cert['fresh_rows']:
        u = r['u']; row = [-1 if ch == '-' else int(ch) for ch in r['row']]
        assert row[u] == -1 and len(row) == N
        parts.validate_coloring(N, edges, row, K, u)
        fresh.setdefault(u, []).append(row)
    ds.G['libarr'] = [np.array(lib[u] + fresh.get(u, []), dtype=np.int64) for u in range(N)]
    G['nbrs'], G['keys'] = expand(cert, q3nbrs, k2nbrs)
    G['cache'] = {k: ds.valid_assignments(k) for k in set(G['keys'])}
    G['declared'] = cert['declared']


def check_u(u):
    cov = ds.covered_mask(u, G['nbrs'], G['keys'], G['cache'])
    bad = [int(ci) for ci in np.nonzero(~cov)[0] if f'{ci}:{u}' not in G['declared']]
    return u, int((~cov).sum()), bad


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cert'); ap.add_argument('--workers', type=int, default=2)
    args = ap.parse_args(); t0 = time.time()
    with gzip.open(args.cert, 'rb') as f:
        cert = json.loads(f.read())
    print(f"{cert['n_configs']} configurations in {cert['n_groups']} groups, {len(cert['declared'])} declared pairs, {len(cert['fresh_rows'])} fresh rows", flush=True)
    undeclared_uncovered = 0; tot_unc = 0
    with Pool(args.workers, initializer=init, initargs=(args.cert,)) as pool:
        for u, nunc, bad in pool.imap_unordered(check_u, range(N), chunksize=1):
            tot_unc += nunc; undeclared_uncovered += len(bad)
            if bad:
                print(f'u={u}: {len(bad)} undeclared uncovered configurations: {bad[:10]}', flush=True)
            if u % 50 == 0:
                print(f'u={u} done; uncovered so far {tot_unc}, undeclared uncovered {undeclared_uncovered} ({time.time()-t0:.0f}s)', flush=True)
    Uhat = {}
    for key in cert['declared']:
        ci, u = key.split(':'); Uhat.setdefault(int(ci), set()).add(int(u))
    hist = {}
    for ci in range(cert['n_configs']):
        k = len(Uhat.get(ci, ())); hist[k] = hist.get(k, 0) + 1
    print('|Û(A)| histogram', dict(sorted(hist.items())), flush=True)
    ok = undeclared_uncovered == 0 and max(hist) <= 4 and tot_unc == len(cert['declared'])
    print(f'uncovered pairs {tot_unc}, declared pairs {len(cert["declared"])} (all uncovered declared: {undeclared_uncovered == 0}); max |Û(A)| = {max(hist)} (< 5: {max(hist) <= 4})')
    print(f'all_checks={str(ok).lower()}  ({time.time()-t0:.0f}s)')


if __name__ == '__main__':
    main()
