#!/usr/bin/env python3
"""Independent exact audit of the universal seven-factor Gaussian kernel.

The checker imports no file from the author packet.  It derives the complete
mixed-derivative polynomial in a square-free power-series ring, reconstructs
the two trace matrices, and proves their spectra from one canonical column
plus the label-permutation symmetry.
"""

from fractions import Fraction as Q
from itertools import combinations, permutations
from math import comb, factorial
from pathlib import Path
import hashlib
import json


ROOT = Path(__file__).resolve().parent
ALPHA = Q(5, 2)
LABELS = tuple(range(7))
FULL_MASK = (1 << 7) - 1


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def rising(value, length):
    answer = Q(1)
    for offset in range(length):
        answer *= value + offset
    return answer


# A polynomial is {monomial: coefficient}; a monomial is a sorted tuple of
# Gram variables (i,j), with repetition allowed.
def poly_add_into(target, source, scale=Q(1)):
    for monomial, coefficient in source.items():
        target[monomial] = target.get(monomial, Q(0)) + scale * coefficient
        if not target[monomial]:
            del target[monomial]


def poly_scale(poly, scale):
    return {monomial: scale * coefficient for monomial, coefficient in poly.items()
            if scale * coefficient}


def poly_mul(left, right):
    answer = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(sorted(monomial_left + monomial_right))
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient_left * coefficient_right
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


ONE_POLY = {(): Q(1)}


# A square-free u-series is {bit mask: polynomial coefficient}.  Terms with
# overlapping masks multiply to zero, implementing Q[u_i]/(u_i^2).
def series_add(left, right):
    answer = {mask: dict(poly) for mask, poly in left.items()}
    for mask, poly in right.items():
        slot = answer.setdefault(mask, {})
        poly_add_into(slot, poly)
        if not slot:
            del answer[mask]
    return answer


def series_scale(series, scale):
    return {mask: poly_scale(poly, scale) for mask, poly in series.items() if scale}


def series_mul(left, right):
    answer = {}
    for mask_left, poly_left in left.items():
        for mask_right, poly_right in right.items():
            if mask_left & mask_right:
                continue
            mask = mask_left | mask_right
            slot = answer.setdefault(mask, {})
            poly_add_into(slot, poly_mul(poly_left, poly_right))
    return {mask: poly for mask, poly in answer.items() if poly}


def series_function(argument, coefficients):
    """Return sum coefficients[r] * argument**r in the square-free ring."""
    answer = {}
    power = {0: ONE_POLY}
    for coefficient in coefficients:
        answer = series_add(answer, series_scale(power, coefficient))
        power = series_mul(power, argument)
    return answer


def gram_var(i, j):
    return ((min(i, j), max(i, j)),)


def direct_mixed_derivative_polynomial():
    """Derive L_7 from the recentered quotient, not from matchings.

    In the square-free ring this expands
      (1+sum u)^(-alpha) exp(-sum G_ii u_i/2
        + sum_{i<j} G_ij u_i u_j/(1+sum u)).
    The negative seventh mixed derivative is L_7.
    """
    u_sum = {1 << i: ONE_POLY for i in LABELS}
    linear = {1 << i: {gram_var(i, i): -Q(1, 2)} for i in LABELS}
    quadratic_numerator = {
        (1 << i) | (1 << j): {gram_var(i, j): Q(1)}
        for i in LABELS for j in range(i + 1, 7)
    }
    reciprocal = series_function(u_sum, [Q((-1) ** r) for r in range(8)])
    exponent = series_add(linear, series_mul(quadratic_numerator, reciprocal))
    exponential = series_function(exponent, [Q(1, factorial(r)) for r in range(8)])
    prefactor = series_function(
        u_sum,
        [Q((-1) ** r) * rising(ALPHA, r) / factorial(r) for r in range(8)],
    )
    coefficient = series_mul(prefactor, exponential)[FULL_MASK]
    return poly_scale(coefficient, -1)  # (-1)^7


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def matching_polynomial():
    """Construct equation (5) by endpoint choice and perfect matchings."""
    answer = {}
    for edge_count in range(4):
        for endpoints in combinations(LABELS, 2 * edge_count):
            for edges in perfect_matchings(endpoints):
                unmatched = tuple(i for i in LABELS if i not in endpoints)
                for scalar_count in range(len(unmatched) + 1):
                    for scalars in combinations(unmatched, scalar_count):
                        scalar_set = set(scalars)
                        diagonals = tuple(i for i in unmatched if i not in scalar_set)
                        monomial = tuple(sorted(
                            [tuple(sorted(edge)) for edge in edges]
                            + [(i, i) for i in diagonals]
                        ))
                        coefficient = rising(ALPHA + edge_count, scalar_count) / 2 ** len(diagonals)
                        answer[monomial] = answer.get(monomial, Q(0)) + coefficient
    return answer


