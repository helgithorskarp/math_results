#!/usr/bin/env python3
"""Same decision problem as ihs_a.py, with a HiGHS MILP master instead of a SAT master.

For middle values of a the SAT master with two tight cardinality constraints is slow
(about 2 minutes per model at a = 30), while HiGHS finds a feasible (R, A) in a few
seconds, so many more killing sets are generated per hour.  Infeasibility reported by
HiGHS closes the value a (solver-trusted); the DRAT certificate is produced afterwards by
certify_a.py on the accumulated family.
"""
from __future__ import annotations
import argparse, json, random, sys, time
import numpy as np
from pathlib import Path
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pool5 import Pool

ap = argparse.ArgumentParser()
ap.add_argument('--a', type=int, required=True)
ap.add_argument('--out', default=None)
ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--family', default=str(HERE / 'family_min.json'))
ap.add_argument('--extra', nargs='*', default=[str(HERE / 'accumulated_killing_sets.jsonl')])
ap.add_argument('--time-limit', type=float, default=1e9)
ap.add_argument('--milp-limit', type=float, default=300.0)
args = ap.parse_args()
a = args.a
out = Path(args.out or (HERE / f'ihs_a{a}_milp')); out.mkdir(exist_ok=True)
rng = random.Random(args.seed)


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


P = Pool()
U = P.U; Uset = set(U); Sset = set(P.S)
xv = {v: i for i, v in enumerate(U)}
n = len(U)
fam = {frozenset(d) for d in json.loads(Path(args.family).read_text())['sets']}
for path in args.extra:
    if Path(path).exists():
        for line in open(path):
            if line.strip():
                try:
                    fam.add(frozenset(json.loads(line)['D']))
                except Exception:
                    pass
sets = [D for D in fam]
seen = set(sets)
log(f'a={a}: |R|={a+1}, |A|={a}; seed family {len(sets)} killing sets')

rowsI, colsI, vals = [], [], []
for i, D in enumerate(sets):
    for v in D:
        rowsI.append(i); colsI.append(xv[v]); vals.append(1.0)
nrow = len(sets)
# degree cuts for the added points (valid by the shape lemma: every w in A has at least
# four neighbours in L u X):  sum_{u in N(w) n U} x_u + |N(w) n L| - 4 x_w >= 0
degrows = []
for w in P.Q5:
    nb = sorted(P.adj[w] & Uset)
    dl = len(P.adj[w] & set(P.L))
    ent = {xv[u]: 1.0 for u in nb}
    ent[xv[w]] = ent.get(xv[w], 0.0) - 4.0
    degrows.append((ent, 4.0 - dl - 4.0))          # sum >= -(dl) + 4 - 4 ... see below
ndeg = len(degrows)
hfile = out / 'new_killing_sets.jsonl'
t0 = time.time(); rounds = 0; res_state = 'timeout'
Sidx = [xv[v] for v in U if v in Sset]
Qidx = [xv[v] for v in U if v not in Sset]
while time.time() - t0 < args.time_limit:
    rounds += 1
    r = list(rowsI) + [nrow] * len(Sidx) + [nrow + 1] * len(Qidx)
    c = list(colsI) + Sidx + Qidx
    v = list(vals) + [1.0] * (len(Sidx) + len(Qidx))
    for j, (ent, _) in enumerate(degrows):
        for col, coef in ent.items():
            r.append(nrow + 2 + j); c.append(col); v.append(coef)
    A = coo_matrix((np.array(v), (r, c)), shape=(nrow + 2 + ndeg, n)).tocsr()
    lo = np.concatenate([np.ones(nrow), [134.0 - a, float(a)],
                         np.array([-len(P.adj[w] & set(P.L)) for w in P.Q5], dtype=float)])
    hi = np.concatenate([np.full(nrow, np.inf), [134.0 - a, float(a)],
                         np.full(ndeg, np.inf)])
    obj = np.zeros(n)   # pure feasibility: HiGHS stops at the first integer solution
    t = time.time()
    res = milp(c=obj, constraints=LinearConstraint(A, lo, hi), integrality=np.ones(n),
               bounds=Bounds(0, 1), options={'time_limit': args.milp_limit, 'presolve': True})
    tm = time.time() - t
    if res.status == 2:
        res_state = 'infeasible'
        log(f'MASTER INFEASIBLE (HiGHS): a={a} closed. {rounds} rounds, {nrow} sets, {time.time()-t0:.0f}s')
        break
    if res.x is None:
        log(f'master status {res.status} ({res.message[:80]}); stopping')
        res_state = f'status{res.status}'
        break
    X = {U[i] for i in range(n) if res.x[i] > 0.5}
    Y = set(X)
    found = 0
    p = P.find_sat_pattern(Y)
    if p is None:
        res_state = 'record'
        log(f'*** BLOCKING SET, |X|={len(X)} ***')
        (out / 'record.json').write_text(json.dumps({'X': sorted(X)}))
        break
    while p is not None:
        D, wit = P.minimal_killing(Uset - Y, p, rng)
        Dk = frozenset(D)
        if Dk not in seen:
            seen.add(Dk); sets.append(Dk)
            for u in Dk:
                rowsI.append(nrow); colsI.append(xv[u]); vals.append(1.0)
            nrow += 1
            verts = sorted(set(P.L) | (Uset - Dk))
            with hfile.open('a') as f:
                f.write(json.dumps({'D': sorted(Dk), 'pattern': p,
                                    'witness': ''.join(str(wit[v]) for v in verts)}) + '\n')
            found += 1
        Y |= set(D)
        p = P.find_sat_pattern(Y)
    if rounds % 10 == 0:
        log(f'round {rounds}: +{found} sets (total {nrow}), |X|={len(X)} (S {len(X & Sset)}), '
            f'master {tm:.1f}s oracle {P.time:.0f}s elapsed {time.time()-t0:.0f}s')
(out / 'result.json').write_text(json.dumps({'a': a, 'result': res_state, 'rounds': rounds,
                                             'sets': nrow, 'elapsed': time.time() - t0}))
log(f'result={res_state} rounds={rounds} sets={nrow}')
