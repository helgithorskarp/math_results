#!/usr/bin/env python3
"""Independent exact census for the Parts-159 fixed-origin pencil.

No implementation module from the reviewed artifact is imported.  Arithmetic
uses E=Q(sqrt(33))[alpha]/(alpha^2+3) as nested rational pairs, and groups
cross edges by independently computed monic quadratic coefficients.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations
from math import isqrt
from pathlib import Path


R_ZERO = (Q(0), Q(0))
R_ONE = (Q(1), Q(0))
E_ZERO = (R_ZERO, R_ZERO)


def r_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def r_neg(a):
    return -a[0], -a[1]


def r_mul(a, b):
    return a[0] * b[0] + 33 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def r_scale(a, q):
    return a[0] * q, a[1] * q


def r_inv(a):
    denominator = a[0] * a[0] - 33 * a[1] * a[1]
    if not denominator:
        raise ZeroDivisionError
    return a[0] / denominator, -a[1] / denominator


def e_add(a, b):
    return r_add(a[0], b[0]), r_add(a[1], b[1])


def e_neg(a):
    return r_neg(a[0]), r_neg(a[1])


def e_mul(a, b):
    # alpha^2=-3.
    real = r_add(r_mul(a[0], b[0]), r_scale(r_mul(a[1], b[1]), -3))
    imaginary = r_add(r_mul(a[0], b[1]), r_mul(a[1], b[0]))
    return real, imaginary


def e_conj(a):
    return a[0], r_neg(a[1])


def e_from_r(a):
    return a, R_ZERO


def e_norm(a):
    return r_add(r_mul(a[0], a[0]), r_scale(r_mul(a[1], a[1]), 3))


def e_inv(a):
    return e_mul(e_conj(a), e_from_r(r_inv(e_norm(a))))


def e_div(a, b):
    return e_mul(a, e_inv(b))


def rational_square_root(q):
    if q < 0:
        return None
    numerator, denominator = isqrt(q.numerator), isqrt(q.denominator)
    if numerator * numerator == q.numerator and denominator * denominator == q.denominator:
        return Q(numerator, denominator)
    return None


def r_sign(a):
    x, y = a
    if not y:
        return (x > 0) - (x < 0)
    if not x:
        return (y > 0) - (y < 0)
    if (x > 0) == (y > 0):
        return (x > 0) - (x < 0)
    comparison = x * x - 33 * y * y
    assert comparison
    return ((x > 0) - (x < 0)) * ((comparison > 0) - (comparison < 0))


def r_is_square(a):
    x, y = a
    if not y:
        return rational_square_root(x) is not None or rational_square_root(x / 33) is not None
    norm_root = rational_square_root(x * x - 33 * y * y)
    if norm_root is None:
        return False
    for sign in (-1, 1):
        first = rational_square_root((x + sign * norm_root) / 2)
        if first is not None and first:
            second = y / (2 * first)
            if r_mul((first, second), (first, second)) == a:
                return True
    return False


def read_points(path):
    points = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        assert len(row) == 16
        assert all(row[i] == 0 for i in range(16) if i not in (0, 5, 9, 12))
        # Original basis: 1, sqrt(33), alpha, i*sqrt(11)=alpha*sqrt(33)/3.
        points.append(((Q(row[0], 12), Q(row[5], 12)),
                       (Q(row[9], 12), Q(row[12], 36))))
    assert len(points) == len(set(points)) == 159 and points[0] == E_ZERO
    return points


def strict_edges(points):
    return [(i, j) for i, j in combinations(range(len(points)), 2)
            if e_norm(e_add(points[i], e_neg(points[j]))) == R_ONE]


def pencil(points, reflected, classification_hash):
    image = [e_conj(point) for point in points] if reflected else points
    norms = [e_norm(point) for point in points]
    groups = defaultdict(list)
    counts = Counter()
    for i in range(1, 159):
        for j in range(1, 159):
            s = r_add(r_add(norms[i], norms[j]), (-Q(1), Q(0)))
            delta = r_add(r_scale(r_mul(norms[i], norms[j]), 4), r_neg(r_mul(s, s)))
            sign = r_sign(delta)
            if sign < 0:
                label = "no_unit_roots"
            elif r_is_square(r_scale(delta, Q(1, 3))):
                label = "roots_in_E"
            else:
                assert sign > 0
                label = "outside_E_pairs"
                c = e_mul(e_conj(points[i]), image[j])
                key = (e_div(e_from_r(s), c), e_div(e_conj(c), c))
                groups[key].append((i, j))
            counts[label] += 1
            classification_hash.update(f"{int(reflected)}:{i},{j}:{label}\n".encode("ascii"))
    return counts, groups


def main():
    here = Path(__file__).resolve().parent
    points_path = here.parent / "hadwiger_nelson_nonmono159_214_lowden2/points159.tsv"
    library_path = here.parent / "hadwiger_nelson_nonmono159_origin_pencil/colorings.txt"
    points = read_points(points_path)
    edges = strict_edges(points)
    assert len(edges) == 646
    library = [tuple(map(int, line)) for line in library_path.read_text().splitlines()]
    assert len(library) == 4
    assert all(len(colors) == 159 and colors[0] == 0 and
               all(color in range(4) for color in colors) and
               all(colors[i] != colors[j] for i, j in edges) for colors in library)
    color_permutations = [(0,) + tail for tail in permutations((1, 2, 3))]

    classification_hash = sha256()
    partition_hash = sha256()
    witness_hash = sha256()
    distinct_edge_sets = set()
    total_classes = 0
    summaries = []
    for reflected in (False, True):
        counts, groups = pencil(points, reflected, classification_hash)
        for edge_set in sorted(tuple(sorted(value)) for value in groups.values()):
            partition_hash.update((f"{int(reflected)}:" +
                                   ";".join(f"{i},{j}" for i, j in edge_set) + "\n").encode("ascii"))
        histogram = Counter(map(len, groups.values()))
        witness_counts = Counter()
        for edge_set in groups.values():
            canonical_edges = tuple(sorted(edge_set))
            witness = next((
                (left, right, p_index)
                for left, left_colors in enumerate(library)
                for right, right_colors in enumerate(library)
                for p_index, p in enumerate(color_permutations)
                if all(left_colors[i] != p[right_colors[j]] for i, j in canonical_edges)
            ), None)
            assert witness is not None
            witness_counts[witness] += 1
            witness_hash.update((f"{int(reflected)}:{canonical_edges}:{witness}\n").encode("ascii"))
            distinct_edge_sets.add(canonical_edges)
        assert sum(size * count for size, count in histogram.items()) == counts["outside_E_pairs"]
        summaries.append((int(reflected), counts, len(groups), histogram, witness_counts))
        total_classes += len(groups)

    expected_counts = {"no_unit_roots": 2937, "roots_in_E": 12906,
                       "outside_E_pairs": 9121}
    assert all(dict(counts) == expected_counts for _, counts, _, _, _ in summaries)
    assert [classes for _, _, classes, _, _ in summaries] == [1490, 1377]
    assert total_classes == 2867 and len(distinct_edge_sets) == 2866
    assert classification_hash.hexdigest() == "d5b57453f3184f7cc337a895b4ea67bd94071abbb131ff0309ac4ba1abd1fdfc"
    assert partition_hash.hexdigest() == "9c01c9e8419cce17660e32a3a683908b69900f8415c3df1be2e4a47d00fe8a70"

    print("component=159,646 library=4")
    for reflected, counts, classes, histogram, witness_counts in summaries:
        rendered = ",".join(f"{size}:{count}" for size, count in sorted(histogram.items()))
        print(f"parity={reflected} pairs={sum(counts.values())} negative={counts['no_unit_roots']} "
              f"in_field={counts['roots_in_E']} outside_pairs={counts['outside_E_pairs']} "
              f"classes={classes} histogram={rendered} witness_types={len(witness_counts)}")
    print(f"classes_total={total_classes} isometries={2*total_classes} "
          f"distinct_edge_sets={len(distinct_edge_sets)} classification_sha256={classification_hash.hexdigest()}")
    print(f"edge_partition_sha256={partition_hash.hexdigest()} witness_sha256={witness_hash.hexdigest()}")
    print("independent_origin_pencil_census=true")


if __name__ == "__main__":
    main()