def homogeneous_form(degree):
    """Construct S_degree directly from equation (8)."""
    answer = {}
    for edge_count in range(min(3, degree) + 1):
        if degree - edge_count > 7 - 2 * edge_count:
            continue
        for endpoints in combinations(LABELS, 2 * edge_count):
            for edges in perfect_matchings(endpoints):
                unmatched = tuple(i for i in LABELS if i not in endpoints)
                for diagonals in combinations(unmatched, degree - edge_count):
                    monomial = tuple(sorted(
                        [tuple(sorted(edge)) for edge in edges]
                        + [(i, i) for i in diagonals]
                    ))
                    coefficient = Q(1, 2 ** len(diagonals)) / rising(ALPHA, edge_count)
                    answer[monomial] = answer.get(monomial, Q(0)) + coefficient
    return answer


def reconstruct_from_forms(forms):
    answer = {}
    for degree, form in enumerate(forms):
        poly_add_into(answer, form, rising(ALPHA, 7 - degree))
    return answer


def relative_parity(left, right):
    permutation = tuple(left.index(label) for label in right)
    inversions = sum(permutation[i] > permutation[j]
                     for i in range(len(permutation))
                     for j in range(i + 1, len(permutation)))
    return inversions % 2


def trace_matrix(order, correction=21):
    """Construct B_2 or B_3 directly from the alignment rule."""
    indices = list(permutations(LABELS, order))
    weights = {2: (35, 14, 4), 3: (315, 126, 36, 8)}[order]
    matrix = []
    for left in indices:
        row = []
        positions_left = {label: position for position, label in enumerate(left)}
        for right in indices:
            positions_right = {label: position for position, label in enumerate(right)}
            shared = set(left).intersection(right)
            aligned = all(positions_left[label] == positions_right[label] for label in shared)
            value = weights[sum(a != b for a, b in zip(left, right))] if aligned else 0
            if order == 3 and set(left) == set(right) and relative_parity(left, right):
                value -= correction
            row.append(value)
        matrix.append(row)
    return indices, matrix


def matrix_polynomial(indices, matrix, denominator, order):
    answer = {}
    for i, left in enumerate(indices):
        for j, right in enumerate(indices):
            value = matrix[i][j]
            if value:
                monomial = tuple(sorted(gram_var(left[r], right[r])[0] for r in range(order)))
                answer[monomial] = answer.get(monomial, Q(0)) + Q(value, denominator)
    if order == 3:
        # 63*(per-det)=126*sum_i G_ii G_jk^2.
        for triple in combinations(LABELS, 3):
            for singleton in triple:
                j, k = (label for label in triple if label != singleton)
                monomial = tuple(sorted(((singleton, singleton), (j, k), (j, k))))
                answer[monomial] = answer.get(monomial, Q(0)) + Q(126, denominator)
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def apply_matrix(matrix, vector):
    return [sum(entry * coordinate for entry, coordinate in zip(row, vector))
            for row in matrix]


def apply_shifted(matrix, vector, shift):
    product = apply_matrix(matrix, vector)
    return [entry - shift * old for entry, old in zip(product, vector)]


def verify_label_equivariance(indices, matrix):
    lookup = {index: position for position, index in enumerate(indices)}
    for adjacent in range(6):
        def swap(label):
            if label == adjacent:
                return adjacent + 1
            if label == adjacent + 1:
                return adjacent
            return label

        transported = [lookup[tuple(swap(label) for label in index)] for index in indices]
        for i in range(len(indices)):
            for j in range(len(indices)):
                require(matrix[i][j] == matrix[transported[i]][transported[j]],
                        "matrix is not S_7-equivariant")


