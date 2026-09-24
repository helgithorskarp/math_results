#!/usr/bin/env python3
"""Independent local proof: a different census and forced-block exhaustion.

No imports from classify/verify, no dual certificate, no solver, and no
canonicalization. All labelled multigraphs are checked individually.
"""

import hashlib
import json
from itertools import combinations, product


def independent_census():
    """Choose two singleton locations and the K_4 edge counts.

    The four edges incident with vertex 4 are then forced by degrees.
    This does not use the ten-edge recursion in classify.py.
    """
    edges = tuple(combinations(range(5), 2))
    first_four = tuple(combinations(range(4), 2))
    result = {}
    for s, t in combinations(range(6), 2):
        # Stars and bars: (s, t-1) is a multiset of two vertices in 0..4.
        singleton_vertices = (s, t - 1)
        singletons = [singleton_vertices.count(i) for i in range(5)]
        for counts in product(range(5), repeat=6):
            degrees = [sum(counts[e] for e, pair in enumerate(first_four) if i in pair)
                       for i in range(4)]
            last = [4 - singletons[i] - degrees[i] for i in range(4)]
            if min(last) < 0 or sum(last) != 4 - singletons[4]:
                continue
            multiplicity = dict(zip(first_four, counts))
            multiplicity.update({(i, 4): last[i] for i in range(4)})
            key = tuple(multiplicity[e] for e in edges)
            columns = ([frozenset([i]) for i in singleton_vertices]
                       + [frozenset(edge) for edge in edges
                          for _ in range(multiplicity[edge])])
            if key in result or len(columns) != 11:
                raise ValueError('independent census failed uniqueness or size')
            result[key] = columns
    return result


def no_four_block_completion(columns):
    # An uncovered point pair is exactly a pair of disjoint column supports.
    missing = [frozenset([u, v]) for u, v in combinations(range(11), 2)
               if columns[u].isdisjoint(columns[v])]
    neighbors = [set() for _ in range(11)]
    for pair in missing:
        u, v = sorted(pair)
        neighbors[u].add(v)
        neighbors[v].add(u)
    if min(map(len, neighbors)) < 4:
        raise ValueError('unexpected missing-pair degree')
    eligible = [i for i, n in enumerate(neighbors) if len(n) == 4]
    forced = {i: frozenset(neighbors[i] | {i}) for i in eligible}
    tried_pairs = 0
    tried_blocks = 0
    for i, j in combinations(eligible, 2):
        first, second = forced[i], forced[j]
        if first == second:
            raise ValueError('equal forced blocks require an additional case')
        if i in second or j in first:
            continue  # Would give a chosen degree-one point two incidences.
        tried_pairs += 1
        remaining = [pair for pair in missing if not (pair <= first or pair <= second)]
        if not remaining:
            raise ValueError('two forced blocks already complete this type')
        available = set(range(11)) - {i, j}
        pivot = remaining[0]
        if not pivot <= available:
            continue
        # At least one of the last two blocks contains the chosen pair.
        for extra in combinations(sorted(available - pivot), 3):
            third = set(pivot) | set(extra)
            tried_blocks += 1
            endpoints = set().union(*(pair for pair in remaining if not pair <= third))
            if endpoints <= available and len(endpoints) <= 5:
                raise ValueError('a possible fourth block survives')
    return tried_pairs, tried_blocks


def main():
    census = independent_census()
    pairs = blocks = 0
    for columns in census.values():
        new_pairs, new_blocks = no_four_block_completion(columns)
        pairs += new_pairs
        blocks += new_blocks
    encoded = json.dumps(sorted(census), separators=(',', ':')).encode()
    print(json.dumps(dict(status='INDEPENDENT_LOCAL_EXHAUSTION_PASSED',
                          labelled_types=len(census), forced_block_pairs=pairs,
                          third_block_trials=blocks,
                          labelled_census_sha256=hashlib.sha256(encoded).hexdigest()),
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
