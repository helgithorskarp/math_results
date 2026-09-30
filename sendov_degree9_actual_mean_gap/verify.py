"""Exact reconstruction of the degree-nine actual-mean gap and radial barrier.

Python 3.11, standard library only. Polynomial arithmetic is over Q[a],
characteristic zero, coefficients in increasing power order, trailing zeros
removed. Gaussian arithmetic is over Q[i]/(i^2+1). No author-module imports,
floating point, root solver, external certificate or ledger is a proof input.
Different algorithms below belong to one author; they are not external review.
"""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from math import comb, factorial
from pathlib import Path
import json
import sys

ZERO = (F(0),)
ONE = (F(1),)
A = (F(0), F(1))
EDGES = tuple(map(F, ("0", "1/4", "1/2", "5/8", "3/4", "7/8", "1")))
POLAR_BERNSTEIN = tuple(map(F, ("8/9", "15/14", "94/75", "41/30",
                              "19/15", "1", "2/3")))
KAPPA = F(256, 32955)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def trim(p):
    out = list(map(F, p))
    while len(out) > 1 and not out[-1]:
        out.pop()
    return tuple(out or [F(0)])


def add(p, q):
    return trim([(p[i] if i < len(p) else F(0)) +
                 (q[i] if i < len(q) else F(0))
                 for i in range(max(len(p), len(q)))])


def scale(p, c):
    return trim([z*c for z in p])


def mul(p, q):
    out = [F(0)]*(len(p)+len(q)-1)
    for i, z in enumerate(p):
        for j, w in enumerate(q):
            out[i+j] += z*w
    return trim(out)


def power(p, k):
    out = ONE
    for _ in range(k):
        out = mul(out, p)
    return out


def affine(p, lo, hi):
    return trim([sum(p[j]*comb(j, k)*lo**(j-k)*(hi-lo)**k
                     for j in range(k, len(p))) for k in range(len(p))])


def bernstein(p, degree):
    require(len(p) <= degree+1, "Bernstein degree too small")
    return tuple(sum(p[j]*F(comb(k, j), comb(degree, j))
                     for j in range(min(k+1, len(p))))
                 for k in range(degree+1))


def inverse(values):
    degree = len(values)-1
    return trim([comb(degree, j)*sum((-1)**(j-k)*comb(j, k)*values[k]
                                   for k in range(j+1))
                 for j in range(degree+1)])


def digest(values):
    data = json.dumps(list(map(str, values)), separators=(",", ":")).encode()
    return sha256(data).hexdigest()


def polynomials():
    delta = add(ONE, scale(A, -1))
    m = add(ONE, scale(mul(power(A, 2), delta), 2))
    g = add(scale(power(add(ONE, A), 2), F(2, 5)),
            scale(mul(power(A, 2), power(m, 3)), -1))
    # Independent binomial expansion of the cubic, with no M^3 convolution.
    other = scale(power(add(ONE, A), 2), F(2, 5))
    for j in range(4):
        other = add(other, scale(mul(power(A, 2+2*j), power(delta, j)),
                                 -comb(3, j)*2**j))
    require(g == other and len(g) == 12, "Complete degree-eleven identity")

    # The polar calculation uses A=a^2 as its independent variable.
    d = delta
    factors = [A, scale(mul(A, d), 2), power(d, 2)]
    cs = [ONE]
    for _ in range(4):
        out = [ZERO]*(len(cs)+2)
        for j, z in enumerate(cs):
            for k, w in enumerate(factors):
                out[j+k] = add(out[j+k], mul(z, w))
        cs = out
    integral = ZERO
    for j, z in enumerate(cs):
        integral = add(integral, scale(z, F(1, j+1)))
    # Separate multinomial integration; compare the complete power polynomial.
    other_integral = ZERO
    for n1 in range(5):
        for n2 in range(5-n1):
            n0 = 4-n1-n2
            coefficient = F(factorial(4)*2**n1,
                            factorial(n0)*factorial(n1)*factorial(n2)*
                            (n1+2*n2+1))
            term = mul(power(A, n0+n1), power(d, n1+2*n2))
            other_integral = add(other_integral, scale(term, coefficient))
    require(integral == other_integral, "Complete independent polar integral")
    q = tuple(map(F, ("8/9", "23/21", "-1/105", "-428/315",
                     "-121/105", "169/105", "-128/315")))
    require(add(ONE, scale(integral, -1)) == mul(power(d, 2), q),
            "Complete polar defect factor identity")
    require(bernstein(q, 6) == POLAR_BERNSTEIN,
            "All seven polar coefficients")
    require(inverse(POLAR_BERNSTEIN) == q, "Complete polar inverse")

    # Back in Q[a], check the rational M identity after clearing (1+a)^2.
    b = add(ONE, scale(power(A, 2), -1))
    lhs = mul(add(add(m, scale(ONE, -1)), scale(mul(power(A, 2), b), -1)),
              power(add(ONE, A), 2))
    require(lhs == mul(power(b, 2), power(A, 2)), "M identity")
    square = power(add(A, scale(ONE, F(-1, 2))), 2)
    require(add(scale(ONE, F(5, 4)), scale(add(A, b), -1)) == square,
            "a+b upper bound square")
    require(add(scale(ONE, F(1, 4)), scale(mul(A, delta), -1)) == square,
            "a(1-a) upper bound square")
    require(F(2, 15)/(4*F(13, 8)**3) == KAPPA,
            "Quantitative margin constant")
    return g, q


