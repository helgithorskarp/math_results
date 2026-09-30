"""Separate set/pair-incidence replay with a complete increasing clique census.
Default imports no production enumerator/search/corpus. --compare additionally
checks the two full record lists entry by entry. Guard failure is INCOMPLETE.
Author: six-code-2, researcher. This is not independent peer review.
"""
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import json
import resource
import time
from geometry import classical_design, generators, mask, move, points, require
from verify_two_gap import enumerate_sets
from verify_three_gap import pair_graph


def close_group(circles):
    start = time.monotonic()
    global_gens, gap_gens = generators()
    gens = global_gens + (gap_gens[-1],)
    group = [tuple(range(17))]
    seen = set(group)
    for p in group:
        require(time.monotonic() - start < 45, 'INCOMPLETE: group closure guard')
        for g in gens:
            q = tuple(p[g[i]] for i in range(17))
            if q not in seen:
                seen.add(q)
                group.append(q)
    require(len(group) == 16320, 'wrong full group size')
    indices = {c: i for i, c in enumerate(circles)}
    circle_points = [points(c) for c in circles]
    permutations = []
    for p in group:
        require(time.monotonic() - start < 45, 'INCOMPLETE: circle group guard')
        images = tuple(mask(p[i] for i in pts) for pts in circle_points)
        require(set(images) == set(circles), 'group element does not preserve circles')
        permutations.append(tuple(indices[c] for c in images))
    require(len(set(permutations)) == len(group), 'group circle action not faithful')
    return group, permutations


def check_normalization(circles, group, circle_perms, four, single):
    start = time.monotonic()
    indices = {c: i for i, c in enumerate(circles)}
    seen = set()
    for case in four['cases']:
        require(time.monotonic() - start < 45, 'INCOMPLETE: four-gap orbit replay guard')
        rep = tuple(indices[c] for c in case['gaps'])
        require(len(rep) == len(set(rep)) == 4, 'invalid gap tuple')
        orbit = {tuple(sorted(p[i] for i in rep)) for p in circle_perms}
        require(len(orbit) == case['orbit_size'] and not orbit & seen,
                'incorrect or overlapping four-gap orbit')
        seen.update(orbit)
    require(len(seen) == comb(68, 4) == four['unordered_gap_quads'], 'four-gap cover incomplete')
    fixed = single['fixed_old_four_set']
    fixed_set = frozenset(points(fixed))
    design_sets = [frozenset(points(c)) for c in circles]
    contained = {frozenset(q) for c in design_sets for q in combinations(sorted(c), 4)}
    noncontained = set(map(frozenset, combinations(range(17), 4))) - contained
    word_orbit = {frozenset(p[i] for i in fixed_set) for p in group}
    require(word_orbit == noncontained and len(word_orbit) == 2040,
            'noncontained four-set orbit incomplete')
    stabilizer = [p for p in group if frozenset(p[i] for i in fixed_set) == fixed_set]
    require(len(stabilizer) == 8, 'wrong four-set stabilizer size')
    forced = {c for c, pts in zip(circles, design_sets) if len(pts & fixed_set) >= 3}
    require(len(forced) == 4 and sorted(forced) == single['forced_gaps'], 'forced gaps mismatch')
    extra_seen = set()
    for case in single['cases']:
        rep = frozenset(points(case['extra_gap']))
        orbit = {mask(p[i] for i in rep) for p in stabilizer}
        require(len(orbit) == case['orbit_size'] and not orbit & extra_seen,
                'wrong or overlapping extra-gap orbit')
        require(sorted(orbit) == case['extra_orbit'], 'entrywise extra-gap orbit mismatch')
        require(sorted(forced | {case['extra_gap']}) == case['gaps'], 'wrong five-gap set')
        extra_seen.update(orbit)
    require(extra_seen == set(circles) - forced, 'extra-gap cover incomplete')
    return {'group_order': len(group), 'four_gap_orbits': len(four['cases']),
            'unordered_gap_quads': len(seen), 'single_word_orbits': len(single['cases']),
            'extra_gap_circles': len(extra_seen), 'seconds': time.monotonic() - start}


