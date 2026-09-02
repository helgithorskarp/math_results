#!/usr/bin/env python3
"""DRAT-certified upper bound: L ∪ Y ∪ Q5 (a strict unit-distance graph, edges from the exact
ambient edge list) is not 4-colourable.  Builds the pinned 4-colouring CNF (one triangle pinned
to colours 0,1,2 — equisatisfiable by colour permutation), runs CaDiCaL with a DRAT proof and
checks the proof with drat-trim.  Writes a small report (CNF sha256, proof size, verdict)."""
import json, sys, time, subprocess, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAIR = HERE.parent / 'hadwiger_nelson_parts509_pair_closure'
CADICAL = 'cadical'
DRAT = 'drat-trim'
Y = json.loads(Path(sys.argv[1]).read_text()); Y = Y['Y'] if isinstance(Y, dict) else Y
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
amb = json.loads((PAIR / 'ambient_w3_edges.json').read_text())
pool = json.loads((HERE / 'pool_S.json').read_text())
verts = sorted(set(range(374)) | set(Y) | set(pool['Q5']))
vs = set(verts); idx = {v: i for i, v in enumerate(verts)}
edges = sorted((a, b) for a, b in amb['edges'] if a in vs and b in vs)
n = len(verts); K = 4
var = lambda v, c: idx[v] * K + c + 1
clauses = [[var(v, c) for c in range(K)] for v in verts]
for a, b in edges:
    for c in range(K):
        clauses.append([-var(a, c), -var(b, c)])
# pin a triangle
adj = {v: set() for v in verts}
for a, b in edges:
    adj[a].add(b); adj[b].add(a)
tri = None
for a in verts:
    for b in adj[a]:
        for c in adj[a] & adj[b]:
            tri = (a, b, c); break
        if tri: break
    if tri: break
assert tri
for i, v in enumerate(tri):
    clauses.append([var(v, i)])
cnf = out / 'upper.cnf'
with cnf.open('w') as f:
    f.write(f'p cnf {n*K} {len(clauses)}\n')
    for cl in clauses:
        f.write(' '.join(map(str, cl)) + ' 0\n')
sha = hashlib.sha256(cnf.read_bytes()).hexdigest()
print(f'graph: {n} vertices ({len(Y)} of S, 168 Q5, 374 L), {len(edges)} edges; CNF {len(clauses)} clauses sha256 {sha}', flush=True)
t = time.time()
proof = out / 'upper.drat'
r = subprocess.run([CADICAL, '-q', str(cnf), str(proof)], capture_output=True, text=True)
verdict = 'UNSAT' if r.returncode == 20 else 'SAT' if r.returncode == 10 else f'rc{r.returncode}'
print(f'cadical: {verdict} in {time.time()-t:.1f}s; proof {proof.stat().st_size if proof.exists() else 0} bytes', flush=True)
if verdict == 'UNSAT':
    t = time.time()
    d = subprocess.run([DRAT, str(cnf), str(proof)], capture_output=True, text=True)
    ok = 's VERIFIED' in d.stdout
    print(f'drat-trim: {"VERIFIED" if ok else "FAILED"} in {time.time()-t:.1f}s', flush=True)
    json.dump({'Y': sorted(Y), 'vertices': n, 'edges': len(edges), 'cnf_sha256': sha, 'pinned_triangle': tri,
               'cadical': verdict, 'proof_bytes': proof.stat().st_size, 'drat_trim_verified': ok,
               'proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest()}, (out / 'upper_report.json').open('w'))
