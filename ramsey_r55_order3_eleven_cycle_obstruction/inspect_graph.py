#!/usr/bin/env python3
"""Definition-level edge-list verifier, also used for every SAT candidate."""
from itertools import combinations
from pathlib import Path
import argparse
import json
import math


def inspect(path):
    rows = [list(map(int, line.split())) for line in path.read_text().splitlines()]
    if not rows or len(rows[0]) != 2:
        raise ValueError('expected n m header')
    n, m = rows[0]
    if n < 5 or m < 0 or len(rows)-1 != m:
        raise ValueError('invalid counts')
    edges = set()
    for row in rows[1:]:
        if len(row) != 2 or not 0 <= row[0] < row[1] < n or tuple(row) in edges:
            raise ValueError('invalid or repeated edge')
        edges.add(tuple(row))
    for five in combinations(range(n), 5):
        red = sum(e in edges for e in combinations(five, 2))
        if red in (0, 10):
            return {'vertices': n, 'edges': m, 'ramsey': False,
                    'obstruction': list(five), 'red': red == 10}
    return {'vertices': n, 'edges': m, 'ramsey': True, 'five_sets_checked': math.comb(n, 5)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('edges', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.edges), sort_keys=True))
