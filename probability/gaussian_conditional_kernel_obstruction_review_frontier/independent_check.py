#!/usr/bin/env python3
"""Independent exact checks for the paired-rank conditional-kernel theorem.

This file imports no author module.  Unlike the author's multivariate Taylor
expansion of Phi, it reconstructs every moment through degree four as a formal
R moment times six independent Gaussian moments (a Wick/product calculation).
All certificate arithmetic uses int and Fraction.
"""
from __future__ import annotations

from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_conditional_kernel_obstruction"
TARGET_COMMIT = "01e1684e032295ee1c4bf11f2bca7836912258e7"
PINNED = {
    ".gitignore": "32dae3052f331ee34d628ef535709b301259a45df7c7522c4d35dcf49873f00b",
    "CERTIFICATE.json": "b2be190a25177a93ff58ef7ae348455e4585c2475033c6c82e540045fb9a9305",
    "PROOF.md": "d55aca6470fef9d7c9908e3f70e9c8435e8c7703aae6ef6426aaa7107f1a2f4c",
    "README.md": "fcfa96fc5b41ad207ddaa6ce7ef07fbf607ba616b7c4175d3bca823624948106",
    "SHA256SUMS": "231c78213bd87b9d7bc78de9681ff4bff3fcca927690ff3ccbfd1a751a54854c",
    "SOURCES.md": "caeafb0076f07b756c4c81e6fdf014655817a9addae6efa835d23c6fec445d97",
    "verify.py": "1e5408062c1fbb4d2c2a7f4ecd619554e595ffac8370ebc5c58acb1f8e5c4348",
}

NVARIABLES = 7  # formal variables R,Z_1,...,Z_6, or Y_0,...,Y_6
ZERO = (0,) * NVARIABLES


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_digest(path):
    return sha256(path.read_bytes()).hexdigest()


def json_digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def clean(poly):
    return {powers: coefficient for powers, coefficient in poly.items() if coefficient}


def constant(value):
    value = Q(value)
    return {ZERO: value} if value else {}


def variable(index):
    powers = list(ZERO)
    powers[index] = 1
    return {tuple(powers): Q(1)}


def add(*polynomials):
    answer = {}
    for poly in polynomials:
        for powers, coefficient in poly.items():
            answer[powers] = answer.get(powers, Q(0)) + coefficient
    return clean(answer)


def scale(poly, coefficient):
    coefficient = Q(coefficient)
    return clean({powers: coefficient * value for powers, value in poly.items()})


def multiply(left, right):
    answer = {}
    for a, u in left.items():
        for b, v in right.items():
            powers = tuple(x + y for x, y in zip(a, b))
            answer[powers] = answer.get(powers, Q(0)) + u * v
    return clean(answer)


def power(poly, exponent):
    require(isinstance(exponent, int) and exponent >= 0, "bad polynomial power")
    answer = constant(1)
    base = poly
    while exponent:
        if exponent & 1:
            answer = multiply(answer, base)
        exponent //= 2
        if exponent:
            base = multiply(base, base)
    return answer


def rising(value, exponent):
    answer = Q(1)
    for offset in range(exponent):
        answer *= value + offset
    return answer


def gaussian_moment(exponent):
    """Moment of one N(0,1/2) coordinate."""
    if exponent & 1:
        return Q(0)
    half = exponent // 2
    numerator = 1
    for value in range(2, exponent + 1):
        numerator *= value
    denominator = (4**half)
    for value in range(2, half + 1):
        denominator *= value
    return Q(numerator, denominator)


def formal_expectation(poly, shape=Q(-1, 2)):
    """Apply ell(R^k)=(shape)_k/2^k and independent Gaussian moments."""
    answer = Q(0)
    for powers, coefficient in poly.items():
        term = coefficient * rising(shape, powers[0]) / (2 ** powers[0])
        for exponent in powers[1:]:
            term *= gaussian_moment(exponent)
        answer += term
    return answer


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), Q(0))


def matrix_rank(rows):
    rows = [list(map(Q, row)) for row in rows]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [entry / pivot_value for entry in rows[rank]]
        for index in range(len(rows)):
            if index != rank and rows[index][column]:
                factor = rows[index][column]
                rows[index] = [a - factor * b for a, b in zip(rows[index], rows[rank])]
        rank += 1
    return rank


