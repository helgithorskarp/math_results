#!/usr/bin/env python3
"""U(A) for arbitrary added point clusters A (points given by their unit
neighbour lists in V and their internal unit edges).

For each cluster and each vertex u: a proper 4-colouring of G - u that extends
to A (list colouring) certifies u notin U(A).  Libraries: base deletion rows,
swap-closure rows, pair-closure rows, triple-closure rows (triple_results/).
Unscreened (A, u) go to a fresh CaDiCaL instance with a conflict budget;
new witnesses are stored, budget/unsat instances are declared (u in U(A)).

Modes:
  --q2k q2k_extra.json     build the type (ii)/(iii) clusters of the delete-4-add-3 reduction
  --clusters FILE          arbitrary clusters: [{"id":..,"points":[{"nbrs":[..]},..],"edges":[[i,j],..]},..]
Output: JSON with per-cluster U(A), statuses, and witness rows for fresh SAT witnesses.
"""
from __future__ import annotations
import argparse, base64, hashlib, importlib.util, json, sys, time
from pathlib import Path
from multiprocessing import Pool

HERE = Path(__file__).resolve().parent
_CAND = [HERE.parent, Path.home() / 'math_results']
PAIRDIR = next(p / 'hadwiger_nelson_parts509_pair_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_pair_closure' / 'pair_certificate.json').exists())
SWAPDIR = next(p / 'hadwiger_nelson_parts509_swap_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_swap_closure' / 'swap_certificate.json').exists())
N, K = 509, 4
G = {}


def load_libraries():
    spec = importlib.util.spec_from_file_location('pc', PAIRDIR / 'pair_closure.py')
    pc = importlib.util.module_from_spec(spec); spec.loader.exec_module(pc)
    parts = pc.load_parts()
    points, edges, rows, fams, qnb, qq_edges = pc.load_all()
    cert = json.loads((PAIRDIR / 'pair_certificate.json').read_text())
    packed = base64.b64decode(cert['family_rows_base64'], validate=True)
    assert hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
    lib = [[rows[u]] + list(fams[u]) for u in range(N)]
    pos, RB = 0, (N - 1) // 4
    for u, size in enumerate(cert['family_sizes']):
        for _ in range(size):
            raw = packed[pos:pos + RB]; pos += RB
            vals = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
            it = iter(vals)
            row = [-1 if v == u else next(it) for v in range(N)]
            parts.validate_coloring(N, edges, row, K, u)
            lib[u].append(row)
    assert pos == len(packed)
    tdir = HERE / 'triple_results'
    ntrip = 0
    for u in range(N):
        f = tdir / f'u_{u:03d}.json'
        if f.exists():
            r = json.loads(f.read_text())
            for s in r['new_rows']:
                row = [-1 if ch == '-' else int(ch) for ch in s]
                parts.validate_coloring(N, edges, row, K, u)
                lib[u].append(row); ntrip += 1
    return parts, edges, lib, qnb, qq_edges, ntrip


def extends(coloring, u, nbrs, internal):
    """List-colouring test: point i may use colours absent from nbrs[i] - {u};
    internal edges force distinct colours."""
    n = len(nbrs)
    fms = []
    for nb in nbrs:
        used = 0
        for w in nb:
            if w != u:
                used |= 1 << coloring[w]
        fms.append(15 - used)
    assigned = []

    def rec(i):
        if i == n:
            return True
        for c in range(K):
            if not (fms[i] >> c & 1):
                continue
            if any(assigned[j] == c for (j, k) in internal if k == i) or any(assigned[k] == c for (j, k) in internal if j == i and k < i):
                continue
            assigned.append(c)
            if rec(i + 1):
                return True
            assigned.pop()
        return False
    return rec(0)


def triangle_avoiding(u, edges, adj):
    for a, b in edges:
        if u in (a, b):
            continue
        for w in sorted(adj[a] & adj[b]):
            if w != u:
                return a, b, w
    raise ValueError


def sat_test(u, nbrs, internal, budget, solver_name='cadical195', deleted=()):
    """4-colourability of G - {u} - deleted + A.  Returns (status, coloring_of_G_minus, point_colours)."""
    from pysat.solvers import Solver
    edges, adj = G['edges'], G['adj']
    dele = set(deleted) | {u}
    n = len(nbrs)
    var = lambda v, c: v * K + c + 1
    pv = lambda i, c: (N + i) * K + c + 1
    clauses = [[var(v, c) for c in range(K)] for v in range(N) if v not in dele]
    for a, b in edges:
        if a not in dele and b not in dele:
            for c in range(K):
                clauses.append([-var(a, c), -var(b, c)])
    for c, v in enumerate(triangle_avoiding(u, edges, adj)):
        if v not in dele:
            clauses.append([var(v, c)])
    for i, nb in enumerate(nbrs):
        clauses.append([pv(i, c) for c in range(K)])
        for w in nb:
            if w not in dele:
                for c in range(K):
                    clauses.append([-pv(i, c), -var(w, c)])
    for (i, j) in internal:
        for c in range(K):
            clauses.append([-pv(i, c), -pv(j, c)])
    with Solver(name=solver_name, bootstrap_with=clauses) as s:
        if budget > 0:
            s.conf_budget(budget)
            res = s.solve_limited()
        else:
            res = s.solve()
        if res is None:
            return 'budget', None, None
        if res is False:
            return 'unsat', None, None
        pos = {l for l in s.get_model() if l > 0}
        col = []
        for v in range(N):
            if v in dele:
                col.append(-1); continue
            cs = [c for c in range(K) if var(v, c) in pos]
            assert cs; col.append(cs[0])
        pc = []
        for i in range(n):
            cs = [c for c in range(K) if pv(i, c) in pos]
            assert cs; pc.append(cs[0])
        for a, b in edges:
            if a not in dele and b not in dele:
                assert col[a] != col[b]
        for i, nb in enumerate(nbrs):
            assert all(col[w] != pc[i] for w in nb if w not in dele)
        for (i, j) in internal:
            assert pc[i] != pc[j]
        return 'sat', col, pc


