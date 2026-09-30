"""Separate set enumeration, pair-incidence graph, full triangle exclusion.

Imports neither production generator nor generated records. All three gap
cases are reconstructed. The geometric and cardinality bridges are written
in TWO_GAP_PROOF.md. A failed guard means incomplete computation.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from geometry import classical_design, generators, mask, move, points, require


def normalize(circles, gap):
    global_gens, gap_gens = generators()
    first_orbit = [gap]
    first_seen = {gap}
    for c in first_orbit:
        for p in global_gens:
            q = move(c, p)
            if q not in first_seen:
                first_seen.add(q)
                first_orbit.append(q)
    require(first_seen == set(circles), 'incomplete first-circle normalization')
    group = [tuple(range(17))]
    group_seen = set(group)
    for p in group:
        for g in gap_gens:
            q = tuple(g[p[x]] for x in range(17))
            if q not in group_seen:
                group_seen.add(q)
                group.append(q)
    require(len(group) == 240, 'unexpected first-circle stabilizer order')
    representatives = {0: 1828, 1: 5169, 2: 362}
    census = []
    union = set()
    for intersection, representative in representatives.items():
        orbit = [representative]
        seen = {representative}
        for c in orbit:
            for p in gap_gens:
                q = move(c, p)
                if q not in seen:
                    seen.add(q)
                    orbit.append(q)
        wanted = {c for c in circles if c != gap and (c & gap).bit_count() == intersection}
        require(seen == wanted, 'incomplete second-circle normalization')
        require(not union & seen, 'overlapping normalized cases')
        union.update(seen)
        census.append({'intersection': intersection, 'representative': representative,
                       'orbit_size': len(seen)})
    require(union == set(circles) - {gap}, 'second-circle cases do not cover all circles')
    return {'first_circle_orbit': len(first_seen), 'stabilizer_order': len(group),
            'second_circle_orbits': census}


def enumerate_sets(circles, gaps, seconds):
    start = time.monotonic()
    design = tuple(frozenset(points(c)) for c in circles)
    circle_set = set(design)
    gap_sets = {frozenset(points(c)) for c in gaps}
    records = []
    histogram = Counter()
    eligible = Counter()
    tested = 0
    nodes = 0
    for pts in combinations(range(17), 5):
        require(time.monotonic() - start < seconds, 'INCOMPLETE: generation time guard')
        b = frozenset(pts)
        if b in circle_set:
            continue
        tested += 1
        blockers = [c for c in design if c not in gap_sets and len(c & b) >= 3]
        if any(len(c & b) >= 4 for c in blockers):
            continue
        # Every four-subset of every mandatory circle is considered;
        # direct compatibility with b filters this to three alternatives.
        options = [tuple(frozenset(q) for q in combinations(sorted(c), 4)
                         if len(frozenset(q) & b) <= 2) for c in blockers]
        require(all(len(qs) == 3 for qs in options), 'invalid direct option count')
        paired_options = [[(q, frozenset(combinations(sorted(q), 2))) for q in qs]
                          for qs in options]
        selected = []
        before = len(records)

        def visit(i, owned_pairs):
            nonlocal nodes
            nodes += 1
            if nodes % 1024 == 0:
                require(time.monotonic() - start < seconds, 'INCOMPLETE: generation time guard')
            if i == len(paired_options):
                records.append((mask(b), tuple(sorted(mask(q) for q in selected))))
                return
            for q, pairs in paired_options[i]:
                if pairs.isdisjoint(owned_pairs):
                    selected.append(q)
                    visit(i + 1, owned_pairs | pairs)
                    selected.pop()

        visit(0, frozenset())
        eligible[len(blockers)] += 1
        histogram[(len(blockers), len(records) - before)] += 1
    records.sort()
    require(tested == 6120 and len(set(records)) == len(records),
            'incorrect old-set coverage or duplicate records')
    return records, {'records': len(records),
                     'eligible_outsiders_by_blocker_count': dict(sorted(eligible.items())),
                     'solution_counts': [{'mandatory_circles': k[0], 'assignments': k[1],
                                         'outsiders': v} for k, v in sorted(histogram.items())],
                     'nodes': nodes, 'seconds': time.monotonic() - start}


def triangle_check(records, seconds):
    start = time.monotonic()
    n = len(records)
    require(n <= 40000, 'graph requires a new memory profile')
    old_triples = {}
    replacement_pairs = {}
    identical_replacements = {}
    for i, (b, qs) in enumerate(records):
        bit = 1 << i
        for t in combinations(points(b), 3):
            old_triples[t] = old_triples.get(t, 0) | bit
        for q in qs:
            identical_replacements[q] = identical_replacements.get(q, 0) | bit
            for pair in combinations(points(q), 2):
                replacement_pairs[pair] = replacement_pairs.get(pair, 0) | bit
    # Pair ownership is independent of the production graph's explicit
    # intersections over all four-set pairs. A valid record containing q
    # cannot also contain a different four-set sharing a pair with q.
    replacement_conflicts = {}
    for q, identical in identical_replacements.items():
        bad = 0
        for pair in combinations(points(q), 2):
            bad |= replacement_pairs[pair]
        replacement_conflicts[q] = bad & ~identical
    universe = (1 << n) - 1
    adjacency = []
    for b, qs in records:
        bad = 0
        for t in combinations(points(b), 3):
            bad |= old_triples[t]
        for q in qs:
            bad |= replacement_conflicts[q]
        adjacency.append(universe & ~bad)
    digest = sha256()
    width = (n + 7) // 8
    directed = sum(row.bit_count() for row in adjacency)
    checked_edges = 0
    for i, row in enumerate(adjacency):
        require(time.monotonic() - start < seconds, 'INCOMPLETE: graph time guard')
        require(not row >> i & 1, 'graph self-loop')
        digest.update(row.to_bytes(width, 'little'))
        later = row & ~((1 << (i + 1)) - 1)
        while later:
            bit = later & -later
            j = bit.bit_length() - 1
            require(adjacency[j] >> i & 1, 'asymmetric adjacency')
            require(not row & adjacency[j], 'compatible triple found')
            checked_edges += 1
            later ^= bit
    require(checked_edges * 2 == directed, 'edge enumeration did not finish')
    return {'vertices': n, 'old_parts': len(identical_replacements), 'edges': checked_edges, 'triangles': 0,
            'graph_sha256': digest.hexdigest(),
            'degree_histogram': dict(sorted(Counter(row.bit_count() for row in adjacency).items())),
            'seconds': time.monotonic() - start}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path,
                        default=Path(__file__).with_name('two_gap_expected.json'))
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text())
    circles, gap = classical_design()
    normalization = normalize(circles, gap)
    require(normalization == expected['normalization'], 'normalization manifest mismatch')
    generator = expected['generator']
    canonical_design = (json.dumps(circles, separators=(',', ':')) + '\n').encode()
    require(generator['design_blocks'] == len(circles), 'incorrect design size')
    require(generator['design_sha256'] == sha256(canonical_design).hexdigest(),
            'incorrect design digest')
    require(generator['first_gap'] == gap, 'incorrect first-gap fixture')
    require(len(generator['cases']) == 3, 'incomplete case manifest')
    results = []
    for case, norm in zip(generator['cases'], normalization['second_circle_orbits']):
        require(case['gap_intersection'] == norm['intersection'], 'case normalization mismatch')
        gaps = sorted([gap, norm['representative']])
        require(case['gaps'] == gaps, 'incorrect normalized gaps')
        records, census = enumerate_sets(circles, gaps, 45)
        canonical = (json.dumps(records, separators=(',', ':')) + '\n').encode()
        enumeration = {'records': census['records'],
                       'records_sha256': sha256(canonical).hexdigest(),
                       'eligible_outsiders': {str(k): v for k, v in
                           census['eligible_outsiders_by_blocker_count'].items()},
                       'solution_counts': census['solution_counts']}
        require(enumeration == case['enumeration'], 'independent enumeration mismatch')
        graph = triangle_check(records, 45)
        verified = {k: graph[k] for k in ('vertices', 'old_parts', 'edges',
                                         'triangles', 'graph_sha256')}
        require(verified == case['graph'], 'independent graph manifest mismatch')
        results.append({'gap_intersection': norm['intersection'],
                        'records': len(records), 'edges': graph['edges'], 'triangles': 0})
    print(json.dumps({'cases': results, 'normalization': normalization,
                      's_at_least_3_implies_gap_at_least_3': True,
                      'at_most_four_outsiders_maximum': 69,
                      'minimum_outsiders_for_70': 5}, sort_keys=True))


if __name__ == '__main__':
    main()
