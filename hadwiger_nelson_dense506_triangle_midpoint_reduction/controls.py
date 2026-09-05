#!/usr/bin/env python3
"""Rational circle fixtures, repeated-pair boundary and false path certificates."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
import json
import engine as E


def rotate(p):
    x, y = p
    return ((x - 3 * y) / 2, (x + y) / 2)


def norm(p):
    return p[0] ** 2 + 3 * p[1] ** 2


def lift(p):
    return (p[0], 0, 0, 0), (p[1], 0, 0, 0)


def main():
    fixtures = {}
    for t in (Q(1, 2), Q(1), Q(2)):
        a = (1 - 3 * t * t) / (1 + 3 * t * t)
        b = 2 * t / (1 + 3 * t * t)
        for center, half_chord in [((a, Q(0)), (Q(0), b)),
                                   ((Q(0), b), (a, Q(0)))]:
            for _ in range(6):
                E.require(norm(center) + norm(half_chord) == 1 and
                          center[0] * half_chord[0] + 3 * center[1] * half_chord[1] == 0,
                          'direct rational unit-circle fixture')
                key = min(half_chord, tuple(-x for x in half_chord))
                fixtures[key] = center
                center, half_chord = rotate(center), rotate(half_chord)
    cases = hits = 0
    for (h, x), (k, y) in combinations_with_replacement(sorted(fixtures.items()), 2):
        cases += 1
        u, v = lift(tuple(2 * a for a in h)), lift(tuple(2 * a for a in k))
        expected = any(norm((sx * x[0] - sy * y[0], sx * x[1] - sy * y[1])) == 1
                       for sx, sy in product((-1, 1), repeat=2))
        actual = E.compatible(E.G.norm(*u), E.G.norm(*v), E.dot(u, v), 4)
        E.require(actual == expected, 'circle-root signs disagree with polynomial')
        hits += expected
    # Opposite unit-separated roots of one host pair have chord norm three,
    # making q=(4-S)/(3S)=1/9 a square. They are not non-field roots.
    E.require(Q(4 - 3, 3 * 3) == Q(1, 3) ** 2, 'repeated-pair boundary')
    labels = [(2 * i, 2 * i + 1) for i in range(5)]
    path_edges = [labels[i] + labels[i + 1] for i in range(4)]
    paths, incident = E.path_components(path_edges)
    E.require(len(paths) == 1 and len(paths[0]) == incident == 5, 'P5 fixture')
    rejected = 0
    for pairs in [[(0, 1), (1, 2), (0, 2)], [(0, 1), (0, 2), (0, 3)]]:
        try:
            E.path_components([labels[a] + labels[b] for a, b in pairs])
        except AssertionError:
            rejected += 1
    E.require(rejected == 2, 'false path decomposition accepted')
    print(json.dumps({'rational_circle_fixtures': len(fixtures),
                      'signed_root_pair_cases': cases, 'compatible_cases': hits,
                      'repeated_pair_square_boundary': True,
                      'valid_path_fixture': True, 'invalid_graphs_rejected': rejected}, indent=2))


if __name__ == '__main__':
    main()
