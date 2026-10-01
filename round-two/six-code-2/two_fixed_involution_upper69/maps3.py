"""Two actual multiplicity-three exchanged saturated-pair map generators.

six-code-2, researcher. Complete multiplicity-three exchanged-pair map census.
Runtime credit: published sharp58 bundle, a70013740de126fe482870dcc6c162a292b042e9.
"""
from itertools import combinations, permutations
from pathlib import Path
import sys
import time
from bootstrap import ensure_runtime
ensure_runtime()
from carrier import check_code, image, mask, matching, normalize, require


def common(quads, mate):
    tails = tuple(sorted(tuple(v for v in q if v != mate) for q in quads if mate in q))
    require(len(tails) == 3 and all(len(t) == 3 for t in tails) and
            len({v for t in tails for v in t}) == 9, 'three disjoint common tails')
    left = tuple(sorted(set(range(18))-{17, mate}-{v for t in tails for v in t}))
    require(len(left) == 7, 'seven complement points')
    return tails, left


def check_map(g, tails, left, mate):
    require(sorted(g) == list(range(18)) and all(g[g[v]] == v for v in range(18)) and
            sum(g[v] == v for v in range(18)) == 2 and g[17] == mate and g[mate] == 17,
            'actual swapped2^8*1^2 permutation')
    require({frozenset(g[v] for v in t) for t in tails} == {frozenset(t) for t in tails}
            and set(g[v] for v in left) == set(left), 'common-tail/complement action')
    fixed = sum({g[v] for v in t} == set(t) for t in tails)
    require(fixed == 1 and sum(g[v] == v for v in left) == 1, 'one fixed tail/complement vertex')
    return fixed


def pair(g, a, b):
    require(g[a] == g[b] == -1 and a != b, 'unassigned transposition')
    g[a], g[b] = b, a


def tail_maps(quads, mate):
    tails, left = common(quads, mate); out = []
    for fixed_tail in range(3):
        a, b = tuple(i for i in range(3) if i != fixed_tail)
        for fixed_vertex in tails[fixed_tail]:
            for target in permutations(tails[b]):
                for complement_fixed in left:
                    for complement_pairs in matching(tuple(v for v in left if v != complement_fixed)):
                        g = [-1]*18; pair(g, 17, mate)
                        g[fixed_vertex] = fixed_vertex; g[complement_fixed] = complement_fixed
                        pair(g, *tuple(v for v in tails[fixed_tail] if v != fixed_vertex))
                        for v, w in zip(tails[a], target):
                            pair(g, v, w)
                        for v, w in complement_pairs:
                            pair(g, v, w)
                        check_map(g, tails, left, mate); out.append(tuple(g))
    require(len(out) == len(set(out)) == 5670, 'tail case count/uniqueness')
    return tuple(sorted(out))


def point_maps(quads, mate, node_cap=100000, seconds=5):
    """All fixed-point choices; independently ordered point/domain DFS."""
    require(0 <= node_cap <= 100000 and 0 < seconds <= 5, 'fixed operational guards')
    tails, left = common(quads, mate)
    block_of = {v: i for i, t in enumerate(tails) for v in t}
    block_of.update({v: 3 for v in left})
    out = []; nodes = 0; started = time.monotonic()
    for fixed_vertices in combinations(sorted(block_of), 2):
        if any(sum(v in t for v in fixed_vertices) == 2 for t in tails):
            continue
        g = [-1]*18; pair(g, 17, mate); partners = {3: 3}
        for v in fixed_vertices:
            g[v] = v; partners[block_of[v]] = block_of[v]
        def visit():
            nonlocal nodes
            nodes += 1
            if nodes > node_cap or time.monotonic()-started > seconds:
                raise TimeoutError('INCOMPLETE point-map100000/5s guard')
            remaining = tuple(v for v in sorted(block_of) if g[v] == -1)
            if not remaining:
                check_map(g, tails, left, mate); out.append(tuple(g)); return
            a = min(remaining, key=lambda v: (0 if block_of[v] in partners else 1, v))
            ia = block_of[a]
            for b in remaining:
                if a == b:
                    continue
                ib = block_of[b]
                if ia in partners and partners[ia] != ib or ib in partners and partners[ib] != ia:
                    continue
                if ia == ib and ia not in partners:
                    continue
                new = ia not in partners
                if new:
                    partners[ia], partners[ib] = ib, ia
                pair(g, a, b); visit(); g[a], g[b] = -1, -1
                if new:
                    del partners[ia]; del partners[ib]
        visit()
    require(len(out) == len(set(out)) == 5670, 'point carrier count/uniqueness')
    return tuple(sorted(out)), nodes


def anchor(quads, mate, g):
    star = tuple(mask(q)|(1 << 17) for q in quads)
    private = tuple(w for w in star if not w >> mate & 1)
    moved = tuple(image(w, g) for w in private)
    if any((a & b).bit_count() > 2 for a in private for b in moved):
        return None
    words = tuple(sorted(set(star)|{image(w, g) for w in star}))
    degrees = check_code(words, g)
    require(len(words) == 37 and degrees[17] == degrees[mate] == 20 and
            sum(w >> 17 & 1 and w >> mate & 1 for w in words) == 3, 'complete multiplicity-three star union')
    return words
