#!/usr/bin/env python3
"""Independent checker for the S-only replacement-budget certificate (repository version).

Rebuilds the pool U = S ∪ Q5 from the sibling directories and checks, without any solver:
  (1) every listed S-killing set D ⊆ S has a proper 4-colouring of L ∪ (U \ D), i.e.
      L ∪ (S \ D) ∪ Q5 is 4-colourable — so a set Y ⊆ S with L ∪ Y ∪ Q5 not 4-colourable
      must meet every D (in particular every singleton = forced vertex, every pair = irreplaceable pair);
  (2) the exact rational weak-duality certificate: weights y ≥ 0 on killing sets with
      Σ_{D∋v} y_D ≤ 1 for every v ∈ S prove |Y| ≥ Σ y_D for every such Y (solver-free bound);
  (3) the upper-bound set Y* ⊆ S: the pinned 4-colouring CNF of L ∪ Y* ∪ Q5 is rebuilt
      byte-for-byte and hashed; with --drat the supplied DRAT proof is checked by drat-trim.
Optionally (--milp / --cbc / --rc2) the minimum hitting set of the minimal killing sets is
recomputed exactly with HiGHS, CBC and/or the RC2 MaxSAT solver (solver-trusted bound).
"""
import argparse, json, time, hashlib, subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIR = HERE.parent / 'hadwiger_nelson_parts509_pair_closure'
SWAP = HERE.parent / 'hadwiger_nelson_parts509_swap_closure'
IFACE = HERE.parent / 'hadwiger_nelson_parts509_interface_lemma'
K = 4
ap = argparse.ArgumentParser()
ap.add_argument('certificate')
ap.add_argument('--drat', help='path to the DRAT proof for the upper-bound CNF')
ap.add_argument('--drat-trim', default='drat-trim')
ap.add_argument('--cnf-out', default='upper.cnf')
ap.add_argument('--milp', action='store_true', help='recompute the minimum hitting set with HiGHS (SciPy)')
ap.add_argument('--cbc', action='store_true', help='recompute it with CBC (PuLP)')
ap.add_argument('--rc2', action='store_true', help='recompute it with the RC2 MaxSAT solver (python-sat)')
args = ap.parse_args()

cert = json.loads(Path(args.certificate).read_text())
amb = json.loads((PAIR / 'ambient_w3_edges.json').read_text())
cp = json.loads((SWAP / 'completion_points.json').read_text())
assert amb['vertices'] == 509 + len(cp['points']) == 1667
adj = [set() for _ in range(amb['vertices'])]
for a, b in amb['edges']:
    adj[a].add(b); adj[b].add(a)
def has5(pt):
    return any(pt['x'][i] != '0' or pt['y'][i] != '0' for i in (2, 3, 6, 7))
Q5 = [509 + i for i, pt in enumerate(cp['points']) if has5(pt) and len(pt['neighbors']) >= 3]
S = list(range(374, 509)); U = S + Q5
assert len(Q5) == 168 and U == cert['pool'] and cert['Q5'] == Q5 and cert['S'] == S, 'pool mismatch'
Uset = set(U); L = list(range(374)); Lset = set(L)
iface = json.loads((IFACE / 'interface_L.json').read_text())
IL = set(iface['interface_L'])
for u in U:
    for l in adj[u] & Lset:
        assert l in IL, f'pool vertex {u} touches L outside the interface'
witL = [row['witness_colouring_L'] for row in iface['classes']]
for w in witL:
    for v in L:
        for u in adj[v]:
            if u < 374:
                assert w[u] != w[v]

