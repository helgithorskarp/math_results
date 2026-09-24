"""Exact compatibility in the common eleven-point local completion problem."""

from functools import cache
from hashlib import sha256
from itertools import combinations, permutations
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def build_local_table(use_symmetry=True):
    # Five through rows are the vertices of K_5 minus edge {0,1}.
    columns = (1, 2) + tuple((1 << u) | (1 << v)
                            for u, v in combinations(range(5), 2) if (u, v) != (0, 1))
    edges = tuple((u, v) for u, v in combinations(range(11), 2)
                  if not columns[u] & columns[v])
    blocks = tuple(sum(1 << p for p in block) for block in combinations(range(11), 5))
    coverage = {block: sum(1 << i for i, (u, v) in enumerate(edges)
                           if block >> u & 1 and block >> v & 1) for block in blocks}

    actions = []
    for first in permutations(range(2)):
        for last in permutations(range(2, 5)):
            perm = first + last
            action = tuple(columns.index(sum(1 << perm[i] for i in range(5) if c >> i & 1))
                           for c in columns)
            require(len(set(action)) == 11, 'local action is not a permutation')
            require({tuple(sorted((action[u], action[v]))) for u, v in edges} == set(edges),
                    'local action does not preserve missed pairs')
            actions.append(action)
    images = {block: tuple(sum(1 << action[p] for p in range(11) if block >> p & 1)
                           for action in actions) for block in blocks}

    # Replacing a coverage mask by a superset cannot hurt an at-most-k cover.
    candidates = []
    for mask in sorted(set(coverage.values()), key=lambda value: (-value.bit_count(), value)):
        if not any(mask | kept == kept for kept in candidates):
            candidates.append(mask)
    incident = tuple(tuple(mask for mask in candidates if mask >> i & 1)
                     for i in range(len(edges)))

    @cache
    def cover(uncovered, remaining):
        if not uncovered:
            return True
        if remaining == 0:
            return False
        if remaining == 1:
            return any(uncovered & mask == uncovered for mask in candidates)
        if uncovered.bit_count() > remaining * max((mask & uncovered).bit_count()
                                                   for mask in candidates):
            return False
        pivot = min((i for i in range(len(edges)) if uncovered >> i & 1),
                    key=lambda i: len(incident[i]))
        return any(cover(uncovered & ~mask, remaining - 1) for mask in incident[pivot])

    universe = (1 << len(edges)) - 1
    block_answers = {}
    allowed = set()
    for block in blocks:
        representative = min(images[block]) if use_symmetry else block
        if representative not in block_answers:
            block_answers[representative] = cover(universe & ~coverage[representative], 4)
        if block_answers[representative]:
            allowed.add(block)

    pair_answers = {}
    compatible = set()
    # Keep the original combination order: it fixes the reference traversal.
    allowed_order = [block for block in blocks if block in allowed]
    for left, right in combinations(allowed_order, 2):
        if use_symmetry:
            representative = min(tuple(sorted((u, v)))
                                 for u, v in zip(images[left], images[right]))
        else:
            representative = tuple(sorted((left, right)))
        if representative not in pair_answers:
            u, v = representative
            pair_answers[representative] = cover(universe & ~(coverage[u] | coverage[v]), 3)
        if pair_answers[representative]:
            compatible.add(tuple(sorted((left, right))))

    encoded = json.dumps(dict(allowed=sorted(allowed), compatible=sorted(compatible)),
                         separators=(',', ':')).encode()
    summary = dict(points=len(columns), missed_pairs=len(edges),
                   allowed_blocks=len(allowed), compatible_pairs=len(compatible),
                   table_sha256=sha256(encoded).hexdigest())
    # Cache size is operational evidence, not part of the mathematical table.
    operational = dict(block_queries=len(block_answers), pair_queries=len(pair_answers),
                       memoized_states=cover.cache_info().misses)
    return columns, allowed, compatible, summary, operational
