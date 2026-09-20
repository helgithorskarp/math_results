#!/usr/bin/env python3
"""Exact corroboration for PROOF.md; CPython 3.11+, standard library only.

Counts are computed by a transfer recurrence, checked against coordinate
enumeration, and compared to an independent multivariate cone expansion.
No floating point, solver, network, randomness, or target-generated inputs.
"""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from math import comb, factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def valid(widths):
    if len(widths) < 3 or len(widths) % 2 != 1:
        raise ValueError("an odd cycle of length at least three is required")
    if any(type(a) is not int or a < 1 for a in widths):
        raise ValueError("positive integer block widths are required")


def count(widths, n):
    """Weighted closed-walk count, keeping the first row sum explicit."""
    valid(widths)
    if type(n) is not int or n < 0:
        raise ValueError("nonnegative integer dilation required")
    weights = [[comb(r + a - 1, a - 1) for r in range(n + 1)] for a in widths]
    total = 0
    for first in range(n + 1):
        values = [0] * (n + 1)
        values[first] = weights[0][first]
        for row in weights[1:]:
            prefix, running = [], 0
            for v in values:
                running += v
                prefix.append(running)
            values = [row[r] * prefix[n - r] for r in range(n + 1)]
        total += sum(values[:n - first + 1])
    return total


def coordinate_count(widths, n):
    """Definition-level enumeration in the full coordinate space."""
    total = 0
    for x in product(range(n + 1), repeat=sum(widths)):
        rows, start = [], 0
        for a in widths:
            rows.append(sum(x[start:start + a]))
            start += a
        total += all(rows[i] + rows[(i + 1) % len(rows)] <= n for i in range(len(rows)))
    return total


def trim(p):
    while p and p[-1] == 0:
        p.pop()
    return p


def poly_mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)


def evaluate(p, x):
    value = F(0)
    for a in reversed(p):
        value = value * x + a
    return value


def interpolate(values, start=0, step=1):
    """Newton differences, returned as a polynomial in the original n."""
    differences = list(map(F, values))
    basis, answer = [F(1)], [F(0)] * len(values)
    for j in range(len(values)):
        for i, v in enumerate(basis):
            answer[i] += differences[0] * v
        differences = [b - a for a, b in zip(differences, differences[1:])]
        basis = poly_mul(basis, [F(-start - step * j, step * (j + 1)),
                                 F(1, step * (j + 1))])
    return trim(answer)


def divide_plus(p):
    require(len(p) >= 2, "cannot divide a constant by 1+t")
    q = [p[0]]
    for x in p[1:-1]:
        q.append(x - q[-1])
    require(q[-1] == p[-1], "nonzero remainder on division by 1+t")
    return trim(q)


def gamma(p):
    require(p == p[::-1], "gamma input is not palindromic")
    degree = len(p) - 1
    remaining, result = p[:], []
    for j in range(degree // 2 + 1):
        value = remaining[j]
        result.append(value)
        for i in range(degree - 2 * j + 1):
            remaining[j + i] -= value * comb(degree - 2 * j, i)
    require(not any(remaining), "gamma reconstruction failed")
    return result


def inverse_cycle(m):
    """Gaussian elimination, independent of the alternating-shift formula."""
    matrix = [[F(int(j == i or j == (i + 1) % m)) for j in range(m)]
              + [F(int(i == j)) for j in range(m)] for i in range(m)]
    for j in range(m):
        pivot = next(i for i in range(j, m) if matrix[i][j])
        matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
        scale = matrix[j][j]
        matrix[j] = [x / scale for x in matrix[j]]
        for i in range(m):
            if i != j:
                factor = matrix[i][j]
                matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[j])]
    return [row[m:] for row in matrix]


def box_mul(p, q, bounds):
    out = {}
    for alpha, x in p.items():
        for beta, y in q.items():
            index = tuple(a + b for a, b in zip(alpha, beta))
            if all(v <= cap for v, cap in zip(index, bounds)):
                out[index] = out.get(index, F(0)) + x * y
    return {i: v for i, v in out.items() if v}


