#!/usr/bin/env python3
"""Extract a small certified core for a closed value a and emit a checkable certificate.

Given the accumulated killing-set family, find a subfamily F such that

    { clause_D : D in F }  and  |R| = a+1, |A| = a

is unsatisfiable, shrink F by repeated unsat-core extraction, and write

  * certificate_a<a>.json : a, the core killing sets with their witness colourings;
  * master_a<a>.cnf       : the DIMACS instance rebuilt with the self-contained Sinz
                            encoder in cardenc.py (variables 1..135 = r_v for v in S in
                            increasing order, 136..303 = q_w for w in Q5, then auxiliaries);
  * a DRAT proof from CaDiCaL, checked with drat-trim.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pool5 import Pool
import cardenc
from pysat.solvers import Solver

ap = argparse.ArgumentParser()
ap.add_argument('--a', type=int, required=True)
ap.add_argument('--family', default=str(HERE / 'family_min.json'))
ap.add_argument('--extra', nargs='*', default=[str(HERE / 'accumulated_killing_sets.jsonl')])
ap.add_argument('--sources', nargs='*', default=[],
                help='extra jsonl files supplying witnesses for sets listed without one')
ap.add_argument('--out', default=str(HERE / 'certs'))
ap.add_argument('--passes', type=int, default=4)
ap.add_argument('--cadical', default='cadical')
ap.add_argument('--drat-trim', default='drat-trim')
ap.add_argument('--no-proof', action='store_true')
ap.add_argument('--greedy-limit', type=float, default=900.0)
args = ap.parse_args()
a = args.a
out = Path(args.out); out.mkdir(exist_ok=True)
P = Pool()
S, Q5 = P.S, P.Q5
Sset, Qset = set(S), set(Q5)
rid = {v: i + 1 for i, v in enumerate(S)}
qid = {w: len(S) + i + 1 for i, w in enumerate(Q5)}
NX = len(S) + len(Q5)

wit = {}
for path in [args.family] + args.extra:
    p = Path(path)
    if not p.exists():
        continue
    if p.suffix == '.json':
        for d in json.loads(p.read_text())['sets']:
            wit.setdefault(frozenset(d), None)
    else:
        for line in open(p):
            if line.strip():
                r = json.loads(line)
                wit.setdefault(frozenset(r['D']), r.get('witness'))
# witnesses for sets that were listed without one (--sources)
for path in args.sources:
    if Path(path).exists():
        for line in open(path):
            if line.strip():
                r = json.loads(line)
                k = frozenset(r['D'])
                if k in wit and wit[k] is None:
                    wit[k] = r['witness']
fam = [D for D in wit if wit[D] is not None]
print(f'{len(fam)} killing sets with witnesses ({len(wit)} total)', flush=True)


def clause_for(D):
    return [-rid[v] for v in D if v in Sset] + [qid[w] for w in D if w in Qset]


def core_pass(sets):
    s = Solver(name='cadical195')
    sel = {}
    nv = NX
    for i, D in enumerate(sets):
        nv += 1
        sel[nv] = D
        s.add_clause([-nv] + clause_for(D))
    cl, nv = cardenc.equals_tot([rid[v] for v in S], a + 1, nv)
    for c in cl:
        s.add_clause(c)
    cl, nv = cardenc.equals_tot([qid[w] for w in Q5], a, nv)
    for c in cl:
        s.add_clause(c)
    r = s.solve(assumptions=sorted(sel))
    if r:
        s.delete()
        return None
    core = [sel[abs(l)] for l in s.get_core()]
    s.delete()
    return core


cur = fam
for i in range(args.passes):
    t = time.time()
    c = core_pass(cur)
    if c is None:
        print(f'pass {i}: SATISFIABLE with {len(cur)} sets -- a={a} is not closed by this family')
        sys.exit(1)
    print(f'pass {i}: core {len(c)} of {len(cur)} in {time.time()-t:.0f}s', flush=True)
    if len(c) == len(cur):
        cur = c
        break
    cur = c

# greedy one-by-one deletion on the small core (time limited)
tg = time.time()
changed = True
while changed and len(cur) <= 600 and time.time() - tg < args.greedy_limit:
    changed = False
    for D in list(cur):
        if time.time() - tg > args.greedy_limit:
            break
        trial = [E for E in cur if E != D]
        if core_pass(trial) is not None:
            cur = trial
            changed = True
print(f'final core: {len(cur)} killing sets', flush=True)

nv = NX
clauses = [clause_for(D) for D in cur]
cl, nv = cardenc.equals_tot([rid[v] for v in S], a + 1, nv)
clauses += cl
cl, nv = cardenc.equals_tot([qid[w] for w in Q5], a, nv)
clauses += cl
cnf = out / f'master_a{a}.cnf'
with cnf.open('w') as f:
    f.write(f'p cnf {nv} {len(clauses)}\n')
    for c in clauses:
        f.write(' '.join(map(str, c)) + ' 0\n')
h = hashlib.sha256(cnf.read_bytes()).hexdigest()
print(f'wrote {cnf} ({nv} vars, {len(clauses)} clauses) sha256 {h}', flush=True)

cert = {'a': a, 'n_S': len(S), 'n_Q5': len(Q5), 'S': S, 'Q5': Q5,
        'killing_sets': [{'D': sorted(D), 'witness': wit[D]} for D in cur],
        'cnf_sha256': h, 'cnf_vars': nv, 'cnf_clauses': len(clauses)}
(out / f'certificate_a{a}.json').write_text(json.dumps(cert))
print('certificate written', flush=True)

if not args.no_proof:
    proof = out / f'master_a{a}.drat'
    t = time.time()
    r = subprocess.run([args.cadical, '--no-binary', str(cnf), str(proof)],
                       capture_output=True, text=True)
    ok = 's UNSATISFIABLE' in r.stdout
    print(f'cadical: {"UNSAT" if ok else r.stdout[-200:]} in {time.time()-t:.0f}s', flush=True)
    if ok:
        t = time.time()
        r2 = subprocess.run([args.drat_trim, str(cnf), str(proof)], capture_output=True, text=True)
        print(f'drat-trim: {"VERIFIED" if "s VERIFIED" in r2.stdout else r2.stdout[-300:]} '
              f'in {time.time()-t:.0f}s', flush=True)
        cert['drat_sha256'] = hashlib.sha256(proof.read_bytes()).hexdigest()
        cert['drat_bytes'] = proof.stat().st_size
        cert['drat_verified'] = 's VERIFIED' in r2.stdout
        (out / f'certificate_a{a}.json').write_text(json.dumps(cert))
