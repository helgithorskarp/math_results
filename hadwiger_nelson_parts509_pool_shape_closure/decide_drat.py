#!/usr/bin/env python3
"""Cardinality decision instances over the certified killing-set family, with DRAT proofs.

--mode pool : variables x_v for v in U; clauses OR_{v in D} x_v for every killing set D,
              plus at most k of the x_v.  UNSAT  =>  every blocking X has |X| >= k+1.
--mode sonly: variables x_v for v in S only, clauses restricted to the killing sets with
              D subset S (these certify L u (S \\ D) u Q5 is 4-colourable), plus at most k.
              UNSAT  =>  h_S >= k+1, i.e. every blocking X keeps at least k+1 vertices of S.
The CNF is built with the self-contained Sinz encoder of cardenc.py; CaDiCaL emits a DRAT
proof which drat-trim checks, so the bound does not rest on solver optimality claims.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pool5 import Pool
import cardenc

ap = argparse.ArgumentParser()
ap.add_argument('--mode', choices=['pool', 'sonly'], default='pool')
ap.add_argument('--k', type=int, required=True)
ap.add_argument('--family', default=str(HERE / 'family_min.json'))
ap.add_argument('--extra', nargs='*', default=[str(HERE / 'accumulated_killing_sets.jsonl')])
ap.add_argument('--out', default=str(HERE / 'drat'))
ap.add_argument('--cadical', default='/scratch/cadical-package/usr/bin/cadical')
ap.add_argument('--drat-trim', default='/scratch/drat-trim-package/usr/bin/drat-trim')
ap.add_argument('--no-check', action='store_true')
args = ap.parse_args()
out = Path(args.out); out.mkdir(exist_ok=True)
P = Pool()
ground = P.U if args.mode == 'pool' else P.S
gset = set(ground)
xid = {v: i + 1 for i, v in enumerate(ground)}
fam = {frozenset(d) for d in json.loads(Path(args.family).read_text())['sets']}
for path in args.extra:
    if Path(path).exists():
        for line in open(path):
            if line.strip():
                try:
                    fam.add(frozenset(json.loads(line)['D']))
                except Exception:
                    pass
use = [D for D in fam if D <= gset]
print(f'mode={args.mode} k={args.k}: {len(use)} usable killing sets of {len(fam)}', flush=True)
nv = len(ground)
clauses = [sorted(xid[v] for v in D) for D in sorted(use, key=lambda d: (len(d), sorted(d)))]
cl, nv = cardenc.atmost_tot([xid[v] for v in ground], args.k, nv)
clauses += cl
name = f'{args.mode}_k{args.k}'
cnf = out / f'{name}.cnf'
with cnf.open('w') as f:
    f.write(f'p cnf {nv} {len(clauses)}\n')
    for c in clauses:
        f.write(' '.join(map(str, c)) + ' 0\n')
print(f'{cnf}: {nv} vars {len(clauses)} clauses sha256 {hashlib.sha256(cnf.read_bytes()).hexdigest()}', flush=True)
if args.no_check:
    sys.exit(0)
proof = out / f'{name}.drat'
t = time.time()
r = subprocess.run([args.cadical, '--no-binary', str(cnf), str(proof)], capture_output=True, text=True)
verdict = 'UNSAT' if 's UNSATISFIABLE' in r.stdout else ('SAT' if 's SATISFIABLE' in r.stdout else 'UNKNOWN')
print(f'cadical: {verdict} in {time.time()-t:.0f}s', flush=True)
res = {'mode': args.mode, 'k': args.k, 'sets': len(use), 'vars': nv, 'clauses': len(clauses),
       'cnf_sha256': hashlib.sha256(cnf.read_bytes()).hexdigest(), 'verdict': verdict,
       'cadical_seconds': time.time() - t}
if verdict == 'UNSAT':
    t = time.time()
    r2 = subprocess.run([args.drat_trim, str(cnf), str(proof)], capture_output=True, text=True)
    res['drat_verified'] = 's VERIFIED' in r2.stdout
    res['drat_bytes'] = proof.stat().st_size
    res['drat_sha256'] = hashlib.sha256(proof.read_bytes()).hexdigest()
    res['drat_seconds'] = time.time() - t
    print(f'drat-trim: {"VERIFIED" if res["drat_verified"] else r2.stdout[-200:]} in {time.time()-t:.0f}s', flush=True)
(out / f'{name}.json').write_text(json.dumps(res, indent=1))