def cone_alternating(widths):
    """Entire B(n), reconstructed from the analytic cone character.

    Compute Z(y)=product sech((T-column dot y)/2) in the exact box jet
    0<=degree(y_i)<=a_i-1, then apply the polynomial differential weights.
    This function does not call count(), nor use the claimed leading terms.
    """
    m = len(widths)
    bounds = tuple(a - 1 for a in widths)
    k = sum(bounds)
    indices = list(product(*(range(b + 1) for b in bounds)))
    inv = inverse_cycle(m)
    sech = [F(0)] * (k + 1)
    sech[0] = F(1)
    for degree in range(2, k + 1, 2):
        sech[degree] = -sum(sech[degree - j] / factorial(j)
                            for j in range(2, degree + 1, 2))
    series = {(0,) * m: F(1)}
    for j in range(m):
        factor = {}
        for alpha in indices:
            degree = sum(alpha)
            value = sech[degree] * factorial(degree)
            for i, exponent in enumerate(alpha):
                value *= (inv[i][j] / 2) ** exponent / factorial(exponent)
            if value:
                factor[alpha] = value
        series = box_mul(series, factor, bounds)

    values = []
    for n in range(k + 1):
        operators = []
        for b in bounds:
            op = [F(1)]
            for j in range(1, b + 1):
                op = poly_mul(op, [F(n, 2) + F(1, 4) + j, F(1)])
            operators.append([v / factorial(b) for v in op])
        total = F(0)
        for alpha, coefficient in series.items():
            term = coefficient
            for i, exponent in enumerate(alpha):
                term *= factorial(exponent) * operators[i][exponent]
            total += term
        values.append(total / (2 ** (m + 1)))
    return interpolate(values)


