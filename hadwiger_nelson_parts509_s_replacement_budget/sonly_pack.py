#!/usr/bin/env python3
"""Pack the S-only killing-set family into the repository certificate (interval version).

certificate.json:
  pool, S, Q5     : ambient indices (U = S ∪ Q5)
  killing_sets    : rows {D ⊆ S, class_index (interface_L.json order), colouring_U_minus_D}
                    each witnessing a proper 4-colouring of L ∪ (U \ D)
  lp_dual         : exact rational weak-duality certificate over the minimal killing sets
                    (indices into killing_sets, rational weights) -> solver-free lower bound
  solver_bound    : recorded exact minimum hitting set of the family (RC2), solver-trusted
  upper_bound     : Y* ⊆ S with L ∪ Y* ∪ Q5 not 4-colourable (DRAT report)
Usage: sonly_pack2.py family.jsonl lp_dual.json upper_report.json out.json RC2_VALUE RC2_SETS
"""
import json, sys, hashlib
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve().parent
pool = json.loads((HERE / 'pool_S.json').read_text())
U = sorted(pool['W_S']); Uset = set(U); L = list(range(374))
iface = json.loads((HERE.parent / 'hadwiger_nelson_parts509_interface_lemma' / 'interface_L.json').read_text())
witL = [row['witness_colouring_L'] for row in iface['classes']]
H = [json.loads(l) for l in Path(sys.argv[1]).read_text().splitlines() if l.strip()]
seen = {}; rows = []
for row in H:
    key = frozenset(row['D'])
    if key in seen:
        continue
    D = sorted(row['D']); assert all(374 <= v < 509 for v in D)
    X = sorted(Uset - set(D)); verts = sorted(set(L) | set(X))
    col = dict(zip(verts, row['witness']))
    ci = witL.index(''.join(col[v] for v in L))
    seen[key] = len(rows)
    rows.append({'D': D, 'class_index': ci, 'colouring_U_minus_D': ''.join(col[v] for v in X)})
dual = json.loads(Path(sys.argv[2]).read_text())
lp = {'weights': [], 'bound': dual['bound'], 'ceil': dual['ceil']}
tot = Fraction(0)
for D, y in zip(dual['sets'], dual['dual']):
    if Fraction(y) != 0:
        lp['weights'].append([seen[frozenset(D)], y]); tot += Fraction(y)
assert tot == Fraction(dual['bound'])
cert = {'pool': U, 'S': list(range(374, 509)), 'Q5': sorted(pool['Q5']), 'killing_sets': rows, 'lp_dual': lp,
        'solver_bound': {'minimum_hitting_set': int(sys.argv[5]), 'minimal_sets': int(sys.argv[6]),
                         'solver': 'RC2 (python-sat 1.8.dev24, CaDiCaL 1.9.5 backend), exact; recomputable with verify_sonly.py --rc2/--milp/--cbc'},
        'upper_bound': json.loads(Path(sys.argv[3]).read_text()),
        'family_sha256': hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()}
Path(sys.argv[4]).write_text(json.dumps(cert))
print('packed', len(rows), 'S-killing sets;', len(lp['weights']), 'weighted in the LP dual (bound', dual['bound'], '->', dual['ceil'], ');', 'solver bound', sys.argv[5])
