#!/usr/bin/env python3
"""Exact necessary fan/interface cover, not an enumeration of spherical maps.

Actual author six-tammes-1, researcher, 2026-10-01. Standard library only.
The written geometric and original-face bridges in PROOF.md are essential.
"""
from collections import Counter
from itertools import combinations, permutations, product
from functools import lru_cache
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


@lru_cache(None)
def partitions(n):
    """All equivalence relations, using restricted growth words."""
    if n == 0:
        return ((),)
    result = []

    def extend(word, highest):
        if len(word) == n:
            result.append(tuple(word))
            return
        for label in range(highest + 2):
            extend(word + [label], max(highest, label))

    extend([0], 0)
    return tuple(result)


def normalize(stars):
    labels = {i: i for i in range(3)}
    for star in stars:
        for point in star:
            if point not in labels:
                labels[point] = len(labels)
    return tuple(tuple(labels[x] for x in star) for star in stars)


def valid(stars, five_edges, triangle_ceiling=2, common_ceiling=2):
    if any(len(s) != 5 or len(set(s)) != 5 or i in s
           for i, s in enumerate(stars)):
        return False
    actual_five_edges = {tuple(sorted((i, j))) for i, s in enumerate(stars)
                         for j in s if j < 3}
    if actual_five_edges != set(five_edges):
        return False
    triangles = {tuple(sorted((i, s[j], s[j + 1])))
                 for i, s in enumerate(stars) for j in range(4)}
    edges = {e for t in triangles for e in combinations(t, 2)}
    points = sorted({x for s in stars for x in s} | {0, 1, 2})
    neighbors = {x: set() for x in points}
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    incidence = Counter(x for t in triangles for x in t)
    if any(incidence[x] > triangle_ceiling or len(neighbors[x]) > 4
           for x in points if x >= 3):
        return False
    if any(neighbors[i] != set(stars[i]) or incidence[i] != 4
           for i in range(3)):
        return False
    if any(len(neighbors[a] & neighbors[b]) > common_ceiling
           for a, b in combinations(points, 2)):
        return False
    if any(sum(a in t and b in t for t in triangles) > 2 for a, b in edges):
        return False
    for a, b in five_edges:
        shared = {t for t in triangles if a in t and b in t}
        if len(shared) != 2:
            return False
        for center, other in [(a, b), (b, a)]:
            j = stars[center].index(other)
            if j not in (1, 2, 3):
                return False
            local = {tuple(sorted((center, other, stars[center][j - 1]))),
                     tuple(sorted((center, other, stars[center][j + 1])))}
            if local != shared:
                return False
    return True


def fan_cover(five_edges):
    """Raw internal placements, both TT matchings, all remaining aliases."""
    neighbors = {i: [] for i in range(3)}
    for a, b in five_edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    choices = [list(permutations((1, 2, 3), len(neighbors[i])))
               for i in range(3)]
    charts = set()
    counts = Counter()
    for positions in product(*choices):
        counts['raw_placement_words'] += 1
        stars = [[3 + 5 * i + j for j in range(5)] for i in range(3)]
        for i in range(3):
            for j, where in zip(neighbors[i], positions[i]):
                stars[i][where] = j
        points = set(range(3)) | {x for s in stars for x in s}
        for matching in product((0, 1), repeat=len(five_edges)):
            counts['TT_matching_words'] += 1
            parent = {x: x for x in points}

            def root(x):
                while parent[x] != x:
                    x = parent[x]
                return x

            for (a, b), flip in zip(five_edges, matching):
                ia, ib = stars[a].index(b), stars[b].index(a)
                left = [stars[a][ia - 1], stars[a][ia + 1]]
                right = [stars[b][ib - 1], stars[b][ib + 1]]
                if flip:
                    right.reverse()
                for x, y in zip(left, right):
                    rx, ry = root(x), root(y)
                    if rx != ry:
                        parent[ry] = rx
            groups = {}
            for x in points:
                groups.setdefault(root(x), set()).add(x)
            # Unknown slots cannot become a five: the prescribed five graph
            # and every five's five distinct neighbors are already complete.
            if any(any(x < 3 for x in g) and len(g) != 1
                   for g in groups.values()):
                continue
            free = sorted((r for r, g in groups.items()
                           if all(x >= 3 for x in g)), key=lambda r: min(groups[r]))
            require(len(free) <= 7, 'Unexpected interface domain size')
            counts['interface_equivalence_relations'] += 1
            for word in partitions(len(free)):
                counts['original_alias_partitions'] += 1
                names = {root(i): i for i in range(3)}
                names.update({r: 3 + label for r, label in zip(free, word)})
                trial = tuple(tuple(names[root(x)] for x in s) for s in stars)
                if valid(trial, five_edges):
                    charts.add(normalize(trial))
    return sorted(charts), dict(sorted(counts.items()))


def qq_ends(edges, deficient):
    return {x: sum(x in e for e in edges) for x in deficient}


def digest_entries(entries):
    return hashlib.sha256(json.dumps(sorted(entries), separators=(',', ':')).encode()).hexdigest()


