#!/usr/bin/env python3
"""Independent exact controls for the effective indecomposable bound.

This file imports no author module or expected record.  It checks the generic
rational repair algebra on fixtures unrelated to the submitted eight-cone
example, reconstructs the combinatorial bounds, and audits the defect handoff.
"""

from fractions import Fraction as Q
from itertools import combinations
from math import ceil, comb, isqrt


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c * a for a in x)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def mat_vec(a, x):
    return tuple(dot(row, x) for row in a)


def transpose(a):
    return tuple(tuple(a[j][i] for j in range(3)) for i in range(3))


def affine(a, c, x):
    return add(mat_vec(a, x), c)


def dist2(x, y):
    return dot(sub(x, y), sub(x, y))


def bisector_reflection(a, ap, x):
    n = sub(ap, a)
    nn = dot(n, n)
    require(nn != 0, "degenerate repair fixture")
    coefficient = (2 * dot(n, x) - dot(ap, ap) + dot(a, a)) / nn
    return sub(x, scale(coefficient, n))


def orthogonal_basis(n):
    """Return two rational, independent vectors perpendicular to nonzero n."""
    if n[0] != 0:
        u = (-n[1], n[0], Q(0))
        v = (-n[2], Q(0), n[0])
    elif n[1] != 0:
        u = (Q(1), Q(0), Q(0))
        v = (Q(0), -n[2], n[1])
    else:
        u = (Q(1), Q(0), Q(0))
        v = (Q(0), Q(1), Q(0))
    require(dot(n, u) == dot(n, v) == 0, "bad bisector basis")
    require(dot(u, u) * dot(v, v) != dot(u, v) ** 2, "dependent basis")
    return u, v


