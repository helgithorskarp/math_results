#!/usr/bin/env python3
"""Separate degree-sequence, sparse Algorithm X, and direct XOR replay."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
U, A, B = 17, 0, 16
W = tuple(range(1, 17))
H = tuple(range(1, 16))
PAIRS = tuple(combinations(range(1, 18), 2))
MULT = ((0, 0, 0, 0), (0, 1, 2, 3), (0, 2, 3, 1), (0, 3, 1, 2))
SQUARE = (0, 1, 3, 2)


def require(value, message):
    if not value:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, separators=(',', ':'), sort_keys=True) + '\n').encode('ascii')


def decode(mask):
    return tuple(x for x in range(18) if mask >> x & 1)


def fixed_weight(vertices, weight):
    value = (1 << weight) - 1
    while value < 1 << len(vertices):
        yield sum(1 << x for i, x in enumerate(vertices) if value >> i & 1)
        low = value & -value
        nxt = value + low
        value = nxt | (((nxt ^ value) // low) >> 2)


def packing(words):
    require(len(words) == len(set(words)) and all(w.bit_count() == 5 and 0 <= w < 1 << 18
                                               for w in words), 'word weights/domain/distinctness')
    require(all((x ^ y).bit_count() >= 6 for x, y in combinations(words, 2)), 'word distances')


def first_star():
    even = [p for p in permutations(range(4))
            if sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0]
    lines = [sum(1 << (4 * x + p[x]) for x in range(4)) for p in even]
    lines += [sum(1 << (4 * x + y) for y in range(4)) for x in range(4)]
    lines += [sum(1 << (4 * x + y) for x in range(4)) for y in range(4)]
    counts = Counter(p for q in lines for p in combinations(decode(q), 2))
    require(len(set(lines)) == 20 and len(counts) == 120 and set(counts.values()) == {1}, 'permutation plane')
    axes = {sum(1 << x for x in (0, 1, 2, 3)), sum(1 << x for x in (0, 4, 8, 12))}
    star = sorted((q ^ 1 | 1 << B | 1 << U) if q & 1 and q not in axes else q | 1 << U
                  for q in lines)
    packing(star)
    require(len(star) == 20, 'first star size')
    return star


def first_group(star):
    generators = [tuple(4 * MULT[2][x] + y for x in range(4) for y in range(4)) + (B, U),
                  tuple(4 * x + MULT[2][y] for x in range(4) for y in range(4)) + (B, U),
                  tuple(4 * y + x for x in range(4) for y in range(4)) + (B, U),
                  tuple(4 * SQUARE[x] + SQUARE[y] for x in range(4) for y in range(4)) + (B, U)]
    seen = {tuple(range(18))}
    queue = list(seen)
    for p in queue:
        for g in generators:
            q = tuple(g[p[x]] for x in range(18))
            if q not in seen:
                seen.add(q)
                queue.append(q)
    require(len(seen) == 36, 'generated first-star group')
    for p in seen:
        require(len(set(p)) == 18 and all(p[x] == x for x in (U, A, B)), 'group permutation')
        require({sum(1 << p[x] for x in decode(w)) for w in star} == set(star), 'group word images')
    require(all(tuple(p[q[x]] for x in range(18)) in seen for p in seen for q in seen), 'group closure')
    return sorted(seen)


def pair_mask(edges):
    edges = set(edges)
    return sum(1 << i for i, p in enumerate(PAIRS) if p in edges)


def pair_edges(mask):
    return tuple(p for i, p in enumerate(PAIRS) if mask >> i & 1)


def degree_leaves(star):
    started = time.monotonic()
    fixed = [w for w in star if w & 1 << A]
    forbidden = {p for w in fixed for p in combinations(decode(w ^ 1 << A), 2)}
    axes_points = set(x for w in fixed for x in decode(w) if x not in (U, A))
    forced = {tuple(sorted((U, x))) for x in W if x not in axes_points}
    forced_degrees = Counter(x for p in forced for x in p)
    require(len(fixed) == 2 and len(axes_points) == 6 and len(forced) == 10
            and not forced & forbidden, 'forced primary leave')
    result = {}
    branch_nodes = 0
    for c, d in combinations(W, 2):
        target = {x: 10 if x == U else 4 if x in (c, d) else 1 for x in range(1, 18)}
        remaining = {x: target[x] - forced_degrees[x] for x in target}
        active = tuple(x for x in target if remaining[x])
        require(all(n >= 0 for n in remaining.values()), 'negative residual degree')

        def visit(chosen):
            nonlocal branch_nodes
            branch_nodes += 1
            if branch_nodes > 200000 or (branch_nodes % 128 == 0 and time.monotonic() - started > 10):
                raise RuntimeError('INCOMPLETE: degree-leave guard; no exclusion')
            positive = tuple(x for x in active if remaining[x])
            if not positive:
                actual = forced | set(chosen)
                degrees = Counter(x for p in actual for x in p)
                require(len(actual) == 16 and all(degrees[x] == target[x] for x in target)
                        and not actual & forbidden, 'degree-generated leaf')
                mask = pair_mask(actual)
                require(mask not in result, 'duplicate degree-generated leaf')
                if c in axes_points or d in axes_points:
                    require((c in axes_points) != (d in axes_points), 'both axes centers survived')
                    centers = (d, c) if c in axes_points else (c, d)
                    kind = 'end'
                else:
                    centers = (c, d)
                    kind = 'triangle' if (c, d) in actual else 'middle'
                result[mask] = (kind,) + centers
                return
            x = positive[0]
            need = remaining[x]
            candidates = tuple(y for y in positive[1:] if tuple(sorted((x, y))) not in forbidden)
            if need > len(candidates):
                return
            for neighbors in combinations(candidates, need):
                remaining[x] = 0
                for y in neighbors:
                    remaining[y] -= 1
                feasible = all(remaining[y] <= sum(remaining[z] > 0 and y != z
                    and tuple(sorted((y, z))) not in forbidden for z in active) for y in active if remaining[y])
                if feasible:
                    visit(chosen + tuple(tuple(sorted((x, y))) for y in neighbors))
                for y in neighbors:
                    remaining[y] += 1
                remaining[x] = need
        visit(())
    require(Counter(k for k, _, _ in result.values()) == {'middle': 900, 'end': 60, 'triangle': 2430},
            'complete degree leaf count')
    return result, forced, forbidden, branch_nodes


def sparse_covers(rows, columns, node_cap=200000, seconds=10):
    """Mutable set Algorithm X; reverse header ties and reverse column order."""
    column_pairs = tuple(tuple(combinations(q, 2)) for q in columns)
    headers = {p: set() for p in rows}
    for i, pairs in enumerate(column_pairs):
        require(len(pairs) == 6 and set(pairs) <= set(headers), 'column domain')
        for p in pairs:
            headers[p].add(i)
    started = time.monotonic()
    nodes = 0
    answers = []

    def cover(i):
        removed = []
        for p in column_pairs[i]:
            opts = headers.pop(p)
            for j in opts:
                for q in column_pairs[j]:
                    if q in headers:
                        require(j in headers[q], 'broken Algorithm X membership')
                        headers[q].remove(j)
            removed.append((p, opts))
        return removed

    def uncover(removed):
        for p, opts in reversed(removed):
            for j in opts:
                for q in column_pairs[j]:
                    if q in headers:
                        headers[q].add(j)
            headers[p] = opts

    def visit(chosen):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap or (nodes % 128 == 0 and time.monotonic() - started > seconds):
            raise RuntimeError('INCOMPLETE: sparse-cover guard; no exclusion')
        if not headers:
            answer = tuple(sorted(columns[i] for i in chosen))
            counts = Counter(p for q in answer for p in combinations(q, 2))
            require(set(counts) == set(rows) and set(counts.values()) <= {1}, 'incorrect sparse cover')
            answers.append(answer)
            return
        p = min(headers, key=lambda p: (len(headers[p]), -p[0], -p[1]))
        for i in sorted(headers[p], reverse=True):
            removed = cover(i)
            try:
                visit(chosen + (i,))
            finally:
                uncover(removed)
    visit(())
    require(len(answers) == len(set(answers)), 'duplicate sparse covers')
    return sorted(answers), nodes


def controls():
    count = 0
    for n in range(6):
        pairs = tuple(combinations(range(n), 2))
        for value in range(1 << len(pairs)):
            rows = tuple(p for i, p in enumerate(pairs) if value >> i & 1)
            columns = tuple(q for q in combinations(range(n), 4) if set(combinations(q, 2)) <= set(rows))
            expected = []
            for bits in range(1 << len(columns)):
                chosen = tuple(q for i, q in enumerate(columns) if bits >> i & 1)
                counts = Counter(p for q in chosen for p in combinations(q, 2))
                if set(counts) == set(rows) and set(counts.values()) <= {1}:
                    expected.append(chosen)
            actual, _ = sparse_covers(rows, columns)
            require(set(actual) == set(expected), 'brute-force cover control')
            count += 1
    aborted = False
    try:
        sparse_covers((), (), node_cap=0)
    except RuntimeError as exc:
        aborted = str(exc).startswith('INCOMPLETE')
    require(aborted, 'zero-cap guard accepted')
    star = first_star()
    plane = tuple(sorted(decode((w ^ 1 << U ^ 1 << B | 1 << A) if w & 1 << B else w ^ 1 << U)
                         for w in star))
    actual, _ = sparse_covers(tuple(combinations(range(16), 2)), plane)
    require(actual == [plane], 'positive affine cover rejected')
    rejected = 0
    for bad in ([star[0]] + star[:-1], [star[0] ^ 1 << U] + star[1:]):
        try:
            packing(bad)
        except ValueError:
            rejected += 1
    require(rejected == 2, 'malformed star accepted')
    return {'brute_force_simple_graphs': count, 'zero_cap_rejected_as_incomplete': aborted,
            'positive_affine_cover': True, 'malformed_stars_rejected': rejected}


def replay():
    star = first_star()
    maps = first_group(star)
    carrier, forced, forbidden, leaf_nodes = degree_leaves(star)
    fixed = [w for w in star if w & 1 << A]
    base = set(combinations(W, 2)) - forbidden
    require(len(base) == 114, 'residual base')
    raw_columns = tuple(sorted(decode(q) for q in fixed_weight(W, 4)
                        if all(((q | 1 << A) ^ w).bit_count() >= 6 for w in star)))
    require(len(raw_columns) == 597, 'initial primary columns')
    secondary_masks = tuple(fixed_weight(H, 4))
    remaining = set(carrier)
    cases = []
    entries = []
    while remaining:
        representative = min(remaining)
        leave = set(pair_edges(representative))
        orbit = {pair_mask(tuple(sorted((g[x], g[y]))) for x, y in leave) for g in maps}
        require(orbit <= remaining, 'degree-generated orbit overlap/domain')
        remaining -= orbit
        rows = tuple(sorted(base - leave))
        columns = tuple(q for q in raw_columns if set(combinations(q, 2)) <= set(rows))
        require(len(rows) == 108, 'replay residual pairs')
        covers, nodes = sparse_covers(rows, columns)
        details = []
        c, d = carrier[representative][1:]
        for cover in covers:
            second = fixed + [sum(1 << x for x in q) | 1 << A for q in cover]
            union = sorted(set(star + second))
            packing(union)
            require(len(second) == 20 and len(union) == 38, 'replay primary union')
            pairs = Counter(p for w in second for p in combinations(decode(w), 2))
            deficits = [(x, 5 - pairs[tuple(sorted((A, x)))]) for x in range(18)
                        if x != A and pairs[tuple(sorted((A, x)))] < 5]
            require(sorted(deficits) == sorted(((U, 3), (c, 1), (d, 1))), 'replay primary row')
            bfixed = sum(bool(w & 1 << B) for w in union)
            bcols = tuple(sorted(decode(q) for q in secondary_masks
                          if all(((q | 1 << B) ^ w).bit_count() >= 6 for w in union)))
            neighbors = {x: 0 for x in H}
            for q in bcols:
                mask = sum(1 << x for x in q)
                for x in q:
                    neighbors[x] |= mask ^ 1 << x
            degrees = [neighbors[x].bit_count() for x in H]
            caps = [d // 3 for d in degrees]
            bound = sum(caps) // 4
            require(bfixed + bound <= 19, 'replay secondary capacity')
            details.append({'primary_extra_quads': [list(q) for q in cover],
                            'secondary_fixed_words': bfixed, 'secondary_needed_for_twenty': 20 - bfixed,
                            'secondary_candidates': len(bcols),
                            'secondary_candidates_sha256': sha256(encoded(bcols)).hexdigest(),
                            'pair_union_edges': sum(degrees) // 2, 'pair_union_degrees': degrees,
                            'point_capacities': caps, 'upper_bound': bound})
            entries.append((representative, cover, bcols))
        cases.append({'index': len(cases), 'representative': representative, 'kind': carrier[representative][0],
                      'high_centers': list(carrier[representative][1:]), 'orbit_size': len(orbit),
                      'rows': rows, 'columns': columns, 'sparse_cover_nodes': nodes,
                      'compatible_primary_stars': details})
    require(len(cases) == 117 and sum(c['orbit_size'] for c in cases) == 3390, 'replay full orbit coverage')
    report = {'status': 'COMPLETE', 'degree_sequence_cases': 120, 'degree_sequence_nodes': leaf_nodes,
              'raw_leaves': len(carrier), 'raw_leave_types': dict(Counter(k for k, _, _ in carrier.values())),
              'first_star_symmetries': len(maps), 'leave_orbits': len(cases),
              'sparse_cover_nodes': sum(c['sparse_cover_nodes'] for c in cases),
              'compatible_primary_stars': len(entries),
              'secondary_extra_upper_bound': max(d['upper_bound'] for c in cases for d in c['compatible_primary_stars']),
              'secondary_total_upper_bound': max(d['secondary_fixed_words'] + d['upper_bound']
                                                for c in cases for d in c['compatible_primary_stars']),
              'all_secondary_saturation_excluded': True, 'global_72_word_exclusion': False,
              'independent_peer_review': False,
              'cases': [{'index': c['index'], 'representative': c['representative'],
                         'sparse_cover_nodes': c['sparse_cover_nodes'],
                         'compatible_primary_stars': len(c['compatible_primary_stars']),
                         'compatible_primary_stars_sha256': sha256(encoded(c['compatible_primary_stars'])).hexdigest()}
                        for c in cases], 'controls': controls()}
    return report, entries, cases, star, carrier, maps


def compare_primary(entries, cases, star, carrier, maps):
    import check_single_isolate as primary
    report, other_entries, other_cases, other_star = primary.data()
    require(entries == other_entries, 'actual primary covers or secondary candidates differ')
    require(set(star) == {sum(1 << x for x in w) for w in other_star}, 'actual first-star words differ')
    require(carrier == primary.raw_leaves() and maps == primary.group(other_star), 'actual carrier/group differ')
    require(len(cases) == len(other_cases), 'case count differs')
    for actual, other in zip(cases, other_cases):
        require(all(actual[k] == (list(other[k]) if k == 'high_centers' else other[k])
                    for k in ('index', 'representative', 'kind', 'high_centers', 'orbit_size', 'rows', 'columns')),
                'actual initial case/row/column differs')
    for actual, other in zip(cases, report['cases']):
        require(actual['compatible_primary_stars'] == other['compatible_primary_stars'], 'all capacity entries differ')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected', action='store_true')
    parser.add_argument('--compare-primary', action='store_true')
    args = parser.parse_args()
    report, entries, cases, star, carrier, maps = replay()
    expected = json.loads((HERE / 'single_isolate_expected.json').read_text())
    require(len(cases) == len(expected['cases']), 'manifest case coverage')
    for actual, other in zip(cases, expected['cases']):
        require(all(actual[k] == other[k] for k in ('index', 'representative', 'kind', 'high_centers', 'orbit_size',
                                                  'compatible_primary_stars')), 'manifest full case entries')
        require(len(actual['rows']) == other['rows'] and len(actual['columns']) == other['columns']
                and sha256(encoded(actual['rows'])).hexdigest() == other['rows_sha256']
                and sha256(encoded(actual['columns'])).hexdigest() == other['columns_sha256'], 'manifest rows/columns')
    if args.compare_primary:
        compare_primary(entries, cases, star, carrier, maps)
    path = HERE / 'single_isolate_replay_expected.json'
    if args.write_expected:
        path.write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    else:
        require(json.loads(path.read_text()) == report, 'replay manifest differs')
    print(json.dumps({k: v for k, v in report.items() if k != 'cases'}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