def clique_census(adjacency):
    """Enumerate all increasing edges/triangles/K4/K5 and reject every K6."""
    start = time.monotonic()
    counts = [0, 0, 0, 0]
    for i, row in enumerate(adjacency):
        require(time.monotonic() - start < 45, 'INCOMPLETE: clique census time guard')
        require(not row >> i & 1, 'self-loop in graph')
        later = row & ~((1 << (i + 1)) - 1)
        while later:
            bit = later & -later
            j = bit.bit_length() - 1
            require(adjacency[j] >> i & 1, 'asymmetric graph edge')
            counts[0] += 1
            common = row & adjacency[j] & ~((1 << (j + 1)) - 1)
            while common:
                bit3 = common & -common
                k = bit3.bit_length() - 1
                counts[1] += 1
                tail = common & adjacency[k] & ~((1 << (k + 1)) - 1)
                while tail:
                    bit4 = tail & -tail
                    l = bit4.bit_length() - 1
                    counts[2] += 1
                    tail2 = tail & adjacency[l] & ~((1 << (l + 1)) - 1)
                    while tail2:
                        bit5 = tail2 & -tail2
                        m = bit5.bit_length() - 1
                        counts[3] += 1
                        require(not tail2 & adjacency[m] & ~((1 << (m + 1)) - 1),
                                'six-clique found')
                        tail2 ^= bit5
                    tail ^= bit4
                common ^= bit3
            later ^= bit
    require(2 * counts[0] == sum(row.bit_count() for row in adjacency), 'incomplete edge census')
    return {'edges': counts[0], 'triangles': counts[1], 'four_cliques': counts[2],
            'five_cliques': counts[3], 'six_cliques': 0,
            'seconds': time.monotonic() - start}


def record_hash(records):
    return sha256((json.dumps(records, separators=(',', ':')) + '\n').encode()).hexdigest()


def check_witness(circles, records, gaps, fixture, fixed=None):
    words = fixture['words']
    require(len(words) == len(set(words)) == fixture['size'], 'duplicate or missing witness words')
    require(all(type(w) is int and 0 <= w < (1 << 18) for w in words), 'word outside universe')
    sets = [frozenset(i for i in range(18) if w >> i & 1) for w in words]
    require(all(len(w) == 5 for w in sets), 'incorrect word weight')
    require(all(len(a & b) <= 2 for a, b in combinations(sets, 2)), 'invalid packing witness')
    require(all(type(i) is int and 0 <= i < len(records) for i in fixture['indices']), 'invalid record indices')
    outsiders = {records[i][0] for i in fixture['indices']}
    qs = {q for i in fixture['indices'] for q in records[i][1]}
    require(len(outsiders) == len(fixture['indices']) == fixture['s'], 'wrong outsider count')
    require(sorted(outsiders) == fixture['outsiders'] and sorted(qs) == fixture['old_parts'], 'wrong witness records')
    design = {frozenset(points(c)): c for c in circles}
    removed = set(gaps) | {c for pts, c in design.items()
                           if any(len(pts & frozenset(points(b))) >= 3 for b in outsiders)}
    expanded = (set(circles) - removed) | outsiders | {q | (1 << 17) for q in qs}
    if fixed is not None:
        expanded.add(fixed | (1 << 17))
    require(sorted(expanded) == words, 'witness expansion mismatch')
    a = len({w for w in words if w >> 17 & 1 and any((w & ((1 << 17) - 1)) & c
                                                          == (w & ((1 << 17) - 1)) for c in circles)})
    t = sum(w >> 17 & 1 for w in words) - a
    r = len(set(circles) - set(words))
    s = len({w for w in words if not w >> 17 & 1} - set(circles))
    require((s, a, t, r, r - a) == tuple(fixture[k] for k in ('s', 'a', 't', 'R', 'g')),
            'incorrect witness parameters')
    return {'size': len(words), 's': s, 't': t, 'g': r - a}


