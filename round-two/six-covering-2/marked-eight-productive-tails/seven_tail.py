"""Complete exact arithmetic controls for marked seven-tail allocations.

Author: six-covering-2, researcher. No search tree, solver, or private input.
The ordinary allocation/essentiality bridges are stated in proof.md.
"""
import argparse
from itertools import combinations, product
import json
from math import gcd, lcm, prod
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def population(parent, modulus, phase):
    factors = ([1, 2, 3, 4, 5, 6, 7, 8],
               list(range(5)) if parent == 4 else [0, 2, 3, 4],
               [1, 2, 3, 5, 6] if parent == 4 else list(range(7)))
    powers = (gcd(modulus, 9), gcd(modulus, 5), gcd(modulus, 7))
    return prod(sum(y % q == phase % q for y in ys)
                for q, ys in zip(powers, factors))


def necessary(parent, extras, half_count, halves, quarters, union):
    active_h = sum(h != 0 for h in halves)
    active_q = sum(q != 0 for q in quarters)
    if parent == 2:
        if extras == 1:
            return half_count == 1 and active_h == 1
        if extras == 2:
            return active_h > 0 if half_count else active_q == 2
        if half_count >= 2:
            return active_h > 0
        return active_h > 0 or active_q >= 2
    if half_count == extras:
        return union == 15  # Placed32 is redundant at every covered hole.
    if extras == 2:
        return half_count == 1 and active_h == 1 and active_q == 1
    if extras == 3:
        return active_h > 0 if half_count else active_q == 3
    if half_count >= 2:
        return active_h > 0
    return active_h > 0 or active_q >= 3


