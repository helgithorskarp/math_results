#!/usr/bin/env python3
"""Independent exact audit for the illumination product criterion.

CPython 3.11+, standard library only.  This imports no target module,
fixture, output, or certificate.  It enumerates finite covering clutters,
solves their primal and dual fractional-cover LPs by exact vertex
enumeration, and computes every ordered product cover on four points.
The universal geometric theorem remains a human proof obligation documented
in REVIEW.md.
"""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def union_all(sets):
    value = 0
    for subset in sets:
        value |= subset
    return value


def maximal_reduction(sets):
    return tuple(subset for subset in sets
                 if not any(subset != other and subset & other == subset
                            for other in sets))


def solve_square(rows, rhs):
    n = len(rhs)
    require(len(rows) == n and all(len(row) == n for row in rows),
            "square system required")
    matrix = [[Fraction(x) for x in row] + [Fraction(b)]
              for row, b in zip(rows, rhs)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if matrix[r][col]), None)
        if pivot is None:
            return None
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [x / scale for x in matrix[col]]
        for r in range(n):
            if r == col or not matrix[r][col]:
                continue
            scale = matrix[r][col]
            matrix[r] = [x - scale * y
                         for x, y in zip(matrix[r], matrix[col])]
    return tuple(row[-1] for row in matrix)


def fractional_cover(n, sets):
    """Return exact optimum, primal weights, and dual weights."""
    sets = tuple(sets)
    require(sets and union_all(sets) == (1 << n) - 1, "covering family required")
    m = len(sets)

    primal_best = None
    primal_weights = None
    # Primal constraints are element coverage equalities or w_j=0 at a vertex.
    primal_constraints = [
        (tuple(int(subset >> i & 1) for subset in sets), Fraction(1))
        for i in range(n)
    ] + [
        (tuple(int(j == k) for j in range(m)), Fraction(0))
        for k in range(m)
    ]
    for active in combinations(primal_constraints, m):
        weights = solve_square([row for row, _ in active], [b for _, b in active])
        if weights is None or any(w < 0 for w in weights):
            continue
        if any(sum(w for subset, w in zip(sets, weights) if subset >> i & 1) < 1
               for i in range(n)):
            continue
        value = sum(weights)
        if primal_best is None or (value, weights) < (primal_best, primal_weights):
            primal_best, primal_weights = value, weights

    dual_best = None
    dual_weights = None
    # Dual constraints are set loads equal to one or z_i=0 at a vertex.
    dual_constraints = [
        (tuple(int(subset >> i & 1) for i in range(n)), Fraction(1))
        for subset in sets
    ] + [
        (tuple(int(i == k) for i in range(n)), Fraction(0))
        for k in range(n)
    ]
    for active in combinations(dual_constraints, n):
        weights = solve_square([row for row, _ in active], [b for _, b in active])
        if weights is None or any(z < 0 for z in weights):
            continue
        if any(sum(z for i, z in enumerate(weights) if subset >> i & 1) > 1
               for subset in sets):
            continue
        value = sum(weights)
        if dual_best is None or value > dual_best or (value == dual_best and weights < dual_weights):
            dual_best, dual_weights = value, weights

    require(primal_best is not None and primal_best == dual_best,
            "primal-dual optimum mismatch")
    return primal_best, primal_weights, dual_weights


def cover_number(n, sets):
    """Exact branch-on-a-required-element set cover."""
    sets = tuple(sets)
    full = (1 << n) - 1
    require(sets and union_all(sets) == full, "covering family required")
    incident = [tuple(subset for subset in sets if subset >> i & 1)
                for i in range(n)]

    @lru_cache(None)
    def recurse(covered):
        if covered == full:
            return 0
        uncovered = full ^ covered
        element = min((i for i in range(n) if uncovered >> i & 1),
                      key=lambda i: sum(bool(subset & uncovered)
                                        for subset in incident[i]))
        return 1 + min(recurse(covered | subset) for subset in incident[element])

    return recurse(0), recurse.cache_info().currsize


def rectangle_product(n, left, right):
    answer = []
    for a, b in product(left, right):
        mask = 0
        for i in range(n):
            if not (a >> i) & 1:
                continue
            for j in range(n):
                if (b >> j) & 1:
                    mask |= 1 << (n * i + j)
        answer.append(mask)
    require(len(set(answer)) == len(answer), "duplicate product class")
    return tuple(answer)


