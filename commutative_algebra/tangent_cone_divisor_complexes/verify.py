#!/usr/bin/env python3
"""Deterministic exact internal checks and published-family comparisons."""
from collections import defaultdict
from itertools import combinations
import hashlib
import json

from betti import (absolute_complex, boundary, face_sums, fine_betti, generators,
                   graded_betti, homology, is_complex, orders, pair, report,
                   support_bound, weights)


def corpus():
    """All minimal numerical generating subsets of {2,...,11}, size 2..4.

    Add N, selected embedding dimensions 5 and 6, and published examples.
    This is a regression corpus, not a finite frontier theorem.
    """
    out = {(1,)}
    for e in range(2, 5):
        for g in combinations(range(2, 12), e):
            try:
                generators(g)
            except ValueError:
                continue
            out.add(g)
    out.update([(6, 7, 8, 9, 10, 11), (7, 9, 10, 11, 12),
                (8, 11, 13, 14, 17), (12, 15, 20, 23), (6, 7, 10)])
    out.update((a, a + 1, 2 * a + 3) for a in range(4, 16))
    return sorted(out)


def matmul_zero(a, b):
    if not a or not b:
        return True
    if len(a[0]) != len(b):
        raise AssertionError("incompatible boundary dimensions")
    return all(sum(a[i][k] * b[k][j] for k in range(len(b))) == 0
               for i in range(len(a)) for j in range(len(b[0])))


def check_topology(g, p):
    cap = support_bound(g)
    order = orders(g, cap + 2 * g[-1])
    sums = face_sums(g)
    checked = 0
    for s in range(cap + 2 * g[-1] + 1):
        w = weights(s, sums, order)
        for j in set(w.values()):
            delta, lam = pair(w, j)
            assert is_complex(delta) and is_complex(lam) and lam <= delta
            f = tuple(sorted(delta - lam))
            d = [boundary(f, i) for i in range(1, len(g) + 1)]
            assert all(matmul_zero(a, b) for a, b in zip(d, d[1:]))
            c = absolute_complex(delta, lam, len(g))
            assert is_complex(c)
            rel = homology(f, len(g), p)
            abs_h = homology(tuple(sorted(c)), len(g) + 1, p)
            assert rel == abs_h[:-1] and abs_h[-1] == 0
            if s > cap:
                assert not any(rel)
                for faces in (delta, lam):
                    assert all((f | 1) in faces for f in faces)
            checked += 1
    return checked


def check_hilbert(g, fine):
    """Check sum (-1)^i beta_ij z^j = (1-z)^e Hilb(G,z)."""
    from math import comb
    graded = graded_betti(fine)
    max_j = max(j for i, j in graded) + len(g) + 2
    # An element with order <= max_j has a maximal factorization of <= max_j
    # terms, so its value is <= max_j*max(g). This bounds this Hilbert prefix.
    order = orders(g, max_j * max(g))
    h = [sum(x == j for x in order) for j in range(max_j + 1)]
    lhs = defaultdict(int)
    for (i, j), b in graded.items():
        lhs[j] += (-1) ** i * b
    for j in range(max_j + 1):
        rhs = sum((-1) ** k * comb(len(g), k) * h[j-k]
                  for k in range(min(j, len(g)) + 1))
        assert lhs[j] == rhs, (g, j, lhs[j], rhs)


def main():
    cases = corpus()
    reports = []
    for g in cases:
        for p in (0, 2, 3):
            fine = fine_betti(g, p, extra=2 * max(g))
            check_hilbert(g, fine)
            b = report(g, p)
            assert b["total_betti"][0] == 1
            assert sum((-1) ** i * x for i, x in enumerate(b["total_betti"])) == (len(g) == 1)
            reports.append(b)
        assert reports[-1]["graded_betti"] == reports[-2]["graded_betti"] == reports[-3]["graded_betti"]
    for a in range(4, 16):
        k = (a - 1) // 3
        assert report((a, a + 1, 2 * a + 3))["total_betti"] == [1, k + 3, 2*k + 2, k]
    assert report((3, 5))["graded_betti"] == [[0, 0, 1], [1, 3, 1]]
    assert report((6, 7, 10))["total_betti"] == [1, 3, 2, 0]
    assert report((12, 15, 20, 23))["total_betti"] == [1, 8, 12, 5, 0]
    selected = [(1,), (3, 5), (6, 7, 15), (6, 7, 10),
                (8, 9, 19), (5, 6, 7, 8, 9), (6, 7, 8, 9, 10, 11)]
    topology_checks = sum(check_topology(g, p) for g in selected for p in (0, 2, 3))
    for bad in [(), (0,), (2, 4), (4, 6), (5, 3), (2, 3, 4)]:
        try:
            generators(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid generating set accepted: {bad}")
    canonical = json.dumps(reports, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps({"semigroups": len(cases), "characteristics": [0, 2, 3],
                      "tables": len(reports), "topological_strands": topology_checks,
                      "report_sha256": hashlib.sha256(canonical).hexdigest(),
                      "checks": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
