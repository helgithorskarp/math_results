"""Damaged certificates and exact negative controls; no assert statements."""
import argparse
from copy import deepcopy
from fractions import Fraction as Q
import json
from pathlib import Path
import tempfile
import audit


def run():
    rejected = []

    def reject(label, fn):
        try:
            fn()
        except ValueError as exc:
            rejected.append({'label': label, 'reason': str(exc)})
        else:
            raise ValueError('invalid evidence accepted: '+label)

    audit.psd([[Q(1), Q(1)], [Q(1), Q(1)]], 'calibration singular PSD', 1)
    reject('zero-diagonal indefinite', lambda: audit.psd([[0, 1], [1, 0]], 'damage'))
    reject('positive-diagonal indefinite', lambda: audit.psd([[1, 2], [2, 1]], 'damage'))
    reject('asymmetric form', lambda: audit.psd([[1, 1], [0, 1]], 'damage'))
    reject('false kernel multiplicity', lambda: audit.psd([[1, 1], [1, 1]], 'damage', 2))
    tables = json.loads((audit.ROOT/'TABLES.json').read_text())['cases']
    for n in range(8, 12):
        damaged = deepcopy(tables)
        damaged[str(n)]['weights'][0][0] = str(Q(damaged[str(n)]['weights'][0][0])+1)
        reject('rank-six table '+str(n)+' diagonal damage', lambda n=n, d=damaged: audit.parameters(n, d))
    damaged = deepcopy(tables)
    damaged['8']['weights'][0][1] = str(Q(damaged['8']['weights'][0][1])+1)
    reject('table off-diagonal damage', lambda: audit.parameters(8, damaged))
    damaged = deepcopy(tables)
    damaged['8']['weights'][5][5] = '1'
    reject('weight on impossible disjoint layers', lambda: audit.parameters(8, damaged))
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/'TABLES.json'
        path.write_bytes((audit.ROOT/'TABLES.json').read_bytes()+b' ')
        reject('input hash damage', lambda: audit.run(path, literal=False))
    # Recompute the actual failing side of each active endpoint. These are
    # matrix-family counterexamples, never universal nonexistence statements.
    outside = []
    for n in range(8, 12):
        j, aa, g, K, U, T = audit.blocks(n, tables)[0]
        B, R = audit.metric(g, U), audit.metric(g, T)
        tau, witness = audit.endpoint(B, R, 'control '+str(n))
        w = list(map(Q, witness['inverse_witness']))
        negative = audit.quadratic(audit.add(B, R, -2*tau), w)
        audit.need(negative < 0, 'negative cap witness')
        one = [Q(1)]*len(K)
        negative_lower = audit.quadratic(audit.metric(g, audit.add(K, T, -1)), one)
        audit.need(negative_lower < 0, 'negative repair parameter fails')
        outside.append({'n': n, 't': str(2*tau), 'negative_cap_quadratic': str(negative),
                        't_minus_one_lower_quadratic': str(negative_lower)})
    return {'rejected': rejected, 'rejection_count': len(rejected), 'outside_fixed_family': outside}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = run()
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'rejections': result['rejection_count'], 'outside_witnesses': len(result['outside_fixed_family'])}))
