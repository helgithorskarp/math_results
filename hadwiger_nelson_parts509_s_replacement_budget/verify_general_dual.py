#!/usr/bin/env python3
"""Solver-free check of the general-pool lower bound certificate (repository version).

Rebuilds U = S ∪ Q5 from the sibling directories, replays every weighted killing set's
witness colouring of L ∪ (U \ D) exactly, and checks the rational weak-duality inequality:
y ≥ 0 with Σ_{D∋v} y_D ≤ 1 for all v ∈ U gives, for every X ⊆ U with L ∪ X not
4-colourable (so X meets every D), |X| ≥ Σ_v Σ_{D∋v} y_D·[v∈X] ≥ Σ_D y_D |D ∩ X| ≥ Σ_D y_D."""
import json, sys, math, time
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAIR = HERE.parent / 'hadwiger_nelson_parts509_pair_closure'
SWAP = HERE.parent / 'hadwiger_nelson_parts509_swap_closure'
IFACE = HERE.parent / 'hadwiger_nelson_parts509_interface_lemma'
K = 4
cert = json.loads(Path(sys.argv[1]).read_text())
amb = json.loads((PAIR / 'ambient_w3_edges.json').read_text())
cp = json.loads((SWAP / 'completion_points.json').read_text())
adj = [set() for _ in range(amb['vertices'])]
for a, b in amb['edges']:
    adj[a].add(b); adj[b].add(a)
def has5(pt):
    return any(pt['x'][i] != '0' or pt['y'][i] != '0' for i in (2, 3, 6, 7))
Q5 = [509 + i for i, pt in enumerate(cp['points']) if has5(pt) and len(pt['neighbors']) >= 3]
U = list(range(374, 509)) + Q5
assert U == cert['pool'] and len(Q5) == 168
Uset = set(U); L = list(range(374)); Lset = set(L)
iface = json.loads((IFACE / 'interface_L.json').read_text())
IL = set(iface['interface_L'])
for u in U:
    assert all(l in IL for l in adj[u] & Lset)
witL = [row['witness_colouring_L'] for row in iface['classes']]
t = time.time()
colsum = {v: Fraction(0) for v in U}; total = Fraction(0)
for i, row in enumerate(cert['killing_sets']):
    D = set(row['D']); assert D and D <= Uset
    y = Fraction(row['y']); assert y > 0
    X = sorted(Uset - D)
    col = {v: int(c) for v, c in zip(L, witL[row['class_index']])}
    col.update({v: int(c) for v, c in zip(X, row['colouring_U_minus_D'])})
    assert len(row['colouring_U_minus_D']) == len(X)
    for v in col:
        assert 0 <= col[v] < K
        for u in adj[v]:
            if u in col and col[u] == col[v]:
                raise SystemExit(f'killing set {i}: witness improper on edge {u}-{v}')
    total += y
    for v in D:
        colsum[v] += y
assert all(c <= 1 for c in colsum.values()), 'dual infeasible'
assert total == Fraction(cert['bound']) and math.ceil(total) == cert['ceil']
print(f'replayed {len(cert["killing_sets"])} weighted killing sets exactly ({time.time()-t:.0f}s); dual sum {float(total):.4f}')
print(f'=> every X ⊆ U (S ∪ Q5) with L ∪ X not 4-colourable has |X| >= {cert["ceil"]}  (solver-free)')
print('all_checks=true')
