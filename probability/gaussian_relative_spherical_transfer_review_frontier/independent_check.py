#!/usr/bin/env python3
"""Independent exact audit of the loss-relative spherical transfer constants.

The target code is not imported.  Coefficient envelopes are recast as exact
univariate polynomial inequalities and certified on z in [0,1/4] through
nonnegative Bernstein coefficients.  A small dual-number implementation
independently checks the radial chain rule.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "gaussian_relative_spherical_transfer"
PINS = {
    "gaussian_relative_spherical_transfer/EXPECTED.json": "db3edd55873316d725deb5f0d9c54419476969806a45d962bef33a8e0342c1b6",
    "gaussian_relative_spherical_transfer/PROOF.md": "5a5532c437e756ee8175ec9cd38f6610b14e9fd5c10452ce6b63d7e3026e28be",
    "gaussian_relative_spherical_transfer/README.md": "a2a43b5dadecb2c229536c9384c385782fdaaef15b3cdd68f17f50e48175b0dc",
    "gaussian_relative_spherical_transfer/SOURCES.md": "4fb74765318a6bce6b6e4186a6a5b245cf7a0c65a45fceacceeb04dedb5efdaf",
    "gaussian_relative_spherical_transfer/verify.py": "70b914b4680f1ee7a61f05c09f1c233299fcf6e9fb8bba5205186b923289cd10",
    "gaussian_majorisation_spherical_tail/PROOF.md": "78ed0501580e9c192b468b41a2d1afda7bd327a0610c5a2fe04f44bd07a0d76b",
    "gaussian_majorisation_high_noise_window/PROOF.md": "e96063604af579e6ebb8cb25e6eb82ca65c07f6716ecc85f67ae6cc137d0bdf9",
    "gaussian_loss_normalized_hinges/PROOF.md": "92e7dcb81ae1f4c032e5528d7ff9568da94b826e84d110957542c0310337f2f8",
    "gaussian_loss_normalized_hinges_review_frontier/REVIEW.md": "093e2aee486bfd4af91a2eede7a0a31f678ac5d241725548d3858492b78b1b23",
    "gaussian_majorisation_hankel_transport/PROOF.md": "2f2f653710bd9214fca898c82b7d56119ec83ea1238c6860ceeb310d657e7fae",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def trim(poly):
    result = list(map(F, poly))
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def add(a, b):
    out = [F(0)] * max(len(a), len(b))
    for j, value in enumerate(a):
        out[j] += value
    for j, value in enumerate(b):
        out[j] += value
    return trim(out)


def scale(a, value):
    return trim([F(value) * x for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def power(a, exponent):
    out = [F(1)]
    base = list(a)
    while exponent:
        if exponent & 1:
            out = mul(out, base)
        base = mul(base, base)
        exponent //= 2
    return out


def bernstein_on_quarter(poly):
    """Bernstein coefficients of poly(z) after z=t/4, 0<=t<=1."""
    power_coefficients = [coefficient / 4**degree
                          for degree, coefficient in enumerate(trim(poly))]
    degree = len(power_coefficients) - 1
    return [sum(power_coefficients[k] * F(comb(i, k), comb(degree, k))
                for k in range(i + 1))
            for i in range(degree + 1)]


def certify(name, poly):
    coefficients = bernstein_on_quarter(poly)
    require(min(coefficients) >= 0, "negative Bernstein coefficient: " + name)
    return name, str(min(coefficients)), len(coefficients) - 1


class Dual:
    def __init__(self, value, derivative=0):
        self.value, self.derivative = F(value), F(derivative)

    def __add__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(self.value + other.value, self.derivative + other.derivative)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Dual) else -F(other))

    def __rsub__(self, other):
        return Dual(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(self.value * other.value,
                    self.derivative * other.value + self.value * other.derivative)

    __rmul__ = __mul__

    def reciprocal(self):
        require(self.value != 0, "dual division by zero")
        return Dual(1 / self.value, -self.derivative / self.value**2)

    def __truediv__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return self * other.reciprocal()

    def __pow__(self, exponent):
        require(type(exponent) is int and exponent >= 0, "bad dual exponent")
        if exponent == 0:
            return Dual(1)
        return Dual(self.value**exponent,
                    exponent * self.value**(exponent - 1) * self.derivative)


def pin_sources():
    for name, expected in PINS.items():
        actual = sha256((ROOT / name).read_bytes()).hexdigest()
        require(actual == expected, "source pin mismatch: " + name)


def chain_rule_checks():
    checks = 0
    for p, b, q, epsilon, mpp, kval, kp in product(
            (F(1, 2), F(1), F(3)),
            (F(1, 4), F(1), F(2)),
            (F(1, 8), F(1), F(5)),
            (F(0), F(1, 64)),
            (F(0), F(1)),
            (F(1, 3), F(2)),
            (F(-1), F(0), F(3))):
        dp = q / b
        p_dual = Dual(p, dp)
        b_dual = Dual(b, (1 - epsilon * mpp) * dp)
        k_dual = Dual(kval, kp * dp)
        automatic = k_dual * p_dual**5 / b_dual
        predicted = (q * p**5 * kp / b**2
                     + q * kval * (5 * p**4 / b**2
                                    - p**5 * (1 - epsilon * mpp) / b**3))
        require(automatic.derivative == predicted, "radial chain rule mismatch")
        checks += 1
    return checks


def coefficient_certificates():
    one, z = [F(1)], [F(0), F(1)]
    ap, am = add(one, z), sub(one, z)
    bp, bm = add(one, scale(z, 2)), sub(one, scale(z, 2))

    records = []
    records.append(certify("R1 upper difference",
        sub(mul(add(one, scale(z, 70)), power(bm, 2)), power(ap, 5))))
    records.append(certify("R1 lower difference",
        sub(power(am, 5), mul(sub(one, scale(z, 70)), power(bp, 2)))))
    records.append(certify("R1 absolute maximum",
        sub(scale(power(bm, 2), 13), power(ap, 5))))

    max_numerator = mul(power(ap, 4), sub(scale(bm, 5), ap))
    min_numerator = mul(power(am, 4), sub(scale(bp, 5), am))
    records.append(certify("R2 upper difference",
        sub(mul(add(scale(one, 4), scale(z, 440)), power(bm, 3)), max_numerator)))
    records.append(certify("R2 lower difference",
        sub(min_numerator, mul(sub(scale(one, 4), scale(z, 440)), power(bp, 3)))))
    records.append(certify("R2 absolute maximum",
        sub(scale(power(bm, 3), 80), max_numerator)))
    records.append(certify("epsilon coefficient",
        sub(scale(power(bm, 3), 25), power(ap, 5))))

    # A deliberately inadequate R1 coefficient must fail its certificate.
    damaged = sub(mul(add(one, scale(z, 40)), power(bm, 2)), power(ap, 5))
    require(min(bernstein_on_quarter(damaged)) < 0,
            "weakened coefficient mutation was not rejected")
    return records


def analytic_constant_checks():
    epsilon, lam, kappa = F(1, 64), F(1, 2), F(63, 64)
    require(kappa**-3 < 3, "strong-convexity inverse bound")
    require(16**2 <= 17**2 * kappa, "modal square-root bound")
    require(22 * epsilon < 1 and 4 + 17 * epsilon < 5,
            "modal exponential envelope")
    require(4 * epsilon / lam == F(1, 8), "prefix separation")

    # Direct recomputation sharpens the source's rational upper 256 to 128.
    require(180**2 < 2 * 128**2, "physical prefix coefficient")
    physical, limiting = 128, 64
    strengthened = (physical + limiting) * epsilon**3 / lam**2
    claimed = 320 * epsilon**3 / lam**2
    require(strengthened == F(3, 1024), "strengthened prefix ratio")
    require(claimed == F(5, 1024) < 1, "claimed prefix ratio")

    require(F(800, 32) * F(1, 4) == F(25, 4), "outer coefficient")
    require(F(25, 4) < 25, "pi<4 absorption")
    require(F(9, 64) > F(1, 8), "transition/high-window overlap")

    eta = F(1, 3888)
    c2_upper = 1 + 450 * 3**9
    required_variance = 2 * c2_upper / eta
    require(c2_upper == 8857351, "two-point exponential constant")
    require(2**37 > required_variance, "advertised variance insufficient")
    require(2**36 < required_variance, "variance mutation was not rejected")
    ratios = []
    for j in (1, 4, 16, 64, 128):
        radius = 1 - F(1, 2**j)
        loss = 2 * (1 - radius**2)
        spherical_lower = eta * loss
        gaussian_error = F(c2_upper, 2**37) * loss
        require(0 < gaussian_error < spherical_lower / 2,
                "loss-uniform calibration failed")
        ratios.append(str(gaussian_error / spherical_lower))
    require(len(set(ratios)) == 1, "calibration ratio depends on loss")
    return {
        "strengthened_prefix_over_D_epsilon": str(strengthened),
        "claimed_prefix_over_D_epsilon": str(claimed),
        "calibration_error_over_spherical_lower": ratios[0],
        "minimum_variance_power": 37,
    }


def main():
    pin_sources()
    chain = chain_rule_checks()
    certificates = coefficient_certificates()
    constants = analytic_constant_checks()
    print("RELATIVE_SPHERICAL_TRANSFER_INDEPENDENT_ACCEPT")
    print(f"exact dual chain-rule evaluations={chain}")
    print("Bernstein certificates=" + repr(certificates))
    print("constant controls=" + repr(constants))


if __name__ == "__main__":
    main()
