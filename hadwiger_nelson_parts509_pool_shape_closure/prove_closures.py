#!/usr/bin/env python3
"""Regenerate the DIMACS instance of each packed closure, prove it unsatisfiable with
CaDiCaL, check the DRAT proof with drat-trim, and record the sizes and hashes in
closures.json.  The instance is rebuilt exactly as verify_pool_closure.py rebuilds it."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cardenc

ap = argparse.ArgumentParser()
ap.add_argument('--dir', required=True, help='directory with killing_sets.json / closures.json')
ap.add_argument('--work', required=True, help='scratch directory for cnf and drat files')
ap.add_argument('--cadical', default='cadical')
ap.add_argument('--drat-trim', default='drat-trim')
ap.add_argument('--only', type=int, default=None)
args = ap.parse_args()
D = Path(args.dir); W = Path(args.work); W.mkdir(parents=True, exist_ok=True)
ks = json.loads((D / 'killing_sets.json').read_text())
cl = json.loads((D / 'closures.json').read_text())
S, Q5 = cl['S'], cl['Q5']
rid = {v: i + 1 for i, v in enumerate(S)}
qid = {w: len(S) + i + 1 for i, w in enumerate(Q5)}
Sset, Qset = set(S), set(Q5)
for a in sorted(cl['closures'], key=int):
    if args.only is not None and int(a) != args.only:
        continue
    info = cl['closures'][a]
    ai = int(a)
    nv = len(S) + len(Q5)
    clauses = []
    for i in info['sets']:
        Dl = ks['sets'][i]['D']
        clauses.append([-rid[v] for v in Dl if v in Sset] + [qid[w] for w in Dl if w in Qset])
    c1, nv = cardenc.equals_tot([rid[v] for v in S], ai + 1, nv); clauses += c1
    c2, nv = cardenc.equals_tot([qid[w] for w in Q5], ai, nv); clauses += c2
    txt = f'p cnf {nv} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)
    h = hashlib.sha256(txt.encode()).hexdigest()
    assert h == info['cnf_sha256'], (a, h, info['cnf_sha256'])
    cnf = W / f'master_a{a}.cnf'; cnf.write_text(txt)
    proof = W / f'master_a{a}.drat'
    t = time.time()
    r = subprocess.run([args.cadical, '--no-binary', str(cnf), str(proof)], capture_output=True, text=True)
    ok = 's UNSATISFIABLE' in r.stdout
    tc = time.time() - t
    if not ok:
        print(f'a={a}: cadical did NOT report UNSAT ({r.stdout[-120:]})', flush=True)
        continue
    t = time.time()
    r2 = subprocess.run([args.drat_trim, str(cnf), str(proof)], capture_output=True, text=True)
    ver = 's VERIFIED' in r2.stdout
    info['drat_bytes'] = proof.stat().st_size
    info['drat_sha256'] = hashlib.sha256(proof.read_bytes()).hexdigest()
    info['drat_verified'] = ver
    info['cadical_seconds'] = round(tc, 1)
    info['drat_trim_seconds'] = round(time.time() - t, 1)
    print(f'a={a}: cadical UNSAT {tc:.0f}s; drat-trim {"VERIFIED" if ver else "FAILED"} '
          f'{time.time()-t:.0f}s; proof {info["drat_bytes"]} bytes', flush=True)
(D / 'closures.json').write_text(json.dumps(cl, indent=1))
print('closures.json updated')
