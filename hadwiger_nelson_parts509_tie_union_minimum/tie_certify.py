#!/usr/bin/env python3
"""Certify the candidate 509-vertex ties G - D + A (|D| = |A| = 3) left by the triple closure.

For every Q3 triple A with |U(A)| >= 3 (U(A) computed as in aggregate_triples.py, i.e. the
conservative superset: swap-implied, declared-pair-implied and explicitly declared vertices),
and every 3-subset D of U(A), build the pinned 4-colouring CNF of the strict unit-distance
graph on (V \ D) ∪ A (edges from the exact ambient edge list), run CaDiCaL with a DRAT proof
and check UNSAT proofs with drat-trim.  SAT answers are recorded with the witness colouring.
Output: ties/tie_results.json (one record per instance) and per-instance proofs under ties/drat/.
"""
from __future__ import annotations
import os, itertools, json, sys, time, hashlib, subprocess
from collections import defaultdict
from pathlib import Path
from multiprocessing import Pool

HN = Path(os.environ.get('HN_SCRATCH', '/scratch/agents/researcher-4/hn'))
TRI = HN / 'triple'
OUT = HN / 'ties'
PAIRDIR = Path.home() / 'math_results' / 'hadwiger_nelson_parts509_pair_closure'
CADICAL = '/scratch/cadical-package/usr/bin/cadical'
DRAT = '/scratch/researcher-3-drat-trim/drat-trim'
N, K, NQ = 509, 4, 1158

amb = json.loads((HN / 'ambient_w3_edges.json').read_text())
EDGES = [tuple(e) for e in amb['edges']]


def instances():
    swaps = json.loads((PAIRDIR / 'swaps.json').read_text())
    swap_u_of_point = defaultdict(set)
    for q, u in swaps:
        swap_u_of_point[q].add(u)
    U = defaultdict(set)
    for f in sorted((TRI / 'triple_results').glob('u_*.json')):
        r = json.loads(f.read_text()); u = r['u']; sp = set(r['swap_points'])
        for t in r['declared_triples']:
            U[tuple(t[:3])].add(u)
        for (a, b) in r['declared_pairs']:
            if a in sp or b in sp:
                continue
            for q in range(NQ):
                if q != a and q != b:
                    U[tuple(sorted((a, b, q)))].add(u)
    inst = []
    for A, us in U.items():
        full = set(us)
        for q in A:
            full |= swap_u_of_point.get(q, set())
        if len(full) >= 3:
            for D in itertools.combinations(sorted(full), 3):
                inst.append((list(A), list(D), len(full)))
    inst.sort()
    return inst


def build_cnf(A, D):
    verts = sorted((set(range(N)) - set(D)) | {N + a for a in A})
    vs = set(verts); idx = {v: i for i, v in enumerate(verts)}
    edges = [(a, b) for a, b in EDGES if a in vs and b in vs]
    var = lambda v, c: idx[v] * K + c + 1
    clauses = [[var(v, c) for c in range(K)] for v in verts]
    for a, b in edges:
        for c in range(K):
            clauses.append([-var(a, c), -var(b, c)])
    adj = {v: set() for v in verts}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    tri = None
    for a in verts:
        for b in sorted(adj[a]):
            common = adj[a] & adj[b]
            if common:
                tri = (a, b, min(common)); break
        if tri:
            break
    for i, v in enumerate(tri):
        clauses.append([var(v, i)])
    text = f'p cnf {len(verts)*K} {len(clauses)}\n' + ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in clauses)
    return verts, edges, tri, text


def run(job):
    A, D, usize = job
    tag = 'A' + '_'.join(map(str, A)) + '_D' + '_'.join(map(str, D))
    d = OUT / 'drat'; d.mkdir(exist_ok=True)
    verts, edges, tri, text = build_cnf(A, D)
    cnf = d / f'{tag}.cnf'; cnf.write_text(text)
    sha = hashlib.sha256(text.encode()).hexdigest()
    proof = d / f'{tag}.drat'
    t0 = time.time()
    r = subprocess.run([CADICAL, '-q', str(cnf), str(proof)], capture_output=True, text=True)
    t1 = time.time() - t0
    rec = {'A': A, 'D': D, 'U_size': usize, 'vertices': len(verts), 'edges': len(edges), 'pinned_triangle': tri,
           'cnf_sha256': sha, 'cadical_seconds': round(t1, 1)}
    if r.returncode == 20:
        t0 = time.time()
        dt = subprocess.run([DRAT, str(cnf), str(proof)], capture_output=True, text=True)
        ok = 's VERIFIED' in dt.stdout
        rec.update({'status': 'UNSAT', 'drat_trim_verified': ok, 'drat_seconds': round(time.time() - t0, 1),
                    'proof_bytes': proof.stat().st_size, 'proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest()})
    elif r.returncode == 10:
        model = set()
        for line in r.stdout.splitlines():
            if line.startswith('v'):
                model.update(int(x) for x in line[1:].split() if int(x) > 0)
        col = {}
        for i, v in enumerate(verts):
            for c in range(K):
                if i * K + c + 1 in model:
                    col[v] = c
        for a, b in edges:
            assert col[a] != col[b]
        rec.update({'status': 'SAT', 'colouring': ''.join(str(col[v]) for v in verts)})
        proof.unlink(missing_ok=True)
    else:
        rec.update({'status': f'rc{r.returncode}', 'stderr': r.stderr[-500:]})
    cnf.unlink()
    return rec


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    inst = instances()
    print(f'{len(inst)} tie instances (|U|>=3 triples: {len({tuple(a) for a,_,_ in inst})})', flush=True)
    res_path = OUT / 'tie_results.json'
    done = {}
    if res_path.exists():
        for r in json.loads(res_path.read_text())['results']:
            done[(tuple(r['A']), tuple(r['D']))] = r
    todo = [j for j in inst if (tuple(j[0]), tuple(j[1])) not in done]
    print(f'{len(done)} done, {len(todo)} to do', flush=True)
    t0 = time.time()
    with Pool(workers) as pool:
        for rec in pool.imap_unordered(run, todo):
            done[(tuple(rec['A']), tuple(rec['D']))] = rec
            print(f"[{time.time()-t0:7.0f}s] A={rec['A']} D={rec['D']} |U|={rec['U_size']} -> {rec['status']}"
                  f" ({rec.get('cadical_seconds')}s{', drat ' + str(rec.get('drat_trim_verified')) if rec['status']=='UNSAT' else ''})", flush=True)
            res_path.write_text(json.dumps({'results': [done[k] for k in sorted(done)]}))
    from collections import Counter
    print('summary', Counter(r['status'] for r in done.values()), flush=True)


if __name__ == '__main__':
    main()
