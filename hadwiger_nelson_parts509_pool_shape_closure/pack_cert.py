#!/usr/bin/env python3
"""Pack the per-a unsat cores into one compact, self-contained certificate bundle.

Output (in the publication directory):
  killing_sets.json : the union of the cores.  Each entry is
        {"D": [...], "p": <interface class index>, "c": "<303 chars>"}
      where c[i] is the colour of the i-th point of U (sorted) and '.' for points of D.
      Together with the class-p witness colouring of L from the committed interface lemma
      this is an explicit proper 4-colouring of L u (U \\ D), certifying that D is a
      killing set.
  closures.json     : for each closed a, the indices of the killing sets whose clauses,
      with |R| = a+1 and |A| = a, are unsatisfiable, plus the SHA-256 of the rebuilt CNF.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pool5 import Pool
import cardenc

ap = argparse.ArgumentParser()
ap.add_argument('--certs', default=str(HERE / 'certs'))
ap.add_argument('--sources', nargs='*', default=[],
                help='jsonl killing-set files (D, pattern, witness) produced by the search')
ap.add_argument('--out', required=True)
args = ap.parse_args()
P = Pool()
S, Q5, U = P.S, P.Q5, P.U
Uidx = {v: i for i, v in enumerate(U)}
rid = {v: i + 1 for i, v in enumerate(S)}
qid = {w: len(S) + i + 1 for i, w in enumerate(Q5)}
Sset, Qset = set(S), set(Q5)

# patterns for every killing set: recover from the source jsonl files
pat = {}
for path in list(args.sources) + [str(p) for p in HERE.glob('ihs_a*/new_killing_sets.jsonl')] \
            + [str(p) for p in HERE.glob('acc*.jsonl')]:
    p = Path(path)
    if not p.exists():
        continue
    for line in open(p):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        pat.setdefault(frozenset(r['D']), (r.get('pattern'), r.get('witness')))

witL = [r['witness_colouring_L'] for r in
        json.loads((Path.home() / 'math_results' / 'hadwiger_nelson_parts509_interface_lemma'
                    / 'interface_L.json').read_text())['classes']]
bundle = {}
order = []
closures = {}
for cf in sorted(Path(args.certs).glob('certificate_a*.json'), key=lambda p: int(p.stem.split('a')[-1])):
    cert = json.loads(cf.read_text())
    a = cert['a']
    idxs = []
    for row in cert['killing_sets']:
        D = frozenset(row['D'])
        if D not in bundle:
            _, w = pat.get(D, (None, None))
            assert w is not None, f'no witness recorded for {sorted(D)}'
            # the class index is read off the witness itself: search histories use
            # different orderings of the 20 interface classes
            p = witL.index(w[:len(P.L)])
            verts = sorted(set(P.L) | (set(U) - D))
            col = {v: int(w[i]) for i, v in enumerate(verts)}
            c = ''.join('.' if v in D else str(col[v]) for v in U)
            bundle[D] = {'D': sorted(D), 'p': p, 'c': c}
            order.append(D)
        idxs.append(order.index(D))
    # rebuild the CNF exactly as the verifier will
    nv = len(S) + len(Q5)
    clauses = []
    for i in idxs:
        Dl = sorted(order[i])
        clauses.append([-rid[v] for v in Dl if v in Sset] + [qid[w] for w in Dl if w in Qset])
    cl, nv = cardenc.equals_tot([rid[v] for v in S], a + 1, nv); clauses += cl
    cl, nv = cardenc.equals_tot([qid[w] for w in Q5], a, nv); clauses += cl
    txt = f'p cnf {nv} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)
    closures[str(a)] = {'sets': idxs, 'cnf_vars': nv, 'cnf_clauses': len(clauses),
                        'cnf_sha256': hashlib.sha256(txt.encode()).hexdigest(),
                        'drat_sha256': None, 'drat_bytes': None, 'drat_verified': None}
    print(f'a={a}: {len(idxs)} killing sets, cnf {nv} vars {len(clauses)} clauses', flush=True)

out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
(out / 'killing_sets.json').write_text(json.dumps({'U': U, 'sets': [bundle[D] for D in order]}))
(out / 'closures.json').write_text(json.dumps({'closures': closures, 'S': S, 'Q5': Q5}, indent=1))
print(f'bundle: {len(order)} distinct killing sets -> {out}')
