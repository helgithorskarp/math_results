#!/usr/bin/env python3
"""Independent exact audit and six-facet refinement for prime-five collapse."""

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import ceil, floor, gcd


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def det(left: tuple[int, int], right: tuple[int, int]) -> int:
    return left[0] * right[1] - left[1] * right[0]


def lin_add(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    return left[0] + right[0], left[1] + right[1]


def lin_scale(
    scalar: Fraction, value: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    return scalar * value[0], scalar * value[1]


def lin_value(value: tuple[Fraction, Fraction], parameter: int) -> Fraction:
    return value[0] + value[1] * parameter


def poly_add(left: tuple[Fraction, ...], right: tuple[Fraction, ...]):
    size = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(size)
    )


def poly_scale(scalar: Fraction, value: tuple[Fraction, ...]):
    return tuple(scalar * entry for entry in value)


def poly_mul(left: tuple[Fraction, ...], right: tuple[Fraction, ...]):
    answer = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return tuple(answer)


def adjacent_vertices(normals, supports):
    vertices = []
    size = len(normals)
    for i in range(size):
        (a, b), (c, d) = normals[i], normals[(i + 1) % size]
        denominator = det(normals[i], normals[(i + 1) % size])
        require(denominator > 0, f"noncyclic normals at {i}")
        first = lin_scale(
            Fraction(1, denominator),
            lin_add(lin_scale(d, supports[i]), lin_scale(-b, supports[(i + 1) % size])),
        )
        second = lin_scale(
            Fraction(1, denominator),
            lin_add(lin_scale(a, supports[(i + 1) % size]), lin_scale(-c, supports[i])),
        )
        vertices.append((first, second))
    return tuple(vertices)


def edge_lengths(normals, vertices):
    lengths = []
    for i, (a, b) in enumerate(normals):
        dx = lin_add(vertices[i][0], lin_scale(-1, vertices[i - 1][0]))
        dy = lin_add(vertices[i][1], lin_scale(-1, vertices[i - 1][1]))
        if b:
            length = lin_scale(Fraction(-1, b), dx)
        else:
            length = lin_scale(Fraction(1, a), dy)
        require((dx, dy) == (lin_scale(-b, length), lin_scale(a, length)),
                f"edge {i} is not in its primitive tangent direction")
        lengths.append(length)
    return tuple(lengths)


def area_polynomial(vertices):
    twice = (Fraction(0), Fraction(0), Fraction(0))
    for i, (x, y) in enumerate(vertices):
        next_x, next_y = vertices[(i + 1) % len(vertices)]
        term = poly_add(poly_mul(x, next_y), poly_scale(-1, poly_mul(y, next_x)))
        twice = poly_add(twice, term)
    return poly_scale(Fraction(1, 2), twice)


def active_profile(rows, support_pair, prime=5):
    image = {
        (
            (rows[0][0] * x + rows[0][1] * y) % prime,
            (rows[1][0] * x + rows[1][1] * y) % prime,
        )
        for x in range(prime)
        for y in range(prime)
    }
    require(len(image) == prime, "active image does not have index five")
    normalized = set()
    annihilators = 0
    for e0, e1 in product(range(prime), repeat=2):
        if (e0, e1) == (0, 0):
            continue
        if all((e0 * rows[0][column] + e1 * rows[1][column]) % prime == 0
               for column in range(2)):
            annihilators += 1
            c = lin_add(lin_scale(e0, support_pair[0]), lin_scale(e1, support_pair[1]))
            require(c[1].denominator == 1 and int(c[1]) % prime == 0,
                    "normalized profile varies with the family parameter")
            residue = int(c[0]) % prime
            require(residue != 0, "a purported bad vertex is integral")
            inverse = pow(residue, -1, prime)
            normalized.add(((inverse * e0) % prime, (inverse * e1) % prime))
    require(annihilators == prime - 1, "wrong annihilator count")
    require(len(normalized) == 1, "profile depends on the character representative")
    return normalized.pop()


def audit_symbolic_family(name, normals, supports, bad_indices, expected):
    require(all(gcd(abs(a), abs(b)) == 1 for a, b in normals),
            f"{name}: nonprimitive facet normal")
    determinants = tuple(det(normals[i], normals[(i + 1) % len(normals)])
                         for i in range(len(normals)))
    require(determinants == expected["determinants"], f"{name}: determinant pattern")
    vertices = adjacent_vertices(normals, supports)
    lengths = edge_lengths(normals, vertices)
    for i, length in enumerate(lengths):
        require(length[1] >= 0 and lin_value(length, 1) > 0,
                f"{name}: facet {i} degenerates")
    for i, vertex in enumerate(vertices):
        for j, normal in enumerate(normals):
            value = lin_add(lin_scale(normal[0], vertex[0]),
                            lin_scale(normal[1], vertex[1]))
            slack = lin_add(supports[j], lin_scale(-1, value))
            if j in (i, (i + 1) % len(normals)):
                require(slack == (0, 0), f"{name}: incident slack {i,j}")
            else:
                require(slack[1] >= 0 and lin_value(slack, 1) > 0,
                        f"{name}: nonincident slack {i,j}")
    profiles = []
    for i in range(len(normals)):
        vertex = vertices[i]
        if i in bad_indices:
            require(determinants[i] == 5, f"{name}: bad determinant")
            profiles.append(active_profile(
                (normals[i], normals[(i + 1) % len(normals)]),
                (supports[i], supports[(i + 1) % len(normals)]),
            ))
            require(any(coordinate.denominator == 5
                        for affine in vertex for coordinate in affine),
                    f"{name}: bad vertex has no denominator-five coordinate")
        else:
            require(all(coordinate.denominator == 1
                        for affine in vertex for coordinate in affine),
                    f"{name}: separator vertex is not integral")
    require(tuple(profiles) == expected["profiles"], f"{name}: profile sequence")
    area = area_polynomial(vertices)
    require(area == expected["area"], f"{name}: area polynomial")
    perimeter = (Fraction(0), Fraction(0))
    for length in lengths:
        perimeter = lin_add(perimeter, length)
    require(perimeter == expected["perimeter"], f"{name}: perimeter")
    return vertices, lengths


def support_values(supports, parameter):
    values = tuple(lin_value(support, parameter) for support in supports)
    require(all(value.denominator == 1 for value in values), "nonintegral support")
    return tuple(int(value) for value in values)


def evaluated_vertices(vertices, parameter):
    return tuple((lin_value(x, parameter), lin_value(y, parameter)) for x, y in vertices)


def ceil_ratio(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def count_points(normals, supports, vertices, parameter, dilation):
    values = support_values(supports, parameter)
    points = evaluated_vertices(vertices, parameter)
    left = floor(min(dilation * point[0] for point in points))
    right = ceil(max(dilation * point[0] for point in points))
    total = 0
    for x in range(left, right + 1):
        lower = None
        upper = None
        for (a, b), support in zip(normals, values):
            rhs = dilation * support - a * x
            if b > 0:
                candidate = rhs // b
                upper = candidate if upper is None else min(upper, candidate)
            elif b < 0:
                candidate = ceil_ratio(rhs, b)
                lower = candidate if lower is None else max(lower, candidate)
            else:
                require(rhs >= 0, "x range included an infeasible vertical constraint")
        require(lower is not None and upper is not None, "unbounded vertical slice")
        if lower <= upper:
            total += upper - lower + 1
    return total


def formula_value(area, perimeter, parameter, dilation):
    evaluated_area = sum(area[i] * parameter**i for i in range(len(area)))
    evaluated_perimeter = lin_value(perimeter, parameter)
    answer = evaluated_area * dilation * dilation + evaluated_perimeter * dilation / 2 + 1
    require(answer.denominator == 1, "claimed Ehrhart polynomial is not integer-valued")
    return int(answer)


def direct_checks(name, normals, supports, vertices, area, perimeter, parameters):
    records = []
    for parameter in parameters:
        for dilation in range(25):
            observed = count_points(normals, supports, vertices, parameter, dilation)
            predicted = formula_value(area, perimeter, parameter, dilation)
            require(observed == predicted,
                    f"{name}: count mismatch at {(parameter, dilation)}")
            records.append((name, parameter, dilation, observed))
    return records


def cyclotomic_reduce(coefficients, prime=5):
    cyclic = [Fraction(0)] * prime
    for exponent, coefficient in enumerate(coefficients):
        cyclic[exponent % prime] += coefficient
    top = cyclic[-1]
    return tuple(cyclic[i] - top for i in range(prime - 1))


def zeta_power(exponent, prime=5):
    raw = [Fraction(0)] * (exponent % prime + 1)
    raw[exponent % prime] = 1
    return cyclotomic_reduce(raw, prime)


def cyclotomic_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def cyclotomic_scale(scalar, value):
    return tuple(Fraction(scalar) * entry for entry in value)


def cyclotomic_mul(left, right):
    raw = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            raw[i + j] += a * b
    return cyclotomic_reduce(raw)


def reciprocal_one_minus(exponent):
    answer = (Fraction(0),) * 4
    for r in range(1, 5):
        answer = cyclotomic_add(
            answer, cyclotomic_scale(Fraction(-r, 5), zeta_power(exponent * r))
        )
    return answer


def profile_cancellation(profiles):
    checks = 0
    zero = (Fraction(0),) * 4
    for mode in range(1, 5):
        total = zero
        for first, second in profiles:
            total = cyclotomic_add(
                total,
                cyclotomic_mul(
                    reciprocal_one_minus(mode * first),
                    reciprocal_one_minus(mode * second),
                ),
            )
        require(total == zero, f"profile cancellation fails in mode {mode}")
        checks += 1
    return checks


TARGET_NORMALS = (
    (1, 1), (-1, 4), (-1, 1), (-4, -1),
    (-1, -1), (1, -4), (1, -1), (4, 1),
)
TARGET_SUPPORTS = (
    (Fraction(0), Fraction(11)), (Fraction(1), Fraction(29)),
    (Fraction(1), Fraction(11)), (Fraction(1), Fraction(29)),
    (Fraction(1), Fraction(11)), (Fraction(3), Fraction(29)),
    (Fraction(3), Fraction(11)), (Fraction(0), Fraction(29)),
)
TARGET_EXPECTED = {
    "determinants": (5, 3, 5, 3, 5, 3, 5, 3),
    "profiles": ((1, 1), (3, 3), (4, 4), (2, 2)),
    "area": (Fraction(-5, 2), Fraction(25), Fraction(182)),
    "perimeter": (Fraction(-1), Fraction(20)),
}


HEX_NORMALS = ((1, 0), (19, 5), (7, 2), (8, 3), (21, 10), (-11, -5))
HEX_SUPPORTS = (
    (Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(0)),
    (Fraction(1), Fraction(3)),
    (Fraction(1), Fraction(22)),
    (Fraction(9), Fraction(130)),
    (Fraction(4), Fraction(5)),
)
HEX_EXPECTED = {
    "determinants": (5, 3, 5, 17, 5, 5),
    "profiles": ((1, 1), (3, 3), (2, 2), (4, 4)),
    "area": (Fraction(14), Fraction(232), Fraction(1855, 2)),
    "perimeter": (Fraction(6), Fraction(45)),
}


def verify():
    target_vertices, _ = audit_symbolic_family(
        "octagon", TARGET_NORMALS, TARGET_SUPPORTS, {0, 2, 4, 6}, TARGET_EXPECTED
    )
    hex_vertices, hex_lengths = audit_symbolic_family(
        "hexagon", HEX_NORMALS, HEX_SUPPORTS, {0, 2, 4, 5}, HEX_EXPECTED
    )
    # The slope supports define an integral polygon with this same fan.
    slope_vertices = adjacent_vertices(
        HEX_NORMALS, tuple((support[1], Fraction(0)) for support in HEX_SUPPORTS)
    )
    require(all(coordinate.denominator == 1
                for vertex in slope_vertices for affine in vertex for coordinate in affine),
            "hexagon slope polygon is not lattice")
    require(tuple(length[1] for length in hex_lengths) == (1, 1, 1, 1, 13, 28),
            "hexagon Minkowski direction lengths changed")

    records = []
    records.extend(direct_checks(
        "octagon", TARGET_NORMALS, TARGET_SUPPORTS, target_vertices,
        TARGET_EXPECTED["area"], TARGET_EXPECTED["perimeter"], (1, 7, 19),
    ))
    records.extend(direct_checks(
        "hexagon", HEX_NORMALS, HEX_SUPPORTS, hex_vertices,
        HEX_EXPECTED["area"], HEX_EXPECTED["perimeter"], (1, 2, 7),
    ))
    # Recheck the target's all-bad quadrilateral congruence for every lift
    # parameter modulo five: the forced determinant quotient is 2, never 1.
    quadrilateral_checks = 0
    for u, w in product(range(5), repeat=2):
        require((-3 - 10 * u + 10 * w + 25 * u * w) % 5 == 2,
                "quadrilateral residue changed")
        quadrilateral_checks += 1

    record = {
        "arithmetic": "exact Fraction and cyclotomic arithmetic",
        "octagon": {
            "direct_count_checks": 75,
            "parameters": [1, 7, 19],
            "profiles": [list(profile) for profile in TARGET_EXPECTED["profiles"]],
        },
        "six_facet_refinement": {
            "area": "(1855*k^2+464*k+28)/2",
            "direct_count_checks": 75,
            "normal_determinants": list(HEX_EXPECTED["determinants"]),
            "normalized_perimeter": "45*k+6",
            "parameters": [1, 2, 7],
            "profiles": [list(profile) for profile in HEX_EXPECTED["profiles"]],
            "slope_polygon_edge_lengths": [1, 1, 1, 1, 13, 28],
        },
        "cyclotomic_mode_checks": (
            profile_cancellation(TARGET_EXPECTED["profiles"])
            + profile_cancellation(HEX_EXPECTED["profiles"])
        ),
        "quadrilateral_lift_checks": quadrilateral_checks,
    }
    payload = json.dumps(records, separators=(",", ":"))
    record["direct_count_record_sha256"] = sha256(payload.encode()).hexdigest()
    return record


def main() -> None:
    print(json.dumps(verify(), sort_keys=True, separators=(",", ":")))
    print("VERIFIED prime-five octagon and six-facet refinement")


if __name__ == "__main__":
    main()
