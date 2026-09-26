#!/usr/bin/env python3
"""Separate author audit: matching reduction and exact quadratic identities.

Does not import verify.py or solve its stationary systems. This is algorithmic
independence within an author package, not independent peer acceptance.
"""
import argparse
from fractions import Fraction as F
import itertools
import json
from pathlib import Path


def check(condition, message):
    if not condition:
        raise ValueError(message)


def scalar(u, v):
    return sum(a*b for a, b in zip(u, v))


def transform(s, x):
    return [scalar(row, x) for row in s]


def squared_distance(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def all_subsets(n):
    for k in range(n+1):
        yield from itertools.combinations(range(n), k)


def sos_matrix(dimension, terms):
    """Terms (coefficient, linear form) produce the exact quadratic matrix."""
    return [[sum(c*v[i]*v[j] for c, v in terms)
             for j in range(dimension)] for i in range(dimension)]


def audit(path):
    data = json.loads(path.read_text())
    a = [[1, 0, 1], [0, 1, 1], [-1, 0, 1], [0, -1, 1]]
    b = [[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1]]
    check(data['A'] == a and data['B'] == b, 'wrong coordinates')
    check(F(data['contrast_bound']) == F(3, 7), 'wrong claimed constant')
    source = a + [[-c for c in row] for row in b] + [[0, 0, 0]]
    target = a + b + [[0, 0, 0]]
    edge_vertices = []
    for u in range(9):
        for v in range(u+1, 9):
            before = squared_distance(source[u], source[v])
            after = squared_distance(target[u], target[v])
            check(before >= after, 'not a contraction')
            if before != after:
                check((before, after) == (9, 1), 'wrong Gaussian product distances')
                edge_vertices.append((u, v))
    check(data['strict_cross_edges'] == [[u, v-4] for u, v in edge_vertices],
          'edge certificate does not match all pairwise distances')
    check(len(edge_vertices) == 8, 'not eight strict pairs')
    independent = [set(t) for t in all_subsets(8)
                   if all(not ({u, v} <= set(t)) for u, v in edge_vertices)]
    maximal = [s for s in independent if all(not (s < t) for t in independent)]
    masks = sorted(sum(1 << i for i in s) for s in maximal)
    check(len(independent) == data['independent_support_count'] == 47,
          'incomplete independent-set enumeration')
    check(masks == [f['mask'] for f in data['maximal_faces']], 'maximal face coverage failed')
    signs = strict = 0
    for entry in data['maximal_faces']:
        support = [i for i in range(8) if entry['mask'] & (1 << i)] + [8]
        matrix = [[F(c) for c in row] for row in entry['reflection']]
        check(len(matrix) == 3 and all(len(row) == 3 for row in matrix), 'bad matrix size')
        for i, j in itertools.product(range(3), repeat=2):
            check(matrix[i][j] == matrix[j][i], 'reflection is not symmetric')
            check(sum(matrix[k][i]*matrix[k][j] for k in range(3)) == int(i == j),
                  'reflection is not orthogonal')
        check(all(transform(matrix, source[i]) == target[i] for i in support),
              'does not map the whole face')
        for i in range(9):
            reflected_target = transform(matrix, target[i])
            check(scalar(reflected_target, reflected_target) == scalar(source[i], source[i]),
                  'polarization requires equal norms')
            displacement = [r-x for r, x in zip(reflected_target, source[i])]
            values = [scalar(source[j], displacement) for j in support]
            check(all(q >= 0 for q in values), 'polarization sign failed')
            signs += len(values)
            if i not in support:
                check(any(q > 0 for q in values), 'strict exterior-site check failed')
                strict += 1

    # Build the edge cycle using shared endpoints, then graph distances.
    adjacency = [[j for j, t in enumerate(edge_vertices)
                  if j != i and set(e).intersection(t)]
                 for i, e in enumerate(edge_vertices)]
    check(all(len(row) == 2 for row in adjacency), 'edge intersection graph not a cycle')
    distances = []
    for root in range(8):
        dist = {root: 0}
        queue = [root]
        for i in queue:
            for j in adjacency[i]:
                if j not in dist:
                    dist[j] = dist[i]+1
                    queue.append(j)
        check(len(dist) == 8, 'disconnected edge cycle')
        distances.append(dist)
    matrix = [[F(1) if distances[i][j] <= 1 else
               F(1, 2) if distances[i][j] == 2 else F(0)
               for j in range(8)] for i in range(8)]
    for i, (u, v) in enumerate(edge_vertices):
        for j, (r, s) in enumerate(edge_vertices):
            check(matrix[i][j] == F(int((u, s) in edge_vertices)
                                    + int((r, v) in edge_vertices), 2),
                  'cycle matrix does not equal vertex-load quadratic')
    # Moving adjacent positive masses to one endpoint preserves their quadratic
    # self-contribution because M_ii=M_ij=M_jj=1. All other terms are linear.
    check(all(matrix[i][i] == matrix[i][j] == matrix[j][j] == 1
              for i in range(8) for j in adjacency[i]), 'mass-merging premise failed')
    counts = {'empty': 0, 'one': 0, 'two': 0, 'three_path': 0,
              'three_edge_and_isolate': 0, 'four_cycle': 0}
    for support in all_subsets(8):
        if any(j in adjacency[i] for i, j in itertools.combinations(support, 2)):
            continue
        n = len(support)
        check(n <= 4, 'matching larger than four')
        restricted = [[matrix[i][j] for j in support] for i in support]
        if n <= 2:
            counts[['empty', 'one', 'two'][n]] += 1
            # q >= sum z_i^2 >= (sum z_i)^2/2 for at most two nonnegative variables.
            check(all(c >= 0 for row in restricted for c in row), 'negative entry')
            check(all(restricted[i][i] == 1 for i in range(n)), 'wrong diagonal')
            continue
        pairs = [(i, j) for i in range(n) for j in range(i+1, n)
                 if restricted[i][j] == F(1, 2)]
        check(all(restricted[i][j] in (0, F(1, 2))
                  for i in range(n) for j in range(i+1, n)), 'unexpected cross coefficient')
        if n == 3 and len(pairs) == 1:
            counts['three_edge_and_isolate'] += 1
            u, v = pairs[0]
            w = next(i for i in range(3) if i not in (u, v))
            first, second = [F(0)]*3, [F(0)]*3
            first[u], first[v] = 1, -1
            second[u], second[v], second[w] = 3, 3, -4
            terms = [(F(1, 4), first), (F(1, 28), second)]
            bound = F(3, 7)
        elif n == 3 and len(pairs) == 2:
            counts['three_path'] += 1
            middle = next(i for i in range(3) if sum(i in pair for pair in pairs) == 2)
            leaves = [i for i in range(3) if i != middle]
            first, second = [F(0)]*3, [F(0)]*3
            first[leaves[0]], first[leaves[1]], second[middle] = 1, -1, 1
            terms = [(F(1, 2), first), (F(1, 2), second)]
            bound = F(1, 2)
        else:
            check(n == 4 and len(pairs) == 4, 'unexpected matching type')
            check(all(sum(i in pair for pair in pairs) == 2 for i in range(4)),
                  'four-edge interaction graph not a cycle')
            counts['four_cycle'] += 1
            terms = []
            for u, v in itertools.combinations(range(4), 2):
                if (u, v) not in pairs:
                    vector = [F(0)]*4
                    vector[u], vector[v] = 1, -1
                    terms.append((F(1, 2), vector))
            bound = F(1, 2)
        residual = [[restricted[i][j]-bound for j in range(n)] for i in range(n)]
        check(residual == sos_matrix(n, terms), 'exact SOS coefficient identity failed')
    check(sum(counts.values()) == 47, 'matching coverage failed')
    flow = [F(x) for x in data['sharp_unit_edge_flow']]
    packet = [F(x) for x in data['sharp_probability_packet']]
    check(len(flow) == len(packet) == 8 and min(flow+packet) >= 0
          and sum(flow) == sum(packet) == 1, 'bad sharp fixture')
    check(all(sum(flow[e] for e, uv in enumerate(edge_vertices) if i in uv) == 2*packet[i]
              for i in range(8)), 'flow and packet mismatch')
    delta = min(sum(packet[i] for i in range(8) if i not in s) for s in maximal)
    tau = sum(packet[u]*packet[v] for u, v in edge_vertices)
    check(delta == F(1, 2) and tau == F(3, 28), 'sharpness failed')
    return {'status': 'SEPARATE_MATCHING_SOS_AUDIT_PASS', 'maximal_faces': len(maximal),
            'polarization_scalar_checks': signs, 'strict_exterior_sites': strict,
            'matching_types': counts, 'sharp_constant': '3/7',
            'claim_scope': 'finite obligations; analytic proof in PROOF.md remains a trust boundary'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).with_name('CERTIFICATE.json'))
    args = parser.parse_args()
    print(json.dumps(audit(args.certificate), sort_keys=True))
