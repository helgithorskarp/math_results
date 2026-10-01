"""Independent audit of graph9091: row-count completion and coefficient proof.

No researcher executable, expected.json or CAS is imported. Published formulas
are inputs checked against separately constructed physical forms and identities.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb, factorial
import hashlib
import json
import sys
from pathlib import Path

from polynomial import P, from_coefficients, shift_coefficients


def check(condition, label):
    if not condition:
        raise ValueError(label)


def choose(n, r):
    return comb(n, r) if 0 <= r <= n else 0


def complete(n, deficits=None):
    """Solve the two counts in each row; do not use the author's low formulas."""
    deficits = deficits or {}
    check(all(type(k) is int and 3 <= k <= n // 2 and type(v) in (int, F)
              for k, v in deficits.items()), "invalid complement coordinate")
    T, s, R = 2 ** (n - 1), 2 ** (n - 1) - n, 2 ** (n - 1) - 2
    beta = [[F() for _ in range(n - 1)] for _ in range(n - 1)]
    for a in range(3, n - 2):
        b = n - a
        beta[a][b] = F(s) - deficits.get(min(a, b), 0)
        beta[a][2] = (b * s - R - (b - 1) * beta[a][b]) / choose(b, 2)
        beta[a][1] = (R - choose(b, 2) * beta[a][2] - beta[a][b]) / b
        beta[1][a], beta[2][a] = beta[a][1], beta[a][2]
    a = n - 2
    beta[a][2] = F(2 * s - R)
    beta[a][1] = F(R - s)
    beta[1][a], beta[2][a] = beta[a][1], beta[a][2]
    high_r = sum(beta[2][b] * choose(n - 2, b) for b in range(3, n - 1))
    high_t = sum(b * beta[2][b] * choose(n - 2, b) for b in range(3, n - 1))
    beta[2][2] = ((n - 2) * s - high_t - R + high_r) / choose(n - 2, 2)
    beta[1][2] = beta[2][1] = (R - high_r - choose(n - 2, 2) * beta[2][2]) / (n - 2)
    beta[1][1] = (R - sum(beta[1][b] * choose(n - 1, b)
                         for b in range(2, n - 1))) / (n - 1)
    for a in range(1, n - 1):
        check(sum(beta[a][b] * choose(n - a, b) for b in range(1, n - 1)) == R,
              "centering count")
        check(sum(b * beta[a][b] * choose(n - a, b) for b in range(1, n - 1)) == (n - a) * s,
              "star count")
        for b in range(1, n - 1):
            check(beta[a][b] == beta[b][a], "symmetric completion")
    return beta


def upper_forms(n, beta):
    """Direct disjoint counting on layer constants and point differences."""
    t = 2 ** (n - 1) - 1
    return [[[F(choose(n - 2 * j, a - j)) *
               (t * int(a == b) + (-1) ** (j + 1) * beta[a][b] * choose(n - a - j, b - j))
               for b in range(1, n - 1)] for a in range(1, n - 1)] for j in (0, 1)]


def matvec(matrix, v):
    return [sum(c * x for c, x in zip(row, v)) for row in matrix]


def energy(matrix, v):
    return sum(x * y for x, y in zip(v, matvec(matrix, v)))


def profiles(n):
    eta, k = F(2 * n * n + 6, n * n), F(2 * n + 3, n)
    p0, p1 = [], []
    for a in range(1, n - 1):
        if a == 1:
            p0.append(eta - k); p1.append(F())
        elif a == 2 or a == n - 2:
            p0.append(2 * eta - k); p1.append(F(1 if a == 2 else -1))
        else:
            d, x = 2 * a - n, (2 * a - n) ** 2
            V = n * n * (3 * n - 4) ** 2 + 8 * (3 * n - 2) * x
            Z = 43 * n ** 4 + 32 * n * n * x - 48 * n * n + 48 * x
            Y = 24 * n ** 5 - 107 * n ** 4 + 136 * n ** 3 + 32 * n * n * x - 48 * n * n + 48 * x
            p0.append(F(-x * Z, n ** 3 * V))
            p1.append(F(2 * d * Y, n ** 3 * V))
    return p0, p1


