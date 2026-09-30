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


def normalization(circles, fixed=15):
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
    require(len(group) == 16320, 'unexpected design permutation group')
    orbit = {move(fixed, p) for p in group}
    contained = {mask(q) for c in circles for q in combinations(points(c), 4)}
    noncontained = {mask(q) for q in combinations(range(17), 4)} - contained
    require(orbit == noncontained and len(orbit) == 2040, 'fixed-word normalization incomplete')
    stabilizer = [p for p in group if move(fixed, p) == fixed]
    require(len(stabilizer) == 8, 'incorrect fixed-word stabilizer')
    forced = {c for c in circles if (c & fixed).bit_count() >= 3}
    require(len(forced) == 4, 'incorrect forced gaps')
    for p in stabilizer:
        require({move(c, p) for c in circles} == set(circles), 'not a design automorphism')
        require({move(c, p) for c in forced} == forced, 'forced gaps not preserved')
    unseen = set(circles) - forced
    cases = []
    while unseen:
        representative = min(unseen)
        extra_orbit = {move(representative, p) for p in stabilizer}
        require(extra_orbit <= unseen, 'extra-gap orbits overlap')
        cases.append({'case': len(cases), 'extra_gap': representative,
                      'orbit_size': len(extra_orbit), 'extra_orbit': sorted(extra_orbit),
                      'gaps': sorted(forced | {representative}),
                      'fixed_intersection': (representative & fixed).bit_count()})
        unseen.difference_update(extra_orbit)
    require(sum(c['orbit_size'] for c in cases) == 64, 'incomplete extra-gap cover')
    return {'group_order': len(group), 'fixed_old_four_set': fixed,
            'noncontained_orbit': len(orbit), 'stabilizer_order': len(stabilizer),
            'stabilizer_permutations': stabilizer, 'forced_gaps': sorted(forced),
            'extra_gap_circles': 64, 'cases': cases}


def enumerate_fixed_extra(circles, gaps, fixed=15):
    start = time.monotonic()
    circle_set, gaps = set(circles), set(gaps)
    require(len(gaps) == 5 and gaps <= circle_set, 'incorrect five-gap case')
    require({c for c in circles if (c & fixed).bit_count() >= 3} <= gaps, 'forced gaps missing')
    records = []
    reasons, eligible, assignments = Counter(), Counter(), Counter()
    nodes = 0
    for pts in combinations(range(17), 5):
        require(time.monotonic() - start < 45, 'INCOMPLETE: fixed-word enumeration guard')
        b = mask(pts)
        if b in circle_set:
            reasons['design_circle'] += 1
            continue
        if (b & fixed).bit_count() > 2:
            reasons['fixed_word_conflict'] += 1
            continue
        meetings = [(c, (b & c).bit_count()) for c in circles if c not in gaps]
        if any(n >= 4 for _, n in meetings):
            reasons['nongap_four_point_circle'] += 1
            continue
        blockers = [c for c, n in meetings if n == 3]
        options = [[c ^ (1 << p) for p in pts if c >> p & 1
                    and ((c ^ (1 << p)) & fixed).bit_count() <= 1]
                   for c in blockers]
        selected = []
        before = len(records)

        def visit(remaining):
            nonlocal nodes
            nodes += 1
            if nodes % 1024 == 0:
                require(time.monotonic() - start < 45, 'INCOMPLETE: enumeration time guard')
                require(len(records) <= 40000, 'INCOMPLETE: record count guard')
            if not remaining:
                records.append((b, tuple(sorted(selected))))
                return
            filtered = [[q for q in qs if all((q & r).bit_count() <= 1 for r in selected)]
                        for qs in remaining]
            i = min(range(len(filtered)), key=lambda j: len(filtered[j]))
            if not filtered[i]:
                return
            tail = filtered[:i] + filtered[i + 1:]
            for q in filtered[i]:
                selected.append(q)
                visit(tail)
                selected.pop()

        visit(options)
        eligible[len(blockers)] += 1
        assignments[(len(blockers), len(records) - before)] += 1
    records.sort()
    require(sum(reasons.values()) + sum(eligible.values()) == 6188, 'old-set universe incomplete')
    require(len(set(records)) == len(records), 'duplicate record')
    return records, {'records': len(records), 'records_sha256': digest(records),
                     'rejection_reasons': dict(sorted(reasons.items())),
                     'eligible_outsiders': {str(k): v for k, v in sorted(eligible.items())},
                     'solution_counts': [{'mandatory_circles': k[0], 'assignments': k[1], 'outsiders': v}
                                         for k, v in sorted(assignments.items())]}


