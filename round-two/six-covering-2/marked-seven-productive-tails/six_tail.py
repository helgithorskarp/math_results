"""Exact finite controls for the complete marked six-tail allocation proof."""
import json
from hashlib import sha256
from itertools import combinations, product
from math import lcm


def require(ok, message):
    if not ok:
        raise ValueError(message)


def audit():
    divisors = [d for d in range(1, 316) if 315 % d == 0]
    unused = divisors[1:]
    odd = {y for y in range(315) if y % 9 != 0 and y % 3 != 1 and y % 7 != 0}
    capacities = {d: max(sum(y % d == a for y in odd) for a in range(d))
                  for d in divisors}
    two_unused = [[a, b, capacities[a] + capacities[b]]
                  for a, b in combinations(unused, 2)]
    three_unused = [[a, b, c, capacities[a] + capacities[b] + capacities[c]]
                    for a, b, c in combinations(unused, 3)]
    two_quarters = [[a, b, lcm(a, b), capacities[lcm(a, b)]]
                    for a, b in combinations(unused, 2)]
    three_quarters = [[a, b, c, lcm(a, b, c), capacities[lcm(a, b, c)]]
                      for a, b, c in combinations(unused, 3)]
    require(max(r[-1] for r in two_unused) == 120, 'Two distinct 16-label bound')
    require(max(r[-1] for r in three_unused) == 150, 'Three distinct 16-label bound')
    require(max(r[-1] for r in two_quarters) == 30, 'Two distinct unused 32-label bound')
    require(max(r[-1] for r in three_quarters) == 18, 'Three distinct unused 32-label bound')

    # Inactive odd footprints are explicitly included as mask0.
    halves = (0, 5, 10)
    quarters = (0, 1, 2, 4, 8)
    controls = []
    for left, right in product(halves, repeat=2):
        if (1 | left | right) == 15:
            require((left | right) == 15, '32 not redundant with two extra16 classes')
        controls.append(['32+two16', left, right, (1 | left | right) == 15])
    for triple in product(halves, repeat=3):
        union = triple[0] | triple[1] | triple[2]
        if (1 | union) == 15:
            require(union == 15, '32 not redundant with three extra16 classes')
        controls.append(['32+three16', list(triple), (1 | union) == 15])
    for half, quarter in product(halves, quarters):
        if (5 | half | quarter) == 15:
            require(half != 0, 'Three-tail parent2 misses an extra16 footprint')
        if (1 | half | quarter) == 15:
            require(half != 0 and quarter != 0, 'Three-tail parent6 inactive required class')
        controls.append(['three-tail-mixed', half, quarter,
                         (5 | half | quarter) == 15, (1 | half | quarter) == 15])
    for a, b, quarter in product(halves, halves, quarters):
        if (1 | a | b | quarter) == 15:
            require(a != 0 or b != 0, 'Four-tail parent6 lacks an active16 footprint')
        controls.append(['four-tail-two16', a, b, quarter,
                         (1 | a | b | quarter) == 15])
    for half, a, b in product(halves, quarters, quarters):
        if (1 | half | a | b) == 15:
            require(half != 0, 'Four-tail mixed parent6 lacks its16 footprint')
        controls.append(['four-tail-one16', half, a, b, (1 | half | a | b) == 15])
    for a, b in product(quarters, repeat=2):
        if (5 | a | b) == 15:
            require(a != 0 and b != 0, 'Three-tail parent2 inactive quarter')
        controls.append(['parent2-two32', a, b, (5 | a | b) == 15])
    for triple in product(quarters, repeat=3):
        union = triple[0] | triple[1] | triple[2]
        if (1 | union) == 15:
            require(all(triple), 'Four-tail parent6 inactive required quarter')
        controls.append(['parent6-three32', list(triple), (1 | union) == 15])

    # Sharp abstract150-hole model: two disjoint odd footprints in parent2.
    left = {y for y in odd if y % 3 == 2 or y % 9 == 3}
    right = {y for y in odd if y % 5 == 0}
    require((len(left), len(right)) == (120, 30), 'Wrong abstract six-tail footprint')
    tails = ((16, 2), (32, 6), (48, 26), (144, 138), (80, 30), (160, 150))
    require(len({m for m, a in tails}) == 6 and all(10080 % m == 0 for m, a in tails),
            'Original labels collide in abstract model')
    points = {x for x in range(10080)
              if (x % 8 == 2 and x % 315 in left) or
                 (x % 8 == 6 and x % 315 in right)}
    require(len(points) == 600, 'Wrong150-hole physical lifts')
    covered = {x: [m for m, a in tails if x % m == a] for x in points}
    require(all(covered.values()), 'A literal six-tail model lift is uncovered')
    exclusive = {m: min(x for x in points if covered[x] == [m]) for m, a in tails}
    require(len(exclusive) == 6, 'Abstract six-tail resource redundant')
    digest = lambda data: sha256(json.dumps(data, separators=(',', ':')).encode()).hexdigest()
    return {'agent': 'six-covering-2', 'role': 'researcher',
            'domain': 'literal H16two28four32six; essential original16/32',
            'six_tail_allocation_cases': [
                ['parents2+4', 'other-parent6-types:two16+one32', 150],
                ['parents2+4', 'other-parent6-types:one16+two32', 120],
                ['parents2+4', 'other-parent6-types:three32', 108],
                ['parents3+3', 'other-parent2-types:two16', 150],
                ['parents3+3', 'other-parent2-types:one16+one32', 120],
                ['parents3+3', 'other-parent2-types:two32', 120]],
            'two_unused_16_rows': two_unused, 'three_unused_16_rows': three_unused,
            'two_unused_32_rows': two_quarters, 'three_unused_32_rows': three_quarters,
            'all_capacity_rows_sha256': digest([two_unused, three_unused, two_quarters, three_quarters]),
            'complete_binary_controls': controls, 'binary_controls': len(controls),
            'binary_controls_sha256': digest(controls),
            'abstract_model_original_TAILs': tails, 'abstract_model_sizes': [120, 30],
            'abstract_model_literal_lifts': len(points), 'abstract_model_exclusive_witnesses': exclusive,
            'maximum_six_tail_BASE_holes': 150, 'abstract_model_is_full_cover': False,
            'independent_reviewer': False, 'ordinary_complete_classification_formalized': False,
            'global_bound_changed': False}


if __name__ == '__main__':
    print(json.dumps(audit(), sort_keys=True))