def init_worker(budget):
    parts, edges, lib, qnb, qq_edges, ntrip = load_libraries()
    adj = [set() for _ in range(N)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    G.update(edges=edges, lib=lib, adj=adj, budget=budget)


def process_cluster(cl):
    t0 = time.time()
    nbrs = [p['nbrs'] for p in cl['points']]
    internal = [tuple(e) for e in cl['edges']]
    lib = G['lib']
    U, status, new_rows = [], {}, []
    for u in range(N):
        if any(extends(col, u, nbrs, internal) for col in lib[u]):
            continue
        st, col, pc = sat_test(u, nbrs, internal, G['budget'])
        if st == 'sat':
            new_rows.append({'u': u, 'row': ''.join('-' if c < 0 else str(c) for c in col)})
            continue
        U.append(u); status[u] = st
    return {'id': cl['id'], 'U': U, 'status': {str(u): s for u, s in status.items()}, 'new_rows': new_rows,
            'seconds': round(time.time() - t0, 1)}


def build_q2k_clusters(path):
    ex = json.loads(Path(path).read_text())
    comp = json.loads((SWAPDIR / 'completion_points.json').read_text())
    q3nb = [list(r['neighbors']) for r in comp['points']]
    amb = json.loads((PAIRDIR / 'ambient_w3_edges.json').read_text())
    qq = set((a - N, b - N) for a, b in amb['edges'] if a >= N and b >= N)
    q2k = ex['q2k']
    cls = []
    for p, a2, a3, adj23 in ex['type_ii']:
        edges = [[0, 1], [0, 2]] + ([[1, 2]] if (min(a2, a3), max(a2, a3)) in qq else [])
        cls.append({'id': f'ii:{p}:{a2}:{a3}', 'type': 'ii', 'points': [{'nbrs': q2k[p]['neighbors'], 'q2k': p},
                    {'nbrs': q3nb[a2], 'q3': a2}, {'nbrs': q3nb[a3], 'q3': a3}], 'edges': edges})
    for p1, p2, a3 in ex['type_iiia']:
        cls.append({'id': f'iiia:{p1}:{p2}:{a3}', 'type': 'iiia', 'points': [{'nbrs': q2k[p1]['neighbors'], 'q2k': p1},
                    {'nbrs': q2k[p2]['neighbors'], 'q2k': p2}, {'nbrs': q3nb[a3], 'q3': a3}], 'edges': [[0, 1], [0, 2], [1, 2]]})
    for p1, p2, p3 in ex['type_iiibK']:
        cls.append({'id': f'iiib:{p1}:{p2}:{p3}', 'type': 'iiibK', 'points': [{'nbrs': q2k[p]['neighbors'], 'q2k': p} for p in (p1, p2, p3)],
                    'edges': [[0, 1], [0, 2], [1, 2]]})
    return cls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--q2k', default=None)
    ap.add_argument('--clusters', default=None)
    ap.add_argument('--out', required=True)
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--budget', type=int, default=20000)
    args = ap.parse_args()
    if args.q2k:
        cls = build_q2k_clusters(args.q2k)
    else:
        cls = json.loads(Path(args.clusters).read_text())
    print(f'{len(cls)} clusters', flush=True)
    t0 = time.time()
    results = []
    hist = {}
    with Pool(args.workers, initializer=init_worker, initargs=(args.budget,)) as pool:
        for r in pool.imap_unordered(process_cluster, cls, chunksize=1):
            results.append(r)
            hist[len(r['U'])] = hist.get(len(r['U']), 0) + 1
            if len(results) % 50 == 0 or len(r['U']) >= 4:
                print(f"{len(results)}/{len(cls)} {r['id']} |U|={len(r['U'])} U={r['U']} fresh={len(r['new_rows'])} {r['seconds']}s elapsed={time.time()-t0:.0f}s", flush=True)
    Path(args.out).write_text(json.dumps({'clusters': cls, 'results': results, 'histogram': hist}))
    print('|U| histogram', dict(sorted(hist.items())), flush=True)
    print('candidates |U|>=4:', [r['id'] for r in results if len(r['U']) >= 4], flush=True)


if __name__ == '__main__':
    main()
