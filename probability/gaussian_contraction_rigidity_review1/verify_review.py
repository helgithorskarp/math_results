#!/usr/bin/env python3
"""Independent exact checks for the Gaussian contraction rigidity review.

The checks deliberately target the finite-dimensional Procrustes reduction
with a non-diagonal positive cross-covariance, a singular aligned example,
and the smallest counterexample to omitting the orthogonal alignment.  A
separate exhaustive one-dimensional enumeration checks the final
pair-distortion-to-rigid-error bound directly from its definitions.
"""

import json
from fractions import Fraction as F
from itertools import product


def fail(message):
    raise RuntimeError(message)


def check(condition, message):
    if not condition:
        fail(message)


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x + y for x, y in zip(arow, brow)]
            for arow, brow in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(arow, brow)]
            for arow, brow in zip(a, b)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in bt] for row in a]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def frobenius_squared(a):
    return sum((x * x for row in a for x in row), F(0))


def symmetric(a):
    return a == transpose(a)


def psd_2_by_2(a):
    check(len(a) == 2 and all(len(row) == 2 for row in a),
          "PSD helper received a non-2-by-2 matrix")
    return (symmetric(a) and a[0][0] >= 0 and a[1][1] >= 0
            and a[0][0] * a[1][1] - a[0][1] * a[1][0] >= 0)


def fraction_text(x):
    return str(x.numerator) if x.denominator == 1 else str(x)


def matrix_text(a):
    return [[fraction_text(x) for x in row] for row in a]


def aligned_fixture():
    # B was obtained as (A^T)^(-1) M.  Thus A^T B=M exactly, but M is
    # non-diagonal and the two covariance matrices do not commute.
    a = [[F(2), F(1)], [F(0), F(1)]]
    b = [[F(1), F(1, 4)], [F(-1, 2), F(3, 4)]]
    kappa = F(1, 2)
    atb = matmul(transpose(a), b)
    ata = matmul(transpose(a), a)
    btb = matmul(transpose(b), b)
    identity = [[F(1), F(0)], [F(0), F(1)]]
    check(atb == [[F(2), F(1, 2)], [F(1, 2), F(1)]],
          "unexpected non-diagonal cross-covariance")
    check(psd_2_by_2(atb), "aligned cross-covariance is not PSD")
    check(psd_2_by_2(sub(ata, scale(kappa, identity))),
          "claimed covariance lower bound fails")
    check(matmul(ata, btb) != matmul(btb, ata),
          "fixture accidentally has commuting covariance matrices")

    u = add(a, b)
    v = sub(a, b)
    h = sub(matmul(a, transpose(a)), matmul(b, transpose(b)))
    lhs = frobenius_squared(h)
    first = F(1, 2) * trace(matmul(matmul(transpose(u), u),
                                         matmul(transpose(v), v)))
    utv = matmul(transpose(u), v)
    second = F(1, 2) * trace(matmul(utv, utv))
    lower = F(1, 2) * kappa * frobenius_squared(v)
    check(symmetric(utv), "U^T V should be symmetric after alignment")
    check(second >= 0, "second trace term should be nonnegative")
    check(lhs == first + second, "trace identity (18) failed")
    check(lhs >= lower, "Procrustes lower bound failed")
    return {
        "A": matrix_text(a),
        "B": matrix_text(b),
        "A_transpose_B": matrix_text(atb),
        "covariances_noncommute": True,
        "kappa": fraction_text(kappa),
        "H_norm_squared": fraction_text(lhs),
        "trace_term_1": fraction_text(first),
        "trace_term_2": fraction_text(second),
        "kappa_error_over_2": fraction_text(lower),
    }


def singular_fixture():
    a = [[F(1), F(0)], [F(0), F(1)]]
    b = [[F(1), F(0)], [F(0), F(0)]]
    atb = matmul(transpose(a), b)
    h = sub(matmul(a, transpose(a)), matmul(b, transpose(b)))
    lhs = frobenius_squared(h)
    lower = F(1, 2) * frobenius_squared(sub(a, b))
    check(psd_2_by_2(atb), "singular cross-covariance is not PSD")
    check(atb[0][0] * atb[1][1] - atb[0][1] * atb[1][0] == 0,
          "cross-covariance should be singular")
    check(lhs >= lower, "singular aligned Procrustes bound failed")
    return {
        "A_transpose_B": matrix_text(atb),
        "H_norm_squared": fraction_text(lhs),
        "kappa_error_over_2": fraction_text(lower),
    }