def scalar(n):
    T, eta, k = 2 ** (n - 1), F(2 * n * n + 6, n * n), F(2 * n + 3, n)
    K0 = n * (-T * n + 2 * T + 5 * n * n - 9 * n + 3)
    K1 = 2 * (n - 2) * (2 * T * n - 4 * T + 2 * n ** 3 - 9 * n * n + 7 * n + 4)
    result = eta ** 2 * K0 + K1 - 2 * k * n * (2 * n - 1) * eta + k ** 2 * n * n
    for a in range(3, n - 2):
        x = (2 * a - n) ** 2
        A1 = n * n * (32 * n ** 5 + 16 * n ** 4 + 97 * n ** 3 - 571 * n * n - 264 * n + 720)
        A2 = 8 * (2 * n * n + 3) * (4 * n ** 3 - 13 * n * n + 11 * n - 30)
        V = n * n * (3 * n - 4) ** 2 + 8 * (3 * n - 2) * x
        result += comb(n, a) * ((n - 2) * k * k - F(x * (A1 + A2 * x), n ** 4 * V))
    return result


def literal_control(n):
    """Use masks on every original vertex; allocate only n6/7 controls."""
    beta, T = complete(n), 2 ** (n - 1)
    s, N = T - n, 2 * T - n - 1
    masks = [v for v in range(1 << n) if v.bit_count() <= n - 2]
    check(len(masks) == N and masks[0] == 0, "literal domain")
    sizes = [v.bit_count() for v in masks]
    L = [[F(1) if not A or not B else
          F(s * int(A == B)) + (beta[sizes[i]][sizes[j]] if not A & B else 0)
          for j, B in enumerate(masks)] for i, A in enumerate(masks)]
    check(all(sum(row) == N for row in L), "full rows")
    M = [[(L[i][j] - s * int(i == j)) / (N - s)
          for j in range(N)] for i in range(N)]
    check(M[0][0] == F(1 - s, N - s), "retained empty loop")
    check(all(M[i][j] == 0 for i, A in enumerate(masks)
              for j, B in enumerate(masks) if A & B), "original intersection support")
    check(all(sum(L[i][j] for j, B in enumerate(masks) if B >> point & 1) == s
              for point in range(n) for i in range(N)), "all original stars")
    U = [[N * int(i == j) - L[i][j] for j in range(N)] for i in range(N)]
    B0, B1 = upper_forms(n, beta)
    for j, B in enumerate([B0, B1]):
        vs = [[F(int(a == r) * (1 if j == 0 else ((A & 1) - ((A >> 1) & 1))))
               for A, a in zip(masks, sizes)] for r in range(1, n - 1)]
        acts = [matvec(U, v) for v in vs]
        for a in range(n - 2):
            for b in range(n - 2):
                check(sum(v * u for v, u in zip(vs[a], acts[b])) == (1 if j == 0 else 2) * B[a][b],
                      "literal physical form metric")
    return {"n": n, "N": N, "empty_loop": str(M[0][0]), "compressed_entries": 2 * (n - 2) ** 2}


def half_partitions(k, smallest=1):
    if not k:
        yield []
    for j in range(smallest, k + 1):
        for rest in half_partitions(k - j, j):
            yield [j] + rest


def moment_polynomial(k):
    n = P.variable("n")
    result = P()
    for shape in half_partitions(k):
        den = 1
        for j in shape:
            den *= factorial(2 * j)
        for j in set(shape):
            den *= factorial(shape.count(j))
        weight = F(factorial(2 * k), den)
        falling = P(1)
        for j in range(len(shape)):
            falling *= n - j
        result += weight * falling
    return result


