#!/usr/bin/env python3
"""Verify the 28-vertex K4-free 7-chromatic Cayley graph.

Only the Python standard library is used.  The non-6-colourability proof is a
finite maximum-independent-set packing argument; it does not call a SAT
solver and does not trust the program that produced the certificate.
"""

from collections import Counter
from itertools import combinations
from pathlib import Path


VERTICES = tuple((i, j) for j in range(4) for i in range(7))
INDEX = {x: k for k, x in enumerate(VERTICES)}
IDENTITY = (0, 0)
CONNECTION_SET = frozenset(
    {
        (2, 0),
        (5, 0),
        (3, 0),
        (4, 0),
        (0, 1),
        (0, 3),
        (1, 1),
        (1, 3),
        (3, 1),
        (3, 3),
        (1, 2),
        (6, 2),
    }
)

# A proper seven-colouring.  Vertex (i,j) has index 7*j+i.
SEVEN_COLOURING = (
    (0, 1, 12, 17, 26),
    (2, 3, 7, 8),
    (4, 5, 9, 14, 23),
    (6, 11, 20, 25),
    (13, 15, 16, 27),
    (10, 18, 19, 24),
    (21, 22),
)


def multiply(x, y):
    """Multiply a^i b^j and a^k b^l, where b a b^-1 = a^-1."""
    i, j = x
    k, ell = y
    return ((i + (-1 if j % 2 else 1) * k) % 7, (j + ell) % 4)


def power(x, exponent):
    answer = IDENTITY
    for _ in range(exponent):
        answer = multiply(answer, x)
    return answer


def inverse(x):
    return next(
        y
        for y in VERTICES
        if multiply(x, y) == IDENTITY and multiply(y, x) == IDENTITY
    )


def build_adjacency():
    rows = []
    for x in VERTICES:
        rows.append(sum(1 << INDEX[multiply(x, s)] for s in CONNECTION_SET))
    return tuple(rows)


ADJACENCY = build_adjacency()
ALL_VERTICES = (1 << 28) - 1


def mask(vertices):
    return sum(1 << v for v in vertices)


def is_independent(vertex_mask):
    remaining = vertex_mask
    while remaining:
        bit = remaining & -remaining
        v = bit.bit_length() - 1
        if ADJACENCY[v] & vertex_mask:
            return False
        remaining -= bit
    return True


def independent_sets(size):
    answer = []
    for vertices in combinations(range(28), size):
        candidate = mask(vertices)
        if is_independent(candidate):
            answer.append(candidate)
    return answer


def affine_automorphisms():
    """Return left translations followed by connection-set-preserving autos.

    Every group automorphism has a -> a^u and b -> a^v b^eps for the
    candidates used here.  We only retain the candidates preserving S.  The
    resulting maps are checked below, so the proof does not trust this
    parametrisation for automorphism correctness or certificate coverage.
    """
    stabilizer = []
    for u in range(1, 7):
        for v in range(7):
            for eps in (1, 3):
                image = []
                for i, j in VERTICES:
                    image.append(
                        INDEX[
                            multiply(power((u, 0), i), power((v, eps), j))
                        ]
                    )
                if {VERTICES[image[INDEX[s]]] for s in CONNECTION_SET} == set(
                    CONNECTION_SET
                ):
                    stabilizer.append(tuple(image))

    permutations = []
    for g in VERTICES:
        for phi in stabilizer:
            permutations.append(
                tuple(INDEX[multiply(g, VERTICES[phi[i]])] for i in range(28))
            )
    return tuple(stabilizer), tuple(permutations)


def permute_mask(vertex_mask, permutation):
    return sum(
        1 << permutation[v] for v in range(28) if (vertex_mask >> v) & 1
    )


def parse_certificate(path):
    records = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.partition("#")[0].strip()
        if not line:
            continue
        fields = line.split()
        if len(fields) < 5:
            raise AssertionError(f"short certificate line {line_number}")
        residual = int(fields[0], 16)
        orbit_size = int(fields[1])
        cycle = tuple(map(int, fields[2:]))
        records.append((residual, orbit_size, cycle))
    return records


