#!/usr/bin/env python3
"""Generate the exact graph-cut CNF for a separable period-6q template."""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


def validate_q(q):
    if not isinstance(q, int) or q < 7 or q > 311:
        raise ValueError('q must be a prime between 7 and 311')
    if any(q % d == 0 for d in range(2, math.isqrt(q) + 1)):
        raise ValueError('q must be prime')


def model(q):
    validate_q(q)
    edges = list(itertools.combinations(range(q), 2))
    labels = {edge: i + 1 for i, edge in enumerate(edges)}

    def edge(x, y):
        if x == y:
            raise ValueError('a cut edge cannot be a loop')
        return labels[tuple(sorted((x, y)))]

    def clause(literals):
        values = set(literals)
        if any(-lit in values for lit in values):
            raise ValueError('unexpected tautology')
        return tuple(sorted(values, key=abs))

    clauses = set()
    for x in range(1, q):
        for y in range(x + 1, q):
            variables = (edge(0, x), edge(0, y), edge(x, y))
            for bits in itertools.product(range(2), repeat=3):
                if sum(bits) % 2:
                    clauses.add(clause(-v if b else v
                                       for v, b in zip(variables, bits)))
    gates = len(clauses)
    supports = set()
    for r in range(1, (q + 1) // 2):
        for a in range(q):
            points = [(a + j * r) % q for j in range(7)]
            variables = tuple(sorted(edge(points[j], points[j + 3])
                                     for j in range(4)))
            supports.add(variables)
            clauses.add(clause(variables))
            clauses.add(clause(-v for v in variables))
    ordered = sorted(clauses)
    text = 'p cnf {} {}\n'.format(len(edges), len(ordered))
    text += ''.join(' '.join(map(str, row)) + ' 0\n' for row in ordered)
    return text, {
        'q': q,
        'period': 6 * q,
        'variables': len(edges),
        'anchor_variables': q - 1,
        'xor_equations': (q - 1) * (q - 2) // 2,
        'xor_cnf_clauses': gates,
        'distinct_ladders': len(supports),
        'ladder_cnf_clauses': len(ordered) - gates,
        'clauses': len(ordered),
        'sha256': hashlib.sha256(text.encode('ascii')).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--q', type=int, default=103)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    text, metadata = model(args.q)
    if args.output:
        args.output.write_text(text, encoding='ascii')
    print(json.dumps(metadata, sort_keys=True))


if __name__ == '__main__':
    main()
