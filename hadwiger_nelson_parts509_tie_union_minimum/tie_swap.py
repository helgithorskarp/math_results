#!/usr/bin/env python3
"""Swap closure of a 509-vertex 5-chromatic tie T = V − D + A (tie hopping).

Ambient: the exact level-2 ambient graph (V ∪ Q3(G) ∪ P2, 1808 points, exact unit-distance edges).
For every tie with A ⊆ P44 this ambient contains every point with >= 3 unit neighbours in T
(such a point has >= 3 neighbours in V ∪ P44 and is therefore in V ∪ Q3(G) ∪ P2(P44) by the
circumcentre argument and the exhaustive level-2 enumeration).
For each u ∈ T and each q ∉ T with >= 4 neighbours in T − u, decide whether T − u + q is 4-colourable
(witness colourings of T − u are shared across q, exactly as in the committed swap closure); the
instances with no witness (solver UNSAT) are the swaps of T; they are DRAT-checked at once.
|U_T(q)| >= 2 for some q would give a 508-vertex 5-chromatic unit-distance graph.
Output: hop/results/<tag>.json with U_T(q) lists, SAT statistics and DRAT reports.
"""
import json, sys, time, os, subprocess, hashlib
from pathlib import Path
from multiprocessing import Pool
HN = Path(os.environ.get('HN_SCRATCH', '/scratch/agents/researcher-4/hn'))
CADICAL = '/scratch/cadical-package/usr/bin/cadical'
DRAT = '/scratch/researcher-3-drat-trim/drat-trim'
K = 4
AMB = json.loads((HN / 'level2' / 'ambient_lvl2_edges.json').read_text())
NV = AMB['vertices']
ADJ = [set() for _ in range(NV)]
for a, b in AMB['edges']:
    ADJ[a].add(b); ADJ[b].add(a)
T = None; TSET = None; Q = None; TEDGES = None


def setup(tie_vertices):
    global T, TSET, Q, TEDGES
    T = sorted(tie_vertices); TSET = set(T)
    Q = sorted(q for q in range(NV) if q not in TSET and len(ADJ[q] & TSET) >= 4)
    TEDGES = [(a, b) for a in T for b in ADJ[a] if b in TSET and a < b]


def init(tv):
    setup(tv)


def triangle_avoiding(u):
    for a in T:
        if a == u:
            continue
        for b in ADJ[a] & TSET:
            if b == u or b <= a:
                continue
            for c in ADJ[a] & ADJ[b] & TSET:
                if c != u and c > b:
                    return (a, b, c)
    raise RuntimeError('no triangle')


def run_u(u):
    from pysat.solvers import Solver
    t0 = time.time()
    verts = [v for v in T if v != u]; vs = set(verts); idx = {v: i for i, v in enumerate(verts)}
    var = lambda v, c: idx[v] * K + c + 1
    X = len(verts)                                     # the added point's colour variables
    xvar = lambda c: X * K + c + 1
    cand = [q for q in Q if len(ADJ[q] & vs) >= 4]
    sel_base = (X + 1) * K
    clauses = [[var(v, c) for c in range(K)] for v in verts]
    clauses.append([xvar(c) for c in range(K)])
    for a, b in TEDGES:
        if a in vs and b in vs:
            for c in range(K):
                clauses.append([-var(a, c), -var(b, c)])
    tri = triangle_avoiding(u)
    for i, v in enumerate(tri):
        clauses.append([var(v, i)])
    for qi, q in enumerate(cand):
        s = sel_base + qi + 1
        for w in ADJ[q] & vs:
            for c in range(K):
                clauses.append([-s, -xvar(c), -var(w, c)])
    def rainbow(col, q):
        seen = set(col[w] for w in ADJ[q] & vs)
        return len(seen) == K
    uncovered = list(range(len(cand)))
    colourings = []; swaps = []; calls = 0
    with Solver(name='cadical195', bootstrap_with=clauses) as solver:
        while uncovered:
            qi = uncovered[0]
            calls += 1
            ok = solver.solve(assumptions=[sel_base + qi + 1])
            if not ok:
                swaps.append(cand[qi]); uncovered.pop(0); continue
            pos = set(l for l in solver.get_model() if l > 0)
            col = {}
            for v in verts:
                for c in range(K):
                    if var(v, c) in pos:
                        col[v] = c; break
            for a, b in TEDGES:
                if a in vs and b in vs:
                    assert col[a] != col[b]
            assert not rainbow(col, cand[qi])
            uncovered = [qj for qj in uncovered if rainbow(col, cand[qj])]
            colourings.append(col)
    return u, len(cand), calls, len(colourings), swaps, time.time() - t0


