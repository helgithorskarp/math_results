#!/usr/bin/env python3
"""Audit all global quantities on a physical graph; conditional Ramsey bounds."""
import argparse
import itertools as it
import json
from collections import Counter
from pathlib import Path


def read_graph(path):
    rows = [list(map(int, line.split())) for line in path.read_text().splitlines()]
    if not rows or len(rows[0]) != 2:
        raise ValueError("expected n m header")
    n, m = rows[0]
    if not 1 <= n <= 63 or m < 0 or len(rows) != m + 1:
        raise ValueError("invalid dimensions")
    a = [0] * n
    seen = set()
    for row in rows[1:]:
        if len(row) != 2:
            raise ValueError("invalid edge row")
        i, j = row
        if not 0 <= i < j < n or (i, j) in seen:
            raise ValueError("invalid or duplicate edge")
        seen.add((i, j))
        a[i] |= 1 << j
        a[j] |= 1 << i
    return a


def validate(a):
    n = len(a)
    if not 1 <= n <= 63 or any(type(x) is not int or x < 0 or x >> n for x in a):
        raise ValueError("invalid adjacency")
    if any(a[i] >> i & 1 for i in range(n)) or any(
            ((a[i] >> j) ^ (a[j] >> i)) & 1 for i, j in it.combinations(range(n), 2)):
        raise ValueError("loops or asymmetric adjacency")


def pentagons(a, mask):
    vertices = [i for i in range(len(a)) if mask >> i & 1]
    for s in it.combinations(vertices, 5):
        sm = sum(1 << i for i in s)
        if all((a[i] & sm).bit_count() == 2 for i in s):
            yield sm


def has_clique(a, mask, size):
    if not size:
        return True
    while mask.bit_count() >= size:
        bit = mask & -mask
        mask ^= bit
        if has_clique(a, mask & a[bit.bit_length() - 1], size - 1):
            return True
    return False


def audit(a):
    validate(a)
    n = len(a)
    full = (1 << n) - 1
    blue = [full ^ (1 << i) ^ a[i] for i in range(n)]
    good = not has_clique(a, full, 5) and not has_clique(blue, full, 5)
    d = [x.bit_count() for x in a]
    qhist = Counter()
    pair_first = 0
    for i, j in it.combinations(range(n), 2):
        color = a if a[i] >> j & 1 else blue
        common = color[i] & color[j]
        q = common.bit_count()
        qhist[q] += 1
        # Induced pentagons are invariant under color reversal.
        pair_first += sum(1 for _ in pentagons(a, common))
    p = 0
    cycle_first = 0
    homogeneous = 0
    max_multiplicity = 0
    for sm in pentagons(a, full):
        p += 1
        multiplicity = 0
        for color in (a, blue):
            u = full ^ sm
            for v in range(n):
                if sm >> v & 1:
                    u &= color[v]
            homogeneous += u.bit_count()
            multiplicity += sum((color[v] & u).bit_count()
                                for v in range(n) if u >> v & 1) // 2
        max_multiplicity = max(max_multiplicity, multiplicity)
        cycle_first += multiplicity
    delta4 = sum((2 * degree - (n - 1)) ** 2 for degree in d)
    triangles = sum(1 for s in it.combinations(range(n), 3)
                    if len({(a[i] >> j) & 1 for i, j in it.combinations(s, 2)}) == 1)
    if pair_first != cycle_first:
        raise ValueError("incidence identity failed")
    if sum(q * count for q, count in qhist.items()) != 3 * triangles:
        raise ValueError("triangle incidence failed")
    if 24 * triangles != n * (n - 1) * (n - 5) + 3 * delta4:
        raise ValueError("Goodman identity failed")
    lower = [0] * 10 + [2, 4, 7, 12]
    result = {"n": n, "edges": sum(d) // 2, "ramsey_5_5": good,
              "pentagons": p, "edge_pentagon_incidences": pair_first,
              "homogeneous_vertex_pentagon_incidences": homogeneous,
              "largest_pentagon_multiplicity": max_multiplicity,
              "q_histogram": {str(k): v for k, v in sorted(qhist.items())},
              "monochromatic_triangles": triangles, "degree_delta4": delta4}
    if good:
        if max(qhist, default=0) > 13:
            raise ValueError("common-neighbor order bound failed")
        local_sum = sum(lower[q] * count for q, count in qhist.items())
        base4 = n * (n - 1) * (n - 41) + 3 * delta4
        slack = sum((lower[q] - 2 * (q - 9)) * count for q, count in qhist.items())
        if 4 * local_sum != base4 + 4 * slack or pair_first < local_sum:
            raise ValueError("global lower bound failed")
        if pair_first > 2 * homogeneous or homogeneous > 26 * p:
            raise ValueError("global upper bound failed")
        result.update({"sum_local_bounds": local_sum, "global_slack": slack,
                       "global_base_times4": base4})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(read_graph(args.graph)), sort_keys=True))
