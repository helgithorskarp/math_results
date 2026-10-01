#!/usr/bin/env python3
"""Complementary incidence/link audit. Imports no production code.

It reconstructs accepted fan charts from triangle-incidence patches and
rechecks all terminal aliases with binary neighbor rows. Completeness of
the raw-to-patch bridge is the written proof, not an independent review.
Actual author six-tammes-1, researcher, 2026-10-01.
"""
from collections import Counter
from itertools import combinations, permutations, product
import hashlib
import json


def ensure(value, message):
    if not value:
        raise RuntimeError(message)


def canonical(words):
    old = [0, 1, 2]
    for row in words:
        for x in row:
            if x not in old:
                old.append(x)
    return tuple(tuple(old.index(x) for x in row) for row in words)


def triangle_patch_words(triangles):
    possibilities = []
    for f in range(3):
        pairs = {tuple(sorted(x for x in t if x != f)) for t in triangles if f in t}
        vertices = sorted({x for e in pairs for x in e})
        ensure(len(vertices) == 5 and len(pairs) == 4, 'Not a four-T five link')
        words = [w for w in permutations(vertices)
                 if {tuple(sorted((w[i], w[i + 1]))) for i in range(4)} == pairs]
        ensure(len(words) == 2, 'Fan path has unexpected orientation count')
        possibilities.append(words)
    return {canonical(ws) for ws in product(*possibilities)}


def incidence_chart_sets():
    pwords = ((3, 1, 4, 5, 6), (4, 0, 3, 2, 7), (3, 1, 7, 8, 9))
    path_triangles = {tuple(sorted((f, w[j], w[j + 1])))
                      for f, w in enumerate(pwords) for j in range(4)}
    ensure(len(path_triangles) == 8, 'Path triangle union changed')
    path = triangle_patch_words(path_triangles)
    clique = set()
    for step in (1, 2):
        triangles = {(0, 1, 2)}
        for i in range(3):
            triangles.add(tuple(sorted((i, (i + step) % 3, 3 + i))))
            triangles.add(tuple(sorted((i, 3 + i, 6 + i))))
        ensure(len(triangles) == 7, 'Triangle patch union changed')
        clique |= triangle_patch_words(triangles)
    ensure(len(path) == 8 and len(clique) == 16, 'Incidence charts changed')
    return {'path': sorted(path), 'clique': sorted(clique)}


def link_cycles(vertices, needed):
    """Hamiltonian four-neighbor cycles containing all known face corners."""
    vertices = set(vertices)
    if len(vertices) == 3:
        # Local fourth-neighbor wildcard; any remaining original gives this
        # same incidence check. It is not a sixteenth actual code point.
        vertices.add(16)
    ensure(len(vertices) == 4, 'Unexpected degree-four neighbor domain')
    start = min(vertices)
    result = []
    for tail in permutations(sorted(vertices - {start})):
        cycle = (start,) + tail
        edges = {tuple(sorted((cycle[i], cycle[(i + 1) % 4]))) for i in range(4)}
        if set(needed) <= edges:
            result.append(edges)
    return result


def bits_add(rows, u, v):
    ensure(u != v, 'Loop in original QQ contact list')
    rows[u] |= 1 << v
    rows[v] |= 1 << u


def checksum(entries):
    return hashlib.sha256(json.dumps(sorted(entries), separators=(',', ':')).encode()).hexdigest()


