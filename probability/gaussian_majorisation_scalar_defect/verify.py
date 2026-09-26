#!/usr/bin/env python3
"""Exact algebra and fixture audit. Does not prove the analytic transfers."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    result = dict(a)
    for k, v in b.items():
        result[k] = result.get(k, Q(0)) + v
        if result[k] == 0:
            del result[k]
    return result


def scale(a, c):
    return {k: v * c for k, v in a.items() if v * c}


def mul(a, b):
    result = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = tuple(x + y for x, y in zip(ka, kb))
            result[k] = result.get(k, Q(0)) + va * vb
    return {k: v for k, v in result.items() if v}


def square(a):
    return mul(a, a)


def poly_identity():
    # Variables u1,u2,v1,v2,r,s,t. Coefficients are exact rationals.
    dim = 7
    one = {(0,) * dim: Q(1)}
    variables = []
    for i in range(dim):
        power = [0] * dim
        power[i] = 1
        variables.append({tuple(power): Q(1)})
    u1, u2, v1, v2, r, s, t = variables
    omt = add(one, scale(t, -1))
    uu, vv = add(square(u1), square(u2)), add(square(v1), square(v2))
    X, Y = add(uu, square(r)), add(vv, square(s))
    b = square(add(r, scale(s, -1)))
    left = add(add(mul(omt, uu), mul(t, vv)),
               square(add(mul(omt, r), mul(t, s))))
    right = add(add(mul(omt, X), mul(t, Y)), scale(mul(mul(t, omt), b), -1))
    require(left == right, "interpolation identity")
    derivative = {}
    for power, coeff in left.items():
        if power[-1]:
            new = power[:-1] + (power[-1] - 1,)
            derivative[new] = derivative.get(new, Q(0)) + coeff * power[-1]
    formula = add(add(scale(X, -1), Y), mul(add(scale(t, 2), scale(one, -1)), b))
    require(derivative == formula, "derivative identity")
    # Endpoint derivative minus derivative is exactly 2(1-t)b.
    endpoint = add(add(scale(X, -1), Y), b)
    require(add(endpoint, scale(derivative, -1)) == scale(mul(omt, b), 2),
            "endpoint controls derivative")
    return len(left)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def rank(rows):
    a = [list(map(Q, row)) for row in rows]
    if not a:
        return 0
    ncol, pivot = len(a[0]), 0
    for col in range(ncol):
        j = next((j for j in range(pivot, len(a)) if a[j][col]), None)
        if j is None:
            continue
        a[pivot], a[j] = a[j], a[pivot]
        c = a[pivot][col]
        a[pivot] = [x / c for x in a[pivot]]
        for k in range(len(a)):
            if k != pivot:
                c = a[k][col]
                a[k] = [x - c * y for x, y in zip(a[k], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def det(rows):
    n = len(rows)
    require(all(len(row) == n for row in rows), "square determinant")
    if not n:
        return Q(1)
    if n == 1:
        return rows[0][0]
    return sum(((-1) ** j * rows[0][j] *
                det([row[:j] + row[j + 1:] for row in rows[1:]])
                for j in range(n)), Q(0))


def T(p):
    x, y, z = p
    return (abs(x) / 2 + y / 20,
            abs(y) / 2 + z / 20,
            z / 2 + abs(x + 2 * y + 2 * z) / 60)


def certify_pair(x, xp, y, yp):
    dx, dy = sub(x, xp), sub(y, yp)
    distance_loss = dot(dx, dx) - dot(dy, dy)
    scalar_cost = (dx[2] - dy[2]) ** 2
    require(distance_loss >= scalar_cost, "scalar criterion failed")
    return distance_loss - scalar_cost


def audit():
    terms = poly_identity()
    bounds = []
    for q, eps, expected in [
        (Q(0), Q(0), True), (Q(1), Q(0), True),
        (Q(2, 5), Q(1, 5), True), (Q(3, 5), Q(1, 5), True),
        (Q(1, 2), Q(1, 10), True), (Q(1, 2), Q(1, 4), False),
    ]:
        lhs = (q + eps) ** 2 + (1 - q + eps) ** 2
        require((lhs <= 1) == (eps * eps + eps <= q * (1 - q)),
                "quadratic budget equivalence")
        require((lhs <= 1) == expected, "budget boundary case")
        bounds.append([str(q), str(eps), str(lhs), expected])

    source = [tuple(map(Q, p)) for p in
              [(0, 0, 0), (1, 0, 0), (-2, 0, 0), (0, 1, 0),
               (0, -2, 0), (0, 0, 1), (0, 0, -2)]]
    target = [T(p) for p in source]
    explicit = [
        (0, 0, 0), (Q(1, 2), 0, Q(1, 60)), (1, 0, Q(1, 30)),
        (Q(1, 20), Q(1, 2), Q(1, 30)), (Q(-1, 10), 1, Q(1, 15)),
        (0, Q(1, 20), Q(8, 15)), (0, Q(-1, 10), Q(-14, 15)),
    ]
    require(target == explicit, "target list")
    require(len(set(target)) == 7, "injective fixture")
    margin_ratios = []
    for i, j in combinations(range(7), 2):
        margin = certify_pair(source[i], source[j], target[i], target[j])
        dx = sub(source[i], source[j])
        ratio = margin / dot(dx, dx)
        require(ratio >= Q(7, 25), "uniform margin")
        margin_ratios.append(ratio)
    paired = [x + y for x, y in zip(source[1:], target[1:])]
    paired_det = det(paired)
    require(rank(paired) == 6 and paired_det != 0, "paired rank six")
    displacement = [sub(x, y) for x, y in zip(source, target)]
    require(rank(displacement) == 3, "displacement span")
    sums = [tuple(2 * a + b for a, b in zip(paired[i], paired[i + 1]))
            for i in (0, 2, 4)]
    require(all(row[:3] == (0, 0, 0) for row in sums), "zero input sums")
    require(rank([row[3:] for row in sums]) == 3, "target sum independence")

    # Derivative differences used in the coordinate obstruction.
    def jac(sx, sy, eta):
        return [(Q(sx, 2), Q(1, 20), Q(0)),
                (Q(0), Q(sy, 2), Q(1, 20)),
                (Q(eta, 60), Q(eta, 30), Q(1, 2) + Q(eta, 30))]
    jacobians = {(sx, sy, eta): jac(sx, sy, eta)
                 for sx, sy, eta in product([-1, 1], repeat=3)}
    for sy, eta in product([-1, 1], repeat=2):
        d = [sub(a, b) for a, b in
             zip(jacobians[1, sy, eta], jacobians[-1, sy, eta])]
        require(d == [(1, 0, 0), (0, 0, 0), (0, 0, 0)], "E11 difference")
    for sx, eta in product([-1, 1], repeat=2):
        d = [sub(a, b) for a, b in
             zip(jacobians[sx, 1, eta], jacobians[sx, -1, eta])]
        require(d == [(0, 0, 0), (0, 1, 0), (0, 0, 0)], "E22 difference")
    require(all(j[0][1] == Q(1, 20) for j in jacobians.values()), "off-diagonal")

    A = [(1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1)]
    B = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)]
    require(rank(A) == rank(B) == 3, "cone spans")
    equations = [a + tuple(-v for v in a) for a in A]
    equations += [b + b for b in B]
    require(rank(equations) == 6, "no nonzero scalar-coordinate certificate")

    rejected = False
    try:
        certify_pair((Q(0), Q(0), Q(1)), (Q(0),) * 3,
                     (Q(0), Q(0), Q(-1)), (Q(0),) * 3)
    except ValueError:
        rejected = True
    require(rejected, "bad certificate accepted")
    return {
        "status": "EXACT_SCALAR_DEFECT_AUDIT_PASSED",
        "symbolic_norm_polynomial_terms": terms,
        "budget_boundaries": bounds,
        "source": [[str(v) for v in p] for p in source],
        "target": [[str(v) for v in p] for p in target],
        "fixture_pairs": len(margin_ratios),
        "minimum_scalar_margin_ratio": str(min(margin_ratios)),
        "uniform_proved_margin": "7/25",
        "paired_rank": 6,
        "paired_determinant": str(paired_det),
        "displacement_rank": 3,
        "jacobian_sign_regions": 8,
        "cone_constraint_rank": 6,
        "false_certificate_rejected": rejected,
        "trust_boundary": "Exact finite algebra only; analytic transfer proof is in PROOF.md.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = json.dumps(audit(), indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(result == expected, "EXPECTED.json differs")
        print("PASS " + hashlib.sha256(result.encode()).hexdigest())
    else:
        print(result, end="")
