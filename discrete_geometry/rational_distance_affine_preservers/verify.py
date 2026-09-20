"""Exact corroboration of the affine-preserver proof; Python 3.11+, stdlib.

All field operations are rational, in Q[c]/(c^4-c^2+1/8), c=cos(pi/8).
No finite computation here proves the imported density theorems.
"""
from fractions import Fraction as Q
from itertools import product
from math import isqrt
from collections import Counter
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def E(*coeffs):
    require(len(coeffs) <= 4, "field coefficient count")
    return tuple(Q(x) for x in coeffs) + (Q(0),) * (4 - len(coeffs))


ZERO, ONE = E(0), E(1)
C = E(0, 1)


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def times(a, b):
    c = [Q(0)] * 7
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    # c^4 = c^2 - 1/8, reduced from the highest power downward.
    for k in range(6, 3, -1):
        c[k-2] += c[k]
        c[k-4] -= c[k]/8
    return tuple(c[:4])


def mul_scalar(a, x):
    return tuple(Q(x)*y for y in a)


def rational(a):
    return all(x == 0 for x in a[1:])


def matrix(a, b, c, d):
    return [[E(a), E(b)], [E(c), E(d)]]


def transpose(M):
    return [list(row) for row in zip(*M)]


def matmul(A, B):
    return [[plus(times(A[i][0], B[0][j]), times(A[i][1], B[1][j]))
             for j in range(2)] for i in range(2)]


def gram(B):
    return matmul(transpose(B), B)


def serial(M):
    return [[[str(x) for x in cell] for cell in row] for row in M]


SQRT2 = plus(mul_scalar(times(C, C), 4), E(-2))
SIN = plus(mul_scalar(times(times(C, C), C), 4), mul_scalar(C, -3))
ROT = [[C, neg(SIN)], [SIN, C]]
IDENTITY = matrix(1, 0, 0, 1)


def predicted_conjugate(a, b, c):
    t = E(Q(a+c, 2))
    delta = mul_scalar(SQRT2, Q(a-c+2*b, 4))
    off = mul_scalar(SQRT2, Q(c-a+2*b, 4))
    return [[plus(t, delta), off], [off, plus(t, neg(delta))]]


def prime(p):
    return p >= 2 and all(p % k for k in range(2, isqrt(p)+1))


def factor(n):
    require(n >= 1, "positive factor input")
    out = Counter()
    d = 2
    while d*d <= n:
        while n % d == 0:
            out[d] += 1
            n //= d
        d += 1
    if n > 1:
        out[n] += 1
    return out


def valuation_integer(n, p):
    require(n != 0 and prime(p), "valuation domain")
    n, v = abs(n), 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def valuation(a, p):
    return valuation_integer(a.numerator, p) - valuation_integer(a.denominator, p)


def rational_square(a):
    return a > 0 and isqrt(a.numerator)**2 == a.numerator and \
        isqrt(a.denominator)**2 == a.denominator