def run():
    uniform = [(a,) * m for m in (3, 5, 7, 9) for a in (1, 2, 3)]
    uniform += [(4,) * 3, (5,) * 3, (1,) * 11, (2,) * 11]
    nonuniform = [(1, 1, 2), (1, 2, 3), (1, 3, 5), (2, 3, 4),
                  (1, 1, 2, 2, 3), (1, 2, 1, 3, 2),
                  (2, 1, 3, 1, 4), (1, 2, 1, 2, 1, 2, 3)]
    cases = uniform + nonuniform
    full_cones = {(1,) * 3, (1,) * 5, (1,) * 7, (2,) * 3, (2,) * 5,
                  (2,) * 7, (3,) * 3, (1, 2, 3), (1, 1, 2, 2, 3)}
    records = []
    coordinate_audits = parity_audits = 0
    for m in (3, 5, 7, 9, 11):
        inv = inverse_cycle(m)
        for i in range(m):
            for j in range(m):
                require(inv[i][j] == F((-1) ** ((j - i) % m), 2), "inverse mismatch")
            require(sum(inv[i]) == F(1, 2), "inverse row sum")
        if m <= 7:
            for slack in product(range(3), repeat=m):
                for n in (0, 1):
                    point = [F(n, 2) - sum(inv[i][j] * slack[j] for j in range(m))
                             for i in range(m)]
                    integral = all(x.denominator == 1 for x in point)
                    require(integral == ((sum(slack) - n) % 2 == 0), "parity filter")
                    parity_audits += 1
    for widths, maximum_n in [((1, 1, 1), 5), ((1, 2, 1), 4),
                               ((2, 2, 2), 3), ((1,) * 5, 3)]:
        for n in range(maximum_n + 1):
            require(count(widths, n) == coordinate_count(widths, n), "coordinate enumeration")
            coordinate_audits += 1

    for widths in cases:
        m, d = len(widths), sum(widths)
        k = d - m
        denominator = 1
        for a in widths:
            denominator *= factorial(a - 1)
        residual = factorial(k) // denominator
        require(F(factorial(k), denominator) == residual, "multinomial integrality")
        values = [count(widths, n) for n in range(2 * d + 8)]
        even = interpolate(values[:2 * d + 1:2], start=0, step=2)
        odd = interpolate(values[1:2 * d + 2:2], start=1, step=2)
        for n in range(2 * d + 2, len(values)):
            require(evaluate(even if n % 2 == 0 else odd, n) == values[n], "extra dilation")
        length = max(len(even), len(odd))
        even += [F(0)] * (length - len(even))
        odd += [F(0)] * (length - len(odd))
        alternating = trim([(x - y) / 2 for x, y in zip(even, odd)])
        require(len(alternating) == k + 1, "alternating degree")
        require(alternating[-1] == F(1, 2 ** (d + 1) * denominator), "alternating leading coefficient")
        h = trim([sum((-1) ** j * comb(d + 1, j) * values[n - 2 * j]
                      for j in range(min(d + 1, n // 2) + 1)) for n in range(len(values))])
        require(len(h) <= 2 * d + 2, "Ehrhart numerator tail")
        r = h[:]
        for _ in range(m):
            r = divide_plus(r)
        require(evaluate(r, -1) == residual, "exact cyclotomic multiplicity/residual")
        record = {"widths": list(widths), "alternating_degree": k,
                  "alternating_leading": str(alternating[-1]),
                  "root_multiplicity": m, "residual_at_minus_one": residual}
        if widths in full_cones:
            cone = cone_alternating(widths)
            require(cone == alternating, "full cone polynomial differs from even/odd interpolation")
            record["full_cone_polynomial"] = [str(x) for x in cone]
        if len(set(widths)) == 1:
            a, b = widths[0], widths[0] - 1
            degree = 2 * a * (m - 1) + 1
            index = (degree - m) // 2
            require(len(h) == degree + 1 and h == h[::-1], "degree/palindromicity")
            gammas = gamma(h)
            require(gammas[index] == (-1) ** index * residual, "terminal gamma")
            require(not any(gammas[index + 1:]), "gamma tail vanishing")
            if b:
                ratio = F(b * (4 * b + 3) * (m * m - 1), 24 * (m * b - 1))
                require(gammas[index - 1] == (-1) ** (index - 1) * residual * ratio,
                        "penultimate gamma")
                require(gammas[index - 1] * gammas[index] < 0, "opposite terminal signs")
                beta = alternating[-1]
                c = 2 * a + 1
                v = F(m * b * (3 * m - 3 * b - 4 * b * b + 4), 24)
                require(alternating[k - 1] == beta * k * F(c, 2), "central linear term")
                require(alternating[k - 2] == beta * (comb(k, 2) * F(c, 2) ** 2 + v),
                        "central quadratic term")
            record.update({"numerator_degree": degree, "last_gamma_index": index,
                           "last_gamma": gammas[index],
                           "penultimate_gamma": gammas[index - 1] if index else None})
            if (m, a) in ((3, 1), (3, 2), (5, 1), (5, 2), (7, 2)):
                record["gamma_vector"] = gammas
        records.append(record)

    # Prior published width-one numerator controls, not new discoveries.
    for m, expected in [(3, [1, 4, 7, 7, 4, 1]),
                        (5, [1, 11, 51, 131, 206, 206, 131, 51, 11, 1])]:
        values = [count((1,) * m, n) for n in range(len(expected))]
        h = [sum((-1) ** j * comb(m + 1, j) * values[n - 2 * j]
                 for j in range(min(m + 1, n // 2) + 1)) for n in range(len(expected))]
        require(h == expected, "Hamano--Hibi--Ohsugi published control")
    require(cone_alternating((2, 2, 2)) == [F(35, 256), F(39, 256), F(15, 256), F(1, 128)],
            "explicit (3,2) alternating polynomial")
    rejected = 0
    for widths in ((1, 1), (1,) * 4, (1, 0, 1), (1, F(3, 2), 1)):
        try:
            count(widths, 1)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid input accepted")
    return {"status": "PASS", "arithmetic": "exact Python integers and Fraction",
            "parameter_cases": len(cases), "uniform_cases": len(uniform),
            "nonuniform_cases": len(nonuniform), "full_cone_comparisons": len(full_cones),
            "coordinate_enumeration_comparisons": coordinate_audits,
            "slack_parity_comparisons": parity_audits,
            "extra_dilations_checked": 6 * len(cases), "invalid_inputs_rejected": rejected,
            "cases": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare the adjacent EXPECTED.json")
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "EXPECTED.json mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
