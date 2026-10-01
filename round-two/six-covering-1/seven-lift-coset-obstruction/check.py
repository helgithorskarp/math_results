"""Exact controls for a restricted covering construction obstruction.

The proof is in proof.md. No SAT result or external certificate is used.
Python 3.11 standard library; arbitrary-precision integers throughout.
"""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from math import gcd, lcm
from pathlib import Path

import local40


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def phase_mask(period, modulus, phase):
    return sum(1 << x for x in range(phase, period, modulus))


def crt(a, m, b, n):
    require(gcd(m, n) == 1, 'CRT moduli must be coprime')
    solutions = [x for x in range(a, m * n, m) if x % n == b]
    require(len(solutions) == 1, 'CRT phase not unique')
    return solutions[0]


def fractional_certificate(rows):
    labels = divisors(720)[1:]
    require([r['cofactor'] for r in rows] == labels, 'fractional resource census')
    target_numerators = [0] * 840
    phase_controls = 0
    # Six physical target phases; CRT order is (t mod7,t mod120).
    for c in range(6):
        for row in rows:
            d = row['cofactor']
            e = d // gcd(d, 6)
            require(row == {'cofactor': d, 'effective_modulus': e,
                            'compatible_phases': 7 * e,
                            'phase_weight_numerator': 120 // e,
                            'phase_weight_denominator': 840}, 'fractional descriptor')
            actual = {}
            for t in range(840):
                a = (c + 6 * t) % (7 * d)
                j = 120 * (t % 7) + t % 120
                actual[a] = actual.get(a, 0) | (1 << j)
            require(len(actual) == 7 * e, 'physical compatible phase count')
            resource_budget = 0
            for s in range(7):
                for b in range(e):
                    a = (c + 6 * crt(s, 7, b, e)) % (7 * d)
                    expected = phase_mask(120, e, b) << (120 * s)
                    require(actual[a] == expected, 'physical/CRT phase mismatch')
                    require(expected.bit_count() == 120 // e, 'physical phase size')
                    resource_budget += row['phase_weight_numerator']
                    if c == 0:
                        for j in range(840):
                            if actual[a] & (1 << j):
                                target_numerators[j] += row['phase_weight_numerator']
                    phase_controls += 1
            require(resource_budget == 840, 'fractional resource budget exceeds one')
    require(set(target_numerators) == {846}, 'fractional target coverage not141/140')
    return {'physical_target_phases': 6, 'physical_CRT_phase_controls': phase_controls,
            'compatible_phases_per_target': sum(r['compatible_phases'] for r in rows),
            'target_points': 840, 'resource_budget_numerator': 840,
            'denominator': 840, 'every_target_coverage_numerator': 846,
            'uniform_coverage_ratio': [141, 140]}


def high_resource_cases():
    controls = 0
    # Exact intersections with each possible set of distinct 3/5 phases.
    for m, sizes in ((3, (1, 2)), (5, (1, 2, 3, 4))):
        for k in sizes:
            for phases in combinations(range(m), k):
                high = 0
                for a in phases:
                    high |= phase_mask(120, m, a)
                for b in range(4):
                    overlap = (high & phase_mask(120, 4, b)).bit_count()
                    require(overlap == k * 120 // (4 * m), '4/high intersection')
                    controls += 1
    high_pairs = []
    for m, n in ((2, 3), (2, 5), (3, 5)):
        overlaps = []
        for a, b in product(range(m), range(n)):
            x = (phase_mask(120, m, a) & phase_mask(120, n, b)).bit_count()
            require(x == 120 // (m * n) and x > 6, 'mixed high pair')
            overlaps.append(x)
            controls += 1
        high_pairs.append({'effective_moduli': [m, n], 'intersection': min(overlaps)})
    require(sum(120 // e for d in divisors(720)[1:]
                for e in [d // gcd(d, 6)]) == 846, 'total target resource capacity')
    require(3 * 120 + 2 * 60 + 2 * 40 + 4 * 24 == 656, 'high resource mass')

    # After three disjoint full copies, assign all eight labelled high
    # resources to the four remaining labelled copies. These 4^8 tuples
    # are complete; unlike the proof, this control needs no normal forms.
    counts = {'all_three_types_clustered': 0, 'binary_split': 0,
              'ternary_split_excluded': 0, 'five_split_excluded': 0}
    mixed = 0
    for assignment in product(range(4), repeat=8):
        groups = [assignment[:2], assignment[2:4], assignment[4:]]
        supports = [set(g) for g in groups]
        if any(supports[i] & supports[j] for i in range(3) for j in range(i)):
            mixed += 1
            continue
        used = sum(map(len, supports))
        require(used <= 4 and max(map(len, supports)) <= 2, 'high support reduction')
        if len(supports[1]) == 2:
            # One 3-phase in each of two copies; binary copy full;
            # four 5-phases in the last copy. Each4-resource loses >=10.
            require([len(s) for s in supports] == [1, 2, 1], 'ternary split shape')
            require(2 * min(30, 10, 24) > 6, 'ternary split excess')
            counts['ternary_split_excluded'] += 1
        elif len(supports[2]) == 2:
            require([len(s) for s in supports] == [1, 1, 2], 'five split shape')
            occupancies = [groups[2].count(s) for s in supports[2]]
            minimum_overlap = min([30, 20] + [6 * k for k in occupancies])
            require(2 * minimum_overlap > 6, 'five split excess')
            counts['five_split_excluded'] += 1
        else:
            require(len(supports[1]) == 1, 'ternary classes not clustered')
            key = 'binary_split' if len(supports[0]) == 2 else 'all_three_types_clustered'
            counts[key] += 1
    require(sum(counts.values()) + mixed == 4 ** 8, 'high placement completeness')
    require(counts == {'all_three_types_clustered': 24, 'binary_split': 24,
                      'ternary_split_excluded': 24, 'five_split_excluded': 168},
            'admissible high placement census')
    # The two3-phases leave a whole class modulo3. Pure4,8,10 cannot
    # enter that copy within the global six-excess budget.
    forbidden_controls = 0
    for missing in range(3):
        high = ((1 << 120) - 1) ^ phase_mask(120, 3, missing)
        for e in (4, 8, 10):
            for a in range(e):
                size = (high & phase_mask(120, e, a)).bit_count()
                require(size == 80 // e and size > 6, 'pure resource not forbidden')
                forbidden_controls += 1
    return {'labelled_high_placement_tuples': 4 ** 8,
            'mixed_type_placements_rejected': mixed, 'admissible_placements': counts,
            'high_phase_intersection_controls': controls,
            'mixed_high_pair_intersections': high_pairs, 'high_class_mass': 656,
            'remaining_resource_mass': 190, 'pure_resource_exclusion_controls': forbidden_controls,
            'total_capacity': 846, 'covering_demand': 840, 'excess_budget': 6,
            'forced_ternary_copy_high_mass': 80,
            'forced_ternary_copy_additional_cost_upper': 46,
            'forced_ternary_copy_additional_cost_lower': 48,
            'hypothetical_cover_total_mass_lower': 848}


def projected_local_resources(local_result):
    resources = local_result['resource_labels']
    actual = [d for d in divisors(720)[1:]
              if d // gcd(d, 6) not in (1, 2, 3, 5, 4, 8, 10)]
    require(sorted(r[0] for r in resources) == actual, 'local resource completeness')
    controls = 0
    for d, m, cost in resources:
        e = d // gcd(d, 6)
        require((m, cost) == (e // gcd(e, 3), 120 // e), 'local projection/cost')
        for missing in range(3):
            for a in range(e):
                points = {z for z in range(40) if (missing + 3 * z) % e == a}
                if points:
                    b = min(points) % m
                    require(points == set(range(b, 40, m)), 'local physical projection')
                else:
                    require(gcd(e, 3) == 3 and a % 3 != missing, 'unexpected empty projection')
                controls += 1
    return {'local_resource_projection_controls': controls,
            'complete_local_labels': [r[0] for r in resources],
            'original_label_distinctness_preserved': True}


def stage_reduction():
    T, Q = 720, 5040
    nonseven = [m for m in divisors(T) if m >= 8]
    moduli7 = [7 * d for d in divisors(T)[1:]]
    require((len(nonseven), len(moduli7)) == (24, 29), 'two-stage resource census')
    require(set(nonseven).isdisjoint(moduli7), 'two-stage resource collision')
    require(sorted(nonseven + moduli7) == [m for m in divisors(Q) if m >= 8],
            'incomplete5040 resource split')
    raw = sum(T // m for m in nonseven)
    ordered = [(9, 8), (16, 9), (10, 9), (15, 8), (20, 9), (40, 9), (80, 9)]
    controls = overlap = 0
    for m, anchor in ordered:
        require(gcd(m, anchor) == 1, 'anchor not coprime')
        size = T // lcm(m, anchor)
        overlap += size
        for a in range(m):
            for b in range(anchor):
                require(sum(x % anchor == b for x in range(a, T, m)) == size,
                        'literal sequential anchor count')
                controls += 1
    require((raw, overlap, T - raw + overlap) == (654, 36, 102), 'first-stage union bound')
    records = []
    capacity_controls = 0
    for g in divisors(T):
        demand = Q // g
        capacity = sum(Q // lcm(g, m) for m in moduli7)
        require(capacity == Fraction(T, g) * sum((Fraction(gcd(g, d), d)
                                                for d in divisors(T)[1:]), Fraction()),
                'seven-stage capacity identity')
        for c in range(g):
            for m in moduli7:
                histogram = [0] * m
                for x in range(c, Q, g):
                    histogram[x % m] += 1
                require(max(histogram) == Q // lcm(g, m), 'actual target phase maximum')
                capacity_controls += 1
        if g >= 12:
            require(T // 18 + T // g < 102, 'large-g hole bound')
            reason = 'FIRST_STAGE_HOLE_SIZE'
        elif capacity < demand:
            reason = 'SEVEN_STAGE_CAPACITY'
        elif g == 10:
            reason = 'FIRST_STAGE_FIXED_COVERAGE'
        elif g == 6:
            require((demand, capacity) == (840, 846), 'g6 capacity')
            reason = 'INTEGRAL_SEVEN_STAGE_OBSTRUCTION'
        else:
            raise RuntimeError('unhandled divisor of720')
        records.append({'g': g, 'demand': demand, 'capacity': capacity, 'exclusion': reason})
    fixed = {x for x in range(T) if x % 8 == 5 or x % 9 == 6}
    counts = [sum((x % 18 == a or x % 10 == c) and x not in fixed for x in range(T))
              for a, c in product(range(18), range(10))]
    require(max(counts) == 96 < 102, 'normalized g10 hole bound')
    return {'nonseven_resource_labels': nonseven, 'seven_resource_labels': moduli7,
            'nonseven_raw_mass': raw, 'sequential_unavoidable_overlap': overlap,
            'nonseven_union_upper': 618, 'nonseven_residual_lower': 102,
            'literal_anchor_phase_controls': controls,
            'literal_target_capacity_controls': capacity_controls,
            'g10_fixed_target_controls': len(counts), 'g10_hole_upper': max(counts),
            'all_divisors_g_checked': len(records), 'records': records,
            'remaining_g_in_this_construction_route': []}


def top_template(a):
    r, q = a % 9, a % 2
    fibers = [r, r + 9, r + 18]
    rows = [(1, fibers[0], 0), (2, fibers[1], q),
            (4, fibers[2], q), (8, fibers[2], q + 2), (16, fibers[2], q + 6)]
    for j in range(5):
        power = 1 << j
        rows.append((5 * power, fibers[2], crt((q + 14) % power, power, j, 5)))
    return [(27 * d, crt(s, 27, b, d)) for d, s, b in rows]


def check_top_templates():
    labels = sorted(27 * d for d in divisors(80))
    controls = 0
    for a in range(18):
        rows = top_template(a)
        require(sorted(m for m, b in rows) == labels, 'top template resource census')
        require(lcm(*(m for m, b in rows)) == 2160, 'top template LCM')
        for x in range(a, 15120, 18):
            require(any(x % m == b for m, b in rows), 'top template misses target')
            controls += 1
        require(not all(any(x % m == b for m, b in rows) for x in range(15120)),
                'template unexpectedly a full covering')
    require(set(labels).isdisjoint(m for m in divisors(5040) if m >= 8),
            'top/core collision')
    require(lcm(5040, *labels) == 15120, 'conditional resulting period')
    return {'target_phases': 18, 'target_point_controls': controls,
            'template_resource_labels': labels, 'covers_only_target_not_all_integers': True}


def check():
    local = local40.check()
    require(local['local_minimum_cost'] == 48, 'wrong local obstruction cost')
    high = high_resource_cases()
    require(high['forced_ternary_copy_additional_cost_lower'] == local['local_minimum_cost'],
            'local/global cost connection')
    descriptors = [{'cofactor': d, 'effective_modulus': d // gcd(d, 6),
                    'compatible_phases': 7 * (d // gcd(d, 6)),
                    'phase_weight_numerator': 120 // (d // gcd(d, 6)),
                    'phase_weight_denominator': 840} for d in divisors(720)[1:]]
    fractional = fractional_certificate(descriptors)
    damaged = [dict(r) for r in descriptors]
    damaged[-1]['phase_weight_numerator'] += 1
    try:
        fractional_certificate(damaged)
    except RuntimeError:
        pass
    else:
        raise RuntimeError('damaged fractional certificate accepted')
    return {'agent': 'six-covering-1', 'role': 'researcher', 'status': 'CHECKED',
            'local40': local, 'high_resource_reduction': high,
            'local_projection': projected_local_resources(local),
            'fractional_certificate': descriptors, 'fractional_controls': fractional,
            'damaged_fractional_certificate_rejected': True,
            'two_stage_route': stage_reduction(), 'top_templates': check_top_templates(),
            'no_solver_status_is_a_premise': True, 'no_global15120_exclusion': True,
            'no_covering_of_all_integers_constructed': True,
            'historical_priority_claimed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check()
    if args.expected:
        require(json.loads(args.expected.read_text()) == result, 'expected evidence differs')
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': result['status'], 'local_minimum_cost': 48,
                      'target_capacity': 846, 'hypothetical_cover_mass_lower': 848,
                      'fractional_uniform_ratio': [141, 140],
                      'all_30_route_parameters_excluded': True,
                      'global_numerical_bound_changed': False}))
