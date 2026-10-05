#!/usr/bin/env python3
"""Independent literal controls for Atlas's Proposition H, checked by Iris.

Does not import Atlas's or Iris's central-boundary counting program.
Enumerates small diagonal semidirect products by explicit multiplication.
One process, standard-library exact arithmetic, at most 6000 elements.
"""

from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import permutations, product
import argparse
import json
from math import gcd, lcm
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


@cache
def totient(n):
    # An alternate route to the author's prime-factor totient calculation.
    return sum(gcd(a, n) == 1 for a in range(1, n + 1))


def prime_support(n):
    divisors = set()
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            divisors.add(candidate)
            while n % candidate == 0:
                n //= candidate
        candidate += 1
    if n > 1:
        divisors.add(n)
    return divisors


def a5_weight_count():
    histogram = Counter()
    for permutation in permutations(range(5)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(5) for j in range(i + 1, 5))
        if inversions % 2:
            continue
        visited, lengths = set(), []
        for start in range(5):
            if start in visited:
                continue
            current, length = start, 0
            while current not in visited:
                visited.add(current)
                length += 1
                current = permutation[current]
            lengths.append(length)
        histogram[lcm(*lengths)] += 1
    count = sum((Fraction(size, totient(order))
                 for order, size in histogram.items()), Fraction())
    require(histogram == {1: 1, 2: 15, 3: 20, 5: 24}, "Wrong A5 cycle census")
    require(count == 32, "Wrong A5 reciprocal-totient sum")
    return {"histogram": dict(sorted(histogram.items())), "cyclic_subgroups": int(count)}


def diagonal_semidirect(p, multipliers, m, expected_count, expected_eta):
    require(prime_support(p) == {p}, "Kernel characteristic is not prime")
    require(gcd(p, 60*m) == 1 and gcd(m, 30) == 1, "Outside Proposition H")
    require(all(0 < a < p and pow(a, m, p) == 1 for a in multipliers),
            "Specified scalars do not define a C_m action")
    dimension = len(multipliers)
    group_order = p**dimension * m
    require(group_order <= 6000, "Outside documented finite computation scope")
    zero = (0,) * dimension
    identity = (zero, 0)
    scalar_powers = tuple(tuple(pow(a, h, p) for a in multipliers) for h in range(m))

    def multiply(x, y):
        v, h = x
        w, k = y
        return (tuple((v_i + a_i*w_i) % p
                      for v_i, w_i, a_i in zip(v, w, scalar_powers[h])),
                (h + k) % m)

    subgroup_sets, histogram = set(), Counter()
    for v in product(range(p), repeat=dimension):
        for h in range(m):
            generator = (v, h)
            current, powers = identity, {identity}
            while True:
                current = multiply(current, generator)
                if current == identity:
                    break
                require(current not in powers, "Premature power-cycle repetition")
                powers.add(current)
                require(len(powers) <= group_order, "Nonterminating power cycle")
            histogram[len(powers)] += 1
            subgroup_sets.add(frozenset(powers))
    count = len(subgroup_sets)
    weighted = sum((Fraction(number, totient(order))
                    for order, number in histogram.items()), Fraction())
    # The 60-element A5 factor is coprime to these groups. Its cyclic count
    # is derived separately above; the uniform coprime product rule is
    # proved in the accompanying internal check, not inferred from examples.
    full_cyclic_count = 32 * count
    support = prime_support(60 * group_order)
    eta = Fraction(full_cyclic_count, 2**len(support))
    require(sum(histogram.values()) == group_order, "Incomplete element census")
    require(weighted == count, "Distinct cyclic sets and totient sum disagree")
    require(count == expected_count, "Unexpected semidirect cyclic count")
    require(eta == expected_eta, "Unexpected A5-product normalized count")
    return {"p": p, "dimension": dimension, "multipliers": list(multipliers),
            "m": m, "semidirect_order": group_order,
            "literal_cyclic_subgroups": count,
            "exact_generator_weight_sum": str(weighted),
            "element_order_histogram": dict(sorted(histogram.items())),
            "a5_product_cyclic_subgroups": full_cyclic_count,
            "a5_product_prime_support": sorted(support), "eta": str(eta)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    a5 = a5_weight_count()
    cases = [
        (23, (2,), 11, 25, 25),
        (23, (2,), 121, 27, 27),
        (23, (2,), 77, 50, 25),
        (23, (1,), 121, 6, 6),
        (23, (2, 1), 11, 71, 71),
        (7, (1, 1), 11, 18, 18),
        (7, (1,), 1, 2, 4),
    ]
    result = {
        "status": "all independent Hall finite controls passed",
        "author": "Iris / studio-researcher-2, researcher",
        "checked_author_artifact_sha256":
            "208096e0a2ba2021dbb713d7ef0741bd4d9b74e6c61bfeb17623d0fd4cd91ee4",
        "scope": "literal semidirect fixtures plus separately derived A5 factor; uniform proof in report",
        "a5": a5,
        "fixtures": [diagonal_semidirect(*case) for case in cases],
    }
    output = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
