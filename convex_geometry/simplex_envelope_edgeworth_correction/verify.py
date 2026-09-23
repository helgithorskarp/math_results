"""Exact coefficient algebra and finite corroboration for the first correction.

Universal validity rests on PROOF.md. Decimal diagnostics are evaluated only
after all identities in Q(r), r^2+r-1=0, have passed exactly.
"""

from decimal import Decimal, getcontext
from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from json import dumps
from math import comb, factorial
from pathlib import Path


# Elements are a+b*r in Q(r), where r^2=1-r.
def q(a=0, b=0):
    return F(a), F(b)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def neg(x):
    return -x[0], -x[1]


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    a, b = x
    c, d = y
    return a * c + b * d, a * d + b * c - b * d


def scale(x, c):
    return mul(x, q(c))


def inverse(x):
    a, b = x
    norm = a * a - a * b - b * b
    if not norm:
        raise ZeroDivisionError("zero element in Q(r)")
    return (a - b) / norm, -b / norm


def divide(x, y):
    return mul(x, inverse(y))


def power(x, n):
    if n < 0:
        return power(inverse(x), -n)
    result = q(1)
    base = x
    while n:
        if n & 1:
            result = mul(result, base)
        base = mul(base, base)
        n //= 2
    return result


R = q(0, 1)


def exponential_moment(j):
    """E[E^j] for E exponential of rate r."""
    return scale(power(R, -j), factorial(j))


def mixed_moment(a, b):
    """E[Y^a (G-1)^b] from the three-component mixture."""
    if a % 2:
        return q(0)
    cube = scale(power(R, 2), F((-1) ** b, a + 1))
    tail = q(0)
    for i in range(a + 1):
        for j in range(b + 1):
            coefficient = comb(a, i) * comb(b, j) * (-1) ** (b - j)
            tail = add(tail, scale(exponential_moment(i + j), coefficient))
    return add(cube, mul(R, tail))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_pair(x):
    return [str(x[0]), str(x[1])]


def exact_coefficient_data():
    v = mixed_moment(2, 0)
    w = mixed_moment(0, 2)
    k21 = mixed_moment(2, 1)
    k03 = mixed_moment(0, 3)
    k40 = sub(mixed_moment(4, 0), scale(mul(v, v), 3))
    k22 = sub(mixed_moment(2, 2), mul(v, w))
    k04 = sub(mixed_moment(0, 4), scale(mul(w, w), 3))

    require(v == q(F(13, 3), F(8, 3)), "variance Y")
    require(w == q(1, 2), "variance cost")
    require(k21 == q(F(38, 3), F(22, 3)), "K21")
    require(k03 == q(8), "K03")
    require(k40 == q(F(878, 15), F(184, 5)), "K40")
    require(k22 == q(F(176, 3), F(116, 3)), "K22")
    require(k04 == q(18, 36), "K04")

    q0 = add(
        add(divide(k40, scale(mul(v, v), 8)),
            divide(k22, scale(mul(v, w), 4))),
        divide(k04, scale(mul(w, w), 8)),
    )
    q0 = sub(q0, divide(scale(mul(k21, k21), 3), scale(mul(mul(v, v), w), 8)))
    q0 = sub(q0, divide(mul(k21, k03), scale(mul(v, mul(w, w)), 4)))
    q0 = sub(q0, divide(scale(mul(k03, k03), 5), scale(power(w, 3), 24)))

    section = q0
    section = add(section, divide(k21, scale(mul(mul(v, w), R), 2)))
    section = add(section, divide(k03, scale(mul(mul(w, w), R), 2)))
    section = sub(section, inverse(mul(w, power(R, 2))))
    gamma = sub(section, q(F(5, 12)))

    require(q0 == q(F(-83, 6), F(314, 15)), "Q0 simplification")
    require(section == q(F(-343, 30), F(284, 15)), "section correction")
    require(gamma == q(F(-237, 20), F(284, 15)), "final correction")
    return {
        "variance_y": text_pair(v),
        "variance_cost": text_pair(w),
        "K21": text_pair(k21),
        "K03": text_pair(k03),
        "K40": text_pair(k40),
        "K22": text_pair(k22),
        "K04": text_pair(k04),
        "Q0": text_pair(q0),
        "section_correction": text_pair(section),
        "gamma": text_pair(gamma),
    }, gamma, v, w


def load_predecessor():
    path = Path(__file__).resolve().parent.parent / "simplex_envelope_asymptotics" / "exact_section.py"
    spec = spec_from_file_location("predecessor_exact_section", path)
    require(spec is not None and spec.loader is not None, "predecessor import spec")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decimal_value(x, r_decimal):
    return Decimal(x[0].numerator) / Decimal(x[0].denominator) + (
        Decimal(x[1].numerator) / Decimal(x[1].denominator)
    ) * r_decimal


def finite_diagnostics(gamma_pair, v_pair, w_pair):
    getcontext().prec = 70
    five = Decimal(5)
    r_dec = (five.sqrt() - 1) / 2
    v_dec = decimal_value(v_pair, r_dec)
    w_dec = decimal_value(w_pair, r_dec)
    gamma_dec = decimal_value(gamma_pair, r_dec)
    beta = Decimal(2) / (r_dec * r_dec) * (r_dec - 1).exp()
    pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592")
    kappa = beta / (r_dec * (2 * pi * v_dec * w_dec).sqrt())

    predecessor = load_predecessor()
    constants = {n: predecessor.sharp_constant(n) for n in range(1, 13)}
    require(constants[1] == F(2) and constants[3] == F(127, 8), "predecessor constants")
    rows = []
    scaled_errors = []
    for n, value in constants.items():
        c_dec = Decimal(value.numerator) / Decimal(value.denominator)
        ratio = c_dec * Decimal(n).sqrt() / (kappa * beta ** n)
        scaled = Decimal(n) * (ratio - 1)
        residual = Decimal(n * n) * (ratio - 1 - gamma_dec / Decimal(n))
        rows.append({
            "n": n,
            "n_times_relative_error": f"{scaled:.18f}",
            "second_residual": f"{residual:.18f}",
        })
        scaled_errors.append(scaled)
    require(all(abs(scaled_errors[n] - gamma_dec) < abs(scaled_errors[n - 1] - gamma_dec)
                for n in range(2, 12)), "finite errors do not approach gamma monotonically")
    return {
        "r": f"{r_dec:.18f}",
        "beta": f"{beta:.18f}",
        "kappa": f"{kappa:.18f}",
        "gamma": f"{gamma_dec:.18f}",
        "rows": rows,
    }


def main():
    exact, gamma, v, w = exact_coefficient_data()
    diagnostics = finite_diagnostics(gamma, v, w)
    print(dumps({
        "status": "EXACT_EDGEWORTH_COEFFICIENT_VERIFIED",
        "field": "Q(r), r^2+r-1=0",
        "exact": exact,
        "finite_corroboration": diagnostics,
        "scope": (
            "Exact algebra and C1..C12 corroborate the coefficient; "
            "the uniform asymptotic remainder is proved in PROOF.md."
        ),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
