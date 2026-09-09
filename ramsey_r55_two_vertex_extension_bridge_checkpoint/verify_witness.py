#!/usr/bin/env python3
"""Literal dense check of the failed catalog obstruction, without the scanner."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def decode(graph6):
    if not isinstance(graph6, str) or len(graph6) != 47 or graph6[0] != 'W':
        raise ValueError('Expected a graph6 record of order 24')
    if any(not 63 <= ord(c) <= 126 for c in graph6[1:]):
        raise ValueError('Invalid graph6 byte')
    stream = ''.join(format(ord(c) - 63, '06b') for c in graph6[1:])
    matrix = [[False] * 24 for _ in range(24)]
    position = 0
    for column in range(1, 24):
        for row in range(column):
            matrix[row][column] = matrix[column][row] = stream[position] == '1'
            position += 1
    if position != len(stream):
        raise ValueError('Unexpected payload size')
    return matrix


def check(matrix, vertices, order, red):
    checked = 0
    for selected in itertools.combinations(vertices, order):
        checked += 1
        if all(matrix[a][b] == red for a, b in itertools.combinations(selected, 2)):
            raise ValueError(f'Forbidden monochromatic {order}-set: {selected}, red={red}')
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('witness', type=Path)
    parser.add_argument('--catalog', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    witness = json.loads(args.witness.read_text())
    vertices = witness['subset_vertices']
    if (len(vertices) != 17 or vertices != sorted(set(vertices)) or
            any(type(v) is not int or not 0 <= v < 24 for v in vertices)):
        raise ValueError('Invalid seventeen-vertex subset')
    matrix = decode(witness['graph6'])
    checks = {
        'host_red_four_sets': check(matrix, range(24), 4, True),
        'host_blue_five_sets': check(matrix, range(24), 5, False),
        'subset_red_four_sets': check(matrix, vertices, 4, True),
        'subset_blue_four_sets': check(matrix, vertices, 4, False),
    }
    subset_degrees = [sum(matrix[v][w] for w in vertices) for v in vertices]
    if subset_degrees != [8] * 17:
        raise ValueError('Unexpected subset degrees')
    membership = 'not requested; graph property is checked literally'
    if args.catalog:
        data = args.catalog.read_bytes()
        if hashlib.sha256(data).hexdigest() != witness['catalog_sha256']:
            raise ValueError('Wrong catalog digest')
        lines = data.decode('ascii').splitlines()
        if lines[witness['record_index']] != witness['graph6']:
            raise ValueError('Catalog record mismatch')
        membership = 'PASS'
    result = {'status': 'VERIFIED_BRIDGE_COUNTEREXAMPLE', 'host_order': 24,
              'subset_order': 17, 'checks': checks, 'subset_degrees': subset_degrees,
              'catalog_membership': membership, 'global_43_family_decided': False,
              'good43_constructed': False,
              'witness_sha256': hashlib.sha256(args.witness.read_bytes()).hexdigest()}
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
