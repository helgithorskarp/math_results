#!/usr/bin/env python3
"""Independent all-point support audit: edge decisions, point partitions, exact cliques."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import time

from exact import (insist, encoded, bits, mask, pairs, words_json, packing,
                   mul, plane, first_star, valid_extension, saturated_row,
                   compatibility, clique_census, point_capacity)

U, A, B = 17, 0, 16
X = (1, 2, 3, 4, 8, 12)
N = tuple(z for z in range(1, 17) if z not in X)
W = tuple(range(1, 17))
H = tuple(range(1, 16))
PAIR_UNIVERSE = tuple(combinations(range(1, 18), 2))
PAIR_INDEX = {p: i for i, p in enumerate(PAIR_UNIVERSE)}
REFERENCE_SHA256 = '50beb3262a2b28d494f423b385bc90b68013e0cd960d4551d3fce267f2b07c5f'


def leave_mask(edges):
    return sum(1 << PAIR_INDEX[p] for p in edges)


def edge_degree_graphs(vertices, degrees, allowed, cap=200000, seconds=10):
    """Binary decisions on edges; exhaust a given degree coefficient exactly."""
    insist(set(vertices) == set(degrees) and all(type(d) is int and d >= 0 for d in degrees.values()), 'degree domain')
    allowed = tuple(sorted(allowed, key=lambda p: (-sum(degrees[x] for x in p), -max(degrees[x] for x in p), p)))
    insist(len(allowed) == len(set(allowed)) and all(len(p) == 2 and p[0] < p[1] and set(p) <= set(vertices) for p in allowed), 'edge domain')
    indices = {x: i for i, x in enumerate(vertices)}
    edges = tuple((indices[x], indices[y]) for x, y in allowed)
    answers, states = [], 0
    started = time.monotonic()

    def visit(k, remaining, selected):
        nonlocal states
        states += 1
        if states > cap or time.monotonic() - started > seconds:
            raise RuntimeError('INCOMPLETE: degree graph guard')
        if not any(remaining):
            answers.append(tuple(sorted(allowed[i] for i in selected)))
            return
        if k == len(edges) or sum(remaining) % 2:
            return
        available = [0] * len(vertices)
        for i, j in edges[k:]:
            if remaining[i] and remaining[j]:
                available[i] += 1
                available[j] += 1
        if any(d > available[i] for i, d in enumerate(remaining)):
            return
        i, j = edges[k]
        if remaining[i] and remaining[j]:
            child = list(remaining)
            child[i] -= 1
            child[j] -= 1
            visit(k + 1, tuple(child), selected + (k,))
        visit(k + 1, remaining, selected)

    visit(0, tuple(degrees[x] for x in vertices), ())
    insist(len(answers) == len(set(answers)), 'duplicate degree graph')
    for edges_out in answers:
        got = Counter(x for edge in edges_out for x in edge)
        insist(all(got[x] == degrees[x] for x in vertices), 'false degree graph')
    return sorted(answers), states


def carrier():
    forced = frozenset((z, U) for z in N)
    forbidden = set(combinations(X[:3], 2)) | set(combinations(X[3:], 2))
    raw, total_states = {}, 0
    for c, d in combinations(W, 2):
        residual = {z: (4 if z in (c, d) else 1) - (z in N) for z in W}
        allowed = [(i, j) for i, j in combinations(W, 2) if (i, j) not in forbidden and residual[i] and residual[j]]
        graphs, states = edge_degree_graphs(W, residual, allowed)
        total_states += states
        for graph in graphs:
            leave = forced | frozenset(graph)
            deg = Counter(z for p in leave for z in p)
            insist(len(leave) == 16 and all(deg[z] == (10 if z == U else 4 if z in (c, d) else 1) for z in range(1, 18)), 'full leave degree')
            key = leave_mask(leave)
            insist(key not in raw, 'duplicate carrier')
            kind = 'end' if (c in X) != (d in X) else 'triangle' if (c, d) in leave else 'middle'
            raw[key] = {'edges': leave, 'centers': (c, d), 'kind': kind}
    return raw, total_states


def symmetry_group(root):
    # All invertible field matrices, with both field automorphisms, then a literal word filter.
    maps, matrices = set(), 0
    for r, s, t, v in product(range(4), repeat=4):
        if mul(r, v) == mul(s, t):
            continue
        matrices += 1
        for conjugate in (False, True):
            f = lambda z: mul(z, z) if conjugate else z
            p = tuple(4 * (mul(r, f(x)) ^ mul(s, f(y))) + (mul(t, f(x)) ^ mul(v, f(y)))
                      for x in range(4) for y in range(4)) + (B, U)
            insist(len(set(p)) == 18, 'singular field matrix')
            if {mask(p[z] for z in bits(w)) for w in root} == set(root):
                maps.add(p)
    insist(matrices == 180 and len(maps) == 36, 'flag group order')
    insist(all(tuple(p[q[z]] for z in range(18)) in maps for p in maps for q in maps), 'flag closure')
    insist(all(all(p[z] == z for z in (U, A, B)) for p in maps), 'flag labels')
    return tuple(sorted(maps))


def point_first_covers(required, columns, cap=200000, seconds=10):
    """Partition one point's neighbors first; memoize complete residual pair-cover suffixes."""
    required = tuple(sorted(required))
    insist(len(required) == len(set(required)), 'duplicate required pair')
    insist(len(columns) == len(set(columns)) and all(w.bit_count() == 4 for w in columns), 'column domain')
    required_set = set(required)
    insist(all(pairs(w) <= required_set for w in columns), 'column outside pair universe')
    if not required:
        return [()], {'point': None, 'partition_states': 0, 'residual_states': 0, 'memo_hits': 0, 'complete_point_partitions': 1}
    index = {p: i for i, p in enumerate(required)}
    row_words = [sum(1 << index[p] for p in pairs(w)) for w in columns]
    row_columns = [0] * len(required)
    for i, word in enumerate(row_words):
        for row in bits(word):
            row_columns[row] |= 1 << i
    conflicts = [0] * len(columns)
    for i, word in enumerate(row_words):
        for row in bits(word):
            conflicts[i] |= row_columns[row]
    vertices = sorted({z for p in required for z in p})
    neighbors = {z: mask(y if x == z else x for x, y in required if z in (x, y)) for z in vertices}
    point = min(vertices, key=lambda z: (neighbors[z].bit_count(), sum(w >> z & 1 for w in columns), z))
    if neighbors[point].bit_count() % 3:
        return [], {'point': point, 'partition_states': 0, 'residual_states': 0,
                    'memo_hits': 0, 'complete_point_partitions': 0}
    tails = [(w ^ 1 << point, i) for i, w in enumerate(columns) if w >> point & 1]
    tail_at = {z: [(tail, i) for tail, i in tails if tail >> z & 1] for z in bits(neighbors[point])}
    started = time.monotonic()
    counts = {'point': point, 'partition_states': 0, 'residual_states': 0, 'memo_hits': 0, 'complete_point_partitions': 0}
    cache, answers = {}, []

    def guard():
        if counts['partition_states'] + counts['residual_states'] > cap or time.monotonic() - started > seconds:
            raise RuntimeError('INCOMPLETE: point-first cover guard')

    def suffix(rows, active):
        counts['residual_states'] += 1
        guard()
        if not rows:
            return ((),)
        if rows in cache:
            counts['memo_hits'] += 1
            return cache[rows]
        best = None
        for row in bits(rows):
            choices = row_columns[row] & active
            if not choices:
                cache[rows] = ()
                return ()
            candidate = (choices.bit_count(), -row, choices)
            if best is None or candidate < best:
                best = candidate
        choices = best[2]
        out = []
        for i in bits(choices):
            insist(row_words[i] & rows == row_words[i], 'used pair in active column')
            for rest in suffix(rows ^ row_words[i], active & ~conflicts[i]):
                out.append(tuple(sorted((i,) + rest)))
        cache[rows] = tuple(out)
        return cache[rows]

    def partition(remaining, chosen, rows, active):
        counts['partition_states'] += 1
        guard()
        if not remaining:
            counts['complete_point_partitions'] += 1
            for rest in suffix(rows, active):
                answers.append(tuple(sorted(chosen + rest)))
            return
        z = (remaining & -remaining).bit_length() - 1
        for tail, i in tail_at[z]:
            if tail & remaining == tail:
                insist(active >> i & 1, 'disjoint tails have conflicting pair sets')
                partition(remaining ^ tail, chosen + (i,), rows ^ row_words[i], active & ~conflicts[i])

    partition(neighbors[point], (), (1 << len(required)) - 1, (1 << len(columns)) - 1)
    insist(len(answers) == len(set(answers)), 'duplicated complete cover')
    result = []
    for ids in answers:
        covered = Counter(p for i in ids for p in pairs(columns[i]))
        insist(set(covered) == required_set and set(covered.values()) == {1}, 'false complete cover')
        result.append(tuple(sorted(tuple(bits(columns[i])) for i in ids)))
    return sorted(result), counts


