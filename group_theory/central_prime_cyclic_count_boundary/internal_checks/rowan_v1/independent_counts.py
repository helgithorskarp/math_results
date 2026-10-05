#!/usr/bin/env python3
"""Rowan's independent arithmetic/structural controls of Iris's v1 artifact.

Uses cycle decomposition and gcd/lcm orders, not Iris's literal powers or
cyclic-subgroup sets. The source fixture hash is checked before comparison.
Standard-library exact arithmetic, one process. This is an internal check.
"""

import hashlib
import json
from collections import Counter, deque
from fractions import Fraction
from itertools import permutations, product
from math import gcd, lcm
from pathlib import Path


INPUT_SHA256 = "707fbaf9de8a012d4d4cda68a51a10c3406fae8a3a2953ab27244a451f08705d"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def phi(n):
    # Direct coprime enumeration: a different totient algorithm from Iris.
    return sum(gcd(k, n) == 1 for k in range(1, n + 1))


def omega(n):
    primes = set()
    for d in range(2, n + 1):
        if d * d > n:
            break
        while n % d == 0:
            primes.add(d)
            n //= d
    if n > 1:
        primes.add(n)
    return len(primes)


def compose(a, b):
    return tuple(a[b[i]] for i in range(5))


def inverse(a):
    return tuple(a.index(i) for i in range(5))


def cycle_lengths(a):
    remaining, lengths = set(range(5)), []
    while remaining:
        x = min(remaining)
        length = 0
        while x in remaining:
            remaining.remove(x)
            length += 1
            x = a[x]
        lengths.append(length)
    return lengths


def a5_controls():
    # Sign comes from cycle lengths, independently of inversion parity.
    elements = [a for a in permutations(range(5))
                if (5 - len(cycle_lengths(a))) % 2 == 0]
    histogram = Counter(lcm(*cycle_lengths(a)) for a in elements)
    require(histogram == Counter({1: 1, 2: 15, 3: 20, 5: 24}),
            "A5 cycle-type histogram failed")
    identity = tuple(range(5))
    x, y = (1, 0, 3, 2, 4), (1, 0, 4, 3, 2)
    commutator = compose(compose(compose(x, y), inverse(x)), inverse(y))
    require(sorted(cycle_lengths(commutator)) == [1, 1, 3],
            "chosen commutator is not a 3-cycle")
    conjugates = {compose(compose(a, commutator), inverse(a)) for a in elements}
    require(len(conjugates) == 20, "3-cycle conjugacy orbit failed")
    closure, pending = {identity}, deque([identity])
    while pending:
        a = pending.popleft()
        for b in conjugates:
            c = compose(a, b)
            if c not in closure:
                closure.add(c)
                pending.append(c)
    require(closure == set(elements), "commutator conjugates do not generate A5")
    center = [a for a in elements
              if all(compose(a, b) == compose(b, a) for b in conjugates)]
    require(center == [identity], "centralizer of generating 3-cycles failed")
    return histogram, {
        "cycle_type_order_histogram": dict(sorted(histogram.items())),
        "commutator_conjugacy_orbit_size": len(conjugates),
        "derived_subgroup_size": len(closure), "center_size": len(center),
    }


def arithmetic_fixture(moduli, a5_histogram, sampled=()):
    coordinates = list(product(*(range(n) for n in moduli)))
    hist = Counter()
    for v in coordinates:
        abelian_order = lcm(*(n // gcd(n, value) for n, value in zip(moduli, v)))
        for e, multiplicity in a5_histogram.items():
            hist[lcm(e, abelian_order)] += multiplicity
    group_order = 60 * len(coordinates)
    require(sum(hist.values()) == group_order, "arithmetic census is incomplete")
    weighted = sum((Fraction(number, phi(e)) for e, number in hist.items()), Fraction(0))
    require(weighted.denominator == 1, "cyclic count is not integral")
    return {
        "order": group_order, "cyclic_subgroups": weighted.numerator,
        "eta": str(weighted / 2 ** omega(group_order)),
        "omega": omega(group_order), "generator_weight_sum": str(weighted),
        "element_order_histogram": {str(e): n for e, n in sorted(hist.items())},
        "quotient_generator_coset_orders": [
            lcm(*(n // gcd(n, value) for n, value in zip(moduli, v))) for v in sampled
        ],
    }


def main():
    path = Path(__file__).with_name("IRIS_FIXTURES_v1.json")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == INPUT_SHA256,
            "Iris fixture version does not match the transferred hash")
    reference = json.loads(raw)
    histogram, structural = a5_controls()
    require(reference["a5_structural_controls"]["derived_subgroup_size"] == 60
            and reference["a5_structural_controls"]["center_size"] == 1,
            "Iris structural output mismatch")
    comparisons = []
    for entry in reference["fixtures"]:
        moduli = entry["moduli"]
        if moduli == [49]:
            sampled = [(1 + 7*k,) for k in range(7)]
        elif moduli == [7, 7]:
            sampled = [(1, k) for k in range(7)]
        else:
            sampled = []
        actual = arithmetic_fixture(moduli, histogram, sampled)
        for field, value in actual.items():
            require(entry[field] == value,
                    entry["name"] + " mismatch in " + field)
        comparisons.append({"name": entry["name"], **actual})
    changed = []
    # New primes, higher exponent and a second squared prime are separate
    # inputs, not merely another execution of the author's examples.
    for moduli, expected_eta in [
        ((121,), 6), ((11, 11), 26),
        ((1331,), 8), ((121, 11), 48),
        ((49, 121), 9), ((7, 7, 121), 27),
    ]:
        actual = arithmetic_fixture(moduli, histogram)
        require(Fraction(actual["eta"]) == expected_eta,
                "changed-input boundary formula failed")
        changed.append({"moduli": moduli, **actual})
    print(json.dumps({
        "status": "INDEPENDENT_FINITE_CONTROLS_PASS",
        "author": "Rowan / studio-researcher-4, researcher",
        "input_sha256": INPUT_SHA256,
        "method": "cycle decomposition and gcd/lcm coordinates; exact totient sums",
        "a5_structural_controls": structural,
        "all_author_fixture_entries_reproduced": len(comparisons),
        "author_fixture_comparisons": comparisons,
        "changed_input_fixtures": changed,
        "scope": "internal check of finite evidence; uniform argument separately audited",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
