#!/usr/bin/env python3
"""Exact all-parameter quartic certificate for symmetric depth-one flaps.

Only Python integers and Fractions are used. See PROOF.md for the reduction.
This does not certify higher degrees, asymmetric weights, or majorisation.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from math import factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def fixture():
    u = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    x, y = list(u), list(u)
    for i in range(4):
        for j in range(4):
            if i != j:
                x.append(tuple(b-a for a, b in zip(u[i], u[j])))
                y.append(tuple(b+a for a, b in zip(u[i], u[j])))
    return x, y


def distances(points):
    return [[sum((a-b)**2 for a, b in zip(p, q)) for q in points] for p in points]


def rational_rank(rows):
    rows = [[Fraction(v) for v in row] for row in rows]
    rank = 0
    for col in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        factor = rows[rank][col]
        rows[rank] = [v/factor for v in rows[rank]]
        for i in range(rank+1, len(rows)):
            factor = rows[i][col]
            rows[i] = [a-factor*b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def ordered_histogram(dx, dy, m):
    """Definition-level replica expansion, all 16**m ordered tuples."""
    result = Counter()
    count = 0
    for labels in product(range(16), repeat=m):
        a = sum(i < 4 for i in labels)
        ex = sum(dx[labels[i]][labels[j]] for i in range(m) for j in range(i))
        ey = sum(dy[labels[i]][labels[j]] for i in range(m) for j in range(i))
        result[a, ey] += 1
        result[a, ex] -= 1
        count += 1
    require(count == 16**m, "ordered enumeration incomplete")
    return {key: v for key, v in result.items() if v}, count


def multiset_histogram(x, y, m):
    """Different enumeration and exponent formula, with exact multiplicities."""
    result = Counter()
    count = 0
    total_multiplicity = 0
    for labels in combinations_with_replacement(range(16), m):
        multiplicity = factorial(m)
        denominator = 1
        for n in Counter(labels).values():
            denominator *= factorial(n)
        require(multiplicity % denominator == 0, "inexact multinomial")
        multiplicity //= denominator
        a = sum(i < 4 for i in labels)
        for sign, points in ((-1, x), (1, y)):
            summed = [sum(points[i][k] for i in labels) for k in range(3)]
            norms = sum(sum(v*v for v in points[i]) for i in labels)
            exponent = m*norms-sum(v*v for v in summed)
            result[a, exponent] += sign*multiplicity
        count += 1
        total_multiplicity += multiplicity
    require(total_multiplicity == 16**m, "multinomial reconstruction incomplete")
    return {key: v for key, v in result.items() if v}, count


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def add(p, q, multiplier=1):
    out = list(p)+[0]*max(0, len(q)-len(p))
    for i, c in enumerate(q):
        out[i] += multiplier*c
    return trim(out)


def multiply(p, q):
    if not p or not q:
        return []
    out = [0]*(len(p)+len(q)-1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                if b:
                    out[i+j] += a*b
    return trim(out)


def replica_polynomial(histogram, m):
    # Return coefficients in the anchor/flap weight ratio, each a polynomial in q.
    rows = [[] for _ in range(m+1)]
    for (a, e), coefficient in histogram.items():
        require(12*e % m == 0, "nonintegral q exponent")
        power = 12*e//m
        if len(rows[a]) <= power:
            rows[a] += [0]*(power+1-len(rows[a]))
        rows[a][power] += coefficient
    return [trim(row) for row in rows]


def multiply_bivariate(p, q):
    out = [[] for _ in range(len(p)+len(q)-1)]
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] = add(out[i+j], multiply(a, b))
    return out


def bernstein_by_binomial(p):
    """Coefficients of (1+t)^d p(t/(1+t)), using the binomial formula."""
    degree = len(p)-1
    out = [0]*(degree+1)
    for j, c in enumerate(p):
        if not c:
            continue
        binomial = 1
        for k in range(degree-j+1):
            out[j+k] += c*binomial
            binomial = binomial*(degree-j-k)//(k+1)
    return trim(out)


def bernstein_by_horner(p):
    """Same transform from homogeneous Horner evaluation; no binomial formula."""
    out = [p[-1]]
    denominator = [1]
    for c in reversed(p[:-1]):
        denominator = add(denominator, [0]+denominator)
        out = add([0]+out, denominator, c)
    return trim(out)


def positive_certificate(name, polynomial):
    p = trim(polynomial)
    require(bool(p), f"{name}: zero polynomial is not the intended certificate")
    zero_order = 0
    while p[0] == 0:
        p = p[1:]
        zero_order += 1
    one_order = 0
    while sum(p) == 0:
        prefix = 0
        quotient = []
        for c in p[:-1]:
            prefix += c
            quotient.append(prefix)
        require(multiply(quotient, [1, -1]) == p, "bad exact factor division")
        p = trim(quotient)
        one_order += 1
    coefficients = bernstein_by_binomial(p)
    require(coefficients == bernstein_by_horner(p), f"{name}: basis transforms disagree")
    require(len(coefficients) == len(p), f"{name}: unexpected degree cancellation")
    require(all(c > 0 for c in coefficients), f"{name}: certificate is not strictly positive")
    return {
        "name": name, "zero_order": zero_order, "one_order": one_order,
        "reduced_degree": len(p)-1, "coefficient_count": len(coefficients),
        "minimum_integer_coefficient": str(min(coefficients)),
        "coefficient_sha256": digest(coefficients),
    }


def verify():
    x, y = fixture()
    dx, dy = distances(x), distances(y)
    deficits = [dx[i][j]-dy[i][j] for i in range(16) for j in range(i)]
    require(min(deficits) >= 0, "fixture is not a contraction")
    rank = rational_rank([[x[i][k]-x[0][k] for k in range(3)] +
                          [y[i][k]-y[0][k] for k in range(3)] for i in range(1, 16)])
    require(rank == 6, "fixture has unexpected paired rank")
    polynomials, summary, compact = {}, [], []
    for m in (2, 3, 4):
        ordered, ordered_count = ordered_histogram(dx, dy, m)
        multiset, multiset_count = multiset_histogram(x, y, m)
        require(ordered == multiset, f"degree {m}: independent replica calculations disagree")
        polynomials[m] = replica_polynomial(ordered, m)
        summary.append({"degree": m, "ordered_tuples": ordered_count,
                        "multisets": multiset_count, "histogram_terms": len(ordered)})
        compact.append([m, [[a, e, c] for (a, e), c in sorted(ordered.items())]])
    p24 = multiply_bivariate(polynomials[2], polynomials[4])
    p33 = multiply_bivariate(polynomials[3], polynomials[3])
    c = [add([81*v for v in a], b, -56) for a, b in zip(p24, p33)]
    require(len(c) == 7 and not c[5] and not c[6], "unexpected weight degree")
    auxiliary = add([4*v for v in multiply(c[1], c[3])], multiply(c[2], c[2]), -1)
    certificates = [positive_certificate(f"C{i}", c[i]) for i in (0, 1, 3, 4)]
    certificates.append(positive_certificate("4*C1*C3-C2^2", auxiliary))
    return {
        "status": "ALL_PARAMETER_QUARTIC_CERTIFICATE_PASS",
        "arithmetic": "Python unbounded integers and exact Fractions; no floating point",
        "pair_count": len(deficits), "positive_deficits": sum(v > 0 for v in deficits),
        "paired_rank": rank, "replica_checks": summary,
        "histogram_sha256": digest(compact), "certificates": certificates,
        "ratio_upper_bound": "4*sqrt(2)/7 < 1 (not claimed optimal)",
        "scope": "Depth-one simplex flaps; every scale, variance, and symmetric weight balance; convex energies of degree at most four only.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare verified result with EXPECTED.json")
    args = parser.parse_args()
    result = verify()
    output = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(output == expected, "expected output mismatch")
    print(output, end="")


if __name__ == "__main__":
    main()