def spectral_certificate(indices, matrix, roots):
    size = len(indices)
    require(all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(size)),
            "matrix is not symmetric")
    verify_label_equivariance(indices, matrix)

    canonical = [int(i == 0) for i in range(size)]
    vector = canonical
    for root in roots:
        vector = apply_shifted(matrix, vector, root)
    require(not any(vector), "canonical annihilating-polynomial check failed")

    # S_7-equivariance and transitivity carry this identity from the canonical
    # ordered tuple to every standard basis vector.  Compute exact spectral
    # multiplicities from the diagonal of each Lagrange projector; equivariance
    # makes every diagonal entry equal.
    multiplicities = {}
    for eigenvalue in roots:
        vector = canonical
        denominator = 1
        for other in roots:
            if other == eigenvalue:
                continue
            vector = apply_shifted(matrix, vector, other)
            denominator *= eigenvalue - other
        multiplicity = Q(size * vector[0], denominator)
        require(multiplicity.denominator == 1 and multiplicity >= 0,
                "invalid projector multiplicity")
        multiplicities[str(eigenvalue)] = int(multiplicity)
    require(sum(multiplicities.values()) == size, "spectral multiplicities are incomplete")
    require(min(roots) >= 0 and len(set(roots)) == len(roots), "roots are not distinct and nonnegative")
    return multiplicities


def matrix_hash(matrix):
    return hashlib.sha256(json.dumps(matrix, separators=(",", ":")).encode()).hexdigest()


def polynomial_hash(poly):
    serial = [
        [[[i, j] for i, j in monomial], str(coefficient)]
        for monomial, coefficient in sorted(poly.items())
    ]
    return hashlib.sha256(json.dumps(serial, separators=(",", ":")).encode()).hexdigest()


def main_record():
    direct = direct_mixed_derivative_polynomial()
    matching = matching_polynomial()
    require(direct == matching, "direct derivative and matching formula differ")
    require(len(direct) == 1850, "wrong L_7 term count")

    forms = [homogeneous_form(degree) for degree in range(8)]
    require(reconstruct_from_forms(forms) == direct, "homogeneous decomposition failed")
    term_counts = [len(form) for form in forms]
    require(term_counts == [1, 28, 231, 665, 665, 231, 28, 1],
            "homogeneous term counts differ")

    roots_by_order = {
        2: [7, 15, 45, 105, 255],
        3: [0, 42, 45, 117, 132, 522, 585, 882, 1755, 3252],
    }
    matrices = {}
    spectra = {}
    for order, denominator in ((2, 280), (3, 15120)):
        indices, matrix = trace_matrix(order)
        require(matrix_polynomial(indices, matrix, denominator, order) == forms[order],
                f"trace decoding failed for order {order}")
        multiplicities = spectral_certificate(indices, matrix, roots_by_order[order])
        matrices[order] = matrix
        spectra[str(order)] = {
            "dimension": len(indices),
            "roots": roots_by_order[order],
            "multiplicities": multiplicities,
            "rank": len(indices) - multiplicities.get("0", 0),
            "integer_matrix_sha256": matrix_hash(matrix),
        }

    # Damage control: changing the order-three projection correction destroys
    # the stated exact spectral certificate.
    bad_indices, bad_matrix = trace_matrix(3, correction=20)
    try:
        spectral_certificate(bad_indices, bad_matrix, roots_by_order[3])
    except ArithmeticError:
        damage_rejected = True
    else:
        damage_rejected = False
    require(damage_rejected, "damaged correction passed")

    scaled_beta = [
        9 * Q(8 * (-1) ** ell * comb(7, ell), (ell + 1) * (ell + 2))
        for ell in range(8)
    ]
    require(scaled_beta == list(map(Q, [36, -84, 126, -126, 84, -36, 9, -1])),
            "beta normalization mismatch")
    require(rising(ALPHA, 7) == Q(11486475, 128), "constant lower bound mismatch")

    return {
        "status": "SEVEN_FACTOR_INDEPENDENT_ACCEPT",
        "mixed_derivative_terms": len(direct),
        "terms_by_gram_degree": term_counts,
        "mixed_derivative_sha256": polynomial_hash(direct),
        "spectra": spectra,
        "beta_scaled_coefficients": [str(value) for value in scaled_beta],
        "kernel_constant": str(rising(ALPHA, 7)),
        "damaged_projection_rejected": damage_rejected,
    }


if __name__ == "__main__":
    record = main_record()
    expected = json.loads((ROOT / "EXPECTED.json").read_text())
    require(record == expected, "output differs from pinned expected record")
    print(json.dumps(record, indent=2, sort_keys=True))
