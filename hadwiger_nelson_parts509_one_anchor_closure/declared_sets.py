#!/usr/bin/env python3
"""Declared-set computation Û(A) for 4-point configurations (one-anchor family).

For each configuration A (points with over-inclusive vertex-neighbour lists and internal unit edges)
and each vertex u: (A, u) is *covered* if some stored proper 4-colouring of G − u (base colouring, swap,
pair and triple witness libraries) extends to A (list colouring: each point avoids the colours of its
surviving neighbours, adjacent points get distinct colours).  Uncovered pairs are tested by SAT
(CaDiCaL through PySAT, conflict budget; 'sat' answers add a fresh witness row; 'unsat'/'budget' are
declared).  Û(A) = declared vertices ⊇ U(A) = {u : G − u + A is 5-chromatic}.  A configuration can
give a 5-chromatic G − D + A with |D| = 5 only if D ⊆ Û(A), so |Û(A)| ≥ 5 is necessary; such
configurations are tested directly on every 5-subset.
usage: declared_sets.py CONFIGS OUT [--workers W] [--budget B]
"""
import argparse, json, sys, time, itertools
from pathlib import Path
from multiprocessing import Pool
import numpy as np
import importlib.util
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from paths import TRIPLE, N, K
import libraries
spec = importlib.util.spec_from_file_location('cu', TRIPLE / 'cluster_U.py')
cu = importlib.util.module_from_spec(spec); spec.loader.exec_module(cu)
cu.load_libraries = libraries.load_libraries      # triple rows from triple_certificate.json instead of triple_results/
G = {}


def valid_assignments(nedges_pattern):
    """All colour assignments of the 4 points respecting the internal edges (list of (i,j))."""
    out = []
    for a in itertools.product(range(K), repeat=4):
        if all(a[i] != a[j] for i, j in nedges_pattern):
            out.append(a)
    return np.array(out, dtype=np.int64)          # (na, 4)


