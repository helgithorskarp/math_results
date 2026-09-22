#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; not an all-finite-groups census."""

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from math import gcd, prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def phi(n):
    require(n >= 1, "nonpositive totient input")
    result, rest, p = n, n, 2
    while p * p <= rest:
        if rest % p == 0:
            result -= result // p
            while rest % p == 0:
                rest //= p
        p += 1
    if rest > 1:
        result -= result // rest
    return result


def omega(n):
    require(n >= 1, "nonpositive order")
    count, p = 0, 2
    while p * p <= n:
        if n % p == 0:
            count += 1
            while n % p == 0:
                n //= p
        p += 1
    return count + int(n > 1)


def digest(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def cyclic_data(elements, identity, multiply):
    """Literal powers, followed by entrywise generator/subgroup verification."""
    universe = set(elements)
    require(len(universe) == len(elements), "duplicate group elements")
    require(identity in universe, "identity missing")
    subgroups, element_orders, generators = set(), {}, Counter()
    for g in elements:
        require(multiply(identity, g) == g == multiply(g, identity),
                "identity law failed")
        powers, x = [identity], g
        while x != identity:
            require(x in universe, "multiplication escaped domain")
            require(len(powers) < len(elements), "power walk did not close")
            powers.append(x)
            x = multiply(x, g)
        subgroup = frozenset(powers)
        require(len(subgroup) == len(powers), "repeated nonidentity power")
        element_orders[g] = len(powers)
        subgroups.add(subgroup)
        generators[subgroup] += 1
    for subgroup in subgroups:
        require(generators[subgroup] == phi(len(subgroup)),
                "generator multiplicity failed")
    order_count = Counter(element_orders.values())
    order_sum = sum(Fraction(n, phi(o)) for o, n in order_count.items())
    require(order_sum == len(subgroups), "element/subgroup counts disagree")
    histogram = sorted(Counter(map(len, subgroups)).items())
    return {
        "order": len(elements),
        "cyclic_subgroups": len(subgroups),
        "subgroup_order_histogram": histogram,
        "element_order_histogram": sorted(order_count.items()),
        "eta": str(Fraction(len(subgroups), 2 ** omega(len(elements)))),
    }, element_orders


def perm_mul(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def alternating(n):
    return [
        a for a in permutations(range(n))
        if sum(a[i] > a[j] for i in range(n) for j in range(i + 1, n)) % 2 == 0
    ]


def eye(d):
    return tuple(int(i == j) for i in range(d) for j in range(d))


def mat_mul(a, b, p, d):
    return tuple(sum(a[i * d + k] * b[k * d + j] for k in range(d)) % p
                 for i in range(d) for j in range(d))


def mat_vec(a, v, p, d):
    return tuple(sum(a[i * d + j] * v[j] for j in range(d)) % p
                 for i in range(d))


def rank(a, p, d):
    rows = [list(a[i * d:(i + 1) * d]) for i in range(d)]
    r = 0
    for col in range(d):
        pivot = next((i for i in range(r, d) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][col], -1, p)
        rows[r] = [x * inv % p for x in rows[r]]
        for i in range(d):
            if i != r:
                coeff = rows[i][col]
                rows[i] = [(x - coeff * y) % p
                           for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def matrix_powers(a, p, d):
    ident, powers = eye(d), [eye(d)]
    bound = prod(p ** d - p ** i for i in range(d))
    x = a
    while x != ident:
        require(len(powers) < bound, "matrix order exceeds GL bound")
        powers.append(x)
        x = mat_mul(x, a, p, d)
    return powers


def extension_check(p, d, h_elements, h_identity, h_mul, actions):
    """Compare literal subgroup sets with the fixed-space formula, per coset."""
    require(gcd(p, len(h_elements)) == 1, "extension is not coprime")
    h_data, h_orders = cyclic_data(h_elements, h_identity, h_mul)
    ident = eye(d)
    require(actions[h_identity] == ident, "identity action failed")
    for h in h_elements:
        require(rank(actions[h], p, d) == d, "singular action matrix")
        for k in h_elements:
            require(actions[h_mul(h, k)] ==
                    mat_mul(actions[h], actions[k], p, d),
                    "action is not a homomorphism")
    vectors = list(product(range(p), repeat=d))
    zero = (0,) * d
    elements = list(product(vectors, h_elements))

    def multiply(x, y):
        v, h = x
        w, k = y
        image = mat_vec(actions[h], w, p, d)
        return tuple((a + b) % p for a, b in zip(v, image)), h_mul(h, k)

    data, orders = cyclic_data(elements, (zero, h_identity), multiply)
    defect = Fraction(0)
    cosets = []
    nontrivial = False
    for h in h_elements:
        a = actions[h]
        fixed = d - rank(tuple((x - y) % p for x, y in zip(a, ident)), p, d)
        fixed_vectors = sum(mat_vec(a, v, p, d) == v for v in vectors)
        require(fixed_vectors == p ** fixed, "rank/fixed-vector disagreement")
        e = h_orders[h]
        actual = Counter(orders[(v, h)] for v in vectors)
        predicted = Counter({e: p ** (d - fixed)})
        if p ** d != p ** (d - fixed):
            predicted[p * e] = p ** d - p ** (d - fixed)
        require(actual == predicted, "coset element-order formula failed")
        defect += Fraction((p - 2) * (p ** (d - fixed) - 1),
                           (p - 1) * phi(e))
        nontrivial |= a != ident
        cosets.append([e, fixed, sorted(actual.items())])
    c_v = 1 + (p ** d - 1) // (p - 1)
    base = c_v * h_data["cyclic_subgroups"]
    require(Fraction(data["cyclic_subgroups"] - base) == defect,
            "exact extension defect failed")
    require((defect == 0) == (p == 2 or not nontrivial),
            "extension equality characterization failed")
    return {
        "p": p, "dimension": d, "complement_order": len(h_elements),
        "cyclic_subgroups": data["cyclic_subgroups"],
        "direct_product_count": base, "defect": str(defect),
        "nontrivial_action": nontrivial, "coset_sha256": digest(cosets),
    }


def cyclic_extension(p, d, matrix, multiplier=1):
    powers = matrix_powers(matrix, p, d)
    m = len(powers) * multiplier
    return extension_check(
        p, d, list(range(m)), 0, lambda h, k: (h + k) % m,
        {h: powers[h % len(powers)] for h in range(m)}
    )


def run():
    fixtures = {}
    a5, id5 = alternating(5), tuple(range(5))
    for name, elements, identity, multiply, expected in [
        ("A5", a5, id5, perm_mul, 32),
        ("S5", list(permutations(range(5))), id5, perm_mul, 67),
        ("A6", alternating(6), tuple(range(6)), perm_mul, 167),
        ("SL2_F5",
         [a for a in product(range(5), repeat=4)
          if (a[0] * a[3] - a[1] * a[2]) % 5 == 1],
         eye(2), lambda a, b: mat_mul(a, b, 5, 2), 49),
    ]:
        data, _ = cyclic_data(elements, identity, multiply)
        require(data["cyclic_subgroups"] == expected, name + " count failed")
        fixtures[name] = data

    def projective(a):
        return min(a, tuple(-x % 5 for x in a))

    projective_elements = sorted({
        projective(a) for a in product(range(5), repeat=4)
        if (a[0] * a[3] - a[1] * a[2]) % 5 == 1
    })
    data, _ = cyclic_data(
        projective_elements, projective(eye(2)),
        lambda a, b: projective(mat_mul(a, b, 5, 2)))
    require(data["cyclic_subgroups"] == 32, "central quotient count failed")
    require(fixtures["SL2_F5"]["cyclic_subgroups"] >=
            data["cyclic_subgroups"] + 1, "strict quotient inequality failed")
    fixtures["PSL2_F5"] = data

    for m in [1, 2, 3, 4, 5, 7, 11, 49, 77]:
        elements = list(product(a5, range(m)))
        data, _ = cyclic_data(
            elements, (id5, 0),
            lambda x, y, m=m: (perm_mul(x[0], y[0]), (x[1] + y[1]) % m)
        )
        squarefree = all(m % (p * p) for p in range(2, m + 1))
        require((data["eta"] == "4") == (squarefree and gcd(m, 30) == 1),
                "A5 product equality failed")
        fixtures["A5_x_C" + str(m)] = data

    data, _ = cyclic_data(
        list(product(a5, a5)), (id5, id5),
        lambda x, y: (perm_mul(x[0], y[0]), perm_mul(x[1], y[1])))
    require(data["eta"] != "4", "two-simple-factor equality")
    fixtures["A5_x_A5"] = data

    census, records = [], []
    # Exhaust all invertible matrices of these sizes with coprime order.
    for p, d in [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2),
                 (5, 1), (7, 1), (11, 1)]:
        invertible, coprime, equality, characteristic_two_nontrivial = 0, 0, 0, 0
        local = []
        for a in product(range(p), repeat=d * d):
            if rank(a, p, d) != d:
                continue
            invertible += 1
            order = len(matrix_powers(a, p, d))
            if order % p == 0:
                continue
            coprime += 1
            record = cyclic_extension(p, d, a)
            record["matrix"] = a
            local.append(record)
            equality += record["defect"] == "0"
            characteristic_two_nontrivial += (
                p == 2 and record["nontrivial_action"])
        require(invertible == prod(p ** d - p ** i for i in range(d)),
                "GL census incomplete")
        records.extend(local)
        census.append({
            "p": p, "dimension": d, "invertible_matrices": invertible,
            "coprime_actions": coprime, "equality_actions": equality,
            "characteristic_two_nontrivial_equalities":
                characteristic_two_nontrivial,
            "entrywise_sha256": digest(local),
        })

    extra = [
        cyclic_extension(5, 1, (4,), multiplier=2),
        cyclic_extension(7, 1, (2,), multiplier=2),
        cyclic_extension(5, 2, (0, 4, 1, 4)),
        cyclic_extension(5, 2, (1, 0, 0, 4)),
    ]
    # Nonabelian complement: S3 on the sum-zero subspace of F5^3,
    # in basis e1-e3, e2-e3.
    h = list(permutations(range(3)))
    actions = {}
    for perm in h:
        cols = []
        for i in range(2):
            cols.append(tuple((int(perm[i] == j) - int(perm[2] == j)) % 5
                              for j in range(2)))
        actions[perm] = tuple(cols[j][i] for i in range(2) for j in range(2))
    extra.append(extension_check(5, 2, h, tuple(range(3)), perm_mul, actions))

    # The order-three unipotent action in characteristic three is outside (5).
    try:
        cyclic_extension(3, 2, (1, 1, 0, 1))
    except RuntimeError as error:
        require(str(error) == "extension is not coprime",
                "wrong rejection for noncoprime control")
    else:
        raise RuntimeError("noncoprime extension was accepted")

    return {
        "status": "VERIFIED",
        "scope": "finite controls; universal result is the written proof",
        "fixtures": fixtures,
        "matrix_action_census": census,
        "additional_extension_cases": extra,
        "total_extensions": len(records) + len(extra),
        "extension_entries_sha256": digest(records + extra),
        "noncoprime_control_rejected": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expected", type=Path,
                        default=Path(__file__).with_name("EXPECTED.json"))
    args = parser.parse_args()
    result = run()
    # Normalize tuples to JSON arrays before an entrywise comparison.
    result = json.loads(json.dumps(result))
    if args.check:
        expected = json.loads(args.expected.read_text())
        require(result == expected, "expected evidence mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