# (1) replay every killing-set witness exactly
t = time.time()
rows = cert['killing_sets']
for i, row in enumerate(rows):
    D = set(row['D']); assert D and D <= set(S)
    X = sorted(Uset - D)
    col = {v: int(c) for v, c in zip(L, witL[row['class_index']])}
    assert len(row['colouring_U_minus_D']) == len(X)
    col.update({v: int(c) for v, c in zip(X, row['colouring_U_minus_D'])})
    for v in col:
        assert 0 <= col[v] < K
        for u in adj[v]:
            if u in col and col[u] == col[v]:
                raise SystemExit(f'killing set {i}: witness improper on edge {u}-{v}')
fam = sorted({frozenset(r['D']) for r in rows}, key=len)
keep = []
for a in fam:
    if not any(b < a for b in keep if len(b) < len(a)):
        keep.append(a)
forced = sorted(v for D in keep if len(D) == 1 for v in D)
pairs = sorted(tuple(sorted(D)) for D in keep if len(D) == 2)
cross = iface['cross_edges_L_S']
IS = sorted({b for a, b in cross})
print(f'(1) replayed {len(rows)} S-killing-set witnesses exactly ({time.time()-t:.0f}s); {len(fam)} distinct sets, {len(keep)} inclusion-minimal')
print(f'    forced vertices (singleton killing sets): {len(forced)}; equal to the S-side interface I_S: {forced == IS}')
print(f'    irreplaceable pairs (minimal killing sets of size 2): {len(pairs)} on {len({v for p in pairs for v in p})} vertices')

# (2) exact rational weak-duality certificate
lp = cert['lp_dual']
colsum = {v: Fraction(0) for v in S}; total = Fraction(0)
for i, y in lp['weights']:
    y = Fraction(y); assert y > 0 and 0 <= i < len(rows)
    total += y
    for v in rows[i]['D']:
        colsum[v] += y
assert all(c <= 1 for c in colsum.values()), 'dual infeasible'
assert total == Fraction(lp['bound']) and -(-total.numerator // total.denominator) == lp['ceil']
LB = lp['ceil']
print(f'(2) rational weak duality: {len(lp["weights"])} weighted killing sets, dual sum {float(total):.4f}')
print(f'    => every Y ⊆ S with L ∪ Y ∪ Q5 not 4-colourable has |Y| >= {LB}  (solver-free)')
sb = cert.get('solver_bound')
if sb:
    print(f'    recorded exact minimum hitting set of the family: {sb["minimum_hitting_set"]} ({sb["solver"]}) -- solver-trusted; recompute with --rc2/--milp/--cbc')

# (3) upper bound CNF
ub = cert['upper_bound']
Y = ub['Y']; assert set(Y) <= set(S)
assert all(set(D) & set(Y) for D in keep), 'Y* misses a killing set'
verts = sorted(Lset | set(Y) | set(Q5)); vs = set(verts); idx = {v: i for i, v in enumerate(verts)}
edges = sorted((a, b) for a, b in amb['edges'] if a in vs and b in vs)
var = lambda v, c: idx[v] * K + c + 1
clauses = [[var(v, c) for c in range(K)] for v in verts]
for a, b in edges:
    for c in range(K):
        clauses.append([-var(a, c), -var(b, c)])
tri = ub['pinned_triangle']
assert tri[1] in adj[tri[0]] and tri[2] in adj[tri[0]] and tri[2] in adj[tri[1]]
for i, v in enumerate(tri):
    clauses.append([var(v, i)])
text = f'p cnf {len(verts)*K} {len(clauses)}\n' + ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in clauses)
sha = hashlib.sha256(text.encode()).hexdigest()
assert sha == ub['cnf_sha256'], 'rebuilt CNF hash differs from the certificate'
assert len(verts) == ub['vertices'] and len(edges) == ub['edges']
Path(args.cnf_out).write_text(text)
print(f'(3) upper-bound set Y* has {len(Y)} vertices of S; CNF of L ∪ Y* ∪ Q5 rebuilt byte-for-byte: {len(verts)} vertices, {len(edges)} edges, sha256 {sha[:16]}...')
if args.drat:
    t = time.time()
    r = subprocess.run([args.drat_trim, args.cnf_out, args.drat], capture_output=True, text=True)
    assert 's VERIFIED' in r.stdout, 'drat-trim did not verify the proof'
    print(f'    drat-trim VERIFIED: L ∪ Y* ∪ Q5 is not 4-colourable ({time.time()-t:.0f}s) => h_S <= {len(Y)}')