def init_worker(budget):
    parts, edges, lib, qnb, qq_edges, ntrip = cu.load_libraries()
    adj = [set() for _ in range(N)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    cu.G.update(edges=edges, lib=lib, adj=adj, budget=budget)
    G['libarr'] = [np.array(lib[u], dtype=np.int64) for u in range(N)]     # (L_u, N) with -1 at u
    G['budget'] = budget


def covered_mask(u, confs_nbrs, confs_edges_key, assign_cache, batch=512):
    """Vectorised coverage of all configurations for one vertex u (batched by edge pattern)."""
    L = G['libarr'][u]                       # (L_u, N)
    Lu = len(L)
    bits = np.left_shift(1, np.where(L >= 0, L, 0)).astype(np.int64)
    bits[L < 0] = 0
    bits = np.concatenate([bits, np.zeros((Lu, 1), dtype=np.int64)], axis=1)   # column N = padding (no colour)
    out = np.zeros(len(confs_nbrs), dtype=bool)
    groups = {}
    for ci, key in enumerate(confs_edges_key):
        groups.setdefault(key, []).append(ci)
    for key, cis in groups.items():
        A = assign_cache[key]                # (na, 4)
        for s0 in range(0, len(cis), batch):
            chunk = cis[s0:s0 + batch]
            B = len(chunk)
            maxd = max(len(nb) for ci in chunk for nb in confs_nbrs[ci])
            idx = np.full((B, 4, maxd), N, dtype=np.int64)
            for bi, ci in enumerate(chunk):
                for pi, nb in enumerate(confs_nbrs[ci]):
                    nb = [w for w in nb if w != u]
                    idx[bi, pi, :len(nb)] = nb
            gathered = bits[:, idx]          # (L_u, B, 4, maxd)
            used = np.bitwise_or.reduce(gathered, axis=3)   # (L_u, B, 4)
            M = 15 & ~used
            ok = np.ones((Lu, B, len(A)), dtype=bool)
            for i in range(4):
                ok &= ((M[:, :, i][:, :, None] >> A[:, i][None, None, :]) & 1).astype(bool)
            cov = ok.any(axis=2).any(axis=0)  # (B,)
            for bi, ci in enumerate(chunk):
                out[ci] = bool(cov[bi])
    return out


def work_u(args):
    """One vertex u: vectorised coverage, then one incremental CaDiCaL solver for all uncovered configurations
    (configuration clauses guarded by a selector literal; solve under the assumption of that selector)."""
    from pysat.solvers import Solver
    u, confs = args
    t0 = time.time()
    nbrs_list = [[p['nbrs'] for p in c['points']] for c in confs]
    keys = [tuple(sorted(tuple(e) for e in c['edges'])) for c in confs]
    cache = {k: valid_assignments(k) for k in set(keys)}
    cov = covered_mask(u, nbrs_list, keys, cache)
    unc = [int(ci) for ci in np.nonzero(~cov)[0]]
    declared, new_rows, nsat = [], [], 0
    if unc:
        edges, adj = cu.G['edges'], cu.G['adj']
        var = lambda v, c: v * K + c + 1
        clauses = [[var(v, c) for c in range(K)] for v in range(N) if v != u]
        for a, b in edges:
            if a != u and b != u:
                for c in range(K):
                    clauses.append([-var(a, c), -var(b, c)])
        for c, v in enumerate(cu.triangle_avoiding(u, edges, adj)):
            if v != u:
                clauses.append([var(v, c)])
        nv = N * K
        pending = set(unc)
        with Solver(name='cadical195', bootstrap_with=clauses) as s:
            for ci in unc:
                if ci not in pending:
                    continue
                pending.discard(ci)
                nbrs = nbrs_list[ci]; internal = [tuple(e) for e in confs[ci]['edges']]
                sel = nv + 1; base = nv + 1
                pv = lambda i, c: base + 1 + i * K + c
                nv = pv(len(nbrs) - 1, K - 1)
                for i, nb in enumerate(nbrs):
                    s.add_clause([-sel] + [pv(i, c) for c in range(K)])
                    for w in nb:
                        if w != u:
                            for c in range(K):
                                s.add_clause([-sel, -pv(i, c), -var(w, c)])
                for (i, j) in internal:
                    for c in range(K):
                        s.add_clause([-sel, -pv(i, c), -pv(j, c)])
                if G['budget'] > 0:
                    s.conf_budget(G['budget']); res = s.solve_limited(assumptions=[sel])
                else:
                    res = s.solve(assumptions=[sel])
                nsat += 1
                if res is None:
                    declared.append((ci, 'budget')); s.add_clause([-sel]); continue
                if res is False:
                    declared.append((ci, 'unsat')); s.add_clause([-sel]); continue
                pos = {l for l in s.get_model() if l > 0}
                col = [-1 if v == u else next(c for c in range(K) if var(v, c) in pos) for v in range(N)]
                pc = [next(c for c in range(K) if pv(i, c) in pos) for i in range(len(nbrs))]
                for a, b in edges:
                    if a != u and b != u:
                        assert col[a] != col[b]
                for i, nb in enumerate(nbrs):
                    assert all(col[w] != pc[i] for w in nb if w != u)
                for (i, j) in internal:
                    assert pc[i] != pc[j]
                s.add_clause([-sel])
                new_rows.append({'u': u, 'row': ''.join('-' if x < 0 else str(x) for x in col)})
                # re-check the remaining uncovered configurations against the new colouring (cheap, vectorised)
                G['libarr'][u] = np.array([col], dtype=np.int64)
                rest = sorted(pending)
                if rest:
                    cov2 = covered_mask(u, [nbrs_list[cj] for cj in rest], [keys[cj] for cj in rest], cache)
                    for cj, ok in zip(rest, cov2):
                        if ok:
                            pending.discard(cj)
    return u, int((~cov).sum()), nsat, declared, new_rows, round(time.time() - t0, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('configs'); ap.add_argument('out')
    ap.add_argument('--workers', type=int, default=2); ap.add_argument('--budget', type=int, default=20000)
    ap.add_argument('--direct-budget', type=int, default=0)
    args = ap.parse_args()
    confs = json.loads(Path(args.configs).read_text())
    print(f'{len(confs)} configurations', flush=True)
    t0 = time.time()
    Uhat = {ci: [] for ci in range(len(confs))}
    status = {}
    rows = []
    tot_unc = tot_sat = 0
    with Pool(args.workers, initializer=init_worker, initargs=(args.budget,)) as pool:
        for u, nunc, nsat, declared, new_rows, secs in pool.imap_unordered(work_u, [(u, confs) for u in range(N)], chunksize=1):
            tot_unc += nunc; tot_sat += nsat; rows.extend(new_rows)
            for ci, st in declared:
                Uhat[ci].append(u); status[f'{ci}:{u}'] = st
            done = sum(1 for _ in [0])  # placeholder
            print(f'u={u}: uncovered {nunc}, SAT calls {nsat}, declared {len(declared)}, fresh rows {len(new_rows)} ({secs}s); total uncovered {tot_unc}, SAT {tot_sat}, elapsed {time.time()-t0:.0f}s', flush=True)
    hist = {}
    for ci, U in Uhat.items():
        hist[len(U)] = hist.get(len(U), 0) + 1
    cands = [ci for ci, U in Uhat.items() if len(U) >= 5]
    print('|Û(A)| histogram', dict(sorted(hist.items())), 'candidates (>=5):', len(cands), flush=True)
    result = {'configs_file': args.configs, 'n_configs': len(confs), 'Uhat': {str(ci): U for ci, U in Uhat.items() if U},
              'status': status, 'new_rows': rows, 'histogram': hist, 'candidates': cands, 'direct': []}
    # direct tests of 5-subsets for candidates
    if cands:
        init_worker(args.direct_budget)
        for ci in cands:
            c = confs[ci]
            nbrs = [p['nbrs'] for p in c['points']]; internal = [tuple(e) for e in c['edges']]
            for D in itertools.combinations(sorted(Uhat[ci]), 5):
                st, col, pc = cu.sat_test(D[0], nbrs, internal, args.direct_budget, deleted=D[1:])
                result['direct'].append({'config': ci, 'D': list(D), 'status': st,
                                         'row': None if col is None else ''.join('-' if x < 0 else str(x) for x in col),
                                         'point_colours': pc})
                print(f'DIRECT config {ci} {c["id"]} D={D}: {st}', flush=True)
                if st != 'sat':
                    print('!!! NOT 4-COLOURABLE (declared) — 508-vertex candidate, verify exactly', flush=True)
    Path(args.out).write_text(json.dumps(result))
    print(f'wrote {args.out}  total {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
