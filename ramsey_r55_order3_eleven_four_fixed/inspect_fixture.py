#!/usr/bin/env python3
"""Small standalone all-five-set checker for a plain edge-list fixture."""
import argparse
from itertools import combinations
import json
from pathlib import Path


def inspect(path):
    lines = path.read_text().splitlines()
    n, m = map(int, lines[0].split())
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    if n != 22 or len(edges) != m or len(set(edges)) != m:
        raise ValueError('header or duplicate edge')
    matrix = [[False]*n for _ in range(n)]
    for a, b in edges:
        if not 0 <= a < b < n:
            raise ValueError('edge endpoints')
        matrix[a][b] = matrix[b][a] = True
    counts = [0, 0]
    checked = 0
    for vs in combinations(range(n), 5):
        total = sum(matrix[a][b] for a, b in combinations(vs, 2))
        counts[0] += total == 10
        counts[1] += total == 0
        checked += 1
    if any(counts):
        raise ValueError(('monochromatic K5', counts))
    return dict(vertices=n, red_edges=m, five_sets=checked,
                red_k5=counts[0], blue_k5=counts[1], verified=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('fixture', type=Path)
    a = p.parse_args()
    print(json.dumps(inspect(a.fixture), sort_keys=True))
