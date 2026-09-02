#!/usr/bin/env python3
"""Enumerate all interface colourings of one side (L or S) of the Parts-509 graph.

Usage: python3 enumerate_side.py S OUTDIR     (or L; the L run reproduces the 20 classes)
Writes OUTDIR/interface_<side>.json and OUTDIR/complete_<side>.cnf; the CNF is unsatisfiable
iff the class list is complete (certify with cadical + drat-trim).  Exact ambient edges from
../hadwiger_nelson_parts509_pair_closure/ambient_w3_edges.json.

Side L = vertices 0..373 (origin 0 included), side S = vertices 374..508 plus the
origin 0.  Cross edges are the 30 ambient edges between L and S; the interface
of a side is the set of its endpoints of cross edges (origin counted on both
sides).  We enumerate every proper 4-colouring of the side restricted to its
interface, with the origin fixed to colour 0 and modulo permutations of the
colours {1,2,3}: after each SAT call the six permuted copies of the found
interface colouring are blocked.  Output: classes (canonical interface colouring
strings), one full witness colouring per class, and the final CNF (side CNF +
blocking clauses) whose unsatisfiability certifies completeness.
"""
import json, sys, time, itertools
from pathlib import Path
from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent.parent / 'hadwiger_nelson_parts509_pair_closure'  # ambient_w3_edges.json lives there
side = sys.argv[1]
out = Path(sys.argv[2])
amb = json.loads((HERE / 'ambient_w3_edges.json').read_text())
VV = [(a, b) for a, b in amb['edges'] if a < 509 and b < 509]
assert len(VV) == 2442
L = set(range(374)); S = set(range(374, 509))
cross = [(a, b) if a in L else (b, a) for a, b in VV if (a in L) != (b in L)]
assert len(cross) == 30
if side == 'L':
    verts = sorted(L)
    inter = sorted({l for l, s in cross})
else:
    verts = sorted(S | {0})
    inter = sorted({s for l, s in cross} | {0})
vset = set(verts)
edges = [(a, b) for a, b in VV if a in vset and b in vset]
K = 4
idx = {v: i for i, v in enumerate(verts)}
var = lambda v, c: idx[v] * K + c + 1
clauses = [[var(v, c) for c in range(K)] for v in verts]
for a, b in edges:
    for c in range(K):
        clauses.append([-var(a, c), -var(b, c)])
clauses.append([var(0, 0)])
base_clauses = list(clauses)
perms = [(0,) + p for p in itertools.permutations((1, 2, 3))]
inter_nz = [v for v in inter if v != 0]
solver = Solver(name='cadical195', bootstrap_with=clauses)
classes = []
witnesses = []
blocking = []
t0 = time.time()
while solver.solve():
    model = solver.get_model()
    col = {}
    for v in verts:
        for c in range(K):
            if model[var(v, c) - 1] > 0:
                col[v] = c
                break
    assert col[0] == 0
    key = tuple(col[v] for v in inter_nz)
    canon = min(tuple(p[c] for c in key) for p in perms)
    classes.append(''.join(map(str, canon)))
    witnesses.append(''.join(str(col[v]) for v in verts))
    for p in perms:
        cl = [-var(v, p[col[v]]) for v in inter_nz]
        solver.add_clause(cl)
        blocking.append(cl)
    if len(classes) % 500 == 0:
        print(f'[{time.time()-t0:.0f}s] {len(classes)} classes', flush=True)
solver.delete()
print(f'side {side}: {len(classes)} interface classes, {time.time()-t0:.0f}s', flush=True)
assert len(set(classes)) == len(classes)
out.mkdir(parents=True, exist_ok=True)
(out / f'interface_{side}.json').write_text(json.dumps({
    'side': side, 'vertices': verts, 'interface': inter, 'interface_nonorigin': inter_nz,
    'cross_edges_L_S': cross, 'origin_colour': 0,
    'classes': classes, 'witness_colourings': witnesses,
    'seconds': round(time.time() - t0, 1)}))
# final CNF for DRAT completeness certificate
all_cl = base_clauses + blocking
with (out / f'complete_{side}.cnf').open('w') as f:
    f.write(f'p cnf {len(verts)*K} {len(all_cl)}\n')
    for cl in all_cl:
        f.write(' '.join(map(str, cl)) + ' 0\n')
print('wrote', out)
