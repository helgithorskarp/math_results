#!/usr/bin/env python3
"""Exact rational LP-dual certificate for a lower bound on the minimum hitting set.

Given killing sets D_1..D_m over U, any y >= 0 with sum_{i: v in D_i} y_i <= 1 for
every v in U certifies min hitting set >= sum_i y_i (weak LP duality: for a
hitting set X, |X| = sum_v 1[v in X] >= sum_v sum_{i: v in D_i} y_i 1[v in X]
= sum_i y_i |D_i ∩ X| >= sum_i y_i).  We take HiGHS's dual values, round them
to rationals, scale them down by the exact maximum column sum, and report the
exact rational bound, which is then a solver-free certificate (only the killing
sets' witnesses and the inequality check are needed to verify it).
"""
import json, sys, math
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

fam_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv) > 2 else None
if fam_path.endswith('.jsonl'):
    H = [json.loads(l) for l in Path(fam_path).read_text().splitlines() if l.strip()]
    rows = [r['D'] for r in H]
else:
    rows = [r['D'] for r in json.loads(Path(fam_path).read_text())['killing_sets']]
U = sorted({v for D in rows for v in D})
level = 1
pool = sorted(json.loads((Path(__file__).resolve().parent / 'pool_S.json').read_text())['W_S'])
if not set(U) <= set(pool):
    pool = list(range(374, json.loads((Path(__file__).resolve().parent / 'pool2.json').read_text())['vertices'])); level = 2
U = pool; xv = {v: i for i, v in enumerate(U)}
sets = sorted({frozenset(D) for D in rows}, key=len)
keep = []
for a in sets:
    if not any(b < a for b in keep if len(b) < len(a)):
        keep.append(a)
A = lil_matrix((len(keep), len(U)))
for i, D in enumerate(keep):
    for v in D:
        A[i, xv[v]] = 1
res = linprog(c=np.ones(len(U)), A_ub=-A.tocsr(), b_ub=-np.ones(len(keep)), bounds=(0, 1), method='highs')
assert res.status == 0
y = -res.ineqlin.marginals  # duals of -A x <= -1, nonnegative
y = np.maximum(y, 0.0)
# rationalise
yq = [Fraction(float(t)).limit_denominator(10**6) for t in y]
colsum = {v: Fraction(0) for v in U}
for i, D in enumerate(keep):
    if yq[i]:
        for v in D:
            colsum[v] += yq[i]
mx = max(colsum.values())
if mx > 1:
    yq = [t / mx for t in yq]
bound = sum(yq)
colsum = {v: Fraction(0) for v in U}
for i, D in enumerate(keep):
    for v in D:
        colsum[v] += yq[i]
assert all(c <= 1 for c in colsum.values())
print(f'LP value {res.fun:.4f}; exact rational dual bound {float(bound):.4f} -> minimum hitting set >= {math.ceil(bound)}; nonzero duals {sum(1 for t in yq if t)} of {len(keep)} sets')
if out_path:
    Path(out_path).write_text(json.dumps({'level': level, 'pool': U, 'sets': [sorted(D) for D in keep], 'dual': [str(t) for t in yq], 'bound': str(bound), 'ceil': math.ceil(bound)}))
    print('wrote', out_path)