def generate():
    ds = [d for d in range(1, 316) if 315 % d == 0]
    unused = ds[1:]
    capacity = {}
    for d in ds:
        a = (0 if d % 3 else 1) + (1 if d % 9 == 0 else 0)
        capacity[d] = (5, 3, 1)[a] * (1 if d % 5 == 0 else 5) * (1 if d % 7 == 0 else 6)
    sums = {str(n): [[*xs, sum(capacity[d] for d in xs)]
                     for xs in combinations(unused, n)] for n in range(1, 5)}
    intersections = {str(n): [[*xs, lcm(*xs), capacity[lcm(*xs)]]
                              for xs in combinations(unused, n)] for n in (2, 3)}
    pair_sums = [[*xs, sum(capacity[lcm(*p)] for p in combinations(xs, 2))]
                 for xs in combinations(unused, 3)]
    triple_sums = [[*xs, sum(capacity[lcm(*p)] for p in combinations(xs, 3))]
                   for xs in combinations(unused, 4)]
    require([max(r[-1] for r in sums[str(n)]) for n in range(1, 5)] == [90, 120, 150, 175],
            'Globally distinct extra16 capacities changed')
    require(max(r[-1] for r in pair_sums) == 54, 'Three-quarter pairwise union bound changed')
    require(max(r[-1] for r in intersections['2']) == 30 and
            max(r[-1] for r in intersections['3']) == 18, 'Quarter intersections changed')
    require(max(r[-1] for r in triple_sums) <= 72, 'Four-quarter triple-union bound changed')

    controls = []
    for parent, numbers in ((2, range(1, 4)), (6, range(2, 5))):
        placed = 5 if parent == 2 else 1
        for extras in numbers:
            for k in range(extras + 1):
                for hs in product((0, 5, 10), repeat=k):
                    for qs in product((0, 1, 2, 4, 8), repeat=extras-k):
                        union = 0
                        for x in (*hs, *qs):
                            union |= x
                        covered = (placed | union) == 15
                        condition = necessary(parent, extras, k, hs, qs, union)
                        require(not covered or condition, 'An inactive binary pattern violates its necessary footprint')
                        controls.append([parent, extras, k, list(hs), list(qs), covered, condition, union])

    # Every physical original-phase pair is retained, including same binary
    # halves and incompatible odd residues. CRT is the producer representation.
    phase_rows = []
    raw_blocks = []
    for parent in (1, 3, 4, 5, 7):
        for g, h in combinations(unused, 2):
            q = lcm(g, h)
            populations = [population(parent, q, a) for a in range(q)]
            phase_rows.append([parent, g, h, q, populations])
            common = gcd(g, h)
            inv = pow(g // common, -1, h // common)
            lookup = []
            for a in range(g):
                row = []
                for b in range(h):
                    if (b - a) % common:
                        row.append(0)
                    else:
                        t = (((b - a) // common) * inv) % (h // common)
                        row.append(populations[(a + g * t) % q])
                lookup.append(row)
            counts = []
            for a in range(parent, 16*g, 8):
                for b in range(parent, 16*h, 8):
                    counts.append(lookup[a % g][b % h] if (a-b) % 16 == 8 else 0)
            raw_blocks.append([parent, g, h, counts])
    third_max = {str(r): max(max(row[4]) for row in phase_rows if row[0] == r)
                 for r in (1, 3, 4, 5, 7)}
    require(third_max == {'1': 28, '3': 28, '4': 25, '5': 28, '7': 28},
            'Literal third-parent capacity changed')
    require(sum(len(row[3]) for row in raw_blocks) == 2698300,
            'Entire raw original phase-pair domain changed')

    cases = [
        ['2+5', 'H', 'HHHQ', 175], ['2+5', 'H', 'HHQQ', 150],
        ['2+5', 'H', 'HQQQ', 138], ['2+5', 'H', 'QQQQ', 162],
        ['3+4', 'HH', 'HHQ', 175], ['3+4', 'HH', 'HQQ', 150],
        ['3+4', 'HH', 'QQQ', 138], ['3+4', 'HQ', 'HHQ', 150],
        ['3+4', 'HQ', 'HQQ', 120], ['3+4', 'HQ', 'QQQ', 108],
        ['3+4', 'QQ', 'HHQ', 150], ['3+4', 'QQ', 'HQQ', 120],
        ['3+4', 'QQ', 'QQQ', 48],
        ['4+3', 'HHH', 'HQ', 175], ['4+3', 'HHQ', 'HQ', 150],
        ['4+3', 'HQQ', 'HQ', 150], ['4+3', 'QQQ', 'HQ', 144],
    ]
    for r in (1, 3, 4, 5, 7):
        cases.append(['2+3+2', 'H', 'HQ', r, 120 + third_max[str(r)]])
    require(max(row[-1] for row in cases) == 175, 'Complete seven-tail table changed')
    return {'agent': 'six-covering-2', 'role': 'researcher',
            'literal_prefix': [[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
            'essential_originals_explicit': [16,32], 'original_moduli_divide': 10080,
            'unused_odd_cofactors': unused, 'capacity_rows': [[d,capacity[d]] for d in ds],
            'globally_distinct_extra16_rows': sums, 'quarter_intersection_rows': intersections,
            'three_quarter_pair_sum_rows': pair_sums, 'four_quarter_triple_sum_rows': triple_sums,
            'complete_inactive_binary_controls': controls,
            'third_parent_all_odd_phase_rows': phase_rows,
            'third_parent_all_raw_original_phase_blocks': raw_blocks,
            'third_parent_maxima': third_max, 'raw_original_phase_pairs': 2698300,
            'complete_seven_tail_capacity_cases': cases, 'maximum_seven_tail_BASE_holes': 175,
            'capacity_175_is_claimed_sharp': False, 'ordinary_bridges_formalized': False,
            'independent_reviewer': False, 'global_bound_changed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    record = generate()
    args.out.write_text(json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({'seven_tail_capacity': record['maximum_seven_tail_BASE_holes'],
                      'raw_original_phase_pairs': record['raw_original_phase_pairs'],
                      'binary_controls': len(record['complete_inactive_binary_controls']),
                      'third_parent_maxima': record['third_parent_maxima']}))
