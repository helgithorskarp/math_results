#!/usr/bin/env python3
"""Independent exact audit of the fixed-Moser three-copy exclusion.

This checker imports no code from the reviewed package.  It implements
Q(sqrt(33), i*sqrt(3)) directly in the four-coordinate basis
1, sqrt(33), i*sqrt(3), i*sqrt(11), rebuilds both component graphs, and
enumerates every cross-edge quadratic in both orientation parities.
"""

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_nonmono159_moser_triple"
POINTS = ROOT / "hadwiger_nelson_nonmono159_214_lowden2" / "points159.tsv"

ZERO = (Q(0), Q(0), Q(0), Q(0))
ONE = (Q(1), Q(0), Q(0), Q(0))
RZERO = (Q(0), Q(0))
RONE = (Q(1), Q(0))

EXPECTED_CLASSIFICATION = "a9c666ea717446644d2cc21ca56c27a0bccb161fded7cb70ff695aa94286aa99"
EXPECTED_PARTITION = "88597ad1b67ec766486fd1befbe183649e92a776ea09350c5a44e4ebe919b04b"
EXPECTED_A_LIBRARY = "92f7c3cbe62a5eb2b0f827fc065e022018c598e16ea2651580aabccfb01c7195"
EXPECTED_B_LIBRARY = "b9285f2967686bf5458588c6f949173ac8795412a7ffd94a60d687e5a8c260a3"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y, strict=True))


def neg(x):
    return tuple(-a for a in x)


def mul(x, y):
    """Multiply in basis 1,s,p,q with s^2=33,p^2=-3,q^2=-11."""
    a, b, c, d = x
    A, B, C, D = y
    return (
        a*A + 33*b*B - 3*c*C - 11*d*D,
        a*B + b*A - c*D - d*C,
        a*C + c*A + 11*(b*D + d*B),
        a*D + d*A + 3*(b*C + c*B),
    )


def conj(x):
    return x[0], x[1], -x[2], -x[3]


def inverse(x):
    n = mul(x, conj(x))
    require(n[2:] == (0, 0), ("nonreal norm", x, n))
    a, b = n[:2]
    denominator = a*a - 33*b*b
    require(denominator != 0, ("zero inverse denominator", x))
    return mul(conj(x), (a/denominator, -b/denominator, Q(0), Q(0)))


def norm(x):
    value = mul(x, conj(x))
    require(value[2:] == (0, 0), ("norm", x, value))
    return value[:2]


def radd(x, y):
    return x[0] + y[0], x[1] + y[1]


def rneg(x):
    return -x[0], -x[1]


def rscale(x, scalar):
    return scalar*x[0], scalar*x[1]


def rmul(x, y):
    return x[0]*y[0] + 33*x[1]*y[1], x[0]*y[1] + x[1]*y[0]


def real_sign(x):
    """Sign of a+b*sqrt(33) in the distinguished real embedding."""
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    comparison = a*a - 33*b*b
    require(comparison != 0, ("unexpected rational sqrt(33)", x))
    return ((a > 0) - (a < 0))*((comparison > 0) - (comparison < 0))


def rational_sqrt(x):
    if x < 0:
        return None
    numerator = isqrt(x.numerator)
    denominator = isqrt(x.denominator)
    if numerator*numerator == x.numerator and denominator*denominator == x.denominator:
        return Q(numerator, denominator)
    return None


def square_in_real_field(value):
    """Decide whether value is a square in Q(sqrt(33)), with verification."""
    a, b = value
    candidates = []
    if b == 0:
        x = rational_sqrt(a)
        y = rational_sqrt(a/Q(33))
        if x is not None:
            candidates.append((x, Q(0)))
        if y is not None:
            candidates.append((Q(0), y))
    else:
        n = rational_sqrt(a*a - 33*b*b)
        if n is not None:
            for x_squared in ((a+n)/2, (a-n)/2):
                x = rational_sqrt(x_squared)
                if x not in (None, 0):
                    candidates.append((x, b/(2*x)))
    for candidate in candidates:
        require(rmul(candidate, candidate) == value, ("false square", value, candidate))
    return bool(candidates)


def embed_real(value):
    return value[0], value[1], Q(0), Q(0)


def read_points():
    raw = POINTS.read_bytes()
    require(sha256(raw).hexdigest() ==
            "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
            "coordinate hash")
    points = []
    for line in raw.decode().splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        require(len(row) == 16, "coordinate width")
        require(all(row[i] == 0 for i in range(16) if i not in (0, 5, 9, 12)),
                "point outside stated field")
        points.append(tuple(Q(row[i], 12) for i in (0, 5, 9, 12)))
    require(len(points) == len(set(points)) == 159 and points[0] == ZERO,
            "source point set")
    return points


def strict_edges(points):
    edges = []
    for high, point in enumerate(points):
        for low, other in enumerate(points[:high]):
            if norm(add(point, neg(other))) == RONE:
                edges.append((low, high))
    return edges


def read_library(path, count, edges, digest):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == digest, ("library hash", path.name))
    rows = [tuple(map(int, line)) for line in raw.decode().splitlines()]
    require(rows and all(len(row) == count and row[0] == 0 for row in rows),
            ("library shape", path.name))
    require(all(all(color in range(4) for color in row) for row in rows),
            ("library colors", path.name))
    require(all(all(row[i] != row[j] for i, j in edges) for row in rows),
            ("monochromatic internal edge", path.name))
    return rows


