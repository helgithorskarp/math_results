#!/usr/bin/env python3
"""Independent literal-period and permutation-action audit; standard library."""

from hashlib import sha256
from itertools import permutations, product
from math import comb, gcd
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def divisors(n):
    return tuple(d for d in range(1, n + 1) if n % d == 0)


def image(mask, permutation):
    result = 0
    while mask:
        bit = mask & -mask
        result |= 1 << permutation[bit.bit_length() - 1]
        mask -= bit
    return result


def classes(period, modulus):
    return tuple(sum(1 << x for x in range(a, period, modulus))
                 for a in range(modulus))


def unions(period, moduli):
    """Enumerate labeled coverage unions; no residual-fiber quotient/pruning."""
    result = {0}
    for modulus in moduli:
        options = (0,) + classes(period, modulus)  # zero means omission
        result = {old | new for old in result for new in options}
    return result


def tree_permutations(q, depth):
    """Enumerate actual leaf permutations, rather than subset-type recursion."""
    if depth == 0:
        return ((0,),)
    child_actions = tree_permutations(q, depth - 1)
    result = []
    for root in permutations(range(q)):
        for children in product(child_actions, repeat=q):
            result.append(tuple(root[y % q] + q * children[y % q][y // q]
                                for y in range(q ** depth)))
    return tuple(result)


def canonical_table(size, actions):
    result = list(range(1 << size))
    for action in actions:
        images = [0] * (1 << size)
        for mask in range(1, 1 << size):
            bit = mask & -mask
            images[mask] = images[mask - bit] | (1 << action[bit.bit_length() - 1])
            result[mask] = min(result[mask], images[mask])
    return tuple(result)


def key(fibers, representatives):
    return tuple(sorted(representatives[u] for u in fibers if u))


def literal_fibers(mask, power, cofactor):
    fibers = [0] * power
    while mask:
        bit = mask & -mask
        x = bit.bit_length() - 1
        fibers[x % power] |= 1 << (x % cofactor)
        mask -= bit
    return tuple(fibers)


def continuation_checks(p, cofactor, depth, parent_samples, representatives):
    old_power = p ** depth
    new_power = p * old_power
    period = new_power * cofactor
    all_unions = unions(period, [new_power * d for d in divisors(cofactor)])
    # Decode every complete labeled coverage choice once, after enumeration.
    uncovered_templates = tuple(literal_fibers(((1 << period) - 1) ^ covered,
                                             new_power, cofactor)
                                for covered in all_unions)
    by_parent_key = {}
    for parents in parent_samples:
        require(len(parents) == old_power, "wrong parent count")
        successors = {
            key((u & parents[r % old_power] for r, u in enumerate(template)),
                representatives)
            for template in uncovered_templates
        }
        parent_key = key(parents, representatives)
        if parent_key in by_parent_key:
            require(successors == by_parent_key[parent_key],
                    "same proposed state has different literal continuation sets")
        else:
            by_parent_key[parent_key] = successors
    return {"p": p, "cofactor": cofactor, "depth": depth,
            "parent_assignments": len(parent_samples),
            "state_keys": len(by_parent_key),
            "literal_coverage_unions": len(all_unions)}


def ambient_action(p, cofactor, depth, parent_action, local_actions):
    old_power = p ** depth
    new_power = p * old_power
    period = new_power * cofactor
    inverse_crt = {(x % new_power, x % cofactor): x for x in range(period)}
    return tuple(inverse_crt[(parent_action[(x % new_power) % old_power]
                             + old_power * ((x % new_power) // old_power),
                             local_actions[x % old_power][x % cofactor])]
                 for x in range(period))


def transport_checks(p, cofactor, depth, actions):
    """Check literal class bijections for generators of independent local action."""
    old_power = p ** depth
    new_power = p * old_power
    period = new_power * cofactor
    identity = tuple(range(cofactor))
    layers = {new_power * d: classes(period, new_power * d)
              for d in divisors(cofactor)}
    checked = 0
    for parent_action in [tuple(range(old_power))]:
        for local in actions:
            # All actions in parent zero; parent permutations generate the rest.
            locals_here = (local,) + (identity,) * (old_power - 1)
            action = ambient_action(p, cofactor, depth, parent_action, locals_here)
            require(len(set(action)) == period, "ambient action is not bijective")
            for modulus, options in layers.items():
                induced = tuple(action[a] % modulus for a in range(modulus))
                require(len(set(induced)) == modulus, "resource options not bijective")
                for a, option in enumerate(options):
                    require(image(option, action) == options[induced[a]],
                            "transport changed an individual modulus")
            checked += 1
    for parent_action in permutations(range(old_power)):
        action = ambient_action(p, cofactor, depth, parent_action,
                                (identity,) * old_power)
        for modulus, options in layers.items():
            for a, option in enumerate(options):
                require(image(option, action) == options[action[a] % modulus],
                        "parent permutation changed an individual modulus")
        checked += 1
    return checked


def main():
    require(sys.version_info >= (3, 10), "Python >=3.10 required")
    tree_reports = {}
    tree_tables = {}
    for q, depth in [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (5, 1)]:
        size = q ** depth
        actions = tree_permutations(q, depth)
        require(len(set(actions)) == len(actions), "duplicate tree action")
        for action in actions:
            require(sorted(action) == list(range(size)), "not a leaf permutation")
            for modulus in divisors(size):
                for option in classes(size, modulus):
                    require(image(option, action) in classes(size, modulus),
                            "tree group fails congruence preservation")
        table = canonical_table(size, actions)
        count = len(set(table))
        predicted = 2
        for _ in range(depth):
            predicted = comb(predicted + q - 1, q)
        require(count == predicted, "tree orbit recurrence mismatch")
        tree_reports[f"{q}^{depth}"] = {"actual_permutations": len(actions),
                                        "subset_orbits": count}
        tree_tables[size] = (table, actions)

    rotation_reports = {}
    rotation_tables = {}
    for size in range(1, 10):
        actions = tuple(tuple((y + shift) % size for y in range(size))
                        for shift in range(size))
        table = canonical_table(size, actions)
        count = len(set(table))
        numerator = sum(2 ** gcd(size, shift) for shift in range(size))
        require(numerator == size * count, "translation Burnside count mismatch")
        rotation_reports[str(size)] = count
        rotation_tables[size] = (table, actions)

    # Exhaust the full symmetric group in a composite control. Every admissible
    # action must preserve each prime-coordinate partition; this checks maximality
    # without constructing the group by CRT or using the proposed characterization.
    composite_actions = []
    for action in permutations(range(6)):
        if all(image(option, action) in classes(6, modulus)
               for modulus in divisors(6) for option in classes(6, modulus)):
            composite_actions.append(action)
    composite_orbits = len(set(canonical_table(6, composite_actions)))
    require(len(composite_actions) == 12 and composite_orbits == 13,
            "full composite congruence group control failed")
    require(composite_orbits != tree_reports['2^1']['subset_orbits']
            * tree_reports['3^1']['subset_orbits'],
            "incorrect factorwise subset-orbit multiplication escaped control")

    continuation_reports = []
    for p, cofactor in [(2, 3), (2, 5), (3, 2)]:
        samples = tuple(product(range(1 << cofactor), repeat=p))
        continuation_reports.append(continuation_checks(
            p, cofactor, 1, samples, tuple(range(1 << cofactor))))
        continuation_reports.append(continuation_checks(
            p, cofactor, 1, samples, rotation_tables[cofactor][0]))
    continuation_reports.append(continuation_checks(
        2, 9, 0, tuple((u,) for u in range(512)), tree_tables[9][0]))
    # Two distinct labeled parents, including empties and equal fibers.
    samples = {(u, 511 ^ u) for u in range(512)}
    samples |= {(1, 3), (7, 19), (341, 511), (511, 341), (511, 511), (0, 0)}
    continuation_reports.append(continuation_checks(
        2, 9, 1, tuple(sorted(samples)), tree_tables[9][0]))

    transport = {
        "binary_M3_two_parents": transport_checks(2, 3, 1, rotation_tables[3][1]),
        "binary_M3_four_parents": transport_checks(2, 3, 2, rotation_tables[3][1]),
        "binary_M9_two_parents": transport_checks(2, 9, 1, tree_tables[9][1]),
        "ternary_M2_three_parents": transport_checks(3, 2, 1, rotation_tables[2][1]),
    }

    # Definition-level bounded full-period feasibility; no symmetry or width cut.
    period_reports = []
    for p, cofactor, largest in [(2, 1, 4), (2, 3, 2), (2, 5, 2), (3, 4, 1)]:
        for depth in range(largest + 1):
            period = p ** depth * cofactor
            for minimum in range(2, 9):
                all_moduli = tuple(d for d in divisors(period) if d >= minimum)
                choices = unions(period, all_moduli)
                atleast = (1 << period) - 1 in choices
                exact = atleast and period % minimum == 0
                period_reports.append({"p": p, "cofactor": cofactor,
                                       "exponent": depth, "minimum": minimum,
                                       "at_least": atleast, "exact": exact})
    require(next(x for x in period_reports if (x['p'], x['cofactor'],
                 x['exponent'], x['minimum']) == (2, 3, 2, 2))['exact'],
            "classical minimum-two positive control failed")
    require(not any(x['exact'] for x in period_reports if x['minimum'] == 8),
            "small minimum-eight negative controls failed")

    cutoffs = {"raw": 2 + comb(511 + 2, 2),
               "translations": 2 + comb(rotation_reports['9'] - 1 + 2, 2),
               "tree": 2 + comb(tree_reports['3^2']['subset_orbits'] - 1 + 2, 2)}
    require(cutoffs == {"raw": 131330, "translations": 1832, "tree": 212},
            "cutoff arithmetic mismatch")
    # This local transformation cannot preserve the earlier single modulus-three
    # class globally, yet the continuation transport remains a valid bijection.
    earlier_uncovered = (6, 6)  # both fibers are {1,2} after removing 0 mod 3
    locally_transformed = (5, 6)  # translate only the first cofactor fiber by one
    before = continuation_checks(2, 3, 1, (earlier_uncovered, locally_transformed),
                                 rotation_tables[3][0])
    require(before['state_keys'] == 1, "independent local normalization failed")
    report = {"reviewer": "six-reviewer-3", "role": "independent reviewer",
              "tree_actions": tree_reports, "translation_subset_orbits": rotation_reports,
              "literal_continuation_checks": continuation_reports,
              "ambient_class_transport_maps": transport,
              "composite_M6": {"all_permutations_checked": 720,
                                "congruence_preserving_permutations": len(composite_actions),
                                "subset_orbits": composite_orbits,
                                "factor_orbit_product": 12},
              "bounded_period_cases": len(period_reports),
              "bounded_period_table_sha256": sha256(json.dumps(period_reports,
                  sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
              "M9_cutoffs": cutoffs,
              "independent_local_normalization_control": before}
    text = json.dumps(report, indent=2, sort_keys=True) + '\n'
    expected = Path(__file__).with_name('expected.json')
    if expected.exists():
        require(json.loads(expected.read_text()) == report, "expected report mismatch")
    print(text, end='')


if __name__ == '__main__':
    main()
