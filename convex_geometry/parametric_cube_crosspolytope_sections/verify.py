"""Exact checker for the parametric diagonal-section first correction.

Only the Python standard library is used. Rational functions are represented
canonically in Q[r]. The asymptotic remainder is proved in PROOF.md; this
script verifies the finite algebra and exact-section corroboration.
"""

from decimal import Decimal, getcontext
from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from json import dumps
from math import comb, factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(poly):
    answer = list(poly)
    while len(answer) > 1 and answer[-1] == 0:
        answer.pop()
    return tuple(F(x) for x in answer)


def poly_add(left, right):
    size = max(len(left), len(right))
    return trim([
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(size)
    ])


def poly_neg(poly):
    return tuple(-x for x in poly)


def poly_subtract(left, right):
    return poly_add(left, poly_neg(right))


def poly_scale(poly, coefficient):
    return trim([F(coefficient) * x for x in poly])


def poly_multiply(left, right):
    answer = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] += x * y
    return trim(answer)


def poly_power(poly, exponent):
    require(type(exponent) is int and exponent >= 0, "polynomial exponent")
    answer = (F(1),)
    base = trim(poly)
    while exponent:
        if exponent & 1:
            answer = poly_multiply(answer, base)
        base = poly_multiply(base, base)
        exponent //= 2
    return answer


def poly_divmod(numerator, denominator):
    numerator = list(trim(numerator))
    denominator = trim(denominator)
    require(denominator != (0,), "zero polynomial divisor")
    if len(numerator) < len(denominator):
        return (F(0),), tuple(numerator)
    quotient = [F(0)] * (len(numerator) - len(denominator) + 1)
    while len(numerator) >= len(denominator) and trim(numerator) != (0,):
        degree = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[degree] = coefficient
        for index, value in enumerate(denominator):
            numerator[degree + index] -= coefficient * value
        numerator = list(trim(numerator))
    return trim(quotient), trim(numerator)


def poly_gcd(left, right):
    left, right = trim(left), trim(right)
    while right != (0,):
        _, remainder = poly_divmod(left, right)
        left, right = right, remainder
    if left == (0,):
        return left
    return poly_scale(left, 1 / left[-1])


def poly_evaluate(poly, value):
    answer = F(0)
    for coefficient in reversed(poly):
        answer = answer * value + coefficient
    return answer