def clique_alias_cover():
    """All original endpoint/opposite aliases, including reciprocal edges."""
    records = []
    for b in range(4):
        a = 6 - 2 * b
        ordinary = set(range(6, 9 + b))
        one = set(range(9 + b, 9 + b + a))
        zero = set(range(9 + b + a, 15))
        deficient = one | zero
        require(len(zero) == b and 2 * a + 4 * b == 12, 'Census mismatch')
        # All three ordinary internals are fixed actual originals 6,7,8.
        # Other endpoints are distinct, outside these, and not zero-T.
        pool = sorted((ordinary - {6, 7, 8}) | one)
        counts = Counter()
        entries = []
        minimum = None
        relaxed = 0
        for endpoints in permutations(pool, 3):
            for opposites in product(sorted(deficient), repeat=3):
                counts['all_endpoint_opposite_assignments'] += 1
                if any(opposites[i] == endpoints[i] for i in range(3)):
                    counts['repeated_Q_original_rejections'] += 1
                    entries.append((endpoints, opposites, 'Q_REPEAT', ()))
                    continue
                if any(opposites[(i + 1) % 3] == endpoints[i] for i in range(3)):
                    counts['sealed_degree_four_link_rejections'] += 1
                    entries.append((endpoints, opposites, 'SEALED_LINK', ()))
                    continue
                counts['proper_link_assignments'] += 1
                if not any(x in one for x in endpoints):
                    require(b == 3 and a == 0, 'Missing one-T endpoint outside zero-T case')
                    counts['forced_T_at_zero_T_opposite'] += 1
                    entries.append((endpoints, opposites, 'ZERO_T_FORCE', ()))
                    continue
                edges = {tuple(sorted((6 + (i - 1) % 3, opposites[i])))
                         for i in range(3)}
                edges |= {tuple(sorted((endpoints[i], opposites[i])))
                          for i in range(3) if endpoints[i] in one}
                ends = qq_ends(edges, deficient)
                total = sum(ends.values())
                minimum = total if minimum is None else min(minimum, total)
                require(total >= 5, 'QQ lower incidence debt failed')
                locally_possible = all(ends[x] <= (2 if x in one else 4)
                                       for x in deficient)
                counts['local_QQ_capacity_rejections'] += int(not locally_possible)
                entries.append((endpoints, opposites,
                                'TOTAL_DEMAND' if locally_possible else 'LOCAL_SUPPLY',
                                tuple(ends[x] for x in sorted(deficient))))
                if locally_possible:
                    require(total + 9 > 12, 'Three-neighbor capacity exclusion failed')
                    counts['total_three_neighbor_capacity_rejections'] += 1
                    relaxed += int(total + 3 <= 12)
        records.append({'b': b, 'a': a, 'ordinary_fours': 3 + b,
                        'counts': dict(sorted(counts.items())),
                        'minimum_certified_non_three_QQ_ends': minimum,
                        'entrywise_sha256': digest_entries(entries),
                        'relaxed_three_neighbor_demand_3_controls': relaxed})
    return records


def path_alias_cover():
    # Exact eight-T union forces ordinary internals6..10, one-T endpoints
    # 11,12 and zero-T points13,14. The three threes are3,4,5.
    one, zero = {11, 12}, {13, 14}
    deficient = one | zero
    entries = []
    for shared in sorted(zero):
        for middle in sorted(deficient):
            edges = {tuple(sorted(e)) for e in
                     [(6, shared), (7, middle), (8, middle),
                      (11, shared), (12, shared)]}
            ends = qq_ends(edges, deficient)
            require(sum(ends.values()) == 7, 'Path incidence debt failed')
            local = all(ends[x] <= (2 if x in one else 4) for x in deficient)
            require(not local or sum(ends.values()) + 9 > 12,
                    'Path three-neighbor debt not excluded')
            entries.append({'shared_opposite': shared, 'middle_opposite': middle,
                            'non_three_QQ_ends': ends,
                            'local_capacity_ok': local,
                            'relaxed_demand_3_control': local and sum(ends.values()) + 3 <= 12})
    require(sum(e['relaxed_demand_3_control'] for e in entries) == 2,
            'Nonempty path control failed')
    return entries


def main():
    path_edges = ((0, 1), (1, 2))
    clique_edges = ((0, 1), (0, 2), (1, 2))
    path, pc = fan_cover(path_edges)
    clique, cc = fan_cover(clique_edges)
    require(len(path) == 8 and len(clique) == 16, 'Fan normal-form cover changed')
    # A concrete released-common-contact control identifies the two external
    # path endpoints. This is a surrogate contact complex, not a packing.
    shared_endpoint = ((3, 1, 4, 5, 6), (4, 0, 3, 2, 7), (3, 1, 7, 8, 6))
    require(not valid(shared_endpoint, path_edges), 'Third common contact accepted')
    require(valid(shared_endpoint, path_edges, common_ceiling=3),
            'Released common-contact control unexpectedly empty')
    graphs = []
    all_edges = ((0, 1), (0, 2), (1, 2))
    for bits in product((0, 1), repeat=3):
        e = sum(bits)
        graphs.append({'five_edges': [p for p, bit in zip(all_edges, bits) if bit],
                       'ordinary_internal_debt': 9 - 2 * e,
                       'internal_capacity_ok': 9 - 2 * e <= 6})
    require(sum(g['internal_capacity_ok'] for g in graphs) == 4,
            'Three-five graph cover changed')
    result = {'actual_agent': 'six-tammes-1', 'role': 'researcher',
              'status': 'exact finite necessary fan/alias checks; written geometry unformalized',
              'scope': 'complete connected strictly convex hemispherical T/Q15 contact graph,9Q,n5=3,all fives4T,1/2<c<3/5',
              'five_graphs': graphs,
              'path': {'cover_counts': pc, 'charts': path, 'opposite_aliases': path_alias_cover()},
              'clique': {'cover_counts': cc, 'charts': clique, 'opposite_aliases': clique_alias_cover()},
              'controls': {'shared_path_endpoint_rejects': True,
                           'same_endpoint_with_common_contact_bound_3_accepts': True,
                           'relaxed_three_neighbor_demand_3_has_nonempty_QQ_prefixes': True,
                           'controls_are_not_spherical_maps': True},
              'exact_angle_comparison_squares': {'49>45': 49 > 45, '529>512': 529 > 512},
              'full_global_Tammes15_bounds_unchanged': True}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