def expand(circles, records, indices, gaps, fixed):
    outsiders = {records[i][0] for i in indices}
    qs = {q for i in indices for q in records[i][1]}
    removed = set(gaps) | {c for c in circles if any((c & b).bit_count() > 2 for b in outsiders)}
    words = sorted((set(circles) - removed) | outsiders
                   | {q | (1 << 17) for q in qs} | {fixed | (1 << 17)})
    sets = [frozenset(p for p in range(18) if w >> p & 1) for w in words]
    require(len(words) == len(set(words)) == 64 + len(indices), 'wrong expansion size')
    require(all(len(w) == 5 for w in sets), 'incorrect expansion weight')
    require(all(len(a & b) <= 2 for a, b in combinations(sets, 2)), 'invalid expansion')
    require(len(removed) - len(qs) == 5, 'wrong gap parameter')
    return {'indices': indices, 'outsiders': sorted(outsiders), 'old_parts': sorted(qs),
            'words': words, 'size': len(words), 's': len(indices), 't': 1,
            'a': len(qs), 'R': len(removed), 'g': 5,
            'degree_histogram': dict(sorted(Counter(sum(p in w for w in sets)
                                                  for p in range(18)).items()))}


def run_case(circles, case, fixed):
    start = time.monotonic()
    records, census = enumerate_fixed_extra(circles, case['gaps'], fixed)
    adjacency, graph_summary = graph(records)
    search = []
    witness = None
    for target in (6, 5, 4, 3):
        indices, coverage = find_clique(adjacency, target)
        coverage.pop('root_coloring', None)
        search.append(coverage)
        if indices is not None:
            witness = expand(circles, records, indices, case['gaps'], fixed)
            break
    require(witness is not None, 'no attaining clique located')
    return {'case': case['case'], 'extra_gap': case['extra_gap'], 'gaps': case['gaps'],
            'orbit_size': case['orbit_size'], 'enumeration': census,
            'graph': {k: graph_summary[k] for k in ('vertices', 'old_parts', 'edges', 'triangles', 'graph_sha256')},
            'search': search, 'witness': witness,
            'complete': True, 'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('four_gap_expected.json'))
    parser.add_argument('--case', type=int)
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text())
    circles, _ = classical_design()
    norm = normalization(circles)
    require(json.loads(json.dumps(norm)) == expected['single_normalization'], 'single-word normalization mismatch')
    chosen = norm['cases'] if args.case is None else [norm['cases'][args.case]]
    for case in chosen:
        result = run_case(circles, case, norm['fixed_old_four_set'])
        entry = expected['single_cases'][case['case']]
        require({k: result['enumeration'][k] for k in entry['enumeration']} == entry['enumeration'] and result['graph'] == entry['graph'], 'five-gap manifest mismatch')
        require(result['witness']['s'] == entry['witness']['s'] < 6, 'unexpected maximum outsider count')
        require(json.loads(json.dumps(result['witness'])) == entry['witness'], 'deterministic witness mismatch')
        print(json.dumps({'case': case['case'], 'records': result['graph']['vertices'], 'maximum_outsiders': result['witness']['s'], 'seconds': result['seconds']}), flush=True)
    print(json.dumps({'complete_cases': len(chosen), 'total_cases': 13, 'all_cases_complete': args.case is None}), flush=True)

if __name__ == '__main__':
    main()