def clique_opposites():
    result = []
    zero_T_released_link_options = set()
    for b in range(4):
        a = 6 - 2 * b
        ordinary = set(range(6, 9 + b))
        one = set(range(9 + b, 9 + b + a))
        zero = set(range(9 + b + a, 15))
        deficient = sorted(one | zero)
        pool = sorted((ordinary - {6, 7, 8}) | one)
        counts, entries = Counter(), []
        least, relaxed = None, 0
        # An unordered endpoint subset and its six original assignments;
        # opposite choices are decoded as base-m digits, not primary loops.
        for subset in combinations(pool, 3):
            for endpoint in permutations(subset):
                for number in range(len(deficient) ** 3):
                    digits, n = [], number
                    for _ in range(3):
                        n, digit = divmod(n, len(deficient))
                        digits.append(deficient[digit])
                    opposite = tuple(digits)
                    counts['all_endpoint_opposite_assignments'] += 1
                    quads = [(i, 6 + (i - 1) % 3, opposite[i], endpoint[i]) for i in range(3)]
                    if any(len(set(q)) < 4 for q in quads):
                        counts['repeated_Q_original_rejections'] += 1
                        entries.append((endpoint, opposite, 'Q_REPEAT', ()))
                        continue
                    possible = True
                    for i in range(3):
                        nxt = (i + 1) % 3
                        neighbors = [i, nxt, endpoint[i], opposite[nxt]]
                        needed = [tuple(sorted(e)) for e in
                                  [(nxt, i), (i, endpoint[i]), (nxt, opposite[nxt])]]
                        if not link_cycles(neighbors, needed):
                            possible = False
                    if not possible:
                        counts['sealed_degree_four_link_rejections'] += 1
                        entries.append((endpoint, opposite, 'SEALED_LINK', ()))
                        continue
                    counts['proper_link_assignments'] += 1
                    if not any(x in one for x in endpoint):
                        ensure(b == 3 and not one, 'Ordinary endpoint census failed')
                        for i in range(3):
                            fi, ii, hi, wild = i, 6 + i, opposite[i], 16
                            required = [tuple(sorted((fi, ii))), tuple(sorted((fi, hi)))]
                            choices = link_cycles([fi, ii, hi, wild], required)
                            for cycle in choices:
                                for second_T in cycle - set(required):
                                    ensure(ii in second_T or hi in second_T,
                                           'Unknown second-T option')
                                    # Ii's two known Ts are full and its other
                                    # one excludes this endpoint. The only
                                    # released option puts the new T at Hi.
                                    if hi in second_T:
                                        zero_T_released_link_options.add((i, hi, tuple(sorted(second_T))))
                        counts['forced_T_at_zero_T_opposite'] += 1
                        entries.append((endpoint, opposite, 'ZERO_T_FORCE', ()))
                        continue
                    rows = [0] * 15
                    for i in range(3):
                        bits_add(rows, 6 + (i - 1) % 3, opposite[i])
                        if endpoint[i] in one:
                            bits_add(rows, endpoint[i], opposite[i])
                    degrees = tuple(rows[x].bit_count() for x in deficient)
                    total = sum(degrees)
                    ensure(total >= 5 and total + 9 > 12, 'QQ debt not excluded')
                    least = total if least is None else min(least, total)
                    local = all(rows[x].bit_count() <= (2 if x in one else 4)
                                for x in deficient)
                    tag = 'TOTAL_DEMAND' if local else 'LOCAL_SUPPLY'
                    counts['local_QQ_capacity_rejections'] += int(not local)
                    if local:
                        counts['total_three_neighbor_capacity_rejections'] += 1
                        relaxed += int(total + 3 <= 12)
                    entries.append((endpoint, opposite, tag, degrees))
        result.append({'b': b, 'a': a, 'ordinary_fours': 3 + b,
                       'counts': dict(sorted(counts.items())),
                       'minimum_certified_non_three_QQ_ends': least,
                       'entrywise_sha256': checksum(entries),
                       'relaxed_three_neighbor_demand_3_controls': relaxed})
    ensure(zero_T_released_link_options, 'Released zero-T link control empty')
    return result, len(zero_T_released_link_options)


def path_opposites():
    result = []
    for j in (13, 14):
        for k in range(11, 15):
            rows = [0] * 15
            for edge in [(6, j), (7, k), (8, k), (11, j), (12, j)]:
                bits_add(rows, *edge)
            degrees = {x: rows[x].bit_count() for x in range(11, 15)}
            ensure(sum(degrees.values()) == 7, 'Path debt changed')
            local = all(degrees[x] <= (2 if x < 13 else 4) for x in degrees)
            result.append({'shared_opposite': j, 'middle_opposite': k,
                           'non_three_QQ_ends': degrees,
                           'local_capacity_ok': local,
                           'relaxed_demand_3_control': local and sum(degrees.values()) + 3 <= 12})
    return result


def main():
    charts = incidence_chart_sets()
    triangles, released = clique_opposites()
    # Raw contact adjacency for the released shared endpoint control.
    bad_words = ((3, 1, 4, 5, 6), (4, 0, 3, 2, 7), (3, 1, 7, 8, 6))
    ts = {tuple(sorted((f, s[i], s[i + 1])))
          for f, s in enumerate(bad_words) for i in range(4)}
    rows = [0] * 15
    for t in ts:
        for u, v in combinations(t, 2):
            bits_add(rows, u, v)
    ensure((rows[0] & rows[2]).bit_count() == 3, 'Released endpoint control lost')
    print(json.dumps({'actual_agent': 'six-tammes-1', 'role': 'researcher',
                      'trust': 'complementary same-author incidence audit; hand-proof bridges unformalized',
                      'fan_charts': charts, 'clique_opposite_aliases': triangles,
                      'path_opposite_aliases': path_opposites(),
                      'released_zero_T_local_link_options': released,
                      'released_endpoint_common_contacts': 3}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