def main():
    # Basic group and graph checks.
    assert len(VERTICES) == len(INDEX) == 28
    assert IDENTITY not in CONNECTION_SET
    assert {inverse(s) for s in CONNECTION_SET} == set(CONNECTION_SET)
    assert all(multiply(IDENTITY, x) == multiply(x, IDENTITY) == x for x in VERTICES)
    assert all(multiply(x, inverse(x)) == IDENTITY for x in VERTICES)
    for x in VERTICES:
        for y in VERTICES:
            for z in VERTICES:
                assert multiply(multiply(x, y), z) == multiply(x, multiply(y, z))

    assert all(row.bit_count() == 12 for row in ADJACENCY)
    assert all(not ((ADJACENCY[v] >> v) & 1) for v in range(28))
    assert all(
        ((ADJACENCY[u] >> v) & 1) == ((ADJACENCY[v] >> u) & 1)
        for u in range(28)
        for v in range(28)
    )
    edge_count = sum(row.bit_count() for row in ADJACENCY) // 2
    assert edge_count == 168

    # Left translations are transitive automorphisms.  Therefore any K4 can
    # be translated to contain the identity, and its other three vertices
    # would form a triangle in G[S].
    neighbourhood = ADJACENCY[INDEX[IDENTITY]]
    assert neighbourhood == mask(INDEX[s] for s in CONNECTION_SET)
    neighbourhood_edges = sum(
        1
        for u, v in combinations(range(28), 2)
        if (neighbourhood >> u) & 1
        and (neighbourhood >> v) & 1
        and (ADJACENCY[u] >> v) & 1
    )
    neighbourhood_triangles = sum(
        1
        for u, v, w in combinations(range(28), 3)
        if all((neighbourhood >> x) & 1 for x in (u, v, w))
        and (ADJACENCY[u] >> v) & 1
        and (ADJACENCY[u] >> w) & 1
        and (ADJACENCY[v] >> w) & 1
    )
    assert neighbourhood_edges == 24
    assert neighbourhood_triangles == 0

    # Explicit upper bound chi(G) <= 7.
    flattened = [v for colour_class in SEVEN_COLOURING for v in colour_class]
    assert sorted(flattened) == list(range(28))
    assert all(is_independent(mask(colour_class)) for colour_class in SEVEN_COLOURING)

    # Maximum independent sets and the automorphisms used for compression.
    independent_fives = independent_sets(5)
    independent_sixes = independent_sets(6)
    assert len(independent_fives) == 56
    assert not independent_sixes

    stabilizer, automorphisms = affine_automorphisms()
    assert len(stabilizer) == 2
    assert len(automorphisms) == len(set(automorphisms)) == 56
    edge_set = {
        (u, v)
        for u in range(28)
        for v in range(u + 1, 28)
        if (ADJACENCY[u] >> v) & 1
    }
    for permutation in automorphisms:
        assert sorted(permutation) == list(range(28))
        assert {
            tuple(sorted((permutation[u], permutation[v]))) for u, v in edge_set
        } == edge_set

    unseen = set(independent_fives)
    independent_orbit_sizes = []
    while unseen:
        representative = min(unseen)
        orbit = {
            permute_mask(representative, permutation)
            for permutation in automorphisms
        }
        assert orbit <= set(independent_fives)
        independent_orbit_sizes.append(len(orbit))
        unseen -= orbit
    assert sorted(independent_orbit_sizes) == [28, 28]

    # If six independent colour classes cover 28 vertices and every class has
    # size at most five, at least four classes have size five.  For every four
    # pairwise-disjoint maximum independent sets, enumerate the remaining
    # eight vertices.  A six-colouring would make that residual bipartite.
    packing_count = 0
    residuals = set()
    for a, b, c, d in combinations(independent_fives, 4):
        if a & b or a & c or a & d or b & c or b & d or c & d:
            continue
        packing_count += 1
        residuals.add(ALL_VERTICES ^ (a | b | c | d))
    assert packing_count == 1820
    assert len(residuals) == 1820

    # Check the independent odd-cycle certificate, including completeness of
    # its symmetry coverage.  The certificate is not generated by this file.
    certificate_path = Path(__file__).with_name("residual_odd_cycles.txt")
    records = parse_certificate(certificate_path)
    assert len(records) == 39
    covered = set()
    orbit_size_counts = Counter()
    for residual, claimed_orbit_size, cycle in records:
        assert residual in residuals
        assert residual.bit_count() == 8
        orbit = {
            permute_mask(residual, permutation) for permutation in automorphisms
        }
        assert orbit <= residuals
        assert residual == min(orbit)
        assert len(orbit) == claimed_orbit_size
        assert not (covered & orbit)
        covered |= orbit
        orbit_size_counts[claimed_orbit_size] += 1

        assert len(cycle) >= 3 and len(cycle) % 2 == 1
        assert len(cycle) == len(set(cycle))
        assert all(0 <= v < 28 and ((residual >> v) & 1) for v in cycle)
        assert all(
            (ADJACENCY[cycle[i]] >> cycle[(i + 1) % len(cycle)]) & 1
            for i in range(len(cycle))
        )
    assert covered == residuals
    assert orbit_size_counts == Counter({56: 26, 28: 13})

    print("vertices=28 edges=168 degree=12")
    print("neighbourhood_edges=24 neighbourhood_triangles=0 K4_free=yes")
    print("independent_5_sets=56 independent_6_sets=0 alpha=5")
    print("independent_5_orbits=2 orbit_sizes=28,28")
    print("four_class_packings=1820 distinct_residuals=1820")
    print("residual_orbits=39 orbit_sizes=13x28+26x56")
    print("every_residual_has_certified_odd_cycle=yes six_colourable=no")
    print("explicit_seven_colouring=yes chromatic_number=7")
    print("verified: K4-free 7-chromatic Cayley graph on 28 vertices")


if __name__ == "__main__":
    main()
