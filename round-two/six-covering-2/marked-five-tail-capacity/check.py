"""Exact footprint capacity for the five-productive-TAIL H32six face.

This checks a finite capacity reduction, not a full covering exclusion.
The ordinary essential-resource and complete five-TAIL classification proofs
are separate. No discovery/solver/old numerical capacity table is imported.
"""
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from math import lcm

BASE = ((8, 0), (9, 0), (10, 1), (14, 0), (12, 10), (28, 4))
D = tuple(d for d in range(1, 316) if 315 % d == 0)
UNUSED = D[1:]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def allocation(g, e, f):
    require(all(type(d) is int and d in UNUSED for d in (g, e, f)),
            'Invalid original odd label')
    labels = (16, 32, 16 * g, 16 * e, 32 * f)
    require(len(set(labels)) == 5 and all(10080 % m == 0 for m in labels),
            'Globally shared original label repeated')
    return labels


def audit():
    require(D == (1, 3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315),
            'Incomplete original odd divisors')
    odd_holes = {y for y in range(315) if y % 9 != 0 and y % 3 != 1 and y % 7 != 0}
    require(len(odd_holes) == 150, 'Wrong initial odd BASE shadow')
    counts = {}
    for d in D:
        histogram = Counter(y % d for y in odd_holes)
        counts[d] = [histogram[a] for a in range(d)]
    physical_records = []
    full_phase_records = 0
    for r in (2, 6):
        holes = {x for x in range(r, 2520, 8)
                 if all(x % m != a for m, a in BASE)}
        require(len(holes) == 150 and {x % 315 for x in holes} == odd_holes,
                'Literal physical BASE parent differs from odd shadow')
        for d in D:
            phases = []
            literal_counts = []
            for a in range(d):
                phase = (r + 8 * (((a - r) * pow(8, -1, d)) % d)) % (8 * d) if d > 1 else r
                require(phase % 8 == r and phase % d == a, 'Wrong original footprint phase')
                phases.append(phase)
                literal_counts.append(len(holes.intersection(range(phase, 2520, 8 * d))))
                full_phase_records += 1
            require(len(set(phases)) == d and literal_counts == counts[d],
                    'Every physical original phase must match independently')
            physical_records.append([r, d, phases, literal_counts])
    capacity = {d: max(values) for d, values in counts.items()}
    require(capacity == {1: 150, 3: 90, 5: 30, 7: 25, 9: 30, 15: 18,
                         21: 15, 35: 5, 45: 6, 63: 5, 105: 3, 315: 1},
            'Whole footprint capacity table changed')

    # Fixed original16 in parent2 occupies alternate binary slots0/2.
    # Fixed original32 in parent6 occupies binary slot0.
    halves = (5, 10)
    quarters = (1, 2, 4, 8)
    two_tail_controls = []
    for kind, mask in [('16', m) for m in halves] + [('32', m) for m in quarters]:
        covers = (5 | mask) == 15
        require(not covers or (kind == '16' and mask == 10),
                'False two-TAIL parent classification')
        two_tail_controls.append([kind, mask, covers])
    three_tail_controls = []
    for kind_a, mask_a in [('16', m) for m in halves] + [('32', m) for m in quarters]:
        for kind_b, mask_b in [('16', m) for m in halves] + [('32', m) for m in quarters]:
            covers = (1 | mask_a | mask_b) == 15
            redundant32 = (mask_a | mask_b) == 15
            allowed = covers and not redundant32
            require(not allowed or sorted((kind_a, kind_b)) == ['16', '32'],
                    'False essential32 three-TAIL type classification')
            if allowed:
                require(sorted((mask_a, mask_b)) == [4, 10],
                        'False essential32 binary phases')
            three_tail_controls.append([kind_a, mask_a, kind_b, mask_b,
                                        covers, redundant32, allowed])
    rows = []
    for g, e, f in product(UNUSED, repeat=3):
        if g == e:
            continue
        labels = allocation(g, e, f)
        q = lcm(e, f)
        rows.append([g, e, f, list(labels), q, capacity[g], capacity[q],
                     capacity[g] + capacity[q]])
    require(len(rows) == 1210, 'Incomplete globally shared original allocation family')
    maximum = max(row[-1] for row in rows)
    require(maximum == 120, 'Wrong entire five-TAIL face capacity')
    achievers = [row for row in rows if row[-1] == maximum]
    require(any(row[:3] == [3, 5, 5] for row in achievers), 'Abstract sharpness control missing')
    # This witness realizes the capacity sets; it is not a full BASE/TAIL cover.
    abstract_left = {y for y in odd_holes if y % 3 == 2}
    abstract_right = {y for y in odd_holes if y % 5 == 0}
    require((len(abstract_left), len(abstract_right)) == (90, 30),
            'Abstract footprint witness changed')
    model_tail = ((16, 2), (32, 6), (48, 26), (80, 30), (160, 150))
    model_points = {x for x in range(10080)
                    if (x % 8 == 2 and x % 315 in abstract_left) or
                       (x % 8 == 6 and x % 315 in abstract_right)}
    require(len(model_points) == 480, 'Wrong abstract four-lift model')
    coverage = {x: [m for m, a in model_tail if x % m == a] for x in model_points}
    require(all(coverage.values()), 'Literal original tails miss an abstract lift')
    essential_witnesses = {m: min(x for x in model_points if coverage[x] == [m])
                           for m, a in model_tail}
    require(len(essential_witnesses) == 5, 'Abstract model resource is redundant')
    rejected = 0
    for bad in ((3, 3, 5), (1, 3, 5), (3, 5, 1), (True, 5, 5), (3, 2, 5)):
        try:
            allocation(*bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('Malformed/shared-label allocation accepted')
    require(rejected == 5 and maximum > 119, 'Damage/strict-bound controls failed')
    digest = lambda data: sha256(json.dumps(data, separators=(',', ':')).encode()).hexdigest()
    return {'agent': 'six-covering-2', 'role': 'researcher', 'period': 10080,
            'domain': 'H16two28four32six; essential original16/32; exactly five productive TAILs',
            'original_BASE_prefix': BASE, 'parents': [2, 6], 'initial_shadow_points_per_parent': 150,
            'odd_divisors': D, 'odd_phase_populations': counts, 'capacity': capacity,
            'physical_records': physical_records, 'physical_phase_records': full_phase_records,
            'two_tail_binary_controls': two_tail_controls,
            'essential32_three_tail_binary_controls': three_tail_controls,
            'allocation_rows': rows, 'allocations': len(rows), 'maximum': maximum,
            'maximizing_allocations': achievers,
            'physical_phase_records_sha256': digest(physical_records),
            'allocation_records_sha256': digest(rows), 'bad_allocations_rejected': rejected,
            'abstract_witness_sizes': [90, 30], 'BASE_hole_threshold_for_at_least_six_TAIL': 121,
            'abstract_model_original_TAILs': model_tail,
            'abstract_model_literal_physical_lifts': len(model_points),
            'abstract_model_exclusive_witnesses': essential_witnesses,
            'abstract_sharpness_is_cover_witness': False, 'all_remaining_covers_excluded': False,
            'P127_or_P161_numerical_table_imported': False,
            'other_old_negative_roots_imported': False, 'independent_reviewer': False,
            'ordinary_classification_formalized': False, 'global_bound_changed': False}


if __name__ == '__main__':
    print(json.dumps(audit(), sort_keys=True))
