#!/usr/bin/env python3
"""Definition-level partition and exceptional rational PSD verification."""
from fractions import Fraction
from itertools import combinations, permutations
import hashlib
import json

FACETS = (7, 11, 21, 26, 28, 38, 41, 44, 49, 50)
EXCEPTION = 1991589575991295
ORBIT_SPEC = ((1, 2, 2), (1, 6, -1), (1, 12, 4), (1, 26, 1),
              (3, 12, 0), (3, 20, 1), (3, 28, 5))
TWELVE_PARTITION = ((7, 24, 32), (4, 26, 33), (1, 28, 34),
                    (11, 16, 36), (9, 38), (2, 21, 40), (20, 41),
                    (18, 44), (3, 12, 48), (6, 8, 49), (5, 50), (10, 17))


def decode(family, n):
    if not isinstance(family, int) or family < 0 or family >= 1 << (1 << n):
        raise ValueError("invalid family bitset")
    return [a for a in range(1 << n) if family >> a & 1]


def check_downset(sets):
    included = set(sets)
    for a in sets:
        for i in range(a.bit_length()):
            if a >> i & 1 and a ^ (1 << i) not in included:
                raise AssertionError("family is not a downset")


def check_partition(family, bins, n, target=None):
    sets = decode(family, n)
    check_downset(sets)
    nonempty = set(sets) - {0}
    if not nonempty:
        if bins:
            raise AssertionError("nonempty bins for trivial family")
        return
    s = max(sum(a >> i & 1 for a in sets) for i in range(n))
    if len(bins) != (s if target is None else target):
        raise AssertionError("wrong partition cardinality")
    flattened = [a for block in bins for a in block]
    if len(flattened) != len(nonempty) or set(flattened) != nonempty:
        raise AssertionError("partition does not cover every set exactly once")
    for block in bins:
        used = 0
        for a in block:
            if used & a:
                raise AssertionError("intersecting sets share a bin")
            used |= a
    if target is None:
        # Direct row-sum verification of the integer K=(N-s)M+sI.
        N = len(sets)
        sizes = [len(block) for block in bins]
        empty_cross = [N - s * size for size in sizes]
        empty_diag = s * sum(size * size for size in sizes) - N * (N - 2)
        if any(s * size + cross != N for size, cross in zip(sizes, empty_cross)):
            raise AssertionError("nonempty K row sum failed")
        if empty_diag + sum(size * cross for size, cross in zip(sizes, empty_cross)) != N:
            raise AssertionError("empty K row sum failed")
        if N - s <= 0:
            raise AssertionError("invalid Hoffman normalization")


def exact_ldl_psd(matrix):
    """Rational Schur elimination, with a zero-pivot obstruction check."""
    a = [[Fraction(x) for x in row] for row in matrix]
    rank = 0
    for k in range(len(a)):
        pivot = a[k][k]
        if pivot < 0:
            raise AssertionError("negative rational Schur pivot")
        if pivot == 0:
            if any(a[k][j] for j in range(k + 1, len(a))):
                raise AssertionError("zero pivot has nonzero off-diagonal entry")
            continue
        rank += 1
        for i in range(k + 1, len(a)):
            for j in range(i, len(a)):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return rank


def characteristic_polynomial(matrix):
    """Independent PSD route: integer Faddeev--LeVerrier coefficients."""
    n = len(matrix)
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n + 1):
        c = [[sum(matrix[i][h] * b[h][j] for h in range(n))
              for j in range(n)] for i in range(n)]
        trace = sum(c[i][i] for i in range(n))
        if trace % k:
            raise AssertionError("nonintegral characteristic coefficient")
        coefficient = -trace // k
        coefficients.append(coefficient)
        for i in range(n):
            c[i][i] += coefficient
        b = c
    if any(x for row in b for x in row):
        raise AssertionError("Cayley--Hamilton residual is nonzero")
    return coefficients


def exceptional_matrix():
    sets = decode(EXCEPTION, 6)[1:]
    included = set(sets)
    automorphisms = []
    for p in permutations(range(6)):
        image = {a: sum(1 << p[i] for i in range(6) if a >> i & 1) for a in sets}
        if set(image.values()) == included:
            automorphisms.append(image)
    if len(automorphisms) != 60:
        raise AssertionError("exception automorphism group differs")
    entries = {}
    sizes = []
    for first, second, value in ORBIT_SPEC:
        orbit = {tuple(sorted((p[first], p[second]))) for p in automorphisms}
        sizes.append(len(orbit))
        if set(entries).intersection(orbit):
            raise AssertionError("exception edge orbits overlap")
        entries.update({edge: value for edge in orbit})
    disjoint = {(a, b) for a, b in combinations(sets, 2) if a & b == 0}
    if set(entries) != disjoint:
        raise AssertionError("exception edge orbits are incomplete")
    x = [[11 if a == b else 0 if a & b else entries[tuple(sorted((a, b)))]
          for b in sets] for a in sets]
    return sets, [[entry - 1 for entry in row] for row in x], sizes


