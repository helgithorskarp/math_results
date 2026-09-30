#!/usr/bin/env python3
"""Complete pair-cover proof for the shared-secondary-anchor carrier."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from check_adjacent_low import all_covers, encoded, field_plane, mul4, require

HERE = Path(__file__).resolve().parent
U, V, A, B = 17, 1, 0, 16
H = tuple(x for x in range(18) if x not in (U, V, B))
W = tuple(x for x in range(18) if x not in (U, V))
AXES = {frozenset((0, 1, 2, 3)), frozenset((0, 4, 8, 12))}
REPRESENTATIVES = (2, 4, 5, 6)


def packing(words):
    require(len(words) == len(set(words)), 'duplicate words')
    require(all(len(w) == 5 and set(w) <= set(range(18)) for w in words),
            'word domain/weight')
    require(all(len(set(x) & set(y)) <= 2 for x, y in combinations(words, 2)),
            'repeated triple')


def root():
    star = [frozenset((line - {A}) | {U, B})
            if A in line and line not in AXES else frozenset(line | {U})
            for line in field_plane()]
    packing(star)
    require(len(star) == 20 and all(U in w for w in star), 'first star')
    fixed = sorted((w for w in star if V in w), key=lambda w: tuple(sorted(w)))
    groups = sorted(tuple(sorted(w - {U, V})) for w in fixed)
    require(len(fixed) == 5 and sum(map(len, groups)) == 15
            and set(x for g in groups for x in g) == set(H), 'shared pencil')
    return star, fixed, groups


def normalization(star):
    maps = []
    for scale, conjugate in product((1, 2, 3), range(2)):
        def square(x):
            return mul4(x, x) if conjugate else x
        mapping = tuple(4 * mul4(scale, square(x)) + square(y)
                        for x, y in product(range(4), repeat=2)) + (B, U)
        require(len(set(mapping)) == 18 and all(mapping[x] == x for x in (U, V, A, B)),
                'bad first-star symmetry')
        require({frozenset(mapping[x] for x in w) for w in star} == set(star),
                'first-star symmetry changes words')
        maps.append(mapping)
    group = set(maps)
    require(len(group) == 6 and all(tuple(p[q[x]] for x in range(18)) in group
            for p in group for q in group), 'six maps do not form a group')
    orbits = [sorted({p[c] for p in maps}) for c in REPRESENTATIVES]
    require(sum(map(len, orbits)) == 14 and set(x for orbit in orbits for x in orbit)
            == set(range(2, 16)), 'incomplete primary-anchor orbits')
    return {'checked_symmetries': 6, 'primary_anchor_orbits': orbits}


def second_instances(c):
    star, fixed, groups = root()
    fixed_pairs = {p for w in fixed for p in combinations(sorted(w - {V}), 2)}
    cgroup = next(set(g) for g in groups if c in g)
    remainder = sorted(set(H) - cgroup)
    require(len(remainder) == 12, 'second origin-line universe')
    possible = [q for q in combinations(W, 4)
                if all(len((frozenset(q) | {V}) & w) <= 2 for w in star)]
    instances = []
    # All 220 three-subsets are considered before any compatibility filter.
    for tail in combinations(remainder, 3):
        special = tuple(sorted((c,) + tail))
        if special not in possible:
            continue
        cpart = {U} | (cgroup - {c}) | set(tail)
        bpart = set(H) - cgroup - set(tail)
        leave = {tuple(sorted((B, c)))}
        leave |= {tuple(sorted((B, x))) for x in cpart}
        leave |= {tuple(sorted((c, x))) for x in bpart}
        require(len(cpart) == 6 and len(bpart) == 9 and len(leave) == 16,
                'wrong complete double-star leave')
        require(not (fixed_pairs & leave), 'shared words cover a forced leave')
        rows90 = set(combinations(W, 2)) - fixed_pairs - leave
        used = set(combinations(special, 2))
        require(len(rows90) == 90 and used <= rows90, 'second-star rows')
        rows = tuple(sorted(rows90 - used))
        columns = tuple(q for q in possible if set(combinations(q, 2)) <= set(rows))
        require(len(rows) == 84 and all(c not in q for q in columns),
                'second-star residual rows/center')
        instances.append({'tail': tail, 'fixed': fixed, 'special': special,
                          'rows': rows, 'columns': columns})
    return star, instances


def anchor_instance(vstar, star):
    union = sorted(set(star + vstar), key=lambda w: tuple(sorted(w)))
    packing(union)
    require(len(union) == 35, 'wrong two-star union')
    fixed = [w for w in union if B in w]
    require(len(fixed) == 6, 'wrong fixed anchor words')
    tails = [set(w) & set(H) for w in fixed]
    require(all(len(t) == 3 for t in tails), 'fixed tail size')
    I = set(x for w in fixed if U in w for x in set(w) & set(H))
    J = set(x for w in fixed if V in w for x in set(w) & set(H))
    require(len(I) == len(J) == 9, 'fixed tail unions')
    T = I & J
    overlap = len(T)
    used = {p for tail in tails for p in combinations(sorted(tail), 2)}
    require(len(used) == 18, 'fixed tails repeat pairs')
    require(3 <= overlap <= 9, 'invalid overlap')
    if overlap >= 5:
        return {'overlap': overlap, 'status': 'POINT_CAPACITY',
                'extra_upper_bound': (60 - overlap) // 4}, []
    columns = tuple(q for q in combinations(H, 4)
                    if all(len((frozenset(q) | {B}) & w) <= 2 for w in union))
    free = set(combinations(H, 2)) - used
    require(len(free) == 87, 'free anchor pairs')
    leaves = []
    if overlap == 3:
        require(I | J == set(H), 'overlap-three carrier')
        for e in sorted(set(H) - T):
            leaves.append((e, {tuple(sorted((e, x))) for x in T}))
    else:
        missing = set(H) - (I | J)
        require(len(missing) == 1, 'overlap-four carrier')
        e = next(iter(missing))
        for neighbors in combinations(sorted(T), 2):
            other = tuple(sorted(T - set(neighbors)))
            leaves.append((e, {tuple(sorted((e, x))) for x in neighbors} | {other}))
    trials = []
    details = []
    for e, leave in leaves:
        # Check the ordinary degree bridge independently of cover execution.
        frequencies = Counter(x for tail in tails for x in tail)
        degrees = Counter(x for edge in leave for x in edge)
        require(len(leave) == 3 and all(degrees[x] == frequencies[x] - 1 + 3 * (x == e)
                for x in H), 'wrong anchor leave-degree vector')
        label = {'e': e, 'leave': [list(p) for p in sorted(leave)]}
        if not leave <= free:
            trials.append({**label, 'status': 'FIXED_PAIR_CONFLICT'})
            details.append((e, tuple(sorted(leave)), None, None))
            continue
        rows = tuple(sorted(free - leave))
        cols = tuple(q for q in columns if set(combinations(q, 2)) <= set(rows))
        require(len(rows) == 84, 'wrong anchor cover rows')
        available_pairs = {p for q in cols for p in combinations(q, 2)}
        missing = sorted(set(rows) - available_pairs)
        require(missing, 'no uncovered-pair certificate; exclusion not established')
        witness = missing[0]
        require(witness in rows and all(not set(witness) <= set(q) for q in cols),
                'invalid uncovered-pair certificate')
        trials.append({**label, 'status': 'UNCOVERABLE_PAIR', 'columns': len(cols),
                       'rows_sha256': sha256(encoded(rows)).hexdigest(),
                       'columns_sha256': sha256(encoded(cols)).hexdigest(),
                       'uncoverable_pair': list(witness), 'uncoverable_pairs': len(missing)})
        details.append((e, tuple(sorted(leave)), rows, cols))
    trials.sort(key=lambda r: (r['e'], r['leave']))
    details.sort()
    return {'overlap': overlap, 'anchor_candidates': len(columns),
            'anchor_candidate_sha256': sha256(encoded(columns)).hexdigest(),
            'status': 'COMPLETED_ANCHOR_TRIALS', 'trials': trials}, details


def data():
    star, _, _ = root()
    normal = normalization(star)
    report = []
    all_stars = {}
    detail = {}
    for c in REPRESENTATIVES:
        _, instances = second_instances(c)
        census = []
        stars = {}
        for case in instances:
            covers, nodes = all_covers(case['rows'], case['columns'])
            census.append({'tail': list(case['tail']), 'columns': len(case['columns']),
                           'cover_nodes': nodes, 'second_stars': len(covers),
                           'rows_sha256': sha256(encoded(case['rows'])).hexdigest(),
                           'columns_sha256': sha256(encoded(case['columns'])).hexdigest()})
            for cover in covers:
                words = case['fixed'] + [frozenset(case['special']) | {V}]
                words += [frozenset(q) | {V} for q in cover]
                packing(words)
                require(len(words) == 20 and all(V in w for w in words)
                        and all(len(x & y) <= 2 for x in star for y in words if x != y),
                        'invalid completed second star')
                key = tuple(sorted(tuple(sorted(w)) for w in words))
                require(key not in stars, 'duplicated second star')
                result, instance_details = anchor_instance(words, star)
                stars[key] = result
                detail[c, key] = instance_details
        all_stars[c] = stars
        report.append({'c': c, 'complete_tail_universe': 220,
                       'compatible_other_origin_lines': len(instances),
                       'second_star_searches': census, 'compatible_second_stars': len(stars),
                       'stars': [{'vstar': [list(w) for w in key], **result}
                                 for key, result in sorted(stars.items())]})
    summary = {'normalization': normal, 'cases': report,
               'compatible_second_stars': sum(map(len, all_stars.values())),
               'anchor_completions': 0, 'status': 'COMPLETE',
               'theorem_depends_on_computation': True, 'global_72_word_exclusion': False}
    return summary, all_stars, detail


def controls():
    # The reused complete-cover kernel was previously checked on all 1,100
    # small graphs. Recheck that audit and a positive affine cover here.
    from check_adjacent_low import controls as cover_controls
    checks = cover_controls()
    star, _, _ = root()
    packing(star)
    rejected = 0
    for bad in (star[:-1] + [star[0]], star[:-1] + [frozenset((0, 1, 2, 4, U))]):
        try:
            packing(bad)
        except ValueError:
            rejected += 1
    require(rejected == 2, 'corrupted first stars accepted')
    checks['new_semantic_corruptions_rejected'] = rejected
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    report, _, _ = data()
    report['controls'] = controls()
    if args.write:
        args.write.write_bytes(encoded(report))
    else:
        require(report == json.loads((HERE / 'two_isolates_expected.json').read_text()),
                'two-isolate replay manifest mismatch')
    print(json.dumps({'status': report['status'], 'compatible_second_stars': report['compatible_second_stars'],
                      'stars_by_c': {r['c']: r['compatible_second_stars'] for r in report['cases']},
                      'anchor_completions': 0, 'manifest_sha256': sha256(encoded(report)).hexdigest()},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
