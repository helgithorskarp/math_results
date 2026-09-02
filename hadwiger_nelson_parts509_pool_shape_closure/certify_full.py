#!/usr/bin/env python3
"""Close a value of a with the full certified family, then shrink the certificate with the
unsatisfiable core that drat-trim extracts from CaDiCaL's proof.

Faster than assumption-based core extraction when the master instance is hard: one plain
UNSAT solve plus one drat-trim pass, instead of repeated solving under 6,800 assumptions.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pool5 import Pool
import cardenc

ap = argparse.ArgumentParser()
ap.add_argument('--a', type=int, required=True)
ap.add_argument('--family', default=str(HERE / 'family_min.json'))
ap.add_argument('--extra', nargs='*', default=[str(HERE / 'accumulated_killing_sets.jsonl')])
ap.add_argument('--work', default=str(HERE / 'full'))
ap.add_argument('--sources', nargs='*', default=[],
                help='extra jsonl files supplying witnesses for sets listed without one')
ap.add_argument('--out', default=str(HERE / 'certs'))
ap.add_argument('--cadical', default='cadical')
ap.add_argument('--drat-trim', default='drat-trim')
args = ap.parse_args()
a = args.a
W = Path(args.work); W.mkdir(exist_ok=True)
OUT = Path(args.out); OUT.mkdir(exist_ok=True)
P = Pool(); S, Q5 = P.S, P.Q5
rid = {v: i + 1 for i, v in enumerate(S)}
qid = {w: len(S) + i + 1 for i, w in enumerate(Q5)}
Sset, Qset = set(S), set(Q5)

wit = {}
for d in json.loads(Path(args.family).read_text())['sets']:
    wit.setdefault(frozenset(d), None)
for path in args.extra:
    if Path(path).exists():
        for line in open(path):
            if line.strip():
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                wit.setdefault(frozenset(r['D']), r.get('witness'))
for path in args.sources:
    if Path(path).exists():
        for line in open(path):
            if line.strip():
                r = json.loads(line)
                k = frozenset(r['D'])
                if k in wit and wit[k] is None:
                    wit[k] = r['witness']
fam = sorted([D for D in wit if wit[D] is not None], key=lambda d: (len(d), sorted(d)))
print(f'a={a}: {len(fam)} killing sets with witnesses', flush=True)


def clause_for(D):
    Dl = sorted(D)
    return [-rid[v] for v in Dl if v in Sset] + [qid[w] for w in Dl if w in Qset]


def write_cnf(sets, path):
    nv = len(S) + len(Q5)
    clauses = [clause_for(D) for D in sets]
    c1, nv = cardenc.equals_tot([rid[v] for v in S], a + 1, nv); clauses += c1
    c2, nv = cardenc.equals_tot([qid[w] for w in Q5], a, nv); clauses += c2
    txt = f'p cnf {nv} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)
    Path(path).write_text(txt)
    return nv, len(clauses), hashlib.sha256(txt.encode()).hexdigest()


cnf = W / f'full_a{a}.cnf'
nv, nc, h = write_cnf(fam, cnf)
print(f'full instance: {nv} vars, {nc} clauses', flush=True)
proof = W / f'full_a{a}.drat'
t = time.time()
r = subprocess.run([args.cadical, '--no-binary', str(cnf), str(proof)], capture_output=True, text=True)
if 's UNSATISFIABLE' not in r.stdout:
    print(f'NOT UNSAT: {r.stdout[-200:]}'); sys.exit(1)
print(f'cadical UNSAT in {time.time()-t:.0f}s, proof {proof.stat().st_size} bytes', flush=True)
core = W / f'core_a{a}.cnf'
t = time.time()
r2 = subprocess.run([args.drat_trim, str(cnf), str(proof), '-c', str(core)], capture_output=True, text=True)
print(f'drat-trim: {"VERIFIED" if "s VERIFIED" in r2.stdout else r2.stdout[-200:]} in {time.time()-t:.0f}s', flush=True)
want = {frozenset(clause_for(D)): D for D in fam}
keep = []
for line in core.read_text().split('\n'):
    line = line.strip()
    if not line or line.startswith('p') or line.startswith('c'):
        continue
    lits = frozenset(int(x) for x in line.split()[:-1])
    if lits in want:
        keep.append(want[lits])
print(f'core keeps {len(keep)} of {len(fam)} killing sets', flush=True)
keep.sort(key=lambda d: (len(d), sorted(d)))
nv2, nc2, h2 = write_cnf(keep, W / f'small_a{a}.cnf')
t = time.time()
r3 = subprocess.run([args.cadical, '--no-binary', str(W / f'small_a{a}.cnf'), str(W / f'small_a{a}.drat')],
                    capture_output=True, text=True)
ok = 's UNSATISFIABLE' in r3.stdout
print(f'small instance ({nv2} vars, {nc2} clauses): cadical {"UNSAT" if ok else "NOT UNSAT"} in {time.time()-t:.0f}s',
      flush=True)
if ok:
    cert = {'a': a, 'n_S': len(S), 'n_Q5': len(Q5), 'S': S, 'Q5': Q5,
            'killing_sets': [{'D': sorted(D), 'witness': wit[D]} for D in keep],
            'cnf_sha256': h2, 'cnf_vars': nv2, 'cnf_clauses': nc2}
    (OUT / f'certificate_a{a}.json').write_text(json.dumps(cert))
    print('certificate written', flush=True)
