"""Independent exhaustive mask audit of the order-10 F_541 lemma."""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations_with_replacement
from math import isqrt
from pathlib import Path


P = 541


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def audit() -> None:
    require(all(P % d for d in range(2, isqrt(P) + 1)), 'modulus is not prime')
    subgroup = {pow(493, j, P) for j in range(10)}
    require(len(subgroup) == 10 and pow(493, 10, P) == 1, 'wrong subgroup order')
    require(subgroup == {1, 48, 124, 140, 228, 313, 401, 417, 493, 540},
            'wrong subgroup elements')

    remaining = set(range(1, P))
    blocks: list[frozenset[int]] = []
    owner: dict[int, int] = {}
    while remaining:
        a = min(remaining)
        block = frozenset(a * h % P for h in subgroup)
        require(block <= remaining and len(block) == 10, 'overlapping cosets')
        for x in block:
            owner[x] = len(blocks)
        blocks.append(block)
        remaining -= block
    require(len(blocks) == 54 and len(owner) == 540 and blocks[0] == subgroup,
            'incomplete coset partition')

    # Derive every forbidden support directly from the modular equation.
    forbidden = set()
    for x, y in combinations_with_replacement(range(1, P), 2):
        z = (x + y) % P
        if z:
            forbidden.add(sum(1 << i for i in {owner[x], owner[y], owner[z]}))
    sizes = Counter(mask.bit_count() for mask in forbidden)
    require(sizes == {2: 216, 3: 4392}, 'wrong forbidden edge counts')
    touching = [[mask for mask in forbidden if mask >> i & 1] for i in range(54)]

    normalized: list[tuple[int, ...]] = []
    nine_count = 0
    nodes = 0

    def recurse(chosen: tuple[int, ...], mask: int) -> None:
        nonlocal nine_count, nodes
        nodes += 1
        if len(chosen) == 8:
            normalized.append(chosen)
        if len(chosen) == 9:
            nine_count += 1
            return
        for v in range(chosen[-1] + 1, 54):
            extended = mask | (1 << v)
            if all((extended & edge) != edge for edge in touching[v]):
                recurse(chosen + (v,), extended)

    recurse((0,), 1)
    require(len(normalized) == 56 and nine_count == 0,
            'wrong normalized maximum or nine-coset survivor')

    # Check all 56 actual residue unions without relying on the hypergraph.
    for chosen in normalized:
        values = set().union(*(blocks[i] for i in chosen))
        require(len(values) == 80, 'wrong residue count')
        require(all((x + y) % P not in values
                    for x, y in combinations_with_replacement(sorted(values), 2)),
                'non-sum-free maximum set')

    all_sets: set[tuple[int, ...]] = set()
    orbits: set[tuple[tuple[int, ...], ...]] = set()
    representatives: set[tuple[int, ...]] = set()
    for chosen in normalized:
        members = {
            tuple(sorted({owner[(a * x) % P] for i in chosen for x in blocks[i]}))
            for a in range(1, P)
        }
        require(all(len(m) == 8 for m in members), 'scalar image changed size')
        require(len(members) == 54, 'wrong scalar orbit size')
        all_sets.update(members)
        orbits.add(tuple(sorted(members)))
        representatives.add(tuple(min(blocks[i]) for i in min(members)))
    require(len(orbits) == 7 and len(all_sets) == 378,
            'wrong number of scaling types or maximum sets')
    fixture_path = (Path(__file__).resolve().parent.parent /
                    'schur6_cyclic541_multiplier_obstruction' /
                    'extremal_representatives.json')
    fixture = json.loads(fixture_path.read_text())
    require(fixture['modulus'] == P and set(fixture['subgroup']) == subgroup,
            'fixture field mismatch')
    require(sorted(map(tuple, fixture['representatives'])) == sorted(representatives),
            'representative catalog mismatch')

    sixth_roots = {x for x in range(1, P) if pow(x, 6, P) == 1}
    require({1, 129, 130} <= sixth_roots and (1 + 129) % P == 130,
            'sixth-root obstruction mismatch')
    require(52 * 52 % P == P - 1, 'order-four subgroup mismatch')
    print('PASS independent_cyclic541',
          'edges=0,216,4392', 'normalized=56', 'maximum_cosets=8',
          'all_maximum_sets=378', 'scaling_types=7', f'nodes={nodes}')


if __name__ == '__main__':
    audit()
