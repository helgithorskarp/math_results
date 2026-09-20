#!/usr/bin/env python3
"""Independent exact audit of the five-antichain copy threshold.

CPython 3.11+, standard library only.  No target source is imported.  Gamma
coordinates are recovered by generic rational Gaussian elimination, and
character inner products are taken over actual permutations rather than a
partition/cycle-index table.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(poly):
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def multiply(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def power(poly, exponent):
    out = [1]
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def substitute_power(poly, exponent):
    out = [0] * ((len(poly) - 1) * exponent + 1)
    for i, value in enumerate(poly):
        out[i * exponent] = value
    return out


def polynomial_value(poly, value):
    return sum(coefficient * value ** i for i, coefficient in enumerate(poly))


def solve_square(matrix, rhs):
    """Generic exact Gaussian elimination; matrix is not assumed triangular."""
    size = len(rhs)
    augmented = [[Fraction(value) for value in row] + [Fraction(rhs[i])]
                 for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if augmented[row][column]), None)
        require(pivot is not None, "singular gamma basis matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [x - multiplier * y
                              for x, y in zip(augmented[row], augmented[column])]
    solution = [augmented[i][-1] for i in range(size)]
    require(all(value.denominator == 1 for value in solution),
            "nonintegral gamma coordinate")
    return [int(value) for value in solution]


def gamma_coordinates(poly, degree):
    require(len(poly) <= degree + 1, "polynomial exceeds declared degree")
    padded = list(poly) + [0] * (degree + 1 - len(poly))
    require(padded == padded[::-1], "gamma polynomial is not palindromic")
    rank = degree // 2 + 1
    bases = []
    for j in range(rank):
        basis = [0] * (degree + 1)
        for q in range(degree - 2 * j + 1):
            basis[j + q] = comb(degree - 2 * j, q)
        bases.append(basis)
    matrix = [[bases[column][row] for column in range(rank)]
              for row in range(rank)]
    answer = solve_square(matrix, padded[:rank])
    reconstruction = [0] * (degree + 1)
    for coefficient, basis in zip(answer, bases):
        for i, value in enumerate(basis):
            reconstruction[i] += coefficient * value
    require(reconstruction == padded, "gamma reconstruction failed")
    return answer


def permutation_cycles(g):
    unseen = set(range(len(g)))
    cycles = []
    while unseen:
        start = min(unseen)
        cursor = start
        cycle = []
        while cursor in unseen:
            unseen.remove(cursor)
            cycle.append(cursor)
            cursor = g[cursor]
        require(cursor == start, "malformed permutation")
        cycles.append(tuple(cycle))
    return cycles


def permutation_sign(g):
    inversions = sum(g[i] > g[j] for i in range(len(g))
                     for j in range(i + 1, len(g)))
    return -1 if inversions % 2 else 1


def fixed_points(g):
    return sum(i == value for i, value in enumerate(g))


def cycle_numerator(h, g):
    out = [1]
    for cycle in permutation_cycles(g):
        out = multiply(out, substitute_power(h, len(cycle)))
    return out


def exact_average(values):
    return Fraction(sum(values), len(values))


def eulerian_from_ehrhart(n):
    counts = [(m + 1) ** n for m in range(n + 1)]
    out = []
    for degree in range(n + 1):
        out.append(sum((-1) ** j * comb(n + 1, j) * counts[degree - j]
                       for j in range(degree + 1)))
    return trim(out)


def natural_posets(n):
    pairs = list(combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        relation = frozenset(pair for bit, pair in enumerate(pairs)
                             if mask & (1 << bit))
        if all((x, z) in relation for x, y in relation for yy, z in relation
               if y == yy):
            yield relation


def chains(n, relation):
    out = []
    for mask in range(1, 1 << n):
        chain = tuple(i for i in range(n) if mask & (1 << i))
        if all((x, y) in relation for x, y in combinations(chain, 2)):
            out.append(chain)
    return out


def maximal_chains(n, relation):
    all_chains = chains(n, relation)
    return [chain for chain in all_chains
            if not any(set(chain) < set(other) for other in all_chains)]


def linear_extension_polynomial(n, relation):
    counts = Counter()
    extension_count = 0
    for word in permutations(range(n)):
        position = {value: i for i, value in enumerate(word)}
        if all(position[x] < position[y] for x, y in relation):
            extension_count += 1
            counts[sum(word[i] > word[i + 1] for i in range(n - 1))] += 1
    return trim([counts[i] for i in range(max(counts, default=0) + 1)]), extension_count


def signed_subset_coefficient(positive, negative, size):
    return sum((-1) ** q * comb(negative, q) * comb(positive, size - q)
               for q in range(size + 1)
               if q <= negative and size - q <= positive)


def exterior_hilbert_from_degree_counts(counts, size):
    """Coefficient of z^size in product_d (1+z*t^d)^counts[d]."""
    states = {(0, 0): 1}
    for degree, amount in enumerate(counts):
        next_states = {}
        for (chosen, total_degree), value in states.items():
            for take in range(min(amount, size - chosen) + 1):
                key = (chosen + take, total_degree + take * degree)
                next_states[key] = next_states.get(key, 0) + value * comb(amount, take)
        states = next_states
    maximum = max((degree for (chosen, degree) in states if chosen == size), default=0)
    return trim([states.get((size, degree), 0) for degree in range(maximum + 1)])


def top_invariants(h):
    degree = len(h) - 1
    require(degree % 2 == 0, "top-character test needs even degree")
    middle = degree // 2
    b = (-1) ** middle * polynomial_value(h, -1)
    e = polynomial_value(h, 1)
    require(b > 0 and e >= b and (e - b) % 2 == 0,
            "invalid nonvanishing signed alphabet")
    return middle, b, e, (e + b) // 2, (e - b) // 2


def a5_audit():
    h = eulerian_from_ehrhart(5)
    require(h == [1, 26, 66, 26, 1], "five-cube numerator mismatch")
    require(gamma_coordinates(h, 4) == [1, 22, 16], "base gamma mismatch")

    identity = gamma_coordinates(power(h, 2), 8)
    exchange = gamma_coordinates(substitute_power(h, 2), 8)
    trivial = [(x + y) // 2 for x, y in zip(identity, exchange)]
    sign = [(x - y) // 2 for x, y in zip(identity, exchange)]
    require(trivial == [1, 18, 281, 292, 188], "S2 trivial list mismatch")
    require(sign == [0, 26, 235, 412, 68], "S2 sign list mismatch")
    require(min(trivial + sign) >= 0, "two-copy action is not effective")

    group3 = list(permutations(range(3)))
    top_values = {}
    for g in group3:
        top_values[g] = gamma_coordinates(cycle_numerator(h, g), 12)[-1]
    decomposition = {
        "trivial": exact_average(list(top_values.values())),
        "standard": exact_average([top_values[g] * (fixed_points(g) - 1)
                                    for g in group3]),
        "sign": exact_average([top_values[g] * permutation_sign(g)
                                for g in group3]),
    }
    require(decomposition == {"trivial": 1648, "standard": 1360, "sign": -272},
            "S3 top decomposition mismatch")

    exterior3 = exterior_hilbert_from_degree_counts(h, 3)
    exterior_gamma = gamma_coordinates(exterior3, 12)
    require(exterior_gamma[-1] == decomposition["sign"] == -272,
            "exterior-cube top coefficient mismatch")

    middle, b, e, positive, negative = top_invariants(h)
    require((middle, b, e, positive, negative) == (2, 16, 120, 68, 52),
            "A5 signed alphabet mismatch")
    require(signed_subset_coefficient(positive, negative, 3) == -272,
            "signed-subset coefficient mismatch")

    restrictions = []
    for copies in range(3, 13):
        restricted_values = []
        restricted_signs = []
        for g3 in group3:
            extended = tuple(g3) + tuple(range(3, copies))
            value = gamma_coordinates(cycle_numerator(h, extended), 4 * copies)[-1]
            restricted_values.append(value)
            restricted_signs.append(permutation_sign(g3))
        multiplicity = exact_average([x * y for x, y in
                                      zip(restricted_values, restricted_signs)])
        expected = -272 * 16 ** (copies - 3)
        require(multiplicity == expected, "restriction persistence mismatch")
        restrictions.append([copies, int(multiplicity)])

    require(26 - 6 * 4 == 2 and 26 - 7 * 4 == -2,
            "A5 first-character boundary mismatch")
    return {
        "base_h": h,
        "base_gamma": [1, 22, 16],
        "s2_trivial": trivial,
        "s2_sign": sign,
        "s3_top_decomposition": [int(decomposition[name])
                                 for name in ("trivial", "standard", "sign")],
        "exterior_cube_top": exterior_gamma[-1],
        "signed_alphabet": [positive, negative],
        "restrictions": restrictions,
    }


def exhaustive_small_poset_audit():
    counts_by_size = {}
    graded = 0
    first_value_checks = 0
    first_inner_product_checks = 0
    top_value_checks = 0
    top_sign_checks = 0
    eventual_bound_checks = 0
    distinct_h = set()

    for n in range(1, 6):
        fixtures = list(natural_posets(n))
        counts_by_size[str(n)] = len(fixtures)
        for relation in fixtures:
            maximal = maximal_chains(n, relation)
            lengths = {len(chain) for chain in maximal}
            if len(lengths) != 1:
                continue
            graded += 1
            h, extension_count = linear_extension_polynomial(n, relation)
            chain_length = next(iter(lengths))
            degree = n - chain_length
            require(len(h) - 1 == degree, "graded degree formula mismatch")
            ordinary_gamma = gamma_coordinates(h, degree)
            require(min(ordinary_gamma) >= 0, "ordinary gamma negativity")
            require(sum(h) == extension_count, "linear extension count mismatch")
            distinct_h.add(tuple(h))

            if degree > 0:
                a = h[1]
                for copies in range(2, 5):
                    group = list(permutations(range(copies)))
                    first_values = []
                    for g in group:
                        actual = gamma_coordinates(
                            cycle_numerator(h, g), copies * degree)[1]
                        expected = a * fixed_points(g) - copies * degree
                        require(actual == expected, "first-character class value mismatch")
                        first_values.append(actual)
                        first_value_checks += 1
                    trivial = exact_average(first_values)
                    standard = exact_average([
                        value * (fixed_points(g) - 1)
                        for value, g in zip(first_values, group)])
                    require(trivial == a - copies * degree and standard == a,
                            "first-character irreducible multiplicity mismatch")
                    first_inner_product_checks += 2
                cutoff = a // degree + 1
                require(a - cutoff * degree < 0, "eventual cutoff is not strict")
                eventual_bound_checks += 1

            if degree > 0 and degree % 2 == 0 and polynomial_value(h, -1):
                middle, b, e, positive, negative = top_invariants(h)
                require(middle == degree // 2 and e == extension_count,
                        "top invariant mismatch")
                for copies in range(1, 6):
                    group = list(permutations(range(copies)))
                    signed_sum = 0
                    for g in group:
                        actual = gamma_coordinates(
                            cycle_numerator(h, g), copies * degree)[-1]
                        odd = sum(len(cycle) % 2 for cycle in permutation_cycles(g))
                        even = len(permutation_cycles(g)) - odd
                        expected = b ** odd * e ** even
                        require(actual == expected, "top cycle-parity value mismatch")
                        signed_sum += permutation_sign(g) * actual
                        top_value_checks += 1
                    multiplicity = Fraction(signed_sum, factorial(copies))
                    coefficient = signed_subset_coefficient(positive, negative, copies)
                    require(multiplicity == coefficient,
                            "top sign multiplicity mismatch")
                    top_sign_checks += 1

    require(counts_by_size == {"1": 1, "2": 2, "3": 7, "4": 40, "5": 357},
            "natural-poset fixture count changed")
    return {
        "posets_by_size": counts_by_size,
        "graded_posets": graded,
        "distinct_graded_h_polynomials": len(distinct_h),
        "first_character_class_values": first_value_checks,
        "first_character_inner_products": first_inner_product_checks,
        "top_character_class_values": top_value_checks,
        "top_sign_inner_products": top_sign_checks,
        "eventual_cutoff_checks": eventual_bound_checks,
    }


def adversarial_controls():
    a3 = eulerian_from_ehrhart(3)
    _, b3, e3, u3, v3 = top_invariants(a3)
    require((a3, b3, e3) == ([1, 4, 1], 2, 6), "A3 control mismatch")
    require(signed_subset_coefficient(u3, v3, 2) == -1,
            "A3 two-copy obstruction missing")

    a7 = eulerian_from_ehrhart(7)
    _, b7, e7, u7, v7 = top_invariants(a7)
    a7_s3 = signed_subset_coefficient(u7, v7, 3)
    require(a7_s3 > 0, "A7 must not be excluded by the S3 sign test")

    require(gamma_coordinates([1], 0) == [1], "chain edge case failed")
    require(signed_subset_coefficient(2, 1, 4) == 0,
            "exterior power above dimension must vanish")
    for bad in ([1, 1], [1, 2, 1]):
        try:
            top_invariants(bad)
        except ValueError:
            pass
        else:
            raise ValueError("top-character hypothesis rejection failed")
    return {
        "A3_h_b_e_s2_sign": [a3, b3, e3, -1],
        "A7_b_e_s3_sign": [b7, e7, a7_s3],
        "chain_gamma": [1],
        "above_dimension_exterior": 0,
        "invalid_top_inputs_rejected": 2,
    }


def run():
    result = {
        "schema": 1,
        "a5": a5_audit(),
        "small_posets": exhaustive_small_poset_audit(),
        "controls": adversarial_controls(),
        "status": "all independent exact checks passed",
    }
    return result


if __name__ == "__main__":
    report = run()
    expected_path = Path(__file__).with_name("EXPECTED.json")
    if expected_path.exists():
        require(report == json.loads(expected_path.read_text()),
                "EXPECTED.json mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))
