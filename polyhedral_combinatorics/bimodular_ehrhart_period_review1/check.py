#!/usr/bin/env python3
"""Independent exact checks for the simple-bimodular Ehrhart review.

No reviewed code or data is imported.  Three audits target distinct human
reductions: extension of row subsets inside determinant-one/two bases;
full support of the unique mod-two image character; and direct Ehrhart
counts for determinant-two parallelepipeds (with optional free cubes).
"""

from fractions import Fraction
from itertools import combinations, product
from math import comb, factorial, gcd
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def determinant(matrix):
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "nonsquare matrix")
    if size == 0:
        return 1
    if size == 1:
        return matrix[0][0]
    if size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if size == 3:
        a, b, c = matrix
        return (a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0]))
    total = 0
    for column, value in enumerate(matrix[0]):
        minor = [row[:column] + row[column + 1:] for row in matrix[1:]]
        total += (-1) ** column * value * determinant(minor)
    return total


def image_index(rows):
    if not rows:
        return 1
    q, width = len(rows), len(rows[0])
    require(q <= width and all(len(row) == width for row in rows),
            "bad rectangular matrix")
    value = 0
    for columns in combinations(range(width), q):
        minor = [[row[column] for column in columns] for row in rows]
        value = gcd(value, abs(determinant(minor)))
    return value


def basis_extension_audit():
    """Exhaust all 3x3 bases over {-1,0,1,2} with determinant 1 or 2."""
    values = (-1, 0, 1, 2)
    bases = {1: 0, 2: 0}
    independent_subsets = 0
    nonprimitive_subsets = 0
    for entries in product(values, repeat=9):
        matrix = [list(entries[3 * row:3 * row + 3]) for row in range(3)]
        delta = abs(determinant(matrix))
        if delta not in (1, 2):
            continue
        bases[delta] += 1
        for size in (1, 2):
            for indices in combinations(range(3), size):
                index = image_index([matrix[index] for index in indices])
                require(index > 0, "subset of a basis became dependent")
                require(index in (1, 2) and delta % index == 0,
                        "projected image index does not divide basis determinant")
                independent_subsets += 1
                nonprimitive_subsets += index == 2
    require(bases[1] and bases[2] and nonprimitive_subsets,
            "basis audit missed a required class")
    return {
        "alphabet": list(values),
        "bases_by_abs_determinant": {str(key): bases[key] for key in (1, 2)},
        "independent_proper_row_subsets": independent_subsets,
        "index_two_proper_row_subsets": nonprimitive_subsets,
    }


def annihilator(rows):
    """Return all nonzero left annihilators of rows modulo two."""
    q, width = len(rows), len(rows[0])
    return [bits for bits in product((0, 1), repeat=q) if any(bits)
            and all(sum(bits[i] * rows[i][j] for i in range(q)) % 2 == 0
                    for j in range(width))]


def subsystem_data(rows, mask):
    selected = [rows[i] for i in range(len(rows)) if mask & (1 << i)]
    if not selected:
        return (), None
    index = image_index(selected)
    require(index in (1, 2), "proper projection of index-two image has larger index")
    if index == 1:
        return tuple(i for i in range(len(rows)) if mask & (1 << i)), None
    characters = annihilator(selected)
    require(len(characters) == 1, "index-two subsystem lacks unique character")
    return tuple(i for i in range(len(rows)) if mask & (1 << i)), characters[0]


def subsystem_solvable(indices, character, rhs):
    if character is None:
        return True
    return sum(character[j] * rhs[index] for j, index in enumerate(indices)) % 2 == 0