def decode_reference(raw_input):
    insist(sha256(raw_input).hexdigest() == REFERENCE_SHA256, 'reference hash mismatch')
    return json.loads(raw_input)


def compare_expected(actual, expected):
    insist(actual == expected, 'independent expected output mismatch')


def controls():
    """Literal small-instance enumerations, positive covers and rejection controls."""
    graph_count = degree_queries = cover_queries = clique_queries = 0
    for n in range(6):
        vertices = tuple(range(n))
        universe = tuple(combinations(vertices, 2))
        groups = defaultdict(list)
        for code in range(1 << len(universe)):
            edges = tuple(p for j, p in enumerate(universe) if code >> j & 1)
            degree = tuple(sum(z in p for p in edges) for z in vertices)
            groups[degree].append(edges)
            graph_count += 1
            edge_set = set(edges)
            columns = tuple(mask(q) for q in combinations(vertices, 4) if set(combinations(q, 2)) <= edge_set)
            literal = []
            for subset in range(1 << len(columns)):
                chosen = [columns[j] for j in bits(subset)]
                covered = Counter(p for w in chosen for p in pairs(w))
                if set(covered) == edge_set and all(d == 1 for d in covered.values()):
                    literal.append(tuple(sorted(tuple(bits(w)) for w in chosen)))
            got, _ = point_first_covers(edges, columns)
            insist(got == sorted(literal), 'point cover disagrees with literal subsets')
            cover_queries += 1
            adjacency = [sum(1 << y for x, y in edges if x == z) |
                         sum(1 << x for x, y in edges if y == z) for z in vertices]
            for size in range(n + 1):
                literal_cliques = [q for q in combinations(vertices, size)
                                   if all(tuple(p) in edge_set for p in combinations(q, 2))]
                got_cliques, _ = clique_census(adjacency, size)
                insist(got_cliques == literal_cliques, 'clique census disagrees with literal subsets')
                clique_queries += 1
        for degree, literal in groups.items():
            got, _ = edge_degree_graphs(vertices, dict(zip(vertices, degree)), universe)
            insist(got == sorted(literal), 'degree census disagrees with literal edge subsets')
            degree_queries += 1
    # All allowed-edge sets on four vertices, including missing allowed edges.
    vertices = tuple(range(4))
    universe = tuple(combinations(vertices, 2))
    restricted_queries = 0
    for code in range(1 << len(universe)):
        allowed = tuple(p for j, p in enumerate(universe) if code >> j & 1)
        groups = defaultdict(list)
        for sub in range(1 << len(allowed)):
            edges = tuple(p for j, p in enumerate(allowed) if sub >> j & 1)
            degree = tuple(sum(z in p for p in edges) for z in vertices)
            groups[degree].append(edges)
        for degree, literal in groups.items():
            got, _ = edge_degree_graphs(vertices, dict(zip(vertices, degree)), allowed)
            insist(got == sorted(literal), 'restricted degree census differs')
            restricted_queries += 1
    affine = plane()
    got, _ = point_first_covers(tuple(combinations(range(16), 2)), affine)
    insist(got == [tuple(sorted(tuple(bits(w)) for w in affine))], 'affine positive cover failed')
    joined = (mask((0, 1, 2, 3)), mask((0, 4, 5, 6)))
    got, _ = point_first_covers(pairs(joined[0]) | pairs(joined[1]), joined)
    insist(got == [tuple(sorted(tuple(bits(w)) for w in joined))], 'two-block positive cover failed')
    guarded = [lambda: edge_degree_graphs((0, 1), {0: 1, 1: 1}, ((0, 1),), cap=0),
               lambda: point_first_covers(pairs(mask(range(4))), (mask(range(4)),), cap=0),
               lambda: clique_census([0], 1, cap=0)]
    for function in guarded:
        try:
            function()
        except RuntimeError as error:
            insist('INCOMPLETE' in str(error), 'incorrect guard status')
        else:
            raise ValueError('zero-cap guard did not reject')
    invalid = [lambda: edge_degree_graphs((0, 1), {0: 1, 1: 1}, ((0, 0),)),
               lambda: point_first_covers(((0, 1), (0, 1)), ()),
               lambda: point_first_covers(((0, 1),), (mask(range(5)),)),
               lambda: clique_census([1], 1),
               lambda: decode_reference(b'{"status":"COMPLETE"}\n'),
               lambda: compare_expected(b'actual', b'altered')]
    for function in invalid:
        try:
            function()
        except ValueError:
            pass
        else:
            raise ValueError('invalid input was accepted')
    return {'literal_simple_graphs': graph_count, 'degree_queries': degree_queries,
            'restricted_degree_queries': restricted_queries, 'pair_cover_queries': cover_queries,
            'clique_queries': clique_queries, 'positive_covers': 2,
            'incomplete_controls': len(guarded), 'invalid_input_controls': len(invalid)}


