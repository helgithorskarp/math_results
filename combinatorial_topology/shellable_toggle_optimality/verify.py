#!/usr/bin/env python3
"""Exact corroboration of shelling-to-toggle compilation; CPython 3.11+, stdlib."""
from collections import Counter, deque
from hashlib import sha256
from heapq import heappop, heappush
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def subsets(mask):
    current = mask
    while True:
        yield current
        if current == 0:
            return
        current = (current - 1) & mask


def encode(facets):
    require(bool(facets), 'nonvoid complex required')
    answer = []
    for facet in facets:
        require(bool(facet), 'facets must be nonempty')
        require(all(type(v) is int and v >= 0 for v in facet), 'bad vertex')
        require(len(set(facet)) == len(facet), 'repeated vertex')
        answer.append(sum(1 << v for v in facet))
    require(len(set(answer)) == len(answer), 'duplicate facet')
    return answer


def restrictions(facets, pure=True):
    masks = encode(facets)
    if pure:
        require(len({f.bit_count() for f in masks}) == 1, 'not pure')
    require(not any(a != b and a & b == a for a in masks for b in masks),
            'nested purported facets')
    old, result = set(), []
    for f in masks:
        new = set(subsets(f)) - old
        require(bool(new), 'no new face')
        r = f
        for x in new:
            r &= x
        require(new == {x for x in subsets(f) if x & r == r},
                'not a shelling order')
        result.append(r)
        old.update(subsets(f))
    return masks, result


def clearing(ideals):
    if not ideals:
        return []
    last = ideals[-1]
    return (clearing(ideals[:-1])
            + clearing([x & last for x in ideals[:-1]])[::-1] + [last])


def compile_word(facets):
    masks, rs = restrictions(facets)
    word = []
    for f, r in zip(masks, rs):
        vertices = [j for j in range(r.bit_length()) if r >> j & 1]
        word.extend(clearing([f ^ (1 << j) for j in vertices]))
        word.append(f)
    return word, rs


def as_set(mask):
    return frozenset(j for j in range(mask.bit_length()) if mask >> j & 1)


def faces_and_mu(facets):
    # Independent of bitmask shelling intervals and the dual-interval formula.
    faces = {frozenset()}
    for f in facets:
        for k in range(len(f) + 1):
            faces.update(frozenset(s) for s in combinations(sorted(f), k))
    ordered = sorted(faces, key=lambda f: (len(f), tuple(sorted(f))))
    mu = {}
    for f in ordered[::-1]:
        mu[f] = -1 - sum(value for g, value in mu.items() if f < g)
    return ordered, mu


def replay(facets, word, optimal=True):
    faces, mu = faces_and_mu(facets)
    on, used, signed = set(), Counter(), Counter()
    for step, move in enumerate(word):
        face = as_set(move)
        require(face in mu, f'nonface move at {step}')
        require(mu[face] != 0, f'zero-Moebius move at {step}')
        ideal = {g for g in faces if g <= face}
        intersection = on & ideal
        require(not intersection or intersection == ideal,
                f'nonmonochromatic move at {step}')
        signed[face] += -1 if intersection else 1
        used[face] += 1
        on.symmetric_difference_update(ideal)
    require(on == set(faces), 'wrong final state')
    require(all(signed[f] == -mu[f] for f in faces), 'wrong net multiplicity')
    if optimal:
        require(all(used[f] == abs(mu[f]) for f in faces), 'not facewise optimal')
    return faces, mu, used


