"""Exact necessary five-gap projection, six-code-2, researcher.

An outsider edge means SOME compatible pair of records exists. Every
actual packing injects into a projected clique; a projected clique need
not give a packing. Guard failure is INCOMPLETE, never an exclusion.
CPython3.11+, standard library only; one CPU process at a time.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, groupby
from pathlib import Path
import argparse
import json
import resource
import time
from geometry import classical_design, mask, points, require
from generate_two_gap import enumerate_masks
from generate_three_gap import find_clique
from verify_four_gap import close_group


def atomic_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)


def load_expected(path):
    expected = json.loads(path.read_text())
    require(expected.get('schema_version') == 1, 'unsupported manifest schema')
    cases = expected['cases']
    require(len(cases) == expected['normalization']['orbits'] == 789,
            'incomplete expected case list')
    require([c['case'] for c in cases] == list(range(789)), 'invalid case numbering')
    require(len({tuple(c['gaps']) for c in cases}) == 789, 'repeated gap representatives')
    require(all(c['K6_excluded'] is True for c in cases), 'expected K6 result incomplete')
    return expected


def project(records):
    start = time.monotonic()
    n = len(records)
    require(n <= 40000, 'INCOMPLETE: projection record guard')
    words, group_masks, owners, old_rows, q_records = [], [], [None] * n, {}, {}
    offset = 0
    for b, entries in groupby(records, key=lambda r: r[0]):
        entries = list(entries)
        end = offset + len(entries)
        g = len(words)
        group_mask = ((1 << len(entries)) - 1) << offset
        words.append(b)
        group_masks.append(group_mask)
        for i in range(offset, end):
            owners[i] = g
            bit = 1 << i
            for q in records[i][1]:
                q_records[q] = q_records.get(q, 0) | bit
        for triple in combinations(points(b), 3):
            t = mask(triple)
            old_rows[t] = old_rows.get(t, 0) | group_mask
        offset = end
        require(time.monotonic() - start < 45, 'INCOMPLETE: projection incidence guard')
    require(offset == n and len(words) == len(set(words)), 'projection partition invalid')
    incidence_seconds = time.monotonic() - start
    q_bad = {}
    for q in q_records:
        bad = 0
        for r, vertices in q_records.items():
            if r != q and (q & r).bit_count() > 1:
                bad |= vertices
        q_bad[q] = bad
    universe = (1 << n) - 1
    projected = []
    for b, entries in groupby(records, key=lambda r: r[0]):
        require(time.monotonic() - start < 45, 'INCOMPLETE: projection row guard')
        old_bad = 0
        for triple in combinations(points(b), 3):
            old_bad |= old_rows[mask(triple)]
        all_replacement_bad = universe
        for _, qs in entries:
            bad = 0
            for q in qs:
                bad |= q_bad[q]
            all_replacement_bad &= bad
        allowed = universe & ~(old_bad | all_replacement_bad)
        row = 0
        while allowed:
            first = (allowed & -allowed).bit_length() - 1
            h = owners[first]
            row |= 1 << h
            allowed &= ~group_masks[h]
        projected.append(row)
    digest = sha256()
    width = (len(words) + 7) // 8
    edges = 0
    for i, row in enumerate(projected):
        require(time.monotonic() - start < 45, 'INCOMPLETE: projection validation guard')
        require(not row >> i & 1, 'projected self-loop')
        digest.update(row.to_bytes(width, 'little'))
        later = row & ~((1 << (i + 1)) - 1)
        while later:
            bit = later & -later
            j = bit.bit_length() - 1
            require(projected[j] >> i & 1, 'projected graph asymmetric')
            edges += 1
            later ^= bit
    require(2 * edges == sum(row.bit_count() for row in projected), 'projection edge census incomplete')
    return projected, words, {'vertices': len(words), 'edges': edges,
        'graph_sha256': digest.hexdigest(),
        'degree_histogram': dict(sorted(Counter(row.bit_count() for row in projected).items())),
        'incidence_seconds': incidence_seconds, 'seconds': time.monotonic() - start}


def normalization(circles):
    start = time.monotonic()
    group, permutations = close_group(circles)
    stabilizer = [p for p in permutations if p[0] == 0]
    require(len(stabilizer) == 240, 'incorrect circle stabilizer')
    to_first = [next(p for p in permutations if p[i] == 0) for i in range(68)]
    indices = {c: i for i, c in enumerate(circles)}
    four = json.loads((Path(__file__).with_name('four_gap_expected.json')).read_text())
    four_cases = four['four_normalization']['cases']
    representatives = {}
    augmentation_count = 0
    for case in four_cases:
        phase_start = time.monotonic()
        old = tuple(indices[c] for c in case['gaps'])
        for extra in sorted(set(range(68)) - set(old)):
            require(time.monotonic() - phase_start < 45, 'INCOMPLETE: augmentation phase guard')
            gaps = old + (extra,)
            canonical = None
            for chosen in gaps:
                normalized = tuple(to_first[chosen][i] for i in gaps)
                require(0 in normalized, 'incorrect distinguished-circle transport')
                for p in stabilizer:
                    image = tuple(sorted(p[i] for i in normalized))
                    if canonical is None or image < canonical:
                        canonical = image
            representatives.setdefault(canonical, gaps)
            augmentation_count += 1
    require(augmentation_count == 92 * 64, 'four-gap augmentation incomplete')
    cases = [{'case': i, 'circle_indices': list(rep), 'gaps': [circles[j] for j in rep]}
             for i, rep in enumerate(sorted(representatives))]
    return {'agent': 'six-code-2', 'role': 'researcher', 'scope': 'g5 projected K6 exclusion, arbitrary noncontained words',
            'status': 'augmentation normalization only; not an exclusion',
            'four_gap_source_commit': 'aa775990f13c916b2fb10da55c4ccfd1c1b6797d',
            'four_gap_orbits': 92, 'augmentations': augmentation_count,
            'group_order': len(group), 'circle_stabilizer_order': len(stabilizer),
            'orbits': len(cases), 'cases': cases,
            'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def run_case(circles, case):
    start = time.monotonic()
    records, enumeration = enumerate_masks(circles, case['gaps'])
    adjacency, words, projection = project(records)
    selected, search = find_clique(adjacency, 6)
    search.pop('root_coloring', None)
    require(enumeration['records'] == case['records']
            and enumeration['records_sha256'] == case['records_sha256'],
            'expected record stream mismatch')
    require(projection['vertices'] == case['outsider_vertices']
            and projection['edges'] == case['projected_edges']
            and projection['graph_sha256'] == case['projected_graph_sha256'],
            'expected projected graph mismatch')
    return {'agent': 'six-code-2', 'role': 'researcher',
            'case': case['case'], 'gaps': case['gaps'], 'complete': search['complete'],
            'K6_excluded': selected is None,
            'projected_six_clique': None if selected is None else [words[i] for i in selected],
            'enumeration': enumeration, 'projection': projection, 'search': search,
            'proof_mechanism': 'every actual outsider record clique injects into this graph',
            'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('five_gap_expected.json'))
    parser.add_argument('--case', type=int)
    parser.add_argument('--from-case', type=int, default=0)
    parser.add_argument('--to-case', type=int, default=789, help='exclusive upper index')
    parser.add_argument('--normalize', action='store_true', help='regenerate the four-gap augmentation')
    parser.add_argument('--normalization-only', action='store_true')
    parser.add_argument('--checkpoint-dir', type=Path, help='scratch output directory outside this repository')
    args = parser.parse_args()
    expected = load_expected(args.expected)
    require(0 <= args.from_case <= args.to_case <= 789, 'invalid case range')
    require(args.case is None or 0 <= args.case < 789, 'invalid case')
    circles, _ = classical_design()
    if args.normalize or args.normalization_only:
        norm = normalization(circles)
        require(norm['orbits'] == 789, 'regenerated orbit count mismatch')
        require([(c['case'], c['gaps'], c['circle_indices']) for c in norm['cases']]
                == [(c['case'], c['gaps'], c['circle_indices']) for c in expected['cases']],
                'regenerated representatives differ entry by entry')
        print(json.dumps({'normalization': {k: v for k, v in norm.items() if k != 'cases'}}), flush=True)
    if args.normalization_only:
        return 0
    cases = expected['cases'][args.from_case:args.to_case] if args.case is None else [expected['cases'][args.case]]
    results = []
    for case in cases:
        try:
            result = run_case(circles, case)
        except ValueError as error:
            if 'INCOMPLETE' not in str(error):
                raise
            result = {'agent': 'six-code-2', 'role': 'researcher', 'case': case['case'],
                      'gaps': case['gaps'], 'complete': False, 'K6_excluded': None, 'limit': str(error)}
        if args.checkpoint_dir is not None:
            atomic_json(args.checkpoint_dir / (str(case['case']) + '.json'), result)
        print(json.dumps({'case': case['case'], 'complete': result['complete'],
                          'K6_excluded': result['K6_excluded'], 'seconds': result.get('seconds'),
                          'limit': result.get('limit')}), flush=True)
        if not result['complete'] or not result['K6_excluded']:
            # A positive projected clique refutes the projection exclusion,
            # but does not certify an actual packing or a larger code.
            return 2
        results.append(result)
    print(json.dumps({'complete_cases': len(results),
                      'coverage': 'all789cases' if len(results) == 789 else 'partial',
                      'records': sum(r['enumeration']['records'] for r in results),
                      'seconds_sum': sum(r['seconds'] for r in results)}), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
