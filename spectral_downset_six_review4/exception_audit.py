#!/usr/bin/env python3
"""Independent direct-formula matrix and fractional audit of the six-point case."""
from fractions import Fraction
from itertools import permutations
import hashlib
import json

FACETS = ((1, 2, 3), (1, 2, 4), (1, 3, 5), (2, 4, 5), (3, 4, 5),
          (2, 3, 6), (1, 4, 6), (3, 4, 6), (1, 5, 6), (2, 5, 6))
TWELVE = ((7, 24, 32), (4, 26, 33), (1, 28, 34), (11, 16, 36),
          (9, 38), (2, 21, 40), (20, 41), (18, 44), (3, 12, 48),
          (6, 8, 49), (5, 50), (10, 17))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def inertia(matrix):
    """Exact symmetric congruence, allowing both one- and two-dimensional pivots."""
    need(all(len(row) == len(matrix) for row in matrix), "square matrix")
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(matrix)) for j in range(len(matrix))), "symmetry")
    a = [[Fraction(v) for v in row] for row in matrix]
    positive = negative = zeros = two_pivots = 0
    while a:
        n = len(a)
        k = next((i for i in range(n) if a[i][i]), None)
        if k is not None:
            order = [k] + [i for i in range(n) if i != k]
            a = [[a[i][j] for j in order] for i in order]
            pivot = a[0][0]
            positive += pivot > 0
            negative += pivot < 0
            a = [[a[i][j] - a[i][0] * a[0][j] / pivot
                  for j in range(1, n)] for i in range(1, n)]
            continue
        pair = next(((i, j) for i in range(n) for j in range(i + 1, n)
                     if a[i][j]), None)
        if pair is None:
            zeros += n
            break
        i, j = pair
        order = [i, j] + [h for h in range(n) if h not in pair]
        a = [[a[r][s] for s in order] for r in order]
        off = a[0][1]
        # The pivot [[0,off],[off,0]] has one eigenvalue of each sign.
        positive += 1
        negative += 1
        two_pivots += 1
        a = [[a[r][s] - (a[r][0] * a[1][s] + a[r][1] * a[0][s]) / off
              for s in range(2, n)] for r in range(2, n)]
    return {"positive": positive, "negative": negative, "zero": zeros,
            "two_by_two_pivots": two_pivots}


def family():
    triples = {sum(1 << (i - 1) for i in t) for t in FACETS}
    members = [a for a in range(64) if a.bit_count() <= 2 or a in triples]
    return members, triples


def numerator(members, triples):
    """Use rank and induced-triple counts, without any automorphism edge orbit."""
    q = []
    for a in members:
        row = []
        for b in members:
            if not a and not b:
                value = 30
            elif not a or not b:
                value = {1: -9, 2: 1, 3: 3}[(a or b).bit_count()]
            elif a & b:
                value = 0
            else:
                x, y = sorted((a, b), key=lambda m: m.bit_count())
                sizes = (x.bit_count(), y.bit_count())
                if sizes == (1, 1):
                    value = 2
                elif sizes == (1, 2):
                    value = -1 if x | y in triples else 4
                elif sizes == (1, 3):
                    value = 1
                elif sizes == (2, 2):
                    union = x | y
                    incident = sum(t & x == x and t & union == t for t in triples)
                    value = 0 if incident in (0, 2) else 1
                elif sizes == (2, 3):
                    value = 5
                else:
                    raise ValueError("unexpected disjoint ranks")
            row.append(value)
        q.append(row)
    return q


def point_partitions(n):
    """Restricted-growth strings enumerate each set partition exactly once."""
    def visit(labels, largest):
        if len(labels) == n:
            blocks = [0] * (largest + 1)
            for i, c in enumerate(labels):
                blocks[c] |= 1 << i
            yield blocks
        else:
            for c in range(largest + 2):
                yield from visit(labels + [c], max(largest, c))
    yield from visit([0], 0)


def check_partition(members, bins):
    flattened = [a for b in bins for a in b]
    need(len(flattened) == len(set(flattened))
         and set(flattened) == set(members) - {0}, "partition coverage")
    for block in bins:
        used = 0
        for a in block:
            need(not used & a, "partition intersections")
            used |= a


