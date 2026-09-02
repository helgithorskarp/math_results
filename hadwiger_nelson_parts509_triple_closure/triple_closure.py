#!/usr/bin/env python3
"""Three-point augmentation closure of the Parts-509 graph (layer 1).

For every vertex u and every 3-set A = {q1,q2,q3} of completion points (Q3:
points with >= 3 unit neighbours in V), decide whether G - u + A is
4-colourable by exhibiting a proper 4-colouring of G - u that extends to A
(list-colouring of the <= 3 internal unit edges of A).  Witnesses are found by
an incremental SAT solver with selector literals and validated directly;
coverage bookkeeping uses exact free-colour masks (bitsets over the witness
library) and never trusts the solver.

Declared instances (A, u): no witness found (solver UNSAT, or conflict budget
exhausted).  Over-declaration is conservative for the closure: U(A) only grows.
Triples containing a swap point of u or a declared pair of u are declared by
implication (not listed individually).

Output per vertex: triple_results/u_XXX.json
"""
from __future__ import annotations
import argparse, base64, hashlib, importlib.util, json, sys, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np

HERE = Path(__file__).resolve().parent
_CAND = [HERE.parent, Path.home() / 'math_results']
PAIRDIR = next(p / 'hadwiger_nelson_parts509_pair_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_pair_closure' / 'pair_certificate.json').exists())
SWAPDIR = next(p / 'hadwiger_nelson_parts509_swap_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_swap_closure' / 'swap_certificate.json').exists())
OUT = HERE / 'triple_results'
N, K = 509, 4
D = {}

POP8 = np.array([bin(i).count('1') for i in range(256)], dtype=np.int64)


