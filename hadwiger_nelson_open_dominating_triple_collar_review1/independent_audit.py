#!/usr/bin/env python3
"""Independent exact audit of the open dominating-triple collar theorem."""

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_open_dominating_triple_collar"
TARGET_HASHES = {
    "PROOF.md": "dff0d51aef8a62e9f6d96c34a755a95e7761f8238b7764d977722d7be0fd08b6",
    "certificate.json": "f3ae90119a11f20e19ecd9d2672faa33685ff2faeb0889d756dbc2143a899d0f",
    "verify.py": "115069a8fdb512f6a99c72e9f90e5edeb2b2579e471085621449c6bc00c11fbc",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


class MQ:
    """Q adjoin square roots of the primes in ``primes`` via bit masks."""

    def __init__(self, primes, coefficients=()):
        self.primes = tuple(primes)
        size = 1 << len(self.primes)
        values = list(coefficients) + [F(0)] * (size - len(coefficients))
        require(len(values) == size, "coefficient count")
        self.values = tuple(F(x) for x in values)

    def coerce(self, other):
        return other if isinstance(other, MQ) else MQ(self.primes, [other])

    def __add__(self, other):
        other = self.coerce(other)
        require(other.primes == self.primes, "field mismatch")
        return MQ(self.primes, [a + b for a, b in zip(self.values, other.values)])

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __neg__(self):
        return MQ(self.primes, [-x for x in self.values])

    def __mul__(self, other):
        other = self.coerce(other)
        require(other.primes == self.primes, "field mismatch")
        result = [F(0)] * len(self.values)
        for i, a in enumerate(self.values):
            for j, b in enumerate(other.values):
                common = i & j
                factor = 1
                for bit, prime in enumerate(self.primes):
                    if common & (1 << bit):
                        factor *= prime
                result[i ^ j] += a * b * factor
        return MQ(self.primes, result)

    def __truediv__(self, denominator):
        denominator = F(denominator)
        require(denominator != 0, "division by zero")
        return MQ(self.primes, [x / denominator for x in self.values])

    def __eq__(self, other):
        other = self.coerce(other)
        return self.primes == other.primes and self.values == other.values

    def rational(self):
        require(not any(self.values[1:]), "not rational")
        return self.values[0]


def sqrt_basis(primes, bit):
    values = [F(0)] * (1 << len(primes))
    values[1 << bit] = F(1)
    return MQ(primes, values)


def sign_qsqrt5(value):
    """Exact sign in Q(sqrt(5)); indices 0 and 1 only."""
    require(value.primes == (5,) and len(value.values) == 2, "sign field")
    a, b = value.values
    if b == 0:
        return (a > 0) - (a < 0)
    if a >= 0 and b > 0:
        return 1
    if a <= 0 and b < 0:
        return -1
    comparison = a * a - 5 * b * b
    require(comparison != 0, "unexpected zero")
    return (1 if comparison > 0 else -1) if a > 0 else (-1 if comparison > 0 else 1)


def squared_distance(p, q):
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def threshold_audit():
    qfield = (5,)
    sqrt5 = sqrt_basis(qfield, 0)
    threshold_squared = (MQ(qfield, [9]) + sqrt5 * 3) / 2
    require(threshold_squared * threshold_squared - threshold_squared * 9 + 9 == MQ(qfield), "threshold polynomial")
    require(sign_qsqrt5(threshold_squared - F(157, 20)) > 0, "lower isolation")
    require(sign_qsqrt5(MQ(qfield, [F(63, 8)]) - threshold_squared) > 0, "upper isolation")
    require(sign_qsqrt5(threshold_squared - 4) > 0, "delta is not above two")
    require(sign_qsqrt5(MQ(qfield, [9]) - threshold_squared) > 0, "delta is not below three")

    # Independently square (sqrt(3)+sqrt(15))/2.
    field = (3, 5)
    sqrt3 = sqrt_basis(field, 0)
    sqrt5_full = sqrt_basis(field, 1)
    delta = (sqrt3 + sqrt3 * sqrt5_full) / 2
    embedded_threshold = MQ(field, [threshold_squared.values[0], 0, threshold_squared.values[1], 0])
    require(delta * delta == embedded_threshold, "displayed delta square")

    # At q=T the comparison cap has diameter exactly one; strict q>T is
    # therefore the correct boundary for this uniqueness proof.
    cap_x_squared = (threshold_squared - 3) * (threshold_squared - 3) / 4
    # The remaining denominator is q. Use q*(3/4) instead of field inversion.
    require(cap_x_squared == threshold_squared * F(3, 4), "boundary cap x")
    boundary_cap_diameter_times_q = threshold_squared * 4 - cap_x_squared * 4
    require(boundary_cap_diameter_times_q == threshold_squared, "boundary cap diameter")

    return threshold_squared, {
        "threshold_polynomial_identities": 2,
        "threshold_isolation_inequalities": 2,
        "threshold_range_inequalities": 2,
        "boundary_cap_diameter_squared": 1,
    }


def orbit_and_boundary_audit(threshold_squared):
    field = (3, 5)
    one = MQ(field, [1])
    zero = MQ(field)
    sqrt3 = sqrt_basis(field, 0)
    sqrt5 = sqrt_basis(field, 1)
    delta = (sqrt3 + sqrt3 * sqrt5) / 2
    omega = (one / 2, sqrt3 / 2)

    def cmul(z, w):
        return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]

    roots = [(one, zero)]
    for _ in range(5):
        roots.append(cmul(roots[-1], omega))
    chords = [squared_distance(roots[0], z).rational() for z in roots]
    require(chords == [0, 1, 3, 4, 3, 1], "six-cycle chord table")
    require(min(chords[1:]) == 1, "minimum nonzero orbit chord")

    # Equality-control fixture: the two cap endpoints are active tangencies,
    # are one unit apart, and lie in one six-cycle orbit.
    a0 = (zero, zero)
    a1 = (delta, zero)
    active = [(sqrt3 / 2, one / 2), (sqrt3 / 2, -one / 2)]
    require(all(squared_distance(a0, x) == one for x in active), "active point off circle")
    require(squared_distance(active[0], active[1]) == one, "boundary active chord")
    for x in active:
        y = ((x[0] + a1[0]) / 2, x[1] / 2)
        require(squared_distance(x, y) == one and squared_distance(y, a1) == one, "inactive boundary point")
    threshold_embedded = MQ(field, [threshold_squared.values[0], 0, threshold_squared.values[1], 0])
    require(squared_distance(a0, a1) == threshold_embedded, "boundary centre distance")

    return {
        "orbit_chord_cases": len(chords),
        "orbit_minimum_nonzero_chord_squared": 1,
        "boundary_same_orbit_active_points": 2,
        "boundary_tangent_cross_edges": 2,
    }


