"""Separate complete five-gap replay, six-code-2, researcher.

Uses fixed-order set enumeration, replacement-pair incidence, a union of
allowed record rows, and increasing clique counts. Default imports no
production enumerator or projector. --compare regenerates and compares
EVERY record and graph row. Same-author checks are not peer review.
Guard failure or interrupted coverage is INCOMPLETE.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, groupby
from math import comb
from pathlib import Path
import argparse
import json
import resource
import time
from geometry import classical_design, points, require
from verify_fixed_word_gap import enumerate_sets, record_hash, clique_census, check_witness
from verify_four_gap import close_group


def atomic_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)


def source_fingerprint(expected_path):
    directory = Path(__file__).resolve().parent
    files = [(p.name, sha256(p.read_bytes()).hexdigest()) for p in sorted(directory.glob('*.py'))]
    files.append(('expected_input', sha256(expected_path.read_bytes()).hexdigest()))
    return sha256(json.dumps(files, separators=(',', ':')).encode()).hexdigest()


def verify_normalization(circles, expected):
    start = time.monotonic()
    group, permutations = close_group(circles)
    indices = {c: i for i, c in enumerate(circles)}
    require({p[0] for p in permutations} == set(range(68)), 'circle action not transitive')
    require(len(expected['cases']) == expected['normalization']['orbits'] == 789,
            'incorrect case count')
    require([c['case'] for c in expected['cases']] == list(range(789)),
            'case numbering invalid')
    covered, results = set(), []
    for case in expected['cases']:
        phase_start = time.monotonic()
        rep = tuple(indices[c] for c in case['gaps'])
        require(len(rep) == len(set(rep)) == 5 and list(rep) == case['circle_indices'],
                'incorrect gap representative')
        pointed_orbit = set()
        for p in permutations:
            require(time.monotonic() - phase_start < 45, 'INCOMPLETE: pointed orbit guard')
            images = tuple(p[i] for i in rep)
            if 0 in images:
                pointed_orbit.add(tuple(sorted(i for i in images if i != 0)))
        require(pointed_orbit and not pointed_orbit & covered,
                'empty or overlapping actual pointed orbits')
        require(all(len(q) == len(set(q)) == 4 and 1 <= min(q) <= max(q) < 68
                    for q in pointed_orbit), 'orbit leaves pointed universe')
        # Transitivity gives five memberships per orbit quintuple, evenly
        # distributed over68 circles. This orbit-size identity is checked
        # independently against the literal stabilizer below.
        require(len(pointed_orbit) * 68 % 5 == 0, 'noninteger full orbit size')
        full_size = len(pointed_orbit) * 68 // 5
        rep_set = set(rep)
        stabilizer = sum(all(p[i] in rep_set for i in rep) for p in permutations)
        require(stabilizer > 0 and len(group) % stabilizer == 0
                and len(group) // stabilizer == full_size, 'orbit-stabilizer count mismatch')
        require(full_size == case['full_orbit_size'], 'expected full orbit size mismatch')
        covered.update(pointed_orbit)
        results.append({'case': case['case'], 'pointed_orbit_size': len(pointed_orbit),
                        'full_orbit_size': full_size, 'stabilizer_order': stabilizer})
    require(len(covered) == comb(67, 4) == 766480, 'pointed-universe cardinality incomplete')
    # A cardinality check suffices after subset validity; literal membership
    # is additionally checked to expose indexing/normalization mistakes.
    phase_start = time.monotonic()
    for q in combinations(range(1, 68), 4):
        require(time.monotonic() - phase_start < 45, 'INCOMPLETE: pointed cover guard')
        require(q in covered, 'missing pointed gap quintuple')
    require(sum(c['full_orbit_size'] for c in results) == comb(68, 5) == 10424128,
            'full five-gap cover cardinality mismatch')
    return {'agent': 'six-code-2', 'role': 'researcher', 'complete': True,
            'scope': 'normalization only, not a completion exclusion',
            'group_order': len(group), 'five_gap_orbits': len(results),
            'pointed_quintuplets': len(covered), 'all_unordered_quintuplets': comb(68, 5),
            'cases': results, 'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def pair_projection(records):
    start = time.monotonic()
    n = len(records)
    require(n <= 40000, 'INCOMPLETE: separate projection record guard')
    words, group_masks, owners = [], [], [None] * n
    old_triples, identical = {}, {}
    offset = 0
    for b, group in groupby(records, key=lambda r: r[0]):
        group = list(group)
        end = offset + len(group)
        g = len(words)
        words.append(b)
        vertices = sum(1 << i for i in range(offset, end))
        group_masks.append(vertices)
        for triple in combinations(points(b), 3):
            old_triples[triple] = old_triples.get(triple, 0) | vertices
        for i in range(offset, end):
            owners[i] = g
            for q in records[i][1]:
                identical[q] = identical.get(q, 0) | (1 << i)
        offset = end
        require(time.monotonic() - start < 45, 'INCOMPLETE: separate incidence guard')
    require(offset == n and len(words) == len(set(words)), 'bad outsider partition')
    replacement_pairs = {}
    for q, vertices in identical.items():
        for pair in combinations(points(q), 2):
            replacement_pairs[pair] = replacement_pairs.get(pair, 0) | vertices
    conflicts = {}
    for q, owners_q in identical.items():
        bad = 0
        for pair in combinations(points(q), 2):
            bad |= replacement_pairs[pair]
        # A record containing q has no other replacement sharing a pair
        # with q, by the set enumerator's internal validity condition.
        # Such records are therefore exactly the allowed identical-q case.
        conflicts[q] = bad & ~owners_q
    universe = (1 << n) - 1
    group_rows = [0] * len(words)
    for i, (b, qs) in enumerate(records):
        require(time.monotonic() - start < 45, 'INCOMPLETE: separate allowed-row guard')
        bad = 0
        for triple in combinations(points(b), 3):
            bad |= old_triples[triple]
        for q in qs:
            bad |= conflicts[q]
        group_rows[owners[i]] |= universe & ~bad
    adjacency = []
    for g, allowed in enumerate(group_rows):
        require(not allowed & group_masks[g], 'same-outsider lifted edge')
        row = 0
        while allowed:
            first = (allowed & -allowed).bit_length() - 1
            h = owners[first]
            row |= 1 << h
            allowed &= ~group_masks[h]
        adjacency.append(row)
    checksum = sha256()
    width = (len(words) + 7) // 8
    for row in adjacency:
        checksum.update(row.to_bytes(width, 'little'))
    return adjacency, words, {'vertices': len(words),
        'graph_sha256': checksum.hexdigest(), 'seconds': time.monotonic() - start}


def verify_case(circles, case, expected, compare):
    start = time.monotonic()
    require(case['K6_excluded'] is True, 'primary case incomplete')
    records, enumeration = enumerate_sets(circles, case['gaps'], ())
    require(enumeration['records'] == case['records']
            and record_hash(records) == case['records_sha256'], 'complete record digest mismatch')
    adjacency, words, projection = pair_projection(records)
    require(projection['vertices'] == case['outsider_vertices']
            and projection['graph_sha256'] == case['projected_graph_sha256'],
            'projection universe or graph digest mismatch')
    if compare:
        from generate_two_gap import enumerate_masks
        from generate_five_gap_projection import project
        other, _ = enumerate_masks(circles, case['gaps'])
        require(records == other, 'record entrywise mismatch')
        other_adjacency, other_words, _ = project(other)
        require(words == other_words and adjacency == other_adjacency, 'projection entrywise mismatch')
        del other, other_adjacency
    census = clique_census(adjacency, 6)
    require(census['cliques_by_size']['2'] == case['projected_edges'], 'complete edge census mismatch')
    require(census['cliques_by_size']['6'] == 0, 'six-clique exclusion mismatch')
    attainment = None
    if case['case'] == expected['five_gap_attainment']['case']:
        attainment = check_witness(circles, records, case['gaps'],
                                    expected['five_gap_attainment']['witness'], ())
        require(attainment == {'size': 68, 's': 5, 't': 0, 'g': 5}, 'wrong sharp fixture parameters')
    return {'agent': 'six-code-2', 'role': 'researcher', 'case': case['case'], 'gaps': case['gaps'],
            'complete': True, 'K6_excluded': True, 'enumeration': enumeration,
            'projection': projection, 'census': census,
            'entrywise_comparison': compare, 'attainment': attainment,
            'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def reusable(result, case, fingerprint, compare):
    return (result.get('complete') and result.get('K6_excluded') is True
            and result.get('source_fingerprint') == fingerprint
            and result.get('case') == case['case'] and result.get('gaps') == case['gaps']
            and result.get('enumeration', {}).get('records') == case['records']
            and result.get('enumeration', {}).get('records_sha256') == case['records_sha256']
            and result.get('projection', {}).get('graph_sha256') == case['projected_graph_sha256']
            and result.get('projection', {}).get('vertices') == case['outsider_vertices']
            and result.get('census', {}).get('cliques_by_size', {}).get('2') == case['projected_edges']
            and result.get('census', {}).get('cliques_by_size', {}).get('6') == 0
            and (not compare or result.get('entrywise_comparison')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('five_gap_expected.json'))
    parser.add_argument('--case', type=int)
    parser.add_argument('--from-case', type=int, default=0)
    parser.add_argument('--to-case', type=int, default=789, help='exclusive upper index')
    parser.add_argument('--normalization-only', action='store_true')
    parser.add_argument('--compare', action='store_true')
    parser.add_argument('--checkpoint-dir', type=Path, help='scratch output directory outside this repository')
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text())
    require(expected.get('schema_version') == 1, 'unsupported expected schema')
    require(args.case is None or 0 <= args.case < 789, 'invalid case')
    require(0 <= args.from_case <= args.to_case <= 789, 'invalid verification range')
    require(not args.resume or args.checkpoint_dir is not None, '--resume requires --checkpoint-dir')
    circles, _ = classical_design()
    fingerprint = source_fingerprint(args.expected)
    normalization = verify_normalization(circles, expected)
    if args.checkpoint_dir is not None:
        atomic_json(args.checkpoint_dir / 'normalization.json',
                    dict(normalization, source_fingerprint=fingerprint))
    print(json.dumps({'normalization': {k: v for k, v in normalization.items() if k != 'cases'}}), flush=True)
    if args.normalization_only:
        return 0
    cases = expected['cases'][args.from_case:args.to_case] if args.case is None else [expected['cases'][args.case]]
    results = []
    resumed = 0
    for case in cases:
        path = None if args.checkpoint_dir is None else args.checkpoint_dir / (str(case['case']) + '.json')
        if args.resume and path.exists():
            old = json.loads(path.read_text())
            if reusable(old, case, fingerprint, args.compare):
                results.append(old)
                resumed += 1
                continue
        try:
            result = verify_case(circles, case, expected, args.compare)
        except ValueError as error:
            if 'INCOMPLETE' not in str(error):
                raise
            result = {'agent': 'six-code-2', 'role': 'researcher', 'case': case['case'],
                      'gaps': case['gaps'], 'complete': False, 'K6_excluded': None, 'limit': str(error)}
        result['source_fingerprint'] = fingerprint
        if path is not None:
            atomic_json(path, result)
        print(json.dumps({'case': case['case'], 'complete': result['complete'],
                          'K6_excluded': result['K6_excluded'],
                          'cliques_by_size': result.get('census', {}).get('cliques_by_size'),
                          'seconds': result.get('seconds'), 'limit': result.get('limit')}), flush=True)
        if not result['complete']:
            return 2
        results.append(result)
    require(len({r['case'] for r in results}) == len(results), 'repeated checked case')
    counts = {str(k): sum(r['census']['cliques_by_size'][str(k)] for r in results) for k in range(1, 7)}
    summary = {'agent': 'six-code-2', 'role': 'researcher', 'complete_cases': len(results),
               'coverage': 'all789cases' if len(results) == 789 else 'partial',
               'source_fingerprint': fingerprint, 'resumed_cases': resumed,
               'all_entrywise': all(r['entrywise_comparison'] for r in results),
               'total_records': sum(r['enumeration']['records'] for r in results),
               'projected_cliques_by_size': counts,
               'seconds_sum': sum(r['seconds'] for r in results),
               'slowest_case_seconds': max((r['seconds'] for r in results), default=0),
               'max_RSS_KiB': max([resource.getrusage(resource.RUSAGE_SELF).ru_maxrss]
                                  + [r['max_RSS_KiB'] for r in results]),
               'normalization_seconds': normalization['seconds'],
               'independent_peer_review': False}
    if args.checkpoint_dir is not None:
        atomic_json(args.checkpoint_dir / 'summary.json', summary)
    print(json.dumps(summary), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
