#!/usr/bin/env python3
"""Independent exact checks for the five-generator tangent-cone review.

This file deliberately imports no code from the reviewed package.  It checks
the chain-level conventions on a finite census and separately checks the
six-vertex projective-plane obstruction used by the universal proof.
Python 3.11+; standard library only.
"""

from fractions import Fraction
from itertools import combinations, permutations
import hashlib
import json
from math import gcd


TARGET_COMMIT = "5a2cf36615c2d8adc728ba4f5db96787e15f2b95"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def closure(facets):
    answer = {0}
    for facet in facets:
        sub = facet
        while True:
            answer.add(sub)
            if sub == 0:
                break
            sub = (sub - 1) & facet
    return frozenset(answer)


def mask(vertices):
    return sum(1 << v for v in vertices)


def facets(faces):
    return frozenset(
        face for face in faces
        if not any(face != other and face & other == face for other in faces)
    )


def permute_face(face, permutation):
    return sum(1 << permutation[v] for v in range(len(permutation)) if face & (1 << v))


def projective_plane_models():
    # The ten facets in Govc--Marzantowicz--Michalak--Pavesic, Theorem 3.6.
    source = closure(mask(v - 1 for v in tri) for tri in (
        (1, 2, 3), (1, 2, 4), (1, 5, 6), (2, 5, 6), (2, 4, 5),
        (1, 3, 5), (1, 4, 6), (3, 4, 6), (2, 3, 6), (3, 4, 5),
    ))
    models = {
        tuple(sorted(permute_face(face, p) for face in source))
        for p in permutations(range(6))
    }
    require(len(models) == 12, "unexpected number of labelled RP2 models")
    return source, models


def boundary_matrix(relative_faces, source_size):
    columns = sorted(face for face in relative_faces if face.bit_count() == source_size)
    row_faces = sorted(face for face in relative_faces if face.bit_count() == source_size - 1)
    rows = {face: i for i, face in enumerate(row_faces)}
    matrix = [[0] * len(columns) for _ in row_faces]
    for col, face in enumerate(columns):
        position = 0
        for vertex in range(6):
            bit = 1 << vertex
            if face & bit:
                lower = face ^ bit
                if lower in rows:
                    matrix[rows[lower]][col] = -1 if position % 2 else 1
                position += 1
    return matrix


