#!/usr/bin/env python3
"""Supplementary exact audits for PROOF.md; CPython, standard library only.

Default: deterministic JSON on stdout. --check: compare it with EXPECTED.json.
Universal analytic claims are established in PROOF.md, not by finite sampling.
"""

import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def norm2(a):
    return dot(a, a)


def dist2(a, b):
    return norm2(sub(a, b))


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][col]
        a[r] = [x / scale for x in a[r]]
        for i in range(r + 1, len(a)):
            scale = a[i][col]
            a[i] = [x - scale * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def determinant(rows):
    n = len(rows)
    require(all(len(row) == n for row in rows), "determinant: nonsquare input")
    if n == 1:
        return rows[0][0]
    return sum((-1) ** j * rows[0][j] * determinant(
        [row[:j] + row[j + 1:] for row in rows[1:]]) for j in range(n))


def affine_rank(rows):
    return rank([sub(row, rows[0]) for row in rows[1:]])


def hull(points):
    points = sorted(set(points))

    def half(seq):
        result = []
        for point in seq:
            while len(result) >= 2 and cross(
                    sub(result[-1], result[-2]), sub(point, result[-1])) <= 0:
                result.pop()
            result.append(point)
        return result

    return half(points)[:-1] + half(reversed(points))[:-1]


def conjugate_product(u, v):
    return (dot(u, v), cross(u, v))


# Sparse exact polynomial ring in the eleven named real indeterminates.
# Reduction uses only S^2=1-C^2 and d^2=1-c^2. All other variables are free.
NAMES = ("C", "S", "c", "d", "ax", "ay", "bx", "by", "az", "bz", "omega")
N = len(NAMES)


class Poly:
    def __init__(self, terms=None):
        self.terms = {m: F(v) for m, v in (terms or {}).items() if v}

    @staticmethod
    def const(value):
        return Poly({(0,) * N: value})

    @staticmethod
    def var(index):
        m = [0] * N
        m[index] = 1
        return Poly({tuple(m): 1})

    def __add__(self, other):
        if not isinstance(other, Poly):
            other = Poly.const(other)
        terms = dict(self.terms)
        for m, v in other.terms.items():
            terms[m] = terms.get(m, F(0)) + v
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -v for m, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Poly) else -F(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not isinstance(other, Poly):
            other = Poly.const(other)
        terms = {}
        for m, v in self.terms.items():
            for k, w in other.terms.items():
                e = tuple(x + y for x, y in zip(m, k))
                terms[e] = terms.get(e, F(0)) + v * w
        return Poly(terms)

    __rmul__ = __mul__

    def square(self):
        return self * self

    def diff(self, index):
        terms = {}
        for m, v in self.terms.items():
            if m[index]:
                e = list(m)
                e[index] -= 1
                terms[tuple(e)] = v * m[index]
        return Poly(terms)

    def reduced(self):
        terms = {}

        def expand(m, v):
            for sine, cosine in ((1, 0), (3, 2)):
                if m[sine] >= 2:
                    e = list(m)
                    e[sine] -= 2
                    expand(tuple(e), v)
                    e[cosine] += 2
                    expand(tuple(e), -v)
                    return
            terms[m] = terms.get(m, F(0)) + v

        for m, v in self.terms.items():
            expand(m, v)
        return Poly(terms)

    def record(self):
        return [[list(m), str(v)] for m, v in sorted(self.terms.items())]


def symbolic_audit():
    C, S, c, d, ax, ay, bx, by, az, bz, omega = [Poly.var(i) for i in range(N)]
    zero = Poly.const(0)
    columns = [(C, S, zero, zero), (-S, C, zero, zero), (zero, zero, c, d)]
    identities = {}
    for i in range(3):
        for j in range(i, 3):
            identities[f"Gram_{i}{j}"] = dot(columns[i], columns[j]) - int(i == j)
    transverse = ax * (C * bx - S * by) + ay * (S * bx + C * by)
    rotated = -ax * (S * bx + C * by) + ay * (C * bx - S * by)
    identities["Cauchy_Schwarz_remainder"] = (
        (ax.square() + ay.square()) * (bx.square() + by.square())
        - transverse.square() - rotated.square())
    inner = transverse + c * az * bz
    derivative = inner.diff(0) * omega * S - inner.diff(1) * omega * C + 2 * inner.diff(2)
    identities["cross_derivative"] = derivative - (2 * az * bz - omega * rotated)
    for name, polynomial in identities.items():
        require(not polynomial.reduced().terms, f"failed polynomial identity: {name}")
    bad_gram = c.square() + 4 * d.square() - 1
    require(bool(bad_gram.reduced().terms), "vertical-scale mutation was not detected")
    record = {name: poly.record() for name, poly in sorted(identities.items())}
    data = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return {"identities": len(identities), "names": sorted(identities),
            "expanded_terms": sum(len(p.terms) for p in identities.values()),
            "expanded_identity_sha256": sha256(data).hexdigest()}


def direction_audit(directions):
    require(len(directions) == 12 and len(set(directions)) == 12, "direction cardinality")
    require(all(norm2(v) == 1 for v in directions), "direction is not unit")
    require({neg(v) for v in directions} == set(directions), "missing antipodal direction")
    gaps = []
    facet_distances = []
    for i, u in enumerate(directions):
        v = directions[(i + 1) % len(directions)]
        require(cross(u, v) > 0 and dot(u, v) > 0, "incorrect direction ordering")
        edge = sub(v, u)
        require(all(cross(edge, sub(w, u)) > 0 for w in directions if w not in (u, v)),
                "listed edge is not a strict supporting edge")
        gaps.append(dot(u, v))
        facet_distances.append(cross(u, v) ** 2 / norm2(edge))
    require(min(gaps) == F(4, 5), "wrong largest gap")
    require(min(facet_distances) == F(9, 10), "wrong unit polygon inradius")
    return gaps, facet_distances


def fixture_audit():
    d = [(F(x, 5), F(y, 5)) for x, y in
         [(5, 0), (4, 3), (3, 4), (0, 5), (-3, 4), (-4, 3),
          (-5, 0), (-4, -3), (-3, -4), (0, -5), (3, -4), (4, -3)]]
    gaps, facets = direction_audit(d)
    p, q = F(3, 4), F(4, 5)
    A = [(p * x, p * y, F(1)) for x, y in d]
    B = [(q * x, q * y, F(1)) for x, y in d]
    origin = (F(0),) * 3
    source = [origin] + A + [neg(b) for b in B]
    target = [origin] + A + B
    require(len(set(source)) == len(set(target)) == 25, "colliding fixture sites")
    losses = []
    strict = []
    records = []
    for i, j in combinations(range(25), 2):
        loss = dist2(source[i], source[j]) - dist2(target[i], target[j])
        predicted = 4 * dot(A[i - 1], B[j - 13]) if 1 <= i <= 12 < j else 0
        require(loss == predicted and loss >= 0, f"bad pair loss: {i},{j}")
        losses.append(loss)
        if loss:
            strict.append(loss)
        records.append([i, j, str(loss)])
    require((len(strict), losses.count(0), min(strict), max(strict)) ==
            (144, 156, F(8, 5), F(32, 5)), "incorrect pair counts or margins")
    paired = [x + y for x, y in zip(source, target)]
    require((rank(A), rank(B), affine_rank(paired), affine_rank(paired[1:]),
             rank([sub(x, y) for x, y in zip(source, target)])) == (3, 3, 6, 5, 3),
            "rank audit failed")
    indices = (0, 3, 6)  # east, north, west
    detA = determinant([list(A[i]) for i in indices])
    detB = determinant([list(B[i]) for i in indices])
    rows = [list(A[i] + A[i]) for i in indices] + [list(neg(B[i]) + B[i]) for i in indices]
    det6 = determinant(rows)
    require((detA, detB, det6) == (F(9, 8), F(32, 25), F(288, 25)), "minor certificate failed")

    # Independently compute every vertex of the dual section from its two
    # adjacent supporting lines, and check all twelve inequalities directly.
    polar = []
    for i, u in enumerate(d):
        v = d[(i + 1) % len(d)]
        delta = cross(u, v)
        w = ((v[1] - u[1]) / (p * delta), (u[0] - v[0]) / (p * delta))
        require(all(dot(e, w) <= 1 / p for e in d), "infeasible dual vertex")
        polar.append(w)
    require(len(hull(polar)) == 12, "dual polygon hull mismatch")
    r2 = q * q * min(facets)
    R2 = max(map(norm2, polar))
    require((r2, R2, r2 / R2) == (F(72, 125), F(160, 81), F(729, 2500)),
            "disk-sandwich certificate mismatch")
    require(4 * r2 > R2, "no strict triangle obstruction")

    changed = list(d)
    changed[1] = (F(4, 5), F(4, 5))
    try:
        direction_audit(changed)
    except ValueError:
        pass
    else:
        raise ValueError("nonunit direction mutation was not detected")
    return {"p": str(p), "q": str(q), "slope_product": str(p * q),
            "directions": [[str(x), str(y)] for x, y in d],
            "sites": len(source), "pairs": len(losses), "strict_pairs": len(strict),
            "preserved_pairs": losses.count(0),
            "minimum_strict_squared_loss": str(min(strict)),
            "maximum_squared_loss": str(max(strict)),
            "paired_affine_rank": affine_rank(paired), "rank_without_origin": affine_rank(paired[1:]),
            "displacement_rank": 3, "det_A": str(detA), "det_B": str(detB),
            "paired_minor": str(det6), "adjacent_gap_cosines": dict(sorted(Counter(map(str, gaps)).items())),
            "inner_radius_squared": str(r2), "outer_radius_squared": str(R2),
            "radius_ratio": "27/50", "radius_ratio_squared": str(r2 / R2),
            "pair_record_sha256": sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()}


def noncircular_audit():
    a, b = F(9, 10), F(1, 20)
    P = [(sx * a, sy * b) for sx, sy in product((-1, 1), repeat=2)]
    W = hull([conjugate_product(u, v) for u, v in product(P, repeat=2)])
    require(len(W) == 6, "noncircular product hull should be a hexagon")
    r2 = a * a + b * b
    require(r2 == F(13, 16), "noncircular circular-envelope slope product")
    lengths2 = Counter(dist2(W[i], W[(i + 1) % len(W)]) for i in range(len(W)))
    require(lengths2 == Counter({F(104329, 40000): 2, F(13, 1600): 4}),
            "noncircular edge lengths mismatch")
    # Exact perimeter is 323/100 + sqrt(13)/10. sqrt(13) < 37/10.
    require(F(37, 10) ** 2 > 13, "incorrect square-root upper bound")
    upper = F(323, 100) + F(37, 100)
    require(upper == F(18, 5) and upper < 4, "perimeter bound fails")
    require(3 * r2 > 2, "example should fail the circular condition using pi>3")
    return {"section_half_widths": [str(a), str(b)],
            "product_hull": [[str(x), str(y)] for x, y in W],
            "perimeter_exact": "323/100 + sqrt(13)/10", "perimeter_strict_upper_bound": str(upper),
            "circular_envelope_slope_product": str(r2)}


def pi_bound_audit():
    # x^4(1-x)^4 = (1+x^2)Q(x)-4, with integral_0^1 Q = 22/7.
    # Integration gives 22/7-pi = integral_0^1 x^4(1-x)^4/(1+x^2) > 0.
    Q = [F(4), F(0), F(-4), F(0), F(5), F(-4), F(1)]
    numerator = [F(0)] * 9
    for i, c in enumerate(Q):
        numerator[i] += c
        numerator[i + 2] += c
    numerator[0] -= 4
    require(numerator == [0, 0, 0, 0, 1, -4, 6, -4, 1], "pi identity polynomial failed")
    integral = sum(c / (i + 1) for i, c in enumerate(Q))
    require(integral == F(22, 7), "pi identity integral failed")
    margin = 2 - integral * F(3, 5)
    require(margin == F(4, 35) and margin > 0, "fixture derivative margin failed")
    # The pair p=q=1 contracts at the endpoints, but its axial path has a
    # negative derivative at a suitable transverse pair: 2-pi < 2-3 < 0.
    require(1 - F(1) == 0 and 2 - 3 * F(1) < 0, "outside-ansatz control failed")
    return {"integral_of_quotient": str(integral), "strict_derivative_margin": str(margin),
            "outside_ansatz_control": "p=q=1: endpoint contraction; axial derivative 2-pi<0"}


def run():
    return {"status": "AXIAL_CONE_EXACT_AUDITS_PASS", "arithmetic": "integers and fractions.Fraction",
            "symbolic": symbolic_audit(), "fixture": fixture_audit(),
            "noncircular": noncircular_audit(), "pi_bound": pi_bound_audit(),
            "controls": ["vertical-scale mutation rejected", "nonunit direction rejected",
                         "origin deletion has rank five", "endpoint contraction outside axial criterion"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = (json.dumps(run(), indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_bytes()
        require(output == expected, "EXPECTED.json does not match the exact audit")
        print("AXIAL_CONE_EXACT_AUDITS_PASS", sha256(output).hexdigest())
    else:
        print(output.decode(), end="")


if __name__ == "__main__":
    main()
