#!/usr/bin/env python3
"""Direct 4-colourability tests G - D + A for every candidate 4-set A (|Û(A)| >= 5, valid) and every 5-subset
D ⊆ Û(A).  A proper 4-colouring of (V \\ D) ∪ A is stored (colouring of V with -1 on D, plus the point colours).
usage: direct4.py [aggregate.json] [out.json] [--budget B (0 = complete)] [--all (also invalid candidates)]
"""
import argparse, json, sys, time, itertools
from pathlib import Path
from paths import HERE, N, K
import uncovered_sets as enum4


def sat_direct(uni, edges, A, D, budget):
    from pysat.solvers import Solver
    dele = set(D)
    nbrs = [uni.point_nbrs(p) for p in A]
    internal = [(i, j) for i, j in itertools.combinations(range(len(A)), 2) if uni.adjacent(A[i], A[j])]
    var = lambda v, c: v * K + c + 1
    pv = lambda i, c: (N + i) * K + c + 1
    clauses = [[var(v, c) for c in range(K)] for v in range(N) if v not in dele]
    for a, b in edges:
        if a not in dele and b not in dele:
            for c in range(K):
                clauses.append([-var(a, c), -var(b, c)])
    for i, nb in enumerate(nbrs):
        clauses.append([pv(i, c) for c in range(K)])
        for w in nb:
            if w not in dele:
                for c in range(K):
                    clauses.append([-pv(i, c), -var(w, c)])
    for i, j in internal:
        for c in range(K):
            clauses.append([-pv(i, c), -pv(j, c)])
    with Solver(name='cadical195', bootstrap_with=clauses) as s:
        if budget > 0:
            s.conf_budget(budget); res = s.solve_limited()
        else:
            res = s.solve()
        if res is None:
            return 'budget', None, None
        if res is False:
            return 'unsat', None, None
        pos = set(l for l in s.get_model() if l > 0)
        col = [-1 if v in dele else next(c for c in range(K) if var(v, c) in pos) for v in range(N)]
        pc = [next(c for c in range(K) if pv(i, c) in pos) for i in range(len(A))]
    for a, b in edges:
        if a not in dele and b not in dele:
            assert col[a] != col[b]
    for i, nb in enumerate(nbrs):
        assert all(col[w] != pc[i] for w in nb if w not in dele)
    for i, j in internal:
        assert pc[i] != pc[j]
    return 'sat', col, pc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('agg', nargs='?', default=str(HERE / 'aggregate4.json'))
    ap.add_argument('out', nargs='?', default=str(HERE / 'direct4.json'))
    ap.add_argument('--budget', type=int, default=0); ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    t0 = time.time()
    uni = enum4.Universe()
    parts, edges, lib, qnb, qq_edges, ntrip = enum4.load_libraries()
    agg = json.loads(Path(args.agg).read_text())
    cands = [c for c in agg['candidates'] if c['valid'] or args.all]
    print(f'{len(cands)} candidates ({len(agg["candidates"])} incl. invalid)', flush=True)
    out = []
    nbad = 0
    for ci, c in enumerate(cands):
        A = c['A']
        for D in itertools.combinations(sorted(c['Uhat']), 5):
            t1 = time.time()
            st, col, pc = sat_direct(uni, edges, A, D, args.budget)
            out.append({'A': A, 'D': list(D), 'status': st, 'colouring': None if col is None else ''.join('-' if x < 0 else str(x) for x in col), 'point_colours': pc})
            flag = '' if st == 'sat' else '   !!! NOT 4-COLOURABLE WITHIN BUDGET -> 508-vertex candidate'
            if st != 'sat': nbad += 1
            print(f'[{ci+1}/{len(cands)}] A={A} D={list(D)}: {st} ({time.time()-t1:.1f}s){flag}', flush=True)
    Path(args.out).write_text(json.dumps({'tests': out, 'n_candidates': len(cands), 'n_tests': len(out), 'not_sat': nbad}))
    print(f'done: {len(out)} tests, not-sat {nbad}, {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