def run():
    need(inertia([[0, 1], [1, 0]]) == {
        "positive": 1, "negative": 1, "zero": 0, "two_by_two_pivots": 1},
        "zero diagonal indefinite control")
    need(inertia([[1, 1], [1, 1]])["zero"] == 1, "singular PSD control")
    members, triples = family()
    mask = sum(1 << a for a in members)
    need(len(members) == 32 and mask == 1991589575991295, "facet decoding")
    for a in members:
        for i in range(6):
            if a & (1 << i):
                need(a ^ (1 << i) in members, "downset")
    need(all(sum(a & (1 << i) != 0 for a in members) == 11 for i in range(6)),
         "largest stars")
    need(all(sum(t & a == a for t in triples) == 2
             for a in members if a.bit_count() == 2), "design pair degrees")
    need(all(63 ^ t not in triples for t in triples), "no complementary triples")
    q = numerator(members, triples)
    need(all(q[i][j] == q[j][i] for i in range(32) for j in range(32)), "Q symmetry")
    need(all(q[i][j] == 0 for i, a in enumerate(members)
             for j, b in enumerate(members) if a & b), "Q support")
    need(all(sum(row) == 21 for row in q), "Q normalization")
    digest = hashlib.sha256(json.dumps(q, separators=(",", ":")).encode()).hexdigest()
    need(digest == "d8a47ca6c5b9513ef624d7467231347ee3da2ae99877f7d26c5fab140fc18b02",
         "matrix agrees with committed orbit prescription")
    k = [[q[i][j] + 11 * (i == j) for j in range(32)] for i in range(32)]
    ik = inertia(k)
    need(ik["negative"] == 0, "full Hoffman PSD")
    w = [[q[i + 1][j + 1] + 11 * (i == j) - 1
          for j in range(31)] for i in range(31)]
    iw = inertia(w)
    need(iw["negative"] == 0 and iw["positive"] == 24, "auxiliary PSD/rank")
    nonempty = [row[1:] for row in q[1:]]
    iq = inertia(nonempty)
    # For inertia Conjecture I, use the same nonempty block and an isolated
    # negative loop at the empty vertex. Row stochasticity is not an I premise.
    i_nonnegative = iq["positive"] + iq["zero"]
    # Dynamic programming checks ALL disjoint collections, including ones
    # that leave ground-set elements unused. Weights are scaled by three.
    best = [0] * 64
    for available in range(1, 64):
        first = available & -available
        values = [best[available ^ first]]
        values += [a.bit_count() - 1 + best[available ^ a]
                   for a in members if a and a & first and a & available == a]
        best[available] = max(values)
    need(max(best) == 3, "complete fractional dual constraints")
    scaled_dual = sum(a.bit_count() - 1 for a in members if a)
    need(scaled_dual == 35, "fractional dual total")
    partitions = list(point_partitions(6))
    need(len(partitions) == 203, "complete Bell set partition count")
    cover = []
    for blocks in partitions:
        sizes = sorted(a.bit_count() for a in blocks)
        if sizes == [1, 2, 3] and all(a in members for a in blocks):
            cover.append((blocks, 3))
        elif sizes == [2, 2, 2]:
            cover.append((blocks, 1))
    need(len(cover) == 45 and sum(c for _, c in cover) == 105,
         "scaled fractional primal total")
    coverage = {a: sum(c for blocks, c in cover if a in blocks)
                for a in members if a}
    need(min(coverage.values()) >= 9, "fractional primal coverage")
    need(set(coverage[a] for a in coverage if a.bit_count() in (2, 3)) == {9}
         and set(coverage[a] for a in coverage if a.bit_count() == 1) == {15},
         "rank-wise exact cover loads")
    check_partition(members, TWELVE)
    automorphisms = 0
    orbit = set()
    for p in permutations(range(6)):
        image = [sum(1 << p[i] for i in range(6) if a & (1 << i)) for a in members]
        image_mask = sum(1 << a for a in image)
        orbit.add(image_mask)
        automorphisms += image_mask == mask
    need(automorphisms == 60 and len(orbit) == 12, "full point orbit")
    return {"family_mask": mask, "N": 32, "s": 11, "automorphisms": 60,
            "labeled_orbit_size": 12, "matrix_sha256": digest,
            "hoffman_full_inertia": ik, "auxiliary_inertia": iw,
            "nonempty_numerator_inertia": iq,
            "tested_inertia_matrix_nonnegative_eigenvalues": i_nonnegative,
            "tested_inertia_matrix_tight": i_nonnegative == 11,
            "fractional_value": "35/3", "fractional_DP_states": 64,
            "point_partitions_checked": 203, "fractional_cover_cliques": 45,
            "integral_cover_number": 12}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
