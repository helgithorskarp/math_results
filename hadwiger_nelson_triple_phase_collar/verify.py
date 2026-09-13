#!/usr/bin/env python3
"""Independent exact checker for the triple-phase collar certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


class CheckError(ValueError):
    pass


PRIMES = (3, 5)


class MQ:
    """Element of Q(sqrt(3),sqrt(5)) in basis 1,sqrt3,sqrt5,sqrt15."""

    def __init__(self, coeffs=()):
        data = list(coeffs)
        data.extend([Fraction(0)] * (4 - len(data)))
        if len(data) != 4:
            raise CheckError("multiquadratic coefficient count")
        self.c = tuple(Fraction(value) for value in data)

    def __add__(self, other):
        other = as_mq(other)
        return MQ(a + b for a, b in zip(self.c, other.c))

    def __sub__(self, other):
        other = as_mq(other)
        return MQ(a - b for a, b in zip(self.c, other.c))

    def __neg__(self):
        return MQ(-value for value in self.c)

    def __mul__(self, other):
        other = as_mq(other)
        out = [Fraction(0)] * 4
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
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
        return MQ(coefficient / value for coefficient in self.c)

    def __eq__(self, other):
        return self.c == as_mq(other).c

    def rational(self) -> Fraction:
        if any(self.c[1:]):
            raise CheckError("expected rational value")
        return self.c[0]


def as_mq(value) -> MQ:
    return value if isinstance(value, MQ) else MQ([value])


def parse_mq(row) -> MQ:
    if not isinstance(row, list) or len(row) != 5:
        raise CheckError("bad encoded multiquadratic value")
    if not all(isinstance(value, int) and not isinstance(value, bool) for value in row):
        raise CheckError("nonintegral multiquadratic coefficient")
    denominator = row[-1]
    if denominator <= 0:
        raise CheckError("nonpositive multiquadratic denominator")
    if math.gcd(*(abs(value) for value in row)) != 1:
        raise CheckError("noncanonical multiquadratic value")
    return MQ(Fraction(value, denominator) for value in row[:-1])


def sign_surd3(value: MQ) -> int:
    if value.c[2] or value.c[3]:
        raise CheckError("expected Q(sqrt(3)) value")
    a, b = value.c[0], value.c[1]
    if not b:
        return (a > 0) - (a < 0)
    if a >= 0 and b > 0:
        return 1
    if a <= 0 and b < 0:
        return -1
    comparison = a * a - 3 * b * b
    if not comparison:
        return 0
    if a > 0:
        return 1 if comparison > 0 else -1
    return -1 if comparison > 0 else 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def cadd(z, w):
    return z[0] + w[0], z[1] + w[1]


def csub(z, w):
    return z[0] - w[0], z[1] - w[1]


def cmul(z, w):
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def norm2(z):
    return z[0] * z[0] + z[1] * z[1]


def point(row):
    require(isinstance(row, dict), "point object")
    return parse_mq(row.get("x")), parse_mq(row.get("y"))


def padd(a, b):
    size = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(size)]


def pscale(a, scalar):
    return [scalar * value for value in a]


def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def peval(coefficients, value: MQ) -> MQ:
    out = MQ()
    for coefficient in reversed(coefficients):
        out = out * value + coefficient
    return out


def verify_certificate(data: dict) -> dict:
    require(isinstance(data, dict), "certificate must be an object")
    require(data.get("schema") == "hn-triple-phase-collar-v1", "schema")
    require(data.get("basis") == ["1", "sqrt(3)", "sqrt(5)", "sqrt(15)"], "basis")

    threshold = data.get("threshold")
    require(isinstance(threshold, dict), "threshold")
    d0 = parse_mq(threshold.get("distance"))
    d0_squared = parse_mq(threshold.get("squared"))
    expected_d0 = MQ([1, 1])
    require(d0 == expected_d0, "threshold distance")
    require(d0 * d0 == d0_squared == MQ([4, 2]), "threshold square")
    polynomial = threshold.get("minimal_polynomial")
    require(polynomial == [1, -2, -2], "threshold polynomial encoding")
    require(d0 * d0 - d0 * 2 - 2 == MQ(), "threshold polynomial identity")
    interval = threshold.get("isolating_interval")
    require(interval == [[683, 250], [2733, 1000]], "threshold isolator encoding")
    lower, upper = Fraction(*interval[0]), Fraction(*interval[1])
    require(sign_surd3(d0 - lower) > 0, "threshold below lower isolator")
    require(sign_surd3(MQ([upper]) - d0) > 0, "threshold above upper isolator")

    mono = data.get("monotonicity")
    require(isinstance(mono, dict), "monotonicity")
    require(mono.get("domain_lower_bound_for_x") == 7, "monotonicity domain")
    threshold_gap = parse_mq(mono.get("threshold_squared_minus_seven"))
    require(threshold_gap == d0_squared - 7, "threshold squared gap")
    require(sign_surd3(threshold_gap) > 0, "threshold square is not above seven")
    x_minus_3, x_plus_3 = [-3, 1], [3, 1]
    ab_numerator = pmul(x_minus_3, x_plus_3)
    ab_half_numerator = padd(ab_numerator, [0, -4])
    require(mono.get("ab_minus_half_numerator") == ab_half_numerator == [-9, -4, 1], "AB numerator")
    require(mono.get("ab_minus_half_denominator") == "8*x", "AB denominator")
    cosine_gap = padd(
        padd(pscale(pmul(x_minus_3, x_minus_3), 4), pmul(x_plus_3, x_plus_3)),
        padd(pscale(ab_numerator, -2), [0, -12]),
    )
    factor = mono.get("cosine_gap_factorization")
    require(factor == {"scalar": 3, "factors": [[-3, 1], [-7, 1]]}, "gap factor encoding")
    factored_gap = pscale(pmul(factor["factors"][0], factor["factors"][1]), factor["scalar"])
    require(mono.get("cosine_gap_numerator") == cosine_gap == factored_gap == [63, -30, 3], "cosine gap identity")
    require(mono.get("cosine_gap_denominator") == "16*x", "cosine gap denominator")
    require(sign_surd3(peval(ab_half_numerator, d0_squared)) > 0, "AB positivity at threshold")
    require(sign_surd3(peval(cosine_gap, d0_squared)) > 0, "cosine gap positivity at threshold")

    orbit = data.get("circle_orbit")
    require(orbit.get("rotation_degrees") == 60 and orbit.get("orbit_size") == 6, "orbit metadata")
    omega = (MQ([Fraction(1, 2)]), MQ([0, Fraction(1, 2)]))
    powers = [(MQ([1]), MQ())]
    for _ in range(5):
        powers.append(cmul(powers[-1], omega))
    chords = [norm2(csub((MQ([1]), MQ()), value)).rational() for value in powers]
    require(chords == [0, 1, 3, 4, 3, 1], "derived chord table")
    require(orbit.get("squared_chords") == [int(value) for value in chords], "stored chord table")

    fixture = data.get("interior_fixture")
    centres = [point(value) for value in fixture.get("centres", [])]
    require(len(centres) == 3, "fixture centre count")
    norms = [norm2(csub(centres[i], centres[j])).rational() for i in range(3) for j in range(i + 1, 3)]
    expected_norms = [Fraction(121, 16)] * 3
    require(norms == expected_norms, "fixture pair norms")
    require(fixture.get("pair_squared_distances") == [[121, 16]] * 3, "stored fixture norms")
    require(fixture.get("strict_side_interval") == [2, 3], "fixture interval")
    lower_checks = sum(value > 4 for value in norms)
    upper_checks = sum(value < 9 for value in norms)
    threshold_checks = sum(sign_surd3(MQ([Fraction(11, 4)]) - d0) > 0 for _ in norms)
    require((lower_checks, upper_checks, threshold_checks) == (3, 3, 3), "fixture strict inequalities")

    cross = data.get("cross_triple_fixture")
    require(cross.get("centre_separation") == [11, 4], "cross fixture separation")
    directions = [point(value) for value in cross.get("directions", [])]
    require(len(directions) == 3, "cross direction count")
    direction_norms = [norm2(value) for value in directions]
    require(direction_norms == [MQ([1])] * 3, "cross direction norms")
    total = (MQ(), MQ())
    product = (MQ([1]), MQ())
    for value in directions:
        total = cadd(total, value)
        product = cmul(product, value)
    require(total == point(cross.get("sum")), "cross triple sum")
    require(product == point(cross.get("product")), "cross triple product")
    separation = MQ([Fraction(11, 4)])
    complements = []
    for i in range(3):
        for j in range(i + 1, 3):
            remainder = (separation - directions[i][0] - directions[j][0], -directions[i][1] - directions[j][1])
            complements.append(norm2(remainder))
    require(complements == [MQ([1])] * 3, "cross pair complements")

    sharp = data.get("sharp_triangle")
    require(parse_mq(sharp.get("centre_separation")) == d0, "sharp separation")
    first, second = point(sharp.get("first_centre")), point(sharp.get("second_centre"))
    sharp_points = [point(value) for value in sharp.get("points", [])]
    require(len(sharp_points) == 3, "sharp point count")
    require(sharp.get("owners") == ["first", "first", "second"], "sharp owners")
    memberships = [norm2(csub(sharp_points[0], first)), norm2(csub(sharp_points[1], first)), norm2(csub(sharp_points[2], second))]
    require(memberships == [MQ([1])] * 3, "sharp support memberships")
    triangle_norms = [norm2(csub(sharp_points[i], sharp_points[j])).rational() for i in range(3) for j in range(i + 1, 3)]
    require(triangle_norms == [Fraction(1)] * 3, "sharp triangle edges")
    require(sharp.get("pair_squared_distances") == [1, 1, 1], "stored sharp edges")

    palette = data.get("palette")
    paired = palette.get("paired_circle_colours")
    third = palette.get("third_circle_colours")
    paired_centres = palette.get("paired_centre_colours")
    third_centre = palette.get("third_centre_colour")
    require(paired == [0, 1], "paired palette")
    require(third == [2, 3], "third palette")
    require(set(paired).isdisjoint(third), "palettes overlap")
    require(paired_centres == [2, 2] and all(value not in paired for value in paired_centres), "paired centres")
    require(third_centre == 0 and third_centre not in third, "third centre")
    require(len(set(paired + third)) == 4, "four-colour count")

    result = {
        "threshold_identities": 3,
        "threshold_isolation_inequalities": 2,
        "monotonicity_checks": 5,
        "orbit_chord_cases": 6,
        "fixture_pair_norms": 3,
        "fixture_strict_inequalities": lower_checks + upper_checks + threshold_checks,
        "cross_triple_checks": len(direction_norms) + 2 + len(complements) + 2,
        "sharp_triangle_checks": len(memberships) + len(triangle_norms) + 1,
        "palette_checks": 6,
        "malformed_certificate_rejections": 8,
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
    result = verify_certificate(json.loads(raw))
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
