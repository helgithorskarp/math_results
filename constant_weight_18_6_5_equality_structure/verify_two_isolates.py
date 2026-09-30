#!/usr/bin/env python3
"""Different replay: relative permutation planes and direct missing-pair certificates."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time

from verify_adjacent_low import (MULT, SQUARE, a4_plane, automorphism_coverage,
                                 check_star, decode, encoded, masks, require)

HERE = Path(__file__).resolve().parent
U, V, A, B = 17, 1, 0, 16
H = tuple(x for x in range(18) if x not in (U, V, B))
AXES = {sum(1 << x for x in q) for q in ((0, 1, 2, 3), (0, 4, 8, 12))}
REPRESENTATIVES = (2, 4, 5, 6)


def root(lines):
    star = sorted(q ^ 1 | 1 << B | 1 << U
                  if q & 1 and q not in AXES else q | 1 << U for q in lines)
    check_star(star, U)
    targets = sorted(decode(w ^ (1 << U) ^ (1 << V)) for w in star if w >> V & 1)
    require(len(targets) == 5 and sum(map(len, targets)) == 15
            and {x for g in targets for x in g} == set(H), 'fixed pencil')
    return star, targets


def first_orbits(star):
    maps = []
    for factor, conjugate in product((1, 2, 3), (0, 1)):
        mapping = tuple(4 * MULT[factor][SQUARE[x] if conjugate else x]
                        + (SQUARE[y] if conjugate else y)
                        for x, y in product(range(4), repeat=2)) + (B, U)
        require(len(set(mapping)) == 18 and all(mapping[x] == x for x in (U, V, A, B)),
                'stabilizer labels')
        require({sum(1 << mapping[x] for x in decode(w)) for w in star} == set(star),
                'stabilizer changes first star')
        maps.append(mapping)
    require(len(set(maps)) == 6 and all(tuple(p[q[x]] for x in range(18)) in maps
            for p in maps for q in maps), 'incomplete stabilizer closure')
    orbits = [sorted({p[c] for p in maps}) for c in REPRESENTATIVES]
    require(sum(map(len, orbits)) == 14 and {x for g in orbits for x in g}
            == set(range(2, 16)), 'missing anchor orbit')
    return orbits


def missing_pair_certificate(rows, columns, pair):
    require(pair in rows, 'certificate pair is not required')
    bitpair = (1 << pair[0]) | (1 << pair[1])
    require(all(q & bitpair != bitpair for q in columns),
            'certificate pair is covered by a legal quadruple')


def replay_anchor(union):
    fixed = [w for w in union if w >> B & 1]
    require(len(fixed) == 6, 'fixed anchor replication')
    frequencies = Counter(x for w in fixed for x in decode(w) if x in H)
    require(sum(frequencies.values()) == 18 and all(frequencies[x] <= 2 for x in H),
            'fixed tail frequencies')
    overlap = sum(frequencies[x] == 2 for x in H)
    used = {(x, y) for w in fixed for x, y in combinations(decode(w), 2) if x in H and y in H}
    require(len(used) == 18, 'fixed tail pairs')
    capacities = [(14 - 2 * frequencies[x]) // 3 for x in H]
    bound = sum(capacities) // 4
    if bound < 14:
        require(overlap >= 5, 'unexpected point-capacity case')
        return {'overlap': overlap, 'status': 'POINT_CAPACITY', 'extra_upper_bound': bound}, []
    require(overlap in (3, 4), 'unexpected surviving overlap')
    qwords = tuple(q for q in masks(H, 4)
                   if all(((q | 1 << B) ^ w).bit_count() >= 6 for w in union))
    qwords = tuple(sorted(qwords, key=decode))
    trials, details = [], []
    # Enumerate all H-leave graphs of three edges from the required degrees.
    # This does not use the primary's star/matching leave formulas.
    for e in H:
        degrees = {x: frequencies[x] - 1 + 3 * (x == e) for x in H}
        if any(d < 0 or d > 3 for d in degrees.values()) or sum(degrees.values()) != 6:
            continue
        carrier = tuple(x for x in H if degrees[x])
        for edges in combinations(tuple(combinations(carrier, 2)), 3):
            actual = Counter(x for edge in edges for x in edge)
            if any(actual[x] != degrees[x] for x in H):
                continue
            leave = set(edges)
            label = {'e': e, 'leave': [list(p) for p in sorted(leave)]}
            if leave & used:
                trials.append({**label, 'status': 'FIXED_PAIR_CONFLICT'})
                details.append((e, tuple(sorted(leave)), None, None))
                continue
            rows = tuple(p for p in combinations(H, 2) if p not in used | leave)
            require(len(rows) == 84, 'wrong anchor pair universe')
            columns = tuple(q for q in qwords
                            if all(p in rows for p in combinations(decode(q), 2)))
            missing = []
            for pair in rows:
                bitpair = (1 << pair[0]) | (1 << pair[1])
                if all(q & bitpair != bitpair for q in columns):
                    missing.append(pair)
            require(missing, 'no missing-pair certificate; exclusion not established')
            witness = min(missing)
            missing_pair_certificate(rows, columns, witness)
            decoded = tuple(decode(q) for q in columns)
            trials.append({**label, 'status': 'UNCOVERABLE_PAIR', 'columns': len(columns),
                           'rows_sha256': sha256(encoded(rows)).hexdigest(),
                           'columns_sha256': sha256(encoded(decoded)).hexdigest(),
                           'uncoverable_pair': list(witness), 'uncoverable_pairs': len(missing)})
            details.append((e, tuple(sorted(leave)), rows, decoded))
    require(len(trials) == (12 if overlap == 3 else 6), 'incomplete anchor leave carrier')
    trials.sort(key=lambda r: (r['e'], r['leave']))
    details.sort()
    return {'overlap': overlap, 'anchor_candidates': len(qwords),
            'anchor_candidate_sha256': sha256(encoded(tuple(decode(q) for q in qwords))).hexdigest(),
            'status': 'COMPLETED_ANCHOR_TRIALS', 'trials': trials}, details


def data():
    lines = a4_plane()
    actions = automorphism_coverage(lines)
    star, targets = root(lines)
    orbits = first_orbits(star)
    groups = sorted(decode(q ^ 1) for q in lines if q & 1)
    assignments = [[(targets[0][0],) + p for p in permutations(targets[0][1:])]]
    assignments += [list(permutations(g)) for g in targets[1:]]
    fixed = {w for w in star if w >> V & 1}
    other_u = [w for w in star if not w >> V & 1]
    all_stars, details, cases = {}, {}, []
    for c in REPRESENTATIVES:
        seen, found = set(), {}
        splits = 0
        start = time.monotonic()
        for index, assignment in enumerate(product(*assignments)):
            if index % 128 == 0 and time.monotonic() - start > 10:
                raise RuntimeError('INCOMPLETE: plane enumeration cap; no exclusion')
            mapping = {0: U}
            mapping.update({x: y for g, t in zip(groups, assignment) for x, y in zip(g, t)})
            plane = tuple(sorted(sum(1 << mapping[x] for x in decode(q)) for q in lines))
            require(plane not in seen, 'repeated normalized plane')
            seen.add(plane)
            pencil = [q for q in plane if q >> c & 1]
            cu = [q for q in pencil if q >> U & 1]
            require(len(pencil) == 5 and len(cu) == 1, 'split pencil')
            for cq in pencil:
                if cq == cu[0]:
                    continue
                splits += 1
                words = sorted(q ^ (1 << c) | 1 << B | 1 << V
                               if q >> c & 1 and q not in (cu[0], cq) else q | 1 << V
                               for q in plane)
                require({w for w in words if w >> U & 1} == fixed, 'fixed shared words changed')
                other_v = [w for w in words if not w >> U & 1]
                if not all((x ^ y).bit_count() >= 6 for x in other_v for y in other_u):
                    continue
                check_star(words, V)
                union = sorted(set(star + words))
                require(len(union) == 35 and all((x ^ y).bit_count() >= 6
                        for i, x in enumerate(union) for y in union[i + 1:]), 'invalid two-star union')
                key = tuple(sorted(decode(w) for w in words))
                require(key not in found, 'second-star duplicate')
                result, instance_details = replay_anchor(union)
                found[key] = result
                details[c, key] = instance_details
        require(len(seen) == 2592 and splits == 10368, 'incomplete relative-plane domain')
        all_stars[c] = found
        cases.append({'c': c, 'relative_planes': len(seen), 'splits': splits,
                      'compatible_second_stars': len(found),
                      'second_star_sha256': sha256(encoded(sorted(found))).hexdigest(),
                      'overlap_histogram': dict(sorted(Counter(r['overlap'] for r in found.values()).items())),
                      'anchor_trials': sum(len(r.get('trials', [])) for r in found.values())})
    return {'automorphism_coverage': actions, 'primary_anchor_orbits': orbits, 'cases': cases,
            'relative_planes': 10368, 'split_stars': 41472,
            'compatible_second_stars': sum(map(len, all_stars.values())), 'anchor_completions': 0,
            'status': 'COMPLETE', 'independent_peer_review': False}, all_stars, details, star


def controls():
    quads = a4_plane()[:14]
    rows = tuple(sorted({p for q in quads for p in combinations(decode(q), 2)}))
    require(len(rows) == 84 and all(sum(all(q >> x & 1 for x in pair) for q in quads) == 1
            for pair in rows), 'positive fourteen-quadruple fixture')
    rejected = 0
    for pair in (rows[0], (0, 17)):
        try:
            missing_pair_certificate(rows, quads, pair)
        except ValueError:
            rejected += 1
    require(rejected == 2, 'corrupted missing-pair certificates accepted')
    return {'positive_fourteen_quadruple_cover': True,
            'corrupted_missing_pair_certificates_rejected': rejected}


def compare_primary(stars, details, star):
    import check_two_isolates as primary
    _, other_stars, other_details = primary.data()
    other_root, _, _ = primary.root()
    require(set(star) == {sum(1 << x for x in w) for w in other_root}, 'first-star entries differ')
    require({c: set(x) for c, x in stars.items()} == {c: set(x) for c, x in other_stars.items()},
            'complete second-star lists differ')
    for key in details:
        require(sorted(details[key]) == sorted(other_details[key]), 'anchor rows/columns/leaves differ')
    for c in REPRESENTATIVES:
        for key, replay in stars[c].items():
            expected = other_stars[c][key]
            require(replay == expected, 'anchor census or missing-pair certificate differs')
    return {'first_star_all_entries': True, 'second_stars_all_entries': True,
            'anchor_leaves_rows_columns_all_entries': True, 'all_missing_pair_certificates': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compare-primary', action='store_true')
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    report, stars, details, star = data()
    report['controls'] = controls()
    if args.compare_primary:
        report['entrywise_comparison'] = compare_primary(stars, details, star)
    if args.write:
        args.write.write_bytes(encoded(report))
    else:
        expected = json.loads((HERE / 'two_isolates_replay_expected.json').read_text())
        if not args.compare_primary:
            expected.pop('entrywise_comparison', None)
        require(encoded(report) == encoded(expected), 'two-isolate replay manifest mismatch')
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
