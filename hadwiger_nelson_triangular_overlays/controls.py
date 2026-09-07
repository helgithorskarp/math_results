#!/usr/bin/env python3
"""Adversarial certificate controls and an independent seven-vertex benchmark."""
import argparse
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import verify as check


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    table = json.loads((args.work/'catalog.json').read_text())
    points = check.coordinates()
    residues = [(-x) % 3 for x, y in points]
    edges = table['seed_edges']
    rejected = []

    def reject(name, callback):
        try:
            callback()
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
        else:
            raise RuntimeError('accepted corrupt case: '+name)

    # All these fail in the initial inventory check, before the large audit.
    for name, mutation in [
        ('wrong family radius', lambda t: t.update(norm_limit=66)),
        ('missing vertex', lambda t: t['points'].pop()),
        ('missing seed edge', lambda t: t['seed_edges'].pop()),
        ('missing origin contact', lambda t: t['universal_cross_edges'].pop()),
        ('missing contact line', lambda t: t['contact_lines'].pop()),
        ('missing irrational line', lambda t: t['irrational'].pop()),
        ('duplicate irrational line', lambda t: t['irrational'].append(t['irrational'][-1])),
        ('missing rational angle', lambda t: t['rational'].pop()),
        ('duplicate rational angle', lambda t: t['rational'].append(t['rational'][-1])),
    ]:
        damaged = deepcopy(table)
        mutation(damaged)
        reject(name, lambda: check.audit(damaged))

    row = deepcopy(table['irrational'][0])
    row['radicand'] += 1
    reject('wrong radicand', lambda: check.audit_irrational(row, points, residues, edges))
    row = deepcopy(table['irrational'][0])
    row['cross_edges'].pop()
    reject('missing irrational unit edge', lambda: check.audit_irrational(row, points, residues, edges))
    row = deepcopy(next(r for r in table['irrational'] if r['zero_edge']))
    row['zero_edge'] = None
    reject('erased four-chromatic witness', lambda: check.audit_irrational(row, points, residues, edges))
    row = deepcopy(next(r for r in table['irrational'] if r['zero_edge']))
    row['chromatic_number'] = 3
    reject('false three-colour label', lambda: check.audit_irrational(row, points, residues, edges))
    row = deepcopy(next(r for r in table['irrational']
                        if any(residues[i] and residues[j] for i, j in r['cross_edges'])))
    row['epsilon'] = 3-row['epsilon']
    reject('wrong residue palette', lambda: check.audit_irrational(row, points, residues, edges))
    row = deepcopy(table['rational'][0])
    row['rotation'][0][0] += 1
    reject('nonunit rational rotation', lambda: check.audit_rational(row, points, residues, edges))
    row = deepcopy(table['rational'][0])
    row['rotation'][0] = [2*x for x in row['rotation'][0]]
    reject('noncanonical rational encoding', lambda: check.audit_rational(row, points, residues, edges))
    row = deepcopy(next(r for r in table['rational'] if r['coincidences']))
    row['coincidences'].pop()
    reject('missing coincidence', lambda: check.audit_rational(row, points, residues, edges))
    row = deepcopy(next(r for r in table['rational'] if r['cross_edges']))
    row['cross_edges'].pop()
    reject('missing rational unit edge', lambda: check.audit_rational(row, points, residues, edges))

    # Exact Moser benchmark in the two-lattice source. D=33, alpha has
    # real part 5/6 and imaginary part -sqrt(11)/6. Here points are stored
    # as (X0,X1,Y0,Y1), physical (X0+X1 sqrt(33),sqrt(3)(Y0+Y1 sqrt(33)))/36.
    diamond = [(0, 0), (2, 0), (1, 1), (3, 1)]
    small = [(18*x, 0, 18*y, 0) for x, y in diamond]
    small += [(15*x, 3*y, 15*y, -x) for x, y in diamond[1:]]
    small_edges = []
    for i, a in enumerate(small):
        for j, b in enumerate(small[:i]):
            x0, x1, y0, y1 = [c-d for c, d in zip(a, b)]
            rat = x0*x0+33*x1*x1+3*y0*y0+99*y1*y1
            rad = 2*x0*x1+6*y0*y1
            check.require(rat != 0 or rad != 0, 'benchmark collision')
            if rat == 36**2 and rad == 0:
                small_edges.append((i, j))
    expected = {(1, 0), (2, 0), (2, 1), (3, 1), (3, 2),
                (4, 0), (5, 0), (5, 4), (6, 4), (6, 5), (6, 3)}
    check.require(set(small_edges) == expected, 'Moser geometry mismatch')
    colour_counts = {}
    for k in (3, 4):
        colour_counts[k] = sum(all(c[i] != c[j] for i, j in small_edges)
                               for c in product(range(k), repeat=7))
    check.require(colour_counts[3] == 0 and colour_counts[4] > 0, 'Moser colour mismatch')
    result = {'rejected_corruptions': len(rejected), 'controls': rejected,
              'benchmark_vertices': 7, 'benchmark_edges': len(small_edges),
              'benchmark_all_assignments': 3**7+4**7,
              'benchmark_proper_colourings': colour_counts,
              'verified': True}
    (args.work/'controls.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
