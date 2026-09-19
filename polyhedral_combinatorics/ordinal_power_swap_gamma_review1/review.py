#!/usr/bin/env python3
"""Independent exact audit of the ordinal-power copy-permutation claim.

CPython 3.11+, standard library only.  This does not import the target code.
For the definition-level tests it recovers equivariant numerators from lattice
counts and a literal permutation-matrix determinant, rather than using the
target's shell convolution or cycle-factor determinant.
"""

from itertools import combinations, permutations, product
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


def add(a, b):
    out = [0] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += value
    return trim(out)


def scale(a, scalar):
    return trim([scalar * value for value in a])


def multiply(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def power(a, exponent):
    out = [1]
    for _ in range(exponent):
        out = multiply(out, a)
    return out


def stretch(a, factor):
    out = [0] * (factor * (len(a) - 1) + 1)
    for i, value in enumerate(a):
        out[factor * i] = value
    return out


def pad(a, size):
    return list(a) + [0] * (size - len(a))


def ordinal_relation(n, relation, copies):
    out = {(a * n + x, a * n + y)
           for a in range(copies) for x, y in relation}
    out.update((a * n + x, b * n + y)
               for a in range(copies) for b in range(a + 1, copies)
               for x in range(n) for y in range(n))
    return out


def all_nonempty_chains(size, relation):
    """Use all chains, not a precomputed maximal-chain decomposition."""
    chains = []
    for mask in range(1, 1 << size):
        subset = tuple(i for i in range(size) if mask & (1 << i))
        if all((min(i, j), max(i, j)) in relation
               for i, j in combinations(subset, 2)):
            chains.append(subset)
    return chains


def fixed_lattice_counts(n, relation, copies, bound):
    relation_q = ordinal_relation(n, relation, copies)
    chains = all_nonempty_chains(n * copies, relation_q)
    group = list(permutations(range(copies)))
    counts = {g: [0] * (bound + 1) for g in group}
    ambient = 0
    feasible = 0
    for m in range(bound + 1):
        for vector in product(range(m + 1), repeat=n * copies):
            ambient += 1
            if any(sum(vector[i] for i in chain) > m for chain in chains):
                continue
            feasible += 1
            for g in group:
                if all(vector[a * n + i] == vector[g[a] * n + i]
                       for a in range(copies) for i in range(n)):
                    counts[g][m] += 1
    return counts, ambient, feasible


def action_matrix(n, copies, g):
    """Homogenizing direction plus the actual coordinate permutation."""
    size = n * copies + 1
    matrix = [[0] * size for _ in range(size)]
    matrix[0][0] = 1
    for a in range(copies):
        for i in range(n):
            matrix[1 + g[a] * n + i][1 + a * n + i] = 1
    return matrix


def determinant_i_minus_ta(matrix):
    """Literal Leibniz determinant over Z[t], suitable for size at most 7."""
    size = len(matrix)
    total = [0]

    def visit(row, used, term, sign):
        nonlocal total
        if row == size:
            total = add(total, scale(term, sign))
            return
        for column in range(size):
            if column in used:
                continue
            entry = [int(row == column), -matrix[row][column]]
            entry = trim(entry)
            if entry == [0]:
                continue
            inversions_added = sum(previous > column for previous in used)
            visit(row + 1, used + (column,), multiply(term, entry),
                  sign * (-1 if inversions_added % 2 else 1))

    visit(0, tuple(), [1], 1)
    return trim(total)


def series_product(series, polynomial, bound):
    out = [0] * (bound + 1)
    for i, x in enumerate(series):
        for j, y in enumerate(polynomial):
            if i + j <= bound:
                out[i + j] += x * y
    return out


def ordinary_h_from_counts(n, relation):
    counts, _, _ = fixed_lattice_counts(n, relation, 1, n)
    ehrhart = counts[(0,)]
    denominator = [(-1) ** j * comb(n + 1, j) for j in range(n + 2)]
    return trim(series_product(ehrhart, denominator, n))


def cycle_lengths(g):
    unseen = set(range(len(g)))
    lengths = []
    while unseen:
        start = min(unseen)
        cursor = start
        length = 0
        while cursor in unseen:
            unseen.remove(cursor)
            length += 1
            cursor = g[cursor]
        require(cursor == start, "invalid permutation")
        lengths.append(length)
    return sorted(lengths)


def predicted_numerator(h, g):
    out = [1]
    for length in cycle_lengths(g):
        out = multiply(out, stretch(h, length))
    return out


def linear_extensions(n, relation):
    out = []
    for word in permutations(range(n)):
        position = {value: index for index, value in enumerate(word)}
        if all(position[x] < position[y] for x, y in relation):
            out.append(word)
    return out


def descents(word):
    return sum(x > y for x, y in zip(word, word[1:]))


def tuple_fixed_numerator(n, relation, copies, g):
    extensions = linear_extensions(n, relation)
    out = [0] * (copies * max(1, n) + 1)
    for words in product(extensions, repeat=copies):
        if all(words[a] == words[g[a]] for a in range(copies)):
            out[sum(descents(word) for word in words)] += 1
    return trim(out)


def gamma_coordinates(poly, degree):
    residual = pad(poly, degree + 1)
    require(residual == residual[::-1], "gamma input is not palindromic")
    coordinates = []
    for j in range(degree // 2 + 1):
        value = residual[j]
        coordinates.append(value)
        basis = [0] * j + [comb(degree - 2 * j, q)
                           for q in range(degree - 2 * j + 1)]
        residual = [x - value * y
                    for x, y in zip(residual, pad(basis, degree + 1))]
    require(not any(residual), "gamma basis did not reconstruct polynomial")
    return coordinates


def c2_gamma_multiplicities(h, copies):
    degree = (len(h) - 1) * copies
    at_identity = gamma_coordinates(power(h, copies), degree)
    at_swap = gamma_coordinates(
        multiply(stretch(h, 2), power(h, copies - 2)), degree)
    trivial = []
    sign = []
    for dimension, value in zip(at_identity, at_swap):
        require((dimension + value) % 2 == 0, "nonintegral C2 multiplicity")
        trivial.append((dimension + value) // 2)
        sign.append((dimension - value) // 2)
    return at_identity, at_swap, trivial, sign


def divide_by_one_plus_t(poly):
    require(len(poly) >= 2, "constant cannot be divided")
    quotient = [poly[0]]
    for value in poly[1:-1]:
        quotient.append(value - quotient[-1])
    require(quotient[-1] == poly[-1], "not divisible by 1+t")
    return trim(quotient)


def root_data(poly):
    reduced = trim(poly)
    multiplicity = 0
    while len(reduced) > 1 and sum((-1) ** i * value
                                   for i, value in enumerate(reduced)) == 0:
        reduced = divide_by_one_plus_t(reduced)
        multiplicity += 1
    return multiplicity, reduced


def audit_obstruction(h, copies):
    degree = len(h) - 1
    multiplicity, reduced = root_data(h)
    require(multiplicity > 0, "root hypothesis absent")
    require((degree - multiplicity) % 2 == 0, "root parity failure")
    index = copies * ((degree - multiplicity) // 2) + multiplicity
    predicted = ((-1) ** index * sum(h) *
                 sum((-1) ** i * value for i, value in enumerate(reduced)) **
                 (copies - 2))
    identity, swap, trivial, sign = c2_gamma_multiplicities(h, copies)
    require(identity[index] == 0, "claimed zero dimension is nonzero")
    require(swap[index] == predicted != 0, "claimed transposition value fails")
    require(trivial[index] == predicted // 2 and sign[index] == -predicted // 2,
            "C2 restriction formula fails")
    require(min(trivial[index], sign[index]) < 0, "negative multiplicity absent")
    return [index, predicted, trivial[index], sign[index]]


def run():
    cases = [
        ("singleton_k1", 1, frozenset(), 1),
        ("singleton_k3", 1, frozenset(), 3),
        ("chain2_k2", 2, frozenset({(0, 1)}), 2),
        ("antichain2_k2", 2, frozenset(), 2),
        ("antichain2_k3", 2, frozenset(), 3),
        ("antichain3_k2", 3, frozenset(), 2),
        ("v_poset_k2", 3, frozenset({(0, 2), (1, 2)}), 2),
    ]
    report = {
        "schema": 1,
        "definition_cases": len(cases),
        "ambient_vectors": 0,
        "feasible_vectors": 0,
        "fixed_action_comparisons": 0,
        "linear_extension_character_comparisons": 0,
    }
    recovered_h = {}
    for name, n, relation, copies in cases:
        h = ordinary_h_from_counts(n, relation)
        recovered_h[name] = h
        dimension = n * copies
        bound = dimension + 1
        counts, ambient, feasible = fixed_lattice_counts(
            n, relation, copies, bound)
        report["ambient_vectors"] += ambient
        report["feasible_vectors"] += feasible
        for g, series in counts.items():
            determinant = determinant_i_minus_ta(action_matrix(n, copies, g))
            actual = trim(series_product(series, determinant, bound))
            expected = predicted_numerator(h, g)
            require(actual == expected,
                    f"definition-level numerator mismatch in {name}, {g}")
            report["fixed_action_comparisons"] += 1
            tuple_value = tuple_fixed_numerator(n, relation, copies, g)
            require(tuple_value == expected,
                    f"permutation-character model mismatch in {name}, {g}")
            report["linear_extension_character_comparisons"] += 1

    require(recovered_h["antichain2_k2"] == [1, 1], "A2 h mismatch")
    require(recovered_h["antichain3_k2"] == [1, 4, 1], "A3 h mismatch")
    require(recovered_h["chain2_k2"] == [1], "chain control mismatch")

    antichain5 = ordinary_h_from_counts(5, frozenset())
    require(antichain5 == [1, 26, 66, 26, 1], "A5 h mismatch")

    root_cases = {}
    for label, h in (("C4_base", [1, 1]), ("double_root_formal", [1, 2, 1])):
        root_cases[label] = {}
        for copies in range(2, 7):
            root_cases[label][str(copies)] = audit_obstruction(h, copies)

    a3 = c2_gamma_multiplicities([1, 4, 1], 2)
    require(a3[2][-1] == 5 and a3[3][-1] == -1,
            "root-free negative control changed")
    a5 = c2_gamma_multiplicities(antichain5, 2)
    require(all(value >= 0 for row in a5[2:] for value in row),
            "root-free positive control changed")
    simplex = c2_gamma_multiplicities([1], 2)
    require(simplex == ([1], [1], [1], [0]), "degree-zero edge case changed")

    family_checks = []
    for n, a in ((2, 1), (2, 3), (4, 1)):
        size = n * a
        relation = frozenset((chain * a + i, chain * a + j)
                             for chain in range(n)
                             for i in range(a) for j in range(i + 1, a))
        extensions = linear_extensions(size, relation)
        h = [0] * (size + 1)
        for word in extensions:
            h[descents(word)] += 1
        h = trim(h)
        require(sum(h) == factorial(size) // factorial(a) ** n,
                "multinomial extension count mismatch")
        index, value, trivial, sign = audit_obstruction(h, 2)
        expected_half = factorial(size) // (2 * factorial(a) ** n)
        require(index == a * (n - 1), "family top index mismatch")
        require((trivial, sign) == (-expected_half, expected_half),
                "family character mismatch")
        family_checks.append({"n": n, "a": a, "top_index": index,
                              "trivial": trivial, "sign": sign,
                              "swap_value": value})

    report.update({
        "base_h_controls": {
            "antichain_2": recovered_h["antichain2_k2"],
            "antichain_3": recovered_h["antichain3_k2"],
            "antichain_5": antichain5,
            "chain_2": recovered_h["chain2_k2"],
        },
        "root_obstruction_cases": root_cases,
        "root_free_negative_A3": {
            "trivial": a3[2], "sign": a3[3]},
        "root_free_positive_A5": {
            "trivial": a5[2], "sign": a5[3]},
        "family_checks": family_checks,
        "status": "all independent exact checks passed",
    })
    return report


if __name__ == "__main__":
    result = run()
    expected_path = Path(__file__).with_name("EXPECTED.json")
    if expected_path.exists():
        require(result == json.loads(expected_path.read_text()),
                "EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
