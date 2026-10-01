"""Sharp local cost48 lemma; no SAT status is a premise."""
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def mask(m, a):
    return sum(1 << x for x in range(a, 40, m))


def duplicate_mass(rows):
    covered = 0
    mass = 0
    for m, a in rows:
        covered |= mask(m, a)
        mass += 40 // m
    return mass - covered.bit_count()


def check():
    # Label, projected modulus, full original class cost.
    resources = [(36, 2, 20), (72, 4, 10), (144, 8, 5),
                 (45, 5, 8), (90, 5, 8), (180, 10, 4),
                 (360, 20, 2), (720, 40, 1),
                 (40, 20, 6), (120, 20, 6),
                 (80, 40, 3), (240, 40, 3)]
    controls = 0
    for a4, a5, b5 in product(range(4), range(5), range(5)):
        require(duplicate_mass([(4, a4), (5, a5), (5, b5)]) >= 4,
                'four/two-five overlap lemma')
        controls += 1
    for a2, a5, b5 in product(range(2), range(5), range(5)):
        require(duplicate_mass([(2, a2), (5, a5), (5, b5)]) >= 8,
                'two/two-five overlap lemma')
        controls += 1
    for a2, a5 in product(range(2), range(5)):
        require(duplicate_mass([(2, a2), (5, a5)]) >= 4, 'two/five overlap')
        controls += 1
    for a2, a4, a5, a8, a10 in product(range(2), range(4), range(5),
                                      [None] + list(range(8)), [None] + list(range(10))):
        rows = [(2, a2), (4, a4), (5, a5)]
        bound = 6
        if a8 is not None:
            rows.append((8, a8)); bound += 1
        if a10 is not None:
            rows.append((10, a10)); bound += 2
        require(duplicate_mass(rows) >= bound, 'one-five incremental overlap')
        controls += 1
    for a2, a4, a10 in product(range(2), range(4), range(10)):
        require(duplicate_mass([(2, a2), (4, a4), (10, a10)]) >= 2,
                'two/four/ten overlap')
        controls += 1
    binary_controls = terminal_controls = 0
    terminal_costs = [4, 2, 1, 6, 6, 3, 3]
    require(sum(sorted(terminal_costs)[:5]) == 13, 'five-terminal minimum cost')
    for a2, a4, a8 in product(range(2), range(4), range(8)):
        rows = [(2, a2), (4, a4), (8, a8)]
        dup = duplicate_mass(rows)
        require(dup == 0 or dup >= 5, 'binary union cases')
        binary_controls += 1
        if dup == 0:
            covered = mask(2, a2) | mask(4, a4) | mask(8, a8)
            missing = ((1 << 40) - 1) ^ covered
            require(missing.bit_count() == 5, 'binary residual size')
            a = next(x for x in range(40) if missing & (1 << x))
            require(missing == mask(8, a % 8), 'binary residual is not an8-coset')
            for m in (10, 20, 40):
                for phase in range(m):
                    require((mask(m, phase) & missing).bit_count() <= 1,
                            'terminal contributes more than one point')
                    terminal_controls += 1

    # All4096 resource subsets are handled by complete phase-independent
    # cases. The literal lemmas above certify the bounds used in each case.
    budget_subsets = density_rejections = bounded_rejections = terminal_rejections = 0
    for bits in range(1 << len(resources)):
        selected = [j for j in range(len(resources)) if bits & (1 << j)]
        cost = sum(resources[j][2] for j in selected)
        if cost > 47:
            continue
        budget_subsets += 1
        cardinality = sum(40 // resources[j][1] for j in selected)
        if cardinality < 40:
            density_rejections += 1
            continue
        has = lambda j: j in selected
        fives = int(has(3)) + int(has(4))
        if not has(0):
            require(has(1) and fives == 2, 'no-two case premises')
            bound = cardinality - 4
        elif fives == 2:
            bound = cardinality - 8
        elif fives == 1:
            if has(1):
                bound = cardinality - 6 - int(has(2)) - 2 * int(has(5))
            else:
                bound = cardinality - 4
        elif not has(1):
            bound = cardinality
        elif not has(2):
            bound = cardinality - (2 if has(5) else 0)
        else:
            # Non-disjoint binary phases lose at least5. Disjoint binary
            # phases leave five points, each terminal covers at most one.
            require(cardinality - 5 < 40, 'non-disjoint binary bound')
            terminals = [j for j in selected if j not in (0, 1, 2)]
            require(len(terminals) <= 4, 'five terminals fit below48cost')
            terminal_rejections += 1
            continue
        require(bound < 40, ('subset phase-union bound fails', selected, cost, bound))
        bounded_rejections += 1

    witness = [(0, 0), (1, 1), (2, 3), (5, 7), (6, 15),
               (7, 23), (10, 31), (11, 39)]
    covered = 0
    total_cost = 0
    for j, a in witness:
        d, m, cost = resources[j]
        covered |= mask(m, a)
        total_cost += cost
    require(covered == (1 << 40) - 1 and total_cost == 48, 'sharp48cost cover')
    damaged = witness[:-1] + [(11, 31)]
    bad = 0
    for j, a in damaged:
        bad |= mask(resources[j][1], a)
    require(bad != (1 << 40) - 1, 'damaged local witness accepted')
    return {'status': 'CHECKED', 'local_minimum_cost': 48,
            'resource_labels': [list(row) for row in resources], 'phase_overlap_controls': controls,
            'binary_phase_controls': binary_controls,
            'terminal_phase_controls': terminal_controls,
            'resource_subsets': 4096, 'budget47_subsets': budget_subsets,
            'density_rejections': density_rejections,
            'phase_bound_rejections': bounded_rejections,
            'five-terminal_rejections': terminal_rejections,
            'sharp_witness': [{'resource': resources[j][0], 'projected_modulus': resources[j][1],
                               'phase': a, 'cost': resources[j][2]} for j, a in witness],
            'sharp_witness_is_only_local': True, 'damaged_witness_rejected': True,
            'no_sat_status_used': True}


if __name__ == '__main__':
    result = check()
    print(json.dumps({k: v for k, v in result.items() if k not in ('resource_labels', 'sharp_witness')}))