def load_pair_module():
    spec = importlib.util.spec_from_file_location('pair_closure_mod', PAIRDIR / 'pair_closure.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_pair_rows(parts, edges):
    """Additional witness rows of the pair-closure certificate, per vertex."""
    cert = json.loads((PAIRDIR / 'pair_certificate.json').read_text())
    packed = base64.b64decode(cert['family_rows_base64'], validate=True)
    assert hashlib.sha256(packed).hexdigest() == cert['packed_rows_sha256']
    fams = [[] for _ in range(N)]
    pos = 0
    RB = (N - 1) // 4
    for u, size in enumerate(cert['family_sizes']):
        for _ in range(size):
            raw = packed[pos:pos + RB]
            pos += RB
            values = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
            it = iter(values)
            row = [-1 if v == u else next(it) for v in range(N)]
            parts.validate_coloring(N, edges, row, K, u)
            fams[u].append(row)
    assert pos == len(packed)
    declared = [set(tuple(sorted(p)) for p in lst) for lst in cert['declared_pairs']]
    return fams, declared


def init(solver_name, budget):
    pc = load_pair_module()
    parts = pc.load_parts()
    points, edges, rows, fams, qnb, qq_edges = pc.load_all()
    pfams, declared_pairs = load_pair_rows(parts, edges)
    nq = len(qnb)
    maxd = max(len(nb) for nb in qnb)
    nbarr = np.full((nq, maxd), -1, dtype=np.int64)
    for i, nb in enumerate(qnb):
        nbarr[i, :len(nb)] = nb
    qadj = [set() for _ in range(nq)]
    for a, b in qq_edges:
        qadj[a].add(b); qadj[b].add(a)
    # Q3-Q3 adjacency as boolean matrix
    QA = np.zeros((nq, nq), dtype=bool)
    for a, b in qq_edges:
        QA[a, b] = QA[b, a] = True
    # triples with >= 2 internal edges: paths a-b-c (b centre) and triangles
    t2 = set()
    for b in range(nq):
        nb = sorted(qadj[b])
        for i in range(len(nb)):
            for j in range(i + 1, len(nb)):
                t2.add(tuple(sorted((nb[i], b, nb[j]))))
    t2 = sorted(t2)
    sw = json.loads((PAIRDIR / 'swaps.json').read_text())
    spo = {}
    for q, uu in sw:
        spo.setdefault(uu, set()).add(q)
    adj = [set() for _ in range(N)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    D.update(edges=edges, rows=rows, fams=fams, pfams=pfams, declared_pairs=declared_pairs,
             qnb=qnb, nq=nq, nbarr=nbarr, qq_edges=qq_edges, qqset=set(qq_edges), qadj=qadj,
             QA=QA, t2=t2, solver=solver_name, budget=budget, swap_points_of=spo, adj=adj)


def free_masks(coloring, u):
    nbarr = D['nbarr']
    col = np.array(coloring + [-1], dtype=np.int64)
    c = col[nbarr]
    c = np.where(nbarr == u, -1, c)
    used = np.zeros(len(nbarr), dtype=np.int64)
    for k in range(K):
        used |= (c == k).any(axis=1).astype(np.int64) << k
    return 15 - used


def fm_scalar(coloring, u, q):
    used = 0
    for w in D['qnb'][q]:
        if w != u:
            used |= 1 << coloring[w]
    return 15 - used


def extends(coloring, u, A):
    """Exact scalar test: does the colouring of G-u extend to the point set A
    (list colouring with the internal unit edges of A)?"""
    fms = [fm_scalar(coloring, u, q) for q in A]
    qqset = D['qqset']
    n = len(A)
    internal = [(i, j) for i in range(n) for j in range(i + 1, n)
                if (min(A[i], A[j]), max(A[i], A[j])) in qqset]
    assigned = []

    def rec(i):
        if i == n:
            return True
        for c in range(K):
            if not (fms[i] >> c & 1):
                continue
            if any(assigned[j] == c for (j, k) in internal if k == i):
                continue
            assigned.append(c)
            if rec(i + 1):
                return True
            assigned.pop()
        return False
    return rec(0)


def path_ok(fa, fb, fc):
    """vectorised: exists cb in fb with fa\{cb} and fc\{cb} nonempty (path a-b-c)."""
    ok = np.zeros(len(fb), dtype=bool)
    for k in range(K):
        has = (fb >> k) & 1 == 1
        ok |= has & ((fa & ~(1 << k) & 15) != 0) & ((fc & ~(1 << k) & 15) != 0)
    return ok


def tri_ok(fa, fb, fc):
    ok = np.zeros(len(fa), dtype=bool)
    for a in range(K):
        for b in range(K):
            if b == a:
                continue
            for c in range(K):
                if c == a or c == b:
                    continue
                ok |= ((fa >> a) & 1 == 1) & ((fb >> b) & 1 == 1) & ((fc >> c) & 1 == 1)
    return ok


class Coverage:
    """Bitset coverage over the witness library for one vertex u."""

    def __init__(self, u):
        self.u = u
        self.nq = D['nq']
        self.m = 0
        self.W = 2                       # 128 colourings capacity, grows if needed
        self.alive = np.zeros((self.nq, self.W), dtype=np.uint64)     # point alive in colouring j
        self.fms = []                    # list of free-mask arrays
        qq = D['qq_edges']
        self.qa = np.array([a for a, b in qq], dtype=np.int64)
        self.qb = np.array([b for a, b in qq], dtype=np.int64)
        self.eok = np.zeros((len(qq), self.W), dtype=np.uint64)       # edge pair extendable in colouring j
        t2 = D['t2']
        self.t2 = t2
        self.t2a = np.array([t[0] for t in t2], dtype=np.int64)
        self.t2b = np.array([t[1] for t in t2], dtype=np.int64)
        self.t2c = np.array([t[2] for t in t2], dtype=np.int64)
        QA = D['QA']
        ab = QA[self.t2a, self.t2b]; bc = QA[self.t2b, self.t2c]; ac = QA[self.t2a, self.t2c]
        self.t2_kind = np.where(ab & bc & ac, 3, 2)     # 3 = triangle, 2 = path (some pair non-adjacent)
        # for paths determine the centre (the point adjacent to both others)
        centre = np.where(ab & ac, 0, np.where(ab & bc, 1, 2))
        self.t2_centre = centre
        self.t2_covered = np.zeros(len(t2), dtype=bool)

    def _grow(self):
        self.W += 2
        pad = np.zeros((self.nq, 2), dtype=np.uint64)
        self.alive = np.concatenate([self.alive, pad], axis=1)
        self.eok = np.concatenate([self.eok, np.zeros((len(self.eok), 2), dtype=np.uint64)], axis=1)

    def add(self, coloring):
        u = self.u
        fm = free_masks(coloring, u)
        j = self.m
        if j >= 64 * self.W:
            self._grow()
        w, bit = divmod(j, 64)
        b = np.uint64(1) << np.uint64(bit)
        al = fm != 0
        self.alive[al, w] |= b
        fa, fb = fm[self.qa], fm[self.qb]
        conflict = (fa == fb) & np.isin(fa, (1, 2, 4, 8))
        eo = al[self.qa] & al[self.qb] & ~conflict
        self.eok[eo, w] |= b
        # t2 triples
        if len(self.t2):
            fA, fB, fC = fm[self.t2a], fm[self.t2b], fm[self.t2c]
            ok = np.zeros(len(self.t2), dtype=bool)
            tri = self.t2_kind == 3
            if tri.any():
                ok[tri] = tri_ok(fA[tri], fB[tri], fC[tri])
            for ci, (x, y, z) in enumerate(((1, 0, 2), (0, 1, 2), (0, 2, 1))):
                sel = (~tri) & (self.t2_centre == ci)
                if sel.any():
                    f = [fA, fB, fC]
                    ok[sel] = path_ok(f[x][sel], f[y][sel], f[z][sel])
            self.t2_covered |= ok
        self.fms.append(fm)
        self.m += 1

    def popcount(self, arr):
        v = arr.view(np.uint8)
        return POP8[v].reshape(arr.shape[0], -1).sum(axis=1)

    def find_uncovered(self, limit, excluded, declared_pairs, rng=None, declared_triples=None):
        """Return up to `limit` uncovered, non-implied triples (canonical tuples)."""
        nq = self.nq
        alive = self.alive
        QA = D['QA']
        found = []
        found_set = set()
        order = np.arange(nq)
        if rng is not None:
            rng.shuffle(order)
        excl = np.zeros(nq, dtype=bool)
        for q in excluded:
            excl[q] = True
        dead_cnt = self.m - self.popcount(alive)
        dead_cnt[excl] = -1
        maxdead = int(dead_cnt.max()) if nq else 0
        # --- zero-edge and one-edge triples via pairs
        for q1 in order:
            q1 = int(q1)
            if excl[q1]:
                continue
            R = alive & alive[q1]                      # (nq, W)
            pc = self.popcount(R)
            # non-edge second points: pair covered by some colouring (pc>0), and a third
            # point must be dead on all of R -> pc <= maxdead; canonical q1 < q2
            cand = np.nonzero((pc > 0) & (pc <= maxdead) & ~excl & ~QA[q1])[0]
            cand = [int(q2) for q2 in cand if q2 > q1]
            # edge second points: use the edge-extendability mask
            ecand = []
            for q2 in D['qadj'][q1]:
                if excl[q2]:
                    continue
                ei = D['edge_index'][(min(q1, q2), max(q1, q2))]
                P = self.eok[ei]
                if not P.any():
                    continue                           # uncovered pair -> declared; skip
                if int(self.popcount(P[None, :])[0]) <= maxdead:
                    ecand.append((int(q2), P))
            for q2, P in [(q2, R[q2]) for q2 in cand] + ecand:
                edge12 = QA[q1, q2]
                if (min(q1, q2), max(q1, q2)) in declared_pairs:
                    continue
                z = ~((alive & P).any(axis=1))
                z &= ~QA[q1] & ~QA[q2] & ~excl
                z[q1] = False; z[q2] = False
                if not edge12:
                    z[:q2 + 1] = False
                for q3 in np.nonzero(z)[0]:
                    q3 = int(q3)
                    t = tuple(sorted((q1, q2, q3)))
                    if declared_triples is not None and t in declared_triples:
                        continue
                    if any((min(a, b), max(a, b)) in declared_pairs for a, b in ((q1, q3), (q2, q3))):
                        continue
                    if t in found_set:
                        continue
                    found.append(t); found_set.add(t)
                    if len(found) >= limit:
                        return found
            # pairs (q1,q2) uncovered as pairs (pc==0, not declared) should not exist after the pair closure
        # --- triples with >= 2 internal edges
        if len(self.t2):
            unc = np.nonzero(~self.t2_covered)[0]
            for i in unc:
                t = self.t2[i]
                if any(excl[q] for q in t):
                    continue
                if any((min(a, b), max(a, b)) in declared_pairs for a in t for b in t if a < b):
                    continue
                if declared_triples is not None and t in declared_triples:
                    continue
                found.append(t)
                if len(found) >= limit:
                    return found
        return found


def triangle_avoiding(u):
    adj = D['adj']
    for a, b in D['edges']:
        if u in (a, b):
            continue
        for w in sorted(adj[a] & adj[b]):
            if w != u:
                return a, b, w
    raise ValueError


def build_solver(u):
    from pysat.solvers import Solver
    edges, qnb, nq = D['edges'], D['qnb'], D['nq']
    var = lambda v, c: v * K + c + 1
    sel = lambda q: (N + nq) * K + q + 1
    clauses = [[var(v, c) for c in range(K)] for v in range(N) if v != u]
    for a, b in edges:
        if a != u and b != u:
            for c in range(K):
                clauses.append([-var(a, c), -var(b, c)])
    for c, v in enumerate(triangle_avoiding(u)):
        clauses.append([var(v, c)])
    for q, nb in enumerate(qnb):
        clauses.append([var(N + q, c) for c in range(K)])
        for w in nb:
            if w != u:
                for c in range(K):
                    clauses.append([-sel(q), -var(N + q, c), -var(w, c)])
    for a, b in D['qq_edges']:
        for c in range(K):
            clauses.append([-sel(a), -sel(b), -var(N + a, c), -var(N + b, c)])
    return Solver(name=D['solver'], bootstrap_with=clauses), var, sel


def run_u(u, batch=64, log_every=10):
    t0 = time.time()
    D['edge_index'] = {e: i for i, e in enumerate(D['qq_edges'])}
    edges, nq = D['edges'], D['nq']
    library = [D['rows'][u]] + list(D['fams'][u]) + list(D['pfams'][u])
    cov = Coverage(u)
    for col in library:
        cov.add(col)
    excluded = set(D['swap_points_of'].get(u, ()))
    declared_pairs = set(D['declared_pairs'][u])
    for (a, b) in declared_pairs:
        assert a in excluded or b in excluded or True
    declared = {}          # triple -> status ('unsat' | 'budget')
    new_rows = []
    calls = sat = unsat = budget_hit = 0
    rng = np.random.default_rng(u)
    solver, var, sel = build_solver(u)
    try:
        it = 0
        while True:
            it += 1
            unc = cov.find_uncovered(batch, excluded, declared_pairs, rng=rng if it > 1 else None,
                                     declared_triples=declared)
            if not unc:
                # final full deterministic scan
                unc = cov.find_uncovered(batch, excluded, declared_pairs, rng=None, declared_triples=declared)
                if not unc:
                    break
            for t in unc:
                # re-check against the current library (may have been covered by a fresh witness)
                if any(extends(col, u, t) for col in reversed(library)):
                    continue
                calls += 1
                if D['budget'] > 0:
                    solver.conf_budget(D['budget'])
                    res = solver.solve_limited(assumptions=[sel(q) for q in t])
                else:
                    res = solver.solve(assumptions=[sel(q) for q in t])
                if res is None:
                    budget_hit += 1
                    declared[t] = 'budget'
                    continue
                if res is False:
                    unsat += 1
                    declared[t] = 'unsat'
                    continue
                sat += 1
                pos = {l for l in solver.get_model() if l > 0}
                coloring = []
                for v in range(N):
                    if v == u:
                        coloring.append(-1)
                        continue
                    s = [c for c in range(K) if var(v, c) in pos]
                    assert s, 'uncoloured vertex'
                    coloring.append(s[0])
                for a, b in edges:
                    if a != u and b != u:
                        assert coloring[a] != coloring[b], 'improper colouring from solver'
                assert extends(coloring, u, t), 'solver model not compatible with the requested triple'
                cov.add(coloring)
                library.append(coloring)
                new_rows.append(coloring)
            if it % log_every == 0:
                print(f'  u={u} it={it} lib={len(library)} calls={calls} sat={sat} unsat={unsat} budget={budget_hit} t={time.time()-t0:.0f}s', flush=True)
    finally:
        solver.delete()
    result = {'u': u, 'library_initial': len(library) - len(new_rows), 'sat_calls': calls,
              'witnesses': sat, 'unsat': unsat, 'budget': budget_hit, 'budget_conflicts': D['budget'],
              'swap_points': sorted(excluded), 'declared_pairs': sorted(declared_pairs),
              'new_rows': [''.join('-' if c < 0 else str(c) for c in col) for col in new_rows],
              'declared_triples': sorted([list(t) + [s] for t, s in declared.items()]),
              'seconds': round(time.time() - t0, 1)}
    (OUT / f'u_{u:03d}.json').write_text(json.dumps(result))
    return result


def _run(args):
    u, batch = args
    return run_u(u, batch=batch)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--budget', type=int, default=20000, help='conflict budget per SAT call (0 = unlimited)')
    ap.add_argument('--batch', type=int, default=64)
    ap.add_argument('--vertices', default=None)
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    todo = [u for u in range(N) if not (OUT / f'u_{u:03d}.json').exists()]
    if args.vertices:
        todo = [int(x) for x in args.vertices.split(',')]
    print(f'{len(todo)} vertices to process', flush=True)
    t0 = time.time()
    tot_unsat = tot_budget = 0
    with Pool(args.workers, initializer=init, initargs=(args.solver, args.budget)) as pool:
        for r in pool.imap_unordered(_run, [(u, args.batch) for u in todo], chunksize=1):
            tot_unsat += r['unsat']; tot_budget += r['budget']
            print(f"u={r['u']:3d} lib0={r['library_initial']:3d} calls={r['sat_calls']:5d} wit={r['witnesses']:4d} unsat={r['unsat']:5d} budget={r['budget']:4d} {r['seconds']:7.1f}s elapsed={time.time()-t0:6.0f}s tot_unsat={tot_unsat} tot_budget={tot_budget}", flush=True)
    print('done', flush=True)


if __name__ == '__main__':
    main()