def universal_identities():
    n, x, T, a = (P.variable(v) for v in P.names)
    h = 3 * n - 4
    A, B = n ** 2 * h ** 2, 8 * (3 * n - 2)
    V = A + B * x
    Z = 43 * n ** 4 + 32 * n ** 2 * x - 48 * n ** 2 + 48 * x
    Y = 24 * n ** 5 - 107 * n ** 4 + 136 * n ** 3 + 32 * n ** 2 * x - 48 * n ** 2 + 48 * x
    U = -x * Z + (2 * n + 3) * n ** 2 * V
    A1 = n ** 2 * (32 * n ** 5 + 16 * n ** 4 + 97 * n ** 3 - 571 * n ** 2 - 264 * n + 720)
    A2 = 8 * (2 * n ** 2 + 3) * (4 * n ** 3 - 13 * n ** 2 + 11 * n - 30)
    d = 2 * a - n
    Va, Ya, Ua = (q.substitute("x", d ** 2) for q in (V, Y, U))
    left = (3 * n ** 2 - 8 * (n - a)) * (2 * a * d * Ya - 2 * (a - 1) * n ** 3 * Va)
    right = (3 * n ** 2 - 8 * a) * (Ua - (2 * n ** 2 + 6) * a * n * Va)
    left.require_equal(right, "universal rational profile relation")
    physical = ((n - 1) * (U ** 2 + (n ** 2 - x) * x * Y ** 2)
                - 4 * (n - 2) * x * Y * n ** 3 * V
                - 2 * (2 * n + 3) * U * n ** 2 * V + (2 * n + 3) ** 2 * n ** 4 * V ** 2)
    simplified = (n - 2) * (2 * n + 3) ** 2 * n ** 4 * V ** 2 - x * (A1 + A2 * x) * n ** 2 * V
    physical.require_equal(simplified, "universal scalar energy reduction")
    # Low coefficients transcribed from the statement, checked from binomial tails.
    b11 = T * n ** 2 - 9 * T * n + 16 * T - n ** 3 + 9 * n ** 2 - 8 * n - 16
    b12 = 2 * (-T * n + 4 * T + 2 * n ** 2 - 4 * n - 4)
    b22 = -4 * (-T * n + 2 * T + 2 * n ** 2 - 2 * n - 2)
    D, s, R = n * (n - 1), T - n, T - 2
    tail0, tail1 = 2 * T - 2 - 2 * n - F(1, 2) * D, n * T - 2 * n ** 2
    (b11 + F(1, 2) * (n - 2) * b12 + 2 * (n - 2) * tail0).require_equal(n * R, "row1")
    (b11 + (n - 2) * b12 + 2 * (n - 2) * tail1).require_equal(D * s, "star1")
    ((n - 2) * b12 + F(1, 2) * (n - 2) * b22 - 2 * (n - 2) * tail0 + s * D).require_equal(R * D, "row2")
    ((n - 2) * b12 + (n - 2) * b22 - 2 * (n - 2) * tail1).require_equal(0, "star2")
    g2 = F(1, 2) * D
    # Physical three-boundary-layer energy, after denominator cancellation.
    K0 = (n * (T - 1) - b11 + 4 * (g2 * (T - 1) - F(1, 4) * (n - 2) * b22)
          + 4 * g2 * (T - 1) - 2 * (n - 2) * b12
          - 4 * n * (n - 1) * (n - 2) - 8 * g2 * (s - n + 2))
    K1 = 2 * D * (n - 2) * (2 * n - 3) + (n - 2) * b22
    K0.require_equal(n * (-T * n + 2 * T + 5 * n ** 2 - 9 * n + 3), "low physical K0")
    K1.require_equal(2 * (n - 2) * (2 * T * n - 4 * T + 2 * n ** 3 - 9 * n ** 2 + 7 * n + 4), "low physical K1")
    mus = [moment_polynomial(j) for j in range(4)]
    expected_moments = [P(1), n, 3 * n ** 2 - 2 * n, 15 * n ** 3 - 30 * n ** 2 + 16 * n]
    for mu, expected in zip(mus, expected_moments):
        mu.require_equal(expected, "independent sign-partition moment")
    S = [2 * T * mu - 2 * n ** (2 * j) - 2 * n * (n - 2) ** (2 * j)
         - n * (n - 1) * (n - 4) ** (2 * j) for j, mu in enumerate(mus)]
    # Reconstruct numerator from the tangent bound, not from supplied P,Q.
    numerator = ((2 * n ** 2 + 6) ** 2 * K0 * n ** 3 * h ** 4
                 + K1 * n ** 7 * h ** 4
                 - 2 * (2 * n + 3) * (2 * n - 1) * (2 * n ** 2 + 6) * n ** 5 * h ** 4
                 + (2 * n + 3) ** 2 * n ** 7 * h ** 4
                 + (n - 2) * (2 * n + 3) ** 2 * S[0] * n ** 5 * h ** 4
                 - (A1 * S[1] + A2 * S[2]) * n * h ** 2
                 + (B * (A1 * S[2] + A2 * S[3])).divide_n())
    derived_P = -F(1, 2) * numerator.coefficient("T", 1)
    derived_Q = numerator.coefficient("T", 0)
    numerator.require_equal(-2 * T * derived_P + derived_Q, "linear T dependence")
    published_P = from_coefficients([-184320, 689664, -1122048, 1266560, -1084736, 590848,
                                    -249184, 128416, -22367, -5875, 375, 288])
    published_Q = from_coefficients([45711360, -198868992, 396853248, -539705344, 575616000,
                                    -488780800, 334354816, -183521792, 79190084, -26501658,
                                    6858539, -1343364, 179448, -9702, -1674, 324])
    derived_P.require_equal(published_P, "reconstructed P")
    derived_Q.require_equal(published_Q, "reconstructed Q")
    shifts = []
    for label, poly in [("A1", A1), ("A2", A2),
                        ("P_minus_256n11", derived_P - 256 * n ** 11),
                        ("384n15_minus_Q", 384 * n ** 15 - derived_Q)]:
        cs = shift_coefficients(poly, 16)
        check(all(c > 0 for c in cs), "strict shift positivity " + label)
        poly.substitute("n", n + 16).require_equal(from_coefficients(cs), "independent shift route")
        shifts.append({"label": label, "degree": len(cs) - 1, "coefficients": [str(c) for c in cs]})
    check(4 * 2 ** 16 > 3 * 17 ** 4 and 18 ** 4 < 2 * 17 ** 4, "exponential induction")
    return {"P": [str(c) for c in derived_P.n_coefficients()],
            "Q": [str(c) for c in derived_Q.n_coefficients()],
            "moments": [[str(c) for c in mu.n_coefficients()] for mu in mus],
            "strict_shifts": shifts}, (left, right, physical, simplified, derived_P, derived_Q)