def full_support_audit():
    """Exhaust small rectangular index-two images and every binary RHS."""
    summary = {}
    for q, width in ((2, 3), (3, 4)):
        matrices = full_support = partial_support = 0
        outside_rhs = minimal_outside_rhs = proper_checks = 0
        for entries in product((-1, 0, 1), repeat=q * width):
            rows = [list(entries[width * i:width * (i + 1)]) for i in range(q)]
            if image_index(rows) != 2:
                continue
            characters = annihilator(rows)
            require(len(characters) == 1, "index-two image lacks unique character")
            character = characters[0]
            matrices += 1
            if all(character):
                full_support += 1
            else:
                partial_support += 1
            subsystems = [subsystem_data(rows, mask) for mask in range((1 << q) - 1)]
            for rhs in product((0, 1), repeat=q):
                if sum(a * b for a, b in zip(character, rhs)) % 2 == 0:
                    continue
                outside_rhs += 1
                minimal = True
                for indices, subcharacter in subsystems:
                    proper_checks += 1
                    if not subsystem_solvable(indices, subcharacter, rhs):
                        minimal = False
                require(minimal == all(character),
                        "minimal nonmembership disagrees with full character support")
                minimal_outside_rhs += minimal
        require(matrices and full_support,
                "full-support audit missed its positive class")
        # With the alphabet {-1,0,1}, a partial character for q=2 would
        # force one row to vanish.  The 3x4 sweep must contain both classes.
        require((q == 2 and partial_support == 0) or
                (q == 3 and partial_support > 0),
                "full-support audit has an unexpected support distribution")
        summary[f"{q}x{width}"] = {
            "index_two_matrices": matrices,
            "full_support_characters": full_support,
            "partial_support_characters": partial_support,
            "outside_binary_rhs": outside_rhs,
            "minimal_outside_rhs": minimal_outside_rhs,
            "proper_subsystem_checks": proper_checks,
        }
    return summary


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_add(left, right):
    result = [Fraction(0)] * max(len(left), len(right))
    for i, value in enumerate(left):
        result[i] += value
    for i, value in enumerate(right):
        result[i] += value
    return trim(result)


def poly_scale(poly, scalar):
    return trim([scalar * value for value in poly])