else:
    print(f'    (DRAT proof not supplied; the upper bound h_S <= {len(Y)} rests on the recorded CaDiCaL/drat-trim run, proof sha256 {ub["proof_sha256"][:16]}...)')

# (4) optional exact recomputation of the minimum hitting set of the minimal family
if args.milp or args.cbc or args.rc2:
    xv = {v: i for i, v in enumerate(S)}
    vals = {}
    if args.milp:
        import numpy as np
        from scipy.optimize import milp, LinearConstraint, Bounds
        from scipy.sparse import lil_matrix
        A = lil_matrix((len(keep), len(S)))
        for i, D in enumerate(keep):
            for v in D:
                A[i, xv[v]] = 1
        t = time.time()
        res = milp(c=np.ones(len(S)), constraints=LinearConstraint(A.tocsr(), lb=np.ones(len(keep))), integrality=np.ones(len(S)), bounds=Bounds(0, 1), options={'mip_rel_gap': 0.0})
        assert res.status == 0, res.message
        vals['HiGHS'] = int(round(res.fun)); h = [v for v in S if res.x[xv[v]] > 0.5]
        assert all(set(D) & set(h) for D in keep)
        print(f'(4) HiGHS: minimum hitting set of the {len(keep)} minimal S-killing sets = {vals["HiGHS"]} ({time.time()-t:.0f}s)')
    if args.cbc:
        import pulp
        prob = pulp.LpProblem('h', pulp.LpMinimize)
        x = {v: pulp.LpVariable(f'x{v}', cat='Binary') for v in S}
        prob += pulp.lpSum(x.values())
        for D in keep:
            prob += pulp.lpSum(x[v] for v in D) >= 1
        t = time.time(); prob.solve(pulp.PULP_CBC_CMD(msg=0, threads=2, gapRel=0))
        vals['CBC'] = int(round(pulp.value(prob.objective)))
        print(f'(4) CBC: minimum hitting set = {vals["CBC"]} ({time.time()-t:.0f}s)')
    if args.rc2:
        from pysat.examples.rc2 import RC2
        from pysat.formula import WCNF
        xvar = {v: i + 1 for i, v in enumerate(S)}
        w = WCNF()
        for D in keep:
            w.append([xvar[v] for v in D])
        for v in S:
            w.append([-xvar[v]], weight=1)
        t = time.time()
        with RC2(w, solver='cd19', adapt=True, exhaust=False, minz=False) as rc2:
            mdl = rc2.compute(); vals['RC2'] = rc2.cost
        h = [v for v in S if xvar[v] in set(mdl)]
        assert all(set(D) & set(h) for D in keep) and len(h) == vals['RC2']
        print(f'(4) RC2 (core-guided MaxSAT, python-sat): minimum hitting set = {vals["RC2"]} ({time.time()-t:.0f}s)')
    assert len(set(vals.values())) == 1, f'solvers disagree: {vals}'
    m = next(iter(vals.values()))
    assert m >= LB and m <= len(Y)
    if sb:
        print(f'    recomputed value {m} {"matches" if m == sb["minimum_hitting_set"] else "DIFFERS FROM"} the recorded {sb["minimum_hitting_set"]}')
    print(f'    => (solver-trusted) every Y ⊆ S with L ∪ Y ∪ Q5 not 4-colourable has |Y| >= {m}')
print(f'summary: {LB} <= h_S (solver-free); {sb["minimum_hitting_set"] if sb else "?"} <= h_S (solver-trusted); h_S <= {len(Y)} (DRAT)')
print('all_checks=true')
