"""Separate full normalization, set enumeration, and direct K4 exclusion.

The default checker imports no production generator or record corpus.
Shared geometry and the earlier separate set enumerator are the only
mathematical code dependencies. Every graph and record is regenerated.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from geometry import classical_design, generators, mask, move, points, require
from verify_two_gap import enumerate_sets


def normalization(circles, cases):
    start = time.monotonic()
    global_gens, gap_gens = generators()
    gens = global_gens + (gap_gens[-1],)
    group = [tuple(range(17))]
    seen = set(group)
    for p in group:
        require(time.monotonic() - start < 45, 'INCOMPLETE: group time guard')
        for g in gens:
            q = tuple(g[p[i]] for i in range(17))
            if q not in seen:
                seen.add(q)
                group.append(q)
    require(len(group) == 16320, 'unexpected full generated group order')
    universe = set(combinations(circles, 3))
    seen_triples = set()
    summaries = []
    for case in cases:
        blocks = [points(c) for c in case['gap_circles']]
        orbit = {tuple(sorted(mask(p[i] for i in c) for c in blocks)) for p in group}
        require(len(orbit) == case['orbit_size'], 'orbit size mismatch')
        require(orbit <= universe and not orbit & seen_triples, 'invalid or overlapping orbits')
        seen_triples.update(orbit)
        summaries.append({'case': case['case'], 'orbit_size': len(orbit)})
    require(seen_triples == universe, 'incomplete three-gap normalization')
    return {'group_order': len(group), 'unordered_gap_triples': len(universe),
            'cases': summaries, 'seconds': time.monotonic() - start}


def pair_graph(records):
    start = time.monotonic()
    n = len(records)
    require(n <= 40000, 'INCOMPLETE: graph memory guard')
    old_triples = {}
    replacement_pairs = {}
    identical = {}
    for i, (b, qs) in enumerate(records):
        bit = 1 << i
        for triple in combinations(points(b), 3):
            old_triples[triple] = old_triples.get(triple, 0) | bit
        for q in qs:
            identical[q] = identical.get(q, 0) | bit
            for pair in combinations(points(q), 2):
                replacement_pairs[pair] = replacement_pairs.get(pair, 0) | bit
    conflicts = {}
    for q, owners in identical.items():
        bad = 0
        for pair in combinations(points(q), 2):
            bad |= replacement_pairs[pair]
        conflicts[q] = bad & ~owners
    universe = (1 << n) - 1
    adjacency = []
    graph_digest = sha256()
    width = (n + 7) // 8
    for i, (b, qs) in enumerate(records):
        require(time.monotonic() - start < 45, 'INCOMPLETE: graph time guard')
        bad = 0
        for triple in combinations(points(b), 3):
            bad |= old_triples[triple]
        for q in qs:
            bad |= conflicts[q]
        row = universe & ~bad
        require(not row >> i & 1, 'self-loop')
        adjacency.append(row)
        graph_digest.update(row.to_bytes(width, 'little'))
    return adjacency, graph_digest.hexdigest()


def no_four_clique(adjacency):
    start = time.monotonic()
    edges = 0
    triangles = 0
    for i, row in enumerate(adjacency):
        require(time.monotonic() - start < 45, 'INCOMPLETE: triangle time guard')
        later = row & ~((1 << (i + 1)) - 1)
        while later:
            bit = later & -later
            j = bit.bit_length() - 1
            require(adjacency[j] >> i & 1, 'asymmetric edge')
            edges += 1
            common = row & adjacency[j] & ~((1 << (j + 1)) - 1)
            while common:
                kbit = common & -common
                k = kbit.bit_length() - 1
                require(adjacency[k] >> i & 1 and adjacency[k] >> j & 1, 'asymmetric triangle')
                # Every increasing i,j,k,l clique has its k in common and
                # its l in this later-neighbor intersection.
                require(not common & adjacency[k] & ~((1 << (k + 1)) - 1),
                        'four-clique found')
                triangles += 1
                common ^= kbit
            later ^= bit
    require(edges * 2 == sum(row.bit_count() for row in adjacency), 'incomplete edge census')
    return {'vertices': len(adjacency), 'edges': edges, 'triangles': triangles,
            'four_cliques': 0, 'seconds': time.monotonic() - start}


def check_colors(adjacency, certificate):
    colors = certificate['colors']
    n = len(adjacency)
    require(certificate['target_clique'] == 5 and len(colors) == 4,
            'incorrect four-color certificate scope')
    flattened = [i for color in colors for i in color]
    require(all(type(i) is int and 0 <= i < n for i in flattened),
            'invalid color vertex')
    require(sorted(flattened) == list(range(n)),
            'colors do not partition the full record universe')
    for color in colors:
        members = sum(1 << i for i in color)
        require(all(not adjacency[i] & members for i in color),
                'edge inside a purported independent color')
    return [len(color) for color in colors]


def normalize_word(circles, fixed):
    start = time.monotonic()
    contained = {mask(q) for c in circles for q in combinations(points(c), 4)}
    noncontained = {mask(q) for q in combinations(range(17), 4)} - contained
    require(len(noncontained) == 2040 and fixed in noncontained,
            'incorrect noncontained four-set universe')
    global_gens, gap_gens = generators()
    gens = global_gens + (gap_gens[-1],)
    orbit = [fixed]
    seen = {fixed}
    for q in orbit:
        require(time.monotonic() - start < 45, 'INCOMPLETE: word normalization guard')
        for p in gens:
            image = move(q, p)
            if image not in seen:
                seen.add(image)
                orbit.append(image)
    require(seen == noncontained, 'incomplete fixed-word normalization')
    return len(seen)


def census_graph(adjacency):
    start = time.monotonic()
    edges = triangles = 0
    for i, row in enumerate(adjacency):
        require(time.monotonic() - start < 45, 'INCOMPLETE: graph census time guard')
        require(not row >> i & 1, 'self-loop')
        later = row & ~((1 << (i + 1)) - 1)
        while later:
            bit = later & -later
            j = bit.bit_length() - 1
            require(adjacency[j] >> i & 1, 'asymmetric graph')
            edges += 1
            triangles += (row & adjacency[j] & ~((1 << (j + 1)) - 1)).bit_count()
            later ^= bit
    require(2 * edges == sum(row.bit_count() for row in adjacency),
            'incomplete edge census')
    return edges, triangles


def verify_witness(circles, records, fixed, gaps, fixture):
    """Direct 18-point set checks and an exact expansion of a four-clique."""
    words = fixture['words']
    require(len(words) == len(set(words)) == 69,
            'witness has incorrect size or duplicate words')
    require(all(type(w) is int and 0 <= w < 1 << 18 and w.bit_count() == 5
                for w in words), 'witness weight or point universe is invalid')
    sets = [frozenset(p for p in range(18) if w >> p & 1) for w in words]
    require(all(len(u & v) <= 2 for u, v in combinations(sets, 2)),
            'witness is not a packing')
    indices = fixture['indices']
    require(len(indices) == len(set(indices)) == 4
            and all(type(i) is int and 0 <= i < len(records) for i in indices),
            'invalid witness record indices')
    outsiders = {records[i][0] for i in indices}
    qs = {q for i in indices for q in records[i][1]}
    removed = set(gaps) | {c for c in circles
                           if any(len(set(points(c)) & set(points(b))) > 2 for b in outsiders)}
    expanded = sorted((set(circles) - removed) | outsiders
                      | {q | (1 << 17) for q in qs} | {fixed | (1 << 17)})
    require(expanded == words and sorted(outsiders) == fixture['outsiders']
            and sorted(qs) == fixture['old_parts'], 'witness expansion mismatch')
    old = {w for w in words if not w >> 17 & 1}
    new_qs = {w ^ (1 << 17) for w in words if w >> 17 & 1}
    contained = {q for q in new_qs if any(q & c == q for c in circles)}
    s = len(old - set(circles))
    a = len(contained)
    t = len(new_qs - contained)
    r = len(set(circles) - old)
    require((s, a, t, r, r - a) == (4, 16, 1, 20, 4),
            'incorrect witness branch parameters')
    histogram = {str(k): v for k, v in sorted(Counter(
        sum(p in w for w in sets) for p in range(18)).items())}
    require(histogram == fixture['degree_histogram'], 'witness degree census mismatch')
    return {'words': len(words), 's': s, 'a': a, 't': t, 'R': r, 'g': r - a,
            'degree_histogram': histogram}


def verify_single(circles, expected, folder):
    census = expected['enumeration']
    fixed = census['fixed_old_four_set']
    require(fixed == 15, 'incorrect normalized fixed word')
    orbit_size = normalize_word(circles, fixed)
    gaps = {c for c in circles if (c & fixed).bit_count() >= 3}
    require(len(gaps) == 4 and sorted(gaps) == census['gaps'], 'incorrect fixed-word gaps')
    # Unlike the production CSP, enumerate all four-gap records first.
    all_records, _ = enumerate_sets(circles, gaps, 45)
    fixed_set = frozenset(points(fixed))
    records = [(b, qs) for b, qs in all_records
               if len(frozenset(points(b)) & fixed_set) <= 2
               and all(len(frozenset(points(q)) & fixed_set) <= 1 for q in qs)]
    raw = (json.dumps(records, separators=(',', ':')) + '\n').encode()
    require(len(records) == census['records'] and sha256(raw).hexdigest() == census['records_sha256'],
            'postfiltered full record universe mismatch')
    adjacency, graph_hash = pair_graph(records)
    graph = expected['graph']
    edges, triangles = census_graph(adjacency)
    old_parts = len({q for _, qs in records for q in qs})
    require((len(records), old_parts, edges, triangles, graph_hash)
            == tuple(graph[k] for k in ('vertices', 'old_parts', 'edges', 'triangles', 'graph_sha256')),
            'fixed-word independent graph mismatch')
    cert_raw = (folder / 'single_word_colors.json').read_bytes()
    require(len(cert_raw) == expected['certificate_bytes']
            and sha256(cert_raw).hexdigest() == expected['certificate_sha256'],
            'color certificate provenance mismatch')
    certificate = json.loads(cert_raw)
    require(certificate['records_sha256'] == sha256(raw).hexdigest()
            and certificate['graph_sha256'] == graph_hash, 'certificate universe mismatch')
    sizes = check_colors(adjacency, certificate)
    require(sizes == expected['color_sizes'] and expected['colors'] == 4,
            'color census mismatch')
    witness = verify_witness(circles, records, fixed, gaps,
                             json.loads((folder / 'single_word_witness69.json').read_text()))
    return {'noncontained_orbit': orbit_size, 'all_four_gap_records': len(all_records),
            'postfiltered_records': len(records), 'edges': edges, 'triangles': triangles,
            'color_sizes': sizes, 'witness': witness}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path,
                        default=Path(__file__).with_name('three_gap_expected.json'))
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text())['generator']
    circles, _ = classical_design()
    raw_design = (json.dumps(circles, separators=(',', ':')) + '\n').encode()
    require(len(circles) == expected['design_blocks']
            and sha256(raw_design).hexdigest() == expected['design_sha256'], 'design manifest mismatch')
    norm = normalization(circles, expected['cases'])
    require(len(expected['cases']) == expected['normalization']['orbits'] == 13
            and norm['unordered_gap_triples'] == expected['normalization']['unordered_gap_triples'],
            'incomplete normalized case count')
    results = []
    for case in expected['cases']:
        records, census = enumerate_sets(circles, case['gap_circles'], 45)
        raw = (json.dumps(records, separators=(',', ':')) + '\n').encode()
        enumeration = {'records': len(records), 'records_sha256': sha256(raw).hexdigest(),
                       'eligible_outsiders': {str(k): v for k, v in
                           census['eligible_outsiders_by_blocker_count'].items()},
                       'solution_counts': census['solution_counts']}
        require(enumeration == case['enumeration'], 'independent record manifest mismatch')
        adjacency, graph_hash = pair_graph(records)
        graph = no_four_clique(adjacency)
        compact = {k: graph[k] for k in ('vertices', 'edges', 'triangles', 'four_cliques')}
        compact.update({'old_parts': len({q for _, qs in records for q in qs}),
                        'graph_sha256': graph_hash})
        require(compact == case['graph'], 'independent graph manifest mismatch')
        results.append({'case': case['case'], 'records': len(records), 'edges': graph['edges'],
                        'triangles': graph['triangles'], 'four_cliques': 0})
    single = verify_single(circles, expected['single_word'], args.expected.parent)
    print(json.dumps({'cases': results, 'normalization': {k: norm[k] for k in
                         ('group_order', 'unordered_gap_triples', 'cases')},
                      'single_word': single, 's_at_least_4_implies_gap_at_least_4': True,
                      'at_most_five_outsiders_maximum': 69, 'minimum_outsiders_for_70': 6},
                     sort_keys=True))


if __name__ == '__main__':
    main()
