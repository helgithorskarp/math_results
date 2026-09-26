#!/usr/bin/env python3
"""Definition-level and exact algebra audits; no third-party dependencies."""

from copy import deepcopy
from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path

from verify import require, verify


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, column)) for column in zip(*b)]
            for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def word_matrix(a, word):
    n = len(a)
    answer = [[int(i == j) for j in range(n)] for i in range(n)]
    for sign in word:
        answer = multiply(answer, a if sign == 1 else transpose(a))
    return answer


def flips(word):
    return sum(x != y for x, y in zip(word, word[1:]))


def brute_hom_numerator(a, word):
    n = len(a)
    total = 0
    for assignment in product(range(n), repeat=len(word) + 1):
        term = 1
        for j, sign in enumerate(word):
            x, y = assignment[j:j + 2]
            term *= a[x][y] if sign == 1 else a[y][x]
        total += term
    return total


class Polynomial(dict):
    """Integer polynomials in x, delta, s, as exponent triples."""

    def __add__(self, other):
        other = other if isinstance(other, Polynomial) else constant(other)
        result = Polynomial(self)
        for power, coefficient in other.items():
            result[power] = result.get(power, 0) + coefficient
            if not result[power]:
                del result[power]
        return result

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({p: -c for p, c in self.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, Polynomial) else constant(other)
        result = Polynomial()
        for left, a in self.items():
            for right, b in other.items():
                power = tuple(x + y for x, y in zip(left, right))
                result = result + Polynomial({power: a * b})
        return result

    __rmul__ = __mul__

    def __pow__(self, exponent):
        result = constant(1)
        for _ in range(exponent):
            result = result * self
        return result


def constant(value):
    return Polynomial({(0, 0, 0): value}) if value else Polynomial()


def determinant(a):
    total = constant(0)
    for permutation in permutations(range(len(a))):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(len(a)) for j in range(i + 1, len(a)))
        term = constant((-1)**inversions)
        for i, j in enumerate(permutation):
            term = term * a[i][j]
        total = total + term
    return total


def polynomial_audit():
    x = Polynomial({(1, 0, 0): 1})
    delta = Polynomial({(0, 1, 0): 1})
    s = Polynomial({(0, 0, 1): 1})
    t = [[constant(1), -delta, constant(0)],
         [delta, constant(0), -s],
         [constant(0), s, constant(0)]]
    char = determinant([[x * int(i == j) - t[i][j] for j in range(3)]
                        for i in range(3)])
    require(char == (x - 1) * (x**2 + s**2) + delta**2 * x,
            "Perron characteristic polynomial mismatch")
    gram = multiply(t, transpose(t))
    at_one = determinant([[constant(int(i == j)) - gram[i][j] for j in range(3)]
                          for i in range(3)])
    require(at_one == delta**4 - 2 * (1 - s**2) * delta**2,
            "Gram polynomial at one mismatch")
    gram_char = determinant([[x * int(i == j) - gram[i][j] for j in range(3)]
                             for i in range(3)])
    at_zero = Polynomial({power: coefficient for power, coefficient in gram_char.items()
                          if power[1] == 0})
    require(at_zero == (x - 1) * (x - s**2)**2, "Gram polynomial at delta=0 mismatch")
    require(all(power[1] % 2 == 0 for power in gram_char), "odd perturbation term")
    return 4


def main():
    # Distinct representations: enumerate vertex maps, then use transfer matrices.
    hom_cases = 0
    for a, denominator, max_length in [
        ([[2, 3], [1, 2]], 4, 7),
        ([[1, 2, 2], [0, 1, 2], [0, 0, 1]], 2, 5),
    ]:
        n = len(a)
        for length in range(max_length + 1):
            for word in product([1, -1], repeat=length):
                brute = brute_hom_numerator(a, word)
                matrix = word_matrix(a, word)
                transfer = sum(map(sum, matrix))
                require(brute == transfer, "definition/transfer mismatch")
                density_ratio = Fraction((2**length) * brute,
                                         n**(length + 1) * denominator**length)
                normalized_product = [
                    [Fraction((2**length) * z, (n * denominator)**length) for z in row]
                    for row in matrix
                ]
                require(density_ratio == sum(map(sum, normalized_product)) / n,
                        "normalization mismatch")
                hom_cases += 1

    reflection_cases = 0
    a = [[2, 3], [1, 2]]
    for length in range(1, 9):
        for word in product([1, -1], repeat=length):
            reflected = tuple(-x for x in reversed(word))
            aw = word_matrix(a, word)
            require(word_matrix(a, reflected) == transpose(aw), "reflection mismatch")
            p = multiply(aw, transpose(aw))
            require(p == word_matrix(a, word + reflected), "concatenation mismatch")
            mean = Fraction(sum(map(sum, p)), 2)
            power = [[1, 0], [0, 1]]
            for repetitions in range(1, 4):
                power = multiply(power, p)
                require(Fraction(sum(map(sum, power)), 2) >= mean**repetitions,
                        "PSD moment inequality mismatch")
                repeated = (word + reflected) * repetitions
                require(flips(repeated) == 2 * repetitions * (flips(word) + 1) - 1,
                        "reflected flip-count mismatch")
                for padding in range(2 * length):
                    require(flips(repeated + (1,) * padding)
                            <= 2 * repetitions * (flips(word) + 1),
                            "padding flip-count mismatch")
            reflection_cases += 1

    certificate = json.loads(Path(__file__).with_name("certificate.json").read_text())
    mutants = []
    for key, index, increment in [
        ("potential", 0, 10**9),
        ("subeigenvector", 0, 10**12),
        ("subeigenvector", 0, -10**18),
    ]:
        mutant = deepcopy(certificate)
        mutant[key][index] += increment
        mutants.append(mutant)
    for mutant in mutants:
        try:
            verify(mutant)
        except ValueError:
            pass
        else:
            raise ValueError("invalid certificate was accepted")

    print(json.dumps({
        "status": "PASS",
        "definition_level_cases": hom_cases,
        "reflection_cases": reflection_cases,
        "polynomial_identities": polynomial_audit(),
        "rejected_mutants": len(mutants),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
