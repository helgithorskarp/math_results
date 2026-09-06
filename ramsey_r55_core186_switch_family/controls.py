#!/usr/bin/env python3
"""Complete small pattern controls and definition-level proof-kernel controls."""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import generate
from check_certificate import input_rows, physical_core
from drat import require, rup, verify_proof
from verify_formula import lookup


def reject(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('corrupt control accepted')


def models(database, n):
    return [bits for bits in product((False, True), repeat=n)
            if all(any(bits[abs(x)-1] == (x > 0) for x in row) for row in database)]


def run():
    table = lookup()
    pairs = list(combinations(range(5), 2))
    for graph in range(1024):
        red = {e for bit, e in enumerate(pairs) if graph & (1 << bit)}
        actual = sorted((c, sum(s[v] << v for v in range(5)))
                        for c, s in generate.patterns(tuple(range(5)), red))
        require(actual == sorted(table[graph]), 'all anchored/truth patterns')
    possible = [frozenset((i+1)*sign for i, sign in enumerate(signs) if sign)
                for signs in product((-1, 0, 1), repeat=2)]
    candidates = []
    for signs in product((-1, 0, 1), repeat=3):
        row = frozenset((i+1)*sign for i, sign in enumerate(signs) if sign)
        candidates.extend((row, p) for p in row)
    checks = Counter()
    for mask in range(512):
        database = {row for i, row in enumerate(possible) if mask & (1 << i)}
        old_models = models(database, 3)
        for row, pivot in candidates:
            if rup(database, row):
                require(all(any(bits[abs(x)-1] == (x > 0) for x in row) for bits in old_models), 'RUP implication')
            checks['rup_semantic_checks'] += 1
            is_rat = all(rup(database, row | (other - {-pivot})) for other in database if -pivot in other)
            if is_rat:
                require(not old_models or models(database | {row}, 3), 'RAT satisfiability preservation')
                checks['accepted_rat_cases'] += 1
            checks['rat_semantic_checks'] += 1
    with TemporaryDirectory(prefix='core186-controls-') as tmp:
        path = Path(tmp)/'case.txt'
        square = {frozenset(row) for row in ((1,2),(-1,2),(1,-2),(-1,-2))}
        path.write_text('1 0\n1 0\nd 1 0\n0\n')
        require(verify_proof(square, path)['additions'] == 3, 'proof multiplicity')
        path.write_text('3 0\n1 0\n0\n')
        require(verify_proof(square, path)['rat_additions'] == 1, 'fresh RAT pivot')
        for text, base in [('0\n',{frozenset((1,2))}), ('1 0\n',square),
                           ('1 0\n0\n1 0\n',square), ('1 1 0\n0\n',square)]:
            path.write_text(text)
            reject(lambda: verify_proof(base, path))
            checks['proof_rejections'] += 1
        # Valid syntax but no physical monochromatic event.
        rows, _ = input_rows()
        mixed = next(spins for spins in range(16)
                     if len({int(bool(rows[u] & (1 << v))) ^ ((spins >> (u-1)) & 1 if u else 0)
                             ^ ((spins >> (v-1)) & 1) for u, v in pairs}) > 1)
        false_clause = ' '.join(str(-v if mixed & (1 << (v-1)) else v) for v in range(1,5))+' 0'
        for text in ['p cnf 40 1\n'+false_clause+'\n',
                     'p cnf 40 1\n1 2 3 41 0\n', 'p cnf 40 1\n1 2 3 0\n',
                     'p cnf 40 1\n1 2 3 4\n', 'p cnf 40 1\n1 1 2 3 4 0\n',
                     'p cnf 40 1\n1 -1 2 3 4 0\n', 'p cnf 40 2\n1 2 3 4 0\n']:
            path.write_text(text)
            reject(lambda: physical_core(path))
            checks['physical_rejections'] += 1
    return {'status': 'PASS', 'base_graphs': 1024, 'physical_switch_cases': 32768,
            'proof_databases': 512, 'positive_proof_regressions': 2, **dict(sorted(checks.items()))}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = run()
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