def drat_check(tie_vertices, u, q, tag):
    """DRAT-certify that T − u + q is not 4-colourable (pinned CNF)."""
    verts = sorted((set(tie_vertices) - {u}) | {q}); vs = set(verts); idx = {v: i for i, v in enumerate(verts)}
    var = lambda v, c: idx[v] * K + c + 1
    clauses = [[var(v, c) for c in range(K)] for v in verts]
    for a in verts:
        for b in ADJ[a] & vs:
            if a < b:
                for c in range(K):
                    clauses.append([-var(a, c), -var(b, c)])
    tri = None
    for a in verts:
        for b in ADJ[a] & vs:
            if b <= a:
                continue
            for c in ADJ[a] & ADJ[b] & vs:
                if c > b:
                    tri = (a, b, c); break
            if tri: break
        if tri: break
    for i, v in enumerate(tri):
        clauses.append([var(v, i)])
    text = f'p cnf {len(verts)*K} {len(clauses)}\n' + ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in clauses)
    work = HN / 'hop' / 'drat'; work.mkdir(exist_ok=True)
    cnf = work / f'{tag}_u{u}_q{q}.cnf'; proof = work / f'{tag}_u{u}_q{q}.drat'
    cnf.write_text(text)
    t = time.time()
    r = subprocess.run([CADICAL, '-q', str(cnf), str(proof)], capture_output=True, text=True)
    d = subprocess.run([DRAT, str(cnf), str(proof)], capture_output=True, text=True) if r.returncode == 20 else None
    ok = d is not None and 's VERIFIED' in d.stdout
    return {'u': u, 'q': q, 'vertices': len(verts), 'edges': (len(clauses) - len(verts) - 3) // K, 'cnf_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'cadical_rc': r.returncode, 'drat_verified': ok, 'proof_bytes': proof.stat().st_size if proof.exists() else 0, 'seconds': round(time.time() - t, 1)}


def main():
    spec = json.loads(sys.argv[1])          # {"D": [...], "A": [...], "tag": "..."}
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    D, A, tag = spec['D'], spec['A'], spec['tag']
    tv = sorted((set(range(509)) - set(D)) | set(A))
    assert len(tv) == 509
    setup(tv)
    out = HN / 'hop' / 'results' / f'{tag}.json'; out.parent.mkdir(exist_ok=True)
    print(f'tie {tag}: D={D} A={A}; |T|={len(T)}, edges {len(TEDGES)}, candidate points (>=4 nbrs in T): {len(Q)}', flush=True)
    t0 = time.time()
    U = {}; stats = []
    with Pool(workers, initializer=init, initargs=(tv,)) as pool:
        for u, ncand, calls, ncol, swaps, sec in pool.imap_unordered(run_u, T, chunksize=1):
            stats.append([u, ncand, calls, ncol, sec])
            for q in swaps:
                U.setdefault(q, []).append(u)
            if swaps:
                print(f'[{time.time()-t0:5.0f}s] u={u}: swaps {swaps} (cand {ncand}, calls {calls})', flush=True)
    print(f'closure done in {time.time()-t0:.0f}s: {sum(len(v) for v in U.values())} swap instances on {len(U)} points; max |U_T(q)| = {max((len(v) for v in U.values()), default=0)}', flush=True)
    reports = []
    for q, us in sorted(U.items()):
        for u in us:
            rep = drat_check(tv, u, q, tag); reports.append(rep)
            print(f'  DRAT u={u} q={q}: verified={rep["drat_verified"]} ({rep["seconds"]}s)', flush=True)
    records = {q: us for q, us in U.items() if len(us) >= 2}
    if records:
        print(f'!!! RECORD CANDIDATES (|U_T(q)| >= 2): {records}', flush=True)
    out.write_text(json.dumps({'tag': tag, 'D': D, 'A': A, 'T': tv, 'candidates': len(Q), 'U': {str(q): us for q, us in U.items()},
                               'records': {str(q): us for q, us in records.items()}, 'drat': reports, 'stats': stats,
                               'seconds': round(time.time() - t0)}))
    print(f'wrote {out}', flush=True)


if __name__ == '__main__':
    main()
