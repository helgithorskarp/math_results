"""Exact supporting controls for the written all-order cubic-region proof.

CPython 3.11+, standard library. No Gaussian quadrature or solver is used.
Finite controls do not prove the theorem's universal analytic quantifiers.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    out = [F(0)] * max(len(a), len(b))
    for p in (a, b):
        for i, v in enumerate(p):
            out[i] += v
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def scale(a, x):
    return [x * v for v in a]


def derivative(a):
    return [(i + 1) * a[i + 1] for i in range(len(a) - 1)] or [F(0)]


def rising(a, n):
    out = F(1)
    for i in range(n):
        out *= a + i
    return out


def value(a, x):
    out = F(0)
    for v in reversed(a):
        out = out * x + v
    return out


def gamma_shift(a, shape):
    """Polynomial in c equal to E a(c+Gamma(shape,1))."""
    out = [F(0)] * len(a)
    for i, coefficient in enumerate(a):
        for c_power in range(i + 1):
            out[c_power] += coefficient * comb(i, c_power) * rising(shape, i - c_power)
    return out


def nonnegative_coefficients(a, label):
    require(all(x >= 0 for x in a), label)


def beta_certificate(base, order):
    for x in (base, order):
        require(type(x) is int, "indices must be integers, not booleans")
    require(base >= 2 and order >= 1, "base>=2 and order>=1 required")
    threshold = 30720 * order ** 3
    return {
        "base": base,
        "order": order,
        "j": base - 2,
        "N": base - 2 + order,
        "required_base": threshold,
        "status": "CUBIC_REGION_CERTIFIED" if base >= threshold else "NOT_COVERED",
        "scope": "conditional on the bounded R3 contraction hypotheses; NOT_COVERED is not a negative sign",
    }


def normal_moment(mean, n):
    out = F(0)
    for j in range(n // 2 + 1):
        even = factorial(2 * j) // (2 ** j * factorial(j))
        out += comb(n, 2 * j) * mean ** (n - 2 * j) * even
    return out


def radial_normal_moments(means, order):
    """Direct coordinate Wick calculation of (|G+means|^2/2)^n."""
    moments = [F(1)] + [F(0)] * order
    for mean in means:
        coordinate = [normal_moment(mean, 2 * n) / 2 ** n for n in range(order + 1)]
        moments = [sum(F(comb(n, j)) * moments[j] * coordinate[n - j]
                       for j in range(n + 1)) for n in range(order + 1)]
    return moments


def poisson_moments(lam, order):
    rows = [[1]]
    answer = [F(1)]
    for n in range(1, order + 1):
        old = rows[-1]
        row = [0] * (n + 1)
        for k in range(1, n + 1):
            row[k] = (old[k - 1] if k - 1 < len(old) else 0)
            row[k] += k * (old[k] if k < len(old) else 0)
        rows.append(row)
        answer.append(sum(F(v) * lam ** k for k, v in enumerate(row)))
    return answer


def audit():
    polynomials = [[F(1)]]
    polynomial_records = []
    constant_controls = 0
    normalization_controls = 0
    for k in range(1, 25):
        direct = [F(0)] * (k + 1)
        falling = F(1)
        for ell in range(k + 1):
            if ell:
                falling *= F(1, 2) - (ell - 1)
            direct[k - ell] = comb(k, ell) * (-1) ** ell * falling
            if ell:
                require(abs(falling) <= F(factorial(ell - 1), 2), "falling bound")
                require(comb(k, ell) * abs(falling) <= F(k ** ell, 2 * ell), "coefficient bound")
        previous = polynomials[-1]
        recurrence = add([F(0)] + previous, scale(previous, k - F(3, 2)))
        recurrence = add(recurrence, [F(0)] + scale(derivative(previous), -1))
        require(direct == recurrence, "Appell recurrence mismatch")
        require(derivative(direct) == scale(previous, k), "Appell derivative mismatch")
        require(all(v < 0 for v in direct[:-1]) and direct[-1] == 1, "h coefficient signs")
        require(value(direct, 2 * k) >= F((2 * k) ** k, 2), "positive-region bound")
        polynomials.append(direct)
        P = list(map(abs, direct))
        G = gamma_shift(direct, F(3))
        expected_G = [F(comb(k, j)) * rising(F(5, 2), k - j) for j in range(k + 1)]
        require(G == expected_G, "Gamma calibration polynomial")
        raw = [F(comb(k, j)) * rising(F(3), k - j) for j in range(k + 1)]
        nonnegative_coefficients(add(scale(G, k + 1), scale(raw, -1)), "raw/G comparison")
        old_G = gamma_shift(previous, F(3))
        nonnegative_coefficients(add(G, scale(old_G, -k)), "G/previous comparison")
        EP = gamma_shift(P, F(3))
        EPprime = gamma_shift(derivative(P), F(3))
        nonnegative_coefficients(add(scale(G, 2 * k + 1), scale(EP, -1)), "P expectation bound")
        nonnegative_coefficients(add(scale(G, 2 * k - 1), scale(EPprime, -1)), "P derivative expectation bound")
        V0 = 32 * k
        for multiplier in (1, 2, 17):
            r = multiplier * 30720 * k ** 3
            epsilon = F(24 * k, r)
            tau = epsilon * V0
            require(r >= 8 * k and F(64 * k, r) <= 1 and F(2 * k, r) <= 1, "localization guard")
            require(tau <= F(1, 40 * k) <= 1, "Taylor guard")
            require(tau * (10 * k - 1) <= F(1, 4), "integrated error guard")
            correction = add(scale(derivative(P), 3), scale(P, 2))
            minorant = add(direct, scale(correction, -tau))
            require(minorant[-1] > 0 and all(v < 0 for v in minorant[:-1]), "one-crossing coefficients")
            Eminorant = gamma_shift(minorant, F(3))
            nonnegative_coefficients(add(Eminorant, scale(G, -F(3, 4))), "untruncated margin")
            tail_ratio = F(2 ** (2 * k + 2) * (k + 1) * (k + 2), 2 ** (16 * k))
            require(tail_ratio <= F(1, 2 ** (12 * k - 3)) <= F(1, 512), "tail bound")
            constant_controls += 1
        # Complete the pair Gaussian square by direct exponent expansion.
        # rho=1/sqrt(r) is rational. These controls audit identity (19).
        rho = F(1, 1 + 30720 * k ** 3)
        r = 1 / rho ** 2
        for shift in (0, 1, 3):
            x = [F(i - 2, 3) for i in range(6)]
            A = [F((i + shift) % 5 - 2, 2) for i in range(6)]
            B = [F((2 * i + shift) % 7 - 3, 3) for i in range(6)]
            v = sum(t * t for t in x) / 2
            left = -sum((rho * t - a) ** 2 + (rho * t - b) ** 2
                        for t, a, b in zip(x, A, B)) / 2 - (r - 2) * v / r
            right = -sum(a * a + b * b for a, b in zip(A, B)) / 2 - v
            right += rho * sum((a + b) * t for t, a, b in zip(x, A, B))
            require(left == right, "Gaussian pair normalization")
            normalization_controls += 1
        polynomial_records.append({"k": k, "h": list(map(str, direct)), "G": list(map(str, G))})

    # Independent calibration: coordinate Gaussian moments versus the
    # Poisson/Gamma noncentral radial representation, through order twelve.
    shifts = [[F(0)] * 6, [F(1, 3)] + [F(0)] * 5,
              [F(v, 5) for v in (1, 2, 3, 1, 0, -2)]]
    noncentral_controls = 0
    for a in shifts:
        radial = radial_normal_moments(a, 12)
        lam = sum(v * v for v in a) / 2
        poisson = poisson_moments(lam, 12)
        for k in range(1, 13):
            direct = sum(c * radial[j] for j, c in enumerate(polynomials[k]))
            in_J = [F(1)]
            for j in range(k):
                in_J = mul(in_J, [F(5, 2) + j, F(1)])
            other = sum(c * poisson[j] for j, c in enumerate(in_J))
            require(direct == other > 0, "noncentral Gaussian calibration")
            noncentral_controls += 1

    negative_controls = 0
    for args in [(True, 8), (2, False), (1, 8), (2, 0), (-1, 2), (F(2), 3)]:
        try:
            beta_certificate(*args)
        except ValueError:
            negative_controls += 1
        else:
            raise ValueError("malformed indices accepted")
    for k in (1, 8, 12, 1000):
        edge = 30720 * k ** 3
        require(beta_certificate(edge, k)["status"] == "CUBIC_REGION_CERTIFIED", "boundary rejected")
        require(beta_certificate(edge - 1, k)["status"] == "NOT_COVERED", "unproved boundary accepted")
        negative_controls += 1
    bad_tau = F(1, 2)
    require(1 - 2 * bad_tau <= 0, "bad one-crossing guard not rejected")
    negative_controls += 1
    require(F(1, 4) - F(1, 2) < 0, "dimension-changing negative calibration")
    negative_controls += 1

    digest = hashlib.sha256(json.dumps(polynomial_records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "status": "CUBIC_BETA_ANALYTIC_CONTROLS_PASS",
        "polynomial_orders_checked": 24,
        "constant_guard_controls": constant_controls,
        "Gaussian_product_controls": normalization_controls,
        "independent_noncentral_calibrations": noncentral_controls,
        "negative_and_boundary_controls": negative_controls,
        "polynomial_record_sha256": digest,
        "eighth_order_minimum_base": 30720 * 8 ** 3,
        "eighth_order_minimum_j": 30720 * 8 ** 3 - 2,
        "h8_coefficients_ascending": list(map(str, polynomials[8])),
        "Gamma3_h8_expectation": str(rising(F(5, 2), 8)),
        "scope": "finite exact controls for a written all-order proof; no quadrature, solver, formalization or independent review",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="emit the exact audit record without reading EXPECTED.json")
    parser.add_argument("--base", type=int)
    parser.add_argument("--order", type=int)
    args = parser.parse_args()
    if args.base is not None or args.order is not None:
        require(args.base is not None and args.order is not None and not args.emit,
                "use --base and --order together, without --emit")
        record = beta_certificate(args.base, args.order)
    else:
        record = audit()
        if not args.emit:
            expected = json.loads((ROOT / "EXPECTED.json").read_text())
            require(record == expected, "expected record mismatch")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
