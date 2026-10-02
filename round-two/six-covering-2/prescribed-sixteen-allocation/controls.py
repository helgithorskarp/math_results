"""Exact controls for a prescribed16 two-layer allocation refinement.

The written counting argument is the proof. These controls independently scan
a positive original-congruence fixture and complete small two-layer models.
Author: six-covering-2, researcher. Standard library, Python >=3.10.
"""
import argparse
from hashlib import sha256
from itertools import product
import json
from math import gcd
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def divisors(n):
    return tuple(d for d in range(1, n + 1) if n % d == 0)


def subsets(items):
    items = tuple(items)
    return tuple(frozenset(items[i] for i in range(len(items)) if mask >> i & 1)
                 for mask in range(1 << len(items)))


def graph(M, V, D1, D2):
    require(type(M) is int and M > 0, 'Invalid cofactor')
    require(V and all(S and all(type(z) is int and 0 <= z < M for z in S)
                      for S in V), 'Invalid initial nonempty fibres')
    require(len(set(D1)) == len(D1) and len(set(D2)) == len(D2),
            'Duplicate original resource')
    require(all(type(d) is int and d > 0 and M % d == 0 for d in (*D1, *D2)),
            'Invalid cofactor resource')
    return frozenset((i, d) for i, S in enumerate(V) for d in set(D1) | set(D2)
                     if len({z % d for z in S}) == 1)


def vertex_cut(M, V, D1, D2, C, B):
    edges = graph(M, V, D1, D2)
    require(set(C) <= set(range(len(V))), 'Invalid fibre vertices')
    require(set(B) <= set(D1) | set(D2), 'Invalid resource vertices')
    require(all(i in C or d in B for i, d in edges), 'Not a vertex cover')
    cost = 4 * len(C) + 2 * len(set(B) & set(D1)) + len(set(B) & set(D2))
    required = 4 * len(V) - 2 * len(D1) - len(D2)
    return {'cost': cost, 'required': required, 'strict_gap': required - cost}


def literal_two_layer(M, V, D1, D2):
    """Enumerate complete original phase unions, with no eraser-graph rule.

    Points are literal triples (initial fibre, final binary child, cofactor).
    A first resource acts on both children of one initial fibre; a second
    resource acts on one final child. Omission is explicitly included.
    """
    points = tuple((i, j, z) for i, S in enumerate(V) for j in range(2)
                   for z in sorted(S))
    full = (1 << len(points)) - 1
    reachable = {0}
    for level, ds in ((1, D1), (2, D2)):
        for d in ds:
            options = {0}
            for i in range(len(V)):
                for j in ((None,) if level == 1 else (0, 1)):
                    for a in range(d):
                        mask = sum(1 << p for p, (ii, jj, z) in enumerate(points)
                                   if ii == i and (j is None or jj == j) and z % d == a)
                        options.add(mask)
            reachable = {u | w for u in reachable for w in options}
    return full in reachable


def audit_small():
    records = []
    totals = {'models': 0, 'feasible': 0, 'strictly_cut': 0,
              'vertex_covers': 0, 'feasible_equality_models': 0}
    digest = sha256()
    for M, T in ((1, 1), (1, 2), (3, 1), (3, 2), (5, 1)):
        pool = subsets(divisors(M))
        nonempty = tuple(S for S in subsets(range(M)) if S)
        local = {'M': M, 'initial_fibres': T, 'models': 0, 'feasible': 0,
                 'strictly_cut': 0}
        for V in product(nonempty, repeat=T):
            for D1 in pool:
                for D2 in pool:
                    first, second = tuple(sorted(D1)), tuple(sorted(D2))
                    edges = graph(M, V, first, second)
                    feasible = literal_two_layer(M, V, first, second)
                    best = None
                    equality = False
                    for C in subsets(range(T)):
                        for B in subsets(D1 | D2):
                            if not all(i in C or d in B for i, d in edges):
                                continue
                            cut = vertex_cut(M, V, first, second, C, B)
                            totals['vertex_covers'] += 1
                            best = cut['cost'] if best is None else min(best, cut['cost'])
                            if feasible:
                                require(cut['strict_gap'] <= 0,
                                        'A necessary cut rejected a genuine completion')
                                equality |= cut['strict_gap'] == 0
                    rhs = 4 * T - 2 * len(D1) - len(D2)
                    strict = best < rhs
                    require(not (strict and feasible), 'Invalid exact exclusion')
                    for record in (totals, local):
                        record['models'] += 1
                        record['feasible'] += int(feasible)
                        record['strictly_cut'] += int(strict)
                    totals['feasible_equality_models'] += int(feasible and equality)
                    digest.update(json.dumps([M, [sorted(S) for S in V], first, second,
                                              feasible, best, rhs], separators=(',', ':')).encode())
        records.append(local)
    require(totals['feasible_equality_models'] > 0, 'Missing equality positive control')
    return {'domains': records, **totals, 'ordered_models_sha256': digest.hexdigest()}