def audit_repairs():
    # Signed-permutation isometries, rational translations, and independently
    # chosen repair endpoints.  The submitted checker uses a single absolute-
    # value fold and central cross-polytope instead.
    fixtures = [
        (((1, 0, 0), (0, 1, 0), (0, 0, 1)),
         (Q(2, 7), Q(-3, 8), Q(5, 11)),
         (Q(-1, 3), Q(2, 5), Q(4, 9)),
         (Q(5, 6), Q(-2, 9), Q(7, 10))),
        (((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
         (Q(-4, 13), Q(7, 12), Q(1, 5)),
         (Q(3, 8), Q(-5, 7), Q(2, 9)),
         (Q(-1, 4), Q(6, 11), Q(5, 12))),
        (((0, 0, 1), (-1, 0, 0), (0, -1, 0)),
         (Q(9, 14), Q(-2, 15), Q(3, 10)),
         (Q(-4, 9), Q(1, 6), Q(5, 8)),
         (Q(7, 13), Q(2, 7), Q(-3, 11))),
        (((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
         (Q(1, 17), Q(4, 9), Q(-7, 16)),
         (Q(2, 3), Q(-1, 8), Q(3, 7)),
         (Q(-5, 12), Q(7, 10), Q(1, 9))),
    ]
    identity_entries = 0
    boundary_checks = 0
    radial_checks = 0
    distance_checks = 0

    for raw_a, c, a, ap in fixtures:
        matrix = tuple(tuple(Q(x) for x in row) for row in raw_a)
        # Choose b so that ap=S^{-1}(b), exactly as in the proof.
        b = affine(matrix, c, ap)
        require(affine(transpose(matrix), scale(Q(-1), mat_vec(transpose(matrix), c)), b) == ap,
                "inverse isometry mismatch")

        midpoint = scale(Q(1, 2), add(a, ap))
        u, v = orthogonal_basis(sub(ap, a))
        boundary = [midpoint, add(midpoint, u), add(midpoint, v),
                    add(midpoint, add(scale(Q(2, 3), u), scale(Q(-5, 7), v)))]

        # G=S o rho is the repaired cone isometry.  Recover its affine
        # columns by evaluation, without copying the author's matrix formula.
        g0 = affine(matrix, c, bisector_reflection(a, ap, (Q(0), Q(0), Q(0))))
        columns = []
        for i in range(3):
            e = tuple(Q(j == i) for j in range(3))
            columns.append(sub(affine(matrix, c, bisector_reflection(a, ap, e)), g0))
        gmat = transpose(tuple(columns))
        gram = tuple(tuple(sum(gmat[k][i] * gmat[k][j] for k in range(3))
                           for j in range(3)) for i in range(3))
        for i in range(3):
            for j in range(3):
                require(gram[i][j] == Q(i == j), "repaired map not orthogonal")
                identity_entries += 1

        require(affine(gmat, g0, a) == b, "repair does not send a to b")
        for z in boundary:
            require(dist2(z, a) == dist2(z, ap), "point misses bisector")
            require(affine(gmat, g0, z) == affine(matrix, c, z),
                    "old and repaired maps disagree on boundary")
            boundary_checks += 1
            for t in (Q(0), Q(1, 7), Q(2, 5), Q(1)):
                y = add(a, scale(t, sub(z, a)))
                expected = add(b, scale(t, sub(affine(matrix, c, z), b)))
                require(affine(gmat, g0, y) == expected,
                        "radial interpolation identity failed")
                radial_checks += 1

        sample = [a] + boundary
        for x, y in combinations(sample, 2):
            require(dist2(x, y) == dist2(affine(gmat, g0, x), affine(gmat, g0, y)),
                    "repaired affine map changes a distance")
            distance_checks += 1

        # Directly check the strict star inequality on a rational interior ray.
        x = add(a, scale(Q(1, 3), sub(a, ap)))
        require(dist2(x, a) < dist2(x, ap), "chosen point is not in Omega")
        for t in (Q(0), Q(1, 11), Q(3, 8), Q(1)):
            y = add(a, scale(t, sub(x, a)))
            if t:
                require(dist2(y, a) < dist2(y, ap), "Omega ray is not star-shaped")

    return len(fixtures), identity_entries, boundary_checks, radial_checks, distance_checks


def arrangement_regions(h, dimension):
    # Generic-region recurrence R(d,h)=R(d,h-1)+R(d-1,h-1), independently
    # accumulated as a Pascal table rather than using the closed form.
    table = [[1] * (h + 1) for _ in range(dimension + 1)]
    for d in range(1, dimension + 1):
        for j in range(1, h + 1):
            table[d][j] = table[d][j - 1] + table[d - 1][j - 1]
    return table[dimension][h]


def h_bound(n):
    return 512 * 2 ** n * (n + 6) + 3 * n + comb(n, 3) + 6


def m_bound(n):
    h = h_bound(n)
    # The recurrence is checked independently below on 81 successive orders;
    # use its closed form here so the very large displayed cases stay cheap.
    return 12 * h * sum(comb(h, j) for j in range(4))


def audit_counts():
    region_checks = 0
    for h in range(81):
        require(arrangement_regions(h, 3) == sum(comb(h, j) for j in range(4)),
                "arrangement count mismatch")
        region_checks += 1

    # Explicit flag counts for three unrelated 3-polytopes.  Each incident
    # edge/facet choice contributes the two endpoint flags, hence 4E flags.
    polyhedra = (("tetrahedron", 6, 4), ("cube", 12, 6), ("octahedron", 12, 8))
    flag_checks = 0
    for _, edges, facets in polyhedra:
        flags = 4 * edges
        require(edges <= 3 * facets - 6, "Euler edge bound failed")
        require(flags <= 12 * facets, "barycentric flag bound failed")
        flag_checks += 1

    displayed = {
        1: 5306422463239896,
        4: 90168788621607057936,
        7: 1054021675129126795053360,
        10: 9904257024005253451602558960,
    }
    for n, expected in displayed.items():
        require(m_bound(n) == expected, "displayed M_N mismatch")
    return region_checks, flag_checks, len(displayed)


def cubature_atoms(k):
    ell = (k - 1).bit_length()
    h = isqrt(ell + 1)
    n = ceil(k / h)
    first = k ** 3 * (2 * comb(2 * ell + 6, 3) - 1)
    second = n ** 3 * (2 * comb(4 * ell + 11, 3) - 1)
    return min(first, second)


def audit_defect_handoff():
    perturbation_checks = 0
    chain_checks = 0
    handoff_checks = 0
    for delta in (Q(1), Q(3, 4), Q(1, 3), Q(1, 17), Q(2, 101)):
        epsilon = delta / (2 * (1 + delta))
        require(-(1 - epsilon) * delta + epsilon == -delta / 2,
                "endpoint perturbation budget failed")
        perturbation_checks += 1
        for m in range(1, 65):
            if m == 1:
                continue
            length = 2 ** (m - 1) - 1
            require(delta / (2 * length) > delta / 2 ** m,
                    "strict chain-gap loss failed")
            require(epsilon / (4 * m) == delta / (8 * m * (1 + delta)),
                    "mesh mass floor failed")
            chain_checks += 1

        k = ceil(6 / delta)
        require(Q(11, 4 * k) < delta / 2, "cubature loss does not leave delta/2")
        n = cubature_atoms(k)
        d = delta / 2
        # Substitute d into d/[8 M(1+d)] without expanding the enormous M_N.
        require(d / (8 * (1 + d)) == delta / (8 * (2 + delta)),
                "consumer mass substitution failed")
        require(4 * 3 < 7 ** 2, "cube diameter is not below 7k")
        require(n >= 1, "empty cubature atom budget")
        handoff_checks += 1
    return perturbation_checks, chain_checks, handoff_checks


def main():
    repairs = audit_repairs()
    counts = audit_counts()
    handoff = audit_defect_handoff()
    print("INDEPENDENT_EFFECTIVE_BOUND_REVIEW_PASS")
    print("repair fixtures/Gram/boundary/radial/distance:", *repairs)
    print("region/flag/displayed-budget checks:", *counts)
    print("perturbation/chain/handoff checks:", *handoff)


if __name__ == "__main__":
    main()