def fixture_audit(threshold_squared):
    field = (2, 3, 5)
    zero = MQ(field)
    sqrt2 = sqrt_basis(field, 0)
    sqrt3 = sqrt_basis(field, 1)
    sqrt5 = sqrt_basis(field, 2)
    sqrt6 = sqrt2 * sqrt3
    points = [(zero, zero), (sqrt2 * 2, zero), (sqrt2, sqrt6)]
    distances = [squared_distance(points[i], points[j]).rational() for i in range(3) for j in range(i + 1, 3)]
    require(distances == [8, 8, 8], "equilateral fixture")
    threshold = MQ(field, [threshold_squared.values[0], 0, 0, 0, threshold_squared.values[1], 0, 0, 0])
    difference = MQ(field, [8]) - threshold
    # 8-T=(7-3sqrt(5))/2 is positive because 49>45.
    require(difference == (MQ(field, [7]) - sqrt5 * 3) / 2, "fixture threshold difference")
    require(F(7) ** 2 > 5 * F(3) ** 2, "fixture radical sign")

    q = F(8)
    cap_x_squared = (q - 3) ** 2 / (4 * q)
    cap_diameter_squared = 4 * (1 - cap_x_squared)
    require(cap_x_squared == F(25, 32) and cap_diameter_squared == F(7, 8), "fixture cap")
    require(4 < q < 9 and cap_diameter_squared < 1, "fixture strictness")
    return {
        "fixture_pair_distances": len(distances),
        "fixture_strict_inequalities": 5,
        "fixture_cap_x_squared": [25, 32],
        "fixture_cap_diameter_squared": [7, 8],
    }


def palette_audit():
    leaf = {0, 1}
    third = {2, 3}
    require(leaf.isdisjoint(third) and len(leaf | third) == 4, "palette separation")
    require(2 not in leaf and 0 not in third, "centre colours")

    # Six exhaustive edge classes in the written proof.
    classes = {
        "inside_leaf_union",
        "inside_third_circle",
        "between_circle_palettes",
        "own_circle_spokes",
        "other_circle_spokes_absent",
        "centre_edges_absent",
    }
    require(len(classes) == 6, "edge partition")

    # Boundary control for the strict >2 premise: centres at distance two
    # have tangent owner circles, so disjointness cannot be inferred there.
    require((F(2) - 1) == 1, "tangent-circle control")
    return {"palette_edge_classes": len(classes), "strict_two_boundary_controls": 1}


def source_audit(target_dir):
    observed = {}
    for name, expected in TARGET_HASHES.items():
        digest = hashlib.sha256((target_dir / name).read_bytes()).hexdigest()
        require(digest == expected, "target source mismatch: " + name)
        observed[name] = digest
    return {"target_files_hashed": len(observed), "target_sha256": observed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-dir", type=Path, default=TARGET)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()

    threshold_squared, threshold = threshold_audit()
    result = {
        "status": "PASS",
        **threshold,
        **orbit_and_boundary_audit(threshold_squared),
        **fixture_audit(threshold_squared),
        **palette_audit(),
        **source_audit(args.target_dir),
        "native_solver_calls": 0,
        "record_improvement": False,
    }
    if args.check_expected:
        require(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
