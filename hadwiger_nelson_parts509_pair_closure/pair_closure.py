#!/usr/bin/env python3
"""Two-point augmentation closure of the Parts-509 graph (layer 1).

For every vertex u and every unordered pair A = {q1, q2} of distinct completion
points (all points of the plane with >= 3 unit neighbours in V), decide whether
G - u + q1 + q2 (strict unit-distance graph, including a q1q2 edge when the two
points are at unit distance) is 4-colourable, by finding a proper 4-colouring
of G - u that extends to both points.  Witness colourings are found with an
incremental SAT solver (per-point selector literals) and validated directly;
coverage is replayed with exact free-colour masks that do not trust the solver.

Output per vertex u: pair_results/u_XXX.json with the new witness rows and the
list of pairs for which the solver reported UNSAT (these are 5-chromatic
510-vertex graphs; they are not part of the 4-colourability certificate).
"""
from __future__ import annotations
import argparse, base64, hashlib, importlib.util, json, sys, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
_CANDIDATES = [HERE.parent / 'hadwiger_nelson_parts509_criticality',
               Path.home() / 'math_results' / 'hadwiger_nelson_parts509_criticality']
BASE = next(p for p in _CANDIDATES if (p / 'parts509.py').exists())
_SW = [HERE.parent / 'hadwiger_nelson_parts509_swap_closure',
       Path.home() / 'math_results' / 'hadwiger_nelson_parts509_swap_closure']
SWAPDIR = next(p for p in _SW if (p / 'swap_certificate.json').exists())
OUT = HERE / 'pair_results'
N, K = 509, 4
D = {}