class RationalFunction:
    """Canonical element of Q(r)."""

    def __init__(self, numerator=0, denominator=1):
        if isinstance(numerator, RationalFunction):
            self.numerator = numerator.numerator
            self.denominator = numerator.denominator
            return
        numerator = self._poly(numerator)
        denominator = self._poly(denominator)
        require(denominator != (0,), "zero rational-function denominator")
        if numerator == (0,):
            self.numerator, self.denominator = (F(0),), (F(1),)
            return
        common = poly_gcd(numerator, denominator)
        numerator, rem_n = poly_divmod(numerator, common)
        denominator, rem_d = poly_divmod(denominator, common)
        require(rem_n == (0,) and rem_d == (0,), "polynomial gcd division")
        leading = denominator[-1]
        self.numerator = poly_scale(numerator, 1 / leading)
        self.denominator = poly_scale(denominator, 1 / leading)

    @staticmethod
    def _poly(value):
        if isinstance(value, (tuple, list)):
            return trim(value)
        return (F(value),)

    def __add__(self, other):
        other = RationalFunction(other)
        return RationalFunction(
            poly_add(
                poly_multiply(self.numerator, other.denominator),
                poly_multiply(other.numerator, self.denominator),
            ),
            poly_multiply(self.denominator, other.denominator),
        )

    __radd__ = __add__

    def __neg__(self):
        return RationalFunction(poly_neg(self.numerator), self.denominator)

    def __sub__(self, other):
        return self + (-RationalFunction(other))

    def __rsub__(self, other):
        return RationalFunction(other) - self

    def __mul__(self, other):
        other = RationalFunction(other)
        return RationalFunction(
            poly_multiply(self.numerator, other.numerator),
            poly_multiply(self.denominator, other.denominator),
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = RationalFunction(other)
        require(other.numerator != (0,), "rational-function division by zero")
        return RationalFunction(
            poly_multiply(self.numerator, other.denominator),
            poly_multiply(self.denominator, other.numerator),
        )

    def __rtruediv__(self, other):
        return RationalFunction(other) / self

    def __pow__(self, exponent):
        require(type(exponent) is int, "rational-function exponent")
        if exponent >= 0:
            return RationalFunction(
                poly_power(self.numerator, exponent),
                poly_power(self.denominator, exponent),
            )
        return RationalFunction(
            poly_power(self.denominator, -exponent),
            poly_power(self.numerator, -exponent),
        )

    def __eq__(self, other):
        other = RationalFunction(other)
        return (self.numerator == other.numerator
                and self.denominator == other.denominator)

    def evaluate(self, value):
        return (poly_evaluate(self.numerator, value)
                / poly_evaluate(self.denominator, value))


R = RationalFunction((0, 1))
ZERO = RationalFunction(0)
ONE = RationalFunction(1)
RHO = 1 / (R * (R + 1))
P = RationalFunction((6, 6, 3, 1))


def exponential_moment(order):
    return factorial(order) / R ** order


def mixed_moment(a, b):
    """E[Y^a (G-rho)^b] from the three-component mixture."""
    if a % 2:
        return ZERO
    inside = R / (R + 1) * F(1, a + 1) * (-RHO) ** b
    tail = ZERO
    for i in range(a + 1):
        for j in range(b + 1):
            tail += (comb(a, i) * comb(b, j) * (-RHO) ** (b - j)
                     * exponential_moment(i + j))
    return inside + tail / (R + 1)


def set_partitions(size):
    answer = []

    def visit(item, blocks):
        if item == size:
            answer.append(tuple(tuple(block) for block in blocks))
            return
        for index in range(len(blocks)):
            blocks[index].append(item)
            visit(item + 1, blocks)
            blocks[index].pop()
        blocks.append([item])
        visit(item + 1, blocks)
        blocks.pop()

    visit(0, [])
    return answer


def partition_cumulant(a, b):
    answer = ZERO
    for partition in set_partitions(a + b):
        blocks = len(partition)
        term = RationalFunction((-1) ** (blocks - 1) * factorial(blocks - 1))
        for block in partition:
            first = sum(index < a for index in block)
            term *= mixed_moment(first, len(block) - first)
        answer += term
    return answer


def recursive_cumulants(max_order):
    """Independent distinguished-slot moment/cumulant recurrence."""
    answer = {}
    for total in range(1, max_order + 1):
        for a in range(total + 1):
            b = total - a
            value = mixed_moment(a, b)
            if a:
                for i in range(1, a + 1):
                    for j in range(b + 1):
                        if (i, j) == (a, b):
                            continue
                        value -= (comb(a - 1, i - 1) * comb(b, j)
                                  * answer[i, j] * mixed_moment(a - i, b - j))
            else:
                for j in range(1, b):
                    value -= (comb(b - 1, j - 1) * answer[0, j]
                              * mixed_moment(0, b - j))
            answer[a, b] = value
    return answer


def quotient_pair(value):
    """Reduce a rational function modulo r^2+r-1 as a+b*r."""
    modulus = (F(-1), F(1), F(1))
    numerator = poly_divmod(value.numerator, modulus)[1]
    denominator = poly_divmod(value.denominator, modulus)[1]
    a = numerator[0] if numerator else F(0)
    b = numerator[1] if len(numerator) > 1 else F(0)
    c = denominator[0] if denominator else F(0)
    d = denominator[1] if len(denominator) > 1 else F(0)
    norm = c * c - c * d - d * d
    require(norm != 0, "noninvertible golden-ratio denominator")
    return (a * (c - d) - b * d) / norm, (b * c - a * d) / norm


def text_pair(pair):
    return [str(pair[0]), str(pair[1])]


def load_exact_section():
    path = (Path(__file__).resolve().parent.parent
            / "simplex_envelope_asymptotics" / "exact_section.py")
    spec = spec_from_file_location("parametric_exact_section", path)
    require(spec is not None and spec.loader is not None, "exact-section import")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decimal_diagnostics(gamma_function):
    getcontext().prec = 70
    decimal = Decimal
    pi = decimal("3.141592653589793238462643383279502884197169399375105820974944592")
    exact_section = load_exact_section()
    answer = {}
    for label, rho_fraction in (("1/2", F(1, 2)), ("1", F(1)), ("2", F(2))):
        rho = decimal(rho_fraction.numerator) / decimal(rho_fraction.denominator)
        saddle = ((1 + 4 / rho).sqrt() - 1) / 2
        polynomial = saddle ** 3 + 3 * saddle ** 2 + 6 * saddle + 6
        variance_y = polynomial / (3 * saddle ** 2 * (saddle + 1))
        variance_g = ((2 * saddle + 1)
                      / (saddle ** 2 * (saddle + 1) ** 2))
        beta = (2 * (saddle + 1) / saddle
                * (-saddle / (saddle + 1)).exp())
        kappa = beta / (saddle * (2 * pi * variance_y * variance_g).sqrt())

        if rho_fraction == 1:
            gamma_pair = quotient_pair(gamma_function)
            root = (decimal(5).sqrt() - 1) / 2
            gamma = (decimal(gamma_pair[0].numerator) / decimal(gamma_pair[0].denominator)
                     + decimal(gamma_pair[1].numerator) / decimal(gamma_pair[1].denominator)
                     * root)
        elif rho_fraction == F(1, 2):
            gamma_fraction = gamma_function.evaluate(F(1))
            gamma = (decimal(gamma_fraction.numerator)
                     / decimal(gamma_fraction.denominator))
        else:
            # At rho=2, r=(sqrt(3)-1)/2; evaluate the exact rational function.
            coefficients_n = [decimal(x.numerator) / decimal(x.denominator)
                              for x in gamma_function.numerator]
            coefficients_d = [decimal(x.numerator) / decimal(x.denominator)
                              for x in gamma_function.denominator]
            numerator = decimal(0)
            denominator = decimal(0)
            for coefficient in reversed(coefficients_n):
                numerator = numerator * saddle + coefficient
            for coefficient in reversed(coefficients_d):
                denominator = denominator * saddle + coefficient
            gamma = numerator / denominator

        rows = []
        for n in (3, 6, 9, 12):
            size = n + 1
            exact = (exact_section.section(size, rho_fraction * size)
                     * F(factorial(n), size ** n))
            exact_decimal = (decimal(exact.numerator) / decimal(exact.denominator))
            ratio = exact_decimal * decimal(n).sqrt() / (kappa * beta ** n)
            rows.append({
                "n": n,
                "n_scaled_first_residual": f"{decimal(n) * (ratio - 1):.18f}",
            })
        answer[label] = {
            "gamma1": f"{gamma:.18f}",
            "rows": rows,
        }
    return answer


def main():
    require([len(set_partitions(n)) for n in range(1, 5)] == [1, 2, 5, 15],
            "Bell-number check")
    cumulants = recursive_cumulants(4)
    for total in range(1, 5):
        for a in range(total + 1):
            b = total - a
            require(cumulants[a, b] == partition_cumulant(a, b),
                    f"cumulant algorithms disagree at {(a, b)}")

    expected = {
        (2, 0): P / (3 * R ** 2 * (R + 1)),
        (0, 2): (2 * R + 1) / (R ** 2 * (R + 1) ** 2),
        (2, 1): (2 * RationalFunction((6, 12, 6, 1))
                 / (3 * R ** 3 * (R + 1) ** 2)),
        (0, 3): (2 * RationalFunction((1, 3, 3))
                 / (R ** 3 * (R + 1) ** 3)),
        (4, 0): (RationalFunction((F(12), F(24), F(12), F(0), F(-2),
                                            F(-4, 5), F(-2, 15)))
                 / (R ** 4 * (R + 1) ** 2)),
        (2, 2): (RationalFunction((F(12), F(36), F(36), F(12), F(4, 3)))
                 / (R ** 4 * (R + 1) ** 3)),
        (0, 4): (RationalFunction((6, 24, 36, 24))
                 / (R ** 4 * (R + 1) ** 4)),
    }
    for key, value in expected.items():
        require(cumulants[key] == value, f"explicit cumulant {key}")

    variance_y = cumulants[2, 0]
    variance_g = cumulants[0, 2]
    k21, k03, k40, k22, k04 = [
        cumulants[key] for key in ((2, 1), (0, 3), (4, 0), (2, 2), (0, 4))
    ]
    q0 = (k40 / (8 * variance_y ** 2)
          + k22 / (4 * variance_y * variance_g)
          + k04 / (8 * variance_g ** 2)
          - 3 * k21 ** 2 / (8 * variance_y ** 2 * variance_g)
          - k21 * k03 / (4 * variance_y * variance_g ** 2)
          - 5 * k03 ** 2 / (24 * variance_g ** 3))
    section_a1 = (q0 + k21 / (2 * variance_y * variance_g * R)
                  + k03 / (2 * variance_g ** 2 * R)
                  - 1 / (variance_g * R ** 2))
    gamma1 = section_a1 - F(5, 12)

    gamma_numerator = RationalFunction((
        -270, -2160, -8370, -16740, -18045, -9504,
        -873, 918, 150, 28, 30,
    ))
    gamma_expected = (gamma_numerator
                      / (60 * (2 * R + 1) ** 3 * P ** 2))
    require(gamma1 == gamma_expected, "displayed gamma1 rational function")
    require(quotient_pair(RHO) == (F(1), F(0)), "rho=1 specialization")
    require(quotient_pair(variance_y) == (F(13, 3), F(8, 3)),
            "golden variance Y")
    require(quotient_pair(variance_g) == (F(1), F(2)), "golden variance G")
    require(quotient_pair(section_a1) == (F(-343, 30), F(284, 15)),
            "golden section correction")
    require(quotient_pair(gamma1) == (F(-237, 20), F(284, 15)),
            "golden normalized correction")
    require(gamma1.evaluate(F(1)) == F(-13709, 103680),
            "rho=1/2 rational specialization")

    print(dumps({
        "status": "PARAMETRIC_SECTION_CORRECTION_VERIFIED",
        "domain": "Q(r), r>0, rho=1/[r(r+1)]",
        "partition_counts": [len(set_partitions(n)) for n in range(1, 5)],
        "covariance": {
            "v": "(r^3+3r^2+6r+6)/(3r^2(r+1))",
            "w": "(2r+1)/(r^2(r+1)^2)",
        },
        "gamma1": (
            "(30r^10+28r^9+150r^8+918r^7-873r^6-9504r^5"
            "-18045r^4-16740r^3-8370r^2-2160r-270)"
            "/(60(2r+1)^3(r^3+3r^2+6r+6)^2)"
        ),
        "specializations": {
            "rho=1": {
                "section_a1": text_pair(quotient_pair(section_a1)),
                "gamma1": text_pair(quotient_pair(gamma1)),
            },
            "rho=1/2": {
                "r": "1",
                "gamma1": str(gamma1.evaluate(F(1))),
            },
        },
        "finite_corroboration": decimal_diagnostics(gamma1),
        "scope": (
            "Exact rational-function algebra and finite sections verify the first "
            "correction; PROOF.md establishes the locally uniform all-orders remainder."
        ),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
