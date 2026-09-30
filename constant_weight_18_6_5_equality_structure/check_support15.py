#!/usr/bin/env python3
"""Exact local carrier checks; external design theorem is not re-proved here."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from reproduce import construct_link

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def components(neighbors):
    unseen = set(range(len(neighbors)))
    result = []
    while unseen:
        reached = set()
        stack = [min(unseen)]
        while stack:
            v = stack.pop()
            if v not in reached:
                reached.add(v)
                stack.extend(neighbors[v] - reached)
        unseen -= reached
        result.append(reached)
    return result


def four_point_carrier():
    pairs = tuple(combinations(range(4), 2))
    cases = Counter()
    orbits = Counter()
    accepted = 0
    for weights in product(range(5), repeat=6):
        neighbors = [set() for _ in range(4)]
        totals = [0] * 4
        for (u, v), w in zip(pairs, weights):
            if w:
                neighbors[u].add(v)
                neighbors[v].add(u)
                totals[u] += w
                totals[v] += w
        degrees = [len(n) for n in neighbors]
        if max(degrees) > 2:
            continue
        if any((d == 2 and t != 5) or (d == 1 and not 2 <= t <= 4)
               for d, t in zip(degrees, totals)):
            continue
        parts = components(neighbors)
        if any(all(degrees[v] == 2 for v in c) or len(c) == 3 for c in parts):
            continue  # Published cycle/path lemmas at h=14.
        accepted += 1
        matrix = {e: w for e, w in zip(pairs, weights)}
        canonical = min(tuple(matrix[tuple(sorted((p[u], p[v])))] for u, v in pairs)
                        for p in permutations(range(4)))
        orbits[canonical] += 1
        if len(parts) == 1:
            endpoint = next(v for v in range(4) if degrees[v] == 1)
            other = next(iter(neighbors[endpoint]))
            w = matrix[tuple(sorted((endpoint, other)))]
            cases['path_endpoint_weight_' + str(w)] += 1
        elif 3 in weights:
            cases['weight_three_anchor_exclusion'] += 1
        elif 4 in weights:
            if sorted(map(len, parts)) == [2, 2] and weights.count(4) == 2:
                cases['K5_plus_matching_design_obstruction'] += 1
            else:
                cases['weight_four_anchor_reduction'] += 1
        else:
            cases['pure_isolated_or_weight_two_components'] += 1
    require(accepted == 82 and len(orbits) == 13, 'four-point carrier count differs')
    require(cases['K5_plus_matching_design_obstruction'] == 3,
            'wrong weight-four-pair boundary')
    return {'weight_assignments_checked': 5 ** 6, 'admissible_labeled_patterns': accepted,
            'isomorphism_types': len(orbits), 'cases': dict(sorted(cases.items())),
            'canonical_types': [{'weights': list(w), 'labeled_patterns': n}
                                for w, n in sorted(orbits.items())]}


def forced_path_blocks():
    checked = 0
    for w in combinations(range(4, 18), 2):
        first = {0, 1, 3, *w}
        last = {0, 2, 3, *w}
        require(len(first) == len(last) == 5 and first != last, 'wrong forced blocks')
        require(len(first & last) == 4, 'path forced blocks do not conflict')
        checked += 1
    return {'missing_H_pairs_checked': checked, 'forced_block_intersection': 4}


def filtered_catalog():
    catalog = json.loads((HERE / 'local_types.json').read_text())
    bad = [row for row in catalog if row['partition'] == [1] * 5
           and row['core_mask'] == (1 << 10) - 1]
    require(len(catalog) == 48 and len(bad) == 1, 'wrong catalog boundary')
    row = bad[0]
    require(row['leaf_counts'] == [0] * 5 and row['isolated_pairs'] == 6,
            'excluded catalog entry is not K5 plus six matching edges')
    edges = construct_link(row)
    require(all(tuple(e) in edges for e in combinations(range(5), 2)), 'K5 missing')
    require(all(not (u < 5 <= v) for u, v in edges), 'high-low edge in excluded link')
    return {'degree_condition_types': 48, 'excluded_types': 1,
            'remaining_necessary_types': 47,
            'exclusion_uses_external_RGDD_theorem': True}


def mul4(a, b):
    # Polynomial multiplication over F2 reduced modulo X^2+X+1.
    value = 0
    while b:
        if b & 1:
            value ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return value


def affine_lines():
    lines = [frozenset(4 * x + (mul4(m, x) ^ c) for x in range(4))
             for m in range(4) for c in range(4)]
    lines += [frozenset(4 * x + y for y in range(4)) for x in range(4)]
    require(len(set(lines)) == 20 and all(len(line) == 4 for line in lines),
            'wrong affine lines')
    counts = Counter(pair for line in lines for pair in combinations(sorted(line), 2))
    require(set(counts) == set(combinations(range(16), 2)) and set(counts.values()) == {1},
            'affine construction does not cover all 120 pairs once')
    require(all(sum(v in line for line in lines) == 5 for v in range(16)),
            'wrong affine point replication')
    return sorted(lines, key=lambda line: tuple(sorted(line)))


def packing_leave(blocks):
    require(len(blocks) == len(set(blocks)) == 20, 'wrong quadruple count')
    require(all(len(b) == 4 and b <= set(range(17)) for b in blocks), 'bad quadruple')
    counts = Counter(pair for b in blocks for pair in combinations(sorted(b), 2))
    require(set(counts.values()) == {1} and len(counts) == 120, 'quadruples repeat a pair')
    require(min(8 - 2 * len(a & b) for a, b in combinations(blocks, 2)) == 6,
            'wrong baseline minimum distance')
    return set(combinations(range(17), 2)) - set(counts)


def affine_split_checks():
    lines = affine_lines()
    unsplit_leave = packing_leave(lines)
    require(unsplit_leave == {(v, 16) for v in range(16)}, 'wrong unused-point leave')
    origin_lines = [line for line in lines if 0 in line]
    require(len(origin_lines) == 5, 'wrong lines through origin')
    checked = 0
    partitions = Counter()
    for r in range(1, 5):
        for chosen in combinations(origin_lines, r):
            moved = set(chosen)
            blocks = [frozenset((line - {0}) | {16}) if line in moved else line
                      for line in lines]
            leave = packing_leave(blocks)
            require((0, 16) in leave and len(leave) == 16, 'wrong split leave')
            require(all(0 in e or 16 in e for e in leave), 'split has a low-low leave')
            for v in range(1, 16):
                require(int((0, v) in leave) + int((v, 16) in leave) == 1,
                        'split is not a double star')
                require(sum(v in b for b in blocks) == 5, 'bad low replication')
            require(sum(0 in b for b in blocks) == 5 - r and
                    sum(16 in b for b in blocks) == r, 'wrong split replications')
            merged = [frozenset((b - {16}) | {0}) if 16 in b else b for b in blocks]
            require(set(merged) == set(lines), 'inverse merge lost an affine line')
            checked += 1
            partitions['+'.join(map(str, sorted((r, 5 - r), reverse=True)))] += 1
    raw = (json.dumps([sorted(line) for line in lines], separators=(',', ':')) + '\n').encode()
    require(checked == 30, 'not all nonempty proper splits were checked')
    return {'affine_lines': 20, 'covered_pairs': 120, 'unused_point_baseline_words': 20,
            'unused_point_baseline_minimum_distance': 6, 'splits_checked': checked,
            'split_deficit_partitions': dict(sorted(partitions.items())),
            'all_inverse_merges_match': True, 'affine_lines_sha256': sha256(raw).hexdigest()}


def incumbent_merges():
    words = (HERE / 'baseline69.txt').read_text().splitlines()
    require(len(words) == 69, 'wrong incumbent')
    blocks = [frozenset(v for v, bit in enumerate(word) if bit == '1') for word in words]
    rows = []
    for x in range(18):
        star = [b - {x} for b in blocks if x in b]
        if len(star) != 20:
            continue
        counts = {v: sum(v in b for b in star) for v in range(18) if v != x}
        centers = [v for v, q in counts.items() if q < 5]
        if len(centers) != 2:
            continue
        a, b = centers
        merged = [frozenset((line - {b}) | {a}) if b in line else line for line in star]
        require(len(set(merged)) == 20 and all(len(line) == 4 for line in merged),
                'incumbent merge duplicates or shrinks a line')
        covered = Counter(pair for line in merged for pair in combinations(sorted(line), 2))
        active = set(range(18)) - {x, b}
        require(set(covered) == set(combinations(sorted(active), 2)) and
                set(covered.values()) == {1}, 'incumbent merge is not an affine plane')
        rows.append({'coordinate': x, 'merged_centers': centers,
                     'center_replications': [counts[v] for v in centers],
                     'affine_lines': 20, 'covered_pairs': len(covered)})
    require(len(rows) == 3, 'wrong number of degree-two saturated incumbent points')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    report = {'h14_four_point_carrier': four_point_carrier(),
              'weight_four_path_block_check': forced_path_blocks(),
              'filtered_local_catalog': filtered_catalog(),
              'affine_split': affine_split_checks(),
              'incumbent_degree_two_merges': incumbent_merges(),
              'external_RGDD_nonexistence_reproduced': False,
              'global_72_word_exclusion': False,
              'theorem_depends_on_computation': False}
    raw = (json.dumps(report, indent=2, sort_keys=True) + '\n').encode('ascii')
    if args.write_expected:
        (HERE / 'support15_expected.json').write_bytes(raw)
    else:
        require((HERE / 'support15_expected.json').read_bytes() == raw,
                'exact output differs from support15_expected.json')
    print(raw.decode('ascii'), end='')


if __name__ == '__main__':
    main()