def poly_multiply(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return trim(result)


def poly_evaluate(poly, value):
    result = Fraction(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def interpolate(nodes, values):
    require(len(nodes) == len(values) and len(set(nodes)) == len(nodes),
            "bad interpolation data")
    result = [Fraction(0)]
    for i, (node, value) in enumerate(zip(nodes, values)):
        basis = [Fraction(1)]
        denominator = Fraction(1)
        for j, other in enumerate(nodes):
            if i == j:
                continue
            basis = poly_multiply(basis, [-other, 1])
            denominator *= node - other
        result = poly_add(result, poly_scale(basis, Fraction(value, denominator)))
    return trim(result)


def divide_at_minus_one(poly):
    poly = trim(poly)
    order = 0
    while poly_evaluate(poly, -1) == 0:
        require(len(poly) > 1, "zero polynomial")
        quotient = [Fraction(0)] * (len(poly) - 1)
        quotient[-1] = poly[-1]
        for i in range(len(poly) - 2, 0, -1):
            quotient[i - 1] = poly[i] - quotient[i]
        require(poly[0] == quotient[0], "synthetic-division remainder")
        poly = trim(quotient)
        order += 1
    return order, poly_evaluate(poly, -1)


def numerator(dimension, even_poly, odd_poly):
    def value(n):
        if n < 0:
            return Fraction(0)
        return poly_evaluate(even_poly if n % 2 == 0 else odd_poly, n)

    coefficients = []
    for degree in range(2 * dimension + 2):
        coefficients.append(sum(
            Fraction((-1) ** j * comb(dimension + 1, j)) * value(degree - 2 * j)
            for j in range(min(dimension + 1, degree // 2) + 1)
        ))
    for degree in range(2 * dimension + 2, 2 * dimension + 6):
        tail = sum(
            Fraction((-1) ** j * comb(dimension + 1, j)) * value(degree - 2 * j)
            for j in range(dimension + 2)
        )
        require(tail == 0, "nonzero numerator tail")
    return trim(coefficients)


def base_count(rank, dilation):
    # y=D x lies in the index-two even-total-sum lattice.  With
    # u=n b-y in {0,...,n}^rank and sum(b) odd, sum(u)=n modulo two.
    total = (dilation + 1) ** rank
    return (total + 1) // 2 if dilation % 2 == 0 else total // 2


def direct_x_count(rank, dilation):
    """Literal integer count from 0 <= n*b-D*x <= n."""
    if rank == 1:
        ranges = [range(0, dilation // 2 + 1)]
    else:
        ranges = [range(-dilation, 1) for _ in range(rank - 1)]
        ranges.append(range(0, (rank * dilation + 1) // 2 + 1))
    total = 0
    for vector in product(*ranges):
        image = list(vector[:-1])
        image.append(sum(vector[:-1]) + 2 * vector[-1])
        lower = [0] * (rank - 1) + [0]
        upper = [dilation] * (rank - 1) + [dilation]
        nb = [0] * (rank - 1) + [dilation]
        slack = [nb[i] - image[i] for i in range(rank)]
        total += all(lower[i] <= slack[i] <= upper[i] for i in range(rank))
    return total


def family_count(rank, free_dimension, dilation):
    return base_count(rank, dilation) * (dilation + 1) ** free_dimension


def check_family(rank, free_dimension):
    dimension = rank + free_dimension
    evens = [2 * i for i in range(dimension + 1)]
    odds = [2 * i + 1 for i in range(dimension + 1)]
    even_poly = interpolate(evens, [family_count(rank, free_dimension, n) for n in evens])
    odd_poly = interpolate(odds, [family_count(rank, free_dimension, n) for n in odds])
    for n in (2 * dimension + 2, 2 * dimension + 3):
        poly = even_poly if n % 2 == 0 else odd_poly
        require(poly_evaluate(poly, n) == family_count(rank, free_dimension, n),
                "definition-level holdout failed")

    parity = poly_scale(poly_add(even_poly, poly_scale(odd_poly, -1)), Fraction(1, 2))
    require(len(parity) - 1 == free_dimension, "wrong parity degree")
    require(parity[-1] == Fraction(1, 4), "wrong leading parity coefficient")

    h_poly = numerator(dimension, even_poly, odd_poly)
    order, residual = divide_at_minus_one(h_poly)
    expected_residual = 2 ** (rank + free_dimension - 1) * factorial(free_dimension)
    require(order == rank, "wrong root order")
    require(residual == expected_residual, "wrong residual")

    fractional_vertices = 0
    for corner in product((0, 1), repeat=rank):
        image = [0] * (rank - 1) + [1]
        image = [image[i] - corner[i] for i in range(rank)]
        last = Fraction(image[-1] - sum(image[:-1]), 2)
        fractional_vertices += last.denominator == 2
    require(fractional_vertices == 2 ** (rank - 1),
            "wrong number of minimal nonintegral faces")

    return {
        "rank": rank,
        "free_dimension": free_dimension,
        "ambient_dimension": dimension,
        "fractional_leading_faces": fractional_vertices,
        "degree_B": len(parity) - 1,
        "leading_B": str(parity[-1]),
        "root_order": order,
        "residual": str(residual),
        "holdouts": 2,
    }


def family_audit():
    literal_checks = 0
    for rank in range(1, 5):
        for dilation in range(4):
            require(direct_x_count(rank, dilation) == base_count(rank, dilation),
                    "literal inequality count disagrees with image-lattice count")
            literal_checks += 1

    records = [check_family(rank, free)
               for rank in range(1, 8) for free in range(4)]
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return {
        "cases": len(records),
        "ranks": list(range(1, 8)),
        "free_dimensions": list(range(4)),
        "literal_inequality_checks": literal_checks,
        "definition_level_holdouts": 2 * len(records),
        "leading_B": "1/4",
        "family_record_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "outside_primitive_type_B_from_rank": 1,
        "dense_shear": "(x,w)->(x+w_1*1,w), unimodular when f>=1",
    }


def main():
    output = {
        "implementation": "independent determinant, mod-two character, and direct-count audits",
        "imports_reviewed_code": False,
        "basis_extension_audit": basis_extension_audit(),
        "full_support_audit": full_support_audit(),
        "parallelepiped_cube_families": family_audit(),
        "status": "PASS",
    }
    expected_path = Path(__file__).with_name("expected.json")
    if expected_path.exists():
        require(output == json.loads(expected_path.read_text()),
                "computed record differs from expected.json")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