def load_parts():
    spec = importlib.util.spec_from_file_location('parts509_base', BASE / 'parts509.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_all():
    parts = load_parts()
    points, edges = parts.load_graph(BASE / 'parts509.vtx')
    cert = json.loads((BASE / 'certificate.json').read_text())
    packed = base64.b64decode(cert['deletion_colorings_base64'], validate=True)
    assert hashlib.sha256(packed).hexdigest() == cert['packed_deletion_colorings_sha256']
    rows = parts.unpack_deletion_rows(packed, N)
    for d, row in enumerate(rows):
        parts.validate_coloring(N, edges, row, K, d)
    comp = json.loads((SWAPDIR / 'completion_points.json').read_text())
    qnb = [tuple(r['neighbors']) for r in comp['points']]          # Q3 order, 1158 points
    amb = json.loads((HERE / 'ambient_w3_edges.json').read_text())
    assert amb['parts_vertices'] == N and amb['q3_points'] == len(qnb)
    qq_edges = sorted((a - N, b - N) for a, b in amb['edges'] if a >= N and b >= N)
    # consistency: Q3-V edges of the ambient reproduce the neighbour lists
    qv = {}
    for a, b in amb['edges']:
        if a < N <= b:
            qv.setdefault(b - N, []).append(a)
    for i, nb in enumerate(qnb):
        assert sorted(qv.get(i, [])) == sorted(nb)
    # swap-closure family rows
    sc = json.loads((SWAPDIR / 'swap_certificate.json').read_text())
    fam_packed = base64.b64decode(sc['family_rows_base64'], validate=True)
    assert hashlib.sha256(fam_packed).hexdigest() == sc['packed_rows_sha256']
    fams = [[] for _ in range(N)]
    pos = 0
    RB = (N - 1) // 4
    for u, size in enumerate(sc['family_sizes']):
        for _ in range(size):
            raw = fam_packed[pos:pos + RB]
            pos += RB
            values = [(b >> s) & 3 for b in raw for s in (0, 2, 4, 6)]
            it = iter(values)
            row = [-1 if v == u else next(it) for v in range(N)]
            parts.validate_coloring(N, edges, row, K, u)
            fams[u].append(row)
    assert pos == len(fam_packed)
    return points, edges, rows, fams, qnb, qq_edges


def init(solver_name):
    points, edges, rows, fams, qnb, qq_edges = load_all()
    nq = len(qnb)
    # neighbour index arrays for vectorised free-mask computation (pad with -1)
    maxd = max(len(nb) for nb in qnb)
    nbarr = np.full((nq, maxd), -1, dtype=np.int64)
    for i, nb in enumerate(qnb):
        nbarr[i, :len(nb)] = nb
    qa = np.array([a for a, b in qq_edges], dtype=np.int64)
    qb = np.array([b for a, b in qq_edges], dtype=np.int64)
    iu = np.triu_indices(nq, 1)
    D.update(edges=edges, rows=rows, fams=fams, qnb=qnb, nq=nq, nbarr=nbarr, qa=qa, qb=qb,
             qq_edges=qq_edges, solver=solver_name, iu=iu)
    adj = [set() for _ in range(N)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    D['adj'] = adj
    # certified swaps (q index in the Q4 list == index in the Q3 list, a prefix)
    sw = json.loads((HERE / 'swaps.json').read_text())
    spo = {}
    for q, uu in sw:
        assert len(qnb[q]) >= 4
        spo.setdefault(uu, set()).add(q)
    D['swap_points_of'] = spo


def free_masks(coloring, u):
    """4-bit mask of colours NOT used on N(q) - u, for every q (vectorised)."""
    nbarr = D['nbarr']
    col = np.array(coloring + [-1], dtype=np.int64)      # index -1 -> padding colour -1
    c = col[nbarr]                                        # (nq, maxd) colours, -1 for padding/u
    c = np.where(nbarr == u, -1, c)
    used = np.zeros(len(nbarr), dtype=np.int64)
    for k in range(K):
        used |= (c == k).any(axis=1).astype(np.int64) << k
    return 15 - used


def coverage_of(coloring, u):
    """Boolean (nq, nq) matrix: pair (i, j) compatible with the colouring."""
    fm = free_masks(coloring, u)
    ok = fm != 0
    cov = np.outer(ok, ok)
    # adjacent pairs with a single, identical free colour cannot both be coloured
    qa, qb = D['qa'], D['qb']
    conflict = (fm[qa] == fm[qb]) & np.isin(fm[qa], (1, 2, 4, 8))
    cov[qa[conflict], qb[conflict]] = False
    cov[qb[conflict], qa[conflict]] = False
    return cov


def compatible(coloring, u, q1, q2):
    """Scalar re-check of compatibility, from the neighbour lists directly."""
    fm = []
    for q in (q1, q2):
        used = 0
        for w in D['qnb'][q]:
            if w != u:
                used |= 1 << coloring[w]
        fm.append(15 - used)
    if fm[0] == 0 or fm[1] == 0:
        return False
    if (min(q1, q2), max(q1, q2)) in D['qqset']:
        return not (fm[0] == fm[1] and fm[0] in (1, 2, 4, 8))
    return True


def triangle_avoiding(u):
    adj = D['adj']
    for a, b in D['edges']:
        if u in (a, b):
            continue
        for w in sorted(adj[a] & adj[b]):
            if w != u:
                return a, b, w
    raise ValueError


def run_u(u):
    from pysat.solvers import Solver
    t0 = time.time()
    edges, rows, fams, qnb, nq = D['edges'], D['rows'], D['fams'], D['qnb'], D['nq']
    D['qqset'] = set(D['qq_edges'])
    iu = D['iu']
    family = [rows[u]] + list(fams[u])
    covered = np.zeros((nq, nq), dtype=bool)
    for col in family:
        covered |= coverage_of(col, u)
    initial_uncovered = int((~covered[iu]).sum())
    # pairs containing a certified swap point of u are 5-chromatic already with
    # one point; declare them without solver calls (implied by the swap certificate)
    trivial = []
    for q in D['swap_points_of'].get(u, ()):
        for q2 in range(nq):
            if q2 != q and not covered[min(q, q2), max(q, q2)]:
                trivial.append((min(q, q2), max(q, q2)))
                covered[min(q, q2), max(q, q2)] = True
    # ---- SAT encoding of G - u with selector-guarded completion points
    var = lambda v, c: v * K + c + 1                 # v in 0..N-1 (Parts) or N..N+nq-1 (Q3)
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
    new_rows, unsat_pairs, calls = [], [], 0
    with Solver(name=D['solver'], bootstrap_with=clauses) as solver:
        while True:
            unc = np.argwhere(~covered[iu])
            if len(unc) == 0:
                break
            # pick the uncovered pair whose points are 'hardest' (fewest covered partners)
            ii, jj = iu[0][unc[:, 0]], iu[1][unc[:, 0]]
            if len(unc) > 200:
                k = 0
            else:
                score = covered.sum(axis=1)
                k = int(np.argmin(score[ii] + score[jj]))
            q1, q2 = int(ii[k]), int(jj[k])
            calls += 1
            if not solver.solve(assumptions=[sel(q1), sel(q2)]):
                unsat_pairs.append((q1, q2))
                covered[q1, q2] = True     # handled (declared), not covered by a witness
                continue
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
            assert compatible(coloring, u, q1, q2), 'solver model not compatible with the requested pair'
            cov = coverage_of(coloring, u)
            assert cov[q1, q2]
            covered |= cov
            new_rows.append(coloring)
    result = {'u': u, 'initial_uncovered_pairs': initial_uncovered, 'sat_calls': calls,
              'swap_implied_pairs': len(trivial), 'swap_points': sorted(D['swap_points_of'].get(u, ())),
              'new_rows': [''.join('-' if c < 0 else str(c) for c in col) for col in new_rows],
              'unsat_pairs': unsat_pairs, 'seconds': round(time.time() - t0, 1)}
    (OUT / f'u_{u:03d}.json').write_text(json.dumps(result))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--workers', type=int, default=6)
    ap.add_argument('--vertices', default=None)
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    todo = [u for u in range(N) if not (OUT / f'u_{u:03d}.json').exists()]
    if args.vertices:
        todo = [int(x) for x in args.vertices.split(',')]
    print(f'{len(todo)} vertices to process', flush=True)
    t0 = time.time()
    tot_unsat = 0
    with Pool(args.workers, initializer=init, initargs=(args.solver,)) as pool:
        for r in pool.imap_unordered(run_u, todo, chunksize=1):
            tot_unsat += len(r['unsat_pairs'])
            print(f"u={r['u']:3d} uncovered0={r['initial_uncovered_pairs']:6d} swapimplied={r['swap_implied_pairs']:5d} calls={r['sat_calls']:4d} rows={len(r['new_rows']):4d} unsat={len(r['unsat_pairs']):4d} {r['seconds']:7.1f}s elapsed={time.time()-t0:6.0f}s total_unsat={tot_unsat}", flush=True)
    print('done', flush=True)


if __name__ == '__main__':
    main()
