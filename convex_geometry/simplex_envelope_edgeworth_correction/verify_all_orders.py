"""Exact all-orders machinery through the second relative correction.

The coefficient field is Q(r), r^2+r-1=0. Universal asymptotic validity is
proved in ALL_ORDERS.md; this script verifies the finite symbolic algebra and
compares with the predecessor's exact constants.
"""

from decimal import Decimal, getcontext
from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from json import dumps
from math import comb, factorial
from pathlib import Path

from verify import add, divide, mixed_moment, mul, power, q, scale, sub


R = q(0, 1)
ZERO = q(0)
ONE = q(1)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_pair(value):
    return [str(value[0]), str(value[1])]


def set_partitions(n):
    """Canonical set partitions of range(n), one block order only."""
    answer = []

    def visit(item, blocks):
        if item == n:
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
    """Joint cumulant from the set-partition formula."""
    answer = ZERO
    for partition in set_partitions(a + b):
        blocks = len(partition)
        term = q((-1) ** (blocks - 1) * factorial(blocks - 1))
        for block in partition:
            first = sum(index < a for index in block)
            term = mul(term, mixed_moment(first, len(block) - first))
        answer = add(answer, term)
    return answer


def recursive_cumulants(max_order):
    """Independent distinguished-slot moment/cumulant recursion."""
    cumulants = {}
    for total in range(1, max_order + 1):
        for a in range(total + 1):
            b = total - a
            value = mixed_moment(a, b)
            if a:
                for i in range(1, a + 1):
                    for j in range(b + 1):
                        if i == a and j == b:
                            continue
                        coefficient = comb(a - 1, i - 1) * comb(b, j)
                        value = sub(value, scale(mul(cumulants[i, j],
                                                     mixed_moment(a - i, b - j)),
                                                 coefficient))
            else:
                for j in range(1, b):
                    coefficient = comb(b - 1, j - 1)
                    value = sub(value, scale(mul(cumulants[0, j],
                                                 mixed_moment(0, b - j)),
                                             coefficient))
            cumulants[a, b] = value
    return cumulants


def polynomial_add(left, right):
    answer = left.copy()
    for key, value in right.items():
        answer[key] = add(answer.get(key, ZERO), value)
    return {key: value for key, value in answer.items() if value != ZERO}


def polynomial_scale(poly, coefficient):
    return {key: scale(value, coefficient) for key, value in poly.items()
            if scale(value, coefficient) != ZERO}


def polynomial_multiply(left, right):
    answer = {}
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            key = a + c, b + d
            answer[key] = add(answer.get(key, ZERO), mul(x, y))
    return {key: value for key, value in answer.items() if value != ZERO}


def polynomial_power(poly, exponent):
    answer = {(0, 0): ONE}
    for _ in range(exponent):
        answer = polynomial_multiply(answer, poly)
    return answer


def hermite(n):
    """Probabilists' Hermite polynomial, degree -> integer coefficient."""
    previous = {0: 1}
    if n == 0:
        return previous
    current = {1: 1}
    for degree in range(1, n):
        following = {power_ + 1: coefficient for power_, coefficient in current.items()}
        for power_, coefficient in previous.items():
            following[power_] = following.get(power_, 0) - degree * coefficient
        previous, current = current, {key: value for key, value in following.items() if value}
    return current


