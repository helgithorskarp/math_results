"""Independent literal-residue controls for the written top-point lemma."""
import json
from collections import defaultdict
from itertools import product
from pathlib import Path
from time import monotonic
from distinct_top_points import prepare, charge, exact_budget


def require(condition, message):
    if not condition:
        raise ValueError(message)


def literal_charge(state, phases):
    # Scan ordinary progressions. No CRT resource active test is imported.
    hits = defaultdict(set)
    multiplicities = defaultdict(int)
    for n, a in phases.items():
        for x in range(a, state['N'], n):
            key = (x % state['B'] % state['T'], x % state['C'])
            hits[key].add(x % state['B'])
            multiplicities[key] += 1
    block_weights = {}
    for x in range(state['N']):
        key = (x % state['B'] % state['T'], x % state['C'])
        w = state['v'][x % state['Q']]
        require(key not in block_weights or block_weights[key] == w, 'Weight is not constant in a block')
        block_weights[key] = w
    actual_u = 0
    for x in range(state['N']):
        actual_u += state['u'][x] * sum(x % n == phases[n] for n in state['free'])
    sharp = actual_u + sum(len(points) * block_weights[key]
                           for key, points in hits.items() if len(points) >= 2)
    old = actual_u + sum(k * block_weights[key]
                         for key, k in multiplicities.items() if k >= 2)
    return sharp, old