def shortest(facets, cost=None):
    # Definition-level BFS/Dijkstra; does not use shelling or the length formula.
    faces, mu = faces_and_mu(facets)
    require(len(faces) <= 16, 'BFS/Dijkstra fixture exceeds declared bound')
    moves = [(sum(1 << i for i, g in enumerate(faces) if g <= f), f)
             for f in faces if mu[f]]
    goal = (1 << len(faces)) - 1
    if cost is None:
        queue, distance = deque([0]), {0: 0}
        while queue:
            state = queue.popleft()
            if state == goal:
                return distance[state]
            for mask, _ in moves:
                if state & mask in (0, mask):
                    nxt = state ^ mask
                    if nxt not in distance:
                        distance[nxt] = distance[state] + 1
                        queue.append(nxt)
    else:
        heap, distance = [(0, 0)], {0: 0}
        while heap:
            dist, state = heappop(heap)
            if distance[state] != dist:
                continue
            if state == goal:
                return dist
            for mask, f in moves:
                if state & mask in (0, mask):
                    nxt, value = state ^ mask, dist + cost(f)
                    if nxt not in distance or value < distance[nxt]:
                        distance[nxt] = value
                        heappush(heap, (value, nxt))
    raise ValueError('goal unreachable')


def polynomial_from_faces(faces, q):
    # Literal f-to-h binomial transform, independent of restriction counts.
    from math import comb
    coeffs = [0] * (q + 1)
    for f in faces:
        for j in range(q - len(f) + 1):
            coeffs[len(f) + j] += (-1) ** j * comb(q - len(f), j)
    return coeffs


def audit(facets):
    word, rs = compile_word(facets)
    faces, mu, used = replay(facets, word)
    q = len(facets[0])
    h = polynomial_from_faces(faces, q)
    require(h == [sum(r.bit_count() == k for r in rs) for k in range(q + 1)],
            'h coefficients disagree')
    require(len(word) == sum(a * 2 ** i for i, a in enumerate(h)), 'h(2) mismatch')
    require(len(word) == sum(abs(v) for v in mu.values()), 'Moebius norm mismatch')
    # Audit the new interval identity entry by entry, not only aggregate counts.
    masks = encode(facets)
    for f in faces:
        count = sum(as_set(mask ^ r) <= f <= as_set(mask)
                    for mask, r in zip(masks, rs))
        require(mu[f] == (-1) ** (q - len(f) + 1) * count, 'dual interval identity')
        require(used[f] == count, 'compiler multiplicity')
    return {'facets': len(facets), 'faces': len(faces), 'h': h,
            'moves': len(word), 'zeros': sum(v == 0 for v in mu.values()),
            'max_abs_mu': max(abs(v) for v in mu.values())}


def all_small():
    families = accepted = rejected = bfs_count = 0
    length_histogram, canonical = Counter(), []
    for q in range(1, 5):
        universe = list(combinations(range(4), q))
        for mask in range(1, 1 << len(universe)):
            family = [f for i, f in enumerate(universe) if mask >> i & 1]
            first = None
            families += 1
            for order in permutations(family):
                try:
                    restrictions(order)
                except ValueError:
                    rejected += 1
                    continue
                record = audit(order)
                accepted += 1
                if first is None:
                    first = record
                require(record == first, 'shelling-dependent invariant')
            if first is not None:
                distance = shortest(family)
                require(distance == first['moves'], 'BFS disagrees')
                bfs_count += 1
                length_histogram[distance] += 1
                canonical.append([q, mask, distance])
    digest = sha256(json.dumps(canonical, separators=(',', ':')).encode()).hexdigest()
    return {'labelled_uniform_families_on_four_labels': families,
            'accepted_orders': accepted, 'rejected_orders': rejected,
            'BFS_optima': bfs_count, 'optimal_length_histogram': dict(sorted(length_histogram.items())),
            'canonical_BFS_sha256': digest}


def fixtures():
    cases = []
    for q in range(1, 8):
        cases.append((f'simplex_{q}', [tuple(range(q))]))
    cases.append(('five_isolated_vertices', [(i,) for i in range(5)]))
    cases.append(('tetrahedron_boundary', list(combinations(range(4), 3))))
    cases.append(('two_tetrahedra', [(0, 1, 2, 3), (1, 2, 3, 4)]))
    for n in (3, 4, 5, 8, 12):
        cases.append((f'cone_cycle_{n}', [(0, i, i % n + 1) for i in range(1, n + 1)]))
    for n, q in ((6, 2), (6, 3), (7, 4)):
        cases.append((f'uniform_{q}_{n}', list(combinations(range(n), q))))
    for q in (2, 3, 4, 6):
        cases.append((f'crosspolytope_boundary_{q}',
                      [tuple(2 * i + bit for i, bit in enumerate(bits))
                       for bits in product((0, 1), repeat=q)]))
    for q in (2, 3, 5):
        cases.append((f'stacked_ball_{q}', [tuple(range(i, i + q)) for i in range(6)]))
    for size in (2, 3, 4):
        def v(i, j):
            return i * (size + 1) + j
        triangles = []
        for i in range(size):
            for j in range(size):
                lower = (v(i, j), v(i + 1, j), v(i + 1, j + 1))
                upper = (v(i, j), v(i, j + 1), v(i + 1, j + 1))
                triangles += [lower, upper] if i == 0 else [upper, lower]
        cases.append((f'grid_disk_{size}', triangles))
    return {name: audit(facets) for name, facets in cases}


