#!/usr/bin/env python3
"""LP relaxations of the strengthened master problem for min |X|, X subset U blocking.

Constraints
  (H)  sum_{v in D} x_v >= 1                for every certified killing set D
  (G)  sum_{w in N(v) n U} x_w >= (4 - |N(v) n L|) x_v      for every v in U
       [valid for an inclusion-minimal blocking set: if v had at most 3 neighbours in
        L u X, a proper 4-colouring of L u (X \\ {v}) -- which exists by minimality --
        would extend to v]
  (S)  sum_{v in S} x_v >= 74               (solver-free bound of the committed budget)
"""
import json, sys, numpy as np
from pathlib import Path
from scipy.optimize import linprog
HERE = Path(__file__).resolve().parent
g = json.loads((HERE / 'pool_geometry.json').read_text())
L, U = list(g['L']), list(g['U'])
Lset, Uset = set(L), set(U)
adj = {v: set() for v in L + U}
for a, b in g['edges']:
    adj[a].add(b); adj[b].add(a)
fam = [frozenset(d) for d in json.loads((HERE / 'family_min.json').read_text())['sets']]
xv = {v: i for i, v in enumerate(U)}
n = len(U)
S = [v for v in U if v < 509]


def solve(useH=True, useG=False, useS=0):
    rows, rhs = [], []
    if useH:
        for D in fam:
            r = np.zeros(n)
            for v in D:
                r[xv[v]] = -1.0
            rows.append(r); rhs.append(-1.0)
    if useG:
        for v in U:
            r = np.zeros(n)
            dL = len(adj[v] & Lset)
            r[xv[v]] = max(0, 4 - dL)
            for w in adj[v] & Uset:
                r[xv[w]] -= 1.0
            rows.append(r); rhs.append(0.0)
    if useS:
        r = np.zeros(n)
        for v in S:
            r[xv[v]] = -1.0
        rows.append(r); rhs.append(-float(useS))
    res = linprog(c=np.ones(n), A_ub=np.array(rows), b_ub=np.array(rhs),
                  bounds=[(0, 1)] * n, method='highs')
    return res


if __name__ == '__main__':
    for useG in (False, True):
        for useS in (0, 74, 90):
            r = solve(True, useG, useS)
            x = r.x
            print(f'degcuts={useG} Scut={useS}: LP {r.fun:.4f} -> ceil {int(np.ceil(r.fun - 1e-9))}; '
                  f'mass S {sum(x[xv[v]] for v in U if v < 509):.2f} Q5 {sum(x[xv[v]] for v in U if v >= 509):.2f}; '
                  f'integral {sum(1 for t in x if t > 1 - 1e-7)}', flush=True)