def replay_case(circles, case, production, fixed=None, compare=False):
    start = time.monotonic()
    records, census = enumerate_sets(circles, case['gaps'], 45)
    raw_records = len(records)
    if fixed is not None:
        fixed_set = frozenset(points(fixed))
        records = [(b, qs) for b, qs in records
                   if len(frozenset(points(b)) & fixed_set) <= 2
                   and all(len(frozenset(points(q)) & fixed_set) <= 1 for q in qs)]
    require(len(records) == production['enumeration']['records']
            and record_hash(records) == production['enumeration']['records_sha256'], 'record universe mismatch')
    if compare:
        if fixed is not None:
            from generate_five_gap_single import enumerate_fixed_extra
            mask_records, _ = enumerate_fixed_extra(circles, case['gaps'], fixed)
        else:
            from generate_two_gap import enumerate_masks
            mask_records, _ = enumerate_masks(circles, case['gaps'])
        require(records == mask_records, 'entrywise record mismatch')
        del mask_records
    adjacency, graph_hash = pair_graph(records)
    require(graph_hash == production['graph']['graph_sha256'], 'graph-row mismatch')
    counts = clique_census(adjacency)
    require((len(records), len({q for _, qs in records for q in qs}), counts['edges'], counts['triangles'])
            == tuple(production['graph'][k] for k in ('vertices', 'old_parts', 'edges', 'triangles')),
            'independent graph census mismatch')
    witness = None
    if production.get('witness'):
        witness = check_witness(circles, records, case['gaps'], production['witness'], fixed)
        claimed = production['witness']['s']
        if claimed == 4:
            require(counts['five_cliques'] == 0, 'claimed maximum four is incorrect')
    return {'case': case['case'], 'complete': True, 'raw_records': raw_records,
            'records': len(records), 'records_sha256': record_hash(records), 'graph_sha256': graph_hash,
            'cliques': counts, 'witness': witness, 'entrywise_comparison': compare,
            'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('four_gap_expected.json'))
    parser.add_argument('--case', type=int)
    parser.add_argument('--single', action='store_true')
    parser.add_argument('--normalize-only', action='store_true')
    parser.add_argument('--compare', action='store_true')
    parser.add_argument('--checkpoint-dir', type=Path)
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text())
    circles, _ = classical_design()
    require(len(expected['four_cases']) == 92 and len(expected['single_cases']) == 13, 'incorrect claim scope')
    require(all(c['checker']['five_cliques'] == 0 and c['checker']['triangles'] > 0 for c in expected['four_cases']), 'manifest lacks K5-free claims or attainment')
    require([c['case'] for c in expected['four_normalization']['cases']] == list(range(92)) and [c['case'] for c in expected['single_normalization']['cases']] == list(range(13)), 'invalid case indexing')
    require(len(circles) == expected['design_blocks'] and record_hash(circles) == expected['design_sha256'], 'design provenance mismatch')
    group, circle_perms = close_group(circles)
    normalization = check_normalization(circles, group, circle_perms, expected['four_normalization'], expected['single_normalization'])
    print(json.dumps({'normalization': normalization}), flush=True)
    del group, circle_perms
    if args.normalize_only:
        return
    entries = [('four', expected['four_normalization'], expected['four_cases'], None),
               ('single', expected['single_normalization'], expected['single_cases'], expected['single_normalization']['fixed_old_four_set'])]
    completed = 0
    for kind, norm, cases, fixed in entries:
        if args.case is not None and (kind == 'single') != args.single:
            continue
        selected = norm['cases'] if args.case is None else [norm['cases'][args.case]]
        for case in selected:
            entry = cases[case['case']]
            result = replay_case(circles, case, entry, fixed, args.compare)
            if 'checker' in entry:
                require({k: result['cliques'][k] for k in ('edges', 'triangles', 'four_cliques', 'five_cliques', 'six_cliques')} == entry['checker'], 'complete clique census mismatch')
            if args.checkpoint_dir:
                args.checkpoint_dir.mkdir(parents=True, exist_ok=True)
                path = args.checkpoint_dir / f"{kind}-{case['case']}.json"
                path.write_text(json.dumps(result, indent=2) + '\n')
            completed += 1
            print(json.dumps({'kind': kind, 'case': case['case'], 'records': result['records'], 'cliques': result['cliques'], 'seconds': result['seconds'], 'entrywise_comparison': args.compare}), flush=True)
    print(json.dumps({'complete_cases': completed, 'total_cases': 105, 'all_cases_complete': args.case is None}), flush=True)

if __name__ == '__main__':
    main()