def edgeworth_series(cumulants):
    """Relative density series (epsilon degree, u degree) through epsilon^4."""
    covariance_y = cumulants[2, 0]
    covariance_cost = cumulants[0, 2]
    cumulant_polynomials = {}
    for total in range(3, 7):
        poly = {}
        for a in range(total + 1):
            b = total - a
            value = cumulants[a, b]
            if value != ZERO:
                poly[a, b] = scale(value, F(1, factorial(a) * factorial(b)))
        cumulant_polynomials[total] = poly

    l3, l4 = cumulant_polynomials[3], cumulant_polynomials[4]
    l5, l6 = cumulant_polynomials[5], cumulant_polynomials[6]
    edgeworth = {
        1: l3,
        2: polynomial_add(l4, polynomial_scale(polynomial_power(l3, 2), F(1, 2))),
        3: polynomial_add(
            polynomial_add(l5, polynomial_multiply(l3, l4)),
            polynomial_scale(polynomial_power(l3, 3), F(1, 6)),
        ),
    }
    fourth = l6
    fourth = polynomial_add(fourth, polynomial_multiply(l3, l5))
    fourth = polynomial_add(fourth, polynomial_scale(polynomial_power(l4, 2), F(1, 2)))
    fourth = polynomial_add(
        fourth,
        polynomial_scale(polynomial_multiply(polynomial_power(l3, 2), l4), F(1, 2)),
    )
    fourth = polynomial_add(fourth, polynomial_scale(polynomial_power(l3, 4), F(1, 24)))
    edgeworth[4] = fourth

    hermites = {n: hermite(n) for n in range(13)}
    series = {(0, 0): ONE}
    for base_order, poly in edgeworth.items():
        for (a, b), coefficient in poly.items():
            first_at_zero = hermites[a].get(0, 0)
            if not first_at_zero:
                continue
            for u_power, second_coefficient in hermites[b].items():
                epsilon_power = base_order + u_power
                if epsilon_power > 4:
                    continue
                require(a % 2 == 0 and (b + u_power) % 2 == 0,
                        "square-root cancellation failed")
                denominator = mul(power(covariance_y, a // 2),
                                  power(covariance_cost, (b + u_power) // 2))
                value = divide(
                    scale(coefficient,
                          first_at_zero * second_coefficient * (-1) ** u_power),
                    denominator,
                )
                key = epsilon_power, u_power
                series[key] = add(series.get(key, ZERO), value)

    gaussian = {
        (0, 0): ONE,
        (2, 2): scale(power(covariance_cost, -1), F(-1, 2)),
        (4, 4): scale(power(covariance_cost, -2), F(1, 8)),
    }
    full = {}
    for (epsilon_a, u_a), x in series.items():
        for (epsilon_b, u_b), y in gaussian.items():
            if epsilon_a + epsilon_b <= 4:
                key = epsilon_a + epsilon_b, u_a + u_b
                full[key] = add(full.get(key, ZERO), mul(x, y))
    return {key: value for key, value in full.items() if value != ZERO}


def exponential_average(series, epsilon_order):
    answer = ZERO
    for (order, degree), coefficient in series.items():
        if order == epsilon_order:
            moment = scale(power(R, -degree), factorial(degree))
            answer = add(answer, mul(coefficient, moment))
    return answer


def load_predecessor():
    path = Path(__file__).resolve().parent.parent / "simplex_envelope_asymptotics" / "exact_section.py"
    spec = spec_from_file_location("predecessor_exact_section_all_orders", path)
    require(spec is not None and spec.loader is not None, "predecessor import spec")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decimal_value(value, r_decimal):
    return (Decimal(value[0].numerator) / Decimal(value[0].denominator)
            + Decimal(value[1].numerator) / Decimal(value[1].denominator) * r_decimal)


def diagnostics(gamma1, gamma2, covariance_y, covariance_cost):
    getcontext().prec = 70
    r_decimal = (Decimal(5).sqrt() - 1) / 2
    beta = Decimal(2) / (r_decimal * r_decimal) * (r_decimal - 1).exp()
    pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592")
    kappa = beta / (
        r_decimal
        * (2 * pi * decimal_value(covariance_y, r_decimal)
           * decimal_value(covariance_cost, r_decimal)).sqrt()
    )
    first = decimal_value(gamma1, r_decimal)
    second = decimal_value(gamma2, r_decimal)
    predecessor = load_predecessor()
    rows = []
    for n in range(1, 13):
        exact = predecessor.sharp_constant(n)
        exact_decimal = Decimal(exact.numerator) / Decimal(exact.denominator)
        ratio = exact_decimal * Decimal(n).sqrt() / (kappa * beta ** n)
        twice_scaled = Decimal(n * n) * (ratio - 1 - first / Decimal(n))
        third_residual = Decimal(n ** 3) * (
            ratio - 1 - first / Decimal(n) - second / Decimal(n * n)
        )
        rows.append({
            "n": n,
            "n2_after_first": f"{twice_scaled:.18f}",
            "n3_after_second": f"{third_residual:.18f}",
        })
    return {
        "gamma1": f"{first:.18f}",
        "gamma2": f"{second:.18f}",
        "rows": rows,
    }


def main():
    require([len(set_partitions(n)) for n in range(1, 7)] == [1, 2, 5, 15, 52, 203],
            "Bell-number partition check")
    cumulants = recursive_cumulants(6)
    for total in range(1, 7):
        for a in range(total + 1):
            b = total - a
            require(cumulants[a, b] == partition_cumulant(a, b),
                    f"cumulant algorithms disagree at {(a, b)}")
    require(cumulants[2, 0] == q(F(13, 3), F(8, 3)), "variance Y")
    require(cumulants[0, 2] == q(1, 2), "variance cost")

    series = edgeworth_series(cumulants)
    require(not any(order in (1, 3) for order, _ in series), "odd powers survived")
    expected_a_poly = {
        0: q(F(-83, 6), F(314, 15)),
        1: q(F(-7, 5), F(23, 5)),
        2: q(F(-1, 10), F(-1, 5)),
    }
    expected_b_poly = {
        0: q(F(48873599, 12600), F(-219673, 35)),
        1: q(F(33529, 50), F(-163097, 150)),
        2: q(F(10733, 300), F(-1372, 25)),
        3: q(F(-5, 6), F(19, 30)),
        4: q(F(1, 40)),
    }
    require({degree: value for (order, degree), value in series.items() if order == 2}
            == expected_a_poly, "first density polynomial")
    require({degree: value for (order, degree), value in series.items() if order == 4}
            == expected_b_poly, "second density polynomial")

    section_a = exponential_average(series, 2)
    section_b = exponential_average(series, 4)
    gamma1 = sub(section_a, q(F(5, 12)))
    gamma2 = add(section_b, add(scale(section_a, F(-17, 12)), q(F(73, 288))))
    require(section_a == q(F(-343, 30), F(284, 15)), "section a1")
    require(section_b == q(F(43987487, 12600), F(-2965409, 525)), "section a2")
    require(gamma1 == q(F(-237, 20), F(284, 15)), "gamma1")
    require(gamma2 == q(F(176779063, 50400), F(-8938472, 1575)), "gamma2")

    selected = {
        f"K{a}{b}": text_pair(cumulants[a, b])
        for a, b in ((0, 5), (2, 3), (4, 1), (0, 6), (2, 4), (4, 2), (6, 0))
    }
    print(dumps({
        "status": "ALL_ORDERS_SECOND_COEFFICIENT_VERIFIED",
        "field": "Q(r), r^2+r-1=0",
        "partition_counts": [len(set_partitions(n)) for n in range(1, 7)],
        "selected_cumulants": selected,
        "density_M_inverse": {str(k): text_pair(v) for k, v in expected_a_poly.items()},
        "density_M_inverse_squared": {str(k): text_pair(v) for k, v in expected_b_poly.items()},
        "section_a1": text_pair(section_a),
        "section_a2": text_pair(section_b),
        "gamma1": text_pair(gamma1),
        "gamma2": text_pair(gamma2),
        "finite_corroboration": diagnostics(
            gamma1, gamma2, cumulants[2, 0], cumulants[0, 2]
        ),
        "scope": (
            "Exact symbolic algebra and finite constants corroborate gamma2; "
            "ALL_ORDERS.md proves the asymptotic expansion."
        ),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
