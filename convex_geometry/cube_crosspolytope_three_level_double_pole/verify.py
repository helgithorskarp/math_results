#!/usr/bin/env python3
"""Standard-library exact verifier for the three-level missing wall."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F
from hashlib import sha256
from json import dumps


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


def isolate_root(defining: Poly, left: F, right: F, steps: int = 100) -> F:
    left_sign, right_sign = sign(peval(defining, left)), sign(peval(defining, right))
    require(left_sign * right_sign < 0, "interval does not bracket a root")
    for _ in range(steps):
        middle = (left + right) / 2
        middle_sign = sign(peval(defining, middle))
        if middle_sign == 0:
            return middle
        if middle_sign == left_sign:
            left = middle
        else:
            right = middle
    return (left + right) / 2


def decimal_string(value: F) -> str:
    getcontext().prec = 30
    return format(Decimal(value.numerator) / Decimal(value.denominator), ".15f")


def main() -> None:
    defining = poly([1, -3, 4, -4, 5, -7, 5, -4, 4, -3, 1])
    left, right = F(127, 200), F(637, 1000)
    sequence = sturm_sequence(defining)
    root_count = variations(sequence, left) - variations(sequence, right)
    require(peval(defining, left) > 0, "wrong left-endpoint sign")
    require(peval(defining, right) < 0, "wrong right-endpoint sign")
    require(root_count == 1, "defining root is not unique in its interval")

    a = Rat.variable()
    beta = a * (1 - a**6) / (1 + a**7)
    boundary = 2 * a * beta / (1 - a)
    target = 2 * beta

    # The first identity is precisely cancellation of the degree-three terms.
    require((a - beta - a**7 * (1 + beta)).is_zero(), "leading identity failed")
    unit3 = 1 / (3 * a**2 * (a - 1) ** 3 * (beta + 1))
    moving3 = -(a**5) / (3 * (a - 1) ** 3 * (a - beta))
    require((unit3 + moving3).is_zero(), "degree-three coefficients do not cancel")

    # Equality of normalized degree-four coefficients reduces exactly to P(a)=0.
    ratio_numerator = 3 * a * beta + 2 * a - 2 * beta**2 - 3 * beta
    _, ratio_remainder = pdivmod(ratio_numerator.numerator, defining)
    require(ratio_remainder == (F(0),), "two-jet condition is not divisible by P")

    rows: list[tuple[str, Rat]] = []
    for k in range(2):
        for ell in range(3):
            for h in range(2):
                rows.append((f"U({k},{ell},{h})", 2 * (k + a * ell + beta * h)))
    for i in range(3):
        for j in range(2):
            for g in range(2):
                rows.append(
                    (
                        f"A({i},{j},{g})",
                        (1 - a) * boundary / a + 2 * (i + a * j + beta * g) / a,
                    )
                )
    for i in range(3):
        for ell in range(3):
            rows.append(
                (
                    f"B({i},{ell})",
                    (1 - beta) * boundary / beta + 2 * (i + a * ell) / beta,
                )
            )
    require(len(rows) == 33, "structural-row enumeration failed")

    identical = []
    coprime = 0
    for label, wall in rows:
        difference = wall - target
        if difference.is_zero():
            identical.append(label)
            continue
        require(
            len(pgcd(difference.numerator, defining)) == 1,
            f"extra row can collide at the algebraic root: {label}",
        )
        coprime += 1
    require(
        identical == ["U(0,0,1)", "A(0,0,0)"],
        "wrong pair of rows at target wall",
    )
    require(coprime == 31, "not all other rows were excluded")

    approximate_root = isolate_root(defining, left, right)
    approximate_beta = beta.evaluate(approximate_root)
    approximate_boundary = boundary.evaluate(approximate_root)
    require(0 < approximate_beta < approximate_root < 1, "bad weight ordering")
    require(approximate_boundary > 0, "boundary is not positive")

    payload = {
        "status": "THREE_LEVEL_DOUBLE_POLE_MISSING_WALL_VERIFIED",
        "root_interval": ["127/200", "637/1000"],
        "sturm_sequence_length": len(sequence),
        "roots_in_interval": root_count,
        "approximate_parameters": {
            "alpha": decimal_string(approximate_root),
            "beta": decimal_string(approximate_beta),
            "boundary": decimal_string(approximate_boundary),
        },
        "structural_rows": len(rows),
        "target_rows": identical,
        "other_rows_coprime_to_polynomial": coprime,
        "cancelled_degrees": [3, 4],
        "minimal_active_dimension": 2 + 2 + 1,
    }
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_sha256"] = sha256(canonical.encode()).hexdigest()
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