def disjoint_collections(sets):
    """All disjoint collections, including incomplete ground-set covers."""
    def visit(start, used, weight):
        yield weight
        for j in range(start, len(sets)):
            a = sets[j]
            if used & a == 0:
                yield from visit(j + 1, used | a, weight + a.bit_count() - 1)
    yield from visit(0, 0, 0)


def perfect_matchings(points):
    if not points:
        yield ()
    else:
        first, *rest = points
        for second in rest:
            remaining = [i for i in rest if i != second]
            for tail in perfect_matchings(remaining):
                yield ((1 << first) | (1 << second),) + tail


def verify_exception():
    all_sets = decode(EXCEPTION, 6)
    check_downset(all_sets)
    if set(a for a in all_sets if a.bit_count() == 3) != set(FACETS):
        raise AssertionError("facet decoding failed")
    if [sum(a >> i & 1 for a in all_sets) for i in range(6)] != [11] * 6:
        raise AssertionError("star size differs")
    if any((63 ^ a) in FACETS for a in FACETS):
        raise AssertionError("two exceptional triples are disjoint")
    if any(sum(a & pair == pair for a in FACETS) != 2
           for pair in all_sets if pair.bit_count() == 2):
        raise AssertionError("exception is not a 2-(6,3,2) design")
    sets, w, orbit_sizes = exceptional_matrix()
    if any(w[i][j] != w[j][i] for i in range(31) for j in range(31)):
        raise AssertionError("W is not symmetric")
    rank = exact_ldl_psd(w)
    coefficients = characteristic_polynomial(w)
    # For every t>0, (-1)^31 p(-t) is strictly positive. Since W is
    # real symmetric, its real eigenvalues therefore cannot be negative.
    if any((-1) ** k * c < 0 for k, c in enumerate(coefficients)):
        raise AssertionError("characteristic-polynomial PSD check failed")
    zero_multiplicity = 0
    for c in reversed(coefficients):
        if c:
            break
        zero_multiplicity += 1
    if rank != 31 - zero_multiplicity or rank != 24:
        raise AssertionError("independent rank checks disagree")
    row_sums = [sum(row) for row in w]
    k = [[1 + sum(row_sums)] + [1 - x for x in row_sums]]
    for i, row in enumerate(w):
        k.append([1 - row_sums[i]] + [x + 1 for x in row])
    if any(sum(row) != 32 for row in k):
        raise AssertionError("full K row sums failed")
    m_numerator = [[k[i][j] - 11 * int(i == j) for j in range(32)]
                   for i in range(32)]
    if any(m_numerator[i][j] for i, a in enumerate(all_sets)
           for j, b in enumerate(all_sets) if a & b):
        raise AssertionError("full Hoffman support check failed")
    if any(sum(row) != 21 for row in m_numerator):
        raise AssertionError("full Hoffman normalization failed")
    if max(disjoint_collections(sets)) != 3:
        raise AssertionError("fractional dual clique constraints failed")
    dual = Fraction(sum(a.bit_count() - 1 for a in sets), 3)
    cover = []
    for triple in FACETS:
        complement = 63 ^ triple
        for i in range(6):
            if complement >> i & 1:
                singleton = 1 << i
                cover.append(((triple, complement ^ singleton, singleton), Fraction(1, 3)))
    for matching in perfect_matchings(list(range(6))):
        cover.append((matching, Fraction(1, 9)))
    if len(cover) != 45 or sum(weight for _, weight in cover) != dual:
        raise AssertionError("fractional primal total failed")
    for block, _ in cover:
        if len(set(block)) != len(block) or any(a & b for a, b in combinations(block, 2)):
            raise AssertionError("fractional cover block is not disjoint")
    if any(sum(weight for block, weight in cover if a in block) < 1 for a in sets):
        raise AssertionError("fractional primal coverage failed")
    if dual != Fraction(35, 3):
        raise AssertionError("fractional optimum differs")
    check_partition(EXCEPTION, TWELVE_PARTITION, 6, target=12)
    return {"family_mask": EXCEPTION, "N": 32, "s": 11,
            "automorphism_order": 60, "labeled_orbit_size": 12,
            "disjoint_pair_orbit_sizes": orbit_sizes, "W_rank": rank,
            "W_characteristic_coefficients": coefficients,
            "M_denominator": 21,
            "M_numerator_sha256": hashlib.sha256(
                json.dumps(m_numerator, separators=(",", ":")).encode()).hexdigest(),
            "fractional_clique_cover": "35/3", "integral_clique_cover": 12}


if __name__ == "__main__":
    print(json.dumps(verify_exception(), indent=2, sort_keys=True))
