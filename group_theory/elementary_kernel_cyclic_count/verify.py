#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; no all-groups census or CFSG input."""

import argparse
import hashlib
import json
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
from math import isqrt
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def phi(n):
    require(n > 0, "nonpositive totient input")
    result, rest, p = n, n, 2
    while p * p <= rest:
        if rest % p == 0:
            result -= result // p
            while rest % p == 0:
                rest //= p
        p += 1
    return result - result // rest if rest > 1 else result


def prime(n):
    return n >= 2 and all(n % k for k in range(2, isqrt(n) + 1))


def omega(n):
    require(n > 0, "nonpositive group order")
    count, p = 0, 2
    while p * p <= n:
        if n % p == 0:
            count += 1
            while n % p == 0:
                n //= p
        p += 1
    return count + int(n > 1)


def digest(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass
class Group:
    name: str
    elements: tuple
    identity: object
    multiply: object
    generators: tuple


@dataclass
class Extension:
    name: str
    p: int
    dimension: int
    group: Group
    quotient: Group
    project: object
    embed: object


def power(group, x, exponent):
    require(exponent >= 0, "negative power")
    result = group.identity
    while exponent:
        if exponent & 1:
            result = group.multiply(result, x)
        x = group.multiply(x, x)
        exponent //= 2
    return result


def group_data(group):
    """Literal subgroup sets and generator entries, independent of norm formulas."""
    elements = group.elements
    index = {x: i for i, x in enumerate(elements)}
    require(len(index) == len(elements), "duplicate group elements")
    require(group.identity in index, "missing identity")
    generated, pending = {group.identity}, deque([group.identity])
    while pending:
        x = pending.popleft()
        for s in group.generators:
            y = group.multiply(x, s)
            require(y in index, "generator multiplication escaped domain")
            if y not in generated:
                generated.add(y)
                pending.append(y)
    require(generated == set(index), "declared generators do not generate group")
    orders, inverses, generators = {}, {}, Counter()
    for x in elements:
        require(group.multiply(group.identity, x) == x
                == group.multiply(x, group.identity), "identity law failed")
        current, powers = group.identity, []
        while not powers or current != group.identity:
            require(current in index, "power multiplication escaped domain")
            require(len(powers) < len(elements), "power walk did not close")
            powers.append(index[current])
            previous = current
            current = group.multiply(current, x)
        require(len(set(powers)) == len(powers), "repeated nonidentity power")
        orders[x] = len(powers)
        inverses[x] = previous
        subgroup = tuple(sorted(powers))
        generators[subgroup] += 1
    for subgroup, number in generators.items():
        require(number == phi(len(subgroup)), "subgroup generator count failed")
    hist = Counter(orders.values())
    require(sum(Fraction(n, phi(e)) for e, n in hist.items()) == len(generators),
            "literal subgroup and element-order count disagree")
    return {
        "order": len(elements),
        "cyclic_subgroups": len(generators),
        "eta": str(Fraction(len(generators), 2 ** omega(len(elements)))),
        "element_order_histogram": sorted(hist.items()),
        "cyclic_subgroup_order_histogram": sorted(
            Counter(map(len, generators)).items()),
        "cyclic_subgroup_sets_sha256": digest(sorted(generators)),
    }, orders, inverses


def eye(d):
    return tuple(tuple(int(i == j) for j in range(d)) for i in range(d))


def matrix_multiply(a, b, p):
    return tuple(tuple(sum(x * y for x, y in zip(row, column)) % p
                       for column in zip(*b)) for row in a)


def matrix_vector(a, v, p):
    return tuple(sum(x * y for x, y in zip(row, v)) % p for row in a)


def rank(a, p):
    rows = [list(row) for row in a]
    require(rows and all(len(row) == len(rows[0]) for row in rows),
            "malformed rank matrix")
    r = 0
    for col in range(len(rows[0])):
        pivot = next((i for i in range(r, len(rows)) if rows[i][col] % p), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inverse = pow(rows[r][col] % p, -1, p)
        rows[r] = [value * inverse % p for value in rows[r]]
        for i in range(len(rows)):
            if i != r:
                factor = rows[i][col] % p
                rows[i] = [(x - factor * y) % p
                           for x, y in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def audit(extension):
    p, d = extension.p, extension.dimension
    require(prime(p), "kernel characteristic is not prime")
    require(d >= 1, "kernel dimension is not positive")
    g, q = extension.group, extension.quotient
    vectors = tuple(product(range(p), repeat=d))
    zero = (0,) * d
    kernel = {v: extension.embed(v) for v in vectors}
    coordinates = {x: v for v, x in kernel.items()}
    require(len(coordinates) == p ** d, "kernel embedding is not injective")
    require(kernel[zero] == g.identity, "kernel identity failed")
    for v in vectors:
        for w in vectors:
            added = tuple((x + y) % p for x, y in zip(v, w))
            require(g.multiply(kernel[v], kernel[w]) == kernel[added],
                    "kernel embedding does not preserve vector addition")
    g_data, g_orders, g_inverses = group_data(g)
    q_data, q_orders, _ = group_data(q)
    fibers = {h: [] for h in q.elements}
    require(extension.project(g.identity) == q.identity, "projection identity failed")
    for x in g.elements:
        h = extension.project(x)
        require(h in fibers, "projection escaped quotient")
        fibers[h].append(x)
        # Every element is a word in the validated generators, so these
        # edge identities imply the homomorphism property for all words.
        for s in g.generators:
            require(extension.project(g.multiply(x, s)) ==
                    q.multiply(h, extension.project(s)),
                    "projection is not a homomorphism on generator edges")
    require(set(fibers[q.identity]) == set(coordinates), "wrong projection kernel")
    require(all(len(fiber) == p ** d for fiber in fibers.values()),
            "quotient fibers have wrong size")

    identity = eye(d)
    a_sum, b_sum = Fraction(0), Fraction(0)
    coprime_defect, divisible_defect = Fraction(0), Fraction(0)
    cosets = []
    all_coprime_trivial, all_divisible_long = True, True
    for number, h in enumerate(q.elements):
        e = q_orders[h]
        x = fibers[h][0]
        x_inverse = g_inverses[x]
        columns = []
        for j in range(d):
            basis = tuple(int(i == j) for i in range(d))
            image = g.multiply(g.multiply(x, kernel[basis]), x_inverse)
            require(image in coordinates, "kernel is not normal")
            columns.append(coordinates[image])
        action = tuple(tuple(columns[j][i] for j in range(d)) for i in range(d))
        require(rank(action, p) == d, "singular conjugation action")
        for v in vectors:
            image = g.multiply(g.multiply(x, kernel[v]), x_inverse)
            require(image == kernel[matrix_vector(action, v, p)],
                    "conjugation action is not the derived linear map")
        fixed = d - rank(tuple(tuple((action[i][j] - identity[i][j]) % p
                                    for j in range(d)) for i in range(d)), p)
        action_power = identity
        norm = [[0] * d for _ in range(d)]
        for _ in range(e):
            norm = [[(norm[i][j] + action_power[i][j]) % p
                     for j in range(d)] for i in range(d)]
            action_power = matrix_multiply(action_power, action, p)
        require(action_power == identity, "quotient order does not annihilate action")
        a_element = power(g, x, e)
        require(a_element in coordinates, "lift power escaped kernel")
        a = coordinates[a_element]
        norm_rank = rank(norm, p)
        augmented = [row + [-a[i] % p] for i, row in enumerate(norm)]
        short = (p ** (d - norm_rank)
                 if rank(augmented, p) == norm_rank else 0)
        actual_orders = Counter(g_orders[y] for y in fibers[h])
        predicted_orders = Counter()
        if short:
            predicted_orders[e] = short
        if short < p ** d:
            predicted_orders[p * e] = p ** d - short
        require(actual_orders == predicted_orders, "affine norm/order entries disagree")
        for v in vectors:
            y = g.multiply(kernel[v], x)
            require(y in fibers[h], "kernel coset parameterization failed")
            predicted_power = tuple((u + w) % p
                                    for u, w in zip(a, matrix_vector(norm, v, p)))
            require(power(g, y, e) == kernel[predicted_power],
                    "affine norm/power entry failed")
        weight = sum(Fraction(n, phi(order)) for order, n in actual_orders.items())
        if e % p:
            a_sum += Fraction(1, phi(e))
            require(short == p ** (d - fixed), "coprime fixed-space count failed")
            defect = Fraction((p - 2) * (p ** (d - fixed) - 1),
                              (p - 1) * phi(e))
            coprime_defect += defect
            all_coprime_trivial &= fixed == d
        else:
            b_sum += Fraction(1, phi(e))
            defect = Fraction((p - 1) * short, p * phi(e))
            divisible_defect += defect
            all_divisible_long &= short == 0
        cosets.append({
            "quotient_index": number, "quotient_order": e,
            "fixed_dimension": fixed, "action": action,
            "lift_power": a, "norm": norm, "norm_rank": norm_rank,
            "short_lifts": short, "lift_orders": sorted(actual_orders.items()),
            "weight": str(weight), "defect": str(defect),
        })
    c_v = 1 + (p ** d - 1) // (p - 1)
    lower = c_v * a_sum + p ** (d - 1) * b_sum
    require(g_data["cyclic_subgroups"] == lower + coprime_defect + divisible_defect,
            "exact total defect formula failed")
    require(g_data["cyclic_subgroups"] >= lower, "lower bound failed")
    equality = g_data["cyclic_subgroups"] == lower
    require(equality == ((p == 2 or all_coprime_trivial) and all_divisible_long),
            "equality conditions failed")
    return {
        "name": extension.name, "p": p, "dimension": d,
        "group": g_data, "quotient": q_data,
        "A_p": str(a_sum), "B_p": str(b_sum), "lower_bound": str(lower),
        "coprime_defect": str(coprime_defect),
        "divisible_defect": str(divisible_defect), "equality": equality,
        "coprime_actions_all_trivial": all_coprime_trivial,
        "divisible_cosets_all_long": all_divisible_long,
        "coset_entries_sha256": digest(cosets),
    }, cosets


def cyclic(n):
    return Group("C" + str(n), tuple(range(n)), 0,
                 lambda x, y: (x + y) % n, (1,) if n > 1 else ())


def abelian(moduli):
    moduli = tuple(moduli)
    zero = (0,) * len(moduli)
    return Group("x".join("C" + str(n) for n in moduli),
                 tuple(product(*(range(n) for n in moduli))), zero,
                 lambda v, w: tuple((x + y) % n for x, y, n in zip(v, w, moduli)),
                 tuple(tuple(int(i == j) for i in range(len(moduli)))
                       for j in range(len(moduli))))


def direct_product(a, b):
    return Group(a.name + "_x_" + b.name, tuple(product(a.elements, b.elements)),
                 (a.identity, b.identity),
                 lambda x, y: (a.multiply(x[0], y[0]), b.multiply(x[1], y[1])),
                 tuple((s, b.identity) for s in a.generators)
                 + tuple((a.identity, s) for s in b.generators))


def cyclic_tower(p, exponent):
    n, q = p ** exponent, cyclic(p ** (exponent - 1))
    return Extension("C%d_over_C%d" % (n, len(q.elements)), p, 1,
                     cyclic(n), q, lambda x: x % len(q.elements),
                     lambda v: len(q.elements) * v[0])


def quaternion_or_dihedral(quaternion):
    g = Group("Q8" if quaternion else "D8", tuple(product(range(4), range(2))),
              (0, 0),
              lambda x, y: ((x[0] + (-1 if x[1] else 1) * y[0]
                             + (2 * x[1] * y[1] if quaternion else 0)) % 4,
                            (x[1] + y[1]) % 2), ((1, 0), (0, 1)))
    return Extension(g.name + "_central_C2", 2, 1, g, abelian((2, 2)),
                     lambda x: (x[0] % 2, x[1]), lambda v: (2 * v[0], 0))


def semidirect(p, d, matrix, m, name):
    powers, current = [], eye(d)
    for _ in range(m):
        powers.append(current)
        current = matrix_multiply(current, matrix, p)
    require(current == eye(d), "action does not have declared complement period")
    vectors, zero = tuple(product(range(p), repeat=d)), (0,) * d

    def multiply(x, y):
        image = matrix_vector(powers[x[1]], y[0], p)
        return tuple((a + b) % p for a, b in zip(x[0], image)), (x[1] + y[1]) % m

    g = Group(name, tuple(product(vectors, range(m))), (zero, 0), multiply,
              tuple((tuple(int(i == j) for i in range(d)), 0) for j in range(d))
              + ((zero, 1),))
    return Extension(name, p, d, g, cyclic(m), lambda x: x[1], lambda v: (v, 0))


def heisenberg(p):
    g = Group("Heisenberg_F%d" % p, tuple(product(range(p), repeat=3)), (0, 0, 0),
              lambda x, y: ((x[0] + y[0]) % p, (x[1] + y[1]) % p,
                            (x[2] + y[2] + x[0] * y[1]) % p),
              ((1, 0, 0), (0, 1, 0)))
    return Extension(g.name + "_central_C%d" % p, p, 1, g, abelian((p, p)),
                     lambda x: x[:2], lambda v: (0, 0, v[0]))


def a5_group():
    elements = tuple(a for a in permutations(range(5))
                     if sum(a[i] > a[j] for i in range(5)
                            for j in range(i + 1, 5)) % 2 == 0)
    return Group("A5", elements, tuple(range(5)),
                 lambda a, b: tuple(a[b[i]] for i in range(5)),
                 ((1, 2, 0, 3, 4), (1, 2, 3, 4, 0)))


def sl2_extension():
    def multiply(a, b):
        return ((a[0] * b[0] + a[1] * b[2]) % 5,
                (a[0] * b[1] + a[1] * b[3]) % 5,
                (a[2] * b[0] + a[3] * b[2]) % 5,
                (a[2] * b[1] + a[3] * b[3]) % 5)

    elements = tuple(a for a in product(range(5), repeat=4)
                     if (a[0] * a[3] - a[1] * a[2]) % 5 == 1)
    identity, generators = (1, 0, 0, 1), ((1, 1, 0, 1), (1, 0, 1, 1))
    g = Group("SL2_F5", elements, identity, multiply, generators)
    canonical = lambda a: min(a, tuple(-x % 5 for x in a))
    q = Group("PSL2_F5", tuple(sorted({canonical(a) for a in elements})),
              canonical(identity), lambda a, b: canonical(multiply(a, b)),
              tuple(canonical(a) for a in generators))
    return Extension("SL2_F5_central_C2", 2, 1, g, q, canonical,
                     lambda v: identity if v[0] == 0 else (4, 0, 0, 4))


def fixtures():
    cases = [cyclic_tower(p, 2) for p in (2, 3, 5, 7)]
    cases += [cyclic_tower(3, 3), cyclic_tower(7, 3)]
    cases.append(Extension("C2_x_C2_over_C2", 2, 1, abelian((2, 2)), cyclic(2),
                           lambda x: x[0], lambda v: (0, v[0])))
    cases += [quaternion_or_dihedral(False), quaternion_or_dihedral(True)]
    cases += [
        semidirect(2, 2, ((0, 1), (1, 1)), 3, "A4_V4_over_C3"),
        semidirect(3, 1, ((2,),), 2, "S3_C3_over_C2"),
        semidirect(5, 2, ((1, 0), (0, 4)), 4, "F5_squared_nonfaithful_C4"),
        semidirect(3, 2, ((1, 1), (0, 1)), 3, "F3_squared_unipotent_C3"),
        heisenberg(3), heisenberg(5), sl2_extension(),
    ]
    a5 = a5_group()
    for p in (2, 3, 5, 7):
        g = direct_product(a5, cyclic(p))
        cases.append(Extension(g.name + "_over_A5", p, 1, g, a5,
                               lambda x: x[0], lambda v: (a5.identity, v[0])))
    g = direct_product(a5, abelian((2, 2)))
    cases.append(Extension(g.name + "_over_A5", 2, 2, g, a5,
                           lambda x: x[0], lambda v: (a5.identity, v)))
    g, q = direct_product(a5, cyclic(49)), direct_product(a5, cyclic(7))
    cases.append(Extension("A5_x_C49_over_A5_x_C7", 7, 1, g, q,
                           lambda x: (x[0], x[1] % 7),
                           lambda v: (a5.identity, 7 * v[0])))
    return cases


def negative_controls():
    controls = []
    cases = [
        (Extension("invalid_C4_as_F2_squared", 2, 2, cyclic(4), cyclic(1),
                   lambda x: 0, lambda v: v[0] + 2 * v[1]),
         "kernel embedding does not preserve vector addition"),
        (Extension("invalid_C4_projection", 2, 1, cyclic(4), cyclic(2),
                   lambda x: x // 2, lambda v: 2 * v[0]),
         "projection is not a homomorphism on generator edges"),
        (Extension("invalid_composite_characteristic", 4, 1, cyclic(4), cyclic(1),
                   lambda x: 0, lambda v: v[0]),
         "kernel characteristic is not prime"),
    ]
    for case, expected in cases:
        try:
            audit(case)
        except ValueError as error:
            require(str(error) == expected, "negative control failed for wrong reason")
            controls.append({"name": case.name, "rejection": str(error)})
        else:
            raise ValueError("invalid extension was accepted")
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare all result entries")
    parser.add_argument("--expected", type=Path,
                        default=Path(__file__).with_name("EXPECTED.json"))
    parser.add_argument("--certificate", type=Path, help="optional complete per-coset entries")
    parser.add_argument("--only", help="run a single named fixture")
    args = parser.parse_args()
    require(not (args.only and args.check), "--check requires all fixtures")
    cases = fixtures()
    if args.only:
        cases = [case for case in cases if case.name == args.only]
        require(len(cases) == 1, "unknown or duplicate fixture")
    results, entries = [], {}
    for case in cases:
        result, cosets = audit(case)
        results.append(result)
        entries[case.name] = cosets
    result = {
        "status": "FINITE_CONTROLS_PASS",
        "scope": "exact fixtures; the universal lemma is the written proof",
        "fixture_count": len(results), "fixtures": results,
        "negative_controls": negative_controls(),
    }
    result = json.loads(json.dumps(result))
    if args.check:
        require(json.loads(args.expected.read_text()) == result,
                "expected finite-control evidence mismatch")
    if args.certificate:
        args.certificate.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