def negative_controls():
    malformed = [[], [()], [(0, 1), (0, 1)], [(0, 0)], [(-1,)], [(True,)],
                 [(0, 1), (2, 3)], [(0, 1), (1, 2), (0, 3, 4)]]
    rejected = 0
    for item in malformed:
        try:
            compile_word(item)
        except ValueError:
            rejected += 1
    require(rejected == len(malformed), 'malformed input accepted')
    cone = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1)]
    word, _ = compile_word(cone)
    corrupt = [word[:-1], word + [1 << 1], [1 << 20] + word, word[1:]]
    rejected_words = 0
    for bad in corrupt:
        try:
            replay(cone, bad)
        except ValueError:
            rejected_words += 1
    require(rejected_words == len(corrupt), 'corrupt word accepted')
    nonpure = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (0, 4)]
    masks, rs = restrictions(nonpure, pure=False)
    bad = []
    for f, r in zip(masks, rs):
        bad += clearing([f ^ (1 << j) for j in range(r.bit_length()) if r >> j & 1]) + [f]
    try:
        replay(nonpure, bad)
    except ValueError as error:
        require('zero-Moebius' in str(error), 'wrong nonpure failure')
    else:
        raise ValueError('nonpure cancellation not detected')
    require(faces_and_mu(nonpure)[1][frozenset({0})] == 0, 'nonpure cancellation')
    witness = encode([(0, 1, 2), (0, 1), (0, 4), (0, 2), (0, 1, 3), (0, 3), (0, 2, 3)])
    replay(nonpure, witness)
    require(shortest(nonpure) == 7, 'nonpure optimum')
    try:
        compile_word(nonpure)
    except ValueError:
        rejected += 1
    else:
        raise ValueError('nonpure compiler input accepted')
    return {'input_rejections': rejected, 'corrupt_word_rejections': rejected_words,
            'nonpure_naive_word_rejected_at_zero': True, 'nonpure_actual_optimum': 7}


def weighted_controls():
    families = [[(0,), (1,), (2,)], [(0, 1), (1, 2)],
                [(0, 1, 2), (1, 2, 3)], list(combinations(range(4), 3))]
    costs = [lambda f: len(f), lambda f: (sum(f) + 2 * len(f) + 1) % 5,
             lambda f: 0 if 0 in f else 3]
    values = []
    for family in families:
        word, _ = compile_word(family)
        _, mu, _ = replay(family, word)
        for cost in costs:
            bound = sum(cost(f) * abs(m) for f, m in mu.items())
            actual = sum(cost(as_set(f)) for f in word)
            require(actual == bound == shortest(family, cost), 'weighted optimum')
            values.append(bound)
    return values


def main():
    evidence = {'small_exhaustive': all_small(), 'fixtures': fixtures(),
                'weighted_Dijkstra_optima': weighted_controls(),
                'negative_controls': negative_controls()}
    digest = sha256(json.dumps(evidence, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = {'status': 'VERIFIED', 'evidence_sha256': digest, 'evidence': evidence}
    if sys.argv[1:] != ['--emit']:
        require(not sys.argv[1:], 'usage: verify.py [--emit]')
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        # JSON canonicalization normalizes histogram integer keys.
        require(json.loads(json.dumps(result)) == expected, 'expected record mismatch')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
