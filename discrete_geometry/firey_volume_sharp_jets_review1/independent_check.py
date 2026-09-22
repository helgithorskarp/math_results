#!/usr/bin/env python3
"""Independent exact audit for the Firey-volume finite reconstruction.

This checker does not call or import the producer's verifier.  Its main
finite model is projective interpolation over small prime fields, rather
than supplied real hyperplane-product certificates.  The finite-field
enumeration tests the incidence/completeness reduction; the rational tests
then replay the two-moment radial formula through linear interpolation.

Python 3.11+, standard library only; all arithmetic is exact.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from json import dumps, loads
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def compositions(total, parts):
    if parts == 1:
        return ((total,),)
    return tuple(
        (first,) + tail
        for first in range(total + 1)
        for tail in compositions(total - first, parts - 1)
    )


def monomial(exponent, point):
    value = 1
    for power, coordinate in zip(exponent, point):
        value *= coordinate**power
    return value


def rank_mod(matrix, prime):
    rows = [[entry % prime for entry in row] for row in matrix]
    if not rows:
        return 0
    row = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(row, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        inverse = pow(rows[row][column], -1, prime)
        rows[row] = [(inverse * entry) % prime for entry in rows[row]]
        for i in range(len(rows)):
            if i != row and rows[i][column]:
                multiplier = rows[i][column]
                rows[i] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(rows[i], rows[row])
                ]
        row += 1
        if row == len(rows):
            break
    return row


def projective_points(dimension, prime):
    """Canonical points of PG(dimension-1, prime)."""
    points = []
    for vector in product(range(prime), repeat=dimension):
        if not any(vector):
            continue
        first = next(entry for entry in vector if entry)
        inverse = pow(first, -1, prime)
        canonical = tuple((inverse * entry) % prime for entry in vector)
        if canonical not in points:
            points.append(canonical)
    return tuple(points)


def evaluation_row(point, basis, prime):
    return [monomial(exponent, point) % prime for exponent in basis]


def audit_projective_family(dimension, prime, sizes):
    """Exhaust every spanning subset and test both separation assertions.

    Degree k-1 evaluations must independently interpolate every listed
    point.  At degree k, no unlisted projective point may annihilate every
    polynomial vanishing on the listed set.  The latter is equivalent to
    its evaluation row not belonging to the listed evaluation-row span.
    """
    universe = projective_points(dimension, prime)
    counts = {
        "configurations": 0,
        "listed_points": 0,
        "excluded_points": 0,
    }
    digest_rows = []
    for size in sizes:
        require(dimension <= size <= len(universe), "invalid projective size")
        k = size - dimension + 2
        low_basis = compositions(k - 1, dimension)
        top_basis = compositions(k, dimension)
        for chosen_indices in combinations(range(len(universe)), size):
            chosen = tuple(universe[index] for index in chosen_indices)
            if rank_mod(chosen, prime) != dimension:
                continue
            low = [evaluation_row(point, low_basis, prime) for point in chosen]
            top = [evaluation_row(point, top_basis, prime) for point in chosen]
            require(rank_mod(low, prime) == size, "degree k-1 interpolation failed")
            require(rank_mod(top, prime) == size, "degree k evaluation failed")
            outside = [point for point in universe if point not in chosen]
            for point in outside:
                extended = top + [evaluation_row(point, top_basis, prime)]
                require(
                    rank_mod(extended, prime) == size + 1,
                    "unlisted common projective zero",
                )
            counts["configurations"] += 1
            counts["listed_points"] += size
            counts["excluded_points"] += len(outside)
            digest_rows.append((dimension, prime, size, chosen_indices))
    return counts, digest_rows


def rref_fraction(matrix):
    rows = [[F(entry) for entry in row] for row in matrix]
    pivots = []
    row = 0
    if not rows:
        return rows, pivots
    for column in range(len(rows[0])):
        pivot = next((i for i in range(row, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        divisor = rows[row][column]
        rows[row] = [entry / divisor for entry in rows[row]]
        for i in range(len(rows)):
            if i != row and rows[i][column]:
                multiplier = rows[i][column]
                rows[i] = [
                    left - multiplier * right
                    for left, right in zip(rows[i], rows[row])
                ]
        pivots.append(column)
        row += 1
        if row == len(rows):
            break
    return rows, pivots


def rank_fraction(matrix):
    return len(rref_fraction(matrix)[1])


def interpolate(rows, target):
    """Solve rows * coefficients = target with free variables set to zero."""
    augmented = [list(row) + [F(value)] for row, value in zip(rows, target)]
    reduced, pivots = rref_fraction(augmented)
    variables = len(rows[0])
    require(len(pivots) == len(rows) and all(pivot < variables for pivot in pivots),
            "interpolation system lacks full row rank")
    solution = [F(0)] * variables
    for i, pivot in enumerate(pivots):
        solution[pivot] = reduced[i][-1]
    require(
        all(sum(a * b for a, b in zip(row, solution)) == value
            for row, value in zip(rows, target)),
        "interpolation solution did not replay",
    )
    return solution


def polynomial_from_coefficients(basis, coefficients):
    return {
        exponent: coefficient
        for exponent, coefficient in zip(basis, coefficients)
        if coefficient
    }


def multiply(left, right):
    answer = {}
    for exponent_a, coefficient_a in left.items():
        for exponent_b, coefficient_b in right.items():
            exponent = tuple(a + b for a, b in zip(exponent_a, exponent_b))
            answer[exponent] = answer.get(exponent, F(0)) + coefficient_a * coefficient_b
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def linear_polynomial(coefficients):
    dimension = len(coefficients)
    return {
        tuple(int(i == j) for i in range(dimension)): F(value)
        for j, value in enumerate(coefficients)
        if value
    }


def moment_table(atoms, degree):
    dimension = len(atoms[0][0])
    return {
        exponent: sum(
            weight * monomial(exponent, endpoint)
            for endpoint, weight in atoms
        )
        for exponent in compositions(degree, dimension)
    }


def apply_moment(moment, polynomial):
    return sum(coefficient * moment[exponent] for exponent, coefficient in polynomial.items())


def outer(vector):
    return tuple(tuple(a * b for b in vector) for a in vector)


def audit_radial_fixture(base_lines, scales, radii, weights):
    """Recover endpoint outer products without hyperplane products.

    ``base_lines`` define the actual endpoint directions; independently
    rescaled ``certificate_lines`` are given to the interpolation system.
    """
    dimension = len(base_lines[0])
    size = len(base_lines)
    require(size >= dimension and rank_fraction(base_lines) == dimension, "nonspanning fixture")
    require(len({outer(line) for line in base_lines}) == size, "repeated fixture line")
    k = size - dimension + 2
    low_basis = compositions(k - 1, dimension)
    certificate_lines = [
        tuple(F(scale) * coordinate for coordinate in line)
        for line, scale in zip(base_lines, scales)
    ]
    evaluation = [
        [F(monomial(exponent, line)) for exponent in low_basis]
        for line in certificate_lines
    ]
    require(rank_fraction(evaluation) == size, "rational interpolation rank")
    endpoints = [
        tuple(F(radius) * coordinate for coordinate in line)
        for line, radius in zip(base_lines, radii)
    ]
    atoms = list(zip(endpoints, map(F, weights)))
    low_moment = moment_table(atoms, 2 * k - 2)
    top_moment = moment_table(atoms, 2 * k)
    recovered = []
    for j, line in enumerate(certificate_lines):
        target = [F(int(i == j)) for i in range(size)]
        interpolant = polynomial_from_coefficients(
            low_basis, interpolate(evaluation, target)
        )
        square = multiply(interpolant, interpolant)
        coordinate = next(i for i, value in enumerate(line) if value)
        normalizer = [F(0)] * dimension
        normalizer[coordinate] = 1 / line[coordinate]
        a_square = multiply(linear_polynomial(normalizer), linear_polynomial(normalizer))
        denominator = apply_moment(low_moment, square)
        numerator = apply_moment(top_moment, multiply(a_square, square))
        require(denominator > 0 and numerator > 0, "nonpositive radial data")
        radius_squared = numerator / denominator
        recovered.append(tuple(tuple(radius_squared * a * b for b in line) for a in line))
    expected = [outer(endpoint) for endpoint in endpoints]
    require(recovered == expected, "two-moment radial recovery failed")
    return {
        "dimension": dimension,
        "lines": size,
        "k": k,
        "kernel_dimension": len(compositions(k, dimension)) - size,
    }, atoms


def scale_atoms(atoms, dilation, dimension):
    """Polar endpoints scale by a^-1; cone masses scale by a^d."""
    a = F(dilation)
    return [
        (tuple(coordinate / a for coordinate in endpoint), weight * a**dimension)
        for endpoint, weight in atoms
    ]


def canonical(value):
    if isinstance(value, F):
        return f"{value.numerator}/{value.denominator}"
    raise TypeError(type(value).__name__)


def run():
    projective_specs = (
        (2, 3, range(2, 5)),
        (3, 2, range(3, 8)),
        (3, 3, range(3, 6)),
        (4, 2, range(4, 7)),
    )
    finite_counts = {"configurations": 0, "listed_points": 0, "excluded_points": 0}
    records = []
    for dimension, prime, sizes in projective_specs:
        counts, rows = audit_projective_family(dimension, prime, sizes)
        for key, value in counts.items():
            finite_counts[key] += value
        records.extend(rows)

    fixtures = (
        (
            ((1, 0), (0, 1)),
            (2, -3), (F(3, 2), F(5, 3)), (2, 5),
        ),
        (
            ((1, 0), (0, 1), (1, 1), (1, -1)),
            (2, -3, 5, -7),
            (F(3, 2), F(5, 3), F(7, 4), F(9, 5)),
            (2, 3, 5, 7),
        ),
        (
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            (2, -3, 5),
            (F(3, 2), F(5, 3), F(7, 4)),
            (2, 3, 5),
        ),
        (
            ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)),
            (2, -3, 5, -7),
            (F(3, 2), F(5, 3), F(7, 4), F(9, 5)),
            (2, 3, 5, 7),
        ),
        (
            ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1)),
            (2, -3, 5, -7, 11),
            (F(3, 2), F(5, 3), F(7, 4), F(9, 5), F(11, 6)),
            (2, 3, 5, 7, 11),
        ),
        (
            ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
            (2, -3, 5, -7),
            (F(3, 2), F(5, 3), F(7, 4), F(9, 5)),
            (2, 3, 5, 7),
        ),
        (
            ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (1, 1, 1, 0)),
            (2, -3, 5, -7, 11),
            (F(3, 2), F(5, 3), F(7, 4), F(9, 5), F(11, 6)),
            (2, 3, 5, 7, 11),
        ),
    )
    radial_records = []
    critical_atoms = None
    for fixture in fixtures:
        record, atoms = audit_radial_fixture(*fixture)
        radial_records.append(record)
        records.append((record, [outer(endpoint) for endpoint, _ in atoms]))
        if record["dimension"] == 4 and record["lines"] == 4:
            critical_atoms = atoms

    require(critical_atoms is not None, "missing scale-critical fixture")
    dilated = scale_atoms(critical_atoms, 3, 4)
    require(moment_table(critical_atoms, 4) == moment_table(dilated, 4),
            "critical top moment is not dilation invariant")
    require(moment_table(critical_atoms, 2) != moment_table(dilated, 2),
            "preceding moment failed to recover critical scale")

    # The roots-of-unity sharpness step reduces to the simple frequency fact:
    # a degree e<2k restriction has frequencies |q|<=e, so no nonzero q is
    # divisible by 2k.  Include every smallest and moderate parameter here.
    frequency_checks = 0
    for dimension in range(2, 13):
        for k in range(2, 17):
            for degree in range(2 * k):
                survivors = [
                    q for q in range(-degree, degree + 1, 2)
                    if q % (2 * k) == 0
                ]
                require(survivors in ([], [0]), "premature rotational frequency")
                require(all(q == 0 for q in survivors), "nonconstant frequency survived")
                frequency_checks += 1

    summary = {
        "finite_field_configurations": finite_counts["configurations"],
        "finite_field_excluded_points": finite_counts["excluded_points"],
        "finite_field_listed_points": finite_counts["listed_points"],
        "frequency_checks": frequency_checks,
        "projective_families": len(projective_specs),
        "radial_fixtures": len(radial_records),
        "radial_pairs": sum(record["lines"] for record in radial_records),
        "scale_critical_examples": 1,
    }
    payload = dumps(records, default=canonical, sort_keys=True, separators=(",", ":"))
    summary["record_sha256"] = sha256(payload.encode()).hexdigest()
    expected_path = Path(__file__).with_name("EXPECTED_OUTPUT.json")
    if expected_path.exists():
        require(summary == loads(expected_path.read_text()), "expected output mismatch")
    return summary


if __name__ == "__main__":
    print(dumps(run(), indent=2, sort_keys=True))
