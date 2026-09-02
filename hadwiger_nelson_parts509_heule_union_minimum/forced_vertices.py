#!/usr/bin/env python3
"""Forced vertices of the tie-union accumulative graph A* = V ∪ P (P = added points of all
known 509-vertex ties).  A vertex u is *forced* if A* − u is 4-colourable (then every 5-chromatic
subgraph of A* contains u).  For each u ∈ A* run CaDiCaL on the pinned 4-colouring CNF of A* − u;
SAT gives a witness colouring (stored), UNSAT means A* − u still contains a 5-chromatic subgraph
(expected exactly for the vertices deleted by some known tie and for points not needed — anything
else is a new 5-chromatic subgraph of A* avoiding u).
Output: forced.json {'forced': [...], 'unforced': [...], 'witness': {u: colouring string over sorted(A*−u)}}
"""
import json, sys, time, subprocess, os
from pathlib import Path
from multiprocessing import Pool
HN = Path(os.environ.get('HN_ROOT', '/scratch/agents/researcher-4/hn'))  # scratch tree of the search (inputs/outputs); set HN_ROOT to relocate
CADICAL = os.environ.get('CADICAL', 'cadical')
K = 4
import os
amb = json.loads(Path(os.environ.get('HN_AMBIENT', str(HN / 'ambient_w3_edges.json'))).read_text())
UNION = Path(sys.argv[2]) if len(sys.argv) > 2 else HN / 'ties' / 'tie_union.json'
TU = json.loads(UNION.read_text())
STAR = sorted(TU['start']); STARSET = set(STAR)
EDGES = [(a, b) for a, b in amb['edges'] if a in STARSET and b in STARSET]
ADJ = {v: set() for v in STAR}
for a, b in EDGES:
    ADJ[a].add(b); ADJ[b].add(a)
WORK = HN / 'ties' / 'work'; WORK.mkdir(exist_ok=True)


def test(u):
    verts = [v for v in STAR if v != u]; vs = set(verts); idx = {v: i for i, v in enumerate(verts)}
    var = lambda v, c: idx[v] * K + c + 1
    clauses = [[var(v, c) for c in range(K)] for v in verts]
    for a, b in EDGES:
        if a in vs and b in vs:
            for c in range(K):
                clauses.append([-var(a, c), -var(b, c)])
    tri = None
    for a in verts:
        for b in sorted(ADJ[a] & vs):
            common = (ADJ[a] & ADJ[b] & vs)
            if common:
                tri = (a, b, min(common)); break
        if tri:
            break
    for i, v in enumerate(tri):
        clauses.append([var(v, i)])
    cnf = WORK / f'forced_{UNION.stem}_{u}.cnf'
    cnf.write_text(f'p cnf {len(verts)*K} {len(clauses)}\n' + ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in clauses))
    t0 = time.time()
    r = subprocess.run([CADICAL, '-q', str(cnf)], capture_output=True, text=True)
    cnf.unlink()
    dt = time.time() - t0
    if r.returncode == 10:
        model = set()
        for line in r.stdout.splitlines():
            if line.startswith('v'):
                model.update(int(x) for x in line[1:].split() if int(x) > 0)
        col = {}
        for v in verts:
            for c in range(K):
                if var(v, c) in model:
                    col[v] = c
        for a, b in EDGES:
            if a in vs and b in vs:
                assert col[a] != col[b]
        return u, 'SAT', dt, ''.join(str(col[v]) for v in verts)
    return u, 'UNSAT' if r.returncode == 20 else f'rc{r.returncode}', dt, None


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print(f'A*: {len(STAR)} vertices, {len(EDGES)} edges; testing {len(STAR)} single deletions', flush=True)
    out = Path(sys.argv[3]) if len(sys.argv) > 3 else HN / 'ties' / 'forced.json'
    res = {}
    if out.exists():
        prev = json.loads(out.read_text())
        for u in prev['forced']:
            res[u] = ('SAT', prev['witness'][str(u)])
        for u in prev['unforced']:
            res[u] = ('UNSAT', None)
        print(f'resumed {len(res)} results from {out}', flush=True)
    todo = [u for u in STAR if u not in res]
    t0 = time.time()
    with Pool(workers) as pool:
        for u, st, dt, wit in pool.imap_unordered(test, todo):
            res[u] = (st, wit)
            print(f'[{time.time()-t0:6.0f}s] u={u} -> {st} ({dt:.1f}s)', flush=True)
            if len(res) % 20 == 0 or len(res) == len(STAR):
                forced = sorted(u for u, (st, _) in res.items() if st == 'SAT')
                unforced = sorted(u for u, (st, _) in res.items() if st != 'SAT')
                out.write_text(json.dumps({'vertices': STAR, 'forced': forced, 'unforced': unforced,
                                           'witness': {str(u): w for u, (st, w) in res.items() if w}}))
    forced = sorted(u for u, (st, _) in res.items() if st == 'SAT')
    unforced = sorted(u for u, (st, _) in res.items() if st != 'SAT')
    print(f'forced {len(forced)}, unforced {len(unforced)}: {unforced}', flush=True)
    print('known deleted vertices:', TU['deleted_vertices'], flush=True)


if __name__ == '__main__':
    main()