GONE = (F(1), F(0))
GZERO = (F(0), F(0))


def gadd(z, w):
    return (z[0]+w[0], z[1]+w[1])


def gmul(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def gscale(z, c):
    return (z[0]*c, z[1]*c)


def gpower(z, k):
    out = GONE
    for _ in range(k):
        out = gmul(out, z)
    return out


def gnorm(z):
    return z[0]**2+z[1]**2


def gaussian_integral(constant, z, w, multiplier):
    cs = [GONE]
    for linear in [z]*4+[w]*4:
        out = [GZERO]*(len(cs)+1)
        for j, value in enumerate(cs):
            out[j] = gadd(out[j], gscale(value, constant))
            out[j+1] = gadd(out[j+1], gmul(value, linear))
        cs = out
    direct = [GZERO]*9
    for i in range(5):
        for j in range(5):
            term = gmul(gpower(z, i), gpower(w, j))
            term = gscale(term, comb(4, i)*comb(4, j)*
                          constant**(8-i-j))
            direct[i+j] = gadd(direct[i+j], term)
    require(cs == direct, "Complete independent Gaussian coefficient vector")
    result = GZERO
    for j, value in enumerate(cs):
        result = gadd(result, gscale(value, F(multiplier, j+1)))
    # Separate double sum, including the integration denominator.
    other = GZERO
    for i in range(5):
        for j in range(5):
            term = gmul(gpower(z, i), gpower(w, j))
            term = gscale(term, F(multiplier*comb(4, i)*comb(4, j), i+j+1)*
                          constant**(8-i-j))
            other = gadd(other, term)
    require(result == other, "Independent Gaussian integration")
    return result


def witness():
    a, h = F(3, 5), F(1, 1000)
    b, r, s = 1-a*a, 1+h, 1-h
    u, v = (F(399, 401), F(40, 401)), (F(15, 17), F(-8, 17))
    require(gnorm(u) == gnorm(v) == 1, "Exact unit directions")
    U, V = gscale(u, r), gscale(v, s)
    xi, xi0 = (U[0]+V[0])/2, (u[0]+v[0])/2
    no = gnorm(gaussian_integral(F(1), gscale(U, -a), gscale(V, -a), 9))
    no /= (r*s)**8
    no0 = gnorm(gaussian_integral(F(1), gscale(u, -a), gscale(v, -a), 9))
    nc = gnorm(gaussian_integral(a, gscale(U, b), gscale(V, b), 1))
    nc0 = gnorm(gaussian_integral(a, gscale(u, b), gscale(v, b), 1))
    slacks = (2*a*U[0]+b*r*r-1, 2*a*V[0]+b*s*s-1)
    balanced_slacks = (2*a*u[0]+b-1, 2*a*v[0]+b-1)
    require(min(r, s) >= 1/(1+a) and r+s == 2, "Radial domain")
    require(min(slacks+balanced_slacks) > 0, "All individual reciprocal disks")
    require(min(xi, xi0) > a+KAPPA*b/a, "Both actual-mean margins")
    require(1 < nc < F(9, 8) and 1 < nc0 < F(9, 8), "Both polar premises")
    require(3 < no < no0 < 4, "Origin norms: not a joint-system witness")
    difference = no-no0
    require(F(-1, 19000) < difference < F(-1, 20000),
            "Strict radial comparison obstruction")
    return {"a": str(a), "h": str(h), "r": str(r), "s": str(s),
            "u": list(map(str, u)), "v": list(map(str, v)),
            "actual_mean": str(xi), "balanced_mean": str(xi0),
            "disk_slacks": list(map(str, slacks)),
            "balanced_disk_slacks": list(map(str, balanced_slacks)),
            "normalized_origin_squared": str(no),
            "balanced_origin_squared": str(no0),
            "polar_squared": str(nc), "balanced_polar_squared": str(nc0),
            "origin_squared_difference": str(difference)}


def validate_cells(records, g):
    require(len(records) == len(EDGES)-1, "Complete cell count")
    for j, row in enumerate(records):
        lo, hi = EDGES[j:j+2]
        require(row["interval"] == [str(lo), str(hi)], "Complete cell coverage")
        require(row["degree"] == 11, "Exact degree")
        values = tuple(map(F, row["coefficients"]))
        require(len(values) == 12 and min(values) > 0,
                "All twelve strictly positive coefficients")
        local = affine(g, lo, hi)
        require(inverse(values) == local, "Full cell inverse identity")
        require(values == bernstein(local, 11), "Entry-level cell reconstruction")
        require(row["minimum"] == str(min(values)), "Exact cell minimum")
        require(row["sha256"] == digest(values), "Canonical cell digest")


def make_manifest():
    g, q = polynomials()
    records = []
    for lo, hi in zip(EDGES, EDGES[1:]):
        values = bernstein(affine(g, lo, hi), 11)
        records.append({"interval": [str(lo), str(hi)], "degree": 11,
                        "coefficients": list(map(str, values)),
                        "minimum": str(min(values)), "sha256": digest(values)})
    validate_cells(records, g)
    return {"schema": "six-sendov-1-actual-mean-gap-v1",
            "coefficient_domain": "Q[a] and Q[i]/(i^2+1), characteristic zero",
            "g_power_coefficients": list(map(str, g)),
            "g_cells": records, "polar_q_power_coefficients": list(map(str, q)),
            "polar_q_bernstein": list(map(str, POLAR_BERNSTEIN)),
            "kappa": str(KAPPA), "witness": witness()}


def check_manifest(candidate, correct):
    g, _ = polynomials()
    validate_cells(candidate["g_cells"], g)
    require(candidate == correct, "Complete manifest entry comparison")


def mutations(correct):
    cases = []
    bad = deepcopy(correct)
    bad["g_cells"].pop()
    cases.append(bad)
    bad = deepcopy(correct)
    bad["g_cells"][1]["interval"] = bad["g_cells"][0]["interval"]
    cases.append(bad)
    bad = deepcopy(correct)
    bad["g_cells"][0]["degree"] = 10
    cases.append(bad)
    bad = deepcopy(correct)
    bad["g_cells"][0]["coefficients"][2] = "-1"
    cases.append(bad)
    bad = deepcopy(correct)
    bad["g_cells"][0]["coefficients"][2] = str(
        F(bad["g_cells"][0]["coefficients"][2])+F(1, 1000))
    cases.append(bad)
    bad = deepcopy(correct)
    bad["witness"]["origin_squared_difference"] = "1/20000"
    cases.append(bad)
    for bad in cases:
        try:
            check_manifest(bad, correct)
        except (ArithmeticError, KeyError, ValueError, TypeError):
            continue
        raise ArithmeticError("Invalid proof manifest was accepted")
    return len(cases)


def main():
    correct = make_manifest()
    if sys.argv[1:] == ["--emit"]:
        print(json.dumps(correct, indent=2))
        return
    require(not sys.argv[1:], "Usage: python3 verify.py [--emit]")
    expected = json.loads(Path(__file__).with_name("expected.json").read_text())
    check_manifest(expected, correct)
    rejected = mutations(correct)
    summary = {"status": "PASS: exact reconstruction, not independent review",
               "strictly_positive_bernstein_entries": 79,
               "complete_inverse_basis_identities": 7,
               "independent_polar_integrals": 1,
               "independent_degree_eleven_identities": 1,
               "independent_gaussian_integral_vectors": 4,
               "rejected_mutations": rejected, "kappa": str(KAPPA),
               "witness_difference_interval": ["-1/19000", "-1/20000"],
               "manifest_sha256": sha256(json.dumps(
                   correct, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
