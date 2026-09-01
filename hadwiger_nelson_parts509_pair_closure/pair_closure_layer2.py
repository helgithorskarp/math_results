#!/usr/bin/env python3
"""Layers 2-3 of the two-point augmentation closure.

From the layer-1 results, U(A) = {u : G - u + A not 4-colourable} for every
pair A = {q1, q2} of completion points.  A 508-vertex graph G - D + A with
|D| = 3 can be 5-chromatic only if D is a subset of U(A) (each G - u + A with u
in D contains it).  For every pair with |U(A)| >= 3 and every 3-subset D of
U(A), this script tests G - D + A directly with a SAT solver.  SAT answers are
stored as validated witness colourings; an UNSAT answer would be a 508-vertex
5-chromatic unit-distance graph and is written out immediately for exact
certification.  Pairs with |U(A)| >= 2 are also listed (509-vertex ties).
"""
from __future__ import annotations
import argparse, itertools, json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pair_closure as L1

N, K = 509, 4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solver', default='cadical195')
    args = ap.parse_args()
    points, edges, rows, fams, qnb, qq_edges = L1.load_all()
    nq = len(qnb)
    qqset = set(qq_edges)
    U = {}
    n_unsat = 0
    for u in range(N):
        r = json.loads((L1.OUT / f'u_{u:03d}.json').read_text())
        for q1, q2 in r['unsat_pairs']:
            U.setdefault((q1, q2), set()).add(u)
            n_unsat += 1
        for q in r['swap_points']:
            for q2 in range(nq):
                if q2 != q:
                    U.setdefault((min(q, q2), max(q, q2)), set()).add(u)
    hist = {}
    for A, s in U.items():
        hist[len(s)] = hist.get(len(s), 0) + 1
    print(f'solver-declared UNSAT (pair, u) instances: {n_unsat}; pairs with U(A) nonempty: {len(U)}; |U(A)| histogram: {dict(sorted(hist.items()))}', flush=True)
    big = {A: sorted(s) for A, s in U.items() if len(s) >= 3}
    ties = {A: sorted(s) for A, s in U.items() if len(s) == 2}
    print(f'pairs with |U(A)| >= 3: {len(big)}; pairs with |U(A)| == 2: {len(ties)}', flush=True)
    # direct tests of G - D + A for |D| = 3
    from pysat.solvers import Solver
    adj = [set() for _ in range(N)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    found = []
    witnesses = []
    t0 = time.time()
    tests = 0
    for A, s in sorted(big.items()):
        q1, q2 = A
        for Dset in itertools.combinations(s, 3):
            tests += 1
            keep = [v for v in range(N) if v not in Dset]
            idx = {v: i for i, v in enumerate(keep)}
            m = len(keep)
            var = lambda i, c: i * K + c + 1
            clauses = [[var(i, c) for c in range(K)] for i in range(m + 2)]
            for a, b in edges:
                if a in idx and b in idx:
                    for c in range(K):
                        clauses.append([-var(idx[a], c), -var(idx[b], c)])
            for j, q in enumerate((q1, q2)):
                for w in qnb[q]:
                    if w in idx:
                        for c in range(K):
                            clauses.append([-var(m + j, c), -var(idx[w], c)])
            if (q1, q2) in qqset:
                for c in range(K):
                    clauses.append([-var(m, c), -var(m + 1, c)])
            with Solver(name=args.solver, bootstrap_with=clauses) as sol:
                ok = sol.solve()
                model = sol.get_model() if ok else None
            if not ok:
                rec = {'A': [q1, q2], 'D': list(Dset), 'note': 'solver reports G - D + A not 4-colourable: 508-VERTEX CANDIDATE'}
                found.append(rec)
                print('!!! 508-VERTEX CANDIDATE', rec, flush=True)
                (HERE / 'FOUND_508_pairs.json').write_text(json.dumps(found, indent=1))
                continue
            pos = {l for l in model if l > 0}
            col = [next(c for c in range(K) if var(i, c) in pos) for i in range(m + 2)]
            # validate directly
            for a, b in edges:
                if a in idx and b in idx:
                    assert col[idx[a]] != col[idx[b]]
            for j, q in enumerate((q1, q2)):
                for w in qnb[q]:
                    if w in idx:
                        assert col[m + j] != col[idx[w]]
            if (q1, q2) in qqset:
                assert col[m] != col[m + 1]
            full = [-1] * N
            for v, i in idx.items():
                full[v] = col[i]
            witnesses.append({'A': [q1, q2], 'D': list(Dset), 'coloring': ''.join('-' if c < 0 else str(c) for c in full), 'q_colors': [col[m], col[m + 1]]})
    print(f'direct triple tests: {tests}, witnesses: {len(witnesses)}, 508 candidates: {len(found)} ({time.time()-t0:.0f}s)', flush=True)
    out = {'U_histogram': {str(k): v for k, v in sorted(hist.items())},
           'pairs_with_U_ge3': [{'A': list(A), 'U': s} for A, s in sorted(big.items())],
           'pairs_with_U_eq2': [{'A': list(A), 'U': s} for A, s in sorted(ties.items())],
           'triple_witnesses': witnesses, 'candidates_508': found}
    (HERE / 'pair_layer2_results.json').write_text(json.dumps(out))
    print('written pair_layer2_results.json', flush=True)


if __name__ == '__main__':
    main()