def enumerate_parity(B, A, reflected, classification):
    moving = [conj(point) for point in A] if reflected else A
    norms_b = [norm(point) for point in B]
    norms_a = [norm(point) for point in moving]
    groups = defaultdict(list)
    counts = Counter()
    identities = 0
    for i in range(1, len(B)):
        for j in range(1, len(A)):
            S = radd(radd(norms_b[i], norms_a[j]), (-Q(1), Q(0)))
            delta = radd(rscale(rmul(norms_b[i], norms_a[j]), 4), rneg(rmul(S, S)))
            sign = real_sign(delta)
            if sign < 0:
                case = "no_unit_roots"
            elif square_in_real_field(rscale(delta, Q(1, 3))):
                case = "roots_in_E"
            else:
                require(sign > 0, ("unclassified double root", i, j))
                case = "outside_E_pairs"
                c = mul(conj(B[i]), moving[j])
                cinv = inverse(c)
                middle = mul(embed_real(S), cinv)
                constant = mul(conj(c), cinv)
                key = middle, constant
                # Check the monic polynomial's discriminant identity exactly.
                lhs = add(mul(middle, middle), neg(tuple(4*x for x in constant)))
                rhs = mul(embed_real(rneg(delta)), mul(cinv, cinv))
                require(lhs == rhs, ("quadratic discriminant", i, j))
                identities += 1
                groups[key].append((i, j))
            counts[case] += 1
            classification.update(f"{int(reflected)}:{i},{j}:{case}\n".encode())
    return counts, groups, identities


def main():
    # Basis-product controls make the coordinate convention explicit.
    s = (Q(0), Q(1), Q(0), Q(0))
    p = (Q(0), Q(0), Q(1), Q(0))
    q = (Q(0), Q(0), Q(0), Q(1))
    require(mul(s, s) == (Q(33), Q(0), Q(0), Q(0)), "s^2")
    require(mul(p, p) == (Q(-3), Q(0), Q(0), Q(0)), "p^2")
    require(mul(q, q) == (Q(-11), Q(0), Q(0), Q(0)), "q^2")
    require(mul(s, p) == tuple(3*x for x in q), "sp=3q")
    require(mul(p, q) == neg(s), "pq=-s")

    A = read_points()
    t = (Q(5, 6), Q(0), Q(0), Q(1, 6))
    require(norm(t) == RONE, "inner multiplier")
    tA = [mul(t, point) for point in A]
    B = list(dict.fromkeys(A + tA))
    require(len(B) == 292 and len(set(A) & set(tA)) == 26 and B[0] == ZERO,
            "inner overlap")
    EA, EB = strict_edges(A), strict_edges(B)
    require((len(EA), len(EB)) == (646, 1251), "strict component edges")
    labels = {point: i for i, point in enumerate(B)}
    inherited = set(EA) | {
        tuple(sorted((labels[tA[i]], labels[tA[j]]))) for i, j in EA
    }
    require(len(set(EB) - inherited) == 18, "new inner cross edges")

    lib_a = read_library(TARGET / "colors_A.txt", len(A), EA, EXPECTED_A_LIBRARY)
    lib_b = read_library(TARGET / "colors_B.txt", len(B), EB, EXPECTED_B_LIBRARY)
    require((len(lib_a), len(lib_b)) == (5, 3), "library row counts")
    color_permutations = [(0,) + tail for tail in permutations((1, 2, 3))]

    classification = sha256()
    partition = sha256()
    summaries = []
    distinct_edge_sets = set()
    covered = 0
    identity_checks = 0
    for reflected in (False, True):
        counts, groups, identities = enumerate_parity(B, A, reflected, classification)
        identity_checks += identities
        require(counts == {
            "no_unit_roots": 5747,
            "roots_in_E": 22966,
            "outside_E_pairs": 17265,
        }, ("classification counts", reflected, counts))
        require(len(groups) == (2216 if reflected else 2391),
                ("quadratic class count", reflected, len(groups)))
        canonical_groups = sorted(tuple(sorted(edges)) for edges in groups.values())
        for edges in canonical_groups:
            partition.update((f"{int(reflected)}:" +
                              ";".join(f"{i},{j}" for i, j in edges) + "\n").encode())
            witness = next((
                (bi, ai, pi)
                for bi, cb in enumerate(lib_b)
                for ai, ca in enumerate(lib_a)
                for pi, permutation in enumerate(color_permutations)
                if all(cb[b] != permutation[ca[a]] for b, a in edges)
            ), None)
            require(witness is not None, ("uncovered class", reflected, edges[:3]))
            covered += 1
            distinct_edge_sets.add(edges)
        histogram = Counter(map(len, groups.values()))
        summaries.append((int(reflected), len(groups), min(histogram), max(histogram)))

    require(classification.hexdigest() == EXPECTED_CLASSIFICATION,
            ("classification digest", classification.hexdigest()))
    require(partition.hexdigest() == EXPECTED_PARTITION,
            ("partition digest", partition.hexdigest()))
    require((covered, len(distinct_edge_sets), identity_checks) == (4607, 4605, 34530),
            ("coverage totals", covered, len(distinct_edge_sets), identity_checks))

    print("PASS source geometry: A=159/646 B=292/1251 overlap=26 inner-new-edges=18")
    print("PASS independent four-coordinate field arithmetic and exact square test")
    for reflected, classes, minimum, maximum in summaries:
        parity = "reflection" if reflected else "rotation"
        print(f"PASS {parity}: pairs=45978 outside-pairs=17265 classes={classes} edge-range={minimum}..{maximum}")
    print(f"PASS all {covered} outside-field classes have explicit four-color witnesses")
    print(f"PASS quadratic discriminant identities={identity_checks} distinct-edge-sets={len(distinct_edge_sets)}")
    print(f"classification_sha256={classification.hexdigest()}")
    print(f"edge_partition_sha256={partition.hexdigest()}")
    print("SCOPE excludes this fixed-inner-placement family; no sub-509 graph is constructed")


if __name__ == "__main__":
    main()
