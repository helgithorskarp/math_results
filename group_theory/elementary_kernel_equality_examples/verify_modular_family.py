#!/usr/bin/env python3
"""Literal controls of the classical modular-family supplement; stdlib exact."""

import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd, isqrt


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def phi(n):
    return sum(gcd(n, k) == 1 for k in range(1, n + 1))


def control(p):
    require(p >= 2 and all(p % k for k in range(2, isqrt(p) + 1)), "p not prime")
    elements, identity = list(product(range(p*p), range(p))), (0, 0)

    def multiply(x, y):
        return ((x[0] + pow(1+p, x[1], p*p)*y[0]) % (p*p),
                (x[1] + y[1]) % p)

    require(pow(1+p, p, p*p) == 1, "invalid multiplier period")
    sets, generators, orders = set(), Counter(), {}
    for g in elements:
        current, members = identity, []
        while not members or current != identity:
            require(current not in members, "premature power repetition")
            require(len(members) < p**3, "power walk failed")
            members.append(current)
            current = multiply(current, g)
        subgroup = frozenset(members)
        sets.add(subgroup)
        generators[subgroup] += 1
        orders[g] = len(members)
    for subgroup in sets:
        require(generators[subgroup] == phi(len(subgroup)), "wrong generators")
    histogram = Counter(orders.values())
    count = sum((Fraction(n, phi(e)) for e, n in histogram.items()), Fraction(0))
    require(count == len(sets), "two count routes disagree")
    kernel = {(p*u, v) for u, v in product(range(p), repeat=2)}
    for u, v, s, t in product(range(p), repeat=4):
        require(multiply((p*u, v), (p*s, t)) ==
                (p*((u+s) % p), (v+t) % p), "kernel not elementary abelian")
    conjugate = multiply(multiply((1, 0), (0, 1)), (p*p-1, 0))
    require(conjugate == (p*(p-1), 1) != (0, 1), "kernel action should be nontrivial")
    cosets = []
    for h in range(p):
        fiber = [g for g in elements if g[0] % p == h]
        require(len(fiber) == p*p, "wrong fiber size")
        local = Counter(orders[g] for g in fiber)
        cosets.append({"quotient_element": h, "lift_orders": sorted(local.items())})
        if h and p != 2:
            require(local == Counter({p*p: p*p}), "odd-p coset has a short lift")
    lower = 2*p+2
    if p == 2:
        require(histogram == Counter({1: 1, 2: 5, 4: 2}) and count == 7,
                "D8 comparison failed")
        require(cosets[1]["lift_orders"] == [(2, 2), (4, 2)], "wrong p=2 lift coset")
        split = True
    else:
        require(histogram == Counter({1: 1, p: p*p-1, p*p: p**3-p*p}),
                "modular-family histogram failed")
        require(count == lower, "odd-p equality failed")
        split = False
    return {
        "p": p, "group_order": p**3, "kernel_order": p*p,
        "kernel_dimension": 2, "kernel_central": False,
        "extension_over_kernel_splits": split,
        "cyclic_subgroups": int(count), "lower_bound": lower,
        "divisible_defect": str(count-lower),
        "element_order_histogram": sorted(histogram.items()),
        "quotient_cosets": cosets,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primes", type=int, nargs="+", default=[2, 3, 5])
    args = parser.parse_args()
    print(json.dumps({"status": "MODULAR_FAMILY_CONTROLS_PASS",
                      "scope": "author controls; independent check pending",
                      "fixtures": [control(p) for p in args.primes]},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
