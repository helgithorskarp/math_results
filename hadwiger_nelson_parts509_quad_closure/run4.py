#!/usr/bin/env python3
"""Driver: for each vertex u, iterate (enumerate uncovered sets -> SAT-test a batch of disjoint open leaves ->
new witness rows or declared sets) until every uncovered set contains a declared set.
Output results/u_XXX.json: new_rows (colourings of G - u), declared (sets with status), statistics.
usage: run4.py [--workers 2] [--budget 20000] [--batch 24] [--only u1 u2 ...]
"""
import argparse, json, sys, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np
from paths import HERE, N, K
import uncovered_sets as enum4
OUT = HERE / 'results'
G = {}


def init_worker(budget):
    G['uni'] = enum4.Universe()
    parts, edges, lib, qnb, qq_edges, ntrip = enum4.load_libraries()
    adj = [set() for _ in range(N)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    G.update(edges=edges, lib=lib, adj=adj, budget=budget)
    from known_declared import load_known_declared
    G['known'] = {str(u): v for u, v in load_known_declared()[0].items()}


def triangle_avoiding(u):
    edges, adj = G['edges'], G['adj']
    for a, b in edges:
        if u in (a, b):
            continue
        for w in sorted(adj[a] & adj[b]):
            if w != u:
                return a, b, w
    raise ValueError


class SatU:
    """One incremental CaDiCaL instance for G - u; each tested point set gets fresh point variables and a selector."""
    def __init__(self, u):
        from pysat.solvers import Solver
        self.u = u
        edges = G['edges']
        var = lambda v, c: v * K + c + 1
        clauses = [[var(v, c) for c in range(K)] for v in range(N) if v != u]
        for a, b in edges:
            if a != u and b != u:
                for c in range(K):
                    clauses.append([-var(a, c), -var(b, c)])
        for c, v in enumerate(triangle_avoiding(u)):
            clauses.append([var(v, c)])
        self.s = Solver(name='cadical195', bootstrap_with=clauses)
        self.nv = N * K
        self.var = var
        self.calls = 0

    def test(self, A):
        uni, u, s = G['uni'], self.u, self.s
        nbrs = [uni.point_nbrs(p) for p in A]
        internal = [(i, j) for i in range(len(A)) for j in range(i + 1, len(A)) if uni.adjacent(A[i], A[j])]
        sel = self.nv + 1; base = sel
        pv = lambda i, c: base + 1 + i * K + c
        self.nv = pv(len(A) - 1, K - 1)
        var = self.var
        for i, nb in enumerate(nbrs):
            s.add_clause([-sel] + [pv(i, c) for c in range(K)])
            for w in nb:
                if w != u:
                    for c in range(K):
                        s.add_clause([-sel, -pv(i, c), -var(w, c)])
        for (i, j) in internal:
            for c in range(K):
                s.add_clause([-sel, -pv(i, c), -pv(j, c)])
        self.calls += 1
        if G['budget'] > 0:
            s.conf_budget(G['budget']); res = s.solve_limited(assumptions=[sel])
        else:
            res = s.solve(assumptions=[sel])
        if res is None:
            s.add_clause([-sel]); return 'budget', None
        if res is False:
            s.add_clause([-sel]); return 'unsat', None
        pos = set(l for l in s.get_model() if l > 0)
        s.add_clause([-sel])
        col = [-1 if v == u else next(c for c in range(K) if var(v, c) in pos) for v in range(N)]
        pc = [next(c for c in range(K) if pv(i, c) in pos) for i in range(len(A))]
        for a, b in G['edges']:
            if a != u and b != u:
                assert col[a] != col[b]
        for i, nb in enumerate(nbrs):
            assert all(col[w] != pc[i] for w in nb if w != u)
        for (i, j) in internal:
            assert pc[i] != pc[j]
        return 'sat', col

    def close(self):
        self.s.delete()


def work_u(args):
    u, batch = args
    t0 = time.time()
    uni = G['uni']
    rows = list(G['lib'][u])
    st = enum4.VertexState(uni, u, rows, G['known'][str(u)])
    sat = SatU(u)
    new_rows, declared, log = [], [], []
    passes = 0
    while True:
        leaves, stats = st.enumerate_uncovered()
        passes += 1
        log.append((passes, len(leaves), stats['nodes'], len(new_rows), len(declared), round(time.time() - t0, 1)))
        print(f'  u={u} pass {passes}: leaves {len(leaves)} (nodes {stats["nodes"]}), rows +{len(new_rows)}, declared {len(declared)}, SAT calls {sat.calls}, {time.time()-t0:.0f}s', flush=True)
        if not leaves:
            break
        # batch: disjoint leaves first (diverse witnesses), then fill up with further leaves; leaves that a witness
        # found earlier in the same batch already covers are skipped
        used, chosen, rest = set(), [], []
        for A in sorted(leaves, key=len):
            if used.isdisjoint(A) and len(chosen) < batch:
                chosen.append(A); used.update(A)
            else:
                rest.append(A)
        chosen += rest[:max(0, batch - len(chosen))]
        nrows0 = len(new_rows)
        for A in chosen:
            if len(new_rows) > nrows0 and not st.fails(A).all():
                continue
            t1 = time.time()
            status, col = sat.test(A)
            print(f'    u={u} SAT {A} -> {status} ({time.time()-t1:.1f}s)', flush=True)
            if status == 'sat':
                new_rows.append(col); st.add_row(col)
            else:
                declared.append((list(A), status)); st.declared.add(frozenset(A))
    sat.close()
    res = {'u': u, 'library_rows': len(G['lib'][u]), 'new_rows': [''.join('-' if x < 0 else str(x) for x in r) for r in new_rows],
           'declared': declared, 'sat_calls': sat.calls, 'passes': passes, 'log': log, 'seconds': round(time.time() - t0, 1),
           'final_families': [sum(x) for x in zip(*st.counts)]}
    OUT.mkdir(exist_ok=True)
    (OUT / f'u_{u:03d}.json').write_text(json.dumps(res))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=2); ap.add_argument('--budget', type=int, default=20000)
    ap.add_argument('--batch', type=int, default=24); ap.add_argument('--only', type=int, nargs='*', default=None)
    args = ap.parse_args()
    us = args.only if args.only is not None else [u for u in range(N) if not (OUT / f'u_{u:03d}.json').exists()]
    print(f'{len(us)} vertices to do', flush=True)
    t0 = time.time()
    tot_sat = tot_dec = tot_rows = 0
    with Pool(args.workers, initializer=init_worker, initargs=(args.budget,)) as pool:
        for i, r in enumerate(pool.imap_unordered(work_u, [(u, args.batch) for u in us], chunksize=1)):
            tot_sat += r['sat_calls']; tot_dec += len(r['declared']); tot_rows += len(r['new_rows'])
            nun = sum(1 for d in r['declared'] if d[1] == 'unsat'); nb = len(r['declared']) - nun
            print(f"[{time.time()-t0:7.0f}s] {i+1}/{len(us)} u={r['u']}: passes {r['passes']}, SAT calls {r['sat_calls']}, new rows {len(r['new_rows'])}, declared {len(r['declared'])} (unsat {nun}, budget {nb}), {r['seconds']}s | totals SAT {tot_sat} rows {tot_rows} declared {tot_dec}", flush=True)


if __name__ == '__main__':
    main()
