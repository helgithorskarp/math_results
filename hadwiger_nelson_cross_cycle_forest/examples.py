"""Exact cycle and field-boundary examples for the cross-forest reduction."""
from fractions import Fraction as Q
from hashlib import sha256
from collections import Counter
import json
from exact import A, require


def cycles(n, edges):
    neighbours = [[] for _ in range(n)]
    for a, b in edges:
        neighbours[a].append(b)
        neighbours[b].append(a)
    found = set()

    def walk(path):
        for v in neighbours[path[-1]]:
            if v == path[0] and len(path) >= 4:
                found.add(tuple(sorted(tuple(sorted((path[i], path[(i+1) % len(path)])))
                                       for i in range(len(path)))))
            elif v not in path:
                walk(path+[v])

    for v in range(n):
        walk([v])
    return dict(sorted(Counter(map(len, found)).items()))


def colouring(n, edges):
    neighbours = [set() for _ in range(n)]
    for i, j in edges:
        neighbours[i].add(j)
        neighbours[j].add(i)
    colours = [-1]*n

    def extend(v):
        if v == n:
            return True
        forbidden = {colours[w] for w in neighbours[v]}
        for c in range(4):
            if c not in forbidden:
                colours[v] = c
                if extend(v+1):
                    return True
        colours[v] = -1
        return False

    require(extend(0), 'no four-colouring for a small calibration example')
    require(all(colours[i] != colours[j] for i, j in edges), 'improper colouring')
    return colours


def case(name, P, Qs, u, expected_cycle, extended=False):
    P, Qs = list(map(A, P)), list(map(A, Qs))
    require(all(x.in_field(extended) for x in P+Qs), 'source outside stated field')
    require(u.norm() == 1, 'rotation norm is not one')
    Z = [u*q for q in Qs]
    points = P+Z
    require(len(points) == len(set(points)), 'unexpected physical coincidence')
    n = len(P)
    norms, edges, cross = [], [], []
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            d = (points[i]-points[j]).norm().rational()
            norms.append(f'{i},{j}:{d.numerator}/{d.denominator}\n')
            if d == 1:
                edges.append((i, j))
                if i < n <= j:
                    cross.append((i, j))
    cycle_counts = cycles(len(points), cross)
    require(cycle_counts == ({expected_cycle: 1} if expected_cycle else {}), 'wrong cross cycle set')
    preserves = u.in_field(extended)
    if not extended and not preserves:
        require(all(k == 4 for k in cycle_counts), 'counterexample to the theorem')
    colours = colouring(len(points), edges)
    return {'case': name, 'source_field': 'E(sqrt(2))' if extended else 'E',
            'source_sizes': [len(P), len(Qs)], 'vertices': len(points),
            'pairs_checked': len(norms), 'strict_edges': len(edges),
            'cross_edges': [[i, j-n] for i, j in cross], 'cross_cycle_lengths': cycle_counts,
            'field_preserving': preserves, 'source_points_all_in_E': all(x.in_field() for x in P+Qs),
            'proper_four_colouring': True, 'colours': colours,
            'squared_distance_sha256': sha256(''.join(norms).encode()).hexdigest(),
            'edge_sha256': sha256(''.join(f'{i},{j}\n' for i, j in edges).encode()).hexdigest()}


def main():
    alpha = A({5: 1})
    root2, root13, imaginary = A({2: 1}), A({32: 1}), A({1: 1})
    omega, eta = (-1+alpha)*Q(1, 2), (1+alpha)*Q(1, 2)
    r = [Q(3, 7), Q(5, 7), Q(-8, 7)]
    r12 = [Q(x, 7) for x in (-5, -8, -3, 5, 8, 3)]
    s12 = [Q(x, 7) for x in (-13, -11, 2, 13, 11, -2)]
    examples = [
        case('non_base_cross_four_cycle', [alpha*Q(1, 4), -alpha*Q(1, 4)],
             [(1+2*alpha)*Q(1, 4), -(1+2*alpha)*Q(1, 4)],
             (1-2*alpha)*root13*Q(1, 13), 4),
        case('field_preserving_six_cycle', r, r, omega, 6),
        case('field_preserving_eight_cycle', [0, 2, 2+2*eta, 2*eta],
             [1, 2+eta, 1+2*eta, eta], A(1), 8),
        case('field_preserving_twelve_cycle', [alpha*x for x in r12], s12, omega, 12),
        case('larger_field_non_base_eight_cycle', [Q(7, 5), Q(1, 5), Q(-7, 5), Q(-1, 5)],
             [root2*Q(x, 5) for x in (4, -3, -4, 3)], (1+imaginary)*root2*Q(1, 2), 8, True),
        case('non_base_quadratic_path', [0, Q(4, 3), Q(-8, 27)],
             [1, Q(7, 9), Q(-95, 81)], (2+A({9: 1}))*Q(1, 3), 0)
    ]
    require(not examples[4]['field_preserving'] and not examples[4]['source_points_all_in_E'],
            'larger-field boundary was not exercised')
    print(json.dumps({'examples': examples,
                      'total_pairs_checked': sum(x['pairs_checked'] for x in examples),
                      'uniform_theorem_requires_PROOF_md': True}, indent=2))


if __name__ == '__main__':
    main()
