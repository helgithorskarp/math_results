#!/usr/bin/env python3
"""Independent exact checks for the six-column Gaussian beta theorem.

The universal sign is an analytic theorem, not a finite computation.  This
checker reconstructs its geometric identity by an exact rational nullspace
calculation, and independently checks the replica and polarization handoffs.
It imports no author code and evaluates no floating-point Gaussian signs.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
EXPECTED = HERE / "REVIEW_EXPECTED.json"

PINS = {
    "probability/gaussian_beta_projection/PROOF.md":
        "1486ad73eae94a733df304a9340660d8aaa974f57ae5269b5429ca0f92004189",
    "probability/gaussian_beta_projection/audit.py":
        "43ec1cd5692d9283c41cee8c9d6825dbe302603a3ddc609807b8fd4504aa771c",
    "probability/gaussian_beta_projection/EXPECTED.json":
        "3239be5d96ed4c74be4d9a51e953e2a4c2c6c28375df4f4dd8178c930afe2865",
    "probability/gaussian_beta_projection/SOURCES.md":
        "8d3f13902cddcaf977b30c78f60bb9159818fdc1e9d820cf090325f1b2473c5b",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def stable_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def check_pins() -> None:
    for name, wanted in PINS.items():
        got = sha256((REPO / name).read_bytes()).hexdigest()
        require(got == wanted, f"changed reviewed input: {name}")


def dot(a: tuple[Q, ...], b: tuple[Q, ...]) -> Q:
    return sum((x * y for x, y in zip(a, b)), Q(0))


def sub(a: tuple[Q, ...], b: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(x - y for x, y in zip(a, b))


def mean(points: list[tuple[Q, ...]]) -> tuple[Q, ...]:
    require(bool(points), "empty mean")
    return tuple(sum((p[j] for p in points), Q(0)) / len(points)
                 for j in range(len(points[0])))


def inverse(matrix: list[list[Q]]) -> list[list[Q]]:
    n = len(matrix)
    require(n > 0 and all(len(row) == n for row in matrix), "square matrix required")
    work = [[Q(x) for x in row] + [Q(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col]), None)
        require(pivot is not None, "singular matrix")
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for row in range(n):
            if row == col:
                continue
            scale = work[row][col]
            work[row] = [x - scale * y for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def nullspace(rows: list[tuple[Q, ...]], dimension: int) -> list[tuple[Q, ...]]:
    """Return an exact RREF basis for vectors annihilated by all rows."""
    if not rows:
        return [tuple(Q(i == j) for i in range(dimension)) for j in range(dimension)]
    require(all(len(row) == dimension for row in rows), "row dimension")
    work = [[Q(x) for x in row] for row in rows]
    pivot_columns: list[int] = []
    pivot_row = 0
    for col in range(dimension):
        pivot = next((row for row in range(pivot_row, len(work)) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [x / scale for x in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            scale = work[row][col]
            work[row] = [x - scale * y for x, y in zip(work[row], work[pivot_row])]
        pivot_columns.append(col)
        pivot_row += 1
        if pivot_row == len(work):
            break
    free_columns = [j for j in range(dimension) if j not in pivot_columns]
    basis = []
    for free in free_columns:
        vector = [Q(0)] * dimension
        vector[free] = Q(1)
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -work[row][free]
        basis.append(tuple(vector))
    require(all(dot(row, vector) == 0 for row in rows for vector in basis),
            "nullspace construction")
    return basis


def perpendicular_form(null_basis: list[tuple[Q, ...]]):
    if not null_basis:
        return lambda _a, _b: Q(0)
    gram = [[dot(a, b) for b in null_basis] for a in null_basis]
    gram_inverse = inverse(gram)

    def form(a: tuple[Q, ...], b: tuple[Q, ...]) -> Q:
        left = [dot(a, w) for w in null_basis]
        right = [dot(b, w) for w in null_basis]
        return sum((left[i] * gram_inverse[i][j] * right[j]
                    for i in range(len(left)) for j in range(len(right))), Q(0))

    return form


def subsets(items: tuple[int, ...]):
    for size in range(len(items) + 1):
        yield from combinations(items, size)


def affine_rank(points: list[tuple[Q, ...]]) -> int:
    if len(points) <= 1:
        return 0
    return len(points[0]) - len(nullspace([sub(p, points[0]) for p in points[1:]],
                                          len(points[0])))


def projection_case(base: list[tuple[Q, ...]], holes: list[tuple[Q, ...]],
                    effective_dimension: int = 5) -> dict[str, object]:
    """Verify the subset-independent energy via the orthogonal nullspace."""
    require(bool(base), "positive block must be nonempty")
    ambient = len(base[0])
    require(ambient > 0 and all(len(p) == ambient for p in base + holes), "point dimension")
    center = mean(base)
    centered = [sub(p, center) for p in base + holes]
    hole_vectors = centered[len(base):]
    null_basis = nullspace(hole_vectors, ambient)
    hole_rank = ambient - len(null_basis)
    require(hole_rank <= effective_dimension, "remaining span exceeds effective dimension")
    perp = perpendicular_form(null_basis)
    energy = sum((perp(v, v) for v in centered[:len(base)]), Q(0))
    require(energy >= 0, "negative perpendicular energy")
    require(all(perp(v, v) == 0 for v in hole_vectors), "remaining vector not in span")
    base_sum = tuple(sum((v[j] for v in centered[:len(base)]), Q(0))
                     for j in range(ambient))
    require(all(x == 0 for x in base_sum) and perp(base_sum, base_sum) == 0,
            "positive perpendicular components do not sum to zero")

    checks = 0
    base_indices = tuple(range(len(base)))
    hole_indices = tuple(range(len(base), len(centered)))
    for chosen in subsets(hole_indices):
        indices = base_indices + chosen
        original_pair_sum = Q(0)
        projected_pair_sum = Q(0)
        for i, j in combinations(indices, 2):
            difference = sub(centered[i], centered[j])
            squared = dot(difference, difference)
            removed = perp(difference, difference)
            require(0 <= removed <= squared, "invalid orthogonal component")
            original_pair_sum += squared
            projected_pair_sum += squared - removed
        require((original_pair_sum - projected_pair_sum) / len(indices) == energy,
                "perpendicular energy depends on subset")
        checks += 1

    return {
        "base_size": len(base),
        "remaining_size": len(holes),
        "remaining_span_rank": hole_rank,
        "whole_affine_rank": affine_rank(base + holes),
        "perpendicular_energy": str(energy),
        "subset_checks": checks,
    }


def generic_points(count: int, dimension: int = 6) -> list[tuple[Q, ...]]:
    return [tuple(Q(((i + 3) ** (j + 1) + 7 * i * j) % 53 - 26,
                          i + 2 * j + 5)
                  for j in range(dimension)) for i in range(count)]


def projection_audit() -> tuple[dict[str, object], dict[str, int]]:
    zero = (Q(0),) * 6
    axes = [tuple(Q(i == j) for j in range(6)) for i in range(6)]
    cases: dict[str, object] = {}
    cases["orthogonal_axis"] = projection_case([axes[5], tuple(-x for x in axes[5])], axes[:5])
    cases["zero_span_repetitions"] = projection_case([axes[5], tuple(-x for x in axes[5])],
                                                       [zero] * 5)
    cases["generic_1_0"] = projection_case(generic_points(1), [])
    cases["generic_3_1"] = projection_case(generic_points(3), generic_points(4)[3:])
    cases["generic_5_3"] = projection_case(generic_points(5), generic_points(8)[5:])
    cases["generic_9_5"] = projection_case(generic_points(9), generic_points(14)[9:])

    x_raw = [(0, 0, 0), (2, 1, 0), (-1, 2, 1), (1, -2, 2),
             (3, 0, -1), (-2, -1, 1), (-1, 1, -3)]
    y_raw = [tuple(abs(a) for a in p) for p in x_raw]
    x = [tuple(Q(a) for a in p) for p in x_raw]
    y = [tuple(Q(a) for a in p) for p in y_raw]
    pair_losses = []
    for i, j in combinations(range(len(x)), 2):
        loss = dot(sub(x[i], x[j]), sub(x[i], x[j])) - dot(sub(y[i], y[j]), sub(y[i], y[j]))
        require(loss >= 0, "fold is not a contraction")
        pair_losses.append(loss)
    require(any(loss > 0 for loss in pair_losses), "fold must be nonisometric")
    fold_points = [tuple(Q(4, 5) * a for a in xp) + tuple(Q(3, 5) * b for b in yp)
                   for xp, yp in zip(x, y)]
    cases["genuine_fold_2_5"] = projection_case(fold_points[:2], fold_points[2:])
    require(cases["genuine_fold_2_5"]["whole_affine_rank"] == 6,
            "fold does not exercise the six-dimensional lift")
    require(cases["orthogonal_axis"]["perpendicular_energy"] == "2",
            "discarded energy control")

    rejected = 0
    try:
        projection_case([zero], axes, effective_dimension=5)
    except AssertionError:
        rejected += 1
    else:
        raise AssertionError("six independent remaining directions were accepted")
    try:
        projection_case([], axes[:5])
    except AssertionError:
        rejected += 1
    else:
        raise AssertionError("empty positive block was accepted")
    return cases, {"pair_checks": len(pair_losses),
                   "strict_pair_losses": sum(loss > 0 for loss in pair_losses),
                   "rejected_controls": rejected}


def gaussian_completion_audit() -> int:
    checks = 0
    for size in range(1, 13):
        points = generic_points(size, dimension=5)
        center = mean(points)
        pair_sum = sum((dot(sub(a, b), sub(a, b)) for a, b in combinations(points, 2)), Q(0))
        for trial in range(7):
            v = tuple(Q((trial + 2) * (j + 3) - 11, trial + j + 5) for j in range(5))
            left = sum((dot(sub(v, p), sub(v, p)) for p in points), Q(0))
            right = size * dot(sub(v, center), sub(v, center)) + pair_sum / size
            require(left == right, "Gaussian completing-square identity")
            checks += 1
    return checks


def product_expansion_audit() -> tuple[int, str]:
    records = []
    checks = 0
    for r in range(6):
        coefficients: dict[tuple[int, ...], int] = {(): 1}
        for label in range(r):
            updated = dict(coefficients)
            for monomial, coefficient in coefficients.items():
                updated[monomial + (label,)] = -coefficient
            coefficients = updated
        expected = {chosen: (-1) ** len(chosen) for chosen in subsets(tuple(range(r)))}
        require(coefficients == expected, "finite-product inclusion-exclusion")
        records.append(sorted((list(key), value) for key, value in coefficients.items()))
        checks += len(coefficients)
    return checks, stable_digest(records)


def normalization_audit() -> dict[str, int]:
    replica = 0
    for m in range(2, 258):
        # derivative 1/(2ms), division by m(m-1), then exchangeability
        coefficient = Q(comb(m, 2), 2 * m * m * (m - 1))
        require(coefficient == Q(1, 4 * m), "replica coefficient")
        replica += 1

    coupling = 0
    for k in range(17):
        for r in range(6):
            labels = tuple(range(r))
            left: dict[tuple[int, ...], int] = {}
            for size in range(r + 1):
                chosen = list(combinations(labels, size))
                require(len(chosen) == comb(r, size), "binomial subset count")
                for subset in chosen:
                    left[subset] = (-1) ** size
            right = {subset: (-1) ** len(subset) for subset in subsets(labels)}
            require(left == right and sum(left.values()) == (1 if r == 0 else 0),
                    f"unused-replica coupling k={k}, r={r}")
            coupling += len(left)

    polarization = 0
    for n in range(81):
        for k in range(n + 1):
            for q in range(k, n + 1):
                direct = Q((n + 1) * comb(n, k) * comb(n - k, q - k),
                           (q + 2) * (q + 1) * comb(n + 2, q + 2))
                grouped = Q(comb(q, k), n + 2)
                require(direct == grouped, "polarization coefficient")
                polarization += 1
    return {"replica_coefficients": replica,
            "coupled_subset_symbols": coupling,
            "polarization_coefficients": polarization}


def run() -> dict[str, object]:
    check_pins()
    projections, fold = projection_audit()
    product_checks, product_digest = product_expansion_audit()
    normalizations = normalization_audit()
    return {
        "status": "INDEPENDENT_GAUSSIAN_BETA_PROJECTION_REVIEW_PASS",
        "reviewed_commit": "8a1e00a5328e9e340b2e511b2adf6893231e5d03",
        "source_pins": len(PINS),
        "arithmetic": "Python integers and Fraction; no floating-point sign evaluation",
        "method": "base-centroid rational nullspace and nullspace-Gram inverse",
        "projection_cases": projections,
        "projection_subset_checks": sum(case["subset_checks"] for case in projections.values()),
        "fold_control": fold,
        "gaussian_completion_checks": gaussian_completion_audit(),
        "finite_product_checks": product_checks,
        "finite_product_digest": product_digest,
        "normalizations": normalizations,
        "scope": "r<=5 projection theorem and polarized coefficients only; no r=6 or full majorisation",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.check:
        wanted = json.loads(EXPECTED.read_text())
        require(result == wanted, "review output differs from REVIEW_EXPECTED.json")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print(result["status"], stable_digest(result))


if __name__ == "__main__":
    main()
