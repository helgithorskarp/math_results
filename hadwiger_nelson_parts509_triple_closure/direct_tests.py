#!/usr/bin/env python3
"""Direct 4-colourability tests G - D + A for every candidate (A, U(A)) with
|U(A)| >= 4 and every 4-subset D of U(A).  A witness colouring proves the
508-vertex graph 4-colourable; an UNSAT answer would be a record candidate
(to be certified separately with DRAT and exact geometry).

Input: candidates_508.json (Q3 triples) and/or extra_U.json (clusters).
Output: direct_witnesses.json
"""
from __future__ import annotations
import itertools, json, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cluster_U as cu

_CAND = [HERE.parent, Path.home() / 'math_results']
PAIRDIR = next(p / 'hadwiger_nelson_parts509_pair_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_pair_closure' / 'pair_certificate.json').exists())
SWAPDIR = next(p / 'hadwiger_nelson_parts509_swap_closure' for p in _CAND if (p / 'hadwiger_nelson_parts509_swap_closure' / 'swap_certificate.json').exists())
N = 509


def main():
    cu.init_worker(0)
    comp = json.loads((SWAPDIR / 'completion_points.json').read_text())
    q3nb = [list(r['neighbors']) for r in comp['points']]
    amb = json.loads((PAIRDIR / 'ambient_w3_edges.json').read_text())
    qq = set((a - N, b - N) for a, b in amb['edges'] if a >= N and b >= N)
    jobs = []
    p = HERE / 'candidates_508.json'
    if p.exists():
        for c in json.loads(p.read_text())['candidates']:
            A = c['A']
            nbrs = [q3nb[q] for q in A]
            internal = [(i, j) for i in range(3) for j in range(i + 1, 3) if (min(A[i], A[j]), max(A[i], A[j])) in qq]
            jobs.append({'id': 'q3:' + ':'.join(map(str, A)), 'nbrs': nbrs, 'internal': internal, 'U': c['U']})
    p = HERE / 'extra_U.json'
    if p.exists():
        ex = json.loads(p.read_text())
        byid = {c['id']: c for c in ex['clusters']}
        for r in ex['results']:
            if len(r['U']) >= 4:
                c = byid[r['id']]
                jobs.append({'id': r['id'], 'nbrs': [pt['nbrs'] for pt in c['points']],
                             'internal': [tuple(e) for e in c['edges']], 'U': r['U']})
    print(f'{len(jobs)} candidates', flush=True)
    out = []
    t0 = time.time()
    alerts = 0
    for jb in jobs:
        for D in itertools.combinations(jb['U'], 4):
            u = D[0]
            st, col, pc = cu.sat_test(u, jb['nbrs'], jb['internal'], 0, deleted=D[1:])
            rec = {'id': jb['id'], 'D': list(D), 'status': st}
            if st == 'sat':
                rec['row'] = ''.join('-' if c < 0 else str(c) for c in col)
                rec['point_colours'] = pc
            else:
                alerts += 1
                print('*** NOT 4-COLOURABLE (record candidate!) ***', jb['id'], D, st, flush=True)
            out.append(rec)
        print(f"{jb['id']} |U|={len(jb['U'])} done {time.time()-t0:.0f}s", flush=True)
    (HERE / 'direct_witnesses.json').write_text(json.dumps(out))
    print('alerts', alerts, flush=True)


if __name__ == '__main__':
    main()
