"""Complete fixed-word frontier from the classical S(3,5,17).
Agent: six-code-2, researcher. CPython3.11+, standard library only.
Timeouts and guards mean INCOMPLETE, never mathematical nonexistence.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import json
import resource
import time
from geometry import classical_design, mask, move, points, require
from generate_two_gap import digest
from generate_three_gap import graph, find_clique
from generate_five_gap_single import normalization as single_normalization

def normalize_pair(circles, fixed=15):
    start = time.monotonic()
    single = single_normalization(circles, fixed)
    stabilizer = single['stabilizer_permutations']
    contained = {mask(q) for c in circles for q in combinations(points(c), 4)}
    noncontained = {mask(q) for q in combinations(range(17), 4)} - contained
    first_forced = {c for c in circles if (c & fixed).bit_count() >= 3}
    domain = set()
    for q in sorted(noncontained):
        forced = {c for c in circles if (c & q).bit_count() >= 3}
        require(len(forced) == 4, 'incorrect second forced-gap count')
        if (q & fixed).bit_count() <= 1 and len(forced & first_forced) == 1:
            domain.add(q)
    require(len(domain) == 132, 'unexpected pointed partner count')
    unseen, cases = set(domain), []
    while unseen:
        require(time.monotonic() - start < 45, 'INCOMPLETE: normalization guard')
        q = min(unseen)
        orbit = {move(q, p) for p in stabilizer}
        require(orbit <= unseen, 'overlapping or invalid pointed orbit')
        forced = first_forced | {c for c in circles if (c & q).bit_count() >= 3}
        require(len(forced) == 7, 'incorrect seven forced gaps')
        cases.append({'case': len(cases), 'second_four_set': q,
                      'orbit_size': len(orbit), 'partner_orbit': sorted(orbit),
                      'gaps': sorted(forced)})
        unseen.difference_update(orbit)
    require(len(cases) == 18 and sum(c['orbit_size'] for c in cases) == 132,
            'pointed partner cover incomplete')
    return {'agent': 'six-code-2', 'role': 'researcher',
            'scope': 's7,t2,g7,target70', 'fixed_four_set': fixed,
            'partner_count': len(domain), 'stabilizer_order': len(stabilizer),
            'orbits': len(cases), 'cases': cases}

def enumerate_fixed_words(circles, gaps, fixed_words):
    start = time.monotonic()
    circle_set, gaps = set(circles), set(gaps)
    require(gaps <= circle_set, 'gap outside design')
    require(len(fixed_words) == len(set(fixed_words)) and fixed_words,
            'incorrect fixed-word list')
    for q in fixed_words:
        require(q.bit_count() == 4 and not any(c & q == q for c in circles),
                'fixed word is contained or has incorrect weight')
        require({c for c in circles if (c & q).bit_count() >= 3} <= gaps,
                'forced gap missing')
    require(all((q & r).bit_count() <= 1 for q, r in combinations(fixed_words, 2)),
            'fixed words incompatible')
    records = []
    reasons, eligible, assignments = Counter(), Counter(), Counter()
    nodes = 0
    for pts in combinations(range(17), 5):
        require(time.monotonic() - start < 45, 'INCOMPLETE: enumeration guard')
        b = mask(pts)
        if b in circle_set:
            reasons['design_circle'] += 1
            continue
        if any((b & q).bit_count() > 2 for q in fixed_words):
            reasons['fixed_word_conflict'] += 1
            continue
        meetings = [(c, (b & c).bit_count()) for c in circles if c not in gaps]
        if any(n >= 4 for _, n in meetings):
            reasons['nongap_four_point_circle'] += 1
            continue
        blockers = [c for c, n in meetings if n == 3]
        options = [[c ^ (1 << p) for p in pts if c >> p & 1
                    and all(((c ^ (1 << p)) & q).bit_count() <= 1 for q in fixed_words)]
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
    require(len(records) <= 40000, 'INCOMPLETE: final record count guard')
    require(sum(reasons.values()) + sum(eligible.values()) == 6188,
            'old-set universe incomplete')
    require(len(set(records)) == len(records), 'duplicate record')
    return records, {'records': len(records), 'records_sha256': digest(records),
                     'distinct_outsiders': len({b for b, qs in records}),
                     'rejection_reasons': dict(sorted(reasons.items())),
                     'eligible_outsiders': {str(k): v for k, v in sorted(eligible.items())},
                     'solution_counts': [{'mandatory_circles': k[0], 'assignments': k[1], 'outsiders': v}
                                         for k, v in sorted(assignments.items())],
                     'seconds': time.monotonic() - start}

def expand(circles, records, indices, gaps, fixed_words):
    outsiders = {records[i][0] for i in indices}
    qs = {q for i in indices for q in records[i][1]}
    removed = set(gaps) | {c for c in circles if any((c & b).bit_count() > 2 for b in outsiders)}
    words = sorted((set(circles) - removed) | outsiders
                   | {q | (1 << 17) for q in qs | set(fixed_words)})
    sets = [frozenset(p for p in range(18) if w >> p & 1) for w in words]
    require(len(outsiders) == len(indices), 'repeated outsider')
    require(len(words) == len(set(words)) == 68 + len(indices) + len(fixed_words) - len(gaps),
            'wrong expansion size')
    require(all(len(w) == 5 for w in sets), 'incorrect expansion weight')
    require(all(len(a & b) <= 2 for a, b in combinations(sets, 2)), 'invalid expansion')
    require(len(removed) - len(qs) == len(gaps), 'wrong gap parameter')
    return {'indices': indices, 'outsiders': sorted(outsiders), 'old_parts': sorted(qs),
            'fixed_words': list(fixed_words), 'words': words, 'size': len(words),
            's': len(indices), 't': len(fixed_words), 'a': len(qs),
            'R': len(removed), 'g': len(gaps)}

def normalize_single(circles, fixed=15):
    start = time.monotonic()
    base = single_normalization(circles, fixed)
    forced = set(base['forced_gaps'])
    stabilizer = base['stabilizer_permutations']
    universe = set(combinations(sorted(set(circles) - forced), 2))
    require(len(universe) == 2016, 'wrong extra-pair universe')
    unseen, cases = set(universe), []
    while unseen:
        require(time.monotonic() - start < 45, 'INCOMPLETE: single normalization guard')
        rep = min(unseen)
        orbit = {tuple(sorted(move(c, p) for c in rep)) for p in stabilizer}
        require(orbit <= unseen, 'overlapping or invalid extra-pair orbit')
        cases.append({'case': len(cases), 'extra_gaps': list(rep),
                      'orbit_size': len(orbit), 'extra_orbit': [list(pair) for pair in sorted(orbit)],
                      'gaps': sorted(forced | set(rep))})
        unseen.difference_update(orbit)
    require(sum(c['orbit_size'] for c in cases) == 2016, 'extra-pair cover incomplete')
    return {'agent': 'six-code-2', 'role': 'researcher', 'scope': 's7,t1,g6,target70',
            'fixed_four_set': fixed, 'extra_pairs': len(universe),
            'stabilizer_order': len(stabilizer), 'orbits': len(cases), 'cases': cases}


def run_case(circles, case, fixed_words):
    start = time.monotonic()
    records, census = enumerate_fixed_words(circles, case['gaps'], fixed_words)
    adjacency, summary = graph(records)
    for target in range(7, 0, -1):
        indices, coverage = find_clique(adjacency, target)
        require(coverage['complete'], 'INCOMPLETE: clique search')
        if indices is not None:
            witness = expand(circles, records, indices, case['gaps'], fixed_words)
            break
    else:
        raise ValueError('no attaining nonempty clique')
    return {'case': case['case'], 'gaps': case['gaps'], 'orbit_size': case['orbit_size'],
            'enumeration': {k: census[k] for k in ('records','records_sha256','distinct_outsiders')},
            'graph': {k: summary[k] for k in ('vertices','old_parts','edges','triangles','graph_sha256')},
            'witness': witness, 'maximum_clique_size': witness['s'],
            'complete': True, 'seconds': time.monotonic() - start,
            'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('fixed_word_gap_expected.json'))
    parser.add_argument('--branch', choices=('single','pair','both'), default='both')
    parser.add_argument('--case', type=int)
    parser.add_argument('--checkpoint-dir', type=Path)
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text())
    circles, _ = classical_design()
    pair = normalize_pair(circles)
    single = normalize_single(circles)
    require(pair == expected['pair_normalization'], 'pair normalization mismatch')
    require(single == expected['single_normalization'], 'single normalization mismatch')
    branches = ('pair','single') if args.branch == 'both' else (args.branch,)
    total, seconds, maxima = 0, 0, Counter()
    for branch in branches:
        norm = pair if branch == 'pair' else single
        cases = norm['cases'] if args.case is None else [norm['cases'][args.case]]
        for case in cases:
            fixed_words = (norm['fixed_four_set'],) if branch == 'single' else (norm['fixed_four_set'],case['second_four_set'])
            result = run_case(circles, case, fixed_words)
            fixture = expected[branch+'_cases'][case['case']]
            for key in ('gaps','orbit_size','enumeration','graph','witness','maximum_clique_size'):
                require(result[key] == fixture[key], 'production '+key+' mismatch')
            if args.checkpoint_dir is not None:
                args.checkpoint_dir.mkdir(parents=True, exist_ok=True)
                path = args.checkpoint_dir / (branch+'-'+str(case['case'])+'.json')
                temporary = path.with_suffix('.tmp')
                temporary.write_text(json.dumps(result,indent=2)+'\n')
                temporary.replace(path)
            total += 1
            seconds += result['seconds']
            maxima[(branch,result['maximum_clique_size'])] += 1
            print(json.dumps({'branch':branch,'case':case['case'],'complete':True,
                              'maximum_outsiders':result['maximum_clique_size'],
                              'packing_size':result['witness']['size'],'seconds':result['seconds']}),flush=True)
    print(json.dumps({'complete_cases':total,'coverage':'all313cases' if total==313 else 'partial',
                      'maxima':{str(k):v for k,v in sorted(maxima.items())},'seconds':seconds}),flush=True)


if __name__ == '__main__':
    main()