def matrix_inverse(matrix):
    size = len(matrix)
    rows = [list(map(Q, row)) + [Q(i == j) for j in range(size)]
            for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((i for i in range(column, size) if rows[i][column]), None)
        require(pivot is not None, "singular Gram matrix")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        pivot_value = rows[column][column]
        rows[column] = [entry / pivot_value for entry in rows[column]]
        for index in range(size):
            if index != column and rows[index][column]:
                factor = rows[index][column]
                rows[index] = [a - factor * b for a, b in zip(rows[index], rows[column])]
    return [row[size:] for row in rows]


def matrix_determinant(matrix):
    rows = [list(map(Q, row)) for row in matrix]
    determinant = Q(1)
    for column in range(len(rows)):
        pivot = next((i for i in range(column, len(rows)) if rows[i][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            determinant = -determinant
        pivot_value = rows[column][column]
        determinant *= pivot_value
        for index in range(column + 1, len(rows)):
            if rows[index][column]:
                factor = rows[index][column] / pivot_value
                rows[index] = [a - factor * b
                               for a, b in zip(rows[index], rows[column])]
    return determinant


def geometry(record):
    source = [tuple(map(Q, row)) for row in record["source"]]
    target = [tuple(map(Q, row)) for row in record["target"]]
    require(len(source) == len(target) == 7, "wrong geometry size")
    losses = []
    for i in range(7):
        for j in range(i):
            source_distance = sum((a - b) ** 2 for a, b in zip(source[i], source[j]))
            target_distance = sum((a - b) ** 2 for a, b in zip(target[i], target[j]))
            losses.append(source_distance - target_distance)
    require(all(loss >= 0 for loss in losses), "fixture is not a contraction")
    require(losses.count(Q(4)) == 3 and losses.count(Q(0)) == 18,
            "unexpected pair-loss distribution")
    require(record["base_pair"] == [1, 2], "unexpected base pair")
    base_loss = (sum((a - b) ** 2 for a, b in zip(source[1], source[2]))
                 - sum((a - b) ** 2 for a, b in zip(target[1], target[2])))
    require(base_loss == 4, "distinguished pair has wrong loss")

    paired = [x + y for x, y in zip(source, target)]
    center = tuple((paired[1][j] + paired[2][j]) / 2 for j in range(6))
    w = [tuple(value - center[j] for j, value in enumerate(row)) for row in paired]
    recorded_w = [[str(value) for value in row] for row in w]
    require(recorded_w == record["w"], "dimensionless coordinates differ")
    differences = [tuple(a - b for a, b in zip(row, w[0])) for row in w[1:]]
    gram = [[dot(a, b) for b in differences] for a in differences]
    require(matrix_rank(differences) == 6, "paired affine rank is not six")
    require(gram == [[Q(2) if i == j else Q(0) for j in range(6)]
                     for i in range(6)], "unexpected explicit Gram matrix")
    return w, gram, {
        "labels": 7,
        "paired_affine_rank": 6,
        "positive_pair_losses": 3,
        "zero_pair_losses": 18,
        "distinguished_pair_loss": 4,
        "gram_determinant": int(matrix_determinant(gram)),
    }


def substituted_y_polynomials(w):
    formal_r = variable(0)
    zs = [variable(index) for index in range(1, 7)]
    ys = []
    for center in w:
        value = formal_r
        for z, coordinate in zip(zs, center):
            displacement = add(z, constant(-coordinate))
            value = add(value, scale(power(displacement, 2), Q(1, 2)))
        ys.append(value)
    return formal_r, ys


def witness_polynomial(variables):
    y0 = variables[0]
    answer = scale(y0, 4)
    for yi in variables[1:]:
        answer = add(answer, scale(power(add(constant(1), y0, scale(yi, -1)), 2), -1))
    return answer


def polynomial_record(poly):
    return [{"powers": list(powers), "coefficient": str(coefficient)}
            for powers, coefficient in sorted(poly.items())]


def moment_certificate(w, gram, record):
    formal_r, substituted_ys = substituted_y_polynomials(w)
    substituted_witness = witness_polynomial(substituted_ys)
    require(substituted_witness == scale(formal_r, 4), "independent P(Y)=4R failed")

    y_variables = [variable(index) for index in range(7)]
    witness = witness_polynomial(y_variables)
    require(polynomial_record(witness) == record["witness_terms"],
            "witness polynomial differs")

    powers_by_y = [[power(substituted_ys[index], exponent) for exponent in range(5)]
                   for index in range(7)]

    @lru_cache(maxsize=None)
    def moment(multi_index):
        poly = constant(1)
        for index, exponent in enumerate(multi_index):
            poly = multiply(poly, powers_by_y[index][exponent])
        return formal_expectation(poly)

    all_indices = sorted(index for index in product(range(5), repeat=7)
                         if sum(index) <= 4)
    moments = {index: moment(index) for index in all_indices}
    require(len(moments) == 330, "degree-four moment coverage failed")
    basis = sorted(index for index in product(range(3), repeat=7) if sum(index) <= 2)
    require(len(basis) == 36, "quadratic basis coverage failed")
    matrix = [[moments[tuple(a + b for a, b in zip(left, right))]
               for right in basis] for left in basis]
    raw = json.dumps([[str(entry) for entry in row] for row in matrix],
                     separators=(",", ":")).encode()
    matrix_digest = sha256(raw).hexdigest()
    require(matrix_digest == record["moment_matrix_sha256"], "moment matrix hash differs")
    vector = [witness.get(index, Q(0)) for index in basis]
    quadratic_value = sum(vector[i] * matrix[i][j] * vector[j]
                          for i in range(36) for j in range(36))
    require(quadratic_value == Q(-1), "negative square differs")
    require(formal_expectation(power(substituted_witness, 2)) == Q(-1),
            "direct Wick witness evaluation differs")

    inverse = matrix_inverse(gram)
    r_polys = []
    for index, yi in enumerate(substituted_ys[1:]):
        difference = tuple(a - b for a, b in zip(w[index + 1], w[0]))
        d_i = dot(difference, difference) / 2
        r_polys.append(add(substituted_ys[0], scale(yi, -1), constant(d_i)))
    gram_quadratic = {}
    for i in range(6):
        for j in range(6):
            gram_quadratic = add(
                gram_quadratic,
                scale(multiply(r_polys[i], r_polys[j]), inverse[i][j]),
            )
    reconstructed_r = add(substituted_ys[0], scale(gram_quadratic, Q(-1, 2)))
    require(reconstructed_r == formal_r, "basis-independent R_G(Y)=R failed")
    require(formal_expectation(power(reconstructed_r, 2)) == Q(-1, 16),
            "general Gram negative square differs")

    controls = []
    for alpha, expected in ((Q(3), Q(0)), (Q(7, 2), Q(3))):
        shape = alpha - 3
        value = formal_expectation(power(substituted_witness, 2), shape)
        require(value == expected, "effective-dimension control differs")
        controls.append({"alpha": str(alpha), "square_value": str(value)})
    require(controls == record["effective_dimension_controls"],
            "effective-dimension record differs")
    return {
        "method": "formal residual moments times six coordinatewise Gaussian moments",
        "moments_through_degree_four": len(moments),
        "moment_matrix_dimension": len(basis),
        "moment_matrix_sha256": matrix_digest,
        "negative_square": str(quadratic_value),
        "substitution": "P(Y)=4R",
        "general_gram_substitution": "R_G(Y)=R",
        "general_gram_square": "-1/16",
        "effective_dimension_controls": controls,
    }


def replication_scatter_controls(w):
    """Check the exact scatter scaling behind the finite-difference bridge."""
    cases = [
        (2, [1, 0, 2, 0, 1, 0, 0]),
        (3, [0, 2, 1, 1, 0, 1, 0]),
        (5, [2, 1, 0, 3, 0, 1, 2]),
    ]
    results = []
    for n, added_counts in cases:
        counts = list(added_counts)
        counts[1] += n
        counts[2] += n
        total = sum(counts)
        direct = (sum(Q(count) * dot(center, center)
                      for count, center in zip(counts, w)) / n)
        vector_sum = tuple(sum(Q(count) * center[j]
                               for count, center in zip(counts, w))
                           for j in range(6))
        direct -= dot(vector_sum, vector_sum) / (n * total)

        weights = [Q(count, n) for count in added_counts]
        closed = Q(2) + sum(weight * dot(center, center)
                            for weight, center in zip(weights, w))
        weighted_sum = tuple(sum(weight * center[j]
                                 for weight, center in zip(weights, w))
                             for j in range(6))
        closed -= dot(weighted_sum, weighted_sum) / (2 + sum(weights))
        require(direct == closed, "replication scatter scaling differs")
        results.append({"n": n, "added_positions": sum(added_counts),
                        "dimensionless_scatter": str(direct)})
    return results


def validate_record(record, geometry_report, moment_report):
    require(record["status"] == "EXACT_CONDITIONAL_JOINT_MOMENT_OBSTRUCTION",
            "wrong author status")
    require(record["p"] == 2 and record["t"] == "1/2"
            and record["variance"] == "1/2", "wrong author normalization")
    require(record["moment_terms_through_degree4"] == 330, "wrong moment count")
    require(record["moment_matrix_dimension"] == 36, "wrong matrix dimension")
    require(record["negative_square_value"] == moment_report["negative_square"],
            "wrong recorded square")
    require(record["moment_matrix_sha256"] == moment_report["moment_matrix_sha256"],
            "wrong recorded matrix hash")
    require(record["formal_residual_second_moment"] == "-1/16",
            "wrong recorded residual moment")
    require(geometry_report["paired_affine_rank"] == 6, "geometry report changed")


def run():
    for name, expected in PINNED.items():
        require(file_digest(TARGET / name) == expected, "changed target: " + name)
    record = json.loads((TARGET / "CERTIFICATE.json").read_text())
    w, gram, geometry_report = geometry(record)
    moment_report = moment_certificate(w, gram, record)
    validate_record(record, geometry_report, moment_report)
    replication = replication_scatter_controls(w)

    rejection_controls = 0
    for field, value in (("negative_square_value", "0"),
                         ("moment_matrix_sha256", "0" * 64)):
        damaged = json.loads(json.dumps(record))
        damaged[field] = value
        try:
            validate_record(damaged, geometry_report, moment_report)
        except RuntimeError:
            rejection_controls += 1
        else:
            raise RuntimeError("damaged record accepted: " + field)
    damaged = json.loads(json.dumps(record))
    damaged["w"][0][0] = "1"
    try:
        geometry(damaged)
    except RuntimeError:
        rejection_controls += 1
    else:
        raise RuntimeError("damaged geometry accepted")
    require(rejection_controls == 3, "rejection controls incomplete")

    return {
        "status": "INDEPENDENT_CONDITIONAL_KERNEL_CLASSIFICATION_REVIEW_PASS",
        "target_graph_ref": "bafkreicivyxiwogu64smlmuc3b2enfxmu7duowy7nr44yw5yzzeaeeutla",
        "target_source_commit": TARGET_COMMIT,
        "pinned_files": PINNED,
        "author_certificate_sha256": PINNED["CERTIFICATE.json"],
        "geometry": geometry_report,
        "moment_certificate": moment_report,
        "replication_scatter_controls": replication,
        "rejection_controls": rejection_controls,
        "analytic_scope": {
            "rank_at_most_five": "positive five-dimensional Gaussian product integral",
            "rank_six": "negative moment square plus Bernstein representation and finite differences",
            "endpoint_beta_sign": "not implied",
        },
    }


if __name__ == "__main__":
    require(sys.argv[1:] in ([], ["--json"]),
            "usage: independent_check.py [--json]")
    report = run()
    summary = {
        "status": report["status"],
        "record_sha256": json_digest(report),
        "moments": report["moment_certificate"]["moments_through_degree_four"],
        "matrix_dimension": report["moment_certificate"]["moment_matrix_dimension"],
        "negative_square": report["moment_certificate"]["negative_square"],
    }
    expected_path = HERE / "EXPECTED.json"
    if expected_path.exists():
        require(summary == json.loads(expected_path.read_text()), "expected record mismatch")
    if sys.argv[1:] == ["--json"]:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(summary["status"])
        print("record_sha256", summary["record_sha256"])
        print("moments", summary["moments"])
        print("matrix_dimension", summary["matrix_dimension"])
        print("negative_square", summary["negative_square"])