def finite_forms():
    tests, energies, norms = 0, {}, {}
    for n in range(6, 25):
        base = complete(n)
        Bs = upper_forms(n, base)
        p0, p1 = profiles(n)
        w = n * (n - 1)
        actual = energy(Bs[0], p0) + w * energy(Bs[1], p1)
        check(actual == scalar(n), "independent physical versus scalar energy")
        energies[str(n)] = str(actual)
        norm = sum(choose(n, a) * p0[a - 1] ** 2 + w * choose(n - 2, a - 1) * p1[a - 1] ** 2
                   for a in range(1, n - 1))
        norms[str(n)] = str(norm)
        for a in range(3, n // 2 + 1):
            varied = upper_forms(n, complete(n, {a: F(-7, 3)}))
            for j in (0, 1):
                delta = [[x - y for x, y in zip(row, old)] for row, old in zip(varied[j], Bs[j])]
                kernels = [[F(1)] * (n - 2),
                           [F(r) if j == 0 else F(2 * r - 2, r) for r in range(1, n - 1)],
                           [F(int(r == n - 2)) for r in range(1, n - 1)]]
                for vector in kernels:
                    check(all(v == 0 for v in matvec(delta, vector)), "free-direction common kernel")
            check(energy(varied[0], p0) + w * energy(varied[1], p1) == actual, "all real-coordinate dual cancellation")
            tests += 1
    check(energies['16'] == str(F(-128339434961554045335923, 1488611666855678976)), "direct boundary16")
    eps16 = -F(energies['16']) / ((2 ** 15 - 1) * F(norms['16']))
    check(eps16 > F(1, 10000), "strict quantitative cap violation at16")
    return {"orders": [6, 24], "complement_directions": tests,
            "physical_energies": energies, "physical_norms": norms,
            "proved_cap_excess_bound_at16": str(eps16)}


def damages(symbolic):
    rejected = []
    trials = [("floating coefficient", lambda: P(0.5)),
              ("nonfree complement", lambda: complete(16, {2: 1})),
              ("floating deficit", lambda: complete(16, {3: 0.5})),
              ("altered profile identity", lambda: (symbolic[0] + 1).require_equal(symbolic[1], "damage")),
              ("altered scalar identity", lambda: symbolic[2].require_equal(symbolic[3] + P.variable('x'), "damage")),
              ("altered P coefficient", lambda: symbolic[4].require_equal(symbolic[4] + 1, "damage")),
              ("wrong moment", lambda: moment_polynomial(3).require_equal(15 * P.variable('n') ** 3, "damage"))]
    for name, action in trials:
        try:
            action()
        except (ValueError, TypeError):
            rejected.append(name)
        else:
            raise ValueError("damage accepted: " + name)
    return rejected


def main():
    universal, symbolic = universal_identities()
    record = {"audit": "six-reviewer-2 / graph9091 / exact independent reconstruction",
              "universal": universal, "finite": finite_forms(),
              "literal_controls": [literal_control(n) for n in [6, 7]],
              "damage_controls": damages(symbolic)}
    encoded = json.dumps(record, sort_keys=True, separators=(',', ':')).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    if '--record' not in sys.argv:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        check(record == expected, "entire frozen record equality")
    if '--record' in sys.argv:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        print(json.dumps({"status": "PASS", "canonical_result_sha256": digest,
                          "universal_shift_coefficients": sum(len(s['coefficients']) for s in universal['strict_shifts']),
                          "independent_complement_directions": record['finite']['complement_directions'],
                          "original_vertex_controls": [x['N'] for x in record['literal_controls']],
                          "negative_boundary16": record['finite']['physical_energies']['16'],
                          "cap_excess16": record['finite']['proved_cap_excess_bound_at16'],
                          "damages_rejected": len(record['damage_controls'])}, sort_keys=True))


if __name__ == '__main__':
    main()