def main():
    start = monotonic()
    fixtures = []
    for name, C, known, u in [
        ('three_resources', 9, [], [0] * 36),
        ('unrestricted_component', 9, [], [1] + [0] * 35),
        ('fixed_coarsest_positive_v', 9, [(4, 0)], [0] * 18 + [1] + [0] * 17),
        ('distinct_block_labels_required', 15, [], [0] * 60),
    ]:
        v = [1] + [0] * (2 * C - 1)
        state = prepare(4, C, 2, known, u, v)
        budget = exact_budget(state)
        require(charge(state, budget['attaining_phases']) == literal_charge(state, budget['attaining_phases']), 'Attaining physical charge')
        fixtures.append({'name': name, **budget})
    require([(f['sharp_budget'], f['multiplicity_budget']) for f in fixtures] ==
            [(2, 3), (4, 6), (4, 5), (2, 4)], 'Exact strict examples')
    # In the last fixture two independently optimized pairs each select q=0.
    # Their relaxed sum is4, but merging their equal labels leaves just2.
    require(fixtures[-1]['sharp_budget'] == 2, 'Distinct block labels cannot be dropped')

    # Exhaust every actual tuple again with ordinary progressions, including
    # point coincidences. The zero-weight blocks can be omitted exactly.
    tuples_checked = 0
    for fixture in fixtures:
        C = 15 if fixture['name'] == 'distinct_block_labels_required' else 9
        A = [(4, 0)] if fixture['name'] == 'fixed_coarsest_positive_v' else []
        u = [0] * (4 * C)
        if fixture['name'] == 'unrestricted_component':
            u[0] = 1
        if fixture['name'] == 'fixed_coarsest_positive_v':
            u[18] = 1
        state = prepare(4, C, 2, A, u, [1] + [0] * (2 * C - 1))
        physical_v = [state['v'][x % state['Q']] for x in range(state['N'])]
        literal_points = {}
        literal_u = {}
        for n in state['S']:
            for a in range(n):
                literal_points[n, a] = [x for x in range(a, state['N'], n) if physical_v[x]]
                literal_u[n, a] = sum(u[a::n])
        fixed = {n: a for n, a in A}
        maxima = [-1, -1]
        for values in product(*(range(n) for n in state['free'])):
            phases = fixed | dict(zip(state['free'], values))
            hits = defaultdict(set)
            counts = defaultdict(int)
            weights = {}
            for n, a in phases.items():
                for x in literal_points[n, a]:
                    key = (x % 4 % 2, x % C)
                    hits[key].add(x % 4)
                    counts[key] += 1
                    weights[key] = physical_v[x]
            ordinary = sum(literal_u[n, a] for n, a in phases.items() if n in state['free'])
            observed = (ordinary + sum(len(points) * weights[key] for key, points in hits.items() if len(points) >= 2),
                        ordinary + sum(k * weights[key] for key, k in counts.items() if k >= 2))
            require(charge(state, phases) == observed, 'Complete actual-tuple literal charge disagreement')
            maxima = [max(a, b) for a, b in zip(maxima, observed)]
            tuples_checked += 1
        require(maxima == [fixture['sharp_budget'], fixture['multiplicity_budget']], 'Independent maxima differ')

    composite_state = prepare(6, 5, 1, [], [0] * 30, [1, 0, 0, 0, 0])
    for a in range(6):
        for c in range(30):
            phases = {6: a, 30: c}
            require(charge(composite_state, phases) == literal_charge(composite_state, phases), 'Composite-radical tuple disagreement')
            tuples_checked += 1

    cover = [(2, 0), (3, 0), (4, 1), (6, 3), (12, 7), (9, 2), (18, 5), (36, 35)]
    require(all(any(x % n == a for n, a in cover) for x in range(36)), 'Genuine covering control')
    subsets = [cover[:i] for i in range(len(cover) + 1)] + [[cover[i]] for i in [2, 4, 7]]
    vectors = [[1] * 18, [x % 5 for x in range(18)]]
    vectors += [[int(x == j) for x in range(18)] for j in range(18)]
    positive = negative_demands = positive_known_top = 0
    for A in subsets:
        uncovered = [not any(x % n == a for n, a in A) for x in range(36)]
        for v in vectors:
            for mode in range(3):
                u = [int(uncovered[x]) * (1 if mode == 0 else (x % 7 if mode == 1 else int(x == 27))) for x in range(36)]
                state = prepare(4, 9, 2, A, u, v)
                phases = {n: a for n, a in cover if n in state['S']}
                observed = charge(state, phases)
                require(observed == literal_charge(state, phases), 'Full literal charge differs')
                known_outside = [(n, a) for n, a in A if n not in state['S']]
                actual_unused_outside = [(n, a) for n, a in cover if n not in state['S'] and n not in dict(A)]
                total = [u[x] + v[x % 18] for x in range(36)]
                known_cost = sum(sum(v[x % 18] for x in range(a, 36, n)) for n, a in known_outside)
                demand = sum(total) - known_cost
                actual_outside = sum(sum(total[a::n]) for n, a in actual_unused_outside)
                require(demand <= actual_outside + observed[0], 'False positive-control exclusion')
                positive += 1
                negative_demands += demand < 0
                positive_known_top += any(n in state['S'] and any(v[x % 18] for x in range(a, 36, n)) for n, a in A)
    require(negative_demands > 0 and positive_known_top > 0, 'Material known-footprint boundaries not exercised')

    # This genuine covering has actualLCM12, strictly less than ambientN60.
    # B12 has radical6, so this also exercises more than two block points.
    cover60 = [(2, 0), (3, 0), (4, 1), (6, 1), (12, 11)]
    require(all(any(x % n == a for n, a in cover60) for x in range(60)), 'Ambient-period control')
    for A in [[], [(12, 11)], cover60[:3], cover60]:
        for v in [[1] * 10] + [[int(x == j) for x in range(10)] for j in range(10)]:
            u = [int(not any(x % n == a for n, a in A)) * (x % 5) for x in range(60)]
            state = prepare(12, 5, 2, A, u, v)
            phases = {12: 11, 60: 0}
            observed = charge(state, phases)
            require(observed == literal_charge(state, phases), 'Composite-radical covering charge')
            total = [u[x] + v[x % 10] for x in range(60)]
            known_cost = sum(sum(v[x % 10] for x in range(a, 60, n)) for n, a in A if n not in state['S'])
            demand = sum(total) - known_cost
            actual_outside = sum(sum(total[a::n]) for n, a in cover60 if n not in state['S'] and n not in dict(A))
            require(demand <= actual_outside + observed[0], 'False smaller-actualLCM exclusion')
            positive += 1
            negative_demands += demand < 0
            positive_known_top += any(n in state['S'] and any(v[x % 10] for x in range(a, 60, n)) for n, a in A)

    rejected = 0
    for operation in [
        lambda: prepare(4, 9, 4, [], [0] * 36, [0] * 36),
        lambda: prepare(4, 9, 2, [(4, 0)], [1] + [0] * 35, [0] * 18),
        lambda: exact_budget(prepare(4, 15, 2, [], [0] * 60, [0] * 30), phase_cap=100),
        lambda: charge(prepare(4, 9, 2, [(4, 0)], [0] * 36, [0] * 18), {4: 1, 12: 0, 36: 0}),
    ]:
        try:
            operation()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('Malformed or incomplete control accepted')
    result = {'agent': 'six-covering-2', 'role': 'researcher', 'all_passed': True,
              'fixtures': fixtures, 'genuine_cover_weight_cases': positive,
              'complete_actual_tuples_checked': tuples_checked,
              'negative_effective_demands': negative_demands, 'positive_prescribed_top_cases': positive_known_top,
              'malformed_or_incomplete_rejections': rejected,
              'seconds': monotonic() - start,
              'scope': 'Written distinct-point charge with fixed top phases; no numerical L_min(8) improvement or practical solver implementation'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
