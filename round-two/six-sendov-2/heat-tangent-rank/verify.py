#!/usr/bin/env python3
"""Exact certificates for heat-tangent independence. Author: six-sendov-2.

Standard-library Fraction arithmetic only. Polynomial expansions certify
identities, not an enumeration of real-rooted profiles. Ordinary proof
bridges are in PROOF.md. There are no assert-based validation gates.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


class P:
    """Sparse exact polynomial in d,v. No CAS and no polynomial division."""
    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): F(a) for k, a in value.items() if a}
        else:
            self.c = {(0, 0): F(value)} if value else {}

    def __add__(self, other):
        other = P(other)
        out = dict(self.c)
        for k, a in other.c.items():
            out[k] = out.get(k, F(0)) + a
            if not out[k]:
                del out[k]
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -a for k, a in self.c.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        other = P(other)
        out = {}
        for (i, j), a in self.c.items():
            for (k, l), b in other.c.items():
                key = (i + k, j + l)
                out[key] = out.get(key, F(0)) + a * b
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "bad power")
        out, base = P(1), self
        while exponent:
            if exponent & 1:
                out = out * base
            base = base * base
            exponent //= 2
        return out

    def __eq__(self, other):
        return self.c == P(other).c

    def at(self, d, v):
        return sum((a * d**i * v**j for (i, j), a in self.c.items()), F(0))

    def encoded(self):
        return [[i, j, str(a)] for (i, j), a in sorted(self.c.items())]


def determinant(matrix):
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "nonsquare matrix")
    out = 0
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = (-1)**inversions
        for i, j in enumerate(perm):
            term = term * matrix[i][j]
        out = out + term
    return out


def adjugate3(matrix):
    return [[(-1)**(i + j) * determinant([
        [matrix[r][c] for c in range(3) if c != i]
        for r in range(3) if r != j
    ]) for j in range(3)] for i in range(3)]


def quadratic(left, matrix, right):
    return sum((left[i] * matrix[i][j] * right[j]
                for i in range(3) for j in range(3)), P(0))


def symbolic_certificate(damage=None):
    d, v = P({(1, 0): 1}), P({(0, 1): 1})
    s = v*v
    a = 9 - 84*d + 70*s
    m = 9 - 24*d + 10*s
    b = -21*d + 35*s - 9
    c = -56*d + 70*s - 9
    e = -126*d + 140*s - 9
    j = -336*d + 350*s - 9
    k = -504*d + 490*s + 9
    p = 1176*d**3 + 567*d*d - 3150*d*s - 162*d + 875*s*s + 900*s - 81
    q = (-381024*d**3 + 82320*d*d*s*s + 952560*d*d*s + 88452*d*d
         - 929040*d*s*s - 166320*d*s + 18468*d + 196000*s**3
         + 185220*s*s - 43740*s + 729)
    r = (-37632*d*d*s + 12096*d*d + 31584*d*s - 4752*d
         + 4900*s*s - 11052*s + 81)
    n5 = v*(336*d*d - 987*d + 925*s - 99)
    n6 = (37632*d**3*s + 266112*d**3 - 724416*d*d*s + 145800*d*d
          + 200200*d*s*s - 72594*d*s + 15309*d + 245000*s**3
          - 101250*s*s - 2997*s + 729)
    n7 = v*(526848*d**4*s - 11176704*d**4 + 94371648*d**3*s
            - 93263184*d**3 - 179065600*d*d*s*s + 290457468*d*d*s
            - 22984074*d*d + 96040000*d*s**3 - 276912300*d*s*s
            + 41959728*d*s - 1497609*d + 78225000*s**3
            - 17915850*s*s + 1356183*s - 37179)
    n8 = (-21504*d**3 + 48384*d*d*s - 38016*d*d - 33088*d*s
          - 1944*d + 59200*s*s - 1386*s - 81)
    if damage == "moment8":
        n8 = n8 + 1
    t0 = [P(7), P(0), P(F(3, 4)), F(5, 8)*v, F(3, 32) + d*F(1, 2)]
    common = 6144*b*c*e
    x = [t*common for t in t0] + [96*c*e*n5, 8*e*n6, 4*n7, b*e*n8]
    k_numerator = -m*F(1, 8)
    b_numerator = v*(14*d - 9)
    recurrences = []
    for degree in range(2, 8):
        lhs = ((degree - 1)*a - 7*m)*x[degree + 1]*common
        rhs = a*sum((x[l]*x[degree + 1 - l] for l in range(1, degree + 1)), P(0))
        rhs = rhs + b_numerator*((7 - degree)*x[degree]*common + sum(
            (x[l]*x[degree - l] for l in range(1, degree)), P(0)))
        rhs = rhs + k_numerator*((14 - degree)*x[degree - 1]*common + sum(
            (x[l]*x[degree - 1 - l] for l in range(1, degree - 1)), P(0)))
        require(lhs == rhs, "moment recurrence fails")
        recurrences.append(degree)
    g = [[t0[i + l] for l in range(3)] for i in range(3)]
    gd = determinant(g)
    require(gd == -j*F(1, 128), "G3 determinant identity")
    adj = adjugate3(g)
    require(all(sum((g[i][l]*adj[l][z] for l in range(3)), P(0))
                == (gd if i == z else P(0)) for i in range(3) for z in range(3)),
            "adjugate identity")
    y3, y4 = x[3:6], x[4:7]
    actual = [
        x[6]*common*gd - quadratic(y3, adj, y3),
        x[7]*common*gd - quadratic(y3, adj, y4),
        x[8]*common*gd - quadratic(y4, adj, y4),
    ]
    factored = [
        ((s - d)*j*p, 48*c*b*b),
        (3*v*(s - d)*(14*d - 9)*j*p, 32*e*c*b*b),
        (-(s - d)*p*r, 384*c*c*b*b),
    ]
    if damage == "schur_sign":
        factored[2] = (-factored[2][0], factored[2][1])
    for actual_n, (n, den) in zip(actual, factored):
        require(actual_n*den == n*common**2*gd, "Schur entry identity")
    bracket = r*e*e + 162*s*c*(14*d - 9)**2*j
    if damage == "determinant_factor":
        q = q + 1
    require(bracket == k*q, "Schur determinant factor identity")
    factors = {name: poly.encoded() for name, poly in [
        ("A", a), ("M", m), ("B", b), ("C", c), ("E", e),
        ("J", j), ("K", k), ("P", p), ("Q", q), ("R", r),
    ]}
    formulas = {
        "moments": [[t.encoded(), P(1).encoded()] for t in t0] + [
            [n5.encoded(), (64*b).encoded()],
            [n6.encoded(), (768*c*b).encoded()],
            [n7.encoded(), (1536*e*c*b).encoded()],
            [n8.encoded(), (6144*c).encoded()]],
        "H5_det_numerator": ((s - d)**2*k*j*j*p*p*q).encoded(),
        "H5_det_denominator": (2359296*e*e*c**3*b**4).encoded(),
    }
    return {
        "recurrence_degrees": recurrences,
        "schur_entry_identities": 3,
        "factor_coefficients": factors,
        "formulas": formulas,
    }


def sign_bounds(damage=None):
    delta = F(69, 5000)
    if damage == "domain":
        delta = F(1, 8)
    bounds = {
        "delta": delta,
        "A_lower": 9 - 84*delta,
        "M_lower": 9 - 24*delta,
        "B_C_E_J_upper": -9 + 14*delta,
        "K_lower": 9 - 504*delta,
        "P_upper": 1176*delta**3 + 1442*delta**2 + 900*delta - 81,
        "Q_lower": 729 - 43740*delta - 166320*delta**2 - 1310064*delta**3,
        "constant_relation_coefficient_upper": 28*delta - 3,
        "rank_drop_a_numerator_lower": F(3, 8) - delta,
    }
    for name in ["A_lower", "M_lower", "K_lower", "Q_lower",
                 "rank_drop_a_numerator_lower"]:
        require(bounds[name] > 0, "positive sign bound")
    for name in ["B_C_E_J_upper", "P_upper", "constant_relation_coefficient_upper"]:
        require(bounds[name] < 0, "negative sign bound")
    return {name: str(value) for name, value in bounds.items()}


def trim(poly):
    out = list(map(F, poly))
    while len(out) > 1 and not out[-1]:
        out.pop()
    return out or [F(0)]


def uadd(left, right):
    n = max(len(left), len(right))
    return trim([(left[i] if i < len(left) else F(0))
                 + (right[i] if i < len(right) else F(0)) for i in range(n)])


def uscale(poly, scalar):
    return trim([a*scalar for a in poly])


def umul(left, right):
    out = [F(0)]*(len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a*b
    return trim(out)


def udiff(poly):
    return trim([i*poly[i] for i in range(1, len(poly))])


def udivide(left, right):
    left, right = trim(left), trim(right)
    require(right != [F(0)], "zero polynomial divisor")
    quotient = [F(0)]*max(1, len(left) - len(right) + 1)
    while left != [F(0)] and len(left) >= len(right):
        k, a = len(left) - len(right), left[-1]/right[-1]
        quotient[k] = a
        left = uadd(left, [F(0)]*k + uscale(right, -a))
    return trim(quotient), left


def real_simple_count(poly):
    chain = [trim(poly), udiff(poly)]
    while chain[-1] != [F(0)]:
        _, rem = udivide(chain[-2], chain[-1])
        if rem == [F(0)]:
            break
        chain.append(uscale(rem, -1))
    require(len(chain[-1]) == 1, "Sturm simplicity fails")
    def variations(infinity):
        signs = []
        for q in chain:
            sign = (q[-1] > 0) - (q[-1] < 0)
            if infinity < 0 and (len(q) - 1) % 2:
                sign = -sign
            signs.append(sign)
        return sum(a != b for a, b in zip(signs, signs[1:]))
    return variations(-1) - variations(1)


def rank(matrix):
    matrix = [list(map(F, row)) for row in matrix]
    pivot = 0
    for column in range(len(matrix[0])):
        chosen = next((i for i in range(pivot, len(matrix)) if matrix[i][column]), None)
        if chosen is None:
            continue
        matrix[pivot], matrix[chosen] = matrix[chosen], matrix[pivot]
        scale = matrix[pivot][column]
        matrix[pivot] = [a/scale for a in matrix[pivot]]
        for i in range(len(matrix)):
            if i != pivot and matrix[i][column]:
                scale = matrix[i][column]
                matrix[i] = [a - scale*b for a, b in zip(matrix[i], matrix[pivot])]
        pivot += 1
        if pivot == len(matrix):
            break
    return pivot


def heat_columns(f, damage=None):
    n = -2*f[6]
    first, second = udiff(f), udiff(udiff(f))
    radial = uadd([F(0)] + first, uscale(f, -8))
    q0 = uadd(second, uscale(radial, -56/n))
    q1 = uadd([F(0)] + second, uscale(first, -7))
    q2 = uadd(uadd([F(0)]*2 + second, uscale([F(0)] + first, -13)), uscale(f, 48))
    require(max(map(len, [q0, q1, q2])) <= 6, "heat degree cancellation")
    a1, a2, a3, a4, a5 = f[1:6]
    r = [35*a1 + 6*a5*a2/n, 24*a2 + 15*a5*a3/(2*n),
         15*a3 + 8*a5*a4/n, 8*a4 + 15*a5*a5/(2*n)]
    t = [6*a3 - 1568*a1/n, 12*a4 - 1008*a2/n,
         20*a5 - 560*a3/n, -15*n - 224*a4/n]
    if damage == "chart":
        t[3] += 1
    rr = uadd(q2, uscale(q1, -a5/(2*n)))
    tt = uadd(uadd(q0, uscale(q1, -28*a5/n**2)), uscale(rr, -56/n))
    require(rr[1:] == trim([0] + r)[1:] and tt[1:] == trim([0] + t)[1:],
            "coefficient chart identity")
    columns = [[F(1)] + [F(0)]*5] + [
        q + [F(0)]*(6 - len(q)) for q in [q0, q1, q2]]
    return columns, r, t


def root_chart_tests(damage=None):
    fixtures = [
        [-1003, -1001, -999, -997, 997, 999, 1001, 1003],
        [-101, -100, -99, -98, 97, 99, 100, 102],
        [-103, -101, -100, -96, 97, 98, 100, 105],
        [-105, -104, -103, -102, 74, 112, 113, 115],
    ]
    out = []
    for u in fixtures:
        require(len(set(u)) == 8 and sum(u) == 0, "original-root domain")
        f = [F(1)]
        for root in u:
            f = umul(f, [-F(root), F(1)])
        n = sum(F(root)**2 for root in u)
        d = sum(F(root)**4 for root in u)/n**2 - F(1, 8)
        skew_squared = sum(F(root)**3 for root in u)**2/n**3
        require(0 <= skew_squared < d <= F(69, 5000), "chart test not in rank domain")
        columns, r, t = heat_columns(f, damage)
        require(rank(columns) == 4, "four heat/constant directions")
        pair = next(((i, j) for i, j in combinations(range(4), 2)
                     if r[i]*t[j] != r[j]*t[i]), None)
        require(pair is not None, "no complement chart")
        remaining = [i + 1 for i in range(4) if i not in pair]
        extended = columns + [
            [F(int(j == i)) for j in range(6)] for i in remaining]
        require(rank(extended) == 6 and determinant(extended) != 0, "incomplete tangent basis")
        out.append({"roots": u, "d": str(d), "s": str(skew_squared),
                    "pivot_degrees": [i + 1 for i in pair], "complement_degrees": remaining,
                    "basis_determinant": str(determinant(extended))})
    hermite = list(map(F, [105, 0, -420, 0, 210, 0, -28, 0, 1]))
    columns, _, _ = heat_columns(hermite)
    require(real_simple_count(hermite) == 8, "Hermite not eight simple real roots")
    require(columns[1] == [F(0)]*6 and rank(columns) == 3, "Hermite rank-loss control")
    powers = newton(hermite, 4)
    require(powers[1] == 0 and powers[2] == 56
            and powers[4] - powers[2]**2/8 == 336, "Hermite variance control")
    return {"high_domain_charts": out,
            "outside_domain_control": {"polynomial": list(map(str, hermite)),
                                       "real_simple_originals": 8, "N": "56",
                                       "D": "336", "d": "3/28", "constant_heat_rank": 3}}


def newton(poly, count):
    """Independent moments from monic coefficients, including degree+1."""
    degree = len(poly) - 1
    require(poly[-1] == 1, "Newton polynomial not monic")
    powers = [F(degree)]
    for k in range(1, count + 1):
        value = F(0)
        for j in range(1, min(k, degree) + 1):
            coefficient = poly[degree - j]
            value += (k*coefficient if j == k
                      else coefficient*powers[k - j])
        powers.append(-value)
    return powers


def ode_newton_tests(symbolic, damage=None):
    out = []
    for d, v in [(F(1, 1000), F(0)), (F(1, 1000), F(1, 100)),
                 (F(69, 5000), F(0)), (F(69, 5000), F(1, 10)),
                 (F(1, 100), -F(3, 40))]:
        s = v*v
        require(0 <= s < d <= F(69, 5000), "formal ODE sample domain")
        k = (F(3, 8) + 5*s/F(12) - d)/(28*d - 3 - 70*s/F(3))
        b = (1 + 56*k)*v/6
        h = [F(0)]*8
        h[7] = F(1)
        for j in reversed(range(7)):
            coefficient = (7 - j)*(5 - j + 56*k)
            require(coefficient != 0, "ODE coefficient denominator")
            h[j] = (-b*(j + 1)*(j - 6)*h[j + 1]
                    - k*(j + 2)*(j + 1)*(h[j + 2] if j + 2 < 8 else F(0)))/coefficient
        if damage == "ode":
            h[0] += 1
        h_first, h_second = udiff(h), udiff(udiff(h))
        residual = uadd(uadd(umul([k, b, F(1)], h_second),
                             umul([-6*b, -(11 + 56*k)], h_first)),
                        uscale(h, 35 + 392*k))
        require(residual == [F(0)], "ODE construction")
        actual = newton(h, 8)
        expected = []
        for numerator, denominator in symbolic["formulas"]["moments"]:
            nn = P({(i, j): F(a) for i, j, a in numerator})
            dd = P({(i, j): F(a) for i, j, a in denominator})
            expected.append(nn.at(d, v)/dd.at(d, v))
        require(actual == expected, "independent ODE/Newton moments")
        gram = [[actual[i + j] for j in range(5)] for i in range(5)]
        det = determinant(gram)
        nn = P({(i, j): F(a) for i, j, a in symbolic["formulas"]["H5_det_numerator"]})
        dd = P({(i, j): F(a) for i, j, a in symbolic["formulas"]["H5_det_denominator"]})
        require(det == nn.at(d, v)/dd.at(d, v) and det < 0, "direct five-by-five determinant")
        out.append({"d": str(d), "v": str(v), "H5_determinant": str(det),
                    "moments_0_through_8": list(map(str, actual)),
                    "polynomial_is_not_claimed_real_rooted": True})
    return out


def damage_controls(symbolic):
    controls = []
    for name, check in [
        ("moment8", lambda: symbolic_certificate("moment8")),
        ("schur_sign", lambda: symbolic_certificate("schur_sign")),
        ("determinant_factor", lambda: symbolic_certificate("determinant_factor")),
        ("domain", lambda: sign_bounds("domain")),
        ("chart", lambda: root_chart_tests("chart")),
        ("ode", lambda: ode_newton_tests(symbolic, "ode")),
    ]:
        try:
            check()
        except ValueError as exc:
            controls.append({"damage": name, "rejected": str(exc)})
        else:
            raise ValueError("damage escaped: " + name)
    return controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    symbolic = symbolic_certificate()
    record = {
        "actual_author": "six-sendov-2",
        "role": "researcher",
        "claim_status": "ordinary unformalized author lemma; no independent review",
        "symbolic_certificate": symbolic,
        "uniform_sign_bounds": sign_bounds(),
        "tangent_chart_checks": root_chart_tests(),
        "independent_coefficient_ODE_Newton_checks": ode_newton_tests(symbolic),
        "damage_controls": damage_controls(symbolic),
        "boundary": "no all-distinct high stationary nonexistence or global angular equality proved",
    }
    if args.expected:
        require(json.loads(args.expected.read_text()) == record, "entire external fixture differs")
    if args.write_expected:
        args.write_expected.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    digest = hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print(json.dumps({"complete": True, "record_sha256": digest,
                      "recurrences": 6, "schur_entry_identities": 3,
                      "high_domain_charts": 4, "independent_ODE_Newton_checks": 5,
                      "outside_domain_rank_loss_control": True,
                      "damage_controls": 6}, sort_keys=True))


if __name__ == "__main__":
    main()