def alignment_is_necessary():
    identity = [[F(1), F(0)], [F(0), F(1)]]
    rotation = [[F(0), F(-1)], [F(1), F(0)]]
    h = sub(matmul(identity, transpose(identity)),
            matmul(rotation, transpose(rotation)))
    unaligned_lhs = frobenius_squared(h)
    unaligned_lower = F(1, 2) * frobenius_squared(sub(identity, rotation))
    check(unaligned_lhs == 0 and unaligned_lower > 0,
          "unaligned rotation should refute the unoptimized bound")
    q = transpose(rotation)
    aligned_b = matmul(rotation, q)
    aligned_lower = F(1, 2) * frobenius_squared(sub(identity, aligned_b))
    check(aligned_b == identity and aligned_lower == 0,
          "orthogonal alignment did not repair the rotation example")
    return {
        "dimension": 2,
        "unaligned_H_norm_squared": fraction_text(unaligned_lhs),
        "unaligned_kappa_error_over_2": fraction_text(unaligned_lower),
        "aligned_error": fraction_text(aligned_lower),
    }


def mean(values):
    return sum(values, F(0)) / len(values)


def variance(values):
    m = mean(values)
    return mean([(x - m) ** 2 for x in values])


def one_dimensional_enumeration():
    x = [F(-1), F(0), F(1)]
    grid = [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]
    admissible = 0
    isometric = 0
    strict = 0
    max_ratio = F(0)
    fold_record = None
    for y_tuple in product(grid, repeat=3):
        y = list(y_tuple)
        if any(abs(y[i] - y[j]) > abs(x[i] - x[j])
               for i in range(3) for j in range(3)):
            continue
        admissible += 1
        distortion = mean([
            (x[i] - x[j]) ** 2 - (y[i] - y[j]) ** 2
            for i in range(3) for j in range(3)
        ])
        rigid_error = min(
            variance([y[i] - x[i] for i in range(3)]),
            variance([y[i] + x[i] for i in range(3)]),
        )
        # Here R=1 and kappa=Var(X)=2/3, so theorem (3) reads error<=3D.
        check(distortion >= 0, "a contraction produced negative distortion")
        check(rigid_error <= 3 * distortion,
              "one-dimensional rigid-error estimate failed")
        check((distortion == 0) == (rigid_error == 0),
              "equality characterization failed on a three-point law")
        if distortion == 0:
            isometric += 1
        else:
            strict += 1
            max_ratio = max(max_ratio, rigid_error / distortion)
        if y == [F(1), F(0), F(1)]:
            fold_record = {
                "D": fraction_text(distortion),
                "optimal_rigid_error_squared": fraction_text(rigid_error),
            }
    check(fold_record is not None, "fold test was not enumerated")
    check(admissible == isometric + strict, "enumeration counts disagree")
    return {
        "support": [fraction_text(v) for v in x],
        "image_grid": [fraction_text(v) for v in grid],
        "admissible_maps": admissible,
        "isometric_maps": isometric,
        "strict_maps": strict,
        "largest_error_over_D": fraction_text(max_ratio),
        "absolute_value_fold": fold_record,
    }


def main():
    report = {
        "arithmetic": "fractions.Fraction; standard library only",
        "non_diagonal_aligned_fixture": aligned_fixture(),
        "singular_aligned_fixture": singular_fixture(),
        "alignment_necessity_adversary": alignment_is_necessary(),
        "one_dimensional_exhaustion": one_dimensional_enumeration(),
        "scope": (
            "Exact finite audit of the alignment and Gram reductions only; "
            "the analytic entropy theorem remains human-checked."
        ),
        "status": "INDEPENDENT_EXACT_CHECKS_PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