def audit(target, only=None):
    path = target / 'single_isolate_expected.json'
    raw_input = path.read_bytes()
    source = decode_reference(raw_input)
    checked_controls = controls()
    root = first_star(B)
    saturated_row(root, U, {A: 3, B: 2})
    fixed = tuple(w for w in root if w & 1)
    forbidden = set(p for w in fixed for p in pairs(w ^ 1))
    raw, degree_states = carrier()
    maps = symmetry_group(root)
    remaining, cases = set(raw), []
    while remaining:
        representative = min(remaining)
        edges = raw[representative]['edges']
        orbit = {leave_mask(tuple(sorted((g[x], g[y]))) for x, y in edges) for g in maps}
        insist(orbit <= remaining, 'overlapping/incomplete leave orbit')
        remaining -= orbit
        cases.append({'representative': representative, 'orbit': orbit, **raw[representative]})
    insist(len(raw) == 3390 and len(cases) == 117, 'carrier/orbit counts differ')
    insist(only is None or 0 <= only < len(cases), 'invalid partial case')
    source_keys = {c['representative'] for c in source['cases']}
    insist({c['representative'] for c in cases} == source_keys, 'representative list differs')
    # Exact disjoint orbit expansion of untrusted representatives equals the independently generated carrier.
    source_carrier = {leave_mask(tuple(sorted((g[x], g[y]))) for x, y in PAIR_UNIVERSE if rep >> PAIR_INDEX[x, y] & 1)
                      for rep in source_keys for g in maps}
    insist(source_carrier == set(raw), 'literal raw leave cover differs')
    primary = tuple(mask(q) for q in combinations(W, 4) if valid_extension(mask(q) | 1, root))
    insist(len(primary) == 597, 'primary universe differs')
    base = set(combinations(W, 2)) - forbidden
    output = []
    for i, case in enumerate(cases):
        if only is not None and i != only:
            continue
        old = next(c for c in source['cases'] if c['representative'] == case['representative'])
        centers = case['centers']
        insist(case['kind'] == old['kind'] and set(centers) == set(old['high_centers']) and len(case['orbit']) == old['orbit_size'], 'orbit metadata differs')
        required = base - case['edges']
        columns = tuple(w for w in primary if pairs(w) <= required)
        row_hash = sha256(encoded(sorted(required))).hexdigest()
        column_hash = sha256(encoded(sorted(list(bits(w)) for w in columns))).hexdigest()
        insist(len(required) == 108 and len(columns) == old['columns'] and row_hash == old['rows_sha256'] and column_hash == old['columns_sha256'], 'cover input entry differs')
        covers, counts = point_first_covers(required, columns)
        old_stars = {tuple(tuple(q) for q in item['primary_extra_quads']): item for item in old['compatible_primary_stars']}
        insist(set(covers) == set(old_stars), 'completed star list differs')
        stars = []
        for cover in covers:
            second = fixed + tuple(mask(q) | 1 for q in cover)
            union = tuple(sorted(set(root) | set(second)))
            packing(union)
            insist(len(union) == 38, 'union size differs')
            saturated_row(union, U, {A: 3, B: 2})
            saturated_row(union, A, {U: 3, centers[0]: 1, centers[1]: 1})
            bfixed = sum(w >> B & 1 for w in union)
            secondary = tuple(mask(q) for q in combinations(H, 4) if valid_extension(mask(q) | 1 << B, union))
            bound, degrees = point_capacity(secondary, H)
            item = old_stars[cover]
            insist(bfixed == item['secondary_fixed_words'] and len(secondary) == item['secondary_candidates'] and degrees == item['pair_union_degrees'] and bound == item['upper_bound'] and sha256(encoded(sorted(list(bits(w)) for w in secondary))).hexdigest() == item['secondary_candidates_sha256'], 'secondary candidate entry differs')
            insist(bfixed + bound <= 19, 'source bound fails')
            graph = compatibility(secondary)
            opt_states = 0
            for maximum in range(bound, -1, -1):
                optima, states = clique_census(graph, maximum)
                opt_states += states
                if optima:
                    break
            witness = union + tuple(secondary[j] | 1 << B for j in optima[0])
            packing(witness)
            saturated_row(witness, U, {A: 3, B: 2})
            saturated_row(witness, A, {U: 3, centers[0]: 1, centers[1]: 1})
            insist(sum(w >> B & 1 for w in witness) == bfixed + maximum, 'false optimal witness')
            stars.append({'primary_extra_quads': [list(q) for q in cover], 'secondary_fixed': bfixed,
                          'secondary_candidates': len(secondary), 'pair_degrees': degrees, 'source_extra_bound': bound,
                          'exact_maximum_extra': maximum, 'sharp_secondary_replication': bfixed + maximum,
                          'optimal_extensions': len(optima), 'optimization_states': opt_states, 'witness': words_json(witness)})
        output.append({'index': i, 'representative': case['representative'], 'centers': list(centers), 'kind': case['kind'],
                       'orbit_size': len(case['orbit']), 'columns': len(columns), 'rows_sha256': row_hash,
                       'columns_sha256': column_hash, 'cover_counts': counts, 'stars': stars})
    return {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
            'status': 'COMPLETE' if only is None else 'PARTIAL', 'reference_sha256': sha256(raw_input).hexdigest(),
            'raw_leaves': len(raw), 'raw_counts': dict(Counter(c['kind'] for c in raw.values())),
            'carrier_states': degree_states, 'raw_leave_sha256': sha256(encoded(sorted(raw))).hexdigest(),
            'field_matrices': 180, 'flag_group': len(maps), 'orbits': len(cases),
            'orbit_counts': dict(Counter(c['kind'] for c in cases)), 'primary_candidates': len(primary),
            'controls': checked_controls, 'cases': output}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=Path, default=Path(__file__).resolve().parents[1] / 'constant_weight_18_6_5_equality_structure')
    parser.add_argument('--case', type=int, help='Explicit partial pilot only')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--record', action='store_true', help='Explicitly record a new independent baseline; does not compare it')
    args = parser.parse_args()
    result = audit(args.target, args.case)
    data = encoded(result)
    if args.case is None and not args.record:
        compare_expected(data, args.expected.read_bytes())
    if args.output:
        args.output.write_bytes(data)
    stars = [s for c in result['cases'] for s in c['stars']]
    print(json.dumps({'status': result['status'], 'orbits': result['orbits'],
                      'raw_leaves': result['raw_leaves'], 'stars': len(stars),
                      'sharp_secondary_maximum': max((s['sharp_secondary_replication'] for s in stars), default=None),
                      'output_sha256': sha256(data).hexdigest(), 'controls': result['controls']}, sort_keys=True))


if __name__ == '__main__':
    main()
