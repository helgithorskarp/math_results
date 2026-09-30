#!/usr/bin/env python3
"""Complete primary-anchor pair covers and an ordinary secondary capacity bound."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from check_adjacent_low import field_plane, mul4, all_covers, capacity, require, encoded

HERE = Path(__file__).resolve().parent
U, A, B = 17, 0, 16
X = (1, 2, 3, 4, 8, 12)
N = (5, 6, 7, 9, 10, 11, 13, 14, 15, 16)
W = tuple(range(1, 17))
H = tuple(range(1, 16))
PAIRS = tuple(combinations(range(1, 18), 2))
PAIR_INDEX = {p: i for i, p in enumerate(PAIRS)}
AXES = {frozenset((0, 1, 2, 3)), frozenset((0, 4, 8, 12))}


def mask_pairs(pairs):
    return sum(1 << PAIR_INDEX[p] for p in pairs)


def unmask_pairs(mask):
    return tuple(p for i, p in enumerate(PAIRS) if mask >> i & 1)


def packing(words):
    require(len(words) == len(set(words)), 'duplicate words')
    require(all(len(w) == 5 and w <= set(range(18)) for w in words), 'word domain/weight')
    require(all(len(w & v) <= 2 for w, v in combinations(words, 2)), 'packing distance')


def first_star():
    star = [frozenset((q - {A}) | {B, U}) if A in q and q not in AXES
            else frozenset(q | {U}) for q in field_plane()]
    packing(star)
    require(len(star) == 20, 'first star size')
    pairs = Counter(p for w in star for p in combinations(sorted(w), 2))
    require([(x, 5 - pairs[tuple(sorted((U, x)))]) for x in range(17)
             if pairs[tuple(sorted((U, x)))] < 5] == [(A, 3), (B, 2)], 'first deficit row')
    return star


def raw_leaves():
    result = {}
    forced = {tuple(sorted((U, n))) for n in N}
    groups = (set(X[:3]), set(X[3:]))

    def put(kind, c, d, other):
        leave = forced | {tuple(sorted(p)) for p in other}
        degrees = Counter(x for p in leave for x in p)
        require(len(leave) == 16 and all(degrees[x] == (10 if x == U else 4 if x in (c, d) else 1)
                for x in range(1, 18)), 'primary leave degrees')
        require(not any(p in leave for g in groups for p in combinations(sorted(g), 2)),
                'leave conflicts with fixed shared word')
        mask = mask_pairs(leave)
        require(mask not in result, 'duplicate leave')
        result[mask] = (kind, c, d)

    for c, d in combinations(N, 2):
        for part in combinations(X, 3):
            put('middle', c, d, {(c, x) for x in part} | {(d, x) for x in set(X) - set(part)})
        for x, y in product(X[:3], X[3:]):
            other = set(X) - {x, y}
            for part in combinations(sorted(other), 2):
                put('triangle', c, d, {(c, d), (x, y)} | {(c, z) for z in part}
                    | {(d, z) for z in other - set(part)})
    for c, d in product(N, X):
        own = next(g for g in groups if d in g)
        put('end', c, d, {(c, x) for x in own} | {(d, x) for x in set(X) - own})
    require(Counter(k for k, _, _ in result.values()) == {'middle': 900, 'triangle': 2430, 'end': 60},
            'raw leave count')
    return result


def group(star):
    maps = set()
    for sx, sy, swap, conjugate in product((1, 2, 3), (1, 2, 3), range(2), range(2)):
        mapping = []
        for x, y in product(range(4), repeat=2):
            if conjugate:
                x, y = mul4(x, x), mul4(y, y)
            if swap:
                x, y = y, x
            mapping.append(4 * mul4(sx, x) + mul4(sy, y))
        mapping = tuple(mapping + [B, U])
        require(len(set(mapping)) == 18 and all(mapping[x] == x for x in (U, A, B)), 'group labels')
        require({frozenset(mapping[x] for x in w) for w in star} == set(star), 'group word images')
        maps.add(mapping)
    require(len(maps) == 36 and all(tuple(p[q[x]] for x in range(18)) in maps
            for p in maps for q in maps), 'group closure')
    return sorted(maps)


def instances():
    star = first_star()
    carrier = raw_leaves()
    maps = group(star)
    columns = tuple(q for q in combinations(W, 4)
                    if all(len((frozenset(q) | {A}) & w) <= 2 for w in star))
    fixed = [w for w in star if A in w]
    fixed_pairs = {p for w in fixed for p in combinations(sorted(w - {A}), 2)}
    base = set(combinations(W, 2)) - fixed_pairs
    require(len(fixed) == 2 and len(columns) == 597 and len(base) == 114, 'primary universes')
    remaining = set(carrier)
    cases = []
    while remaining:
        representative = min(remaining)
        leave = unmask_pairs(representative)
        orbit = {mask_pairs(tuple(sorted((g[x], g[y]))) for x, y in leave) for g in maps}
        require(orbit <= remaining, 'leave orbit overlap/domain')
        remaining -= orbit
        rows = tuple(sorted(base - set(leave)))
        row_set = set(rows)
        legal = tuple(q for q in columns if set(combinations(q, 2)) <= row_set)
        require(len(rows) == 108, 'primary residual pair count')
        cases.append({'index': len(cases), 'representative': representative,
                      'kind': carrier[representative][0], 'high_centers': carrier[representative][1:],
                      'orbit_size': len(orbit), 'rows': rows, 'columns': legal})
    require(len(cases) == 117 and sum(c['orbit_size'] for c in cases) == 3390, 'orbit coverage')
    return star, fixed, carrier, maps, cases


def data():
    star, fixed, carrier, maps, cases = instances()
    raw_b = tuple(q for q in combinations(H, 4)
                  if all(len((frozenset(q) | {B}) & w) <= 2 for w in star))
    require(len(raw_b) == 279, 'root-compatible secondary universe')
    # Precompute only literal cross-word compatibility, with no packing prune.
    all_a = {q for case in cases for q in case['columns']}
    compatible_b = {q: sum(1 << i for i, p in enumerate(raw_b)
                          if len((frozenset(p) | {B}) & (frozenset(q) | {A})) <= 2)
                    for q in all_a}
    result = []
    entries = []
    for case in cases:
        covers, nodes = all_covers(case['rows'], case['columns'], node_cap=200000, seconds=10)
        details = []
        for cover in covers:
            second = fixed + [frozenset(q) | {A} for q in cover]
            union = sorted(set(star + second), key=lambda w: tuple(sorted(w)))
            packing(union)
            require(len(second) == 20 and len(union) == 38, 'primary star/union size')
            pairs = Counter(p for w in second for p in combinations(sorted(w), 2))
            deficits = [(x, 5 - pairs[tuple(sorted((A, x)))]) for x in range(18)
                        if x != A and pairs[tuple(sorted((A, x)))] < 5]
            c, d = case['high_centers']
            require(sorted(deficits) == sorted(((U, 3), (c, 1), (d, 1))), 'primary deficit row')
            bfixed = sum(B in w for w in union)
            require(bfixed == (7 if B in (c, d) else 8), 'fixed secondary degree')
            active = (1 << len(raw_b)) - 1
            for q in cover:
                active &= compatible_b[q]
            columns = tuple(q for i, q in enumerate(raw_b) if active >> i & 1)
            bound = capacity(columns, H)
            require(bfixed + bound['upper_bound'] <= 19, 'secondary anchor bound')
            details.append({'primary_extra_quads': [list(q) for q in cover],
                            'secondary_fixed_words': bfixed, 'secondary_needed_for_twenty': 20 - bfixed,
                            'secondary_candidates': len(columns),
                            'secondary_candidates_sha256': sha256(encoded(columns)).hexdigest(), **bound})
            entries.append((case['representative'], cover, tuple(columns)))
        result.append({'index': case['index'], 'representative': case['representative'],
                       'kind': case['kind'], 'high_centers': list(case['high_centers']),
                       'orbit_size': case['orbit_size'], 'rows': len(case['rows']),
                       'columns': len(case['columns']),
                       'rows_sha256': sha256(encoded(case['rows'])).hexdigest(),
                       'columns_sha256': sha256(encoded(case['columns'])).hexdigest(),
                       'cover_nodes': nodes, 'compatible_primary_stars': details})
    report = {'status': 'COMPLETE', 'raw_leave_types': dict(Counter(k for k, _, _ in carrier.values())),
              'raw_leaves': len(carrier), 'first_star_symmetries': len(maps), 'leave_orbits': len(cases),
              'first_star_compatible_primary_quads': 597, 'first_star_compatible_secondary_quads': len(raw_b),
              'cover_nodes': sum(c['cover_nodes'] for c in result),
              'realized_leave_orbits': sum(bool(c['compatible_primary_stars']) for c in result),
              'compatible_primary_stars': len(entries),
              'primary_stars_by_kind': dict(Counter(case['kind'] for case in result
                        for _ in case['compatible_primary_stars'])),
              'secondary_extra_upper_bound': max(d['upper_bound'] for c in result
                                                for d in c['compatible_primary_stars']),
              'secondary_total_upper_bound': max(d['secondary_fixed_words'] + d['upper_bound']
                                                for c in result for d in c['compatible_primary_stars']),
              'all_secondary_saturation_excluded': True, 'global_72_word_exclusion': False,
              'independent_peer_review': False, 'cases': result}
    return report, entries, cases, star


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    report, _, _, _ = data()
    path = HERE / 'single_isolate_expected.json'
    if args.write_expected:
        path.write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    else:
        require(json.loads(path.read_text()) == report, 'primary manifest differs')
    print(json.dumps({k: v for k, v in report.items() if k != 'cases'}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
