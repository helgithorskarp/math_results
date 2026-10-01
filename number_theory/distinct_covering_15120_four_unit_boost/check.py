"""Exact finite-period certificate; Python >=3.10, standard library only.

Actual author: six-covering-1, researcher. No solver or private search input.
"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
N, B, P = 15120, 2160, 7
MODULI = [m for m in range(8, N + 1) if N % m == 0]
BASE = [m for m in MODULI if m % P]
TAILS = [m for m in MODULI if m % P == 0]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode_input(data):
    require(data.get('period') == N and data.get('base_period') == B,
            'Wrong finite-period domain')
    rows = data.get('fixed_classes')
    require(isinstance(rows, list), 'Missing fixed classes')
    fixed = []
    for row in rows:
        require(isinstance(row, dict) and set(row) == {'modulus', 'phase'},
                'Malformed class')
        m, a = row['modulus'], row['phase']
        require(type(m) is int and type(a) is int and 0 <= a < m,
                'Noncanonical class')
        fixed.append((m, a))
    require([m for m, a in fixed] == BASE,
            'Every eligible non-seven modulus is prescribed exactly once')
    require(fixed[:2] == [(8, 5), (9, 6)], 'Wrong prescribed anchors')
    points = data.get('boost_points')
    require(isinstance(points, list) and len(points) == 4
            and all(type(z) is int and 0 <= z < B for z in points)
            and points == sorted(set(points)), 'Invalid four-point boost')
    return fixed, points


def phase_weights(w, m):
    # Literal physical phases, each evaluated by its arithmetic progression.
    return [sum(w[x] for x in range(a, N, m)) for a in range(m)]


def verify(data):
    fixed, points = decode_input(data)
    require(math.gcd(B, P) == 1 and N == B * P, 'Wrong prime-fibre domain')
    require(BASE == [m for m in range(8, B + 1) if B % m == 0]
            and len(BASE) == 34 and len(TAILS) == 39, 'Missing resource label')
    uncovered = [x for x in range(N) if all(x % m != a for m, a in fixed)]
    H = sorted({x % B for x in uncovered})
    Hset = set(H)
    require(uncovered == [x for x in range(N) if x % B in Hset],
            'Residual is not a complete union of prime fibres')
    require(all(z in Hset for z in points), 'Boost intersects a fixed class')
    uniform = [int(x % B in Hset) for x in range(N)]
    boosted = uniform[:]
    for z in points:
        for x in range(z, N, B):
            boosted[x] += 1
    require(all(boosted[x] == 0 for m, a in fixed for x in range(a, N, m)),
            'Weight meets a fixed class')
    events = hashlib.sha256()
    capacities = []
    profiles = []
    phase_count = 0
    for m in TAILS:
        record = {'modulus': m}
        for label, w in [('uniform', uniform), ('boosted', boosted)]:
            values = phase_weights(w, m)
            record[label] = max(values)
            for a, value in enumerate(values):
                events.update(f'{label}:{m}:{a}:{value}\n'.encode())
            phase_count += len(values)
            if label == 'uniform':
                d = m // P
                require(B % d == 0 and d >= 2
                        and all(values[a] == values[a % d] for a in range(m)),
                        'Physical phase profile does not equal its CRT projection')
                profiles.append((d, values[:d]))
        capacities.append(record)
    uniform_demand, boosted_demand = sum(uniform), sum(boosted)
    uniform_capacity = sum(row['uniform'] for row in capacities)
    boosted_capacity = sum(row['boosted'] for row in capacities)
    g = uniform_demand - uniform_capacity
    boosted_gap = boosted_demand - boosted_capacity
    require(boosted_gap > 0, 'Four-point weight is not strict')
    qplus = {z: 0 for z in H}
    qminus = {z: 0 for z in H}
    D2 = 0
    for d, values in profiles:
        M = max(values)
        peaks = values.count(M)
        if peaks == 1:
            S = max(v for v in values if v < M)
            D2 += min(2, M - S)
        elif peaks == 2:
            D2 += 1
        for z in H:
            if values[z % d] == M:
                qplus[z] += 1
                qminus[z] += int(peaks == 1)
    qplus_min, qminus_max = min(qplus.values()), max(qminus.values())
    singles = {'minus': g - P + qminus_max, 'plus': g + P - qplus_min}
    pairs = {'--': g - 2 * P + D2, '-+': g + qminus_max,
             '+-': g + qminus_max, '++': g + 2 * P - qplus_min}
    require(max(singles.values()) <= 0 and max(pairs.values()) <= 0,
            'Analytic signed one/two-unit nonseparation fails')
    lower_mass = len(points) - 1
    require(g + P * lower_mass <= 0,
            'A smaller nonnegative integer boost has not been excluded')
    require(boosted_demand == uniform_demand + P * len(points),
            'Wrong boost mass')
    return {
        'agent': 'six-covering-1', 'role': 'researcher',
        'status': 'SPECIFIED_BASE_EXCLUDED_BY_A_MINIMAL_FOUR_UNIT_POSITIVE_BOOST',
        'period': N, 'base_period': B, 'prime_fibre_size': P,
        'fixed_class_count': len(fixed), 'fixed_lcm': math.lcm(*BASE),
        'minimum_prescribed_modulus': min(BASE), 'unused_tail_labels': len(TAILS),
        'base_residual_points': len(H),
        'residual_sha256': hashlib.sha256(json.dumps(H, separators=(',', ':')).encode()).hexdigest(),
        'uniform_demand': uniform_demand, 'uniform_tail_capacity': uniform_capacity,
        'uniform_gap': g, 'minimum_qplus': qplus_min, 'maximum_qminus': qminus_max,
        'two_deletion_capacity_drop_bound': D2,
        'signed_single_gap_upper_bounds': singles,
        'signed_pair_gap_upper_bounds': pairs,
        'distinct_coordinate_signed_pairs_accounted': 4 * math.comb(len(H), 2),
        'signed_pair_enumeration_required': False,
        'boost_points': points, 'boosted_projected_mass': boosted_demand // P,
        'boosted_demand': boosted_demand, 'boosted_tail_capacity': boosted_capacity,
        'boosted_gap': boosted_gap, 'boosted_maximum_weight': max(boosted),
        'minimum_physical_holes': (boosted_gap + max(boosted) - 1) // max(boosted),
        'upper_gap_for_any_positive_integer_boost_of_mass_at_most_three': g + P * lower_mass,
        'minimum_positive_integer_added_mass_for_strict_separation': len(points),
        'physical_capacities': capacities, 'physical_phase_values': phase_count,
        'ordered_phase_sha256': events.hexdigest(),
        'scope': 'One prescribed34-class base at period15120. All39 tail phases or omissions. No whole-period exclusion, new cover or L_min(8) improvement.'
    }


def controls(data, expected):
    mutations = []
    wrong_period = copy.deepcopy(data)
    wrong_period['period'] = 10080
    mutations.append(wrong_period)
    omitted = copy.deepcopy(data)
    omitted['fixed_classes'].pop()
    mutations.append(omitted)
    duplicate = copy.deepcopy(data)
    duplicate['fixed_classes'][2] = duplicate['fixed_classes'][1]
    mutations.append(duplicate)
    phase = copy.deepcopy(data)
    phase['fixed_classes'][2]['phase'] = 10
    mutations.append(phase)
    overlap = copy.deepcopy(data)
    overlap['boost_points'][0] = 5
    mutations.append(overlap)
    repeated = copy.deepcopy(data)
    repeated['boost_points'][1] = repeated['boost_points'][0]
    mutations.append(repeated)
    for damaged in mutations:
        try:
            verify(damaged)
        except ValueError:
            continue
        raise ValueError('Malformed certificate accepted by a control')
    damaged_expected = copy.deepcopy(expected)
    damaged_expected['boosted_gap'] += 1
    require(verify(data) != damaged_expected, 'Changed expected gap was accepted')
    return len(mutations) + 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT / 'input.json').read_text())
    actual = verify(data)
    expected = json.loads((ROOT / 'expected.json').read_text())
    require(actual == expected, 'Exact output differs from expected.json')
    if args.controls:
        count = controls(data, expected)
        print(json.dumps({'controls_passed': count}, sort_keys=True))
    print(json.dumps(actual, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
