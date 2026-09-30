"""Exact six-outsider frontier replay; CPython 3.11+, standard library only.
Author: six-code-2, researcher. Failed resource guards mean INCOMPLETE.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
from math import comb
import argparse
import json
import resource
import time
from geometry import classical_design, generators, mask, move, points, require
from generate_two_gap import digest, enumerate_masks
from generate_three_gap import graph, find_clique


def normalization(circles):
    start = time.monotonic()
    positions = {c: i for i, c in enumerate(circles)}
    global_gens, gap_gens = generators()
    gens = global_gens + (gap_gens[-1],)
    permutations = [tuple(positions[move(c, p)] for c in circles) for p in gens]
    require(all(sorted(p) == list(range(68)) for p in permutations), 'not a circle permutation')
    unseen = set(combinations(range(68), 4))
    total = len(unseen)
    require(total == comb(68, 4), 'incorrect four-gap universe')
    cases = []
    while unseen:
        require(time.monotonic() - start < 45, 'INCOMPLETE: four-gap orbit guard')
        representative = min(unseen)
        orbit, seen = [representative], {representative}
        for quad in orbit:
            if len(seen) % 2048 == 0:
                require(time.monotonic() - start < 45, 'INCOMPLETE: orbit guard')
            for p in permutations:
                image = tuple(sorted(p[i] for i in quad))
                if image not in seen:
                    seen.add(image)
                    orbit.append(image)
        require(seen <= unseen, 'overlapping four-gap orbits')
        unseen.difference_update(seen)
        gaps = tuple(circles[i] for i in representative)
        cases.append({'case': len(cases), 'gaps': gaps, 'circle_indices': representative,
                      'orbit_size': len(seen),
                      'pair_intersections': sorted((a & b).bit_count() for a, b in combinations(gaps, 2)),
                      'triple_intersections': sorted((a & b & c).bit_count() for a, b, c in combinations(gaps, 3)),
                      'common_points': (gaps[0] & gaps[1] & gaps[2] & gaps[3]).bit_count()})
    require(sum(c['orbit_size'] for c in cases) == total, 'incomplete four-gap coverage')
    return {'unordered_gap_quads': total, 'orbit_count': len(cases), 'cases': cases,
            'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def expand(circles, records, indices, gaps):
    outsiders = {records[i][0] for i in indices}
    qs = {q for i in indices for q in records[i][1]}
    removed = set(gaps) | {c for c in circles if any((c & b).bit_count() > 2 for b in outsiders)}
    words = sorted((set(circles) - removed) | outsiders | {q | (1 << 17) for q in qs})
    sets = [frozenset(p for p in range(18) if w >> p & 1) for w in words]
    require(len(words) == len(set(words)) == 64 + len(indices), 'incorrect expansion size')
    require(all(len(w) == 5 for w in sets), 'incorrect expansion weights')
    require(all(len(a & b) <= 2 for a, b in combinations(sets, 2)), 'invalid expansion packing')
    require(len(removed) - len(qs) == 4, 'incorrect gap count')
    return {'indices': indices, 'outsiders': sorted(outsiders), 'old_parts': sorted(qs),
            'words': words, 'size': len(words), 's': len(indices), 't': 0,
            'a': len(qs), 'R': len(removed), 'g': 4,
            'degree_histogram': dict(sorted(Counter(sum(p in w for w in sets)
                                                  for p in range(18)).items()))}


def run_case(circles, case, only_six=False):
    start = time.monotonic()
    records, census = enumerate_masks(circles, case['gaps'])
    adjacency, summary = graph(records)
    searches, witness = [], None
    for target in ((6,) if only_six else (6, 5, 4, 3)):
        indices, search = find_clique(adjacency, target)
        search.pop('root_coloring', None)
        searches.append(search)
        if indices is not None:
            witness = expand(circles, records, indices, case['gaps'])
            break
    require(only_six or witness is not None, 'no attaining clique found')
    return {'case': case['case'], 'gaps': case['gaps'], 'orbit_size': case['orbit_size'],
            'enumeration': census,
            'graph': {k: summary[k] for k in ('vertices', 'old_parts', 'edges', 'triangles', 'graph_sha256')},
            'searches': searches, 'witness': witness, 'complete': True,
            'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('four_gap_expected.json'))
    parser.add_argument('--case', type=int)
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text())
    circles, _ = classical_design()
    norm = normalization(circles)
    structural = {k: v for k, v in norm.items() if k not in ('seconds', 'max_RSS_KiB')}
    require(json.loads(json.dumps(structural)) == expected['four_normalization'], 'four-gap normalization mismatch')
    chosen = norm['cases'] if args.case is None else [norm['cases'][args.case]]
    for case in chosen:
        result = run_case(circles, case, only_six=True)
        require(result['witness'] is None and result['searches'][0]['complete'], 'six-clique found or incomplete')
        entry = expected['four_cases'][case['case']]
        require({k: result['enumeration'][k] for k in entry['enumeration']} == entry['enumeration'] and result['graph'] == entry['graph'], 'four-gap manifest mismatch')
        print(json.dumps({'case': case['case'], 'records': result['graph']['vertices'], 'six_cliques': 0, 'seconds': result['seconds']}), flush=True)
    print(json.dumps({'complete_cases': len(chosen), 'total_cases': 92, 'all_cases_complete': args.case is None}), flush=True)

if __name__ == '__main__':
    main()