def obstruction(alpha):
    require(alpha > 0 and not rational_square(alpha), "positive nonsquare required")
    ps = sorted(set(factor(alpha.numerator)) | set(factor(alpha.denominator)))
    p = next(p for p in ps if valuation(alpha, p) % 2)
    d = 3 if p == 2 else next(d for d in range(1, p)
                             if pow(-d, (p-1)//2, p) == p-1)
    return p, d


def certificate_valid(alpha, p, d):
    if alpha <= 0 or not prime(p) or valuation(alpha, p) % 2 != 1:
        return False
    if p == 2:
        return d == 3
    return 0 < d < p and (-d) % p not in {x*x % p for x in range(p)}


def local_norm_audit(p, d):
    """Independent residue check behind the valuation proof."""
    if p == 2:
        pairs = [(x, y) for x, y in product(range(16), repeat=2) if (x % 2 or y % 2)]
        for x, y in pairs:
            v = valuation_integer(x*x + d*y*y, p)
            require(v in (0, 2), "dyadic primitive norm valuation")
        return len(pairs)
    zeros = [(x, y) for x, y in product(range(p), repeat=2)
             if (x*x+d*y*y) % p == 0]
    require(zeros == [(0, 0)], "odd-prime anisotropy")
    return p*p


def main():
    require(times(SQRT2, SQRT2) == E(2), "quadratic subfield")
    require(gram(ROT) == IDENTITY, "exact orthogonal rotation")
    require(times(C, SIN) == mul_scalar(SQRT2, Q(1, 4)), "double-angle identity")

    digest = hashlib.sha256()
    matrices = scalar = 0
    # Direct physical image coordinates, independently compared to formula (2).
    for a, b, c, d in product(range(-2, 3), repeat=4):
        if a*d == b*c:
            continue
        A = matrix(a, b, c, d)
        s, t, u = a*a+c*c, a*b+c*d, b*b+d*d
        got = gram(matmul(A, ROT))
        want = predicted_conjugate(s, t, u)
        require(got == want, "direct Gram vs conjugation identity")
        is_scalar = s == u and t == 0
        require(all(rational(x) for row in got for x in row) == is_scalar,
                "two-test scalar rigidity")
        scalar += is_scalar
        matrices += 1
        digest.update(json.dumps([[a, b, c, d], serial(got)], separators=(",", ":")).encode())

    # The displayed rational anisotropy example.
    bad = gram(matmul(matrix(2, 0, 0, 1), ROT))
    expected_bad = [[plus(E(Q(5, 2)), mul_scalar(SQRT2, Q(3, 4))),
                     mul_scalar(SQRT2, Q(-3, 4))],
                    [mul_scalar(SQRT2, Q(-3, 4)),
                     plus(E(Q(5, 2)), mul_scalar(SQRT2, Q(-3, 4)))]]
    require(bad == expected_bad and not rational(bad[0][0]), "anisotropic counterexample")
    # A nonrational initial Gram fails already on the first test.
    require(not rational(gram([[C, ZERO], [ZERO, ONE]])[0][0]), "first-test boundary")
    # Arbitrary real orthogonal maps are allowed: ROT is an exact such example.
    require(gram(ROT) == IDENTITY, "irrational rotation positive control")

    alphas = sorted({Q(a, b) for a, b in product(range(1, 25), repeat=2)})
    local = {}
    certificates = []
    positive = 0
    norm_samples = 0
    for alpha in alphas:
        if rational_square(alpha):
            r = Q(isqrt(alpha.numerator), isqrt(alpha.denominator))
            require(r*r == alpha, "rational scale")
            positive += 1
            continue
        p, d = obstruction(alpha)
        require(certificate_valid(alpha, p, d), "bad norm certificate")
        if (p, d) not in local:
            local[p, d] = local_norm_audit(p, d)
            for x, y in product(range(-12, 13), repeat=2):
                if x or y:
                    require(valuation_integer(x*x+d*y*y, p) % 2 == 0,
                            "integer norm sample")
                    norm_samples += 1
        # Negative valuations matter: denominators are not discarded.
        certificates.append([str(alpha), p, d, valuation(alpha, p)])
    require(any(row[3] < 0 for row in certificates), "denominator coverage")

    # Independent homogeneous certificates for 2*x^2+6*y^2=1.
    # A rational solution would clear to primitive integers 2X^2+6Y^2=Z^2.
    residue_counts = {}
    for modulus, p in [(9, 3), (16, 2)]:
        survivors = [(x, y, z) for x, y, z in product(range(modulus), repeat=3)
                     if (x % p or y % p or z % p)
                     and (2*x*x+6*y*y-z*z) % modulus == 0]
        require(not survivors, "primitive local solution in scale-sqrt2 example")
        residue_counts[str(modulus)] = len(survivors)
    require(2*(Q(1, 2)**2 + Q(1, 2)**2) == 1, "two fixed tests alone are insufficient")

    invalid = [(Q(2), 2, 1), (Q(4), 2, 3), (Q(3), 3, 2), (Q(3), 9, 1)]
    require(all(not certificate_valid(*row) for row in invalid), "invalid certificate accepted")
    rejected = 0
    for alpha in [Q(0), Q(-2), Q(1), Q(4, 9)]:
        try:
            obstruction(alpha)
        except ValueError:
            rejected += 1
    require(rejected == 4, "invalid scale accepted")
    print(json.dumps({
        "status": "VERIFIED",
        "matrix_cases": matrices,
        "scalar_cases": scalar,
        "anisotropic_cases": matrices-scalar,
        "matrix_record_sha256": digest.hexdigest(),
        "rational_squared_scales": len(alphas),
        "rational_scale_positive_controls": positive,
        "nonsquare_scale_certificates": len(certificates),
        "negative_valuation_certificates": sum(row[3] < 0 for row in certificates),
        "scale_certificate_sha256": hashlib.sha256(json.dumps(certificates, separators=(",", ":")).encode()).hexdigest(),
        "local_norm_certificates": [{"p": p, "d": d, "residue_pairs": n}
                                    for (p, d), n in sorted(local.items())],
        "integer_norm_samples": norm_samples,
        "sqrt2_example_primitive_residue_survivors": residue_counts,
        "invalid_certificates_rejected": len(invalid),
        "invalid_scale_inputs_rejected": rejected,
        "trust_boundary": "Exact finite corroboration only; universal group classification is proved in PROOF.md and uses CTZ density criteria."
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