def determinant_bareiss(matrix):
    work = [row[:] for row in matrix]
    n = len(work)
    require(all(len(row) == n for row in work), "determinant needs a square matrix")
    sign = 1
    previous = 1
    for col in range(n - 1):
        pivot = next((row for row in range(col, n) if work[row][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            sign = -sign
        value = work[col][col]
        for row in range(col + 1, n):
            for k in range(col + 1, n):
                numerator = work[row][k] * value - work[row][col] * work[col][k]
                require(numerator % previous == 0, "nonexact Bareiss division")
                work[row][k] = numerator // previous
        previous = value
    return sign * work[-1][-1]


def rank(matrix, characteristic):
    if not matrix or not matrix[0]:
        return 0
    if characteristic == 0:
        work = [[Fraction(value) for value in row] for row in matrix]
    else:
        work = [[value % characteristic for value in row] for row in matrix]
    pivot_row = 0
    for col in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work)) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][col]
        inverse = 1 / value if characteristic == 0 else pow(value, -1, characteristic)
        work[pivot_row] = [
            entry * inverse if characteristic == 0 else entry * inverse % characteristic
            for entry in work[pivot_row]
        ]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            value = work[row][col]
            if value:
                work[row] = [
                    a - value * b if characteristic == 0 else (a - value * b) % characteristic
                    for a, b in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def topology_check(rp2):
    checked_partitions = 0
    determinants = []
    ranks = []
    for apex in range(6):
        apex_bit = 1 << apex
        remaining = 63 ^ apex_bit
        deletion = frozenset(face for face in rp2 if not face & apex_bit)
        link = frozenset(face ^ apex_bit for face in rp2 if face & apex_bit)
        link_facets = facets(link)
        deletion_facets = facets(deletion)
        edges = frozenset(face for face in link_facets if face.bit_count() == 2)
        triangles = frozenset(face for face in deletion_facets if face.bit_count() == 3)
        require(link_facets == edges and len(edges) == 5, "link is not a five-cycle")
        require(deletion_facets == triangles and len(triangles) == 5,
                "deletion does not have five triangular facets")
        nonedges = {
            pair for pair in range(64)
            if pair & apex_bit == 0 and pair.bit_count() == 2 and pair not in edges
        }
        require(triangles == {remaining ^ pair for pair in nonedges},
                "deletion facets are not complements of cycle nonedges")

        # H is the weak-high set.  The proof says an edge cannot lie in H,
        # while some deletion triangle is disjoint from every independent H.
        for high in range(64):
            if high & apex_bit:
                continue
            if all(edge & high != edge for edge in edges):
                require(any(triangle & high == 0 for triangle in triangles),
                        "threshold obstruction failed")
            checked_partitions += 1

        relative = deletion - link
        matrix = boundary_matrix(relative, 3)
        require(len(matrix) == 5 and all(len(row) == 5 for row in matrix),
                "unexpected RP2 relative boundary size")
        determinants.append(abs(determinant_bareiss(matrix)))
        ranks.append((rank(matrix, 0), rank(matrix, 2), rank(matrix, 3)))

    require(checked_partitions == 192, "wrong threshold-partition count")
    require(set(determinants) == {2}, "RP2 determinant is not +/-2")
    require(set(ranks) == {(5, 4, 5)}, "RP2 field ranks are wrong")
    return checked_partitions


def maximum_lengths(generators, bound):
    values = [-1] * (bound + 1)
    values[0] = 0
    for value in range(1, bound + 1):
        prior = [values[value - g] for g in generators if g <= value and values[value - g] >= 0]
        if prior:
            values[value] = 1 + max(prior)
    return values


def is_minimal_numerical_generating_set(generators):
    if gcd(*generators) != 1:
        return False
    for index, value in enumerate(generators):
        others = generators[:index] + generators[index + 1:]
        if maximum_lengths(others, value)[value] >= 0:
            return False
    return True


def boundary_entries(faces, weights, generators, orders, s, j, direct):
    answer = []
    for face in sorted(faces):
        residual = s - sum(generators[v] for v in range(5) if face & (1 << v))
        position = 0
        for vertex in range(5):
            bit = 1 << vertex
            if not face & bit:
                continue
            lower = face ^ bit
            if direct:
                survives = orders[residual + generators[vertex]] == orders[residual] + 1
            else:
                survives = weights.get(lower) == j
            if survives:
                answer.append((lower, face, -1 if position % 2 else 1))
            position += 1
    return tuple(answer)


def absolute_complex(delta, lower, apex=5):
    if not lower:
        return delta
    return frozenset(delta | lower | {face | (1 << apex) for face in lower})


def chain_census(rp2_models):
    semigroups = [
        generators for generators in combinations(range(5, 14), 5)
        if is_minimal_numerical_generating_set(generators)
    ]
    bound = 100
    strands = 0
    complexes = 0
    rp2_hits = 0
    transcript = hashlib.sha256()
    for generators in semigroups:
        orders = maximum_lengths(generators, bound)
        face_sums = {
            face: sum(generators[v] for v in range(5) if face & (1 << v))
            for face in range(32)
        }
        for s in range(bound + 1):
            weights = {
                face: orders[s - total] + face.bit_count()
                for face, total in face_sums.items()
                if total <= s and orders[s - total] >= 0
            }
            for j in sorted(set(weights.values())):
                exact = frozenset(face for face, value in weights.items() if value == j)
                direct = boundary_entries(exact, weights, generators, orders, s, j, True)
                relative = boundary_entries(exact, weights, generators, orders, s, j, False)
                require(direct == relative,
                        f"chain mismatch for {generators}, s={s}, j={j}")
                strands += 1

                delta = frozenset(face for face, value in weights.items() if value >= j)
                lower = frozenset(face for face, value in weights.items() if value >= j + 1)
                complex_faces = absolute_complex(delta, lower)
                fingerprint = tuple(sorted(complex_faces))
                if fingerprint in rp2_models:
                    rp2_hits += 1
                transcript.update(repr((generators, s, j, direct, fingerprint)).encode())
                complexes += 1
    require(rp2_hits == 0, "an attainable absolute complex is RP2")
    return {
        "five_generator_semigroups": len(semigroups),
        "s_bound_checked": bound,
        "chain_strands": strands,
        "absolute_complexes": complexes,
        "attainable_rp2_hits": rp2_hits,
        "transcript_sha256": transcript.hexdigest(),
    }


def main():
    rp2, models = projective_plane_models()
    partitions = topology_check(rp2)
    result = {
        "target_commit": TARGET_COMMIT,
        "projective_plane_labelings": len(models),
        "projective_plane_apices": 6,
        "threshold_partitions": partitions,
        "relative_boundary_abs_det": 2,
        "relative_boundary_ranks_Q_F2_F3": [5, 4, 5],
        **chain_census(models),
        "status": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