def check_fractional_certificate(n, sets, primal, dual, expected):
    require(all(w >= 0 for w in primal) and all(z >= 0 for z in dual),
            "negative fractional weight")
    require(all(sum(w for subset, w in zip(sets, primal) if subset >> i & 1) >= 1
                for i in range(n)), "primal certificate misses an element")
    require(all(sum(z for i, z in enumerate(dual) if subset >> i & 1) <= 1
                for subset in sets), "dual certificate overloads a set")
    require(sum(primal) == expected == sum(dual), "certificate objective mismatch")


def tensor_certificates(n, left, right, left_data, right_data):
    tau, wp, zd = left_data
    sigma, wq, ze = right_data
    sets = rectangle_product(n, left, right)
    primal = tuple(a * b for a, b in product(wp, wq))
    dual = tuple(a * b for a, b in product(zd, ze))
    check_fractional_certificate(n * n, sets, primal, dual, tau * sigma)
    return sets


def ceiling(value):
    return (value.numerator + value.denominator - 1) // value.denominator


def rational_power_bound(vertices, tau, exponent):
    tau = Fraction(tau)
    require(vertices >= 2 and tau > 1 and exponent >= 1, "power-bound domain")
    return ceiling(tau ** exponent) * (1 + exponent * (vertices - 1).bit_length())


def first_sufficient_exponent(vertices, tau, ordinary):
    require(Fraction(1) < tau < ordinary, "strict fractional gap required")
    exponent = 1
    while rational_power_bound(vertices, tau, exponent) >= ordinary ** exponent:
        exponent += 1
    require(exponent == 1 or
            rational_power_bound(vertices, tau, exponent - 1) >= ordinary ** (exponent - 1),
            "nonminimal sufficient exponent search")
    return exponent, rational_power_bound(vertices, tau, exponent), ordinary ** exponent


def strict_homogeneous_feasible(normals):
    """Solve a.u<0 in R^2 by four exact L1-normalized quadrant intervals."""
    for sign_x, sign_y in product((-1, 1), repeat=2):
        lower, lower_strict = Fraction(0), False
        upper, upper_strict = Fraction(1), False
        possible = True
        # Write u=(sign_x*x, sign_y*(1-x)), 0<=x<=1.
        for a, b in normals:
            coefficient = a * sign_x - b * sign_y
            constant = b * sign_y
            if coefficient == 0:
                if constant >= 0:
                    possible = False
                    break
                continue
            bound = Fraction(-constant, coefficient)
            if coefficient > 0:  # x < bound
                if bound < upper:
                    upper, upper_strict = bound, True
                elif bound == upper:
                    upper_strict = True
            else:  # x > bound
                if bound > lower:
                    lower, lower_strict = bound, True
                elif bound == lower:
                    lower_strict = True
        if not possible or lower > upper:
            continue
        if lower == upper and (lower_strict or upper_strict):
            continue
        x = lower if lower == upper else (lower + upper) / 2
        if not (0 <= x <= 1):
            continue
        witness = (sign_x * x, sign_y * (1 - x))
        if witness != (0, 0) and all(a * witness[0] + b * witness[1] < 0
                                     for a, b in normals):
            return witness
    return None


