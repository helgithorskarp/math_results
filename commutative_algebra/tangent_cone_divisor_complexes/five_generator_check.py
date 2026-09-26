#!/usr/bin/env python3
"""Exact checks for FIVE_GENERATORS.md. Python >=3.11, standard library only.

The six-vertex classification is an external mathematical theorem, not proved
by this script. No finite corpus establishes the universal semigroup theorem.
"""
import argparse
import hashlib
from itertools import combinations, permutations
import json

from betti import (absolute_complex, boundary, fine_betti, generators,
                   homology, is_complex, rank)


def closure(facets):
    faces = set()
    for f in facets:
        sub = f
        while True:
            faces.add(sub)
            if not sub:
                break
            sub = (sub - 1) & f
    return frozenset(faces)


def mask(vertices):
    return sum(1 << v for v in vertices)


def determinant(a):
    """Small integer determinant by the Leibniz formula, without elimination."""
    n = len(a)
    assert all(len(row) == n for row in a)
    answer = 0
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        term = (-1) ** inversions
        for i, col in enumerate(perm):
            term *= a[i][col]
        answer += term
    return answer


def topology_checks():
    cycle = [(v, (v + 1) % 5) for v in range(5)]
    triangles = [(0, 1, 3), (0, 2, 3), (0, 2, 4), (1, 2, 4), (1, 3, 4)]
    d = closure(map(mask, triangles))
    l = closure(map(mask, cycle))
    rp2 = absolute_complex(d, l, 5)
    assert is_complex(rp2)
    assert [sum(f.bit_count() == i for f in rp2) for i in range(1, 4)] == [6, 15, 10]
    assert homology(tuple(sorted(rp2)), 6, 0) == (0, 0, 0, 0, 0, 0, 0)
    assert homology(tuple(sorted(rp2)), 6, 2) == (0, 0, 1, 1, 0, 0, 0)
    assert homology(tuple(sorted(rp2)), 6, 3) == (0, 0, 0, 0, 0, 0, 0)
    partitions = 0
    for apex in range(6):
        vertex = 1 << apex
        ground = 63 ^ vertex
        deletion = frozenset(f for f in rp2 if not f & vertex)
        link = frozenset(f ^ vertex for f in rp2 if f & vertex)
        edges = {f for f in link if f.bit_count() == 2}
        tris = {f for f in deletion if f.bit_count() == 3}
        assert len(edges) == len(tris) == 5
        assert max(map(int.bit_count, link)) == 2
        assert max(map(int.bit_count, deletion)) == 3
        # A simple 2-regular graph on five vertices is necessarily a five-cycle.
        for v in range(6):
            if v != apex:
                assert sum(bool(edge & (1 << v)) for edge in edges) == 2
        all_pairs = {f for f in range(64) if not f & vertex and f.bit_count() == 2}
        assert tris == {ground ^ edge for edge in all_pairs - edges}
        # This relative complex really has 2-torsion: its only boundary is a
        # 5x5 matrix of determinant +/-2. It cannot be discarded on size alone.
        relative = tuple(sorted(deletion - link))
        matrix = boundary(relative, 3)
        assert len(matrix) == 5 and all(len(row) == 5 for row in matrix)
        assert abs(determinant(matrix)) == 2
        assert [rank(matrix, p) for p in (0, 2, 3)] == [5, 4, 5]
        assert homology(relative, 6, 0) == (0, 0, 0, 0, 0, 0, 0)
        assert homology(relative, 6, 2) == (0, 0, 1, 1, 0, 0, 0)
        # U is the strict-low set a_v < b/j. Every link edge must meet U,
        # while a length-j factorization forbids a deletion triangle in U.
        for low in range(64):
            if low & vertex:
                continue
            covers_edges = all(edge & low for edge in edges)
            avoids_triangles = all(tri & low != tri for tri in tris)
            assert not (covers_edges and avoids_triangles)
            partitions += 1
    assert partitions == 192
    return {"projective_plane_apices": 6, "threshold_partitions": partitions,
            "torsion_positive_control": "PASS"}


def five_generator_corpus():
    result = []
    for g in combinations(range(5, 16), 5):
        try:
            generators(g)
        except ValueError:
            continue
        result.append(g)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--singular", help="also check every fine entry using this Singular executable")
    args = parser.parse_args()
    summary = topology_checks()
    corpus = five_generator_corpus()
    assert len(corpus) == 109
    records = []
    noncm = []
    for g in corpus:
        tables = [fine_betti(g, p) for p in (0, 2, 3)]
        assert tables[0] == tables[1] == tables[2], g
        if any(i == 5 for i, s, j in tables[0]):
            noncm.append(g)
        for p, fine in zip((0, 2, 3), tables):
            records.append([list(g), p, [[i, s, j, b] for (i, s, j), b in sorted(fine.items())]])
    assert noncm == [(6, 7, 10, 11, 15), (8, 9, 13, 14, 15)]
    canonical = json.dumps(records, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    summary.update({"semigroups": len(corpus), "non_Cohen_Macaulay": len(noncm),
                    "tables": len(records), "tables_sha256": digest, "checks": "PASS"})
    if args.singular:
        from singular_check import check_cases
        cases = [(g, p) for g in corpus for p in (0, 2, 3)]
        independent = check_cases(cases, args.singular)
        assert independent["tables_sha256"] == digest
        summary["singular_fine_entrywise_matches"] = independent["fine_entrywise_matches"]
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
