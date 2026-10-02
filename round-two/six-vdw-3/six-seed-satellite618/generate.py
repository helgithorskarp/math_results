#!/usr/bin/env python3
"""Field-ladder model for the unique sparse six-seed satellite word.

The common pair mechanism is credited to the author's single-satellite618
source b18c33b5. The new fixed word contains two opposite points.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def parameters(q, case):
    if q == 103:
        need(case == 1, 'Only the sparse production case is supported')
        holes = (5, 53, 101)
        original = tuple(range(6)) + (7, 52, 53, 55, 56, 101)
        fixed = {(4-x)%q: int(x in (53, 55)) for x in original}
    else:
        need(q in (7, 11, 13) and case in (1, 2, 3), 'Bad small control')
        holes = (0, 1, case+1)
        core = tuple(x for x in range(q) if x not in holes)[:4]
        fixed = {x: int(j >= 2) for j, x in enumerate(core)}
    regular = tuple(x for x in range(q) if x not in holes)
    need(len(fixed) == (12 if q == 103 else 4), 'Wrong fixed-word domain')
    need(set(fixed) <= set(regular) and fixed[regular[0]] == 0, 'Bad root or hole')
    return holes, regular, fixed


def generate(q, case, path):
    holes, regular, fixed = parameters(q, case)
    root = regular[0]
    labels = {pair: i+1 for i, pair in enumerate(itertools.combinations(regular, 2))}
    def edge(x, y):
        return labels[tuple(sorted((x, y)))]
    rows = set()
    for x, y in itertools.combinations(regular[1:], 2):
        a, b, c = edge(root, x), edge(root, y), edge(x, y)
        rows.update(tuple(sorted(row)) for row in
                    ((-a,b,c), (a,-b,c), (a,b,-c), (-a,-b,-c)))
    cycles = len(rows)
    ladders = set()
    for step in range(1, (q+1)//2):
        for start in range(q):
            ap = tuple((start+j*step)%q for j in range(7))
            if set(holes).intersection(ap):
                continue
            row = tuple(sorted(edge(ap[j], ap[j+3]) for j in range(4)))
            ladders.add(row)
            rows.add(row)
            rows.add(tuple(sorted(-x for x in row)))
    units = {(edge(root,x) if value else -edge(root,x),)
             for x, value in fixed.items() if x != root}
    rows.update(units)
    raw = ('p cnf '+str(len(labels))+' '+str(len(rows))+'\n'+
           ''.join(' '.join(map(str,row))+' 0\n' for row in sorted(rows))).encode()
    path.write_bytes(raw)
    return {'q': q, 'case': case, 'holes': list(holes), 'root': root,
            'fixed_core_bits': [[x,fixed[x]] for x in sorted(fixed)],
            'regular_columns': list(regular), 'variables': len(labels),
            'root_cycle_clauses': cycles, 'seven_ladders': len(ladders),
            'fixed_core_units': len(units),
            'positive_core_units': sum(x[0] > 0 for x in units),
            'clauses': len(rows), 'other_regular_bits_free': len(regular)-len(fixed),
            'extra_growth_cuts': 0, 'no_five_assumption': False,
            'no_six_assumption': False, 'counter_variables': 0, 'weight_cap': None,
            'reflection_invariance_imposed': False,
            'cnf_sha256': hashlib.sha256(raw).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--q', type=int, default=103)
    parser.add_argument('--case', type=int, default=1)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(generate(args.q, args.case, args.output)))
