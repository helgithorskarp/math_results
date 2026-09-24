#!/usr/bin/env python3
"""Independent exact verifier for the q=5 isolated double-pole classification."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F
from hashlib import sha256
from json import dumps
from math import comb, factorial


Poly = tuple[F, ...]  # ascending coefficients


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def poly(entries) -> Poly:
    answer = tuple(F(entry) for entry in entries)
    while len(answer) > 1 and answer[-1] == 0:
        answer = answer[:-1]
    return answer or (F(0),)


def padd(left: Poly, right: Poly) -> Poly:
    size = max(len(left), len(right))
    return poly(
        (left[index] if index < len(left) else 0)
        + (right[index] if index < len(right) else 0)
        for index in range(size)
    )


def pneg(value: Poly) -> Poly:
    return poly(-entry for entry in value)


def psub(left: Poly, right: Poly) -> Poly:
    return padd(left, pneg(right))


def pmul(left: Poly, right: Poly) -> Poly:
    answer = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] += x * y
    return poly(answer)


def ppow(value: Poly, exponent: int) -> Poly:
    require(exponent >= 0, "negative polynomial exponent")
    answer = poly([1])
    base = value
    while exponent:
        if exponent & 1:
            answer = pmul(answer, base)
        base = pmul(base, base)
        exponent //= 2
    return answer


def pderivative(value: Poly) -> Poly:
    return poly(index * value[index] for index in range(1, len(value)))


def peval(value: Poly, point: F) -> F:
    answer = F(0)
    for coefficient in reversed(value):
        answer = answer * point + coefficient
    return answer


def pdivmod(dividend: Poly, divisor: Poly) -> tuple[Poly, Poly]:
    require(divisor != (F(0),), "polynomial division by zero")
    remainder = list(dividend)
    quotient = [F(0)] * max(1, len(dividend) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and any(remainder):
        shift = len(remainder) - len(divisor)
        factor = remainder[-1] / divisor[-1]
        quotient[shift] += factor
        for index, coefficient in enumerate(divisor):
            remainder[index + shift] -= factor * coefficient
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()
    return poly(quotient), poly(remainder)


def pmonic(value: Poly) -> Poly:
    require(value != (F(0),), "zero polynomial has no monic associate")
    return poly(entry / value[-1] for entry in value)


def pgcd(left: Poly, right: Poly) -> Poly:
    while right != (F(0),):
        _, remainder = pdivmod(left, right)
        left, right = right, remainder
    return pmonic(left)


def sturm_sequence(value: Poly) -> list[Poly]:
    sequence = [value, pderivative(value)]
    while sequence[-1] != (F(0),):
        _, remainder = pdivmod(sequence[-2], sequence[-1])
        if remainder == (F(0),):
            break
        sequence.append(pneg(remainder))
    return sequence


def sign(value: F) -> int:
    return (value > 0) - (value < 0)


def variations(sequence: list[Poly], point: F) -> int:
    signs = [sign(peval(entry, point)) for entry in sequence]
    signs = [entry for entry in signs if entry]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def root_count(value: Poly, left: F, right: F) -> int:
    sequence = sturm_sequence(value)
    return variations(sequence, left) - variations(sequence, right)


def strip_endpoint_roots(value: Poly) -> Poly:
    answer = value
    for factor in (poly([0, 1]), poly([-1, 1])):
        while len(answer) > 1:
            quotient, remainder = pdivmod(answer, factor)
            if remainder != (F(0),):
                break
            answer = quotient
    return answer


@dataclass(frozen=True)
class Rat:
    numerator: Poly
    denominator: Poly

    def __post_init__(self) -> None:
        require(self.denominator != (F(0),), "zero rational-function denominator")

    @staticmethod
    def constant(value) -> "Rat":
        return Rat(poly([value]), poly([1]))

    @staticmethod
    def variable() -> "Rat":
        return Rat(poly([0, 1]), poly([1]))

    @staticmethod
    def coerce(value) -> "Rat":
        return value if isinstance(value, Rat) else Rat.constant(value)

    def __add__(self, other) -> "Rat":
        other = Rat.coerce(other)
        return Rat(
            padd(
                pmul(self.numerator, other.denominator),
                pmul(other.numerator, self.denominator),
            ),
            pmul(self.denominator, other.denominator),
        )

    __radd__ = __add__

    def __neg__(self) -> "Rat":
        return Rat(pneg(self.numerator), self.denominator)

    def __sub__(self, other) -> "Rat":
        return self + (-Rat.coerce(other))

    def __rsub__(self, other) -> "Rat":
        return Rat.coerce(other) - self

    def __mul__(self, other) -> "Rat":
        other = Rat.coerce(other)
        return Rat(
            pmul(self.numerator, other.numerator),
            pmul(self.denominator, other.denominator),
        )

    __rmul__ = __mul__

    def __truediv__(self, other) -> "Rat":
        other = Rat.coerce(other)
        require(other.numerator != (F(0),), "rational-function division by zero")
        return Rat(
            pmul(self.numerator, other.denominator),
            pmul(self.denominator, other.numerator),
        )

    def __rtruediv__(self, other) -> "Rat":
        return Rat.coerce(other) / self

    def __pow__(self, exponent: int) -> "Rat":
        require(exponent >= 0, "negative rational-function exponent")
        return Rat(ppow(self.numerator, exponent), ppow(self.denominator, exponent))

    def is_zero(self) -> bool:
        return self.numerator == (F(0),)

    def evaluate(self, point: F) -> F:
        denominator = peval(self.denominator, point)
        require(denominator != 0, "evaluation at a pole")
        return peval(self.numerator, point) / denominator


def reduce_rat(value: Rat) -> Rat:
    common = pgcd(value.numerator, value.denominator)
    numerator, numerator_remainder = pdivmod(value.numerator, common)
    denominator, denominator_remainder = pdivmod(value.denominator, common)
    require(
        numerator_remainder == (F(0),) and denominator_remainder == (F(0),),
        "rational reduction failed",
    )
    if denominator[-1] < 0:
        numerator, denominator = pneg(numerator), pneg(denominator)
    return Rat(numerator, denominator)


def rat_product(values) -> Rat:
    answer = Rat.constant(1)
    for value in values:
        answer *= value
    return answer


def remove_n(values: list[Rat], target: Rat, number: int) -> list[Rat]:
    answer = list(values)
    for _ in range(number):
        answer.remove(target)
    return answer


def row_coefficients(
    supplier: Rat, remaining: list[Rat], tails: list[Rat], boundary: Rat
) -> dict[int, Rat]:
    """Reconstruct the two jets of one labeled double-pole tail row."""
    size = len(remaining)
    require(remaining.count(supplier) == 2, "supplier is not a double pole")
    other = remove_n(remaining, supplier, 2)
    t0 = -(1 - supplier) / supplier
    regularized_denominator = (
        (1 - t0) ** size
        * rat_product(remaining)
        * supplier**2
        * rat_product(1 - weight + weight * t0 for weight in other)
    )
    highest = 1 / regularized_denominator
    logarithmic_derivative = size / (1 - t0) - sum(
        (weight / (1 - weight + weight * t0) for weight in other),
        Rat.constant(0),
    )
    next_highest = highest * logarithmic_derivative

    # coefficient, B power, B shift, final hinge degree so far
    states = [
        (highest / factorial(size - 2), 1, Rat.constant(0), size - 2),
        (next_highest / factorial(size - 1), 0, Rat.constant(0), size - 1),
    ]
    lam = (1 - supplier) / supplier
    for weight in tails:
        updated = []
        for coefficient, b_power, shift, slack_power in states:
            for moment in range(b_power + 1):
                eta = weight**moment / (1 + weight + lam * weight) ** (
                    moment + 1
                ) - 1 / (weight * (1 + lam) ** (moment + 1))
                beta_factor = F(
                    comb(b_power, moment)
                    * factorial(moment)
                    * factorial(slack_power),
                    factorial(moment + slack_power + 1),
                )
                updated.append(
                    (
                        coefficient * eta * beta_factor,
                        b_power - moment,
                        shift + 2 * weight,
                        slack_power + moment + 1,
                    )
                )
        states = updated
    answer: dict[int, Rat] = {}
    for coefficient, b_power, shift, slack_power in states:
        value = coefficient * (boundary + shift) ** b_power
        answer[slack_power] = answer.get(slack_power, Rat.constant(0)) + value
    return answer


def two_jet_ratio(
    supplier: Rat,
    remaining: list[Rat],
    tails: list[Rat],
    boundary: Rat,
    wall: Rat,
) -> Rat:
    """Formula c4/c3 for q=5 and residual multiplicity two."""
    other = [weight for weight in remaining if weight != supplier]
    bracket = Rat.constant(len(remaining)) - sum(
        (weight / (supplier - weight) for weight in other), Rat.constant(0)
    ) + sum(
        ((supplier + 2 * weight) / (supplier + weight) for weight in tails),
        Rat.constant(0),
    )
    return bracket / (4 * (boundary + wall))


def pattern_data(pattern, beta: Rat):
    ell, h, i, g = pattern
    a = Rat.variable()
    one = Rat.constant(1)
    unit_tails = [a] * ell + [beta] * h
    unit_remaining = remove_n([one, one, a, a, beta], a, ell)
    unit_remaining = remove_n(unit_remaining, beta, h)
    moving_tails = [one] * i + [beta] * g
    moving_remaining = remove_n([one, one, a, a, beta], one, i)
    moving_remaining = remove_n(moving_remaining, beta, g)
    boundary = 2 * (a * (ell * a + h * beta) - (i + g * beta)) / (1 - a)
    wall = 2 * (ell * a + h * beta)
    return (
        unit_remaining,
        unit_tails,
        moving_remaining,
        moving_tails,
        boundary,
        wall,
    )


def sign_at_root(expression: Rat, defining: Poly, left: F, right: F) -> int:
    require(root_count(defining, left, right) == 1, "defining root not isolated")
    midpoint = (left + right) / 2
    for value, name in (
        (expression.numerator, "numerator"),
        (expression.denominator, "denominator"),
    ):
        require(root_count(value, left, right) == 0, f"{name} changes sign")
        require(peval(value, midpoint) != 0, f"{name} vanishes at midpoint")
    return sign(peval(expression.numerator, midpoint)) * sign(
        peval(expression.denominator, midpoint)
    )


def isolate_root(defining: Poly, left: F, right: F, steps: int = 110) -> F:
    left_sign, right_sign = sign(peval(defining, left)), sign(peval(defining, right))
    require(left_sign * right_sign < 0, "interval does not bracket a root")
    for _ in range(steps):
        midpoint = (left + right) / 2
        midpoint_sign = sign(peval(defining, midpoint))
        if midpoint_sign == 0:
            return midpoint
        if midpoint_sign == left_sign:
            left = midpoint
        else:
            right = midpoint
    return (left + right) / 2


def decimal_string(value: F) -> str:
    getcontext().prec = 35
    return format(Decimal(value.numerator) / Decimal(value.denominator), ".15f")


def main() -> None:
    a = Rat.variable()
    one = Rat.constant(1)

    p1 = poly([1, -3, 4, -4, 5, -7, 5, -4, 4, -3, 1])
    p2 = poly([4, -8, 4, 0, 0, 0, -6, -2, 2, 6, 0, 0, 0, 1, 2, 1])
    p3 = poly([-1, 4, -5, 0, 4, 0, -1, 1, -1, 1, 0, -4, 0, 5, 4, 1])
    p4 = poly([-1, 2, -1, 0, 0, 0, 6, -2, -2, 6, 0, 0, 0, 4, 8, 4])
    p5 = poly([1, 1, 1, 1, 1, 1, -2, 1, 1, 1, 1, 1, 1])
    polynomials = {"P1": p1, "P2": p2, "P3": p3, "P4": p4, "P5": p5}
    root_counts = {name: root_count(value, F(0), F(1)) for name, value in polynomials.items()}
    require(root_counts == {"P1": 1, "P2": 2, "P3": 1, "P4": 1, "P5": 0}, "unit root census")

    d1 = a**6 - a**5 + a**4 - a**3 + a**2 - a + 1
    n1 = -a * (a - 1) * (a**2 - a + 1) * (a**2 + a + 1)
    d2 = a**8 + a**7 + 2 * a - 2
    n2 = a * (a**7 + a**6 + 2 * a - 2)
    d3 = a**9 + 2 * a**8 + a**7 + a**2 - 2 * a + 1
    n3 = a * (a**2 + 1) * (a**2 + a - 1) * (a**4 + a**3 - a + 1)
    d4 = 2 * a**8 + 2 * a**7 - a + 1
    n4 = a * (2 * a**7 + 2 * a**6 + a - 1)
    phi1, phi2, phi3, phi4 = n1 / d1, n2 / d2, -n3 / d3, n4 / d4

    for denominator, numerator, name in (
        (d1, n1, "D1"),
        (d2, n2, "D2"),
        (d3, n3, "D3"),
        (d4, n4, "D4"),
    ):
        require(
            pgcd(denominator.numerator, numerator.numerator) == poly([1]),
            f"simultaneous zero in {name}",
        )

    shortlist = [
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (1, 1, 0, 1),
        (2, 0, 0, 1),
        (2, 0, 1, 1),
        (2, 1, 0, 0),
        (2, 1, 1, 0),
        (2, 1, 2, 0),
    ]
    branch_map = {
        (0, 1, 0, 0): phi1,
        (1, 0, 0, 0): phi2,
        (1, 1, 0, 1): -phi2,
        (2, 0, 0, 1): n3 / d3,
        (2, 0, 1, 1): phi4,
        (2, 1, 0, 0): phi3,
        (2, 1, 1, 0): -phi4,
        (2, 1, 2, 0): phi1,
    }
    eliminants = {
        (0, 1, 0, 0): p1,
        (1, 0, 0, 0): p2,
        (1, 1, 0, 1): p2,
        (2, 0, 0, 1): p3,
        (2, 0, 1, 1): p4,
        (2, 1, 0, 0): p3,
        (2, 1, 1, 0): p4,
        (2, 1, 2, 0): p5,
    }

    # Reconstruct both jets independently for every nondegenerate branch.
    for pattern in shortlist:
        beta = branch_map[pattern]
        (
            unit_remaining,
            unit_tails,
            moving_remaining,
            moving_tails,
            boundary,
            wall,
        ) = pattern_data(pattern, beta)
        unit = row_coefficients(one, unit_remaining, unit_tails, boundary)
        moving = row_coefficients(a, moving_remaining, moving_tails, boundary)
        unit_factor = comb(2, pattern[0])
        moving_factor = comb(2, pattern[2])
        c3_sum = unit_factor * unit[3] + moving_factor * moving[3]
        require(c3_sum.is_zero(), f"leading branch failure at {pattern}")

        ratio_difference = reduce_rat(two_jet_ratio(
            one, unit_remaining, unit_tails, boundary, wall
        ) - two_jet_ratio(a, moving_remaining, moving_tails, boundary, wall)
        )
        defining = eliminants[pattern]
        quotient, remainder = pdivmod(ratio_difference.numerator, defining)
        require(remainder == (F(0),), f"eliminant failure at {pattern}")
        require(
            root_count(strip_endpoint_roots(quotient), F(0), F(1)) == 0,
            f"extra ratio root at {pattern}",
        )
        require(
            pgcd(defining, ratio_difference.denominator) == poly([1]),
            f"ratio pole on eliminant at {pattern}",
        )
        c4_sum = unit_factor * unit[4] + moving_factor * moving[4]
        _, c4_remainder = pdivmod(c4_sum.numerator, defining)
        require(c4_remainder == (F(0),), f"next-jet failure at {pattern}")

    # The five additional roots of the factorized leading equations are inadmissible.
    def boundary_for(pattern, beta):
        ell, h, i, g = pattern
        return 2 * (a * (ell * a + h * beta) - (i + g * beta)) / (1 - a)

    require((2 * a - a - a).is_zero(), "b=2a exclusion")
    require(
        (boundary_for((2, 0, 1, 1), 2 * a - 1) + 4 * a).is_zero(),
        "b=2a-1 boundary",
    )
    require((-2 * a + 2 * a).is_zero(), "b=-2a exclusion")
    require(
        (boundary_for((2, 1, 1, 0), 1 - 2 * a) + 2).is_zero(),
        "b=1-2a boundary",
    )
    require(
        (boundary_for((2, 1, 2, 0), 2 - 2 * a) + 4).is_zero(),
        "b=2-2a boundary",
    )

    boxes = {
        "I": (p1, F(127, 200), F(637, 1000), phi1, (0, 1, 0, 0)),
        "II": (p2, F(27, 40), F(677, 1000), phi2, (1, 0, 0, 0)),
        "II-bad": (p2, F(9, 10), F(901, 1000), phi2, (1, 0, 0, 0)),
        "III": (p3, F(64, 125), F(513, 1000), phi3, (2, 1, 0, 0)),
        "P4": (p4, F(71, 125), F(569, 1000), phi4, (2, 0, 1, 1)),
    }
    expected_signs = {
        "I": (1, 1, 1),
        "II": (1, 1, 1),
        "II-bad": (1, -1, 1),
        "III": (1, 1, 1),
        "P4": (-1, 1, 1),
    }
    for name, (defining, left, right, beta, pattern) in boxes.items():
        require(root_count(defining, left, right) == 1, f"root box {name}")
        observed = (
            sign_at_root(beta, defining, left, right),
            sign_at_root(a - beta, defining, left, right),
            sign_at_root(boundary_for(pattern, beta), defining, left, right),
        )
        require(observed == expected_signs[name], f"admissibility {name}: {observed}")

    require(
        sign_at_root(-phi2, p2, F(27, 40), F(677, 1000)) < 0
        and sign_at_root(-phi2, p2, F(9, 10), F(901, 1000)) < 0,
        "reflected P2",
    )
    require(
        sign_at_root(n3 / d3, p3, F(64, 125), F(513, 1000)) < 0,
        "reflected P3",
    )
    require(
        sign_at_root(-phi4, p4, F(71, 125), F(569, 1000)) > 0
        and sign_at_root(
            boundary_for((2, 1, 1, 0), -phi4),
            p4,
            F(71, 125),
            F(569, 1000),
        )
        < 0,
        "reflected P4",
    )

    physical_boxes = {
        "I": boxes["I"],
        "II": boxes["II"],
        "III": boxes["III"],
    }
    physical = []
    for name, (defining, left, right, beta, pattern) in physical_boxes.items():
        boundary = boundary_for(pattern, beta)
        wall = 2 * (pattern[0] * a + pattern[1] * beta)
        walls: list[tuple[str, Rat]] = []
        for k in range(2):
            for ell in range(3):
                for h in range(2):
                    walls.append((f"U({k},{ell},{h})", 2 * (k + ell * a + h * beta)))
        for i in range(3):
            for j in range(2):
                for g in range(2):
                    walls.append(
                        (
                            f"A({i},{j},{g})",
                            (1 - a) * boundary / a
                            + 2 * (i + j * a + g * beta) / a,
                        )
                    )
        for i in range(3):
            for ell in range(3):
                walls.append(
                    (
                        f"b({i},{ell})",
                        (1 - beta) * boundary / beta
                        + 2 * (i + ell * a) / beta,
                    )
                )
        require(len(walls) == 33, "wall enumeration")
        identical = []
        coprime = 0
        for label, candidate in walls:
            difference = reduce_rat(candidate - wall)
            if difference.is_zero():
                identical.append(label)
                continue
            require(
                pgcd(defining, difference.numerator) == poly([1]),
                f"extra collision {name} {label}",
            )
            require(
                pgcd(defining, difference.denominator) == poly([1]),
                f"wall denominator {name} {label}",
            )
            coprime += 1
        require(len(identical) == 2 and coprime == 31, f"isolation {name}")

        root = isolate_root(defining, left, right)
        beta_value = beta.evaluate(root)
        boundary_value = boundary.evaluate(root)
        physical.append(
            {
                "family": name,
                "pattern": list(pattern),
                "root_interval": [str(left), str(right)],
                "alpha_approx": decimal_string(root),
                "beta_approx": decimal_string(beta_value),
                "B_approx": decimal_string(boundary_value),
                "rows_at_wall": len(identical),
                "other_rows_coprime": coprime,
            }
        )

    payload = {
        "status": "Q5_THREE_LEVEL_DOUBLE_POLE_CLASSIFICATION_VERIFIED",
        "pair_patterns": 36,
        "sign_and_boundary_feasible_patterns": len(shortlist),
        "leading_branches": 13,
        "root_counts_in_unit_interval": root_counts,
        "physical_family_count": len(physical),
        "physical_families": physical,
        "structural_rows": 33,
    }
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_sha256"] = sha256(canonical.encode()).hexdigest()
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