def original_fixture():
    M, N = 315, 10080
    parents = (1, 3, 4, 5, 6, 7)
    points = tuple(x for x in range(N) if x % 8 in parents and x % M in (2, 17))
    require(len(points) == 48, 'Wrong literal fixture')
    fixed = ((8, 0), (9, 0), (10, 1), (14, 0), (12, 4))
    require(all(all(x % n != a for n, a in fixed) for x in points),
            'Fixture demand already covered by a fixed core anchor')
    # (cofactor label, parent b, high binary digit, cofactor phase).
    first = [(1, 1, 0, 0), (3, 3, 0, 0), (5, 4, 0, 0), (15, 5, 0, 0),
             (7, 6, 0, 0), (9, 6, 0, 15), (21, 7, 0, 0), (35, 7, 0, 15),
             (45, 1, 1, 0), (63, 1, 1, 15), (105, 3, 1, 0), (315, 3, 1, 15)]
    second = [(1, 4, 1, 0), (3, 4, 3, 0), (5, 5, 1, 0), (15, 5, 3, 0),
              (7, 6, 1, 0), (9, 6, 1, 15), (21, 6, 3, 0), (35, 6, 3, 15),
              (45, 7, 1, 0), (63, 7, 1, 15), (105, 7, 3, 0), (315, 7, 3, 15)]
    classes = []
    for power, rows in ((16, first), (32, second)):
        require(tuple(sorted(row[0] for row in rows)) == divisors(M),
                'Missing or duplicated original tail label')
        for d, b, j, z in rows:
            z += 2
            binary = b + 8 * j
            require(0 <= binary < power and gcd(power, d) == 1, 'Invalid CRT input')
            # CRT construction; the independent verifier below only tests x % n.
            phase = binary + power * (((z - binary) * pow(power, -1, d)) % d) if d > 1 else binary
            classes.append((power * d, phase))
    require(len(set(n for n, a in classes)) == 24, 'Moduli not distinct')
    require(all(N % n == 0 and n >= 8 and 0 <= a < n for n, a in classes),
            'Invalid original congruence')
    require(all(any(x % n == a for n, a in classes) for x in points),
            'Unconditioned witness misses literal demand')
    require((16, 1) in classes, 'Wrong free16 phase')
    require(all(x % 16 != 2 for x in points), 'Prescribed16 has positive gain')
    V = (frozenset((2, 17)),) * 12
    D2 = divisors(M)
    D1 = tuple(d for d in D2 if d != 1)
    B = frozenset(divisors(15))
    conditioned = vertex_cut(M, V, D1, D2, frozenset(), B)
    free = vertex_cut(M, V, D2, D2, frozenset(), B)
    require(conditioned == {'cost': 10, 'required': 14, 'strict_gap': 4},
            'Wrong prescribed resource cut')
    require(free == {'cost': 12, 'required': 12, 'strict_gap': 0},
            'Wrong unconditioned equality')
    return {'period': N, 'parents': parents, 'marked_parent': 2,
            'cofactor_pair': [2, 17], 'subset_of_fixed_root_residual': True,
            'demand_points': len(points), 'point_sha256': sha256(json.dumps(points).encode()).hexdigest(),
            'original_classes': classes, 'free16': [16, 1], 'prescribed16': [16, 2],
            'single_eraser_labels': sorted(B), 'free_cut': free,
            'conditioned_cut': conditioned,
            'scope': 'Artificial residual demand; realization by a chosen core not asserted'}


def run():
    return {'author': 'six-covering-2', 'role': 'researcher',
            'small_audit': audit_small(), 'fixture': original_fixture()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = json.loads(json.dumps(run()))
    if args.expected:
        require(result == json.loads(args.expected.read_text()), 'Frozen manifest mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
