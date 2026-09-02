#!/usr/bin/env python3
"""Pack a compact solver-free lower-bound certificate for the general pool question
(min |X|, X ⊆ U = S ∪ Q5, with L ∪ X not 4-colourable): the killing sets carrying a
nonzero rational LP dual, each with its witness colouring, plus the dual values.
Usage: general_dual_pack.py lp_dual.json hyperedges.jsonl out.json"""
import json, sys
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve().parent
PAIR = HERE.parent / 'hadwiger_nelson_parts509_pair_closure'
dual = json.loads(Path(sys.argv[1]).read_text())
H = [json.loads(l) for l in Path(sys.argv[2]).read_text().splitlines() if l.strip()]
wit = {}
for r in H:
    wit.setdefault(frozenset(r['D']), r)
U = dual['pool']; Uset = set(U); L = list(range(374))
iface = json.loads((Path(__file__).resolve().parent.parent / 'hadwiger_nelson_parts509_interface_lemma' / 'interface_L.json').read_text())
witL = [row['witness_colouring_L'] for row in iface['classes']]
rows = []
for D, y in zip(dual['sets'], dual['dual']):
    if Fraction(y) == 0:
        continue
    r = wit[frozenset(D)]
    X = sorted(Uset - set(D)); verts = sorted(set(L) | set(X))
    col = dict(zip(verts, r['witness']))
    ci = witL.index(''.join(col[v] for v in L))
    rows.append({'D': sorted(D), 'y': y, 'class_index': ci, 'colouring_U_minus_D': ''.join(col[v] for v in X)})
cert = {'pool': U, 'bound': dual['bound'], 'ceil': dual['ceil'], 'killing_sets': rows}
Path(sys.argv[3]).write_text(json.dumps(cert))
print('packed', len(rows), 'weighted killing sets; bound', dual['bound'], '->', dual['ceil'])
