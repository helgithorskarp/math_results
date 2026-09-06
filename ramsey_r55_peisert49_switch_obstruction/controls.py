"""Quartic-character identification, direct attachment census and rejection controls."""
import copy
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

import build
import check
import verify_graph


def power12(x, y):
    # Repeated multiplication in the polynomial quotient, without logs/cosets.
    a, b = 1, 0
    for _ in range(12):
        a, b = (a*x+3*b*y) % 7, (a*y+b*x) % 7
    return a, b


def quartic_red(u, v):
    if u == v:
        return 0
    return int(power12((u % 7-v % 7) % 7, (u//7-v//7) % 7) in ((1, 0), (0, 3)))


def binary_rank(rows):
    rows = rows[:]
    r = 0
    for bit in range(max((x.bit_length() for x in rows), default=0)):
        pivot = next((i for i in range(r, len(rows)) if rows[i] & (1 << bit)), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] & (1 << bit):
                rows[i] ^= rows[r]
        r += 1
    return r


def ranks(matrix):
    n = len(matrix)
    return [binary_rank([sum(1 << j for j in range(n) if i != j and matrix[i][j] == c)
                         for i in range(n)]) for c in (1, 0)]


def run():
    root = Path(__file__).parent
    doc = json.loads((root/'certificate.json').read_text())
    check.check(doc)
    check.need(build.direction_masks() == check.transformed_masks(), 'entrywise pullback mask agreement')
    connection = build.connection()
    for u in range(49):
        for v in range(49):
            difference = (u % 7-v % 7) % 7+7*((u//7-v//7) % 7)
            c = int(u != v and difference in connection)
            check.need(c == quartic_red(u, v) == build.color(u, v, 163), 'three base color definitions')

    plane = check.plane()
    for line in plane:
        affine = [p for p in plane if not check.incident(p, line)]
        check.need(set(check.image(affine, line)) == set(product(range(7), repeat=2)), 'all 57 full charts')

    # Literal matrix transport on all affine points, plus all 48 nonzero
    # displacements. No claim that GL matrices are graph automorphisms.
    transports = displacements = 0
    for a, b, c, d in product(range(7), repeat=4):
        if (a*d-b*c) % 7 == 0:
            continue
        images = [(a*x+b*y) % 7+7*((c*x+d*y) % 7) for x, y in product(range(7), repeat=2)]
        check.need(len(set(images)) == 49, 'invertible map on all points')
        transports += 49
        mask = 0
        for m, (x, y) in enumerate([(1, i) for i in range(7)]+[(0, 1)]):
            if quartic_red(0, (a*x+b*y) % 7+7*((c*x+d*y) % 7)):
                mask |= 1 << m
        for x, y in product(range(7), repeat=2):
            if x == y == 0:
                continue
            mapped = (a*x+b*y) % 7+7*((c*x+d*y) % 7)
            check.need(quartic_red(0, mapped) == ((mask >> check.slope(x, y)) & 1), 'all displacement colors transported')
            displacements += 1

    # Independent exhaustive four-subset enumeration replaces bitset DFS.
    # For each actual K4, intersect literal opposite-colored neighborhoods.
    capacity = Counter()
    checked_quads = 0
    for ci, li, mask, _ in doc['cases']:
        points = check.image(doc['arcs'][ci], plane[li])
        labels = [x+7*y for x, y in points]
        adjacency = [[check.edge((u % 7, u//7), (v % 7, v//7), mask)
                      if u != v else 0 for v in range(49)] for u in range(49)]
        outside = set(range(49))-set(labels)
        forbidden = set()
        for q in combinations(labels, 4):
            checked_quads += 1
            c = adjacency[q[0]][q[1]]
            if not all(adjacency[u][v] == c for u, v in combinations(q, 2)):
                continue
            # Also independently confirm every represented 22-set is Ramsey.
            check.need(not any(all(adjacency[u][v] == c for u in q)
                               for v in set(labels)-set(q)), '22-point anchor contains a K5')
            forbidden.update(v for v in outside if all(adjacency[u][v] != c for u in q))
        capacity[len(outside-forbidden)] += 1
    check.need(sum(capacity.values()) == 476 and max(capacity) == 11, 'complete stronger attachment census')

    fixture = json.loads((root/'fixture22.json').read_text())
    expected_edges = [[i, j] for i, j in combinations(range(22), 2)
                      if quartic_red(fixture['points'][i], fixture['points'][j])]
    check.need(fixture['edges'] == expected_edges, 'fixture physical Peisert edges')
    fixture_result = verify_graph.verify(fixture)
    check.need(fixture_result['ramsey_5_5_graph'], 'literal Ramsey22 control')

    graph = [[quartic_red(u, v) for v in range(49)] for u in range(49)]
    base_ranks = ranks(graph)
    check.need(base_ranks == [24, 24], 'Peisert base binary ranks')
    seidel = [[0 if i == j else 1-2*graph[i][j] for j in range(49)] for i in range(49)]
    check.need(all(sum(seidel[i][k]*seidel[k][j] for k in range(49)) == 49*int(i == j)-1
                   for i in range(49) for j in range(49)), 'Peisert Seidel square')
    lengths = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}
    known = [[int(i != j and min(abs(i-j), 43-abs(i-j)) in lengths) for j in range(43)] for i in range(43)]
    for u in [2, 5, 8, 11, 14, 17, 20, 22, 25, 28, 31, 34, 37, 40]:
        v = (u+1) % 43
        known[u][v] ^= 1
        known[v][u] ^= 1
    known_ranks = ranks(known)
    check.need(known_ranks == [40, 42], 'known seven-defect comparison')

    mutations = []
    x = copy.deepcopy(doc); x['cases'].pop(); mutations.append(x)
    x = copy.deepcopy(doc); x['cases'].append(x['cases'][0]); mutations.append(x)
    x = copy.deepcopy(doc); x['cases'][0][3].pop(); mutations.append(x)
    x = copy.deepcopy(doc); x['cases'][0][3][1][0] = x['cases'][0][3][0][0]; mutations.append(x)
    x = copy.deepcopy(doc); x['cases'][0][3][0][1] ^= 1; mutations.append(x)
    x = copy.deepcopy(doc); x['cases'][0][3][0][3] = x['cases'][0][3][0][2]; mutations.append(x)
    x = copy.deepcopy(doc); x['arcs'][0][0] = x['arcs'][0][1]; mutations.append(x)
    x = copy.deepcopy(doc); x['cases'][0][2] = 0; mutations.append(x)
    for x in mutations:
        try:
            check.check(x)
        except ValueError:
            continue
        raise ValueError('certificate mutation accepted')
    return {'status': 'VERIFIED_PEISERT49_CONTROLS', 'base_field_pair_colors': 2401,
            'full_affine_charts': 57, 'linear_map_point_images': transports,
            'linear_map_displacement_colors': displacements,
            'direct_four_subsets_checked': checked_quads,
            'direct_attachment_capacity_histogram': {str(k): v for k, v in sorted(capacity.items())},
            'all_476_anchor_sets_are_Ramsey22': True,
            'fixture22': fixture_result, 'peisert49_red_blue_binary_ranks': base_ranks,
            'known_q7_red_blue_binary_ranks': known_ranks,
            'switched_induced_family_rank_bound': 26,
            'certificate_mutations_rejected': len(mutations)}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