def pentagon_geometry_audit():
    vertices = ((0, 0), (4, 0), (5, 3), (2, 5), (-1, 3))
    normals = []
    bounds = []
    for p, q in zip(vertices, vertices[1:] + vertices[:1]):
        normal = (q[1] - p[1], p[0] - q[0])
        bound = normal[0] * p[0] + normal[1] * p[1]
        require(all(normal[0] * x[0] + normal[1] * x[1] <= bound
                    for x in vertices), "pentagon orientation or convexity")
        normals.append(normal)
        bounds.append(bound)
    active = [tuple(normal for normal, bound in zip(normals, bounds)
                    if normal[0] * p[0] + normal[1] * p[1] == bound)
              for p in vertices]
    require(all(len(rows) == 2 for rows in active), "nonsimple pentagon vertex")

    feasible_pairs = []
    for i, j in combinations(range(5), 2):
        if strict_homogeneous_feasible(active[i] + active[j]) is not None:
            feasible_pairs.append((i, j))
    wanted_pairs = sorted(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
    require(sorted(feasible_pairs) == wanted_pairs, "maximal incidence is not C5")
    feasible_triples = sum(
        strict_homogeneous_feasible(active[i] + active[j] + active[k]) is not None
        for i, j, k in combinations(range(5), 3)
    )
    require(feasible_triples == 0, "one direction illuminates three vertices")

    directions = ((0, 6), (-4, 2), (-4, -5), (4, -5), (4, 2))
    masks = []
    incidence_checks = 0
    for direction in directions:
        mask = 0
        for i, rows in enumerate(active):
            illuminated = all(a * direction[0] + b * direction[1] < 0 for a, b in rows)
            mask |= int(illuminated) << i
            incidence_checks += 1
        masks.append(mask)
    require(tuple(masks) == tuple((1 << i) | (1 << ((i + 1) % 5))
                                  for i in range(5)), "displayed direction incidence")

    chosen = ((0, 0), (0, 1), (1, 0), (1, 3),
              (2, 2), (3, 1), (3, 4), (4, 3))
    full = (1 << 25) - 1
    products = []
    for i, j in chosen:
        mask = 0
        for x in range(5):
            for y in range(5):
                if masks[i] >> x & 1 and masks[j] >> y & 1:
                    mask |= 1 << (5 * x + y)
        products.append(mask)
    require(union_all(products) == full, "eight-direction square cover")
    deletion_holes = []
    for removed in range(8):
        missing = full ^ union_all(products[:removed] + products[removed + 1:])
        require(missing, "redundant displayed product direction")
        deletion_holes.append(missing.bit_count())
    return {
        "active_normal_checks": 10,
        "feasible_pairs": len(feasible_pairs),
        "feasible_triples": feasible_triples,
        "representative_incidence_checks": incidence_checks,
        "product_vertex_checks": 25,
        "deletion_hole_sizes": deletion_holes,
    }


def enumerate_four_point_clutters():
    full = 15
    raw_count = 0
    clutters = set()
    for code in range(1, 1 << 15):
        family = tuple(subset for subset in range(1, 16)
                       if code >> (subset - 1) & 1)
        if union_all(family) != full:
            continue
        raw_count += 1
        reduced = maximal_reduction(family)
        require(union_all(reduced) == full, "maximal reduction lost coverage")
        clutters.add(reduced)
    return raw_count, tuple(sorted(clutters, key=lambda x: (len(x), x)))


def named_families():
    cycle4 = tuple((1 << i) | (1 << ((i + 1) % 4)) for i in range(4))
    cycle5 = tuple((1 << i) | (1 << ((i + 1) % 5)) for i in range(5))
    fano = (
        0b0000111, 0b0011001, 0b1100001, 0b0101010,
        0b1001100, 0b1010010, 0b0110100,
    )
    answer = {}
    for name, n, family in (
        ("full_set", 4, (15,)),
        ("singletons", 4, (1, 2, 4, 8)),
        ("cycle4", 4, cycle4),
        ("cycle5", 5, cycle5),
        ("fano_lines", 7, fano),
    ):
        tau, primal, dual = fractional_cover(n, family)
        ordinary, _ = cover_number(n, family)
        check_fractional_certificate(n, family, primal, dual, tau)
        row = {"n": n, "classes": len(family), "fractional": str(tau),
               "ordinary": ordinary}
        if 1 < tau < ordinary:
            r, bound, power = first_sufficient_exponent(n, tau, ordinary)
            row["sufficient_exponent"] = r
            row["bound"] = bound
            row["ordinary_power"] = power
        answer[name] = row
    require(answer["full_set"]["fractional"] == "1", "abstract tau=1 boundary")
    require(answer["singletons"]["ordinary"] == 4, "disjoint requirement boundary")
    require(answer["cycle4"]["fractional"] == "2", "even-cycle boundary")
    require(answer["cycle5"]["fractional"] == "5/2", "pentagon boundary")
    require(answer["fano_lines"]["fractional"] == "7/3", "Fano boundary")
    return answer


def run():
    raw_count, clutters = enumerate_four_point_clutters()
    require(raw_count == 32297 and len(clutters) == 114,
            "four-point family completeness count")

    data = {}
    distribution = {}
    digest = sha256()
    maximum_lp_denominator = 1
    gap_clutters = 0
    sufficient_exponents = []
    for family in clutters:
        tau, primal, dual = fractional_cover(4, family)
        ordinary, states = cover_number(4, family)
        check_fractional_certificate(4, family, primal, dual, tau)
        data[family] = (tau, primal, dual, ordinary)
        key = f"tau={tau},I={ordinary}"
        distribution[key] = distribution.get(key, 0) + 1
        maximum_lp_denominator = max(
            maximum_lp_denominator,
            *(x.denominator for x in primal),
            *(x.denominator for x in dual),
        )
        if tau < ordinary:
            gap_clutters += 1
            sufficient_exponents.append(first_sufficient_exponent(4, tau, ordinary)[0])
        digest.update(json.dumps(
            [family, str(tau), ordinary, [str(x) for x in primal],
             [str(x) for x in dual], states], separators=(",", ":")
        ).encode() + b"\n")

    product_checks = 0
    zero_gap_product_checks = 0
    strict_product_pairs = 0
    maximum_product_states = 0
    for left, right in product(clutters, repeat=2):
        tau, wp, zd, il = data[left]
        sigma, wq, ze, ir = data[right]
        rectangles = tensor_certificates(
            4, left, right, (tau, wp, zd), (sigma, wq, ze)
        )
        integer_product, states = cover_number(16, rectangles)
        maximum_product_states = max(maximum_product_states, states)
        require(Fraction(integer_product) >= tau * ir,
                "left fractional mixed bound")
        require(Fraction(integer_product) >= sigma * il,
                "right fractional mixed bound")
        require(integer_product <= il * ir, "product upper bound")
        if tau == il or sigma == ir:
            require(integer_product == il * ir, "zero-gap multiplier failure")
            zero_gap_product_checks += 1
        if integer_product < il * ir:
            strict_product_pairs += 1
        product_checks += 1
        digest.update(json.dumps(
            [left, right, str(tau * sigma), integer_product, states],
            separators=(",", ":")
        ).encode() + b"\n")

    # Exact recurrence boundary behind the rational block estimate.
    decay_checks = 0
    for numerator, denominator, vertices, exponent in (
        (2, 1, 2, 1), (5, 2, 5, 1), (5, 2, 5, 2),
        (7, 3, 7, 1), (7, 3, 7, 2), (2001, 1000, 17, 5),
    ):
        mass = Fraction(numerator, denominator) ** exponent
        q = ceiling(mass)
        require((1 - 1 / mass) ** q < Fraction(1, 2), "block does not halve")
        blocks = 1 + exponent * (vertices - 1).bit_length()
        require(vertices ** exponent * (1 - 1 / mass) ** (q * blocks) < 1,
                "rational block count does not cover")
        decay_checks += 1

    require(zero_gap_product_checks == 12635, "zero-gap pair count")
    require(gap_clutters == 19, "strict-gap clutter count")
    return {
        "status": "pass",
        "four_point_families": raw_count,
        "four_point_covering_clutters": len(clutters),
        "four_point_gap_clutters": gap_clutters,
        "fractional_integral_distribution": dict(sorted(distribution.items())),
        "maximum_lp_denominator": maximum_lp_denominator,
        "ordered_product_checks": product_checks,
        "zero_gap_product_checks": zero_gap_product_checks,
        "strict_product_pairs": strict_product_pairs,
        "maximum_product_dp_states": maximum_product_states,
        "sufficient_exponent_range_for_four_point_gaps": [
            min(sufficient_exponents), max(sufficient_exponents)
        ],
        "rational_decay_checks": decay_checks,
        "pentagon_geometry": pentagon_geometry_audit(),
        "named_adversaries": named_families(),
        "entrywise_sha256": digest.hexdigest(),
    }


if __name__ == "__main__":
    result = run()
    if "--emit" not in sys.argv[1:]:
        expected = Path(__file__).with_name("EXPECTED_OUTPUT.json")
        require(result == json.loads(expected.read_text()), "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
