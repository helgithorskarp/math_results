#!/usr/bin/env python3
"""Direct literal graph check, independent of SAT auxiliaries and constraints."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def inspect(path):
    data = path.read_bytes()
    lines = data.decode().splitlines()
    n, m = map(int, lines[0].split())
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    if not (1 <= n <= 43 and len(edges) == m and len(set(edges)) == m):
        raise ValueError('invalid graph header or repeated edges')
    if not all(len(e) == 2 and 0 <= e[0] < e[1] < n for e in edges):
        raise ValueError('invalid graph edge')
    red = set(edges)
    first_mono = None
    count = 0
    for vertices in combinations(range(n), 5):
        count += 1
        if len({edge in red for edge in combinations(vertices, 2)}) == 1:
            first_mono = list(vertices)
            break
    return {'vertices': n, 'red_edges': m, 'five_sets_inspected': count,
            'monochromatic_five_set': first_mono, 'ramsey': first_mono is None,
            'sha256': hashlib.sha256(data).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('graph', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.graph), sort_keys=True))
