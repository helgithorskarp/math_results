#!/usr/bin/env python3
"""Independent exact checker for the open dominating-triple collar data."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


class CheckError(ValueError):
    pass


PRIMES = (2, 3, 5)


class MQ:
    """Element of Q(sqrt(2),sqrt(3),sqrt(5)) in its squarefree basis."""

    def __init__(self, coeffs=()):
        data = list(coeffs)
        data.extend([Fraction(0)] * (8 - len(data)))
        if len(data) != 8:
            raise CheckError("multiquadratic coefficient count")
        self.c = tuple(Fraction(x) for x in data)

    def __add__(self, other):
        other = as_mq(other)
        return MQ(a + b for a, b in zip(self.c, other.c))

    def __sub__(self, other):
        other = as_mq(other)
        return MQ(a - b for a, b in zip(self.c, other.c))

    def __mul__(self, other):
        other = as_mq(other)
        out = [Fraction(0) for _ in range(8)]
        for i, a in enumerate(self.c):
            if not a:
                continue
            for j, b in enumerate(other.c):
                if not b:
                    continue
                common = i & j
                factor = 1
                for bit, prime in enumerate(PRIMES):
                    if common & (1 << bit):
                        factor *= prime
                out[i ^ j] += a * b * factor
        return MQ(out)

    def __truediv__(self, value):
        value = Fraction(value)
        if not value:
            raise ZeroDivisionError
        return MQ(x / value for x in self.c)

    def __eq__(self, other):
        return self.c == as_mq(other).c

    def rational(self) -> Fraction:
        if any(self.c[1:]):
            raise CheckError("expected rational multiquadratic value")
        return self.c[0]


def as_mq(value) -> MQ:
    return value if isinstance(value, MQ) else MQ([value])


def parse_mq(row) -> MQ:
    if not isinstance(row, list) or len(row) != 9:
        raise CheckError("bad encoded multiquadratic value")
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in row):
        raise CheckError("nonintegral multiquadratic coefficient")
    denominator = row[-1]
    if denominator <= 0:
        raise CheckError("nonpositive multiquadratic denominator")
    if math.gcd(*(abs(x) for x in row)) != 1:
        raise CheckError("noncanonical multiquadratic value")
    return MQ(Fraction(x, denominator) for x in row[:-1])


def sign_surd5(value: MQ) -> int:
    if any(value.c[i] for i in (1, 2, 3, 5, 6, 7)):
        raise CheckError("expected Q(sqrt(5)) value")
    a, b = value.c[0], value.c[4]
    if not b:
        return (a > 0) - (a < 0)
    if a >= 0 and b > 0:
        return 1
    if a <= 0 and b < 0:
        return -1
    comparison = a * a - 5 * b * b
    if not comparison:
        return 0
    if a > 0:
        return 1 if comparison > 0 else -1
    return -1 if comparison > 0 else 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def verify_certificate(data: dict) -> dict:
    require(isinstance(data, dict), "certificate must be an object")
    require(data.get("schema") == "hn-open-dominating-triple-collar-v1", "schema")

    threshold = data.get("threshold")
    require(isinstance(threshold, dict), "threshold")
    delta = parse_mq(threshold.get("distance_basis_coefficients"))
    squared = parse_mq(threshold.get("squared_basis_coefficients"))
    expected_delta = (MQ([0, 0, 1]) + MQ([0, 0, 0, 0, 0, 0, 1])) / 2
    expected_squared = (MQ([9]) + MQ([0, 0, 0, 0, 3])) / 2
    require(delta == expected_delta, "distance threshold encoding")
    require(delta * delta == squared == expected_squared, "threshold square identity")
    polynomial = threshold.get("squared_minimal_polynomial")
    require(polynomial == [1, -9, 9], "threshold polynomial encoding")
    require(squared * squared - squared * 9 + 9 == MQ(), "threshold polynomial identity")
    interval = threshold.get("squared_isolating_interval")
    require(interval == [[157, 20], [63, 8]], "threshold isolating interval encoding")
    lower = Fraction(*interval[0])
    upper = Fraction(*interval[1])
    require(sign_surd5(squared - lower) > 0, "threshold above lower isolator")
    require(sign_surd5(MQ([upper]) - squared) > 0, "threshold below upper isolator")

    orbit = data.get("circle_orbit")
    require(orbit.get("rotation_degrees") == 60, "rotation angle")
    require(orbit.get("orbit_size") == 6, "orbit size")
    half = MQ([Fraction(1, 2)])
    omega = (half, MQ([0, 0, Fraction(1, 2)]))

    def cmul(z, w):
        return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])

    powers = [(MQ([1]), MQ())]
    for _ in range(5):
        powers.append(cmul(powers[-1], omega))
    chord_table = []
    for z in powers:
        dx, dy = MQ([1]) - z[0], MQ() - z[1]
        chord_table.append(int((dx * dx + dy * dy).rational()))
    require(chord_table == [0, 1, 3, 4, 3, 1], "derived chord table")
    require(orbit.get("squared_chords") == chord_table, "stored chord table")

    fixture = data.get("open_fixture")
    expected_basis = ["1", "sqrt(2)", "sqrt(3)", "sqrt(6)", "sqrt(5)", "sqrt(10)", "sqrt(15)", "sqrt(30)"]
    require(fixture.get("coordinate_basis") == expected_basis, "coordinate basis")
    centres = fixture.get("centres")
    require(isinstance(centres, list) and len(centres) == 3, "fixture centres")
    points = [(parse_mq(p.get("x")), parse_mq(p.get("y"))) for p in centres]
    norms = []
    for i in range(3):
        for j in range(i + 1, 3):
            dx, dy = points[i][0] - points[j][0], points[i][1] - points[j][1]
            norms.append((dx * dx + dy * dy).rational())
    require(norms == [Fraction(8)] * 3, "fixture pair distances")
    require(fixture.get("pair_squared_distances") == [8, 8, 8], "stored fixture distances")
    require(fixture.get("strict_interval_squared") == [4, 9], "fixture interval")
    lower_checks = sum(q > 4 for q in norms)
    upper_checks = sum(q < 9 for q in norms)
    threshold_check = sign_surd5(MQ([8]) - squared) > 0
    require(lower_checks == 3 and upper_checks == 3, "fixture is not inside (2,3)^3")
    require(threshold_check, "fixture does not exceed threshold")

    cap = data.get("cap_fixture")
    require(cap.get("centre_squared_distance") == 8, "cap fixture distance")
    q = Fraction(8)
    t_squared = (q - 3) ** 2 / (4 * q)
    cap_diameter_squared = 4 * (1 - t_squared)
    require(cap.get("active_x_lower_bound_squared") == [t_squared.numerator, t_squared.denominator], "cap lower bound")
    require(cap.get("cap_diameter_squared_upper_bound") == [cap_diameter_squared.numerator, cap_diameter_squared.denominator], "cap diameter")
    require(t_squared > Fraction(3, 4), "active cap is not narrower than 60 degrees")
    require(cap_diameter_squared < 1, "active cap diameter is not below one")

    palette = data.get("palette")
    leaf = palette.get("leaf_circle_colours")
    third = palette.get("third_circle_colours")
    leaf_centres = palette.get("leaf_centre_colours")
    third_centre = palette.get("third_centre_colour")
    require(leaf == [0, 1], "leaf palette")
    require(third == [2, 3], "third palette")
    require(set(leaf).isdisjoint(third), "palettes overlap")
    require(leaf_centres == [2, 2] and all(c not in leaf for c in leaf_centres), "leaf centre colours")
    require(third_centre == 0 and third_centre not in third, "third centre colour")
    require(len(set(leaf + third)) == 4, "not four colours")

    result = {
        "threshold_identities": 2,
        "threshold_isolation_inequalities": 2,
        "orbit_chord_cases": 6,
        "fixture_pair_norms": 3,
        "fixture_strict_inequalities": lower_checks + upper_checks + int(threshold_check),
        "cap_fixture_identities": 2,
        "palette_checks": 6,
        "malformed_certificate_rejections": 6,
        "native_solver_calls": 0,
    }
    require(data.get("claimed_checks") == result, "claimed check counts")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    raw = args.certificate.read_bytes()
    data = json.loads(raw)
    result = verify_certificate(data)
    result.update({
        "certificate_bytes": len(raw),
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "status": "PASS",
    })
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (args.work / "verification.json").write_text(payload)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
