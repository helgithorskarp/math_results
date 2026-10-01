#!/usr/bin/env python3
"""Rational maximal-rank repair under the STRICT inherited pair-deletion cap.

See STRICT_DELETION_REPAIR.md. Failure of the strict scalar hypothesis is
outside this construction, and is not H or capped-H nonexistence.
"""
from fractions import Fraction as F
from itertools import combinations

import certificates as base
import deletions as inherited
import maxrank_mixtures as repair


def _integer(value, minimum, name):
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(name + ' must be an integer >= ' + str(minimum))


def normalized_pairs(n, deleted_pairs):
    _integer(n, 4, 'n')
    result = []
    for pair in deleted_pairs:
        if not isinstance(pair, (tuple, list)) or len(pair) != 2:
            raise ValueError('Every deleted edge must have two endpoints')
        a, b = pair
        _integer(a, 0, 'endpoint'); _integer(b, 0, 'endpoint')
        if a >= n or b >= n or a == b:
            raise ValueError('Invalid deleted edge')
        edge = tuple(sorted((a, b)))
        if edge in result:
            raise ValueError('Repeated deleted edge')
        result.append(edge)
    result.sort()
    if len({a for edge in result for a in edge}) == n:
        raise ValueError('At least one coordinate must be untouched')
    return result


def members(n, deleted_pairs, shift=0):
    edges = normalized_pairs(n, deleted_pairs)
    _integer(shift, 0, 'shift')
    deleted = set(edges)
    return sorted([0] + [1 << (shift+i) for i in range(n)] +
                  [(1 << (shift+a)) | (1 << (shift+b))
                   for a, b in combinations(range(n), 2) if (a, b) not in deleted])


def bipartite_components(n, deleted_pairs):
    """Each nonisolated bipartite component, with a deterministic signed basis."""
    edges = normalized_pairs(n, deleted_pairs)
    neighbors = [set() for _ in range(n)]
    for a, b in edges:
        neighbors[a].add(b); neighbors[b].add(a)
    unseen = {i for i in range(n) if neighbors[i]}
    answer = []
    while unseen:
        first = min(unseen); signs = {first: 1}; stack = [first]
        vertices = set(); bipartite = True
        while stack:
            a = stack.pop()
            if a in vertices:
                continue
            vertices.add(a); unseen.discard(a)
            for b in sorted(neighbors[a]):
                if b in signs:
                    if signs[b] != -signs[a]:
                        bipartite = False
                else:
                    signs[b] = -signs[a]; stack.append(b)
        if bipartite:
            answer.append({'vertices': sorted(vertices),
                           'signs': [signs.get(i, 0) for i in range(n)],
                           'vertex': first, 'neighbor': min(neighbors[first])})
    return answer


def uniform_entry(n, t, a, b):
    if a == b:
        return F(n-1)
    if a & b:
        return F(-1)
    if a.bit_count() == b.bit_count() == 1:
        return -1 + (n-2)*(n-3)*t
    if a.bit_count() == b.bit_count() == 2:
        return F(2, n-2) + t
    return F(2, n-2) - (n-3)*t


def parameters(n, deleted_pairs):
    edges = normalized_pairs(n, deleted_pairs)
    data = inherited.deletion_data(n, edges)
    _, scalar = inherited.cap_test(n, edges)
    if scalar >= 1:
        raise ValueError('Strict inherited cap hypothesis fails; no nonexistence verdict')
    N = data['N']
    mu = data['delta'] * (1-scalar) / N
    gamma = F((n-2)*(n-3)*(2*n-1), 2)
    t = mu / (2*gamma)
    untouched = sorted(set(range(n)) - {a for edge in edges for a in edge})
    components = bipartite_components(n, edges)
    family = members(n, edges)
    original = [(2*next(i for i in range(n) if a >> i & 1)
                 if a.bit_count() == 1 else
                 sum(i for i in range(n) if a >> i & 1)) % n
                for a in family[1:]]
    colors = []
    for component in components:
        row = original[:]
        a, b = component['vertex'], component['neighbor']
        row[family[1:].index(1 << a)] = (a+b) % n
        colors.append(row)
    beta = max([0] + [n*max(row.count(c) for c in range(n))-N for row in colors])
    epsilon = mu / (2*(mu+2*beta)) if components else None
    return dict(n=n, N=N, s=n, r=len(untouched), k=len(edges), edges=edges,
                untouched=untouched, components=components, scalar=scalar,
                delta=data['delta'], mu=mu, gamma=gamma, t=t,
                colors=colors, beta=beta, epsilon=epsilon)


def retained_core(n, deleted_pairs):
    data = parameters(n, deleted_pairs)
    family = members(n, data['edges'])
    C = [[uniform_entry(n, data['t'], a, b) for b in family[1:]]
         for a in family[1:]]
    if data['components']:
        partitions = [repair.partition_core(row, n) for row in data['colors']]
        number = len(partitions)
        P = [[sum(A[i][j] for A in partitions)/number
              for j in range(len(C))] for i in range(len(C))]
        C = repair.mix_cores(C, P, data['epsilon'])
    return C


def certificate(n, deleted_pairs, shift=0):
    edges = normalized_pairs(n, deleted_pairs)
    family = members(n, edges, shift)
    return family, base.lift(retained_core(n, edges), n), n


def matching_certificate(n, k, shift=0):
    _integer(n, 4, 'n'); _integer(k, 0, 'k')
    if 2*k >= n:
        raise ValueError('Matching must leave an untouched coordinate')
    return certificate(n, [(a, n-1-a) for a in range(k)], shift)


def partial_star_certificate(n, k, shift=0):
    _integer(n, 4, 'n'); _integer(k, 0, 'k')
    if k > n-2:
        raise ValueError('Partial star must leave an untouched coordinate')
    return certificate(n, [(0, a) for a in range(1, k+1)], shift)
